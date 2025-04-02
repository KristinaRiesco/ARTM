import cv2
import mediapipe as mp
import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

#Import gesture detection functions from gesture_utils.py
from gesture_utils import (
    detect_peace_sign,
    detect_thumbs_up,
    detect_index_up,
    detect_rock_and_roll_salute,
    detect_fist,
    detect_letter_l
)


class GestureCapturePage(QWidget):
    def __init__(self, home_page=None):
        super().__init__()
        self.home_page = home_page

        # Set up the page layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create and configure the QLabel for video feed
        self.video_label = QLabel()
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setScaledContents(True)
        self.layout.addWidget(self.video_label)

        # Status Label
        self.status_label = QLabel("Gesture detection in progress...")
        self.layout.addWidget(self.status_label)

        # Timer for updating video feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.held_gesture = None
        self.held_gesture_start_time = None


        # Initialize MediaPipe Hands class
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,  # Higher confidence threshold for better accuracy
            min_tracking_confidence=0.7
        )
        self.mp_drawing = mp.solutions.drawing_utils

        self.cap = None  # Camera will be initialized in start_camera()

        # Gesture Timers (to confirm a gesture after 1.5 seconds)
        self.gesture_timers = {}
        self.REQUIRED_HOLD_TIME = 3  # Time (seconds) a gesture must be held
        self.COOLDOWN_TIME = 3  # Time (seconds) before detecting another gesture

        #Flags to prevent repeated detections
        self.gesture_detected = False
        self.last_detected_time = 0

        self.current_gesture_label = QLabel("Current Gesture: None")
        self.current_gesture_label.setStyleSheet("font-size: 16px; font-weight: bold; color: blue;")
        self.layout.addWidget(self.current_gesture_label)

        self.countdown_label = QLabel("")
        self.countdown_label.setStyleSheet("font-size: 24px; font-weight: bold; color: red;")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.countdown_label)

    def start_camera(self):
        """ Initializes and starts the camera when the page is shown. """
        if self.cap is not None:
            self.stop_camera()

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_label.setText("Error: Cannot access webcam.")
            return

        self.timer.start(30)
        self.status_label.setText("Camera started.")

    def stop_camera(self):
        """ Releases the camera when leaving the page. """
        if self.cap is not None and self.cap.isOpened():
            self.timer.stop()
            self.cap.release()
            self.cap = None
            self.video_label.clear()



    def update_frame(self):
        """ Continuously updates the webcam feed on the GUI and detects gestures. """
        if self.cap is None or not self.cap.isOpened():
            self.status_label.setText("Error: Camera feed lost.")
            return

        ret, frame = self.cap.read()
        if not ret:
            self.status_label.setText("Error: No frame received from webcam.")
            return

        frame = cv2.flip(frame, 1)  # Flip for selfie view
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame for hand tracking
        hand_results = self.hands.process(rgb_frame)
        detected_gesture = None

        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                # Draw the hand landmarks on the frame
                self.mp_drawing.draw_landmarks(
                    rgb_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                #Check for predefined gestures using imported functions
                if detect_peace_sign(hand_landmarks):
                    detected_gesture = "Peace Sign"
                elif detect_thumbs_up(hand_landmarks):
                    detected_gesture = "Thumbs Up"
                elif detect_index_up(hand_landmarks):
                    detected_gesture = "Index Up"
                elif detect_rock_and_roll_salute(hand_landmarks):
                    detected_gesture = "Rock and Roll Salute"
                elif detect_fist(hand_landmarks):
                    detected_gesture = "Fist"
                elif detect_letter_l(hand_landmarks):
                    detected_gesture = "L Sign"

                #Check cooldown
                current_time = time.time()
                if self.gesture_detected and current_time - self.last_detected_time < self.COOLDOWN_TIME:
                    continue  # Skip detection during cooldown

                #Start/Reset timer for detected gesture
                if detected_gesture:
                    self.current_gesture_label.setText(f"Current Gesture: {detected_gesture}")

                    if self.held_gesture != detected_gesture:
                        self.held_gesture = detected_gesture
                        self.held_gesture_start_time = current_time
                        self.countdown_label.setText("Detecting...")
                    else:
                        held_duration = current_time - self.held_gesture_start_time
                        self.countdown_label.setText(f"Holding: {int(held_duration)}s")

                        if held_duration >= self.REQUIRED_HOLD_TIME:
                            self.status_label.setText(f"Gesture Confirmed: {detected_gesture}")
                            print(f"Triggering macro for: {detected_gesture}")
                            if self.home_page:
                                self.home_page.handle_detected_gesture(detected_gesture)

                            #reset tracking for time and gesture
                            self.held_gesture = None
                            self.held_gesture_start_time = None
                            self.countdown_label.setText("")

                #else:
                #    self.current_gesture_label.setText("Current Gesture: None")
                #    self.countdown_label.setText("")
                #    self.held_gesture = None
                #    self.held_gesture_start_time = None


        # Convert to QImage
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Display the frame on the QLabel
        self.video_label.setPixmap(QPixmap.fromImage(q_img))

        if detected_gesture is None:
            self.current_gesture_label.setText("Current Gesture: None")
            self.countdown_label.setText("")
            self.held_gesture = None
            self.held_gesture_start_time = None

    def closeEvent(self, event):
        """ Releases the webcam when the window is closed. """
        self.stop_camera()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = GestureCapturePage()
    window.start_camera()
    window.show()
    app.exec_()

