#Use this code to find image coordinates from image:
import cv2
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        
        #place coordiantes on the image as text
        cv2.putText(img, str(x) + ',' + str(y), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        cv2.imshow('image', img)
        
        #Draw point on the image 
        cv2.circle(img, (x,y), 3, (0,255,255), -1)
        
    # checking for right mouse clicks     
    if event==cv2.EVENT_RBUTTONDOWN:
  
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
  
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('image', img)
    
#read the input image
img = cv2.imread('Study room_additions.png', 1)

#display the image
cv2.imshow('image', img)

#setting mouse handler for the image
cv2.setMouseCallback('image', click_event)

#display the image
while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k ==27 or k ==113: #press esc or q to exit 
        break
cv2.destroyAllWindows()
