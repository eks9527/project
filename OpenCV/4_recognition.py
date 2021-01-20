# 動態人臉識別

import cv2
import numpy as np
import time

names = ['liu']

# 建立 人臉辨識器物件
model = cv2.face.LBPHFaceRecognizer_create()
# 讀取 人臉辨識模型
model.read('faces.data')
# 讀取成功
print('load training data done')


# 建立 人臉分類器
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# 建立 眼睛分類器
# eye_cascade = cv2.Ca1scadeClassifier(cv2.data.haarcascades+'haarcascade_eye.xml')
# 建立 微笑分類器
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_smile.xml')

# 打開攝影機
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_BRIGHTNESS, 80) # 亮度調整，預設50

# 打開視窗(可以自動調整)
cv2.namedWindow('video', cv2.WINDOW_NORMAL)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    # 讀取影像
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    # frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 3)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # 在人臉區域進行 眼睛分類器 節省計算資源
        face_img = cv2.resize(gray[y: y + h, x: x + w], (400, 400))
        try:
            params = model.predict(face_img)
            print('label: {}, confidence: {}'.format(params[0], params[1]))
            # 如果 信賴度 < 50
            if params[1] < 50:
                # 把他的id印在辨識框上
                cv2.putText(frame, names[params[0]], (x, y - 10),
                            font, 1, (255,255,0), 3, cv2.LINE_AA)

            smiles = smile_cascade.detectMultiScale(face_img,scaleFactor= 1.16
                                                    ,minNeighbors=65,minSize=(25, 25)
                                                    ,flags=cv2.CASCADE_SCALE_IMAGE)
            for (sx,sy,sw,sh) in smiles:
                cv2.rectangle(face_img,(sx,sy),(sx+sw,sy+sh),(0,0,255),1)
                cv2.putText(frame, ':)', (x+100, y-10)
                            , font, 1, (0, 0, 255)
                            , 3, cv2.LINE_AA)

            datet = str(time.asctime(time.localtime(time.time())))
            frame = cv2.putText(frame, datet, (10, 50), font,
                                0.5, (0, 255, 255), 2, cv2.LINE_AA)

            # fps = 'FPS: ' + str(cap.get(cv2.CAP_PROP_FPS))
            # frame = cv2.putText(frame, fps, (10, 100), font,ˊ
            #                     0.5, (0, 255, 255), 2, cv2.LINE_AA)
        except:
            # 如果不是持續偵測
            continue

    cv2.imshow('video', frame)
    # ESC 結束
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break
