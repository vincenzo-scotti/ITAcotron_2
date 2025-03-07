import numpy as np
import torch
from torch import nn
from torch.nn.utils import weight_norm

from ..layers.wavegrad import DBlock, FiLM, UBlock, Conv1d


class Wavegrad(nn.Module):
    # pylint: disable=dangerous-default-value
    def __init__(self,
                 in_channels=80,
                 out_channels=1,
                 use_weight_norm=False,
                 y_conv_channels=32,
                 x_conv_channels=768,
                 dblock_out_channels=[128, 128, 256, 512],
                 ublock_out_channels=[512, 512, 256, 128, 128],
                 upsample_factors=[5, 5, 3, 2, 2],
                 upsample_dilations=[[1, 2, 1, 2], [1, 2, 1, 2], [1, 2, 4, 8],
                                     [1, 2, 4, 8], [1, 2, 4, 8]]):
        super().__init__()

        self.use_weight_norm = use_weight_norm
        self.hop_len = np.prod(upsample_factors)
        self.noise_level = None
        self.num_steps = None
        self.beta = None
        self.alpha = None
        self.alpha_hat = None
        self.noise_level = None
        self.c1 = None
        self.c2 = None
        self.sigma = None

        # dblocks
        self.y_conv = Conv1d(1, y_conv_channels, 5, padding=2)
        self.dblocks = nn.ModuleList([])
        ic = y_conv_channels
        for oc, df in zip(dblock_out_channels, reversed(upsample_factors)):
            self.dblocks.append(DBlock(ic, oc, df))
            ic = oc

        # film
        self.film = nn.ModuleList([])
        ic = y_conv_channels
        for oc in reversed(ublock_out_channels):
            self.film.append(FiLM(ic, oc))
            ic = oc

        # ublocks
        self.ublocks = nn.ModuleList([])
        ic = x_conv_channels
        for oc, uf, ud in zip(ublock_out_channels, upsample_factors, upsample_dilations):
            self.ublocks.append(UBlock(ic, oc, uf, ud))
            ic = oc

        self.x_conv = Conv1d(in_channels, x_conv_channels, 3, padding=1)
        self.out_conv = Conv1d(oc, out_channels, 3, padding=1)

        if use_weight_norm:
            self.apply_weight_norm()

    def forward(self, x, spectrogram, noise_scale):
        shift_and_scale = []

        x = self.y_conv(x)
        shift_and_scale.append(self.film[0](x, noise_scale))

        for film, layer in zip(self.film[1:], self.dblocks):
            x = layer(x)
            shift_and_scale.append(film(x, noise_scale))

        x = self.x_conv(spectrogram)
        for layer, (film_shift, film_scale) in zip(self.ublocks,
                                                   reversed(shift_and_scale)):
            x = layer(x, film_shift, film_scale)
        x = self.out_conv(x)
        return x

    def load_noise_schedule(self, path):
        sched = np.load(path, allow_pickle=True).item()
        self.compute_noise_level(**sched)

    @torch.no_grad()
    def inference(self, x, y_n=None):
        """ x: B x D X T """
        if y_n is None:
            y_n = torch.randn(x.shape[0], 1, self.hop_len * x.shape[-1], dtype=torch.float32).to(x)
        else:
            y_n = torch.FloatTensor(y_n).unsqueeze(0).unsqueeze(0).to(x)
        sqrt_alpha_hat = self.noise_level.to(x)
        for n in range(len(self.alpha) - 1, -1, -1):
            y_n = self.c1[n] * (y_n -
                        self.c2[n] * self.forward(y_n, x, sqrt_alpha_hat[n].repeat(x.shape[0])))
            if n > 0:
                z = torch.randn_like(y_n)
                y_n += self.sigma[n - 1] * z
            y_n.clamp_(-1.0, 1.0)
        return y_n


    def compute_y_n(self, y_0):
        """Compute noisy audio based on noise schedule"""
        self.noise_level = self.noise_level.to(y_0)
        if len(y_0.shape) == 3:
            y_0 = y_0.squeeze(1)
        s = torch.randint(1, self.num_steps + 1, [y_0.shape[0]])
        l_a, l_b = self.noise_level[s-1], self.noise_level[s]
        noise_scale = l_a + torch.rand(y_0.shape[0]).to(y_0) * (l_b - l_a)
        noise_scale = noise_scale.unsqueeze(1)
        noise = torch.randn_like(y_0)
        noisy_audio = noise_scale * y_0 + (1.0 - noise_scale**2)**0.5 * noise
        return noise.unsqueeze(1), noisy_audio.unsqueeze(1), noise_scale[:, 0]

    def compute_noise_level(self, num_steps, min_val, max_val, base_vals=None):
        """Compute noise schedule parameters"""
        beta = np.linspace(min_val, max_val, num_steps)
        if base_vals is not None:
            beta *= base_vals
        alpha = 1 - beta
        alpha_hat = np.cumprod(alpha)
        noise_level = np.concatenate([[1.0], alpha_hat ** 0.5], axis=0)

        self.num_steps = num_steps
        # pylint: disable=not-callable
        self.beta = torch.tensor(beta.astype(np.float32))
        self.alpha = torch.tensor(alpha.astype(np.float32))
        self.alpha_hat = torch.tensor(alpha_hat.astype(np.float32))
        self.noise_level = torch.tensor(noise_level.astype(np.float32))

        self.c1 = 1 / self.alpha**0.5
        self.c2 = (1 - self.alpha) / (1 - self.alpha_hat)**0.5
        self.sigma = ((1.0 - self.alpha_hat[:-1]) / (1.0 - self.alpha_hat[1:]) * self.beta[1:])**0.5

    def remove_weight_norm(self):
        for _, layer in enumerate(self.dblocks):
            if len(layer.state_dict()) != 0:
                try:
                    nn.utils.remove_weight_norm(layer)
                except ValueError:
                    layer.remove_weight_norm()

        for _, layer in enumerate(self.film):
            if len(layer.state_dict()) != 0:
                try:
                    nn.utils.remove_weight_norm(layer)
                except ValueError:
                    layer.remove_weight_norm()


        for _, layer in enumerate(self.ublocks):
            if len(layer.state_dict()) != 0:
                try:
                    nn.utils.remove_weight_norm(layer)
                except ValueError:
                    layer.remove_weight_norm()

        nn.utils.remove_weight_norm(self.x_conv)
        nn.utils.remove_weight_norm(self.out_conv)
        nn.utils.remove_weight_norm(self.y_conv)

    def apply_weight_norm(self):
        for _, layer in enumerate(self.dblocks):
            if len(layer.state_dict()) != 0:
                layer.apply_weight_norm()

        for _, layer in enumerate(self.film):
            if len(layer.state_dict()) != 0:
                layer.apply_weight_norm()


        for _, layer in enumerate(self.ublocks):
            if len(layer.state_dict()) != 0:
                layer.apply_weight_norm()

        self.x_conv = weight_norm(self.x_conv)
        self.out_conv = weight_norm(self.out_conv)
        self.y_conv = weight_norm(self.y_conv)
