import cv2


def temporal_smooth(frames):
    if len(frames) < 2:
        return frames

    result = [frames[0]]
    for i in range(1, len(frames)):
        prev = result[-1]
        curr = frames[i]
        blended = cv2.addWeighted(prev, 0.7, curr, 0.3, 0)
        result.append(blended)
    return result
