# OpenCV_Camera-Calibration
This is the camera calibration using open cv

## Camera Calibration Results

* **The number of selected images:** 4  
* **RMS error:** 1.3263262575554606  
* **Camera matrix (K):**

| | | |
|-|-|-|
|463.77380377|0|485.86564978|
|0|462.2257834|252.51163683|
|0|0|1|


### Distortion Coefficient

|k1|k1|p1|p2|k3|...|
|-|-|-|-|-|-|
|-1.2699291e-01|5.50924856e-01|-5.13339561e-03|-4.75228044e-04|-4.75228044e-04|

#### Distortion Correction
* Camera Caliberation을 통해 얻은 카메라 행렬(K)과 왜곡 계수(distortion coefficient)를 기반으로 
cv.undistort(frame, K, dist_coeff) 함수를 적용하여 입력 영상의 렌즈 왜곡을 보정.
보정된 결과는 undistortedchessboard.mp4 파일로 생성.

## ScreenShots
* Camera Caliberation Screenshots





