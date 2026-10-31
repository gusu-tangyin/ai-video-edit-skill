import cv2
from typing import List


def write_video(output_path: str, frames: List, fps: int = 30):
    if not frames:
        raise ValueError("No frames to write.")

    h, w = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    for frame in frames:
        out.write(frame)

    out.release()
    print(f"Saved video: {output_path}")
