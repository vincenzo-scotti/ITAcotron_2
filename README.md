# ITAcotron 2

Codebase for the paper "[ITAcotron 2: Transfering English Speech Synthesis Architectures and Speech Features to Italian]()".
For all the references, contributions and credits, please refer to the paper.

This code was originally developed as part of the M.Sc. Thesis in Cognitive Science "[Conditional Text to Speech by Means of Transfer Learning]()".
The M.Sc. degree was released by the Center for Mind/Brain Sciences ([CIMeC](https://www.cimec.unitn.it)) of the Università degli Studi di Trento ([UniTn](https://www.unitn.it)).
The Thesis was supervised at Politecnico di Milano ([PoliMI](https://www.polimi.it)) by the staff of the [ARCSlab](https://arcslab.dei.polimi.it).

## Usage

## Model weights

Link to download the weights of the trained models:
- Tacotron 2 [[link]()] (trained on Italian data)
- FB-MelGAN Vocoder [[link]()] (taken from the original repo, trained on English data)
- Speaker Encoder [[link]()] (taken from the original repo, trained on English data)

## Changes from origin

The code in this repository is based on a fork of the [Mozilla TTS repository](https://github.com/mozilla/TTS).
Please refer to the source for the documentation.

With respect to the original implementation, we modified the following files:
- `TTS/tts/datasets/preprocess.py`
- `TTS/tts/datasets/TTSDataset.py`
- `path/to/file`
- `path/to/file`
- `path/to/file`

The code was taken from [this commit](https://github.com/mozilla/TTS/tree/2136433).

## Cite work

If you are willing to use our code, please cite our work through the following BibTeX entry:
```latex
``` 

## Acknowledgments

We wish to thank all the contributors to the "[TTS: Text-to-Speech for all](https://github.com/mozilla/TTS)" repository for their help. 
