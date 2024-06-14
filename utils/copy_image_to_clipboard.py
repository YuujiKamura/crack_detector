import win32clipboard
import io
from PIL import Image

def copy_image_to_clipboard(image):
    output = io.BytesIO()
    image.save(output, format="BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()
