# ITAcotron 2

Codebase for the paper "[ITAcotron 2: Transfering English Speech Synthesis Architectures and Speech Features to Italian](https://aclanthology.org/2021.icnlsp-1.10/)".
For all the references, contributions and credits, please refer to the paper.

This code was originally developed as part of the M.Sc. Thesis in Cognitive Science "[Conditional Text to Speech by Means of Transfer Learning]()".
The M.Sc. degree was released by the Center for Mind/Brain Sciences ([CIMeC](https://www.cimec.unitn.it)) of the Università degli Studi di Trento ([UniTn](https://www.unitn.it)).
The Thesis was supervised at Politecnico di Milano ([PoliMI](https://www.polimi.it)) by the staff of the [ARCSlab](https://arcslab.dei.polimi.it).

## Usage 

To generate Italian clips, you can use the notebook at the following path: `notebooks/ITAcotron-2_synthesis.ipynb`

## Model weights

Link to download the weights of the trained models:
- Tacotron 2 [ [link](https://polimi365-my.sharepoint.com/:u:/g/personal/10451445_polimi_it/EaVCldj6tN5FqrUxdIT3wx8BE4wM5m6juQotK6qAc5pDxw?e=O2hMpn) ] (trained on Italian data)
- FB-MelGAN Vocoder [ [link](https://polimi365-my.sharepoint.com/:u:/g/personal/10451445_polimi_it/EVPp9Olk8Y5PkxyN1URudC4Bxp8K6v6Ct1_05uk54z0NfA?e=NLKLdd) ] and vocoder configuration file [ [link](https://polimi365-my.sharepoint.com/:u:/g/personal/10451445_polimi_it/EWcY4y3ZZYVDnWifqmjjbooBv4gMNSwRulG0rgwTIuq6Zw?e=rCoEXC) ] (taken from the original repo, trained on English data)
- Speaker Encoder [ [link](https://polimi365-my.sharepoint.com/:u:/g/personal/10451445_polimi_it/EcXCpALD4_FIiAYBu-MugoIBj2oIBhkBjT0jM5kD6XlBCg?e=ziwVIl) ] and speaker encoder configuration file [ [link](https://polimi365-my.sharepoint.com/:u:/g/personal/10451445_polimi_it/ESdU__SvK-RMpC8C72lLwswBPS9udG3zW4j__bifBs1rcw?e=Id23Rd) ] (taken from the original repo, trained on English data)

## Changes from origin

The code in this repository is based on a fork of the [Mozilla TTS repository](https://github.com/mozilla/TTS).
Please refer to the source for the documentation.

With respect to the original implementation, we modified the following files:
- `TTS/tts/datasets/preprocess.py`
- `TTS/tts/datasets/TTSDataset.py`
- `TTS/tts/utils/text/__init__.py`
- `TTS/tts/utils/text/cleaners.py`
- `TTS/tts/utils/text/symbols.py`
- `TTS/bin/train_tacotron.py`

The code was taken from [this commit](https://github.com/mozilla/TTS/tree/2136433).

## Added configurations 

Configuration files added for the training of Italian TTS: 
- `TTS/tts/configs/config_first_finetuning.json`
- `TTS/tts/configs/config_second_finetuning.json`

## Cite work

If you are willing to use our code, please cite our work through the following BibTeX entry:
```latex
@inproceedings{favaro-etal-2021-itacotron,
    title = "{ITA}cotron 2: Transfering {E}nglish Speech Synthesis Architectures and Speech Features to {I}talian",
    author = "Favaro, Anna  and
      Sbattella, Licia  and
      Tedesco, Roberto  and
      Scotti, Vincenzo",
    booktitle = "Proceedings of The Fourth International Conference on Natural Language and Speech Processing (ICNLSP 2021)",
    month = "12--13 " # nov,
    year = "2021",
    address = "Trento, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.icnlsp-1.10",
    pages = "83--88",
}
``` 

## Acknowledgments

We wish to thank all the contributors to the "[TTS: Text-to-Speech for all](https://github.com/mozilla/TTS)" repository for their help. 
