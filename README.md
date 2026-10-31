# AI Video Editing Skill Platform

This project demonstrates a modular AI video editing workflow focused on:

- face swap
- avatar replacement
- lip sync
- background replacement
- unified video processing pipeline

## Overview

The project is built as an engineering scaffold for AI avatar and digital human workflows. It includes:

- a modular skill layer for each editing task
- a unified API layer
- a simple web demo
- a pipeline orchestrator for end-to-end workflow composition

## Project structure

```text
.
├── api.py
├── api_demo.py
├── run.py
├── requirements.txt
├── README.md
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
│   ├── color_match.py
│   ├── lighting_match.py
│   ├── temporal_smooth.py
│   ├── face_swap.py
│   ├── avatar_replace.py
│   ├── background_replace.py
│   └── lip_sync.py
└── outputs/
```

## Quick start

```bash
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

Then open the demo UI:

```text
http://localhost:8000/
```

### Demo backend

```bash
uvicorn api_demo:app --host 0.0.0.0 --port 8000 --reload
```

## API usage

### Face swap

```http
POST /skills/face_swap
```

### Avatar replace

```http
POST /skills/avatar_replace
```

### Lip sync

```http
POST /skills/lip_sync
```

### Background replace

```http
POST /skills/background_replace
```

### Full pipeline

```http
POST /pipeline/video_edit
```

## Notes

This repository is a practical prototype focused on modular design and realistic video-editing workflow composition. The advanced face swapping logic includes:

- color matching
- lighting normalization
- temporal smoothing
- blending stability improvements

This is intended as a solid foundation for future AI avatar, digital human, and virtual video creation workflows.
