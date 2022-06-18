import cv2
import numpy as np
import matplotlib.pyplot as plt



if __name__ == '__main__':
    img = cv2.imread("./3.jpg")
    cv2.imshow("1", img)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv_low = np.array([0, 0, 46])
    hsv_high = np.array([180, 23, 220])
    mask = cv2.inRange(img_hsv, lowerb=hsv_low, upperb=hsv_high)
    img_done = cv2.add(img_hsv, img_hsv, mask=mask)
    img_done = cv2.cvtColor(img_done, cv2.COLOR_HSV2RGB)
    cv2.imshow("2", img_done)
    cv2.imwrite("6.jpg", img_done)

    cv2.waitKey(0)