import cv2 as cv
import imutils
import pytesseract
from pytesseract.pytesseract import image_to_string

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# Load the image
image = cv.imread("operacion.png")
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
# Draw contours in image
#cv.drawContours(image,cnts,-1,(0,255,0),2)
#Erase the contours that we don'want
for c in cnts:
    # Calculate the area of the contours
    area = cv.contourArea(c)
    # Get values from each contours painted
    x,y,w,h = cv.boundingRect(c)
    # Epsilon
    epsilon = 0.0805*cv.arcLength(c,True)
    # Allows us to calculate the vertices of the contours
    approx = cv.approxPolyDP(c,epsilon,True)
    if len(approx) == 4 and area> 10000 and area<100000:
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

# Results
cv.imshow("Image", image)
cv.waitKey(0)
cv.destroyAllWindows()