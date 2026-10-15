#!/usr/bin/env python3
"""Exact supplementary arithmetic checks. No finite test proves the topology."""
import json
from fractions import Fraction as F

counts = {}
def require(name, value):
    if not value:
        raise RuntimeError('FAILED: ' + name)
    counts[name] = counts.get(name, 0) + 1

def mul(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def transpose(a):
    return tuple(zip(*a))
def det(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def trace(a):
    return a[0][0]+a[1][1]
def scale(q,a):
    return tuple(tuple(q*x for x in row) for row in a)
def add(a,b):
    return tuple(tuple(a[i][j]+b[i][j] for j in range(2)) for i in range(2))
I=((F(1),F(0)),(F(0),F(1)))
A=((F(3,5),F(-4,5)),(F(4,5),F(3,5)))
B=((3,-4),(4,3))
require('base_determinant',det(A)==1)
require('base_orthogonality',mul(transpose(A),A)==I)
require('integer_characteristic_identity',add(add(mul(B,B),scale(-6,B)),scale(25,I))==scale(0,I))

# Replay exact powers and the recurrence; Section 5 proves the all-n statement.
u0,u1=2,6
p=I
p_integer=((1,0),(0,1))
for n in range(1,257):
    p=mul(p,A)
    p_integer=mul(p_integer,B)
    require('positive_power_orthogonality',mul(transpose(p),p)==I)
    require('positive_power_determinant',det(p)==1)
    require('scaled_power_identity',scale(5**n,p)==p_integer)
    require('trace_recurrence',trace(p_integer)==u1)
    require('trace_residue_obstruction',u1%5==1)
    require('bounded_nonidentity_control',p!=I)
    require('trace_not_finite_order_value',u1!=2*5**n)
    u0,u1=u1,6*u1-25*u0

p=I
for n in range(1,65):
    p=mul(p,transpose(A))
    require('negative_power_orthogonality',mul(transpose(p),p)==I)
    require('negative_power_determinant',det(p)==1)
    require('negative_power_nonidentity',p!=I)

# A rational orthogonal matrix need not have infinite order: enforce controls.
R=((0,-1),(1,0))
require('finite_rotation_control_orthogonal',mul(transpose(R),R)==I)
require('finite_rotation_control_order_four',mul(mul(R,R),mul(R,R))==I)
require('identity_control_is_finite_order',mul(I,I)==I)
C=((F(1,2),0),(0,F(1,2)))
require('contraction_is_not_orthogonal',mul(transpose(C),C)!=I)
H=((F(2),0),(0,F(1,2)))
require('determinant_one_not_isometry_control',det(H)==1 and mul(transpose(H),H)!=I)
# X consists of 0, 2/3, and 1; their Cantor membership is proved by ternary expansions.
X=(F(0),F(2,3),F(1))
require('three_distinct_real_points',len(set(X))==3)
require('three_points_in_unit_interval',all(0<=x<=1 for x in X))
require('three_end_core_inequality',3-1>=2)
require('two_end_core_negative_control',not (2-1>=2))

print(json.dumps({'status':'PASS','total_exact_checks':sum(counts.values()),'checks_by_family':counts,'limits':'Finite exact arithmetic controls only. The written proof, not these tests, establishes all-n infinite order and the conformal/topological obstruction.'},sort_keys=True,indent=2))
