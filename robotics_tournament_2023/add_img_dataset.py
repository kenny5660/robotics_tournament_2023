import cv2 as cv
import time
from ultralytics import YOLO

def main():
    print("Hello, World!")
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    model = YOLO('robotics.pt')
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        results = model.predict(frame, imgsz=640, conf=0.5, verbose=False)
        if results.__len__() > 0:
            for r in results:
                im_array = r.plot()
            cv.imshow('frame', im_array)
        else:
            cv.imshow('frame', frame)
        key = cv.waitKey(10)

        if key == ord('q'):
            break
        elif key == ord('p'):
            print("Saving image...")
            cv.imwrite(f'image-{int(time.time())}.jpg', frame)
    cap.release()
    cv.destroyAllWindows()
    

if __name__ == '__main__':
    main()