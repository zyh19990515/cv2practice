import cv2
import numpy as np
from selenium import webdriver

def camera_init():
    bor = webdriver.Chrome()
    bor.get("http://192.168.137.156")

    select = bor.find_element_by_id('framesize')
    all_options = select.find_elements_by_tag_name('option')
    for option in all_options:
        if (option.get_attribute("value") == '7'):
            print("finish")
            option.click()
            break
    bor.quit()


def pre_treat(img):
    img = cv2.resize(img, (400, 400))
    img_hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    for i in range(0, 400):
        for j in range(0, 400):
            img_hls[i][j][1] = 150
            img_hls[i][j][2] = 255

    img_rgb = cv2.cvtColor(img_hls, cv2.COLOR_HLS2RGB)
    for i in range(0, 400):
        for j in range(0, 400):
            if (img_rgb[i][j][2] != 255):
                img[i][j][0] = 0
                img[i][j][1] = 0
                img[i][j][2] = 0
            if (img_rgb[i][j][2] == 255):
                img[i][j][0] = 255
                img[i][j][1] = 255
                img[i][j][2] = 255
    k = np.array([[1 / 16, 2 / 16, 1 / 16], [2 / 16, 4 / 16, 2 / 16], [1 / 16, 2 / 16, 1 / 16]], dtype=np.float32)
    img_np = np.array(img)
    img_r = cv2.filter2D(img_np, -1, kernel=k)
    return img_r

def cornerdetec(img):
    img = np.array(img, dtype=np.uint8)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    corners = cv2.goodFeaturesToTrack(img_gray, 4, qualityLevel=0.1, minDistance=50)
    corners = np.int0(corners)
    corner_arr = []
    for i in corners:
        x, y = i.ravel()
        corner_arr.append((x, y))
        #cv2.circle(img, (x, y), 5, color=255, thickness=1)
    return corner_arr

def houghtTransform(img):
    edge = cv2.Canny(img, 50, 200)
    lines = cv2.HoughLines(edge, 1, np.pi / 180, 100)
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
    camera_init()

    video = cv2.VideoCapture("http://192.168.137.214:81/stream")

    print('ready')
    while True:
        sucess, img = video.read()

        if not sucess:
            print(sucess)
            continue

        cv2.imshow("img_done", img)

        k = cv2.waitKey(1)


        if k == 27:

            cv2.destroyAllWindows()
            break


