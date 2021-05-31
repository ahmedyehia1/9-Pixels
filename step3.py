import cv2 
import numpy as np

def write_on_board(warp,board,solved_board):
    color = (0,255,255) 
    fontType = cv2.LINE_AA
    fontScale = 1
    thickness = 3
    font = cv2.FONT_HERSHEY_SIMPLEX

    size = 9

    h = int(warp.shape[0] / 9)
    w = int(warp.shape[1] / 9)

    offset_h = int(h / 20)
    offset_w = int(w / 20)

    for i in range(size):
        for j in range(size):
            if(solved_board[i][j] != board[i][j]):    # If user fill this cell
                digit = str(solved_board[i][j])
                (text_h, text_w), baseLine = cv2.getTextSize(digit, font, fontScale, thickness)
            
                font_scale = 0.6 * min(w, h) / max(text_h, text_w)
                text_h *= font_scale
                text_w *= font_scale
                bottom_left__x = w*j + int((w - text_w) / 2) + offset_w
                bottom_left__y = h*(i+1) - int((h - text_h) / 2) + offset_h
                warp = cv2.putText(warp, digit, (bottom_left__x, bottom_left__y), font, font_scale, color, thickness, fontType)
    
    return warp
    

img = cv2.imread("puzzle6.png",1)

grid = np.array([[5,4,1,2,8,7,0,0,3]
                ,[2,3,6,1,4,9,0,0,0]
                ,[7,8,9,3,5,0,0,2,0]
                ,[1,2,3,4,6,5,0,8,0]
                ,[4,5,7,8,9,1,0,3,0]
                ,[6,0,8,0,2,0,0,1,0]
                ,[3,0,4,5,7,0,0,0,0]
                ,[8,0,5,9,0,2,3,4,7]
                ,[9,7,0,6,0,4,0,5,1]])



def compare_boards(old_board,new_board):
    return (old_board == new_board).all() 

# grid_solved = np.array([[5,4,1,2,8,7,6,9,3],
#  [2,3,6,1,4,9,5,7,8],
#  [7,8,9,3,5,6,1,2,4],
#  [1,2,3,4,6,5,7,8,9],
#  [4,5,7,8,9,1,2,3,6],
#  [6,9,8,7,2,3,4,1,5],
#  [3,1,4,5,7,8,9,6,2],
#  [8,6,5,9,1,2,3,4,7],
#  [9,7,2,6,3,4,8,5,1]])

# # img = write_on_board(img,grid,grid_solved)
# # cv2.imshow("",img)
# # cv2.waitKey(0)
# print(compare_boards(grid.copy(),grid.copy()))
# print(compare_boards(grid.copy(),grid_solved.copy()))

