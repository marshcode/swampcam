import cv2

#print("Before URL")
cap = cv2.VideoCapture('rtsp://192.168.86.150:8080/h264_ulaw.sdp')
#print("After URL")

while True:

    #print('About to start the Read command')
    ret, frame = cap.read()
    #print('About to show frame of Video.')
    if ret:
        cv2.imshow("Capturing",frame)
    #print('Running..')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()