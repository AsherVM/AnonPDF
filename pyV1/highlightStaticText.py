# pip3 install pytesseract, opencv-contrib-python
# Base code: https://betterprogramming.pub/highlighting-specific-word-in-an-input-image-1cf3d4f8ae27
# Works well, next step: 
#     font detect?
#     Replace text in image?
#     PII detect/spoof (new info)?


import pytesseract
from pytesseract import Output
import cv2

imgFilePath = '/Users/asher/Projects/AnonPDF/JS_resume.jpg'
filterWordsArr = ['test', 'EDUCATION', 'John']
padInt = 5

img = cv2.imread(imgFilePath)
testObj=pytesseract.image_to_data(img, output_type=Output.DICT)
d = testObj
n_boxes=len(d['level'])
overlay = img.copy()

for i in range(n_boxes):
    text = d['text'][i]
    if text in filterWordsArr:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        (x1, y1, w1, h1) = (d['left'][i + 1], d['top'][i + 1], d['width'][i + 1], d['height'][i + 1])
        (x2, y2, w2, h2) = (d['left'][i + 2], d['top'][i + 2], d['width'][i + 2], d['height'][i + 2])
        # cv2.rectangle(img, (x, y), (x1 + w1, y1 + h1), (0, 255, 0), 2)
        cv2.rectangle(overlay, (x - padInt, y - padInt), (x + w + padInt , y + h + padInt), (255, 0, 0), -1)
        # cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)
        # cv2.rectangle(overlay, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), -1)
        print(text)


alpha = 0.4  # Transparency factor.
# Following line overlays transparent rectangle over the image
img_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

r = 1000.0 / img_new.shape[1]  # resizing image without loosing aspect ratio
dim = (1000, int(img_new.shape[0] * r))
# perform the actual resizing of the image and show it
resized = cv2.resize(img_new, dim, interpolation=cv2.INTER_AREA)
cv2.imshow('img', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()