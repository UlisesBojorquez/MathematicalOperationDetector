import cv2 as cv
import imutils
import pytesseract
from pytesseract.pytesseract import image_to_string

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# Load the image
#image = cv.imread("pic5.jpg") #operacion.png pic.jpg

image = cv.VideoCapture(0)
# Pre-processing the image

while(True):
    #Read frame by frame
    ret, frame = image.read()
    
    #frame = imutils.resize(frame,width=700,height=500)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5,5), 0)
    edged = cv.Canny(blurred, 50, 200, 255)
    cnts,_=cv.findContours(edged,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        area = cv.contourArea(c)
        x,y,w,h = cv.boundingRect(c)
        epsilon = 0.055*cv.arcLength(c,True)
        approx = cv.approxPolyDP(c,epsilon,True)
        if len(approx) == 4 and area> 100 and area<120000:
            #print('area=',area)
            #cv.drawContours(frame,[c],0,(0,255,0),2)
            aspect_ratio = float(w)/h
            #print(aspect_ratio)
            if aspect_ratio > 2.4:
                operacion = gray[y:y+h,x:x+w]
                text = pytesseract.image_to_string(operacion, config='--psm 11')
                if "5" in text or "+" in text or "2" in text:
                    cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
                    cv.putText(frame,text,(x+20,y-10),1,2.2,(0,255,0),3)
                else:
                    cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
                    cv.putText(frame,"error",(x+20,y-10),1,2.2,(0,255,0),3)
                #print('text=',text)
                #cv.imshow("operacion", operacion)
                #cv.moveWindow("operacion",780,100)
                #cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
                #cv.putText(frame,text,(x+20,y-10),1,2.2,(0,255,0),3)
    cv.imshow("hola", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


# Results
image.release()
cv.destroyAllWindows()

