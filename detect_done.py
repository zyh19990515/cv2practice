import cv2
import numpy as np
import time
from selenium import webdriver
import xlwt
from detect import Detect
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

if __name__ == '__main__':
    ip = serialData()
    camera_init(ip)
    videoIp = "http://" + ip + ":81/stream"
    video = cv2.VideoCapture(videoIp)

    while True:
        sucess, img = video.read()

        if not sucess:
            print(sucess)
            continue
        BD = Detect(img)
        img_b, corner_pts = BD.board_main()
        img_ball, ballpt = BD.ball_main()


        cv2.imshow("img_DONE", img)

        k = cv2.waitKey(1)

        if k == 27:
            cv2.destroyAllWindows()

            break