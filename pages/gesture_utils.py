import mediapipe as mp

# Initialize MediaPipe Hands class
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize MediaPipe drawing utils
mp_drawing = mp.solutions.drawing_utils

# -------------------------------------------------------------------
# PREMADE GESTURES & UTILITY FUNCTIONS
# -------------------------------------------------------------------

# List of premade gestures used throughout the application.
PREMADE_GESTURES = [
    "Fist",
    "Index Up",
    "L",
    "Peace Sign",
    "Rock & Roll",
    "Thumbs Up"
]

def get_premade_gestures():
    """
    Returns the list of premade gestures.
    """
    return PREMADE_GESTURES

def is_valid_gesture(gesture):
    """
    Checks if the given gesture is valid.
    A gesture is valid if it is in PREMADE_GESTURES or if it is the special "Capture Gesture".
    """
    return gesture in PREMADE_GESTURES or gesture == "Capture Gesture"


# -------------------------------------------------------------------
# GESTURE DETECTION FUNCTIONS
# -------------------------------------------------------------------

# Function to detect peace sign gesture
def detect_peace_sign(hand_landmarks):
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    index_extended = index_finger_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_extended = middle_finger_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_curled = ring_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_curled = pinky_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y

    return index_extended and middle_extended and ring_curled and pinky_curled


# Function to detect thumbs up gesture
def detect_thumbs_up(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    thumb_extended = thumb_tip.y < thumb_ip.y
    index_curled = index_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_curled = middle_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_curled = ring_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_curled = pinky_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y

    return thumb_extended and index_curled and middle_curled and ring_curled and pinky_curled


# Function to detect index upwards gesture
def detect_index_up(hand_landmarks):
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    index_extended = index_finger_tip.y < index_finger_pip.y
    middle_curled = middle_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_curled = ring_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_curled = pinky_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y

    return index_extended and middle_curled and ring_curled and pinky_curled


# Function to detect rock and roll salute gesture
def detect_rock_and_roll_salute(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]

    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]

    pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

    thumb_extended = thumb_tip.x < thumb_ip.x
    index_extended = index_finger_tip.y < index_finger_pip.y
    pinky_extended = pinky_finger_tip.y < pinky_finger_pip.y

    middle_curled = middle_finger_tip.y > middle_finger_pip.y
    ring_curled = ring_finger_tip.y > ring_finger_pip.y

    return thumb_extended and index_extended and pinky_extended and middle_curled and ring_curled


# Function to detect fist gesture
def detect_fist(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]

    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]

    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

    thumb_curled = thumb_tip.x > thumb_ip.x
    index_curled = index_tip.y > index_pip.y
    middle_curled = middle_tip.y > middle_pip.y
    ring_curled = ring_tip.y > ring_pip.y
    pinky_curled = pinky_tip.y > pinky_pip.y

    return thumb_curled and index_curled and middle_curled and ring_curled and pinky_curled


# Function to detect the L Sign Gesture
def detect_letter_l(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    thumb_extended = thumb_tip.x < thumb_ip.x
    index_extended = index_tip.y < index_pip.y
    middle_curled = middle_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_curled = ring_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_curled = pinky_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y

    return thumb_extended and index_extended and middle_curled and ring_curled and pinky_curled
