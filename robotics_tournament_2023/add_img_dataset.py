import numpy as np
import cv2 as cv
drawing = False # true if mouse is pressed
ix,iy = -1,-1
img = np.zeros((360,512,3), np.uint8)

def draw_rectanlge(event, x, y, flags, param):
        """ Draw rectangle on mouse click and drag """
        global ix,iy,drawing,mode
        # if the left mouse button was clicked, record the starting and set the drawing flag to True
        if event == cv.EVENT_LBUTTONDOWN:
            drawing = True
            ix,iy = x,y
        # mouse is being moved, draw rectangle
        elif event == cv.EVENT_MOUSEMOVE:
            if drawing == True:
                cv.rectangle(img, (ix, iy), (x, y), (255, 255, 0), -1)
        # if the left mouse button was released, set the drawing flag to False
        elif event == cv.EVENT_LBUTTONUP:
            drawing = False

def main():

    cv.namedWindow('image') 
    cv.setMouseCallback('image',draw_rectanlge)

    while(1):
        cv.imshow('image',img)
        if cv.waitKey(20) & 0xFF == 27:
            break
        
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()