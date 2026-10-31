import os
import subprocess


def lip_sync_skill(input_video: str, audio_file: str, output_path: str, checkpoint_path: str, wav2lip_dir: str) -> dict:
    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Input video not found: {input_video}")
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint file not found: {checkpoint_path}")
    if not os.path.exists(wav2lip_dir):
        raise FileNotFoundError(f"Wav2Lip directory not found: {wav2lip_dir}")

    inference_script = os.path.join(wav2lip_dir, "inference.py")
    if not os.path.exists(inference_script):
        raise FileNotFoundError(f"Wav2Lip inference.py not found at {inference_script}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    cmd = [
        "python",
        inference_script,
        "--checkpoint_path",
        checkpoint_path,
        "--face",
        input_video,
        "--audio",
        audio_file,
        "--outfile",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Wav2Lip failed: {result.stderr}")

    return {"result_path": output_path, "status": "success"}
