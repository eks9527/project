# 獲取人臉資料

import cv2

# 將圖像存在 xxx.pgm檔
def saveImage(image, index):
    filename = 'images/h0/{:02d}.pgm'.format(index)
    cv2.imwrite(filename, image)
    print(filename)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cv2.namedWindow('video', cv2.WINDOW_NORMAL)

n = 1
idx = 0
max_idx = 100

while n > 0:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (600, 480))
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 3)

    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if n % 5 == 0:
            face_img = cv2.resize(gray[y: y + h, x: x + w], (400, 400))
            saveImage(face_img, idx)
            idx += 1
            if idx >= max_idx:
                print('get training data done')
                n = -1
                break
        n += 1

    cv2.imshow('video', frame)
    cv2.waitKey(1)
