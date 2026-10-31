import os

from utils.video_reader import read_video_frames
from utils.video_writer import write_video
from utils.background_replace import replace_background


def background_replace_skill(input_video: str, background_image: str, output_path: str, fps: int = 30) -> dict:
    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Input video not found: {input_video}")
    if not os.path.exists(background_image):
        raise FileNotFoundError(f"Background image not found: {background_image}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    frames = read_video_frames(input_video)
    processed = replace_background(frames, background_image)
    write_video(output_path, processed, fps=fps)

    return {"result_path": output_path, "status": "success"}
