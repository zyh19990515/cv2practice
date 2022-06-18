import cv2
import numpy as np
import os

path = "D:\\picture\\kd990515 15889627618\\2022.4.20"
countnum = 1
for root, dir, files in os.walk(path):
    for name in files:
        file_path = os.path.join(root, name)
        print(os.path.join(root, name))
        img = cv2.imread(file_path)
        save_path = "D:\\picture\\kd990515 15889627618\\2022.4.20\\" + str(countnum)+".jpg"
        cv2.imwrite(save_path, img)
        countnum+=1
