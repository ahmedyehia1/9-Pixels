import numpy as np
from imutils import perspective
import imutils
import cv2

def get_euler_distance(pt1, pt2):
        return ((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)**0.5

def extract_puzzle(img):
    # print(len(img.shape))
    if len(img.shape) == 3:
        img_copy = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(img_copy, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, 1, 1, 11, 2)
    minLineLength = max(img.shape[0],img.shape[1])
    maxLineGap = 10
    lines = cv2.HoughLinesP(thresh,1,np.pi/180,100,minLineLength,maxLineGap)
    new_img = np.zeros(thresh.shape,np.uint8)
    new_img_2 = np.zeros(thresh.shape,np.uint8)
    if lines is None or len(lines)< 1:
        return None
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(new_img,(x1,y1),(x2,y2),255,2)
    
    contours, _ = cv2.findContours(new_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) < 1:
        return img
    c = max(contours,key=cv2.contourArea)
    epsilon = 0.1*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    if (len(approx))!= 4:
        return img
    # x,y,w,h = cv2.boundingRect(c)
    # cv2.rectangle(img,(x,y),(x+w,y+h),1)
    # cv2.drawContours(img, [c], 0, (0,255,0), 1)

    
    # print(approx)
    # src_pts = np.array([[8, 136], [415, 52], [420, 152], [14, 244]], dtype=np.float32)
    points = perspective.order_points(approx.reshape(4,2))
    (tl, tr, br, bl) = points
    # print(points)
    # points = np.array(points.reshape(4,2),dtype=np.float32)
    # pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
    width = max(get_euler_distance(tl,tr),get_euler_distance(bl, br))
    height = max(get_euler_distance(tl,bl),get_euler_distance(tr, br))
    # print(width,height)
    dst = np.array([[0, 0],[width-1, 0],[width-1, height-1],[0, height-1]], dtype = np.float32)
    # print(width,height)
    M = cv2.getPerspectiveTransform(points, dst)
    warp = cv2.warpPerspective(img, M, (int(width), int(height)))

    inv_M = np.linalg.pinv(M)
    
    # print(M)
    # cv2.drawContours(new_img_2, [approx], 0, 255, 3)
    return warp,inv_M


def unwarp_puzzle(img,warp,inv_M):
    mask = np.zeros_like(img)

    unwarp =cv2.warpPerspective(warp, inv_M, (img.shape[1], img.shape[0]))
    mask[unwarp > 0] = 255
    mask = 255 - mask
    img = cv2.bitwise_and(mask,img)
    result = cv2.bitwise_or(img,unwarp)
    return result



# img = cv2.imread("sudoku_puzzle2.png",1)
# img,inv = extract_puzzle(img)
# cv2.imwrite("puzzle6.png",img)
# cv2.imshow("",img)
# cv2.waitKey(0)