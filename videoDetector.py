import cv2 as cv
import imutils
import pytesseract
from pytesseract.pytesseract import image_to_string

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

'''Obtain the input'''
# Video capture
camera = cv.VideoCapture(0)
# Declare the counter
img_counter = 0
# Declare name of the input image taken
img_name = "input.png"
# Manage error
successful = False
while(True):
    #Read frame by frame
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame")
        break
    # 
    cv.imshow("Instructions: SPACE = Take picture, ESC = Exit",frame)
    key = cv.waitKey(1)
    if key%256 == 27: # 27 is the ESC Key pressed
        print("Escape hit")
        break
    elif key%256 == 32: # 32 is the SPACE Key pressed
            cv.imwrite(img_name, frame)
            successful = True
            print("Screenshot taken")

# Results
camera.release()
cv.destroyAllWindows()

'''Function'''
def preProcessing():
    print("[ <3 ] Staring pre.processing")

'''Pre-processing'''
if not successful:
    print("[ ! ] Not input image taken. Try again")
else:
    preProcessing()



