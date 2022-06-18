import cv2
import numpy as np
import random

def genImg():

    img = np.zeros((480, 640, 3), np.uint8)

    i1 = random.randint(200, 240)
    j1 = random.randint(120, 160)
    i2 = random.randint(200, 240)
    j2 = random.randint(320, 360)
    i3 = random.randint(400, 440)
    j3 = random.randint(120, 160)
    i4 = random.randint(400, 440)
    j4 = random.randint(320, 360)

    pts = np.array([[[i1, j1], [i2, j2], [i4, j4], [i3, j3]]], dtype=np.int32)
    print(pts)
    # cv2.line(img, (i1, j1), (i2, j2), color=255, thickness=1)
    # cv2.line(img, (i1, j1), (i3, j3), color=255, thickness=1)
    # cv2.line(img, (i3, j3), (i4, j4), color=255, thickness=1)
    # cv2.line(img, (i2, j2), (i4, j4), color=255, thickness=1)
    cv2.polylines(img, pts, isClosed=True, color=(255, 255, 255), thickness=1)

    cv2.fillPoly(img, pts, color=(255, 255, 255))
    return img
#corners = cv2.goodFeaturesToTrack(img, 4, qualityLevel=0.01, minDistance=10)

#corners = np.int0(corners)
#print(corners)
# for i in corners:
#     x, y = i.ravel()
#     cv2.circle(img, (x, y), 10, color=255, thickness=1)
if __name__ == '__main__':
    for countnum in range(0, 1000):
        img = genImg()
        path = 'D:\\code\\python\\cv2practice\\imgDataset\\'+str(countnum)+'.jpg'
        #cv2.imwrite(path, img)

