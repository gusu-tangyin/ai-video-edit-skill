import cv2
import numpy as np
from typing import List

try:
    from rembg import remove
    HAS_REMBG = True
except Exception:
    HAS_REMBG = False


def replace_background(frames: List, background_img: str) -> List:
    if not frames:
        raise ValueError("No frames provided.")

    bg = cv2.imread(background_img)
    if bg is None:
        raise FileNotFoundError(f"Background image not found: {background_img}")

    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        bg_resized = cv2.resize(bg, (w, h))

        if HAS_REMBG:
            rgba = remove(frame)
            if rgba.shape[2] == 4:
                bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
                alpha = rgba[:, :, 3]
            else:
                bgr = rgba
                alpha = np.ones(frame.shape[:2], dtype=np.uint8) * 255

            mask = alpha.astype(np.uint8)
            inv_mask = cv2.bitwise_not(mask)
            fg_masked = cv2.bitwise_and(bgr, bgr, mask=mask)
            bg_masked = cv2.bitwise_and(bg_resized, bg_resized, mask=inv_mask)
            result.append(cv2.add(fg_masked, bg_masked))
        else:
            result.append(bg_resized)

    return result
