import cv2
import numpy as np

def initial_perspective_transform(cv2, pts1, img, width, height):
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(img, M, (width, height))
