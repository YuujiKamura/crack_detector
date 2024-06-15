import cv2
import numpy as np

def initial_perspective_transform(cv2, pts1, img, width, height):
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    M = cv2.getPerspectiveTransform(pts1, pts2)

    perspective_transformed = cv2.warpPerspective(img, M, (width, height))

    # 縦方向の圧縮を適用
    #compression_factor = 0.8 # 圧縮の強さを調整
    #return apply_vertical_compression(cv2, perspective_transformed, compression_factor)

    #stretch_factor = 0.0
    #return apply_vertical_stretch(cv2, perspective_transformed, stretch_factor)

    return enhance_contrast( perspective_transformed )

def enhance_contrast(image, clip_limit=1, brightness_increase=50):
    # 画像をグレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # CLAHEオブジェクトを作成、clipLimitを高く設定
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))

    kernel_size = 5
    # ガウシアンフィルタを適用してノイズを除去
    blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    # CLAHEを適用してコントラストを強化
    enhanced = clahe.apply(gray)

    # 明るさを上げる
    brightened = cv2.add(enhanced, np.full(enhanced.shape, brightness_increase, dtype=enhanced.dtype))

    # グレースケール画像を3次元に変換して返す
    return cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)

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
