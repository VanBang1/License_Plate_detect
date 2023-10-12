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

import glob
import os.path

#ap = argparse.ArgumentParser()
#ap.add_argument('-i', '--image', required=True, help='path to input image')
#args = ap.parse_args()

yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/LP_detector.pt', force_reload=True, source='local')
yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/LP_ocr.pt', force_reload=True, source='local')
yolo_license_plate.conf = 0.60 #0.60
def xuly_boundingbox(img):
    img = cv2.imread(img)
    plates = yolo_LP_detect(img, size=1000)
    list_plates = plates.pandas().xyxy[0].values.tolist()
    list_read_plates = set()

    if len(list_plates) == 0:
        lp = helper.read_plate(yolo_license_plate,img)
        if lp != "unknown":
            cv2.putText(img, lp, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (24,255,12), 2)
            #cv2.putText(img, lp, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            list_read_plates.add(lp)
    else:
        for plate in list_plates:
            flag = 0
            x = int(plate[0]) # xmin
            y = int(plate[1]) # ymin
            w = int(plate[2] - plate[0]) # xmax - xmin
            h = int(plate[3] - plate[1]) # ymax - ymin
            crop_img = img[y:y+h, x:x+w]
            cv2.rectangle(img, (int(plate[0]),int(plate[1])), (int(plate[2]),int(plate[3])), color = (0,0,225), thickness = 2)
            cv2.imwrite("crop.jpg", crop_img)
            rc_image = cv2.imread("crop.jpg")
    #blur the plate
        # img[y:y + h, x:x + w] = cv2.blur(img[y:y + h, x:x + w], ksize=(10, 10))
    #read the license number
        ''' lp = ""
            for cc in range(0,2):
                for ct in range(0,2):
                    lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                    if lp != "unknown":
                        list_read_plates.add(lp)
                        cv2.putText(img, lp, (int(plate[0]), int(plate[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                        flag = 1
                        break
                if flag == 1:
                    break              
                '''
    #cv2.imwrite("image_blurred1.jpg", img)
    return img
#cv2.imshow('frame', img)
#cv2.waitKey()

#Input folder name
path = glob.glob("folder2/*.jpg")

for file in path:
    print(file)
    file_name = os.path.basename(file)
    img = xuly_boundingbox(file)
    #cv2.imshow('frame', img)
    #Output folder name (tu tao)
    cv2.imwrite(f"folder2_xl/{file_name}", img)
cv2.destroyAllWindows()