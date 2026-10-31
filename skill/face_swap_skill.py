import os

from utils.video_reader import read_video_frames
from utils.video_writer import write_video
from utils.face_swap import EnhancedFaceSwapper
from utils.temporal_smooth import temporal_smooth


def face_swap_skill(input_video: str, source_face: str, output_path: str, fps: int = 30) -> dict:
    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Input video not found: {input_video}")
    if not os.path.exists(source_face):
        raise FileNotFoundError(f"Source face image not found: {source_face}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    frames = read_video_frames(input_video)
    swapper = EnhancedFaceSwapper()
    processed = [swapper.swap(source_face, frame) for frame in frames]
    processed = temporal_smooth(processed)
    write_video(output_path, processed, fps=fps)

    return {"result_path": output_path, "status": "success"}
