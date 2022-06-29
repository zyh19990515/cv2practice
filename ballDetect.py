import cv2
import numpy as np


def imgMask(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv_low = np.array([0, 0, 0])
    hsv_high = np.array([180, 255, 100])
    mask = cv2.inRange(img_hsv, lowerb=hsv_low, upperb=hsv_high)
    cv2.imshow("mask", mask)
    img_done = cv2.add(img_hsv, img_hsv, mask=mask)
    img_done = cv2.cvtColor(img_done, cv2.COLOR_HSV2RGB)
    return mask

def pre_treat(img):
    img = imgMask(img)
    #img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_canny = cv2.Canny(img, -1, 80, 300)
    #cv2.imshow("11", img_canny)
    return img_canny

if __name__ == '__main__':
    img = cv2.imread(".\\ball2.jpg")
    img_pre = img
    cv2.imshow("111", img_pre)
    img = pre_treat(img)
    # cv2.imshow("img", img)
    #
    cv2.imshow("img_1", img)
    #img = pre_treat(img)
    circle = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 3, 10, param1=100, param2=36, minRadius=0, maxRadius=10)
    print(circle)

    ballPt = [int(circle[0, 0, 0]), int(circle[0, 0, 1])]
    #print(ballPt)
    cv2.circle(img_pre, ballPt, radius=10, color=(255, 0, 0), thickness=1)

    cv2.imshow("img", img_pre)

    cv2.waitKey(0)