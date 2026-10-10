#!/usr/bin/env python3
"""Recompute the earlier exact local Jacobian witness; not a universality test."""
from fractions import Fraction as F
from itertools import product
import json

weights = ((1,2,3,4),(2,3,4,5),(3,4,5,6))
matrix = []
for x in list(product((0,1), repeat=4))[1:]:
    probabilities = []
    for row in weights:
        z = 1
        for a,bit in zip(row,x):
            z *= a**bit
        probabilities.append(F(z,1+z))
    matrix.append(list(map(F,x))+[s-F(1,2) for s in probabilities]+[F(bit)*s for s in probabilities[:2] for bit in x])
det = F(1)
for k in range(15):
    pivot = next((i for i in range(k,15) if matrix[i][k]),None)
    if pivot is None:
        raise ValueError('zero determinant')
    if pivot != k:
        matrix[pivot],matrix[k]=matrix[k],matrix[pivot]
        det = -det
    d = matrix[k][k]
    det *= d
    for i in range(k+1,15):
        scale = matrix[i][k]/d
        matrix[i] = [a-scale*b for a,b in zip(matrix[i],matrix[k])]
expected = F(-4292546820857203,11884241136598188669271898437500)
if det != expected:
    raise ValueError('different prior determinant')
print(json.dumps({'status':'PASS_PRIOR_JACOBIAN_RECHECK','determinant':str(det),'rank':15,'scope':'nonempty local image only; no global universality implication'},indent=2))
