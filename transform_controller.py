import cv2
import numpy as np
from transformer import initial_perspective_transform

class TransformController:
    def __init__(self):
        self.points = []
        self.initial_dst = None
        self.original_image = None
        self.dragging_point_index = None
        self.running = True

    def set_selected_image(self, image):
        self.original_image = image.copy()

    def select_points(self, cv2, event, x, y, flags, image_data):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.dragging_point_index = self.get_nearest_point_index(x, y)
            if self.dragging_point_index is None:
                if len(self.points) == 4:
                    self.points = [(x, y)]
                    image_data[:] = self.original_image.copy()  # 画像をリセット
                    print(f"Reset points. New start point: ({x}, {y})")
                else:
                    self.points.append((x, y))
                    print(f"Point selected: ({x}, {y})")
            self.draw_points_and_lines(cv2, image_data)
            cv2.imshow('image', image_data)

        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            if self.dragging_point_index is not None:
                self.points[self.dragging_point_index] = (x, y)
                image_data[:] = self.original_image.copy()  # 画像をリセット
                self.draw_points_and_lines(cv2, image_data)
                cv2.imshow('image', image_data)

        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging_point_index = None

        elif event == cv2.EVENT_RBUTTONDOWN:
            print("Right button clicked, stopping waitKey.")
            self.running = False

    def draw_points_and_lines(self, cv2, image_data):
        c_white = (255,255,255)
        c_red = (0,0,255)

        if image_data is not None:
            for point in self.points:
                cv2.circle(image_data, point, 5, c_red, -1)
            if len(self.points) > 1:
                for i in range(len(self.points) - 1):
                    cv2.line(image_data, self.points[i], self.points[i + 1], c_white, 1)
            if len(self.points) == 4:
                cv2.line(image_data, self.points[-1], self.points[0], c_white, 1)  # 4点目と1点目を結ぶ

    def get_nearest_point_index(self, x, y, threshold=10):
        for i, (px, py) in enumerate(self.points):
            if abs(px - x) < threshold and abs(py - y) < threshold:
                return i
        return None

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
