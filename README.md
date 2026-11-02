# AI Video Editing Skill Platform

This project is a modular AI video editing platform focused on creating digital-human and virtual-content workflows. It includes the following capabilities:

- Face swap
- Avatar replacement
- Lip sync
- Background replacement
- Unified pipeline orchestration

## Overview

The repository is designed to provide a practical engineering scaffold for AI avatar workflows, digital human generation, and virtual scene transformation. It is structured as a modular system where each editing skill is developed independently and can be chained together through a unified processing pipeline.

The project currently includes:

- modular skill implementation
- a FastAPI-based API layer
- a browser demo interface
- workflow orchestration logic
- local Wav2Lip integration support
- enhanced face blending and stability logic

## Project goals

- Replace a face in a video with a target human face
- Replace the character region with a target avatar image
- Synchronize mouth motion to a speech audio stream
- Replace the original background with a virtual scene
- Compose these capabilities into one end-to-end pipeline
- Expose the features via API and prototype UI

## Architecture

```text
.
├── api.py
├── api_demo.py
├── run.py
├── requirements.txt
├── README.md
├── WAV2LIP_SETUP.md
├── config.yaml
├── templates/
│   └── index.html
├── skill/
│   ├── __init__.py
│   ├── face_swap_skill.py
│   ├── avatar_replace_skill.py
│   ├── lip_sync_skill.py
│   ├── background_replace_skill.py
│   └── video_edit_pipeline.py
├── utils/
│   ├── __init__.py
│   ├── video_reader.py
│   ├── video_writer.py
│   ├── face_swap.py
│   ├── avatar_replace.py
│   ├── background_replace.py
│   ├── lip_sync.py
│   ├── color_match.py
│   ├── lighting_match.py
│   └── temporal_smooth.py
├── scripts/
│   └── setup_wav2lip.sh
├── checkpoints/
│   └── .gitkeep
├── uploads/
│   └── .gitkeep
├── outputs/
│   └── .gitkeep
├── .gitignore
└── LICENSE
```

## Features

### 1. Face swap
The face swap skill detects prominent faces in the source image and target video frame, aligns them, and applies color and lighting correction before blending them into the frame.

### 2. Avatar replacement
The avatar replacement skill detects the face in the target avatar and video frames, aligns the avatar to the largest detected video face using five facial landmarks, and blends the aligned face with a feathered face mask. If a 106-point face contour is available, it is used for the mask; otherwise, the skill falls back to an oval mask. Frames without a detected target face are preserved.

The first run downloads InsightFace's `buffalo_l` model pack to the local InsightFace model cache. Use avatar images and video subjects that you have permission to edit.

### 3. Lip sync
The lip sync module integrates with Wav2Lip locally. It expects a valid Wav2Lip repository and checkpoint to be available on the machine running the pipeline.

### 4. Background replacement
The background replacement skill can replace the source background with a custom scene image or virtual environment to improve storytelling and production quality.

### 5. Unified workflow
Multiple skills can be chained into a single pipeline so users can perform end-to-end video editing from a single request.

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Wav2Lip locally

This project uses a real Wav2Lip integration for lip-sync processing. The model files are too large to be committed to GitHub, so they must be set up locally.

Use the helper script:

```bash
bash scripts/setup_wav2lip.sh
```

Or clone manually:

```bash
git clone https://github.com/justinjohn0306/Wav2Lip.git ../Wav2Lip
```

Then place the checkpoint at:

```text
./checkpoints/wav2lip.pth
```

See `WAV2LIP_SETUP.md` for the full setup guide.

### 3. Run the API

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Run the demo UI

```bash
uvicorn api_demo:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

```text
http://localhost:8000/
```

## API endpoints

### Face swap

```http
POST /skills/face_swap
```

### Avatar replacement

```http
POST /skills/avatar_replace
```

The request accepts `input_video`, `target_avatar`, `output_path`, and `fps`. The CLI also supports this skill:

```bash
python run.py \
  --input assets/input_video.mp4 \
  --target-avatar assets/avatar.png \
  --output outputs/avatar_replace.mp4
```

### Lip sync

```http
POST /skills/lip_sync
```

### Background replacement

```http
POST /skills/background_replace
```

### End-to-end workflow

```http
POST /pipeline/video_edit
```

## Example CLI usage

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

## Notes

This repository serves as a practical engineering prototype for AI video generation workflows. It balances speed of development with a realistic architecture for AI avatar and digital-human content production.

Important implementation notes:

- The project is intentionally modular so each skill can be independently optimized.
- The Wav2Lip model and checkpoint are external runtime dependencies.
- Output files and uploaded assets are treated as local runtime artifacts and are excluded from Git tracking.
- The face-swap logic includes color matching, lighting normalization, and temporal smoothing to reduce obvious artifacts.

## Use cases

- AI presenter generation
- Digital human creation
- Virtual avatar customization
- Short-form content production
- Virtual environments and advertising scenes
- Character replacement for storytelling and brand content

## Future directions

- improve face blurring and temporal consistency
- enhance avatar-quality blending
- add fine-grained background segmentation and modeling
- improve integration with more advanced speech-driven animation systems
- package the workflow as a more polished product-ready service

## License

This project is distributed under the MIT license unless otherwise noted in third-party dependencies.
