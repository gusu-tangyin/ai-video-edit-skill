import cv2
from insightface.app import FaceAnalysis
from utils.color_match import color_match
from utils.lighting_match import lighting_match


class EnhancedFaceSwapper:
    def __init__(self):
        self.app = FaceAnalysis(name="antelopev2", root="~/.insightface")
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def detect_faces(self, img):
        return self.app.get(img)

    def get_best_face(self, faces):
        if not faces:
            return None
        return max(faces, key=lambda f: f.bbox[2] * f.bbox[3])

    def swap(self, source_image: str, frame):
        source = cv2.imread(source_image)
        if source is None:
            raise FileNotFoundError(f"Source image not found: {source_image}")

        source_faces = self.detect_faces(source)
        target_faces = self.detect_faces(frame)
        if not source_faces or not target_faces:
            return frame

        source_face = self.get_best_face(source_faces)
        target_face = self.get_best_face(target_faces)

        src_x1, src_y1, src_x2, src_y2 = map(int, source_face.bbox.astype(int))
        tgt_x1, tgt_y1, tgt_x2, tgt_y2 = map(int, target_face.bbox.astype(int))

        pad = 25
        src_x1 = max(0, src_x1 - pad)
        src_y1 = max(0, src_y1 - pad)
        src_x2 = min(source.shape[1], src_x2 + pad)
        src_y2 = min(source.shape[0], src_y2 + pad)

        tgt_x1 = max(0, tgt_x1 - pad)
        tgt_y1 = max(0, tgt_y1 - pad)
        tgt_x2 = min(frame.shape[1], tgt_x2 + pad)
        tgt_y2 = min(frame.shape[0], tgt_y2 + pad)

        src_crop = source[src_y1:src_y2, src_x1:src_x2]
        dst_roi = frame[tgt_y1:tgt_y2, tgt_x1:tgt_x2]
        if dst_roi.size == 0:
            return frame

        resized = cv2.resize(src_crop, (dst_roi.shape[1], dst_roi.shape[0]))
        resized = color_match(resized, dst_roi)
        resized = lighting_match(resized, dst_roi)

        blended = cv2.addWeighted(dst_roi, 0.75, resized, 0.25, 0)
        out = frame.copy()
        out[tgt_y1:tgt_y2, tgt_x1:tgt_x2] = blended
        return out
