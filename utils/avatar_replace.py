import cv2


def replace_avatar_region(frame, avatar_image: str):
    avatar = cv2.imread(avatar_image)
    if avatar is None:
        raise FileNotFoundError(f"Avatar image not found: {avatar_image}")

    h, w = frame.shape[:2]
    return cv2.resize(avatar, (w, h))
