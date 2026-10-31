# Wav2Lip Setup Guide

This project includes a real Wav2Lip integration for lip-sync generation. The model files must be downloaded and placed locally because they are too large to be committed into GitHub.

## 1. Clone the Wav2Lip repository

From the parent directory of this project:

```bash
git clone https://github.com/justinjohn0306/Wav2Lip.git ../Wav2Lip
```

This repo should end up in a folder named `Wav2Lip` adjacent to `ai-video-edit-skill`.

Example:

```text
parent/
├── ai-video-edit-skill/
├── Wav2Lip/
└── checkpoints/
```

## 2. Prepare the checkpoint

Download a compatible Wav2Lip checkpoint and place it here:

```text
./checkpoints/wav2lip.pth
```

This project expects the checkpoint file to exist before running the lip-sync step.

## 3. Use the setup script

From the repo root:

```bash
bash scripts/setup_wav2lip.sh
```

The script will:

- create a `checkpoints` folder if needed
- clone `Wav2Lip` next to this project if it does not already exist
- print the path where the checkpoint should be placed

## 4. Run the pipeline

Example:

```bash
python run.py \
  --input assets/input_video.mp4 \
  --source-face assets/source_face.png \
  --audio assets/input_audio.wav \
  --background assets/background.jpg \
  --output outputs/final.mp4 \
  --wav2lip-dir ../Wav2Lip \
  --checkpoint ./checkpoints/wav2lip.pth
```

## 5. Important notes

- Wav2Lip is required for the real mouth-sync step.
- If the checkpoint or repo is missing, the skill will fail with a clear error.
- The model files are intentionally not stored in this repository.

## 6. Production improvements

- add automatic checkpoint download support
- add GPU detection and CPU fallback
- add validation scripts for repo and checkpoint checks
- add metadata for generated outputs and pipeline status
