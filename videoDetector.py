import cv2 as cv
import imutils
import pytesseract
from pytesseract.pytesseract import image_to_string
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


'''Obtain the input'''
# Video capture
camera = cv.VideoCapture(0)
widthSize = 640
heightSize = 480
# Declare the counter
img_counter = 0
# Declare name of the input image taken
img_name = "input.png"
# Manage error
successful = FalseglobalY,globalH, globalX,globalW = int(widthSize/4)-int(widthSize/8), int(heightSize/3), int(widthSize/4)*3 , int(heightSize/3)

if camera.isOpened() == False:               
    print ("error: capWebcam not accessed successfully\n")      
    os.system("pause")       
    
while(camera.isOpened()):
    #Read frame by frame
    ret, image = camera.read()
    
    image = imutils.resize(image, width = widthSize, height=heightSize)   
    reg = image
    if not ret:
        print("Failed to grab frame")
        break
    # Display screen
    x, y, w, h = int(widthSize/4)-int(widthSize/8), int(heightSize/3), int(widthSize/4)*3 , int(heightSize/3)
    sub_img = image[y:y+h, x:x+w]
    
    y_ref = y+h
    x_ref = x+w
    
    temp = image.copy()
    temp2 = image.copy()

    image = cv.GaussianBlur(image, (9, 9), 0)
    image[y_ref:y, x_ref:x] = temp[y_ref:y, x_ref:x]
    image = cv.rectangle(image, (x_ref, y_ref), (x, y), (242, 135, 115), 2)
    image[y:y+h, x:x+w] = reg[y:y+h, x:x+w]
    
    cv.imshow("Instructions: SPACE = Take picture, ESC = Exit",image)
    key = cv.waitKey(1)
    if key%256 == 27: # 27 is the ESC Key pressed
        print("Escape hit")
        break
    elif key%256 == 32: # 32 is the SPACE Key pressed
            imgRes = image[y:y+h, x:x+w]
            cv.imwrite(img_name, imgRes)
            successful = True
            print("Screenshot taken")

# Results
camera.release()
cv.destroyAllWindows()

'''Functions'''

def postProcessing(img):

    # Threshold to obtain binary image
    thresh = cv.threshold(img, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
    cv.imshow("thresh", thresh)

    # Create custom kernel
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
    # Perform closing (dilation followed by erosion)
    close = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

    # Invert image to use for Tesseract
    result = 255 - close

    return result

def preProcessing(img):
    print("[ <3 ] Staring pre-processing")

    # Load the image
    image = cv.imread(img) #operacion.png pic.jpg
    # Pre-processing the image
    #image = imutils.resize(image,width=700,height=500)
    # Convert it to gray scale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imshow("gray", gray)
    # Apply gaussian blur
    blurred = cv.GaussianBlur(gray, (5,5), 0)
    # Canny edge detector for the edge of the input
    edged = cv.Canny(blurred, 50, 200, 255)
    cv.imshow("edged", edged)
    # Detect contours
    cnts,_=cv.findContours(edged,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    #Iterate the countours founded
    for c in cnts:
        # Calculate the area of the contours
        area = cv.contourArea(c)
        # Get values from each contours painted
        x,y,w,h = cv.boundingRect(c)
        # Epsilon
        epsilon = 0.045*cv.arcLength(c,True)
        # Allows us to calculate the vertices of the contours
        approx = cv.approxPolyDP(c,epsilon,True)
        print("------------------")
        if len(approx) == 4 and area>90000: #and area> 70000 and area<100000
            print('area=',area)
            cv.drawContours(image,[c],0,(0,255,0),2)
            aspect_ratio = float(w)/h
            print("ratio"+ str(aspect_ratio))
            if aspect_ratio > 2.4:
                operacion = gray[globalY:globalY+globalH, globalX:globalX+globalW]
                operacionPost = postProcessing(operacion)
                text = pytesseract.image_to_string(operacionPost, config='--psm 11')
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