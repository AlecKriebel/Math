#!/usr/bin/env python3
"""Exact finite algebra checks. Does not certify geometric K-theory claims."""
from fractions import Fraction
from itertools import product
from collections import Counter
import json

def require(condition):
    if not condition:
        raise RuntimeError("Exact identity check failed")

# Coordinates: f(x)[0]_y, f(x)H_y, [0]_x f(y), H_x f(y).
# Treat m as a formal variable by representing constant and linear coefficient.
eta = [(0,0),(1,0),(0,1),(0,0)]
swap_eta = [(0,1),(0,0),(0,0),(1,0)]
boundary_pair = [(0,1),(-1,0),(0,-1),(1,0)]
sub = lambda a,b: [(x[0]-y[0],x[1]-y[1]) for x,y in zip(a,b)]
require(sub(swap_eta,eta)==boundary_pair)

# Theta(P)=A, theta(2P)=B, theta(3P)=A.
h = {1:0,2:1,3:0}
epsilon = {1:0,2:1,3:0}
def wedge(i,j):
    return 0 if i==j else (1 if (i,j)==(0,1) else -1)
pairs=[]
for c,d in product(range(1,4),repeat=2):
    if c%2==0 and d%2==0:
        continue
    actual=wedge(h[c],h[d])
    potential=epsilon[d]-epsilon[c]
    require(actual==potential)
    pairs.append({'c':c,'d':d,'symbol_coefficient':actual})

# Unit scaling and strict congruence action on denominator modulo 4.
for c in range(1,4):
    for unit in (1,3):
        require(epsilon[(unit*c)%4]==epsilon[c])
for a,c,k in product(range(4),range(1,4),range(4)):
    transformed=(4*k*a+c)%4
    require(epsilon[transformed]==epsilon[c])

# Every closed vertex walk telescopes, including walks with repeated vertices.
cycles=0
for length in range(2,7):
    for vertices in product((1,2,3),repeat=length):
        edges=list(zip(vertices,vertices[1:]+vertices[:1]))
        if any(c==2 and d==2 for c,d in edges):
            continue
        require(sum(wedge(h[c],h[d]) for c,d in edges)==0)
        cycles+=1

raw=24**2
mixed=2*24
smoothed=raw+mixed
require(raw==576 and mixed==48 and smoothed==5**4-1==624)
require(Fraction(624,576)==Fraction(13,12))
# Standard tame residues in the unramified good-model base K.
q_exp=2
raw_exp=q_exp*raw%7
smoothed_exp=q_exp*smoothed%7
mixed_exp=q_exp*mixed%7
require((raw_exp,smoothed_exp,mixed_exp)==(4,2,5))
require((raw_exp+mixed_exp)%7==smoothed_exp)
# Restriction to the marked quadratic field multiplies exponents by e=2.
require((2*raw_exp)%7==1)

result={
 'gersten_sign':'boundary(pair) = swap(eta) - eta under the declared standard tame convention',
 'cyclic_four_admissible_pairs':pairs,
 'unit_and_strict_congruence_invariance':True,
 'closed_walks_checked':cycles,
 'normalization':{'raw':raw,'mixed':mixed,'smoothed':smoothed},
 'good_model_base_tame_exponents_mod_7':{'theta_pair':q_exp,'raw_pair':raw_exp,'smoothed_pair':smoothed_exp,'mixed_difference':mixed_exp},
 'marked_field_ramification_index':2,
 'scope':'Finite algebra only; no assertion of global arithmetic calibration or homology generation.'
}
print(json.dumps(result,indent=2,sort_keys=True))
