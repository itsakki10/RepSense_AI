import cv2
import av

from services.vision.exercise_video_processor import (
    VideoProcessorClass
)


def analyze_uploaded_video(
    video_path,
    exercise
):

    cap = cv2.VideoCapture(
        video_path
    )

    processor = VideoProcessorClass()

    processor.set_exercise(
        exercise
    )

    frame_count = 0

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            break

        frame_count += 1

        if frame_count % 3 != 0:
            continue

        video_frame = av.VideoFrame.from_ndarray(
            frame,
            format="bgr24"
        )

        processor.recv(
            video_frame
        )

    cap.release()

    return (
        processor.get_latest_metrics()
    )