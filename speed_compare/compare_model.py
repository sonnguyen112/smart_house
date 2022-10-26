import cv2
import face_recognition
import time
from mtcnn import MTCNN

def face_recognize_model(img):
    if not(img is None):
        start_time = time.perf_counter()
        face_loc = face_recognition.face_locations(img)
        end_time = time.perf_counter()
        print(face_loc)
        print(end_time - start_time)


def mtcnn_model(img):
    detector = MTCNN()
    start_time = time.perf_counter()
    face_loc = detector.detect_faces(img)
    end_time = time.perf_counter()
    print(face_loc)
    print(end_time - start_time)


# webcam = cv2.VideoCapture(0)
# time.sleep(5)
# isTrue, img = webcam.read()
# cv2.imwrite("test.jpg", img)
# print("Da ghi")

img = cv2.imread(r"/home/pi/data/smart_house/src/smart_door/face_accept/dark_son.jpg")
face_recognize_model(img)
mtcnn_model(img)