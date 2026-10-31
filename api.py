from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from skill.face_swap_skill import face_swap_skill
from skill.avatar_replace_skill import avatar_replace_skill
from skill.lip_sync_skill import lip_sync_skill
from skill.background_replace_skill import background_replace_skill
from skill.video_edit_pipeline import video_edit_pipeline

app = FastAPI(
    title="Video Edit Skill API",
    description="AI video editing toolkit for face swap, avatar replacement, lip sync, and background replacement.",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "video_edit_skill"}


class FaceSwapRequest(BaseModel):
    input_video: str
    source_face: str
    output_path: str = "outputs/face_swap.mp4"
    fps: int = 30


class AvatarReplaceRequest(BaseModel):
    input_video: str
    target_avatar: str
    output_path: str = "outputs/avatar_replace.mp4"
    fps: int = 30


class LipSyncRequest(BaseModel):
    input_video: str
    audio_file: str
    output_path: str = "outputs/lip_sync.mp4"
    checkpoint_path: str = "./checkpoints/wav2lip.pth"
    wav2lip_dir: str = "./Wav2Lip"


class BackgroundReplaceRequest(BaseModel):
    input_video: str
    background_image: str
    output_path: str = "outputs/background_replace.mp4"
    fps: int = 30


class PipelineRequest(BaseModel):
    input_video: str
    source_face: Optional[str] = None
    target_avatar: Optional[str] = None
    audio_file: Optional[str] = None
    background_image: Optional[str] = None
    output_path: str = "outputs/final.mp4"
    fps: int = 30
    wav2lip_dir: Optional[str] = None
    checkpoint_path: Optional[str] = None
    use_face_swap: bool = False
    use_avatar_replace: bool = False
    use_lip_sync: bool = False
    use_background_replace: bool = False


@app.post("/skills/face_swap")
def api_face_swap(req: FaceSwapRequest):
    try:
        return face_swap_skill(
            input_video=req.input_video,
            source_face=req.source_face,
            output_path=req.output_path,
            fps=req.fps,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/skills/avatar_replace")
def api_avatar_replace(req: AvatarReplaceRequest):
    try:
        return avatar_replace_skill(
            input_video=req.input_video,
            target_avatar=req.target_avatar,
            output_path=req.output_path,
            fps=req.fps,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/skills/lip_sync")
def api_lip_sync(req: LipSyncRequest):
    try:
        return lip_sync_skill(
            input_video=req.input_video,
            audio_file=req.audio_file,
            output_path=req.output_path,
            checkpoint_path=req.checkpoint_path,
            wav2lip_dir=req.wav2lip_dir,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/skills/background_replace")
def api_background_replace(req: BackgroundReplaceRequest):
    try:
        return background_replace_skill(
            input_video=req.input_video,
            background_image=req.background_image,
            output_path=req.output_path,
            fps=req.fps,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/pipeline/video_edit")
def api_pipeline(req: PipelineRequest):
    try:
        return video_edit_pipeline(
            input_video=req.input_video,
            source_face=req.source_face,
            target_avatar=req.target_avatar,
            audio_file=req.audio_file,
            background_image=req.background_image,
            output_path=req.output_path,
            fps=req.fps,
            wav2lip_dir=req.wav2lip_dir,
            checkpoint_path=req.checkpoint_path,
            use_face_swap=req.use_face_swap,
            use_avatar_replace=req.use_avatar_replace,
            use_lip_sync=req.use_lip_sync,
            use_background_replace=req.use_background_replace,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
