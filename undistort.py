import cv2
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
    cv2.setMouseCallback('image', lambda event, x, y, flags, param=img_copy: tc.select_points(cv2, event, x, y, flags, img_copy))

    cv2.imshow('image', img_copy)
    print("画像上で4つのポイントをクリックしてください（左上、右上、右下、左下の順序で）")
    cv2.waitKey(0)

    points = tc.get_points()
    if len(points) != 4:
        print("4つのポイントを指定してください")
        return

    # オリジナルの画像を渡す
    initial_dst = tc.transform_image(cv2, img, gc.get_width_height()[0], gc.get_width_height()[1])
    if initial_dst is None:
        return

    gc.set_final_dst(initial_dst)
    gc.original_image = initial_dst.copy()  # オリジナルの画像を保持
    gc.set_image_by_stage("original", initial_dst.copy())  # 初期変換後の画像を保存

    root = create_settings_window(gc, cv2, copy_image_to_clipboard)

    cv2.namedWindow('Transformed')
    cv2.imshow('Transformed', gc.get_final_dst())

    root.mainloop()

if __name__ == "__main__":
    main()
