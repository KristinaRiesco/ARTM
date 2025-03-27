import cv2
import mediapipe as mp
import time
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QApplication, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt


class GestureCreationPage(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the page layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create and configure the QLabel for video feed
        self.video_label = QLabel()
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setScaledContents(True)
        self.layout.addWidget(self.video_label)

        # Status Label (White text for visibility)
        self.status_label = QLabel("Ready to capture a new gesture.")
        self.status_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")  # White text
        self.layout.addWidget(self.status_label)

        # Capture Gesture Button
        self.capture_button = QPushButton("Capture Custom Gesture")
        self.capture_button.setStyleSheet("background-color: green; color: white; font-size: 14px;")
        self.capture_button.clicked.connect(self.start_gesture_capture)
        self.layout.addWidget(self.capture_button, alignment=Qt.AlignCenter)

        # Timer for updating video feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Initialize MediaPipe Hands class
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

        self.cap = None  # Camera will be initialized in start_camera()

        # Gesture Capture State
        self.is_capturing = False
        self.gesture_start_time = None  # Start time for holding the gesture
        self.REQUIRED_HOLD_TIME = 1.5  # Time (seconds) to hold the gesture
        self.detected_hand_landmarks = None  # Stores the detected hand landmarks

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

    def start_gesture_capture(self):
        """ Starts the gesture capture process and waits for the user to hold a pose. """
        self.is_capturing = True
        self.gesture_start_time = None  # Reset start time
        self.status_label.setText("<b style='color:white;'>✋ Hold your gesture for 1.5 seconds...</b>")

    def save_gesture(self):
        """ Saves the captured hand landmarks as a user-defined gesture. """
        if self.detected_hand_landmarks is None:
            self.status_label.setText("Error: No gesture detected.")
            return

        # Ask user to name their gesture
        gesture_name, ok = QInputDialog.getText(self, "Save Gesture", "Enter a name for this gesture:")
        if not ok or not gesture_name.strip():
            self.status_label.setText("Gesture saving canceled.")
            return

        # Extract landmarks as a list of (x, y, z) coordinates (rounded for consistency)
        gesture_data = {
            "name": gesture_name.strip(),
            "landmarks": [
                [round(lm.x, 4), round(lm.y, 4), round(lm.z, 4)] for lm in self.detected_hand_landmarks.landmark
            ]
        }

        # Save the gesture data to a JSON file
        try:
            with open("custom_gestures.json", "r") as file:
                saved_gestures = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            saved_gestures = []

        saved_gestures.append(gesture_data)

        with open("custom_gestures.json", "w") as file:
            json.dump(saved_gestures, file, indent=4)

        # Show Success Message (WHITE text for visibility)
        self.status_label.setText(f"<b style='color:white;'>✅ Gesture '{gesture_name}' saved successfully!</b>")

        # Hide message after 3 seconds (previously 2 seconds)
        QTimer.singleShot(3000, lambda: self.status_label.setText("Ready to capture a new gesture."))

        self.is_capturing = False  # Stop capturing after saving

    def update_frame(self):
        """ Continuously updates the webcam feed on the GUI. """
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
        self.detected_hand_landmarks = None  # Reset landmark storage

        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    rgb_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                self.detected_hand_landmarks = hand_landmarks  # Store last detected hand landmarks

        # Gesture Holding Logic
        if self.is_capturing and self.detected_hand_landmarks:
            if self.gesture_start_time is None:
                self.gesture_start_time = time.time()  # Start timer when gesture appears
            elif time.time() - self.gesture_start_time >= self.REQUIRED_HOLD_TIME:
                self.save_gesture()  # Save gesture when held for long enough
        else:
            self.gesture_start_time = None  # Reset timer if hand moves away

        # Convert to QImage
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Display the frame on the QLabel
        self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        """ Releases the webcam when the window is closed. """
        self.stop_camera()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = GestureCreationPage()
    window.start_camera()
    window.show()
    app.exec_()
