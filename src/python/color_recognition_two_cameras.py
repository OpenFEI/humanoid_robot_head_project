import cv2
import cv2.cv as cv
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('image')
# create trackbars for color change
cv2.createTrackbar('H_Low','image',0,255,nothing)
cv2.createTrackbar('H_High','image',0,255,nothing)
cv2.createTrackbar('S_Low','image',0,255,nothing)
cv2.createTrackbar('S_High','image',255,255,nothing)
cv2.createTrackbar('V_Low','image',0,255,nothing)
cv2.createTrackbar('V_High','image',255,255,nothing)


cap_2 = cv2.VideoCapture(1)
cap_1 = cv2.VideoCapture(0)
#set resolution:
cap_1.set(3,640)
cap_1.set(4,480)

cap_2.set(3,640)
cap_2.set(4,480)

# initialisation
Av = []
compt = 0
X_coor = 0

while(1):

    # Take each frame
    ret_1, frame_1 = cap_1.read()
    ret_2, frame_2 = cap_2.read()
    
    # Convert BGR to HSV
    hsv_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2HSV)
    hsv_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2HSV)

    # get current positions of four trackbars
    h_high  = cv2.getTrackbarPos('H_High','image')
    h_low = cv2.getTrackbarPos('H_Low','image')
    s_high = cv2.getTrackbarPos('S_High','image')
    s_low = cv2.getTrackbarPos('S_Low','image')
    v_high = cv2.getTrackbarPos('V_High','image')
    v_low = cv2.getTrackbarPos('V_Low','image')
    
    #orange:
    lower_blue = np.array([h_low,s_low,v_low]) 
    upper_blue = np.array([h_high,s_high,v_high])
    
    # Threshold the HSV image to get only orange colors
    mask_1 = cv2.inRange(hsv_1, lower_blue, upper_blue)
    mask_2 = cv2.inRange(hsv_2, lower_blue, upper_blue)

	#erosion
    kernel = np.ones((5,5),np.uint8)
    erosion_1 = cv2.erode(mask_1,kernel,iterations=3)
    erosion_2 = cv2.erode(mask_2,kernel,iterations=3)

    #dilation
    dilation_1 = cv2.dilate(erosion_1,kernel,iterations=3)
    dilation_2 = cv2.dilate(erosion_2,kernel,iterations=3)

    img_1 = cv2.medianBlur(dilation_1,21)
    img_2 = cv2.medianBlur(dilation_2,21)

    # Bitwise-AND mask and original image
    res_1 = cv2.bitwise_and(frame_1,frame_1, mask=dilation_1)
    res_2 = cv2.bitwise_and(frame_2,frame_2, mask=dilation_2)

    momento_1 = cv2.moments(img_1)
    momento_2 = cv2.moments(img_2)
    try:
        cx_1 = float(momento_1['m10']/momento_1['m00'])
        cy_1 = int(momento_1['m01']/momento_1['m00'])
        area_1 = momento_1['m00']
        cx_2 = float(momento_2['m10']/momento_2['m00'])
        cy_2 = int(momento_2['m01']/momento_2['m00'])
        area_2 = momento_2['m00']

        # Cacul distance between center
        X = float(cx_1-cx_2)

        if X < 0 :
            X = -X

        Y = cy_1-cy_2

        # iteration to make a average of X
        
    
        if compt < 200 :
            Av.append(X)
            compt += 1

        if compt == 200 :
            X_coor = sum(Av)/len(Av)
            print X_coor
            compt = 0
        
        # Calcul Distance to the ball
        Disparity = 1/X
        D = 218400*(Disparity**3)-53520*(Disparity**2)+5767*Disparity+0.5364

        print cx_1, cy_1, area_1, cx_2, cy_2, area_2, compt, D
    except ZeroDivisionError:
        pass

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img_1,'Press: ',(30,30), font, 0.5, 160)
    cv2.putText(img_1,'o for orange',(30,50), font, 0.5, 160)
    cv2.putText(img_1,'y for yellow',(30,70), font, 0.5, 160)
    cv2.putText(img_1,'g for green',(30,90), font, 0.5, 160)
    cv2.putText(img_1,'v for violet',(30,110), font, 0.5, 160)
    cv2.putText(img_1,'r for red',(30,130), font, 0.5, 160)
    cv2.putText(img_1,'b for blue',(30,150), font, 0.5, 160)
    cv2.putText(img_1,'Esc for exit',(30,170), font, 0.5, 160)


    

    cv2.imshow('image',img_1)
    cv2.imshow('frame',frame_1)
    cv2.imshow('frame_2',frame_2)
    cv2.imshow('cor',res_1)
    cv2.imshow('cor_2',res_2)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    if k ==  98: #b - blue
        cv2.setTrackbarPos('H_High', 'image', 130)
        cv2.setTrackbarPos('H_Low', 'image', 75)
    if k ==  111: #o - orange
        cv2.setTrackbarPos('H_High', 'image', 22)
        cv2.setTrackbarPos('H_Low', 'image', 0)
    if k ==  121: #y - yellow
        cv2.setTrackbarPos('H_High', 'image', 38)
        cv2.setTrackbarPos('H_Low', 'image', 22)
    if k ==  103: #g - green
        cv2.setTrackbarPos('H_High', 'image', 92)
        cv2.setTrackbarPos('H_Low', 'image', 75)     
    if k ==  118: #v - violet
        cv2.setTrackbarPos('H_High', 'image', 160)
        cv2.setTrackbarPos('H_Low', 'image', 130)  
    if k ==  114: #r - red
        cv2.setTrackbarPos('H_High', 'image', 179)
        cv2.setTrackbarPos('H_Low', 'image', 160)

cv2.destroyAllWindows()
