#Use the face_recognition library
import cv2
import face_recognition
import time
#import RPi.GPIO as GPIO
import serial
import requests
import threading
import gtts
import os
from playsound import playsound
# import pyttsx3
from utils import util


#GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of boardnumbers
#RELAIS_1_GPIO = 17
#GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
# ser = serial.Serial("/dev/rfcomm1", 9600, timeout = 1)

path_known_images = ["/home/pi/data/smart_house/src/smart_door/face_accept/" + file for file in os.listdir("/home/pi/data/smart_house/src/smart_door/face_accept")]
encode_known_images = []

for path in path_known_images:
    image = face_recognition.load_image_file(path)
    encode_known_images.append(face_recognition.face_encodings(image)[0])

serial_door = serial.Serial("/dev/rfcomm1", 9600)

time.sleep(2)

r_file = open("/home/pi/data/smart_house/src/backend/extra_files/wanIP.txt", "r")
WAN_IP = r_file.read()
r_file.close()
print("WANIP=", WAN_IP)

print("Done set up")

class SmartDoor:
    def __init__(self):
        self.ser = serial_door
        self.is_stop = False
        self.is_lock = False
        self.img_for_process = None
        self.is_exit = False
        # self.capture = cv2.VideoCapture("rtsp://admin:Son[1122002]@192.168.1.12/cam/realmonitor?channel=1&subtype=00&authbasic=YWRtaW46TDJENjNGOTQ=")
        self.capture = cv2.VideoCapture(0)

    def face_recognize(self):
        start_time = time.perf_counter()
        if not(self.img_for_process is None):
            print("Processing...")
            img = self.img_for_process
            cv2.imwrite("test.jpg", img)
            face_enc = face_recognition.face_encodings(img)
            if len(face_enc) != 0:
                face_enc = face_enc[0]
                result = face_recognition.compare_faces(encode_known_images, face_enc)
                if True in result:
                    print("Unlock")
                    time.sleep(1)
                    #GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
                    try:
                        self.ser.write(b'0')
                        requests.get("http://{}/smart_door/set_status?status=0".format(WAN_IP), timeout=2)
                        util.update_status_is_watching(False)
                        self.is_exit = True
                        self.capture.release()
                        print("Release Camera")
                        sound_unlock = threading.Thread(target=self.play_sound, args=("Đã mở khóa", "vi"))
                        sound_unlock.start()
                        #time.sleep(10)
                        #GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
                        #self.ser.write(b"0")
                    except Exception as e:
                        # self.ser = serial.Serial("/dev/rfcomm1", 9600, timeout = 1)
                        # time.sleep(0.1)
                        print(e)
                    return
                else:
                    sound_invalid = threading.Thread(target=self.play_sound, args=("Khuôn mặt không hợp lệ", "vi"))
                    sound_invalid.start()
            print("Done Processing")
            self.img_for_process = None
            end_time = time.perf_counter()
            print(end_time - start_time)

    def read_ip_cam(self):
        while 1:
            if self.is_stop or self.is_exit:
                print("Stop Watching")
                return
            else:
                try:
                    isTrue, img = self.capture.read()
                    while isTrue == False:
                        pass
                    # img = cv2.resize(img, (img.shape[1]//2,img.shape[0]//2))
                    self.img_for_process = img
                except Exception as e:
                    print(e)

    def play_sound(self, text, language):
        tts = gtts.gTTS(text, lang = language)
        tts.save("{}.mp3".format(text))
        playsound("{}.mp3".format(text))
        os.remove("{}.mp3".format(text))
            
    
    def watch(self):
        reader = threading.Thread(target=self.read_ip_cam)
        reader.start()
        while True:
            if self.is_stop:
                print("Stop")
                self.ser.write(b'0')
                self.capture.release()
                util.update_status_is_watching(False)
                sound_unlock = threading.Thread(target=self.play_sound, args=("Đã mở khóa", "vi"))
                sound_unlock.start()
                return
            if self.is_lock == False:
                try:
                    print("Lock")
                    self.ser.write(b'1')
                    self.is_lock = True
                    sound_lock = threading.Thread(target=self.play_sound, args=("Đã khóa", "vi"))
                    sound_lock.start()
                except:
                    util.update_status_is_watching(False)
                    return
            # print("Watching...")
            self.face_recognize()
            if self.is_exit:
                print("Exit")
                return
            # cv2.imshow("Image", img)
            # if cv2.waitKey(20) != -1:
            #     break

# runner = SmartDoor()
# runner.watch()