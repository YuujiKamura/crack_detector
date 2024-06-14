import numpy as np
from transformer import initial_perspective_transform

class TransformController:
    def __init__(self):
        self.points = []
        self.initial_dst = None
        self.original_image = None

    def set_original_image(self, img):
        self.original_image = img

    def select_points(self, cv2, event, x, y, flags, image_data):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.points) == 4:
                self.points = [(x, y)]
                image_data[:] = self.original_image.copy()  # 画像をリセット
                print(f"Reset points. New start point: ({x}, {y})")
            else:
                self.points.append((x, y))
                print(f"Point selected: ({x}, {y})")

            # 画像データに対して赤い点を描画
            if image_data is not None:
                cv2.circle(image_data, (x, y), 5, (0, 0, 255), -1)
                if len(self.points) > 1:
                    cv2.line(image_data, self.points[-2], self.points[-1], (0, 0, 255), 1)
                if len(self.points) == 4:
                    cv2.line(image_data, self.points[-1], self.points[0], (0, 0, 255), 1)  # 4点目と1点目を結ぶ
                cv2.imshow('image', image_data)
                cv2.waitKey(1)

    def get_points(self):
        return self.points

    def set_initial_dst(self, dst):
        self.initial_dst = dst

    def get_initial_dst(self):
        return self.initial_dst

    def transform_image(self, cv2, img, width, height):
        if len(self.points) != 4:
            print("4つのポイントを指定してください")
            return None

        pts1 = np.float32(self.points)
        self.initial_dst = initial_perspective_transform(cv2, pts1, img, width, height)
        return self.initial_dst
