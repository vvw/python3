#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from vec import Vec
from mat import Mat
from matutil import rowdict2mat
from solver import solve
from perspective_lab import move2board, D, make_equations, w, b, make_nine_equations, L, hvec, H, mat_move2board


def problem1():
    print('------problem1------')
    y = Vec({'y1','y2','y3'}, {'y1':1,'y2':3,'y3':5})
    print(move2board(y))

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem2():
    print('------problem2------')
    print(D)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem3():
    print('------problem3------')
    for v in make_equations(8,25,1,0): print(v)
    print('~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~')
    for v in make_equations(18,23,1,1): print(v)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem4():
    print('------problem4------')
    print(w)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem5():
    print('------problem5------')
    print(b)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem6():
    print('------problem6------')
    # corn = [('top','left'), ('bottom','left'), ('top','right'), ('bottom','right')]
    corn = [(358, 36), (329, 597), (592, 157), (580, 483)]
    print(make_nine_equations(corn))

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem8():
    print('------problem8------')
    print(L)
    print(b)
    print(hvec)
    print(L*hvec)
    err = (L*hvec) - b
    print(err*err)
    myH = Mat(({'y1','y2','y3'}, {'x1','x2','x3'}), {('y1', 'x1'):1.0, ('y1', 'x2'):0.0516934, ('y1', 'x3'):-359.861, ('y2', 'x1'):-0.381521, ('y2', 'x2'):0.737818, ('y2', 'x3'):110.023, ('y3', 'x1'):-0.721936, ('y3', 'x2'):-0.0116907, ('y3', 'x3'):669.476})
    print(myH)
    print(H)
    print(H * Vec({'x1','x2','x3'}, {'x1':592, 'x2':157, 'x3':1}))
    
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem9():
    print('------problem9------')
    Y_in = Mat(({'y1', 'y2', 'y3'}, {0,1,2,3}),
        {('y1',0):2, ('y2',0):4, ('y3',0):8,
        ('y1',1):10, ('y2',1):5, ('y3',1):5,
        ('y1',2):4, ('y2',2):25, ('y3',2):2,
        ('y1',3):5, ('y2',3):10, ('y3',3):4})
    print(Y_in)
    print(mat_move2board(Y_in))

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def main():
    os.system('clear')
    print('\n')
    problem3()
    print('\n\n')

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

if __name__ == '__main__':
    main()
