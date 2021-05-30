import cv2
import numpy as np
import math
import copy
from scipy import ndimage
from step0 import load_ocr_model

def extract_board(puzzle,model):

    warp = puzzle.copy()
    gray = cv2.cvtColor(warp,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, 1, 1, 11, 2)
    warp = cv2.bitwise_not(thresh)
    _, warp = cv2.threshold(warp, 150, 255, cv2.THRESH_BINARY)


    size = 9

    board = []
    zero_list = [0,0,0,0,0,0,0,0,0]
    for l in range(9):
        board.append(zero_list.copy())

    h = int(warp.shape[0] / 9)
    w = int(warp.shape[1] / 9)

    offset_w = int(w / 10)
    offset_h = int(h / 10)

    for i in range(size):
        for j in range(size):

            crop_image = warp[h*i+offset_h:h*(i+1)-offset_h, w*j+offset_w:w*(j+1)-offset_w]        
            
            
            ratio = 0.6        
            
            while np.sum(crop_image[0]) <= (1-ratio) * crop_image.shape[1] * 255:
                crop_image = crop_image[1:]
            
            while np.sum(crop_image[:,-1]) <= (1-ratio) * crop_image.shape[1] * 255:
                crop_image = np.delete(crop_image, -1, 1)

            while np.sum(crop_image[:,0]) <= (1-ratio) * crop_image.shape[0] * 255:
                crop_image = np.delete(crop_image, 0, 1)

            while np.sum(crop_image[-1]) <= (1-ratio) * crop_image.shape[0] * 255:
                crop_image = crop_image[:-1]    


            crop_image = cv2.bitwise_not(crop_image)

            crop_image = crop_image.astype('uint8')
            num_labels, output, stats, centroids = cv2.connectedComponentsWithStats(crop_image, connectivity=8)
            sizes = stats[:, -1]

            if(len(sizes) <= 1):
                crop_image = np.zeros(crop_image.shape)
                crop_image.fill(255)
            else:
                max_l = 1
                max_s = sizes[1]     

                for k in range(2, num_labels):
                    if sizes[k] > max_s:
                        max_l = k
                        max_s = sizes[k]

                crop_image = np.zeros(output.shape)
                crop_image.fill(255)
                crop_image[output == max_l] = 0
            
            digit_size = 28
            crop_image = cv2.resize(crop_image, (digit_size,digit_size))

    

            if crop_image.sum() >= digit_size**2*255 - digit_size * 1 * 255:
                board[i][j] = 0
                continue    
            
            

            center_w = int(crop_image.shape[1] / 2)
            center_h = int(crop_image.shape[0] / 2)
            x_start = int(center_h / 2)
            x_end = int(center_h / 2) + center_h
            y_start = int(center_w / 2)
            y_end = int(center_w / 2) + center_w
            center_part = crop_image[x_start:x_end, y_start:y_end]
            
            if center_part.sum() >= center_w * center_h * 255 - 255:
                board[i][j] = 0
                continue
            
            
            
            rows, cols = crop_image.shape

            
            
            _, crop_image = cv2.threshold(crop_image, 200, 255, cv2.THRESH_BINARY) 
            crop_image = crop_image.astype(np.uint8)



            crop_image = cv2.bitwise_not(crop_image)

            y_center, x_center = ndimage.measurements.center_of_mass(crop_image)
            dx = np.round(cols/2.0-x_center).astype(int)
            dy = np.round(rows/2.0-y_center).astype(int)
            rows,cols = crop_image.shape
            M = np.float32([[1,0,dx],[0,1,dy]])
            crop_image = cv2.warpAffine(crop_image,M,(cols,rows))

            crop_image = cv2.bitwise_not(crop_image)
            
            

            crop_image = crop_image.reshape(-1, 28, 28, 1)
            crop_image = crop_image.astype('float32')
            crop_image /= 255

            pred = model.predict([crop_image])
            board[i][j] = np.argmax(pred[0]) + 1
    return board

# img = cv2.imread("puzzle6.png",1)
# model = load_ocr_model()
# board = extract_board(img,model)
# print(board)