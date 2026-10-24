"""Exact coefficient-change diagnostic for a selected cyclic cover.
This does not satisfy all-cover rational boundedness and is not a solution.
"""
import json

def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def power(a,n):
    out=[[int(i==j) for j in range(3)] for i in range(3)]
    for _ in range(n):out=mul(out,a)
    return out

def det(a):
    return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])

m=[[0,0,1],[1,0,1],[0,1,0]]
m4=power(m,4);m7=power(m,7)
a=[[m7[i][j]-int(i==j) for j in range(3)] for i in range(3)]
assert a==[[2*x for x in row] for row in m4]
assert det(m4)==1 and det(a)==8
print(json.dumps({'matrix':m,'power4':m4,'power7_minus_identity':a,'identity':'M^7-I=2M^4','unimodular_factor_determinant':1,'smith_factors':[2,2,2],'degree7_cover_H2_integral':0,'degree7_cover_b2_Q':0,'degree7_cover_b2_F2':3,'degree7_cover_H1_integral':'Z plus (C2)^3','scope':'selected cyclic cover only, not all-cover boundedness'},indent=2))
