import cv2
import numpy as np

def initial_perspective_transform(cv2, pts1, img, width, height):
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    M = cv2.getPerspectiveTransform(pts1, pts2)

    perspective_transformed = cv2.warpPerspective(img, M, (width, height))

    # 縦方向の比率を変更（手前をほんの少し延ばして奥を縮める処理
    stretch_factor = 0.2
    return apply_vertical_stretch(cv2, perspective_transformed, stretch_factor)

def apply_vertical_compression(cv2, img, compression_factor):
    height, width = img.shape[:2]
    map_y = np.zeros_like(img[:,:,0], dtype=np.float32)
    for y in range(height):
        scale = 1.0 - (compression_factor * (y / height))
        map_y[y, :] = y * scale

    map_x = np.tile(np.arange(width, dtype=np.float32), (height, 1))
    compressed_img = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)
    return compressed_img


def apply_vertical_stretch(cv2, img, stretch_factor):
    height, width = img.shape[:2]
    map_y = np.zeros_like(img[:, :, 0], dtype=np.float32)

    for y in range(height):
        # 画像の下部 (手前) を引き伸ばす
        scale = 1.0 + (stretch_factor * (1 - y / height))
        map_y[y, :] = y * scale

    map_x = np.tile(np.arange(width, dtype=np.float32), (height, 1))
    stretched_img = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)
    return stretched_img
