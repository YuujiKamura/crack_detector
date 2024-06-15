import cv2
from utils import select_file, copy_image_to_clipboard
from grid_controller import GridController
from transform_controller import TransformController
from settings_window import create_settings_window

def main():
    gc = GridController()
    tc = TransformController()

    success, img = select_file()
    if not success:
        print("画像が選択されないか、読み込まれませんでした。")

    img_selected = img.copy()
    tc.set_selected_image(img_selected)  # 元の画像を設定

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', lambda event, x, y, flags, param=img_selected: tc.select_points(cv2, event, x, y, flags, img_selected))

    while True:
        cv2.imshow('image', img_selected)
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # Enter key to break
            break
        if not tc.running:  # 右クリックでtc.runningがFalseになると待機状態を解除
            break

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
    gc.set_image("original", initial_dst.copy())  # 初期変換後の画像を保存

    cv2.namedWindow('Transformed')
    cv2.imshow('Transformed', gc.get_final_dst())

    root = create_settings_window(gc, cv2, copy_image_to_clipboard)

    root.mainloop()

if __name__ == "__main__":
    main()
