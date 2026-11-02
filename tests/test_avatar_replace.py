import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import cv2
import numpy as np

from skill.avatar_replace_skill import avatar_replace_skill
from utils.avatar_replace import AvatarReplacer


def make_face(bbox, landmarks):
    return SimpleNamespace(
        bbox=np.asarray(bbox, dtype=np.float32),
        kps=np.asarray(landmarks, dtype=np.float32),
    )


class StaticDetector:
    def __init__(self, source_face, target_faces):
        self.source_face = source_face
        self.target_faces = target_faces
        self.calls = 0

    def get(self, image):
        self.calls += 1
        if self.calls == 1:
            return [self.source_face]
        return self.target_faces


class AvatarReplacerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.avatar_path = str(Path(self.temp_dir.name) / "avatar.png")
        avatar = np.zeros((160, 160, 3), dtype=np.uint8)
        avatar[:] = (20, 20, 220)
        self.assertTrue(cv2.imwrite(self.avatar_path, avatar))

        source_landmarks = [
            [65, 70],
            [95, 70],
            [80, 85],
            [70, 100],
            [90, 100],
        ]
        target_landmarks = [
            [75, 70],
            [117, 70],
            [96, 91],
            [82, 112],
            [110, 112],
        ]
        self.target_face = make_face([60, 50, 140, 150], target_landmarks)
        self.detector = StaticDetector(
            make_face([50, 50, 110, 120], source_landmarks),
            [self.target_face],
        )
        self.replacer = AvatarReplacer(self.avatar_path, detector=self.detector)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_aligns_and_blends_avatar_only_inside_face_mask(self):
        frame = np.full((200, 200, 3), 100, dtype=np.uint8)

        output = self.replacer.replace(frame)

        self.assertFalse(np.array_equal(output[95, 96], frame[95, 96]))
        np.testing.assert_array_equal(output[0, 0], frame[0, 0])
        self.assertEqual(self.detector.calls, 2)

    def test_preserves_frame_when_no_target_face_is_detected(self):
        self.detector.target_faces = []
        frame = np.full((200, 200, 3), 100, dtype=np.uint8)

        output = self.replacer.replace(frame)

        np.testing.assert_array_equal(output, frame)

    def test_requires_a_detectable_face_in_avatar(self):
        detector = StaticDetector(None, [])
        detector.get = lambda image: []

        with self.assertRaisesRegex(ValueError, "No detectable face"):
            AvatarReplacer(self.avatar_path, detector=detector)

    def test_video_skill_reuses_one_replacer_for_all_frames(self):
        frame = np.zeros((200, 200, 3), dtype=np.uint8)
        with patch("skill.avatar_replace_skill.os.path.exists", return_value=True), patch(
            "skill.avatar_replace_skill.read_video_frames", return_value=[frame, frame]
        ), patch("skill.avatar_replace_skill.AvatarReplacer") as replacer_class, patch(
            "skill.avatar_replace_skill.write_video"
        ) as write_video:
            replacer_class.return_value.replace.side_effect = lambda value: value

            result = avatar_replace_skill("input.mp4", "avatar.png", "out.mp4")

        replacer_class.assert_called_once_with("avatar.png")
        self.assertEqual(replacer_class.return_value.replace.call_count, 2)
        write_video.assert_called_once()
        self.assertEqual(result, {"result_path": "out.mp4", "status": "success"})


if __name__ == "__main__":
    unittest.main()
