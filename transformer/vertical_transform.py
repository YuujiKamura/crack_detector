import numpy as np

def vertical_transform(cv2, weight, initial_dst, width, height):

    scale_factor = float(weight) * 0.01

    final_dst = cv2.resize(initial_dst, (width, int(height * scale_factor)))
    if final_dst.shape[0] > height:
        final_dst = final_dst[:height, :]
    else:
        padding = np.zeros((height - final_dst.shape[0], width, 3), dtype=np.uint8)
        final_dst = np.vstack((final_dst, padding))


    cv2.resizeWindow("Transformed", width, int( height*scale_factor ) )

    final_dst_copy = final_dst.copy()

    return final_dst_copy
