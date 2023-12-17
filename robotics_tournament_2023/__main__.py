import cv2 
import time
from  robotics_tournament_2023.vision import Vision
from robotics_tournament_2023.kangaroo_x2  import Kangaroo_x2, Kangaroo_x2_Motor
from robotics_tournament_2023.omni_wheel  import omni_wheel_3
from robotics_tournament_2023.motor  import Motor_gpio
from robotics_tournament_2023.servo import Servo
import serial as pyserial
import wiringpi

BUTTON_START_1 = 16
BUTTON_START_2 = 15
FRAME_CENTER = (320,240)

serial = pyserial.Serial( '/dev/ttyS2', 115200)
kanga_130 = Kangaroo_x2(130,serial)
kanga_135 = Kangaroo_x2(135,serial)

def main():
    global kanga_130,kanga_135
    wiringpi.wiringPiSetup()  
    wiringpi.pinMode(BUTTON_START_1, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(BUTTON_START_2, wiringpi.GPIO.INPUT)
    wiringpi.pullUpDnControl(BUTTON_START_1, 2)
    wiringpi.pullUpDnControl(BUTTON_START_2, 2)
    motor_L = Motor_gpio(27,25)
    motor_R = Motor_gpio(26,23)
    motor_L.stop()
    motor_R.stop()
    servo_bot = Servo(2)
    servo_top = Servo(21)

    print("Hello, World!")


    motorA = Kangaroo_x2_Motor(kanga_130, '1', 3,inverted=False)
    motorB = Kangaroo_x2_Motor(kanga_130, '2', 3,inverted=True)
    motorC = Kangaroo_x2_Motor(kanga_135, '1', 3,inverted=False)
    omni = omni_wheel_3(motorA,motorB,motorC,radius=1)#100mm
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    vision = Vision('./robotics_nano.rknn')

    counter_motors_start = 0
    omni.stop()

    while(wiringpi.digitalRead(BUTTON_START_2)):
            time.sleep(0.3)
            print("wait button")
            motor_L.stop()
            motor_R.stop()
            kanga_130.CmdStart(chnl='1')
            kanga_130.CmdStart(chnl='2')
            kanga_135.CmdStart(chnl='1')

    kanga_130.CmdStart(chnl='1')
    kanga_130.CmdStart(chnl='2')
    kanga_135.CmdStart(chnl='1')
    
    servo_bot.attach()
    servo_bot.move_angle(100)

    servo_top.attach()
    servo_top.move_angle(160)

    motor_L.MoveContinue(-100)
    motor_R.MoveContinue(-100)
    # omni.move2(0,500,0)
    # time.sleep(4)
    # omni.stop()
    # motor_L.stop()
    # motor_R.stop()
    omni.move2(0,500,0)
    counter = 0
    while True:
        start_frame_time = time.time()
        ret, frame = cap.read()
        frame = cv2.flip(frame,0)
        original = frame.copy()
        frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_AREA)
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        detections,plot_image = vision.get_detections(frame)
        flow_object(omni,detections)
        counter +=1
        counter_motors_start += 1
        if wiringpi.digitalRead(BUTTON_START_1) == 0:
            kanga_130.CmdStart(chnl='1')
            kanga_130.CmdStart(chnl='2')
            kanga_135.CmdStart(chnl='1')

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
    
    
counter_flow = 0
def flow_object(omni,detections):
    global kanga_130,kanga_135
    TIMEOUT = 40
    P = -0.17
    SPEED = 400
    global counter_flow
    # SPEED = 0
    center_pt,max_index = nearest_object(detections)
    if max_index is not None:
        print(center_pt,detections[max_index]["class_name"])
        error = FRAME_CENTER[0] - center_pt[0]
        counter_flow = 0
    else:
        counter_flow +=1
        error = 0
    if counter_flow < TIMEOUT:
        omni.move2(0,SPEED,error*P)
        print(counter_flow)
    else:
        kanga_130.CmdStart(chnl='1')
        kanga_130.CmdStart(chnl='2')
        kanga_135.CmdStart(chnl='1')
        print("error_detect")
        omni.move2(0,-SPEED,-350)
        if counter_flow > TIMEOUT+5:
            counter_flow = 0


if __name__ == '__main__':
    main()