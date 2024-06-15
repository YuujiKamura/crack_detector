import cv2
from tkinter import filedialog
from tkinter import Tk

def select_file():
    # Tkinterを使ってファイル選択ダイアログを表示
    root = Tk()
    root.withdraw()  # メインウィンドウを表示しない
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
    root.destroy()

    if not file_path:
        return False, None

    img = cv2.imread(file_path)
    if img is None:
        print(f"Error: Could not read image from {file_path}")
        return False, None

    return True, img
