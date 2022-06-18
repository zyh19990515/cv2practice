import cv2
import numpy as np
import time

def pre(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_canny = cv2.Canny(img_gray, -1, 80, 300)
    return img_canny

def houghtTransform(img):

    lines = cv2.HoughLines(img, 1, np.pi / 180, 90)
    print(lines)
    lines_1 = lines[:, 0, :]
    print("line_1:\n", lines_1)
    img_zero = np.zeros((400, 400, 3), dtype=np.int8)
    for rho, theta in lines_1:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(img_zero, (x1, y1), (x2, y2), (255, 0, 0), 1)
    return img_zero

def equal(img_gray):
    equ = cv2.equalizeHist(img_gray)

    res = np.hstack((img_gray, equ))
    return res

if __name__ == '__main__':

    img = cv2.imread("D:\\code\\python\\cv2practice\\3.jpg")
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_pre = pre(img)
    cv2.imshow("canny", img_pre)
    img_hough = houghtTransform(img_pre)
    cv2.imshow("hough", img_hough)
    img_equal = equal(img_gray)
    cv2.imshow("equal", img_equal)

    cv2.waitKey(0)