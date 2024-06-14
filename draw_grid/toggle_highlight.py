import cv2
from .draw_grid import draw_grid, update_cell

def toggle_highlight(event, x, y, flags, param, grid_size, line_thickness, font_scale):
    global highlighted_cells, is_drawing, last_cell

    if param is None or not hasattr(param, 'shape'):
        print(f"Unexpected param type: {type(param)}")
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        is_drawing = True
        last_cell = update_cell(x, y, grid_size)

    elif event == cv2.EVENT_MOUSEMOVE:
        if is_drawing:
            current_cell = (x // grid_size, y // grid_size)
            if current_cell != last_cell:
                last_cell = update_cell(x, y, grid_size)

    elif event == cv2.EVENT_LBUTTONUP:
        is_drawing = False
        update_cell(x, y, grid_size)

    param_copy = param.copy()
    draw_grid(param_copy, grid_size, line_thickness, font_scale)
    cv2.imshow('Transformed', param_copy)
