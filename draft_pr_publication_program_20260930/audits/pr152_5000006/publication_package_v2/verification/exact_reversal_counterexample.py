#!/usr/bin/env python3
"""Exact Q(sqrt(5)) certificate for the pentagon palindrome witness.

Coordinates are x in Q(sqrt(5)), y=s*y_coeff, s=sin(pi/5)>0.
No nonstandard imports and no removable assert controls.
"""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[0],-x[1])
def sub(x,y):return add(x,neg(y))
def mul(x,y):return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def inv(x):
    den=x[0]*x[0]-5*x[1]*x[1]
    return (x[0]/den,-x[1]/den)
def scalar(p,q=1):return (F(p,q),F(0))
def scale(x,p,q=1):return mul(x,scalar(p,q))
def positive(x):
    a,b=x
    if b==0:return a>0
    if a>=0 and b>0:return True
    if a<=0 and b<0:return False
    return (5*b*b>a*a) if b>0 else (a*a>5*b*b)
def serial(x):return [str(x[0]),str(x[1])]
c=(F(1,4),F(1,4)) # cos36
u=(F(-1,4),F(1,4)) # cos72
s2=sub(scalar(1),mul(c,c))
v_coeff=scale(c,2) # sin72/sin36
A=(scalar(0),scalar(2))
B=(scalar(5,4),scale(mul(c,c),2))
checks={}
def ck(name,v):
    if not v:raise RuntimeError(name)
    checks[name]=True
ck('regular_pentagon_cosine_relation',sub(sub(scale(mul(c,c),4),scale(c,2)),scalar(1))==scalar(0))
ck('cos72_identity',u==sub(scale(mul(c,c),2),scalar(1)))
ck('cos36_cos72_quarter',mul(c,u)==scalar(1,4))
# Side1 is P1=(-u,2c*s) to P2=(1/2,(2c+1)*s).
t=mul(u,inv(c))
ck('A_on_side1_x',add(neg(u),mul(t,c))==A[0])
ck('A_on_side1_y',add(v_coeff,t)==A[1])
ck('A_strict_side_interior',positive(t) and positive(sub(scalar(1),t)))
# Side3 is P4=(1,0) to P3=(1+u,2c*s), B=P4+c*(P3-P4).
ck('B_on_side3_x',add(scalar(1),mul(c,u))==B[0])
ck('B_on_side3_y',mul(c,v_coeff)==B[1])
ck('B_strict_side_interior',positive(c) and positive(sub(scalar(1),c)))
# AB is normal to side3 (whose tangent is (u,v_coeff*s)).
dx=sub(B[0],A[0]);dy=sub(B[1],A[1])
dot=add(mul(dx,u),mul(mul(dy,v_coeff),s2))
ck('AB_normal_to_side3',dot==scalar(0))
# Side1 unit tangent=(c,s). Reflection of d=(0,1) gives
# d'=(2cs,2s^2-1)=(sin72,-cos72), parallel to AB.
# Direct reflection of the positive vertical vector (0,s) in side1.
# Unit tangent is (c,s); y is represented by its coefficient of s.
first_rx=scale(mul(c,s2),2)
first_ry=sub(scale(s2,2),scalar(1))
ck('first_side1_reflection_collinear_with_AB',sub(mul(first_rx,dy),mul(first_ry,dx))==scalar(0))
ck('first_side1_reflection_positive_scale',positive(first_rx) and positive(dx))
ck('side3_tangent_unit',add(mul(u,u),mul(mul(v_coeff,v_coeff),s2))==scalar(1))
# Reflection of BA in side1 must point vertically down to O.
final_dot=neg(add(mul(dx,c),mul(dy,s2)))
final_rx=add(scale(mul(c,final_dot),2),dx)
final_ry=add(scale(final_dot,2),dy)
ck('final_side1_reflection_vertical',final_rx==scalar(0))
ck('final_side1_reflection_downwards',positive(neg(final_ry)))
ck('normal_middle_reflection_retraces',dot==scalar(0))
# The final reflected direction is (0,-1), so O-A-B-A-O is physical and
# reversing its orientation gives the identical billiard path.
alpha=F(1,2);beta=F(1,2);N=4;n=5
s=F(n,2)*(beta-alpha)
k=int(s-1)%(n-2)
ar=1-beta;br=1-alpha
kr=int(F(n,2)*(br-ar)-1)%(n-2)
ck('forward_source_type_2',k==2)
ck('physical_reverse_source_type_2',kr==2)
ck('contradicts_unqualified_minus_k',kr!=(-k)%(n-2))
receipt={'status':'PASS','field':'Q(sqrt(5)) with y scaled by positive sin(pi/5)',
         'coordinates':{'A':[serial(A[0]),serial(A[1])],'B':[serial(B[0]),serial(B[1])]},
         'side_reflections_zero_based':[1,3,1],'segments':N,'initial_angle_pi_units':str(alpha),'terminal_beta_pi_units':str(beta),
         'source_type':k,'physical_reverse_source_type':kr,'candidate_unqualified_prediction':(-k)%(n-2),
         'checks':checks,'check_count':len(checks),
         'limitation':'Counterexample to the unqualified physical source-label reversal statement, not to sine-ratio Conjecture 2.7.'}
(ROOT/'exact_reversal_counterexample.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
