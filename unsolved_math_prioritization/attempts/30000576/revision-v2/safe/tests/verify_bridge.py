#!/usr/bin/env python3
"""Exact finite controls only. None of these finite-dimensional models is hypercyclic."""
from fractions import Fraction as Q
from itertools import product
import json

counts = {}
def eq(name, a, b):
    assert a == b, (name, a, b)
    counts[name] = counts.get(name, 0) + 1

def add(x,y): return tuple(a+b for a,b in zip(x,y))
def scale(c,x): return tuple(c*a for a in x)
def shear(t,x): return (x[0]+t*x[1],x[1])
def cscale(a,b,z):
    x,y=z
    return (add(scale(a,x),scale(-b,y)),add(scale(b,x),scale(a,y)))
def complex_shear(t,z): return tuple(shear(t,x) for x in z)
def norm2(z):
    x,y=z
    # Sup_theta max_j |cos(theta)x_j-sin(theta)y_j| squared.
    return max(x[j]*x[j]+y[j]*y[j] for j in range(2))
def rnorm(x): return max(map(abs,x))

v = list(product([Q(-1),Q(0),Q(1)],repeat=2))
times = [Q(0),Q(1,3),Q(1,2),Q(1),Q(2)]
for x,t,s in product(v,times,times):
    eq('semigroup_law',shear(t,shear(s,x)),shear(t+s,x))
    eq('commutation',shear(t,shear(s,x)),shear(s,shear(t,x)))
for x,y,t in product(v,v,times):
    z=(x,y)
    eq('real_projection_intertwines',complex_shear(t,z)[0],shear(t,x))
    eq('diagonal_identification',complex_shear(t,z),(shear(t,x),shear(t,y)))
    for n in [1,2,5,17]:
        eq('perturbation_identity',shear(t,add(x,scale(Q(1,n),y))),
           add(shear(t,x),scale(Q(1,n),shear(t,y))))
    for a,b in [(Q(0),Q(0)),(Q(1),Q(0)),(Q(0),Q(1)),(Q(3,5),Q(4,5)),(Q(-2),Q(3))]:
        eq('complex_linearity',complex_shear(t,cscale(a,b,z)),
           cscale(a,b,complex_shear(t,z)))
        eq('norm_complex_homogeneity_squared',norm2(cscale(a,b,z)),(a*a+b*b)*norm2(z))
    assert max(rnorm(x)**2,rnorm(y)**2)<=norm2(z)<=(rnorm(x)+rnorm(y))**2
    counts['norm_equivalence_bounds']=counts.get('norm_equivalence_bounds',0)+1
for x,y,n in product(v,v,range(1,13)):
    def bp(w):return (((-1)**n)*w[0],(2**n)*w[1])
    complex_periodic=(bp(x),bp(y))==(x,y)
    eq('fixed_n_periodic_coordinates',complex_periodic,bp(x)==x and bp(y)==y)
    if complex_periodic:
        eq('periodic_projection',bp(x),x)
# A naive sum norm fails complex homogeneity even for a unit scalar.
z=((Q(1),Q(0)),(Q(0),Q(0)))
rz=cscale(Q(3,5),Q(4,5),z)
eq('reject_naive_sum_norm',rnorm(rz[0])+rnorm(rz[1]),Q(7,5))
eq('correct_rotation_norm',norm2(rz),norm2(z))
print(json.dumps({'status':'pass','exact_checks':counts,
                  'total_exact_checks':sum(counts.values()),
                  'finite_controls_only':True,
                  'hypercyclicity_numerically_tested':False},indent=2,sort_keys=True))
