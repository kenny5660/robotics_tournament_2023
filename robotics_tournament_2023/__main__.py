import cv2 
import time
import wiringpi
from ultralytics import YOLO

def main():
    wiringpi.wiringPiSetup()  
    print("Hello, World!")
    print(int(time.time()))
    img = cv2.imread('./test.jpg')
    model = YOLO('robotics.pt')
    results = model.predict(img, imgsz=640, conf=0.5, verbose=False)
    if results.__len__() > 0:
            for r in results:
                im_array = r.plot()
    cv2.imwrite("result.jpg",im_array)

if __name__ == '__main__':
    main()