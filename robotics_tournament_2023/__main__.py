import cv2 as cv
import time
import wiringpi
# from ultralytics import YOLO

def main():
    wiringpi.wiringPiSetup()  
    print("Hello, World!")
    print(int(time.time()))
    wiringpi.pinMode(6, 1)       # Set pin 6 to 1 ( OUTPUT )
    wiringpi.digitalWrite(6, 1)  # Write 1 ( HIGH ) to pin 6
    wiringpi.digitalRead(6)
    

if __name__ == '__main__':
    main()