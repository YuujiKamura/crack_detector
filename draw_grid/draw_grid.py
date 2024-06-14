import cv2

def draw_grid(cv2, img, grid_size, line_thickness, font_scale):
    if line_thickness == 0: return

    height, width = img.shape[:2]
    for i in range(0, width, grid_size):
        cv2.line(img, (i, 0), (i, height), (0, 165, 255), line_thickness)
    for j in range(0, height, grid_size):
        cv2.line(img, (0, j), (width, j), (0, 165, 255), line_thickness)

def update_cell(cv2, img, x, y, grid_size, line_thickness, font_scale, state):
    # セルの状態を更新するロジック
    # 仮にstateが0なら消去、1なら斜線、2ならバッテンのロジックとする
    cell_x = (x // grid_size) * grid_size
    cell_y = (y // grid_size) * grid_size

    if state == 1:
        cv2.line(img, (cell_x, cell_y), (cell_x + grid_size, cell_y + grid_size), (0, 0, 255), line_thickness)
    elif state == 2:
        cv2.line(img, (cell_x + grid_size, cell_y), (cell_x, cell_y + grid_size), (0, 0, 255), line_thickness)
    elif state == 0:
        # 背景色で塗りつぶす
        cv2.rectangle(img, (cell_x, cell_y), (cell_x + grid_size, cell_y + grid_size), (255, 255, 255), -1)

def toggle_highlight(cv2, event, x, y, flags, param, grid_size, line_thickness, font_scale):
    # グリッドのハイライトの切り替えロジック
    if event == cv2.EVENT_LBUTTONDOWN:
        update_cell(cv2, param, x, y, grid_size, line_thickness, font_scale, 1)
        cv2.imshow('Transformed', param)
    elif event == cv2.EVENT_LBUTTONUP:
        update_cell(cv2, param, x, y, grid_size, line_thickness, font_scale, 2)
        cv2.imshow('Transformed', param)
