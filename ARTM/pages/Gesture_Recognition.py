import cv2
import mediapipe as mp
from gesture_utils import (
    detect_peace_sign,
    detect_thumbs_up,
    detect_index_upwards,
    detect_rock_and_roll_salute,
    detect_fist,
)

# Initialize MediaPipe Pose and Hands classes
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose()
hands = mp_hands.Hands()

# Initialize MediaPipe drawing utils
mp_drawing = mp.solutions.drawing_utils

# Dictionary to keep track of gesture timestamps
gesture_timers = {
    'Peace Sign': 0,
    'Thumbs Up': 0,
    'Index Up': 0,
    'Rock and Roll Salute': 0,
    'Fist': 0
}

GESTURE_DETECTION_TIME = 1.5

def start_recognition():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for selfie view
        frame = cv2.flip(frame, 1)

        # Convert the image from BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame for pose and hand estimation
        pose_results = pose.process(rgb_frame)
        hand_results = hands.process(rgb_frame)

        # Draw landmarks and detect gestures
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                )

                gesture = detect_gesture(hand_landmarks)

                # Display detected gesture
                if gesture:
                    cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow('Gesture Recognition', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def detect_gesture(hand_landmarks):
    if detect_peace_sign(hand_landmarks):
        return 'Peace Sign'
    elif detect_thumbs_up(hand_landmarks):
        return 'Thumbs Up'
    elif detect_index_upwards(hand_landmarks):
        return 'Index Up'
    elif detect_rock_and_roll_salute(hand_landmarks):
        return 'Rock and Roll Salute'
    elif detect_fist(hand_landmarks):
        return 'Fist'

    return None
