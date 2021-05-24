import cv2
# import sys

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# profile_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
# body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

video_capture = cv2.VideoCapture(0)

video_capture.set(3, 1280)
video_capture.set(4, 720)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
#     profile_faces = profile_face_cascade.detectMultiScale(
#         gray,
#         scaleFactor=1.1,
#         minNeighbors=5,
#         minSize=(30, 30)
#     )

#    bodies = body_cascade.detectMultiScale(
#        gray,
#        scaleFactor=1.1,
#        minNeighbors=5,
#        minSize=(30, 30)
#    )

    # Draw a rectangle around the faces
    # for (x, y, w, h) in faces:
    #    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
#     for (x, y, w, h) in profile_faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

#    for (x, y, w, h) in bodies:
#        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()