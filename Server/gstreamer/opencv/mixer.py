
import cv2
cap = cv2.VideoCapture('dvbbasebin modulation="QAM 64" trans-mode=8k bandwidth=8 frequency=538000000 code-rate-lp=AUTO code-rate-hp=2/3 guard=4  hierarchy=0 program-numbers=3 ! decodebin  ! videoconvert ! appsink') 
while True:
    ret,frame = cap.read()
    cv2.imshow('',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
