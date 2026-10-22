#!/usr/bin/env python3
"""Independent exact double-pentagon checks; no candidate modules imported."""
from fractions import Fraction as F
import json

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    c=[F(0)]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    # Q[r]/(1+r+r^2+r^3+r^4), exact rational arithmetic.
    for d in range(6,3,-1):
        for j in range(4): c[d-4+j]-=c[d]
        c[d]=F(0)
    return tuple(c[:4])
Z=(F(0),)*4
I=(F(1),F(0),F(0),F(0))
r=(F(0),F(1),F(0),F(0))
def power(n):
    out=I
    for _ in range(n%5): out=mul(out,r)
    return out

def vertex(j,conj=False):
    out=Z
    for t in range(j): out=add(out,power(-t if conj else t))
    return out
P=[vertex(j) for j in range(5)]
Q=[vertex(j,True) for j in range(5)]
assert power(5)==I
assert sum((1 for _ in []),0)==0
corner_map=[]
edge_gluings=[]
for j in range(5):
    target=(1-j)%5
    assert sub(I,P[j])==Q[target]
    corner_map.append([j,target])
    k=(-j)%5
    v=sub(P[(j+1)%5],P[j])
    assert v==power(j)
    assert sub(Q[(k+1)%5],Q[k])==v
    trans=sub(P[j],Q[k])
    assert add(Q[(k+1)%5],trans)==P[(j+1)%5]
    for t in [F(0),F(1,5),F(1,2),F(4,5),F(1)]:
        point=add(P[j],tuple(t*x for x in v))
        h_in_P=add(sub(I,point),trans)
        expected=add(P[j],tuple((1-t)*x for x in v))
        assert h_in_P==expected
        assert (h_in_P==point)==(t==F(1,2))
    edge_gluings.append({'P_edge':j,'Q_edge':k,'h_reverses_edge_parameter':True})
# A0 terminal boundary direction -2pi/5 is r^-1; among Q clockwise outgoing edges it occurs only at q1.
a0_corners=[j for j in range(5) if sub(Q[(j+1)%5],Q[j])==power(-1)]
assert a0_corners==[1]
# Discrete exceptional directions, in units pi/5; no trigonometry or floating comparisons needed.
# For the four rays to the other initial pentagon vertices, beta = alpha + 2, N=1.
exceptions=[{'alpha_pi_over_5':a,'beta_pi_over_5':a+2,'N_segments':1,'graph_distance':1 if a in (0,3) else 2,'parity_selected_type':'A0' if a in (0,3) else ('A2' if a==1 else 'A1')} for a in range(4)]
print(json.dumps({'arithmetic':'Q[r]/(1+r+r^2+r^3+r^4)','h_P_to_Q_corner_indices':corner_map,'edge_gluings':edge_gluings,'A0_terminal_Q_corner_indices':a0_corners,'odd_N_bare_angle_exceptions':exceptions,'result':'all exact assertions passed'},indent=2))
