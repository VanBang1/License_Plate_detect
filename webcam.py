from PIL import Image
import cv2
import torch
import math 
import function.utils_rotate as utils_rotate
from IPython.display import display
import os
import time
import argparse
import function.helper as helper

# load model
yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/LP_detector_nano_61.pt', force_reload=True, source='local')
yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/LP_ocr_nano_62.pt', force_reload=True, source='local')
yolo_license_plate.conf = 0.60 #0.60

prev_frame_time = 0
new_frame_time = 0 #0
#screenshot
#vid = cv2.VideoCapture(0)
#inser vid
vid = cv2.VideoCapture("1.mp4")
while(True):
    ret, frame = vid.read()
    plates = yolo_LP_detect(frame, size=3000)#640
    list_plates = plates.pandas().xyxy[0].values.tolist()
    list_read_plates = set()
    for plate in list_plates:
        flag = 0
        x = int(plate[0]) # xmin 0
        y = int(plate[1]) # ymin 1
        w = int(plate[2] - plate[0]) # xmax - xmin  2 0
        h = int(plate[3] - plate[1]) # ymax - ymin  3 1
        crop_img = frame[y:y+h, x:x+w]
        cv2.rectangle(frame, (int(plate[0]),int(plate[1])), (int(plate[2]),int(plate[3])), color = (0,0,225), thickness = 2) #2
        cv2.imwrite("crop.jpg", crop_img)
        rc_image = cv2.imread("crop.jpg")

        frame[y:y + h, x:x + w] = cv2.blur(frame[y:y + h, x:x + w], ksize=(10, 10))

        '''   lp = ""
        for cc in range(0,2):
            for ct in range(0,2):
                lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                if lp != "unknown":
                    list_read_plates.add(lp)
                    cv2.putText(frame, lp, (int(plate[0]), int(plate[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                    flag = 1
                    break
            if flag == 1:
                break
           '''
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    cv2.putText(frame, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()