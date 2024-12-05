import cv2
import sys
import time
import numpy as np
import mediapipe as mp
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

from gesture_utils import (
    detect_peace_sign,
    detect_thumbs_up,
    detect_index_upwards,
    detect_rock_and_roll_salute,
    detect_fist
)

class GestureCapturePage(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the page layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create a label to display the video feed
        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)

        # Initialize video capture
        self.cap = cv2.VideoCapture(0)

        # Set up a QTimer to update the video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Initialize MediaPipe Hands class
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        # Initialize MediaPipe drawing utils
        self.mp_drawing = mp.solutions.drawing_utils

        # Initialize gesture timers
        self.gesture_timers = {
            'Peace Sign': 0,
            'Thumbs Up': 0,
            'Index Up': 0,
            'Rock and Roll Salute': 0,
            'Fist': 0
        }

        self.GESTURE_DETECTION_TIME = 1.5  # 1.5 seconds

    def update_frame(self):
        # Read a frame from the webcam
        ret, frame = self.cap.read()
        if not ret:
            return

        # Flip the frame horizontally for a selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert the image from BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame for hand tracking
        hand_results = self.hands.process(rgb_frame)

        # Initialize gesture variable
        gesture = 'No gesture detected'

        # Draw hand landmarks and detect gestures
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                # Draw the hand landmarks on the frame
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                )

                # Check for gestures
                if detect_peace_sign(hand_landmarks):
                    if self.gesture_timers['Peace Sign'] == 0:
                        self.gesture_timers['Peace Sign'] = time.time()
                    elif time.time() - self.gesture_timers['Peace Sign'] >= self.GESTURE_DETECTION_TIME:
                        gesture = 'Peace Sign Detected'
                else:
                    self.gesture_timers['Peace Sign'] = 0

                if detect_thumbs_up(hand_landmarks):
                    if self.gesture_timers['Thumbs Up'] == 0:
                        self.gesture_timers['Thumbs Up'] = time.time()
                    elif time.time() - self.gesture_timers['Thumbs Up'] >= self.GESTURE_DETECTION_TIME:
                        gesture = 'Thumbs Up Detected'
                else:
                    self.gesture_timers['Thumbs Up'] = 0

                if detect_index_upwards(hand_landmarks):
                    if self.gesture_timers['Index Up'] == 0:
                        self.gesture_timers['Index Up'] = time.time()
                    elif time.time() - self.gesture_timers['Index Up'] >= self.GESTURE_DETECTION_TIME:
                        gesture = 'Index Up Detected'
                else:
                    self.gesture_timers['Index Up'] = 0

                if detect_rock_and_roll_salute(hand_landmarks):
                    if self.gesture_timers['Rock and Roll Salute'] == 0:
                        self.gesture_timers['Rock and Roll Salute'] = time.time()
                    elif time.time() - self.gesture_timers['Rock and Roll Salute'] >= self.GESTURE_DETECTION_TIME:
                        gesture = 'Rock and Roll Salute Detected'
                else:
                    self.gesture_timers['Rock and Roll Salute'] = 0

                if detect_fist(hand_landmarks):
                    if self.gesture_timers['Fist'] == 0:
                        self.gesture_timers['Fist'] = time.time()
                    elif time.time() - self.gesture_timers['Fist'] >= self.GESTURE_DETECTION_TIME:
                        gesture = 'Fist Gesture Detected'
                else:
                    self.gesture_timers['Fist'] = 0

        # Display the gesture on the frame
        cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Convert the frame back to QImage to display in QLabel
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Set the pixmap of the video_label to the new frame
        self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        # Release the video capture when closing the page
        self.cap.release()
        self.timer.stop()
        super().closeEvent(event)

