import numpy as np

def check(y,x,n,grid):
    # on the same row
    if n in grid[y]: return 0

    # on the same column
    for i in range(0,9):
        if grid[i][x] == n: return 0

    # on the same minor grid
    x = 3*int(x/3)
    y = 3*int(y/3)
    for i in range(0,3):
        for j in range(0,3):
            if grid[y+i][x+j] == n: return 0
    return 1

def solve(grid):
    # check if the grid is valid
    for y in range(0,9):
        for x in range(0,9):
            if grid[y][x] != 0:
                n = grid[y][x]
                grid[y][x] = 0
                if not check(y,x,n,grid):
                    grid[y][x] = n
                    return 0,grid
                grid[y][x] = n

    # solve the grid
    for y in range(0,9):
        for x in range(0,9):
            if grid[y][x] == 0:
                for i in range(1,10):
                    if check(y,x,i,grid):
                        grid[y][x] = i
                        c,igrid = solve(grid)
                        if c: return 1,igrid
                grid[y][x] = 0
                return 0,grid
    return 1,grid