import numpy as np
def check(y,x,n,grid):
    if n in grid[y]: return 0
    for i in range(0,9):
        if grid[i][x] == n: return 0
    x = 3*int(x/3)
    y = 3*int(y/3)
    for i in range(0,3):
        for j in range(0,3):
            if grid[y+i][x+j] == n: return 0
    return 1
def solve(grid):
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