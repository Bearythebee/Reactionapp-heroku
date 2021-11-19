import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose


WRIST = 0
THUMB_CMC = 1
THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4
INDEX_FINGER_MCP = 5
INDEX_FINGER_PIP = 6
INDEX_FINGER_DIP = 7
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_MCP = 9
MIDDLE_FINGER_PIP = 10
MIDDLE_FINGER_DIP = 11
MIDDLE_FINGER_TIP = 12
RING_FINGER_MCP = 13
RING_FINGER_PIP = 14
RING_FINGER_DIP = 15
RING_FINGER_TIP = 16
PINKY_MCP = 17
PINKY_PIP = 18
PINKY_DIP = 19
PINKY_TIP = 20

def framestocoord(image_path):

    # Input: image frame
    # Output: Numpy array

    with mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as holistic :

        Image = cv2.imread(image_path)
        image = cv2.flip(Image, 1)

        #image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        image_height, image_width, _ = image.shape

        # Convert the BGR image to RGB before processing.
        results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        lefthand_landmarks = results.left_hand_landmarks
        righthand_landmarks = results.right_hand_landmarks

        if lefthand_landmarks ==  None or righthand_landmarks == None :
            return

        arr = []

        leftwrist = ''
        for point in mp_hands.HandLandmark :
            normalizedLandmark = lefthand_landmarks.landmark[point]
            if point == mp_hands.HandLandmark.WRIST :
                leftwrist = normalizedLandmark
            else:
                arr.append(normalizedLandmark.x - leftwrist.x)
                arr.append(normalizedLandmark.y - leftwrist.y)
                arr.append(normalizedLandmark.z - leftwrist.z)



        rightwrist = ''
        for point in mp_hands.HandLandmark :
            normalizedLandmark = righthand_landmarks.landmark[point]
            if point == mp_hands.HandLandmark.WRIST :
                rightwrist = normalizedLandmark
            else :
                arr.append(normalizedLandmark.x - rightwrist.x)
                arr.append(normalizedLandmark.y - rightwrist.y)
                arr.append(normalizedLandmark.z - rightwrist.z)

        main_arr = np.array(arr)

        return main_arr
