#!/usr/bin/env python
# coding: utf-8

import os
from glob import glob
import re
import sys
from pathlib import Path

from TTS.utils.io import  load_config
from tqdm import tqdm
import pandas as pd
from TTS.tts.utils.generic_utils import split_dataset
from TTS.utils.io import load_config



####################
# UTILITIES
####################

def load_meta_data(datasets, eval_split=True):
    meta_data_train_all = []
    meta_data_eval_all = [] if eval_split else None
    for dataset in datasets:
        name = dataset['name']
        root_path = dataset['path']
        meta_file_train = dataset['meta_file_train']
        meta_file_val = dataset['meta_file_val']
        # setup the right data processor
        preprocessor = get_preprocessor_by_name(name)
        # load train set
        meta_data_train = preprocessor(root_path, meta_file_train)
        print(f" | > Found {len(meta_data_train)} files in {Path(root_path).resolve()}")
        # load evaluation split if set
        if eval_split:
            if meta_file_val is None:
                meta_data_eval, meta_data_train = split_dataset(meta_data_train)
            else:
                meta_data_eval = preprocessor(root_path, meta_file_val)
            meta_data_eval_all += meta_data_eval
        meta_data_train_all += meta_data_train
        
        # load attention masks for duration predictor training
        if 'meta_file_attn_mask' in dataset:
            meta_data = dict(load_attention_mask_meta_data(dataset['meta_file_attn_mask']))
            for idx, ins in enumerate(meta_data_train_all):
                attn_file = meta_data[ins[1]].strip()
                meta_data_train_all[idx].append(attn_file)
            if meta_data_eval_all is not None:
                for idx, ins in enumerate(meta_data_eval_all):
                    attn_file = meta_data[ins[1]].strip()
                    meta_data_eval_all[idx].append(attn_file)
    return meta_data_train_all, meta_data_eval_all


def load_attention_mask_meta_data(metafile_path):
    """Load meta data file created by compute_attention_masks.py"""
    with open(metafile_path, 'r') as f:
        lines = f.readlines()

    meta_data = []
    for line in lines:
        wav_file, attn_file = line.split('|')
        meta_data.append([wav_file, attn_file])
    return meta_data


def get_preprocessor_by_name(name):
    """Returns the respective preprocessing function."""
    thismodule = sys.modules[__name__]
    return getattr(thismodule, name.lower())


########################
# DATASETS
########################

def my_data(root_path, meta_file):
    """Normalize the common voice meta data file to TTS format."""

    items = []

    txt_file = os.path.join(root_path, meta_file)
    tts_data = pd.read_csv(txt_file, encoding = "utf-8-sig") #apro il mio csv as a dataframe
    sentences = list(tts_data.sentence.dropna())
    speaker = list(tts_data.client_id.dropna())
        #dataset = list(tts_data.dataset)
    wav = list(tts_data.path.dropna())

    for i, j, c in zip(sentences, wav, speaker):
        items.append([i, os.path.join(root_path, j), c])

    return items







