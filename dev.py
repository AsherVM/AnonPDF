from presidio_analyzer import AnalyzerEngine, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
#
import pytesseract
from pytesseract import Output
import cv2
#
import json
from pprint import pprint



imgFilePath = '/Users/asher/Projects/AnonPDF/JS_resume.jpg'
img = cv2.imread(imgFilePath)

imgStr=pytesseract.image_to_string(img)
imgObj = pytesseract.image_to_data(img, output_type=Output.DICT)
imgStrToScan = imgStr # Make copy

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry

registry = RecognizerRegistry()
registry.load_predefined_recognizers()

# Add the recognizer to the existing list of recognizers
# registry.add_recognizer(titles_recognizer )

# Set up analyzer with our updated recognizer registry
analyzer = AnalyzerEngine(registry=registry)
# analyzer = AnalyzerEngine(default_score_threshold=0.0)
analyzer_results = analyzer.analyze(text=imgStrToScan, language='en')
print(analyzer_results)

print(imgStr)
print('\n\n\n\n')
# print(analyzer_results.text)

PIIStrArr=[]
for result in analyzer_results:
	# print(type(result))
	PIIStr = imgStrToScan[result.start:result.end]
	print(PIIStr)
	PIIStrLen = len(PIIStr)
	PIIStrArr.append(PIIStr)

pprint(PIIStrArr)

filterWordsArr = PIIStrArr
padInt = 5


# imgObj = pytesseract.image_to_data(img, output_type=Output.DICT)


d = imgObj
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


