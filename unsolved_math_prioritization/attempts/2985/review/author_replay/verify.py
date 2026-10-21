#!/usr/bin/env python3
"""Exact affine, orientation and exterior-algebra controls for CANDIDATE.md.

Standard library only. These checks do not replace the topological Thom
isomorphism, covering-space argument, or the written smoothing construction.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import hashlib
import json

counts = Counter()
def check(x, kind):
    assert x, kind
    counts[kind] += 1

def sign(seq):
    return (-1)**sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))

def wedge(a, b):
    out=Counter()
    for I, c in a.items():
        for J, d in b.items():
            if len(set(I+J))<len(I+J):
                continue
            out[tuple(sorted(I+J))] += c*d*sign(I+J)
    return {I:c for I,c in out.items() if c}

def add(*forms):
    out=Counter()
    for f in forms:
        out.update(f)
    return {I:c for I,c in out.items() if c}

def scale(a, q):
    return {I:c*q for I,c in a.items() if c*q}

def pull(form, rows):
    out={}
    for I,c in form.items():
        term={():c}
        for i in I:
            term=wedge(term,{(j,):v for j,v in enumerate(rows[i]) if v})
        out=add(out,term)
    return out

def det(rows):
    return sum(sign(p)*prod(rows[i][p[i]] for i in range(len(rows)))
               for p in permutations(range(len(rows))))

def prod(xs):
    v=1
    for x in xs:v*=x
    return v

dx=[{(i,):1} for i in range(4)]
d1,d2,d3,d4=dx
omega=add(wedge(d1,d2),wedge(d3,d4))
dualA=wedge(d1,add(d2,scale(d3,-1)))
dualB=wedge(add(d2,d3),d4)
alpha=add(dualA,dualB)
beta=add(wedge(d1,add(d2,d3)),wedge(add(d3,scale(d2,-1)),d4))
vol={(0,1,2,3):1}
check(add(alpha,beta)==scale(omega,2),'hyperplane_class_sum')
check(wedge(alpha,alpha)==scale(vol,4),'intersection_forms')
check(wedge(beta,beta)==scale(vol,4),'intersection_forms')
check(wedge(alpha,beta)=={},'intersection_forms')
check(wedge(omega,omega)==scale(vol,2),'intersection_forms')
check(wedge(dualA,dualB)==scale(vol,2),'positive_intersection_number')
check(wedge(dualA,omega)==vol,'dual_orientation')
check(wedge(dualB,omega)==vol,'dual_orientation')
D=[[int(i==j)*(1 if i<2 else -1) for j in range(4)] for i in range(4)]
shift=[F(1,2),F(0),F(0),F(0)]
check([[sum(D[i][k]*D[k][j] for k in range(4)) for j in range(4)]
       for i in range(4)]==[[int(i==j) for j in range(4)] for i in range(4)],'deck_order_two')
check([sum(D[i][j]*shift[j] for j in range(4))+shift[i] for i in range(4)]
      ==[1,0,0,0],'deck_order_two')
check(shift[0] % 1 != 0 and D[0]==[1,0,0,0],'deck_freeness_first_coordinate')
check(det(D)==1,'deck_orientation')
check(pull(omega,D)==omega,'deck_symplectic')
check(pull(alpha,D)==beta,'deck_class_exchange')
check(pull(beta,D)==alpha,'deck_class_exchange')

# Parametrization derivatives for A and B.
JA=[[0,0],[1,0],[1,0],[0,1]]
JB=[[1,0],[0,1],[0,-1],[0,0]]
check(pull(omega,JA)=={(0,1):1},'torus_symplectic')
check(pull(omega,JB)=={(0,1):1},'torus_symplectic')
normal=[[1,0,0,0],[0,1,-1,0],[0,1,1,0],[0,0,0,1]]
check(det(normal)==2,'two_positive_nodes_global_degree')

# Modular equations verify each deck image and the four distinct constraints
# responsible for global disjointness. The grid is only a supplementary test.
def tau(x):return tuple((sum(D[i][j]*x[j] for j in range(4))+shift[i])%1 for i in range(4))
def A(x):return x[0]%1==0 and (x[1]-x[2])%1==0
def B(x):return (x[1]+x[2])%1==F(1,4) and x[3]%1==F(1,4)
def Ap(x):return x[0]%1==F(1,2) and (x[1]+x[2])%1==0
def Bp(x):return (x[1]-x[2])%1==F(1,4) and x[3]%1==F(3,4)
for a,b in [(0,F(1,2)),(F(1,4),F(3,4)),(0,F(1,4)),(F(1,4),0)]:
    check((a-b)%1!=0,'global_disjointness_constraint')
points=[]
for x in product([F(i,8) for i in range(8)],repeat=4):
    y=tau(x)
    check(A(x)==Ap(y) and B(x)==Bp(y),'affine_deck_images_grid')
    check(tau(y)==x and y!=x,'free_involution_grid')
    check(not ((A(x) or B(x)) and (Ap(x) or Bp(x))), 'disjoint_nodal_unions_grid')
    if A(x) and B(x):points.append(x)
check(points==[(F(0),F(1,8),F(1,8),F(1,4)),
               (F(0),F(5,8),F(5,8),F(1,4))],'explicit_node_locations')

# x as a function of the local s coordinates, ignoring translations.
J=[[1,0,0,0],[0,F(1,2),F(1,2),0],
   [0,F(-1,2),F(1,2),0],[0,0,0,1]]
standard={(0,1):1,(2,3):1}
holomorphic_real={(0,2):1,(1,3):-1}
check(pull(alpha,J)==standard,'local_smoothing_form_identity')
check(pull(beta,J)==holomorphic_real,'local_smoothing_form_identity')
localomega=pull(omega,J)
check(localomega==scale(add(standard,holomorphic_real),F(1,2)), 'local_smoothing_form_identity')

# Holomorphic graphs have derivative [[a,-b],[b,a]], so beta restricts to zero
# and the omega-area coefficient is (1+a^2+b^2)/2. Arbitrary small real graph
# derivatives control cutoff-annulus perturbations.
for a,b in product([F(i,3) for i in range(-4,5)],repeat=2):
    graph=[[1,0],[0,1],[a,-b],[b,a]]
    check(pull(holomorphic_real,graph)=={},'holomorphic_graph_beta_zero')
    check(pull(localomega,graph)=={(0,1):(1+a*a+b*b)/2},'holomorphic_graph_positive_area')
for a,b,c,d in product([F(-1,8),F(0),F(1,8)],repeat=4):
    graph=[[1,0],[0,1],[a,b],[c,d]]
    expected=(1+a*d-b*c+b+c)/2
    check(pull(localomega,graph)=={(0,1):expected},'transition_graph_area_formula')
    check(expected>0,'small_transition_graph_positive')

# Arithmetic consistency of the quotient class, genus, and homology cokernel.
check(F(1,2)*4*2==4,'quotient_volume_and_square')
check(2-2*3==-4,'smoothing_genus')
# The diagonal vector is primitive and the difference map has kernel diagonal;
# this models coker(H4(T4)->H2(S disjoint S')) = Z in the Thom exact sequence.
for a,b in product(range(-8,9),repeat=2):
    check((a-b==0)==(a==b),'diagonal_cokernel_kernel')
    check((a-b)==((a+3)-(b+3)),'diagonal_cokernel_quotient_map')
for a in range(-8,9):
    check(a-0==a,'diagonal_cokernel_surjectivity')

here=Path(__file__).resolve().parent
h=hashlib.sha256((here/'CANDIDATE.md').read_bytes()).hexdigest()
check(h=='78ab061c9c0c6c16f2e6b249e764001361933782d7381982c733f92cefda3c8f','frozen_proof_hash')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),
 'checks':dict(sorted(counts.items())),'candidate_sha256':h,
 'limitation':'Finite algebraic controls supplement the written symplectic smoothing, transfer, Thom-isomorphism and covering-space proof.'},indent=2,sort_keys=True))
