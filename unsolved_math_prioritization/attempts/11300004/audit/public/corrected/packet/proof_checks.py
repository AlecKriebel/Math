#!/usr/bin/env python3
"""Finite exact diagnostics only. No claim to prove the wild-knot conjecture."""
from fractions import Fraction as F
from itertools import combinations
import json
import math
import os
import sys

def require(condition, message):
    if not condition:
        raise ValueError(message)

def determinant(matrix):
    a=[[F(x) for x in row] for row in matrix]
    n=len(a)
    require(n>0 and all(len(row)==n for row in a),'square matrix required')
    det=F(1)
    for i in range(n):
        pivot=next((j for j in range(i,n) if a[j][i]),None)
        if pivot is None:
            return F(0)
        if pivot!=i:
            a[i],a[pivot]=a[pivot],a[i]
            det=-det
        q=a[i][i]
        det*=q
        for k in range(i,n):
            a[i][k]/=q
        for j in range(i+1,n):
            q=a[j][i]
            for k in range(i,n):
                a[j][k]-=q*a[i][k]
    return det

def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def sub(a,b):return tuple(x-y for x,y in zip(a,b))

def collinear(points):
    require(len(points)>=2 and points[0]!=points[1],'distinct base points required')
    v=sub(points[1],points[0])
    return all(cross(v,sub(p,points[0]))==(0,0,0) for p in points[2:])

def main():
    # Variables t0,t1,t2,t3,A,B,C,D. Rows alternate y and z constraints.
    jac=[]
    for i in range(4):
        y=[0]*8;z=[0]*8
        y[4]=-1;y[5]=-i;z[6]=-1;z[7]=-i
        (y if i<2 else z)[i]=1
        jac.extend([y,z])
    det=determinant(jac)
    require(abs(det)==1,'transversal Jacobian determinant')
    # Separate the two distinct-support arguments from tuple counts.
    marked_counts=[]
    for m in [4,5,8,12,32]:
        pts=[(F(j,m),F(0),F(0)) for j in range(m)]
        count=sum(1 for q in combinations(pts,4) if collinear(q))
        require(count==math.comb(m,4),'one-line marked count')
        marked_counts.append({'contacts':m,'marked_unordered_quadruples':count,'supporting_lines':1})
    collapse=[]
    for n in [6,10,100,1000]:
        e=F(1,n)
        witness=[(j*e,F(0),F(0)) for j in [-3,-1,1,3]]
        require(len(set(witness))==4 and collinear(witness),'four-point collapse witness')
        require(max(p[0] for p in witness)-min(p[0] for p in witness)==6*e,'collapse span')
        # At distinct selected x values, the limit parabola is not collinear.
        limit_points=[(p[0],p[0]**2,F(0)) for p in witness]
        require(not collinear(limit_points),'parabola not collinear')
        collapse.append({'epsilon':str(e),'span':str(6*e),'uniform_error_bound':str(25*e*e)})
    # Exact tangent cluster vectors; normalization divides dot products by 5.
    plus=(F(0),F(1),F(2));minus=(F(0),F(1),F(-2))
    norm2=sum(x*x for x in plus)
    cosine=sum(x*y for x,y in zip(plus,minus))/norm2
    require(norm2==5 and cosine==F(-3,5),'limiting tangent cosine')
    # Straightening shear and its inverse, with rational test functions.
    for x,y,z in [(F(1,3),F(2,5),F(-4,7)),(F(-2),F(0),F(8))]:
        u=x*x;v=x*x*x
        moved=(x,y-u,z-v)
        back=(moved[0],moved[1]+u,moved[2]+v)
        require(back==(x,y,z),'shear inverse')
    print(json.dumps({'schema':'wild-quadrisecants-finite-checks-v1','main_problem_resolved':False,'formal_certification':False,'transversal_jacobian_determinant':str(det),'one_line_counts':marked_counts,'collapse_samples':collapse,'limiting_tangent_cosine':str(cosine),'uid':os.geteuid(),'optimize':sys.flags.optimize,'scope':'exact finite diagnostics; mathematical arguments remain human-readable'},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except (ValueError,ArithmeticError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr)
        sys.exit(1)
