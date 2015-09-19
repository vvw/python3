#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from GF2 import one, One
from math import sqrt, pi
from matutil import coldict2mat, listlist2mat
from solver import solve
from mat import Mat
from vec import Vec
from vecutil import list2vec
from basisutils import exchange
from independence import is_independent, rank
from Dimension_problems import direct_sum_decompose, is_invertible, find_matrix_inverse, find_triangular_matrix_inverse

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~



# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem1():
    print('------problem1------')
    w0 = Vec({0,1,2}, {0:1})
    w1 = Vec({0,1,2}, {1:1})
    w2 = Vec({0,1,2}, {2:1})
    v0 = Vec({0,1,2}, {0:1, 1:2, 2:3})
    v1 = Vec({0,1,2}, {0:1, 1:3, 2:3})
    v2 = Vec({0,1,2}, {1:3, 2:3})
    S = {w0, w1, w2}
    A = {}
    print('     ----')
    print(exchange(S, A, v0))
    S = {w0, w1, v0}
    A = {v0}
    print('     ----')
    print(exchange(S, A, v1))
    S = {w0, v0, v1}
    A = {v0, v1}
    print('     ----')
    print(exchange(S, A, v2))

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem2():
    print('------problem2------')
    w0 = Vec({0,1,2}, {1:one})
    w1 = Vec({0,1,2}, {2:one})
    w2 = Vec({0,1,2}, {0:one, 1:one, 2:one})
    v0 = Vec({0,1,2}, {0:one, 2:one})
    v1 = Vec({0,1,2}, {0:one})
    v2 = Vec({0,1,2}, {0:one, 1:one})
    S = {w0, w1, w2}
    A = {}
    print('     ----')
    print(exchange(S, A, v0))
    S = {w1, w2, v0}
    A = {v0}
    print('     ----')
    print(exchange(S, A, v1))
    S = {w2, v0, v1}
    A = {v0, v1}
    print('     ----')
    print(exchange(S, A, v2))

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def morph(S, B):
    '''
    Input:
        - S: a list of distinct Vecs
        - B: a list of linearly independent Vecs all in Span S
    Output: a list of pairs of vectors to inject and eject (see problem description)
    '''
    S0 = S.copy()
    A = set([])
    pairs = []
    for z in B:
        w = exchange(set(S0), A, z)
        # S0 = (S0 | {z}) - {w}
        S0.append(z)
        S0.remove(w)
        # A = A | {z}
        A = A | {z}
        pairs.append((z,w))
    return pairs
        
        

def problem3():
    print('------problem3------')
    #w0 = Vec({0,1,2}, {1:one})
    #w1 = Vec({0,1,2}, {2:one})
    #w2 = Vec({0,1,2}, {0:one, 1:one, 2:one})
    #v0 = Vec({0,1,2}, {0:one, 2:one})
    #v1 = Vec({0,1,2}, {0:one})
    #v2 = Vec({0,1,2}, {0:one, 1:one})
    #S = [w0, w1, w2]
    #B = [v0, v1, v2]
    #print(morph(S, B))
    #print(morph(S, B) ==  [(Vec({0, 1, 2},{0: one, 2: one}), Vec({0, 1, 2},{0: 0, 1: one, 2: 0})), (Vec({0, 1, 2},{0: one}), Vec({0, 1, 2},{0: 0, 1: 0, 2: one})), (Vec({0, 1, 2},{0: one, 1: one}), Vec({0, 1, 2},{0: one, 1: one, 2: one}))])
    print('~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~')
    S = [list2vec(v) for v in [[1,0,0],[0,1,0],[0,0,1]]]
    B = [list2vec(v) for v in [[1,1,0],[0,1,1],[1,0,1]]]
    D = {0, 1, 2}
    print(morph(S, B) == [(Vec(D,{0: 1, 1: 1, 2: 0}), Vec(D,{0: 1, 1: 0, 2: 0})), (Vec(D,{0: 0, 1: 1, 2: 1}), Vec(D,{0: 0, 1: 1, 2: 0})), (Vec(D,{0: 1, 1: 0, 2: 1}), Vec(D,{0: 0, 1: 0, 2: 1}))])
    print(S == [list2vec(v) for v in [[1,0,0],[0,1,0],[0,0,1]]])
    print(B == [list2vec(v) for v in [[1,1,0],[0,1,1],[1,0,1]]])
    print('~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~')
    D = {0, 1, 2, 3, 4, 5, 6, 7}
    S = [Vec(D,{1: one, 2: one, 3: one, 4: one}), Vec(D,{1: one, 3: one}), Vec(D,{0: one, 1: one, 3: one, 5: one, 6: one}), Vec(D,{3: one, 4: one}), Vec(D,{3: one, 5: one, 6: one})]
    B = [Vec(D,{2: one, 4: one}), Vec(D,{0: one, 1: one, 2: one, 3: one, 4: one, 5: one, 6: one}), Vec(D,{0: one, 1: one, 2: one, 5: one, 6: one})]
    sol = morph(S, B)
    print(sol == [(B[0],S[0]), (B[1],S[2]), (B[2],S[3])] or sol == [(B[0],S[1]), (B[1],S[2]), (B[2],S[3])])
    print('~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~')
    from random import random
    sol = morph(sorted(S, key=lambda x:random()), B)
    print(sol == [(B[0],S[0]), (B[1],S[2]), (B[2],S[3])] or sol == [(B[0],S[1]), (B[1],S[2]), (B[2],S[3])])

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def subset_basis(T):
    '''
    Input:
        - T: a set of Vecs
    Output: 
        - set S containing Vecs from T that is a basis for Span T.
    '''
    S = set()
    for v in T:
        if is_independent(S | {v}):
            S = S | {v}
    return S

def problem5():
    print('------problem5------')
    a0 = Vec({'a','b','c','d'}, {'a':1})
    a1 = Vec({'a','b','c','d'}, {'b':1})
    a2 = Vec({'a','b','c','d'}, {'c':1})
    a3 = Vec({'a','b','c','d'}, {'a':1,'c':3})
    sb = subset_basis({a0, a1, a2, a3})
    print(len(sb))
    print(all(v in [a0, a1, a2, a3] for v in sb))
    print(is_independent(sb))
    print('~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~')
    b0 = Vec({0,1,2,3},{0:2,1:2,3:4})
    b1 = Vec({0,1,2,3},{0:1,1:1})
    b2 = Vec({0,1,2,3},{2:3,3:4})
    b3 = Vec({0,1,2,3},{3:3})
    sb = subset_basis({b0, b1, b2, b3})
    print(len(sb))
    print(all(v in [b0, b1, b2, b3] for v in sb))
    print(is_independent(sb))
    print('~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~')
    D = {'a','b','c','d'}
    c0, c1, c2, c3, c4 = Vec(D,{'d': one, 'c': one}), Vec(D,{'d': one, 'a': one, 'c': one, 'b': one}), Vec(D,{'a': one}), Vec(D,{}), Vec(D,{'d': one, 'a': one, 'b': one})
    print(subset_basis({c0,c1,c2,c3,c4}) == {c0,c1,c2,c4})

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def superset_basis(C, T):
    '''
    Input:
        - C: linearly independent set of Vecs
        - T: set of Vecs such that every Vec in C is in Span(T)
    Output:
        Linearly independent set S consisting of all Vecs in C and some in T
        such that the span of S is the span of T (i.e. S is a basis for the span
        of T).
    '''
    S = set()
    for v in C:
        if is_independent(S | {v}):
            S = S | {v}
    for v in T:
        if is_independent(S | {v}):
            S = S | {v}
    return S
        

def problem6():
    print('------problem6------')
    a0 = Vec({'a','b','c','d'}, {'a':1})
    a1 = Vec({'a','b','c','d'}, {'b':1})
    a2 = Vec({'a','b','c','d'}, {'c':1})
    a3 = Vec({'a','b','c','d'}, {'a':1,'c':3})
    sb = superset_basis({a0, a3}, {a0, a1, a2})
    print(a0 in sb and a3 in sb)
    print(is_independent(sb))
    print(all(x in [a0,a1,a2,a3] for x in sb))

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def my_is_independent(L):
    '''
    Input:
        - L: a list of Vecs
    Output:
        - boolean: true if the list is linearly independent
    '''
    return rank(L) == len(L)

def problem7():
    print('------problem7------')
    D = {0, 1, 2}
    L = [Vec(D,{0: 1}), Vec(D,{1: 1}), Vec(D,{2: 1}), Vec(D,{0: 1, 1: 1, 2: 1}), Vec(D,{0: 1, 1: 1}), Vec(D,{1: 1, 2: 1})]
    print(my_is_independent(L))
    print(my_is_independent(L[:2]))
    print(my_is_independent(L[:3]))
    print(my_is_independent(L[1:4]))
    print(my_is_independent(L[0:4]))
    print(my_is_independent(L[2:]))
    print(my_is_independent(L[2:5]))
    print(L == [Vec(D,{0: 1}), Vec(D,{1: 1}), Vec(D,{2: 1}), Vec(D,{0: 1, 1: 1, 2: 1}), Vec(D,{0: 1, 1: 1}), Vec(D,{1: 1, 2: 1})])
    
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def my_rank(L):
    '''
    Input: 
        - L: a list of Vecs
    Output: 
        - the rank of the list of Vecs
    Example:
        >>> L = [list2vec(v) for v in [[1,2,3],[4,5,6],[1.1,1.1,1.1]]]
        >>> my_rank(L)
        2
        >>> L == [list2vec(v) for v in [[1,2,3],[4,5,6],[1.1,1.1,1.1]]]
        True
        >>> my_rank([list2vec(v) for v in [[1,1,1],[2,2,2],[3,3,3],[4,4,4],[123,432,123]]])
        2
    '''
    return len(subset_basis(L))

def problem8():
    print('------problem8------')
    L = [list2vec(v) for v in [[1,2,3],[4,5,6],[1.1,1.1,1.1]]]
    print(my_rank(L))
    print(L == [list2vec(v) for v in [[1,2,3],[4,5,6],[1.1,1.1,1.1]]])
    print(my_rank([list2vec(v) for v in [[1,1,1],[2,2,2],[3,3,3],[4,4,4],[123,432,123]]]))

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem9():
    print('------problem9------')
    D = {0,1,2,3,4,5}
    U_basis = [Vec(D,{0: 2, 1: 1, 2: 0, 3: 0, 4: 6, 5: 0}), Vec(D,{0: 11, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0}), Vec(D,{0: 3, 1: 1.5, 2: 0, 3: 0, 4: 7.5, 5: 0})]
    V_basis = [Vec(D,{0: 0, 1: 0, 2: 7, 3: 0, 4: 0, 5: 1}), Vec(D,{0: 0, 1: 0, 2: 15, 3: 0, 4: 0, 5: 2})]
    w = Vec(D,{0: 2, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0})
    (u, v) = direct_sum_decompose(U_basis, V_basis, w)
    print((u + v - w).is_almost_zero())
    # True
    U_matrix = coldict2mat(U_basis)
    V_matrix = coldict2mat(V_basis)
    print((u - U_matrix*solve(U_matrix, u)).is_almost_zero())
    # True
    print((v - V_matrix*solve(V_matrix, v)).is_almost_zero())
    # True
    print('~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~')
    ww = Vec(D,{0: 2, 1: 5, 2: 51, 4: 1, 5: 7})
    (u, v) = direct_sum_decompose(U_basis, V_basis, ww)
    print((u + v - ww).is_almost_zero())
    # True
    print((u - U_matrix*solve(U_matrix, u)).is_almost_zero())
    # True
    print((v - V_matrix*solve(V_matrix, v)).is_almost_zero())
    # True
    print(U_basis == [Vec(D,{0: 2, 1: 1, 2: 0, 3: 0, 4: 6, 5: 0}), Vec(D,{0: 11, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0}), Vec(D,{0: 3, 1: 1.5, 2: 0, 3: 0, 4: 7.5, 5: 0})])
    # True
    print(V_basis == [Vec(D,{0: 0, 1: 0, 2: 7, 3: 0, 4: 0, 5: 1}), Vec(D,{0: 0, 1: 0, 2: 15, 3: 0, 4: 0, 5: 2})])
    # True
    print(w == Vec(D,{0: 2, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0}))
    # True

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem10():
    print('------problem10------')
    M = Mat(({0, 1, 2, 3}, {0, 1, 2, 3}), {(0, 1): 0, (1, 2): 1, (3, 2): 0, (0, 0): 1, (3, 3): 4, (3, 0): 0, (3, 1): 0, (1, 1): 2, (2, 1): 0, (0, 2): 1, (2, 0): 0, (1, 3): 0, (2, 3): 1, (2, 2): 3, (1, 0): 0, (0, 3): 0})
    print(is_invertible(M))
    M1 = Mat(({0,1,2},{0,1,2}),{(0,0):1,(0,2):2,(1,2):3,(2,2):4})
    print(is_invertible(M1))

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem11():
    print('------problem11------')
    M1 = Mat(({0,1,2}, {0,1,2}), {(0, 1): one, (1, 0): one, (2, 2): one})
    print(find_matrix_inverse(M1) == Mat(M1.D, {(0, 1): one, (1, 0): one, (2, 2): one}))
    M2 = Mat(({0,1,2,3},{0,1,2,3}),{(0,1):one,(1,0):one,(2,2):one})
    print(find_matrix_inverse(M2) == Mat(M2.D, {(0, 1): one, (1, 0): one, (2, 2): one}))

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def problem12():
    print('------problem12------')
    A = listlist2mat([[1, .5, .2, 4],[0, 1, .3, .9],[0,0,1,.1],[0,0,0,1]])
    print(find_triangular_matrix_inverse(A) == Mat(({0, 1, 2, 3}, {0, 1, 2, 3}), {(0, 1): -0.5, (1, 2): -0.3, (3, 2): 0.0, (0, 0): 1.0, (3, 3): 1.0, (3, 0): 0.0, (3, 1): 0.0, (2, 1): 0.0, (0, 2): -0.05000000000000002, (2, 0): 0.0, (1, 3): -0.87, (2, 3): -0.1, (2, 2): 1.0, (1, 0): 0.0, (0, 3): -3.545, (1, 1): 1.0}))

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def main():
    os.system('clear')
    print('\n')
    problem12()
    print('\n\n')

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

if __name__ == '__main__':
    main()


