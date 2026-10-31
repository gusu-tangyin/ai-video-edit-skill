import argparse
from skill.video_edit_pipeline import video_edit_pipeline


def main():
    parser = argparse.ArgumentParser(description="AI video editing pipeline")
    parser.add_argument("--input", required=True, help="Input video path")
    parser.add_argument("--source-face", help="Face image for face swap")
    parser.add_argument("--target-avatar", help="Avatar image")
    parser.add_argument("--audio", help="Audio file")
    parser.add_argument("--background", help="Background image")
    parser.add_argument("--output", default="outputs/final.mp4")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--wav2lip-dir", default="./Wav2Lip")
    parser.add_argument("--checkpoint", default="./checkpoints/wav2lip.pth")
    args = parser.parse_args()

    result = video_edit_pipeline(
        input_video=args.input,
        source_face=args.source_face,
        target_avatar=args.target_avatar,
        audio_file=args.audio,
        background_image=args.background,
        output_path=args.output,
        fps=args.fps,
        wav2lip_dir=args.wav2lip_dir,
        checkpoint_path=args.checkpoint,
        use_face_swap=bool(args.source_face),
        use_avatar_replace=bool(args.target_avatar),
        use_lip_sync=bool(args.audio),
        use_background_replace=bool(args.background),
    )

    print(result)


if __name__ == "__main__":
    main()
