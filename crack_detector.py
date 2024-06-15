import cv2
import numpy as np

def enhance_contrast(image, clip_limit):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    return enhanced

def detect_edges(image, method='canny', threshold1=100, threshold2=200):
    if method == 'canny':
        edges = cv2.Canny(image, threshold1, threshold2)
    elif method == 'sobel':
        sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
        sobel_combined = cv2.sqrt(sobelx ** 2 + sobely ** 2)
        edges = cv2.convertScaleAbs(sobel_combined)
    elif method == 'laplacian':
        edges = cv2.Laplacian(image, cv2.CV_64F)
        edges = cv2.convertScaleAbs(edges)
    else:
        raise ValueError(f"Unknown edge detection method: {method}")
    return edges

def detect_cracks(image, method='canny', threshold1=100, threshold2=200, clip_limit=2.0):
    enhanced = enhance_contrast(image, clip_limit)
    edges = detect_edges(enhanced, method, threshold1, threshold2)

    if len(edges.shape) == 3:
        edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)

    if edges.dtype != np.uint8:
        edges = cv2.convertScaleAbs(edges)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    crack_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10:
            cv2.drawContours(image, [contour], -1, (0, 150, 255), 1)
            crack_area += area * 10

    total_area = image.shape[0] * image.shape[1]
    crack_percentage = (crack_area / total_area) * 100

    # クラック面積の割合を画像に描画
    text = f" total_area: {total_area:.1f} crack_area: {crack_area:.1f} / {crack_percentage:.1f}%"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 2
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_x = 10
    text_y = 30
    text_color = (0, 0, 0)
    cv2.putText(image, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

    return image

