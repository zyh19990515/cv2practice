import cv2
import numpy as np
import time

# def pre_treat(img):
#     img = cv2.resize(img, (400, 400))
#     img_hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
#     for i in range(0, 400):
#         for j in range(0, 400):
#             img_hls[i][j][1] = 150
#             img_hls[i][j][2] = 255
#
#     img_rgb = cv2.cvtColor(img_hls, cv2.COLOR_HLS2RGB)
#     for i in range(0, 400):
#         for j in range(0, 400):
#             if (img_rgb[i][j][2] != 255):
#                 img[i][j][0] = 0
#                 img[i][j][1] = 0
#                 img[i][j][2] = 0
#             if (img_rgb[i][j][2] == 255):
#                 img[i][j][0] = 255
#                 img[i][j][1] = 255
#                 img[i][j][2] = 255
#     k = np.array([[1 / 16, 2 / 16, 1 / 16], [2 / 16, 4 / 16, 2 / 16], [1 / 16, 2 / 16, 1 / 16]], dtype=np.float32)
#     img_np = np.array(img)
#     img_r = cv2.filter2D(img_np, -1, kernel=k)
#     return img_r

def imgMask(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv_low = np.array([0, 0, 46])
    hsv_high = np.array([180, 23, 220])
    mask = cv2.inRange(img_hsv, lowerb=hsv_low, upperb=hsv_high)
    img_done = cv2.add(img_hsv, img_hsv, mask=mask)
    img_done = cv2.cvtColor(img_done, cv2.COLOR_HSV2RGB)
    return img_done

def pre_treat(img):
    img = imgMask(img)
    cv2.imshow("1111", img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_canny = cv2.Canny(img_gray, -1, 80, 300)
    return img_canny

def cornerdetec(img):
    img = np.array(img, dtype=np.uint8)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    corners = cv2.goodFeaturesToTrack(img_gray, 4, qualityLevel=0.1, minDistance=200)
    corners = np.int0(corners)
    corner_arr = []
    for i in corners:
        x, y = i.ravel()
        corner_arr.append((x, y))
        #cv2.circle(img, (x, y), 5, color=255, thickness=1)
    cor_position = []
    cor_position.append(corner_arr[0][0]+corner_arr[0][1])
    cor_position.append(corner_arr[1][0] + corner_arr[1][1])
    cor_position.append(corner_arr[2][0] + corner_arr[2][1])
    cor_position.append(corner_arr[3][0] + corner_arr[3][1])
    cor = {cor_position[0]:0, cor_position[1]:1, cor_position[2]:2, cor_position[3]:3}
    cor_position.sort()
    temp = [cor[cor_position[0]], cor[cor_position[1]], cor[cor_position[2]], cor[cor_position[3]]]
    corner_arr[0], corner_arr[1], corner_arr[2], corner_arr[3] = \
        corner_arr[temp[0]], corner_arr[temp[2]], corner_arr[temp[3]], corner_arr[temp[1]]
    return corner_arr

def houghtTransform(img):

    lines = cv2.HoughLines(img, 1, np.pi / 180, 110)
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

if __name__ == '__main__':
    img = cv2.imread("D:\\code\\python\\cv2practice\\1.jpg")

    start = time.time()
    img = cv2.resize(img, (400, 400))
    cv2.imshow("img", img)
    start_pre = time.time()
    img_pre = pre_treat(img)

    cv2.imshow("pre", img_pre)
    end_pre = time.time()
    start_hough = time.time()
    img_hough = houghtTransform(img_pre)
    cv2.imshow("hough", img_hough)
    end_hough = time.time()

    start_cor = time.time()
    corner_pt = cornerdetec(img_hough)
    end_cor = time.time()
    #corner_pt[2], corner_pt[3] = corner_pt[3], corner_pt[2]
    print(corner_pt)
    for i in corner_pt:
        cv2.circle(img, i, radius=5, color=(255, 0, 0), thickness=1)
    corner_pt = np.array([corner_pt])
    cv2.polylines(img, corner_pt, isClosed=True, color=(0, 255, 0), thickness=1)
    end = time.time()
    cv2.imshow("img_done", img)
    print("总运行时间：", end-start)
    #print("pre时间：", end_pre-start_pre)
    #print("hough时间：", end_hough - start_hough)
    #print("cor时间：", end_cor - start_cor)
    #cv2.imshow("2", img_zero)
    cv2.waitKey(0)
