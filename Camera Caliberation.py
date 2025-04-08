import numpy as np
import cv2 as cv


def select_img_from_video(video_file, board_pattern, select_all = False, wait_msec=10, wnd_name='Camera Calibration'):
    # Open a video
    video = cv.VideoCapture(video_file)
    assert video.isOpened(), "영상 파일을 열 수 없습니다."

    # Select images
    img_select = []
    while True:
        valid, img = video.read()
        if not valid:
            break

        if select_all:
            img_select.append(img)
        else:
            # 원본 이미지 복사 및 텍스트 추가
            display = img.copy()
            cv.putText(display, f'NSelect: {len(img_select)}',
                       (20, 40), cv.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0))
            cv.imshow(wnd_name, display)

            # Process the key event
            key = cv.waitKey(wait_msec)
            if key == ord(' '):  # Space: Pause and show corners
                complete, pts = cv.findChessboardCorners(img, board_pattern)
                cv.drawChessboardCorners(display, board_pattern, pts, complete)
                cv.imshow(wnd_name, display)
                key = cv.waitKey()
                if key == ord('\r'):
                    img_select.append(img)  # Enter: Select the image
            if key == 27:  # ESC: Exit (Complete image selection)
                break

    cv.destroyAllWindows()
    return img_select


def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    # Find 2D corner points from given images
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0, "체스보드 코너 검출에 성공한 이미지가 없습니다."

    # Prepare 3D points of the chess board
    obj_pts = [[c, r, 0]
               for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) *
                  board_cellsize] * len(img_points)

    # Calibrate the camera
    return cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)


if __name__ == '__main__':
    video_file = 'data/newchessboard.mp4'
    board_pattern = (8, 6)   # 보드 패턴
    board_cellsize = 0.025   # 각 셀의 크기 25mm
    

    img_select = select_img_from_video(
        video_file, board_pattern)
    assert len(img_select) > 0, '선택된 이미지가 없습니다!'
    rms, K, dist_coeff, rvecs, tvecs = calib_camera_from_chessboard(
        img_select, board_pattern, board_cellsize)

    # Print calibration results
    print('## Camera Calibration Results')
    print(f'* The number of selected images = {len(img_select)}')
    print(f'* RMS error = {rms}')
    print(f'* Camera matrix (K) = \n{K}')
    print(
        f'* Distortion coefficient (k1, k2, p1, p2, k3, ...) = {dist_coeff.flatten()}')
    cap = cv.VideoCapture(video_file)
    if not cap.isOpened():
        raise Exception("비디오 파일을 열 수 없습니다.")

    # 비디오 속성 가져오기
    fps = cap.get(cv.CAP_PROP_FPS)
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter('data/undistortedchessboard.mp4',
                         fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # cv.undistort를 이용해 왜곡 제거 (보정 파라미터를 적용)
        undistorted_frame = cv.undistort(frame, K, dist_coeff)
        out.write(undistorted_frame)

    cap.release()
    out.release()
    cv.destroyAllWindows()
