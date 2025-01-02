
#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import torch 
import torch.nn as nn
import numpy as np
import os 
import sys
import librosa

def read_and_config_file(args, input_path, decode=0):
    """
    Reads and processes the input file or directory to extract audio file paths or configuration data.
    
    Parameters:
    args: The args
    input_path (str): Path to a file or directory containing audio data or file paths.
    decode (bool): If True (decode=1) for decoding, process the input as audio files directly (find .wav or .flac files) or from a .scp file.
                   If False (decode=0) for training, assume the input file contains lines with paths to audio files.
    
    Returns:
    processed_list (list): A list of processed file paths or a list of dictionaries containing input 
                           and optional condition audio paths.
    """
    processed_list = []  # Initialize list to hold processed file paths or configurations

    if decode:
        if args.task == 'target_speaker_extraction':
            if args.network_reference.cue== 'lip':
                # If decode is True, find video files in a directory or single file
                if os.path.isdir(input_path):
                    # Find all .mp4 , mov .avi files in the input directory
                    processed_list = librosa.util.find_files(input_path, ext="mp4")
                    processed_list += librosa.util.find_files(input_path, ext="avi")
                    processed_list += librosa.util.find_files(input_path, ext="mov")
                    processed_list += librosa.util.find_files(input_path, ext="MOV")
                    processed_list += librosa.util.find_files(input_path, ext="webm")
                else:
                    # If it's a single file and it's a .wav or .flac, add to processed list
                    if input_path.lower().endswith(".mp4") or input_path.lower().endswith(".avi") or input_path.lower().endswith(".mov") or input_path.lower().endswith(".webm"):
                        processed_list.append(input_path)
                    else:
                        # Read file paths from the input text file (one path per line)
                        with open(input_path) as fid:
                            for line in fid:
                                path_s = line.strip().split()  # Split paths (space-separated)
                                processed_list.append(path_s[0])  # Add the first path (input audio path)
                return processed_list

        # If decode is True, find audio files in a directory or single file
        if os.path.isdir(input_path):
            # Find all .wav files in the input directory
            processed_list = librosa.util.find_files(input_path, ext="wav")
            if len(processed_list) == 0:
                # If no .wav files, look for .flac files
                processed_list = librosa.util.find_files(input_path, ext="flac")
        else:
            # If it's a single file and it's a .wav or .flac, add to processed list
            if input_path.lower().endswith(".wav") or input_path.lower().endswith(".flac"):
                processed_list.append(input_path)
            else:
                # Read file paths from the input text file (one path per line)
                with open(input_path) as fid:
                    for line in fid:
                        path_s = line.strip().split()  # Split paths (space-separated)
                        processed_list.append(path_s[0])  # Add the first path (input audio path)
        return processed_list

    # If decode is False, treat the input file as a configuration file
    with open(input_path) as fid:
        for line in fid:
            tmp_paths = line.strip().split()  # Split paths (space-separated)
            if len(tmp_paths) == 2:
                # If two paths per line, treat the second as 'condition_audio'
                sample = {'inputs': tmp_paths[0], 'condition_audio': tmp_paths[1]}
            elif len(tmp_paths) == 1:
                # If only one path per line, treat it as 'inputs'
                sample = {'inputs': tmp_paths[0]}
            processed_list.append(sample)  # Append processed sample to list
    return processed_list

