import cv2
import numpy as np
import time

class perspectiveMatrix():
    def __init__(self):
        self.A = np.zeros((8, 8), dtype=np.float)   # 系数矩阵
        self.XY = np.zeros((8, 1), dtype=np.float)  # 系数矩阵后两列
    def matrixInit(self, pt1, pt2):     # 系数矩阵初始化
        self.A[0][2] = 1
        self.A[1][2] = 1
        self.A[2][2] = 1
        self.A[3][2] = 1
        self.A[4][5] = 1
        self.A[5][5] = 1
        self.A[6][5] = 1
        self.A[7][5] = 1
        self.A[0:4, 0:2] = pt1
        self.A[4:8, 3:5] = pt1
        X = pt2[:, 0]
        temp1 = -X*pt1.T
        self.A[0:4, 6:8] = temp1.T
        Y = pt2[:, 1]
        temp2 = -Y*pt1.T
        self.A[4:8, 6:8] = temp2.T
        self.XY[0:4, 0] = pt2[:, 0]
        self.XY[4:8, 0] = pt2[:, 1]

    def getperspectiveMatrix(self, pt1, pt2):   #得到透视变换矩阵
        self.matrixInit(pt1, pt2)

        a = np.linalg.solve(self.A, self.XY)
        answer = np.zeros((3, 3), dtype=np.float)
        answer[0][:] = a[0:3].T
        answer[1][:] = a[3:6].T
        answer[2][0:2] = a[6:8].T
        answer[2][2] = 1

        return answer

    def matrixNormalize(self, p):   #将[x,y]转换成[x,y,1]
        n = np.ones((4, 3), dtype=np.float)
        n[:, 0:2] = p
        return n

    def ptSort(self, pt):   # 对获得的四个点顺序进行调整
        pt_position = []
        pt_position.append(pt[0][0] + pt[0][1])
        pt_position.append(pt[1][0] + pt[1][1])
        pt_position.append(pt[2][0] + pt[2][1])
        pt_position.append(pt[3][0] + pt[3][1])
        cor = {pt_position[0]: 0, pt_position[1]: 1, pt_position[2]: 2, pt_position[3]: 3}
        pt_position.sort()

        temp = [cor[pt_position[0]], cor[pt_position[1]], cor[pt_position[2]], cor[pt_position[3]]]

        pt_temp = np.zeros((4, 2), dtype=np.float)
        pt_temp[0] = pt[temp[0]]
        pt_temp[1] = pt[temp[2]]
        pt_temp[2] = pt[temp[3]]
        pt_temp[3] = pt[temp[1]]
        pt = pt_temp
        return pt

    def genImg(self, pts):
        img = np.zeros((480, 640, 3), np.uint8)
        cv2.polylines(img, pts, isClosed=True, color=(255, 255, 255), thickness=1)
        cv2.fillPoly(img, pts, color=(255, 255, 255))
        return img

    def calculatePerspective(self, pt, perspectiveMatrix):  #透视变换矩阵与点坐标相乘计算，得到透视变换或逆透视变换后的矩阵
        pt = self.matrixNormalize(pt)

        img = perspectiveMatrix.dot(pt.T).T
        #print(img)
        img = img.T / img[:, 2]
        pts = img.T[:, 0:2]

        pts = self.ptSort(pts)

        pts = np.array(pts, dtype=np.int32)
        return pts
# i1 = 220
# j1 = 140
#
# i2 = 420
# j2 = 140
#
# i3 = 220
# j3 = 340
#
# i4 = 420
# j4 = 340




if __name__ == '__main__':
    p1 = np.array([220, 140])
    p2 = np.array([420, 140])
    p3 = np.array([220, 340])
    p4 = np.array([420, 340])

    P1 = np.array([210, 140])
    P2 = np.array([424, 148])
    P3 = np.array([203, 355])
    P4 = np.array([420, 328])
    pt1 = np.array([p1, p2, p3, p4])
    pt2 = np.array([P1, P2, P3, P4])


    M = perspectiveMatrix()
    answer = M.getperspectiveMatrix(pt1, pt2)

    pts = M.calculatePerspective(pt1, answer)
    img = M.genImg(np.array([pts]))
    cv2.imshow("a", img)
    pts2 = M.calculatePerspective(pt2, np.linalg.pinv(answer))
    img_2 = M.genImg(np.array([pts2]))
    cv2.imshow("b", img_2)

    cv2.waitKey(0)