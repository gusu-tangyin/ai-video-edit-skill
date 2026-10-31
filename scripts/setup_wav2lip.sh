#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PARENT_DIR="$(dirname "$ROOT_DIR")"
WAV2LIP_DIR="$PARENT_DIR/Wav2Lip"
CHECKPOINT_DIR="$ROOT_DIR/checkpoints"

mkdir -p "$CHECKPOINT_DIR"

if [ ! -d "$WAV2LIP_DIR" ]; then
  echo "Cloning Wav2Lip into $WAV2LIP_DIR"
  git clone https://github.com/justinjohn0306/Wav2Lip.git "$WAV2LIP_DIR"
else
  echo "Wav2Lip already exists at $WAV2LIP_DIR"
fi

echo "Place a checkpoint file at: $CHECKPOINT_DIR/wav2lip.pth"
source_dir="$ROOT_DIR"
if [ -d "$source_dir" ]; then
  echo "Project root: $source_dir"
fi
