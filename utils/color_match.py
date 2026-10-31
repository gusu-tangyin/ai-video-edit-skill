import cv2
import numpy as np


def color_match(src, dst):
    src_lab = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)
    dst_lab = cv2.cvtColor(dst, cv2.COLOR_BGR2LAB)

    src_mean = src_lab.mean(axis=(0, 1))
    dst_mean = dst_lab.mean(axis=(0, 1))
    diff = dst_mean - src_mean

    src_adjusted = src_lab.astype(np.float32)
    src_adjusted[:, :, 0] += diff[0]
    src_adjusted[:, :, 1] += diff[1]
    src_adjusted[:, :, 2] += diff[2]

    src_adjusted = np.clip(src_adjusted, 0, 255).astype(np.uint8)
    return cv2.cvtColor(src_adjusted, cv2.COLOR_LAB2BGR)
