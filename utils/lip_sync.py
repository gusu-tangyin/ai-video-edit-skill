import os
import subprocess


class LipSyncProcessor:
    def __init__(self, wav2lip_dir: str):
        self.wav2lip_dir = wav2lip_dir

    def process(self, input_video: str, input_audio: str, output_video: str, checkpoint_path: str):
        if not os.path.exists(self.wav2lip_dir):
            raise FileNotFoundError(f"Wav2Lip directory not found: {self.wav2lip_dir}")

        inference_script = os.path.join(self.wav2lip_dir, "inference.py")
        if not os.path.exists(inference_script):
            raise FileNotFoundError(f"Wav2Lip inference script not found at {inference_script}")

        cmd = [
            "python",
            inference_script,
            "--checkpoint_path",
            checkpoint_path,
            "--face",
            input_video,
            "--audio",
            input_audio,
            "--outfile",
            output_video,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Wav2Lip failed: {result.stderr}")

        if not os.path.exists(output_video):
            raise FileNotFoundError(f"Wav2Lip output video not created: {output_video}")

        return output_video
