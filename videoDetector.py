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
    # Display screen
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
def preProcessing(img):
    print("[ <3 ] Staring pre-processing")

    # Load the image
    image = cv.imread(img) #operacion.png pic.jpg
    # Pre-processing the image
    image = imutils.resize(image,width=700,height=500)
    # Convert it to gray scale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Apply gaussian blur
    blurred = cv.GaussianBlur(gray, (5,5), 0)
    # Canny edge detector for the edge of the input
    edged = cv.Canny(blurred, 50, 200, 255)
    # Detect contours
    cnts,_=cv.findContours(edged,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    #Iterate the countours founded
    for c in cnts:
        # Calculate the area of the contours
        area = cv.contourArea(c)
        # Get values from each contours painted
        x,y,w,h = cv.boundingRect(c)
        # Epsilon
        epsilon = 0.065*cv.arcLength(c,True)
        # Allows us to calculate the vertices of the contours
        approx = cv.approxPolyDP(c,epsilon,True)
        if len(approx) == 4 and area> 70000 and area<100000: #and area> 10000 and area<100000
            print('area=',area)
            cv.drawContours(image,[c],0,(0,255,0),2)
            aspect_ratio = float(w)/h
            if aspect_ratio > 2.4:
                operacion = gray[y:y+h,x:x+w]
                text = pytesseract.image_to_string(operacion, config='--psm 11')
                print('text=',text)
                cv.imshow("operacion", operacion)
                cv.moveWindow("operacion",780,100)
                cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
                cv.putText(image,text,(x+20,y-10),1,2.2,(0,255,0),3)

    cv.imshow("Image", image)
    cv.waitKey(0)
    cv.destroyAllWindows()

'''Pre-processing'''
if not successful:
    print("[ ! ] Not input image taken. Try again")
else:
    preProcessing(img_name)