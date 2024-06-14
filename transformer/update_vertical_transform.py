import numpy as np

def update_vertical_transform( cv2, weight, initial_dst, width, height, grid_size, line_thickness, font_scale, draw_grid):
    weight = float(weight) / 100.0
    scale_factor = 1.0 + (weight - 0.5)

    final_dst = cv2.resize(initial_dst, (width, int(height * scale_factor)))
    if final_dst.shape[0] > height:
        final_dst = final_dst[:height, :]
    else:
        padding = np.zeros((height - final_dst.shape[0], width, 3), dtype=np.uint8)
        final_dst = np.vstack((final_dst, padding))

    final_dst_copy = final_dst.copy()
    draw_grid( cv2, final_dst_copy, grid_size, line_thickness, font_scale)
    return final_dst_copy
