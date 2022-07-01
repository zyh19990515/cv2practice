import cv2
import numpy as np
import time
from selenium import webdriver
import xlwt

class Detect():
    def __init__(self, img):
        self.img = img
        self.size = img.shape

    def boardMask(self, img):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        hsv_low = np.array([0, 0, 46])
        hsv_high = np.array([180, 35, 255])
        mask = cv2.inRange(img_hsv, lowerb=hsv_low, upperb=hsv_high)
        # img_done = cv2.add(img_hsv, img_hsv, mask=mask)
        # img_done = cv2.cvtColor(img_done, cv2.COLOR_HSV2RGB)
        #cv2.imshow("maskb", mask)
        return mask

    def ballMask(self, img):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        hsv_low = np.array([0, 0, 0])
        hsv_high = np.array([180, 255, 100])
        mask = cv2.inRange(img_hsv, lowerb=hsv_low, upperb=hsv_high)
        #cv2.imshow("mask", mask)
        img_done = cv2.add(img_hsv, img_hsv, mask=mask)
        img_done = cv2.cvtColor(img_done, cv2.COLOR_HSV2RGB)
        return mask
    def boardPreTreat(self, img):
        #cv2.imshow("324132", img)
        img = self.boardMask(img)
        #img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_canny = cv2.Canny(img, -1, 80, 300)
        #cv2.imshow("canny", img_canny)
        return img_canny

    def ballPreTreat(self, img):
        img = self.ballMask(img)
        # img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_canny = cv2.Canny(img, -1, 80, 300)
        # cv2.imshow("11", img_canny)
        return img_canny
    def houghtTransform(self, img):
        #cv2.imshow("23", img)
        lines = cv2.HoughLines(img, 1, np.pi / 180, 95)
        # print(lines)
        lines_1 = lines[:, 0, :]
        # print("line_1:\n", lines_1)
        img_zero = np.zeros(self.size, dtype=np.int8)
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
            #cv2.imshow("hough", img_zero)
        return img_zero

    def cornerdetec(self, img):
        img = np.array(img, dtype=np.uint8)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        corners = cv2.goodFeaturesToTrack(img_gray, 4, qualityLevel=0.1, minDistance=200)
        corners = np.int0(corners)
        corner_arr = []
        for i in corners:
            x, y = i.ravel()
            corner_arr.append((x, y))
            # cv2.circle(img, (x, y), 5, color=255, thickness=1)
        cor_position = []
        cor_position.append(corner_arr[0][0] + corner_arr[0][1])
        cor_position.append(corner_arr[1][0] + corner_arr[1][1])
        cor_position.append(corner_arr[2][0] + corner_arr[2][1])
        cor_position.append(corner_arr[3][0] + corner_arr[3][1])
        cor = {cor_position[0]: 0, cor_position[1]: 1, cor_position[2]: 2, cor_position[3]: 3}
        cor_position.sort()
        temp = [cor[cor_position[0]], cor[cor_position[1]], cor[cor_position[2]], cor[cor_position[3]]]
        corner_arr[0], corner_arr[1], corner_arr[2], corner_arr[3] = \
            corner_arr[temp[0]], corner_arr[temp[2]], corner_arr[temp[3]], corner_arr[temp[1]]
        #print(corner_arr)
        return corner_arr
    def getImg(self, img, corner_pt, ballpt):
        for i in corner_pt:
            cv2.circle(self.img, i, radius=5, color=(255, 0, 0), thickness=1)
        corner_pt_line = np.array([corner_pt])
        cv2.polylines(self.img, corner_pt_line, isClosed=True, color=(0, 255, 0), thickness=1)
        cv2.circle(img_pre, ballPt, radius=5, color=(255, 0, 0), thickness=1)

    def board_main(self):
        print(self.size)
        img_pre = self.boardPreTreat(self.img)
        img_hough = self.houghtTransform(img_pre)
        corner_pt = self.cornerdetec(img_hough)
        # for i in corner_pt:
        #     cv2.circle(self.img, i, radius=5, color=(255, 0, 0), thickness=1)
        # corner_pt_line = np.array([corner_pt])
        # cv2.polylines(self.img, corner_pt_line, isClosed=True, color=(0, 255, 0), thickness=1)
        return np.array(corner_pt)

    def ball_main(self):
        img_pre = self.ballPreTreat(self.img)
        circle = cv2.HoughCircles(img_pre, cv2.HOUGH_GRADIENT, 3, 10, param1=100, param2=36, minRadius=0, maxRadius=10)
        ballPt = [int(circle[0, 0, 0]), int(circle[0, 0, 1])]

        return np.array(ballPt)

if __name__ == '__main__':
    img = cv2.imread(".\\no.2.jpg")
    BD = Detect(img)
    corner_pts = BD.board_main()
    ballpt = BD.ball_main()

    print("cor", corner_pts)
    #print("ball", ballpt)
    #print(corner_pts[:, :, 0])
    cv2.imshow("1", img)
    #cv2.imshow("2", img_ball)
    cv2.waitKey(0)
