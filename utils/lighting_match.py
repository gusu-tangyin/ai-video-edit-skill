import cv2
import numpy as np


def lighting_match(src, dst):
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    src_mean = src_gray.mean()
    dst_mean = dst_gray.mean()
    alpha = dst_mean / max(src_mean, 1e-6)

    adjusted = src.astype(np.float32) * alpha
    adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
    return adjusted
