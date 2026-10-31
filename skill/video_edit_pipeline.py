from skill.face_swap_skill import face_swap_skill
from skill.avatar_replace_skill import avatar_replace_skill
from skill.lip_sync_skill import lip_sync_skill
from skill.background_replace_skill import background_replace_skill


def video_edit_pipeline(
    input_video,
    source_face=None,
    target_avatar=None,
    audio_file=None,
    background_image=None,
    output_path="outputs/final.mp4",
    fps=30,
    wav2lip_dir=None,
    checkpoint_path=None,
    use_face_swap=False,
    use_avatar_replace=False,
    use_lip_sync=False,
    use_background_replace=False,
):
    temp = input_video
    steps = []

    if use_face_swap and source_face:
        temp = face_swap_skill(temp, source_face, "outputs/step_face_swap.mp4", fps=fps)["result_path"]
        steps.append("face_swap")

    if use_avatar_replace and target_avatar:
        temp = avatar_replace_skill(temp, target_avatar, "outputs/step_avatar.mp4", fps=fps)["result_path"]
        steps.append("avatar_replace")

    if use_lip_sync and audio_file and wav2lip_dir and checkpoint_path:
        temp = lip_sync_skill(
            temp,
            audio_file,
            "outputs/step_lipsync.mp4",
            checkpoint_path,
            wav2lip_dir,
        )["result_path"]
        steps.append("lip_sync")

    if use_background_replace and background_image:
        temp = background_replace_skill(temp, background_image, output_path, fps=fps)["result_path"]
        steps.append("background_replace")

    return {
        "result_path": output_path if use_background_replace else temp,
        "steps": steps,
        "status": "success",
    }
