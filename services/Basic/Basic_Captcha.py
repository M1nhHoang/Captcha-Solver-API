from PIL import Image
import pytesseract
import sys

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def predict(img):
    im = img.convert("L")
    # 1. threshold the image
    threshold = 120
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    out = im.point(table, '1').resize((145, 50))
    # out.show()
    # 2. recognize with tesseract
    num = pytesseract.image_to_string(out, lang='eng')
    return num.split("\n")[0]