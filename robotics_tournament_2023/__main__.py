import cv2 
import time
from  robotics_tournament_2023.vision import Vision

def main():
    print("Hello, World!")
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
        counter +=1
        if (counter >30):
            cv2.imwrite(f'./robot-dataset/original-{int(time.time())}.jpg', original)
            cv2.imwrite(f'./robot-dataset/plot-{int(time.time())}.jpg', plot_image)
            counter = 0
        print("fps = ",1/(time.time()-start_frame_time))
        print(detections)

    cap.release()
    vision.end()
    

if __name__ == '__main__':
    main()