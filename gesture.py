import cv2
import mediapipe as mp
from pynput.keyboard import Controller

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
keyboard = Controller()

def press_key(key):
    keyboard.press(key)

def release_key(key):
    keyboard.release(key)

def detect_hand_position_in_frame(hand_landmarks, image_width):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    wrist_x = wrist.x * image_width
    if wrist_x < image_width * 0.3:
        return 'left'
    elif wrist_x > image_width * 0.7:
        return 'right'
    else:
        return 'center'

cap = cv2.VideoCapture(0)

gesture_state = None
key_pressed = {'w': False, 'a': False, 'd': False}
current_key = None  

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
        
        image = cv2.flip(image, 1)
        image_height, image_width, _ = image.shape
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                hand_position = detect_hand_position_in_frame(hand_landmarks, image_width)

                if hand_position == 'left' and current_key != 'a':
                    if current_key is not None:
                        release_key(current_key)
                    press_key('a')
                    current_key = 'a'

                elif hand_position == 'right' and current_key != 'd':
                    if current_key is not None:
                        release_key(current_key)
                    press_key('d')
                    current_key = 'd'

                elif hand_position == 'center' and current_key != 'w':
                    if current_key is not None:
                        release_key(current_key)
                    press_key('w')
                    current_key = 'w'

        cv2.imshow('Hand Gesture Control', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
