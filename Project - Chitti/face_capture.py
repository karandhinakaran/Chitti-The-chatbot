import cv2
import numpy as np
from keras.models import model_from_json

emotion_dict = {0:'Angry', 1:'Disgusted', 2:'Fearful', 3:'Happy', 4:'Neutral', 5:'Sad', 6:'Surprised'}
json_file = open('emotion_detection\\emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json) # type: ignore
emotion_model.load_weights('emotion_detection\\emotion_model.h5') # type: ignore

#use the webcam feed using the opencv tool 
def bot():
    ans = []
    cap = cv2.VideoCapture(0)
    num = 0
    while num < 10:
        #find hard cascade to draw bounding box around the face 
        ret, frame = cap.read()
        if not ret:
            break
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #detect faces on camera
        num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor = 1.3, minNeighbors = 5)
        #take each face on the camera and preprocess it 
        if len(num_faces) == 0:
            ans.append(4)
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y:y+h, x:x+w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            #predict the emotion 
            emotion_prediction = emotion_model.predict(cropped_img, verbose = 0) # type: ignore
            maxindex = int(np.argmax(emotion_prediction))
            ans.append(maxindex)
            # cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_4)

        # cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
        num += 1
    try:
        return max(set(ans), key = ans.count)
    except:
        return 4
    cap.release()
    cv2.destroyAllWindows()
 

# print(bot())