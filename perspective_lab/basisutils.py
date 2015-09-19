#!/usr/bin/env python
#-*- coding:utf-8 -*-

from GF2 import one, One
from math import sqrt, pi
from matutil import coldict2mat
from solver import solve
from vec import Vec
from vecutil import list2vec

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def is_superfluous(S, v):
    '''
    Input:
        - S: set of vectors as instances of Vec class
        - v: vector in S as instance of Vec class
    Output:
        True if the span of the vectors of S is the same
        as the span of the vectors of S, excluding v.

        False otherwise.
    '''
    assert v in S
    new_S = S - {v}

    # empty space restriction
    if len(new_S) == 0:
        if len(v.f) == 0:
            return True
        return False
    basis = coldict2mat(list(new_S))
    # finding a representation of v in the new basis
    rep_v = solve(basis, v)
    err = basis * rep_v - v
    # if a vector over GF(2)
    GF2 = False
    for key in v.f:
        if isinstance(v.f[key], One):
            GF2= True
            break
    # is the representation addecuate
    if GF2:
        if err == Vec(err.D , {}):
            return True
        return False
    else:
        # if err^2 < 1e-20 is zero, therefore if superfluous
        if err*err < 1e-20:
            return True
        return False


def is_independent(S):
    '''
    Input:
        - S: a set of Vecs
    Output:
        - boolean: True if vectors in S are linearly independent
    '''
    if len(S) == 0:
        return True
    if (len(S) == 1):
        (vect, ) = S
        if len(vect.f) == 0:
            return False
    for vect in S:
        if is_superfluous(S, vect):
            return False
    return True


def exchange(S, A, z):
    '''
    Input:
        - S: a set of Vecs (not necessarily linearly independent)
        - A: a set of Vecs, a proper subset of S
        - z: an instance of Vec such that A | {z} is linearly independent
    Output: a vector w in S but not in A such that Span S = Span ({z} | S - {w})
    '''
    basis = coldict2mat(list(S))
    rep = solve(basis, z)

    for alpha, col in zip(rep, basis.D[1]):
        if alpha != 0:
            new_v = Vec(z.D, {i:basis[row,col] for i, row in zip(z.D, basis.D[0])})
            if new_v not in A:
                return (new_v)
