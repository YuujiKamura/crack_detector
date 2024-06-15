from tkinter import Tk, Scale, HORIZONTAL, Button, Label, Frame, OptionMenu, StringVar
from crack_detector import detect_cracks

def add_labeled_slider(frame, label_text, from_, to, orient, length, command, default_value, row, resolution=1):
    label = Label(frame, text=label_text)
    label.grid(row=row, column=0, sticky='e')
    slider = Scale(frame, from_=from_, to=to, orient=orient, length=length, command=command, resolution=resolution)
    slider.set(default_value)
    slider.grid(row=row, column=1, padx=10, pady=5)
    return slider

def create_settings_window(gc, cv2, copy_image_to_clipboard):
    root = Tk()
    root.title("Adjust Settings")

    frame = Frame(root)
    frame.pack(pady=10, padx=10)

    gc.slider = add_labeled_slider(
        frame, "Vertical Transform", 1, 200, HORIZONTAL, 400,
        lambda val: gc.update_slider(cv2, val), 20, 0
    )

    gc.grid_slider = add_labeled_slider(
        frame, "Grid Size", 10, 100, HORIZONTAL, 400,
        lambda val: gc.update_grid_size(cv2, val), 90, 1
    )

    gc.line_thickness_slider = add_labeled_slider(
        frame, "Line Thickness", 0, 10, HORIZONTAL, 400,
        lambda val: gc.update_line_thickness(cv2, val), 1, 2
    )

    copy_button = Button(root, text="Copy to Clipboard", command=lambda: gc.copy_button_click(cv2, copy_image_to_clipboard, gc.slider))
    copy_button.pack(pady=10)

    detect_cracks_button = Button(root, text="Detect Cracks", command=lambda: detect_and_update_cracks(gc, cv2))
    detect_cracks_button.pack(pady=10)

    gc.update_slider(cv2, 50)

    return root

def detect_and_update_cracks(gc, cv2):
    method = "canny"  # edge detection method, could be configurable
    threshold1 = 130
    threshold2 = 150

    cracked_image = detect_cracks(gc.transformed_image.copy(), method, threshold1, threshold2)
    gc.cracked_image = cracked_image

    gc.set_final_dst( gc.draw_grid(cv2), stage="cracked")
    cv2.imshow('Transformed', gc.get_final_dst())
