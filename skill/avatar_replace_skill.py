import os

from utils.video_reader import read_video_frames
from utils.video_writer import write_video
from utils.avatar_replace import AvatarReplacer


def avatar_replace_skill(input_video: str, target_avatar: str, output_path: str, fps: int = 30) -> dict:
    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Input video not found: {input_video}")
    if not os.path.exists(target_avatar):
        raise FileNotFoundError(f"Target avatar image not found: {target_avatar}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    frames = read_video_frames(input_video)
    replacer = AvatarReplacer(target_avatar)
    processed = [replacer.replace(frame) for frame in frames]
    write_video(output_path, processed, fps=fps)

    return {"result_path": output_path, "status": "success"}
