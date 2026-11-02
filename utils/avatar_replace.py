from typing import Optional

import cv2
import numpy as np


class AvatarReplacer:
    def __init__(self, avatar_image: str, detector=None):
        image = cv2.imread(str(avatar_image), cv2.IMREAD_UNCHANGED)
        if image is None:
            raise FileNotFoundError(f"Avatar image not found or unreadable: {avatar_image}")

        if image.ndim == 2:
            self.avatar = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            self.avatar_alpha = None
        elif image.shape[2] == 4:
            self.avatar = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
            self.avatar_alpha = image[:, :, 3]
        else:
            self.avatar = image
            self.avatar_alpha = None

        self.detector = detector or self._create_detector()
        source_faces = self.detector.get(self.avatar)
        if not source_faces:
            raise ValueError(f"No detectable face found in avatar image: {avatar_image}")

        source_face = max(source_faces, key=self._face_area)
        self.source_landmarks = self._landmarks(source_face)
        self.source_bbox = np.asarray(source_face.bbox, dtype=np.float32)
        self.source_mask = self._make_face_mask(
            self.avatar.shape[:2], self.source_bbox, source_face
        )
        if self.avatar_alpha is not None:
            self.source_mask = cv2.min(self.source_mask, self.avatar_alpha)

    @staticmethod
    def _create_detector():
        try:
            from insightface.app import FaceAnalysis
        except ImportError as exc:
            raise RuntimeError(
                "Avatar replacement requires InsightFace; install the project requirements."
            ) from exc

        app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=-1, det_size=(640, 640))
        return app

    @staticmethod
    def _face_area(face) -> float:
        x1, y1, x2, y2 = face.bbox
        return max(0.0, float(x2 - x1)) * max(0.0, float(y2 - y1))

    @staticmethod
    def _landmarks(face) -> np.ndarray:
        landmarks = getattr(face, "kps", None)
        if landmarks is None:
            raise ValueError("Face detector did not return five-point landmarks.")
        landmarks = np.asarray(landmarks, dtype=np.float32)
        if landmarks.shape != (5, 2) or not np.isfinite(landmarks).all():
            raise ValueError("Face detector returned invalid five-point landmarks.")
        return landmarks

    @staticmethod
    def _make_face_mask(shape, bbox, face, offset=None) -> np.ndarray:
        height, width = shape
        x1, y1, x2, y2 = bbox
        mask = np.zeros((height, width), dtype=np.uint8)

        contour = getattr(face, "landmark_2d_106", None)
        if contour is not None:
            contour = np.asarray(contour, dtype=np.float32).copy()
            if offset is not None:
                contour -= np.asarray(offset, dtype=np.float32)
            if (
                contour.ndim == 2
                and contour.shape[1] == 2
                and len(contour) >= 3
                and np.isfinite(contour).all()
            ):
                contour = np.rint(contour).astype(np.int32)
                contour[:, 0] = np.clip(contour[:, 0], 0, width - 1)
                contour[:, 1] = np.clip(contour[:, 1], 0, height - 1)
                cv2.fillConvexPoly(mask, cv2.convexHull(contour), 255)
                return mask

        center = (
            int(round((x1 + x2) / 2)),
            int(round(y1 + (y2 - y1) * 0.53)),
        )
        axes = (
            max(1, int(round((x2 - x1) * 0.49))),
            max(1, int(round((y2 - y1) * 0.58))),
        )
        cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)
        return mask

    def replace(self, frame: np.ndarray) -> np.ndarray:
        target_faces = self.detector.get(frame)
        if not target_faces:
            return frame.copy()

        target_face = max(target_faces, key=self._face_area)
        target_landmarks = self._landmarks(target_face)
        x1, y1, x2, y2 = np.asarray(target_face.bbox, dtype=np.float32)
        face_width = max(1.0, x2 - x1)
        face_height = max(1.0, y2 - y1)

        frame_height, frame_width = frame.shape[:2]
        padding_x = int(round(face_width * 0.4))
        padding_y = int(round(face_height * 0.4))
        roi_x1 = max(0, int(np.floor(x1)) - padding_x)
        roi_y1 = max(0, int(np.floor(y1)) - padding_y)
        roi_x2 = min(frame_width, int(np.ceil(x2)) + padding_x)
        roi_y2 = min(frame_height, int(np.ceil(y2)) + padding_y)
        if roi_x2 <= roi_x1 or roi_y2 <= roi_y1:
            return frame.copy()

        target_local = target_landmarks - np.array([roi_x1, roi_y1], dtype=np.float32)
        transform, _ = cv2.estimateAffinePartial2D(
            self.source_landmarks,
            target_local,
            method=cv2.LMEDS,
        )
        if transform is None:
            raise RuntimeError("Could not align avatar landmarks to the target face.")

        roi_size = (roi_x2 - roi_x1, roi_y2 - roi_y1)
        warped_avatar = cv2.warpAffine(
            self.avatar,
            transform,
            roi_size,
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_CONSTANT,
        )
        warped_mask = cv2.warpAffine(
            self.source_mask,
            transform,
            roi_size,
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
        )

        target_bbox = np.array(
            [x1 - roi_x1, y1 - roi_y1, x2 - roi_x1, y2 - roi_y1],
            dtype=np.float32,
        )
        target_mask = self._make_face_mask(
            (roi_size[1], roi_size[0]),
            target_bbox,
            target_face,
            offset=(roi_x1, roi_y1),
        )

        mask = cv2.min(warped_mask, target_mask)
        blur_size = max(3, int(round(min(face_width, face_height) * 0.08)) | 1)
        mask = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)
        alpha = mask.astype(np.float32)[:, :, None] / 255.0

        output = frame.copy()
        target_roi = output[roi_y1:roi_y2, roi_x1:roi_x2].astype(np.float32)
        avatar_roi = warped_avatar.astype(np.float32)
        output[roi_y1:roi_y2, roi_x1:roi_x2] = np.clip(
            avatar_roi * alpha + target_roi * (1.0 - alpha), 0, 255
        ).astype(np.uint8)
        return output


def replace_avatar_region(
    frame: np.ndarray, avatar_image: str, replacer: Optional[AvatarReplacer] = None
) -> np.ndarray:
    processor = replacer or AvatarReplacer(avatar_image)
    return processor.replace(frame)
