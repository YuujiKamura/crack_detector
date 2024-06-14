from PIL import Image
from transformer import update_vertical_transform
from draw_grid import draw_grid, toggle_highlight as draw_grid_toggle_highlight

class GridController:
    def __init__(self):
        self.highlighted_cells = {}
        self.is_drawing = False
        self.last_cell = None

        self.final_dst = None
        self.original_image = None
        self.transformed_image = None
        self.cracked_image = None
        self.images = {}

        self.width = 500
        self.height = 1000
        self.grid_size = 50
        self.line_thickness = 1
        self.font_scale = 0.5
        self.points = []

    def set_final_dst(self, dst, stage="default"):
        self.final_dst = dst
        self.images[stage] = dst

    def get_final_dst(self):
        return self.final_dst

    def get_image_by_stage(self, stage):
        return self.images.get(stage, None)

    def set_image_by_stage(self, stage, image):
        self.images[stage] = image

    def get_width_height(self):
        return self.width, self.height

    def get_grid_size(self):
        return self.grid_size

    def set_grid_size(self, size):
        self.grid_size = size

    def get_line_thickness(self):
        return self.line_thickness

    def set_line_thickness(self, thickness):
        self.line_thickness = thickness

    def get_font_scale(self):
        return self.font_scale

    def set_font_scale(self, scale):
        self.font_scale = scale

    def update_slider(self, cv2, value):
        self.final_dst = update_vertical_transform(cv2, value, self.get_image_by_stage("original").copy(), self.width, self.height, self.grid_size, self.line_thickness, self.font_scale, draw_grid)
        draw_grid( cv2, self.final_dst, self.grid_size, self.line_thickness, self.font_scale)
        self.set_final_dst(self.final_dst, stage="vertical_transformed")
        cv2.imshow('Transformed', self.final_dst)
        # ウィンドウのサイズを画像のサイズに合わせて変更
        cv2.resizeWindow('Transformed', self.final_dst.shape[1], self.final_dst.shape[0])

    def update_line_thickness(self, cv2, value):
        self.line_thickness = int(value)
        self.update_slider(cv2, self.slider.get())

    def update_font_scale(self, cv2, value):
        self.font_scale = float(value)
        self.update_slider(cv2, self.slider.get())

    def update_grid_size(self, cv2, size):
        self.grid_size = int(size)
        self.update_slider(cv2, self.slider.get())

    def draw_grid(self, cv2):
        if self.cracked_image is not None:
            img_copy = self.cracked_image.copy()
        elif self.transformed_image is not None:
            img_copy = self.transformed_image.copy()
        else:
            img_copy = self.final_dst.copy()

        draw_grid(cv2, img_copy, self.grid_size, self.line_thickness, self.font_scale)
        cv2.imshow('Transformed', img_copy)

    def copy_button_click(self, cv2, copy_image_to_clipboard, slider):
        if self.final_dst is not None:
            width, height = self.get_width_height()
            trimmed_height = int(height * (1.0 + (slider.get() - 50) / 100.0))
            if trimmed_height > height:
                trimmed_height = height
            trimmed_dst = self.final_dst[:trimmed_height, :]

            # グリッドを描画
            grid_img = trimmed_dst.copy()
            draw_grid(cv2, grid_img, self.grid_size, self.line_thickness, self.font_scale)

            img_pil = Image.fromarray(cv2.cvtColor(grid_img, cv2.COLOR_BGR2RGB))
            copy_image_to_clipboard(img_pil)
            print("変換結果がクリップボードにコピーされました。")

    def toggle_highlight(self, cv2, event, x, y, flags, param):
        draw_grid_toggle_highlight(cv2, event, x, y, flags, param, self.grid_size, self.line_thickness)
