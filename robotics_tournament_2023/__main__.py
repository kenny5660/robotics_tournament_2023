import cv2 
import time
from  robotics_tournament_2023.vision import Vision
from robotics_tournament_2023.kangaroo_x2  import Kangaroo_x2, Kangaroo_x2_Motor
from robotics_tournament_2023.omni_wheel  import omni_wheel_3
import serial as pyserial
import wiringpi

BUTTON_START_1 = 16
BUTTON_START_2 = 15
FRAME_CENTER = (320,240)

def main():
    wiringpi.wiringPiSetup()  
    wiringpi.pinMode(BUTTON_START_1, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(BUTTON_START_2, wiringpi.GPIO.INPUT)
    wiringpi.pullUpDnControl(BUTTON_START_1, 2)
    wiringpi.pullUpDnControl(BUTTON_START_2, 2)
    print("Hello, World!")
    serial = pyserial.Serial( '/dev/ttyS2', 115200)
    kanga_130 = Kangaroo_x2(130,serial)
    kanga_135 = Kangaroo_x2(135,serial)
    motorA = Kangaroo_x2_Motor(kanga_130, '1', 3,inverted=False)
    motorB = Kangaroo_x2_Motor(kanga_130, '2', 3,inverted=True)
    motorC = Kangaroo_x2_Motor(kanga_135, '1', 3,inverted=False)
    omni = omni_wheel_3(motorA,motorB,motorC,radius=1)#100mm



    omni.stop()

    while(wiringpi.digitalRead(BUTTON_START_2)):
        pass

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    vision = Vision('./robotics_nano.rknn')
    counter = 0
    while True:
        start_frame_time = time.time()
        ret, frame = cap.read()
        frame = cv2.flip(frame,0)
        original = frame.copy()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        detections,plot_image = vision.get_detections(frame)
        flow_object(detections)
        counter +=1
        if (counter >30):
            cv2.imwrite(f'./robot-dataset/original-{int(time.time())}.jpg', original)
            cv2.imwrite(f'./robot-dataset/plot-{int(time.time())}.jpg', plot_image)
            counter = 0
        # print("fps = ",1/(time.time()-start_frame_time))
        # print(detections)

    cap.release()
    vision.end()


def center_of_max_object(detections):
    if len(detections) < 1:
        return None, None
    max_area = 0
    max_index = -1
    i = 0
    for det in detections:
        if det["class_id"] == 2 or det["class_id"] == 1:
            area = det["box"][0]-det["box"][2]*det["box"][1]-det["box"][3]
            if max_area < area:
                max_area = area
                max_index = i
        i += 1

    det = detections[max_index]
    center_pt = (det["box"][0] + (det["box"][0]-det["box"][2] / 2),det["box"][1] + (det["box"][1]-det["box"][3]) /2)
    return center_pt,max_index

def nearest_object(detections):
    if len(detections) < 1:
        return None, None
    max_y= 0
    max_pt = (0,0)
    max_index = -1
    i = 0
    for det in detections:
        if det["class_id"] == 2 or det["class_id"] == 1:
            center_pt = (det["box"][0] + (det["box"][0]-det["box"][2] / 2),det["box"][1] + (det["box"][1]-det["box"][3]) /2)
            if max_y < center_pt[1]:
                max_y = center_pt[1]
                max_index = i
                max_pt = center_pt
        i += 1
    if max_index >= 0 :
        return max_pt,max_index
    else:
        return None,None
    
    

def flow_object(detections):
   center_pt,max_index = nearest_object(detections)
   if max_index is not None:
        print(center_pt,detections[max_index]["class_name"])
        error = FRAME_CENTER[0] - center_pt[0]
        
        


if __name__ == '__main__':
    main()