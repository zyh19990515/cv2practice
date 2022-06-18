import cv2
import numpy as np
import time
from selenium import webdriver
import xlwt
import serial
import re
def serialData():
    s = serial.Serial('com3', 115200)

    st = ''
    while True:

        while True:
            char = str(s.read(), 'utf-8')
            # print(char)
            try:
                # print(char)
                st = st + char

            except:
                continue
            if (char == '\n'):
                break
        try:
            ipList = re.findall(r'[0-9]+(?:\.[0-9]+){3}', st)
            print(ipList[0])

            break
        except:
            print(st)
            continue
    return str(ipList[0])

def camera_init(ip):
    bor = webdriver.Chrome()
    ip = "http://" + ip
    #bor.get("http://192.168.137.156")
    bor.get(ip)


    select = bor.find_element_by_id('framesize')
    all_options = select.find_elements_by_tag_name('option')
    for option in all_options:
        if (option.get_attribute("value") == '10'):
            print("finish")
            option.click()
            break
    bor.quit()

def pre_treat(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_canny = cv2.Canny(img_gray, -1, 80, 300)
    return img_canny

def houghtTransform(img):

    lines = cv2.HoughLines(img, 1, np.pi / 180, 90)
    #print(lines)
    lines_1 = lines[:, 0, :]
    #print("line_1:\n", lines_1)
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
    cor_position.append(corner_arr[0][0] + corner_arr[0][1])
    cor_position.append(corner_arr[1][0] + corner_arr[1][1])
    cor_position.append(corner_arr[2][0] + corner_arr[2][1])
    cor_position.append(corner_arr[3][0] + corner_arr[3][1])
    cor = {cor_position[0]: 0, cor_position[1]: 1, cor_position[2]: 2, cor_position[3]: 3}
    cor_position.sort()
    temp = [cor[cor_position[0]], cor[cor_position[1]], cor[cor_position[2]], cor[cor_position[3]]]
    corner_arr[0], corner_arr[1], corner_arr[2], corner_arr[3] = \
        corner_arr[temp[0]], corner_arr[temp[2]], corner_arr[temp[3]], corner_arr[temp[1]]
    print(corner_arr)
    return corner_arr

#def ballDetect():

def dataSave(corner_pt, cnt):

    print(corner_pt)
    sheet.write(cnt, 0, str(corner_pt[0][0][0]))
    sheet.write(cnt, 1, str(corner_pt[0][0][1]))
    sheet.write(cnt, 2, str(corner_pt[0][1][0]))
    sheet.write(cnt, 3, str(corner_pt[0][1][1]))
    sheet.write(cnt, 4, str(corner_pt[0][2][0]))
    sheet.write(cnt, 5, str(corner_pt[0][2][1]))
    sheet.write(cnt, 6, str(corner_pt[0][3][0]))
    sheet.write(cnt, 7, str(corner_pt[0][3][1]))

if __name__ == '__main__':
    ip = serialData()
    camera_init(ip)
    cnt = 1
    videoIp = "http://" + ip + ":81/stream"
    #video = cv2.VideoCapture("http://192.168.137.156:81/stream")
    video = cv2.VideoCapture(videoIp)
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('points')
    sheet.write(0, 0, 'p1_x')
    sheet.write(0, 1, 'p1_y')
    sheet.write(0, 2, 'p2_x')
    sheet.write(0, 3, 'p2_y')
    sheet.write(0, 4, 'p3_x')
    sheet.write(0, 5, 'p3_y')
    sheet.write(0, 6, 'p4_x')
    sheet.write(0, 7, 'p4_y')

    print('ready')
    while True:
        sucess, img = video.read()

        if not sucess:
            print(sucess)
            continue
        img = cv2.resize(img, (400, 400))
        img_save = img
        img_pre = pre_treat(img)
        cv2.imshow("pre", img_pre)


        try:
            img_hough = houghtTransform(img_pre)
            cv2.imshow("img_hough", img_hough)
            corner_pt = cornerdetec(img_hough)
            # corner_pt[2], corner_pt[3] = corner_pt[3], corner_pt[2]
            #print(corner_pt)
            print(corner_pt)
            for i in corner_pt:
                cv2.circle(img, i, radius=5, color=(255, 0, 0), thickness=1)
            corner_pt = np.array([corner_pt])

            cv2.polylines(img, corner_pt, isClosed=True, color=(0, 255, 0), thickness=1)
            #print(corner_pt)
            # try:
            #     dataSave(corner_pt, cnt)
            #     cnt += 1
            # except:
            #     print("no points")
        except:
            print('error')
            #continue
        cv2.imshow("img_DONE", img_save)

        k = cv2.waitKey(1)

        if k == 27:
            cv2.destroyAllWindows()
            book.save("pt_data.csv")
            break