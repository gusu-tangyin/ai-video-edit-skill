import os
import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from skill.face_swap_skill import face_swap_skill
from skill.lip_sync_skill import lip_sync_skill
from skill.background_replace_skill import background_replace_skill

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
TEMPLATE_DIR = BASE_DIR / "templates"

UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
TEMPLATE_DIR.mkdir(exist_ok=True, parents=True)

app = FastAPI(title="AI Avatar Demo")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def save_upload(file: UploadFile, folder: Path) -> str:
    folder.mkdir(exist_ok=True, parents=True)
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    dest = folder / filename
    with dest.open("wb") as f:
        f.write(file.file.read())
    return str(dest)


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=(TEMPLATE_DIR / "index.html").read_text(encoding="utf-8"))


@app.post("/api/demo/ai_avatar")
async def demo_ai_avatar(
    input_video: UploadFile = File(...),
    source_face: UploadFile = File(...),
    audio: UploadFile = File(default=None),
    background: UploadFile = File(default=None),
    wav2lip_dir: str = Form("./Wav2Lip"),
    checkpoint_path: str = Form("./checkpoints/wav2lip.pth"),
):
    video_path = save_upload(input_video, UPLOAD_DIR)
    face_path = save_upload(source_face, UPLOAD_DIR)

    audio_path = save_upload(audio, UPLOAD_DIR) if audio else None
    background_path = save_upload(background, UPLOAD_DIR) if background else None

    steps = []
    temp_video = video_path

    face_output = OUTPUT_DIR / f"{uuid.uuid4().hex}_face_swap.mp4"
    face_result = face_swap_skill(
        input_video=video_path,
        source_face=face_path,
        output_path=str(face_output),
        fps=30,
    )
    temp_video = face_result["result_path"]
    steps.append("face_swap")

    if audio_path:
        if os.path.exists(wav2lip_dir) and os.path.exists(checkpoint_path):
            lip_output = OUTPUT_DIR / f"{uuid.uuid4().hex}_lip_sync.mp4"
            lip_result = lip_sync_skill(
                input_video=temp_video,
                audio_file=audio_path,
                output_path=str(lip_output),
                checkpoint_path=checkpoint_path,
                wav2lip_dir=wav2lip_dir,
            )
            temp_video = lip_result["result_path"]
            steps.append("lip_sync")
        else:
            steps.append("lip_sync_skipped_missing_model")

    final_output = OUTPUT_DIR / f"{uuid.uuid4().hex}_final.mp4"
    if background_path:
        bg_result = background_replace_skill(
            input_video=temp_video,
            background_image=background_path,
            output_path=str(final_output),
            fps=30,
        )
        final_path = bg_result["result_path"]
        steps.append("background_replace")
    else:
        final_path = temp_video

    return {
        "status": "success",
        "result_path": str(final_path),
        "steps": steps,
        "error": None,
    }
