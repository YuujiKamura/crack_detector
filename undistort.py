import cv2

from draw_grid import draw_grid
from transformer import update_vertical_transform
from utils import select_file, copy_image_to_clipboard
from grid_controller import GridController
from transform_controller import TransformController
from settings_window import create_settings_window


def main():
    gc = GridController()
    tc = TransformController()

    image_path = select_file()
    if not image_path:
        print("画像が選択されませんでした。")
        return

    img = cv2.imread(image_path)
    if img is None:
        print(f"画像が読み込まれませんでした。パスを確認してください: {image_path}")
        return

    img_copy = img.copy()
    tc.set_original_image(img_copy)  # 元の画像を設定

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',
                         lambda event, x, y, flags, param=img_copy: tc.select_points(cv2, event, x, y, flags, img_copy))

    cv2.imshow('image', img_copy)
    print("画像上で4つのポイントをクリックしてください（左上、右上、右下、左下の順序で）")
    cv2.waitKey(0)

    points = tc.get_points()
    if len(points) != 4:
        print("4つのポイントを指定してください")
        return

    # オリジナルの画像を渡す
    original_dst = tc.transform_image(cv2, img, gc.get_width_height()[0], gc.get_width_height()[1])
    if original_dst is None:
        return

    gc.set_final_dst(original_dst, stage="original")

    # 初回の縦方向変換を適用
    vertical_transformed_dst = update_vertical_transform(cv2, 50, original_dst, gc.get_width_height()[0],
                                                         gc.get_width_height()[1], gc.grid_size, gc.line_thickness,
                                                         gc.font_scale, draw_grid)
    gc.set_final_dst(vertical_transformed_dst, stage="vertical_transformed")

    root = create_settings_window(gc, cv2, copy_image_to_clipboard)

    cv2.namedWindow('Transformed')
    cv2.imshow('Transformed', gc.get_final_dst())
    cv2.setMouseCallback('Transformed',
                         lambda event, x, y, flags, param=gc.get_final_dst(): gc.toggle_highlight(cv2, event, x, y,
                                                                                                  flags, param))

    root.mainloop()


if __name__ == "__main__":
    main()
