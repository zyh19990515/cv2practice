import cv2
import numpy as np

if __name__ == '__main__':
    img = cv2.imread("D:\\code\\python\\cv2practice\\imgfile\\2.jpg")
    img = cv2.resize(img, (400, 400))
    img_hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    for i in range(0, 400):
        for j in range(0, 400):
            img_hls[i][j][1] = 150
            img_hls[i][j][2] = 255
    img_rgb = cv2.cvtColor(img_hls, cv2.COLOR_HLS2RGB)
    for i in range(0, 400):
        for j in range(0, 400):
            if(img_rgb[i][j][2]!=255):
                img[i][j][0] = 0
                img[i][j][1] = 0
                img[i][j][2] = 0
            if(img_rgb[i][j][2]==255):
                img[i][j][0] = 255
                img[i][j][1] = 255
                img[i][j][2] = 255
    k = np.array([[1/16, 2/16, 1/16], [2/16, 4/16, 2/16], [1/16, 2/16, 1/16]], dtype=np.float32)
    img_np = np.array(img)
    img_r = cv2.filter2D(img_np, -1, kernel=k)
    cv2.imshow("平滑", img_r)
    cv2.imshow("ori", img)
    cv2.imshow("1", img_rgb)
    cv2.waitKey(0)