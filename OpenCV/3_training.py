# 訓練人臉識別資料

import cv2
import numpy as np

images = []
labels = []

for index in range(100):
    filename = 'images/h0/{:02d}.pgm'.format(index)
    print('read ' + filename)
    # 讀取 images/h0/xx.pgm
    img = cv2.imread(filename, cv2.COLOR_BGR2GRAY)
    # 加入至 image list
    images.append(img)
    # 給一個編號
    labels.append(0)

# 訓練開始
print('training...')
# 建立 人臉識別器物件
model = cv2.face.LBPHFaceRecognizer_create()
# 訓練識別器
model.train(np.asarray(images), np.asarray(labels))
# 儲存識別器
model.save('faces.data')
# 訓練結束
print('training done')
