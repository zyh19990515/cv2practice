import cv2
import numpy as np
import random
import math
def genImg(pts):

    img = np.zeros((480, 640, 3), np.uint8)





    cv2.polylines(img, pts, isClosed=True, color=(255, 255, 255), thickness=1)

    cv2.fillPoly(img, pts, color=(255, 255, 255))
    return img

if __name__ == '__main__':
    i1 = 220
    j1 = 140

    i2 = 420
    j2 = 140

    i3 = 220
    j3 = 340

    i4 = 420
    j4 = 340

    theta = np.pi/3.0

    m = np.array([[1.07325475e+00, -2.62449354e-01, 3.35917338e+01], [1.51234885e-01, 8.75133697e-01, -1.52081434e+01], [3.85193559e-04, -5.75597586e-04, 1.00000000e+00]], dtype=np.float)
    print(m)
    p1 = np.array([[i1], [j1], [1]], dtype=np.float)
    p2 = np.array([[i2], [j2], [1]], dtype=np.float)
    p3 = np.array([[i3], [j3], [1]], dtype=np.float)
    p4 = np.array([[i4], [j4], [1]], dtype=np.float)

    p1 = m.dot(p1)
    p2 = m.dot(p2)
    p3 = m.dot(p3)
    p4 = m.dot(p4)
    print("点乘后：")
    for j in (p1, p2, p3, p4):
        print(j)
    w = p1[2]
    print(w)
    p1 = [p1[0]/w, p1[1]/w]
    p2 = [p2[0]/w, p2[1]/w]
    p3 = [p3[0]/w, p3[1]/w]
    p4 = [p4[0]/w, p4[1]/w]
    for i in (p1, p2, p3, p4):
        print(i)


    # print(p1)

    pts_1 = np.array([[[i1, j1], [i2, j2], [i4, j4], [i3, j3]]], dtype=np.int32)
    pts_2 = np.array([[p1, p2, p4, p3]], dtype=np.int32)
    print("\n\n\n\n\n")
    print(pts_2)
    print("\n\n\n\n\n")
    img = genImg(pts_1)
    img_r = genImg(pts_2)
    # pts = np.array([[[i1, j1], [i2, j2], [i4, j4], [i3, j3]]], dtype=np.int32)
    # img = genImg(pts)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #
    #
    cv2.imshow("img", img)
    cv2.imshow("img_result", img_r)
    # print("finish")
    cv2.waitKey(0)
