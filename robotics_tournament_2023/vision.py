import cv2
from rknnlite.api import RKNNLite
import argparse

import cv2.dnn
import numpy as np


CLASSES = ["BOTTLE","RED","WHITE"]
colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    """
    Draws bounding boxes on the input image based on the provided arguments.

    Args:
        img (numpy.ndarray): The input image to draw the bounding box on.
        class_id (int): Class ID of the detected object.
        confidence (float): Confidence score of the detected object.
        x (int): X-coordinate of the top-left corner of the bounding box.
        y (int): Y-coordinate of the top-left corner of the bounding box.
        x_plus_w (int): X-coordinate of the bottom-right corner of the bounding box.
        y_plus_h (int): Y-coordinate of the bottom-right corner of the bounding box.
    """
    label = f'{CLASSES[class_id]} ({confidence:.2f})'
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

class Vision:
    def __init__(self,model_path):
        self.rknn_lite = RKNNLite(verbose=False, verbose_file='./inference.log')
        ret = self.rknn_lite.load_rknn(model_path)

        ret = self.rknn_lite.init_runtime(core_mask=RKNNLite.NPU_CORE_AUTO)
        if ret != 0:
            print('Init runtime environment failed')
            exit(ret)

    def end(self):
        self.rknn_lite.release()

    def get_detections(self,input_image):

        original_image: np.ndarray = input_image
        [height, width, _] = original_image.shape

        # Prepare a square image for inference
        length = max((height, width))
        image = np.zeros((length, length, 3), np.uint8)
        image[0:height, 0:width] = original_image

        # Calculate scale factor
        scale = length / 640

        # resized = cv2.resize(original_image, (640,640), interpolation = cv2.INTER_AREA)
        resized = np.expand_dims(image, 0)

        outputs = self.rknn_lite.inference(inputs=[resized])

        # Prepare output array
        outputs = np.array([cv2.transpose(outputs[0][0])])
        rows = outputs.shape[1]

        boxes = []
        scores = []
        class_ids = []

        # Iterate through output to collect bounding boxes, confidence scores, and class IDs
        for i in range(rows):
            classes_scores = outputs[0][i][4:]
            (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
            if maxScore >= 0.25:
                box = [
                    outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                    outputs[0][i][2], outputs[0][i][3]]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)

        # Apply NMS (Non-maximum suppression)
        result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.5, 0.1, 0.1)

        detections = []

        # Iterate through NMS results to draw bounding boxes and labels
        for i in range(len(result_boxes)):
            index = result_boxes[i]
            box = boxes[index]
            detection = {
                'class_id': class_ids[index],
                'class_name': CLASSES[class_ids[index]],
                'confidence': scores[index],
                'box': box,
                'scale': scale}
            detections.append(detection)
            draw_bounding_box(original_image, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
                               round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))
        # Display the image with bounding boxes
        

        return detections,original_image

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame = cv2.flip(frame,0)
    vision = Vision('./robotics_nano.rknn')
    detections,plot_image = vision.get_detections(frame)
    cv2.imwrite('./result.jpg', plot_image)
    print(detections)

