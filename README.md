#License Plate Detection

## Installation

```bash
  git clone https://github.com/VanBang1/License_Plate_detect
  cd License-Plate-Recognition

  # install dependencies using pip 
  pip install -r ./requirement.txt
```

- **Pretrained model** provided in ./model folder in this repo 

- **Download yolov5 and copy yolov5 folder to project folder
## Run License Plate detect

```bash
  # run inference on webcam (15-20fps if there is 1 license plate in scene)
  python webcam.py 

  # run inference on folder image
  python lp_image.py

  # run LP_recognition.ipynb if you want to know how model work in each step
```

## Vietnamese Plate Dataset

This repo uses 2 sets of data for 2 stage of license plate recognition problem:

- [License Plate Detection Dataset](https://drive.google.com/file/d/1xchPXf7a1r466ngow_W_9bittRqQEf_T/view?usp=sharing)
- [Character Detection Dataset](https://drive.google.com/file/d/1bPux9J0e1mz-_Jssx4XX1-wPGamaS8mI/view?usp=sharing)

-This dataset is belong to [Mì Ai](https://www.miai.vn/thu-vien-mi-ai/) and [winter2897](https://github.com/winter2897/Real-time-Auto-License-Plate-Recognition-with-Jetson-Nano/blob/main/doc/dataset.md).

-This model based on this project https://github.com/Marsmallotr/License-Plate-Recognition.git
## Training

**Training code for Yolov5:**

Use code in ./training folder
```bash
  training/Plate_detection.ipynb     #for LP_Detection
  training/Letter_detection.ipynb    #for Letter_detection
```
