# 動態人臉偵測

import cv2


# 人臉分類器
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# 選擇默認攝影機
cap = cv2.VideoCapture(0)
ESC = 27

while True:
    # 讀取影像
    ret, frame = cap.read()
    # 圖像縮放
    frame = cv2.resize(frame, (320, 240))
    # 圖像 水平翻轉
    frame = cv2.flip(frame, 1)
    # 圖像轉成灰階
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 偵測人臉的方法
    # scalFactor=1.1 (圖像縮放比例)
    # minNeighbors=5 (針對特徵點附近進行檢測)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # 把人臉用綠框框起來
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # 視窗設定 可以自由調整大小
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    # 顯示影像
    cv2.imshow('video', frame)
    # 按ESC 關閉攝影機
    if cv2.waitKey(1) == ESC:
        break

# 釋放攝影機
cap.release()
# 關閉視窗
cv2.destroyAllWindows()
