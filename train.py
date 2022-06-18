import cv2
import numpy as np

if __name__ == '__main__':
    p1 = np.array([220, 140])
    p2 = np.array([420, 140])
    p3 = np.array([220, 340])
    p4 = np.array([420, 340])

    P1 = np.array([232, 140])
    P2 = np.array([414, 158])
    P3 = np.array([203, 355])
    P4 = np.array([409, 358])
    pt1 = np.array([p1, p2, p3, p4])
    pt2 = np.array([P1, P2, P3, P4])
