# ClearerVoice Denoiser
## What this is about
This is a Containerised ClearerVoice Denoiser.

(https://github.com/modelscope/ClearerVoice-Studio/tree/main/clearvoice)

Model used here is only MossFormer2_SE_48K. Models: 
- 'MossFormer2_SE_48K' (https://huggingface.co/alibabasglab/MossFormer2_SE_48K)

Checkpoint for this model can be downloaded from 

(https://drive.google.com/drive/u/1/folders/1-7bFEDMfrKkRyx0alzyumhYvexPBBczE (If you are part of ASR-FAMILY) or https://huggingface.co/alibabasglab/MossFormer2_SE_48K/tree/main)

 and should be placed into /clearvoice/checkpoints as a /MossFormer2_SE_48K folder

## How to build container
1. Build the Docker Container
```console
docker-compose build clearervoice
```

## How to use
1. Put one or more audio clips to be denoised in /data/noisy

2. Run the docker container:
```console
docker-compose run clearervoice
```

3. Run clearvoice/denoising.py:

```console
python3 denoising.py
```

4. Denoised audio clips can be found in /data/clean