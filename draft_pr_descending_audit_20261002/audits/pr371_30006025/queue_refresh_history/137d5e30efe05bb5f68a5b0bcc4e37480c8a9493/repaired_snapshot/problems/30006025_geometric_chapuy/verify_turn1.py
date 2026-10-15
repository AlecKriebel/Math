#!/usr/bin/env python3
"""Exact framed-holonomy controls and finite cubic-map examples. Requires SymPy."""
import sympy as S,json
from itertools import product
from collections import Counter
from fractions import Fraction as Q
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
z,q=S.symbols('z q',nonzero=True);R=S.Matrix([[S.sqrt(3)/2,S.Rational(1,2)],[-S.Rational(1,2),S.sqrt(3)/2]]);A=S.diag(q,1/q)*R
ck(S.simplify(A.det())==1,'one_step_determinant')
ck(S.simplify(S.trace(A)-S.sqrt(3)*(q+1/q)/2)==0,'one_step_trace')
polys=[S.Integer(2),z]
for n in range(2,115):polys.append(S.expand(z*polys[-1]-polys[-2]))
for n in range(1,115):
 ck(S.Poly(polys[n],z).degree()==n and S.Poly(polys[n],z).LC()==1,'trace_polynomial_monic_degree')
 ck(S.expand(polys[n]-2*S.chebyshevt(n,z/2))==0,'trace_polynomial_chebyshev')
for n in range(1,9):ck(S.simplify(S.trace(A**n)-polys[n].subs(z,S.trace(A)))==0,'matrix_trace_power_identity')
# Field arithmetic a+b*sqrt(3), all rational.
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[0],-x[1])
def mul(x,y):return (x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
zero=(Q(0),Q(0));one=(Q(1),Q(0));I=((one,zero),(zero,one))
def matmul(A,B):return tuple(tuple(add(mul(A[i][0],B[0][j]),mul(A[i][1],B[1][j])) for j in range(2)) for i in range(2))
def step(t):return (((Q(0),t/2),(t/2,Q(0))),((-1/(2*t),Q(0)),(Q(0),1/(2*t))))
def det(A):return add(mul(A[0][0],A[1][1]),neg(mul(A[0][1],A[1][0])))
def cyc(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i in seen:continue
  j=i;c=[]
  while j not in seen:seen.add(j);c.append(j);j=p[j]
  out.append(c)
 return out
adj={i:list(range(3,6)) for i in range(3)};adj.update({i:list(range(3)) for i in range(3,6)})
alpha={3*v+j:3*w+adj[w].index(v) for v in range(6) for j,w in enumerate(adj[v])}
ck(all(alpha[alpha[i]]==i and alpha[i]!=i for i in alpha),'edge_pairing_involution')
counts=Counter();examples=[]
for signs in product((1,-1),repeat=6):
 sigma={3*v+j:3*v+(j+signs[v])%3 for v in range(6) for j in range(3)};phi={i:sigma[alpha[i]] for i in alpha};faces=cyc(phi)
 ck(all(len(v)==3 for v in cyc(sigma)),'cubic_rotation_vertices')
 F=len(faces);g=(2-6+9-F)//2;ck(6-9+F==2-2*g,'map_euler_genus');counts[F]+=1
 if F!=1:continue
 word=faces[0];edgekeys=sorted({tuple(sorted((i,alpha[i]))) for i in alpha});labels={e:j for j,e in enumerate(edgekeys)};w=[labels[tuple(sorted((i,alpha[i])))] for i in word]
 ck(len(w)==18 and all(w.count(j)==2 for j in range(9)),'one_face_word_lengths')
 H=I
 for j in w:H=matmul(H,step(Q(3,2)+Q(j,20)))
 ck(det(H)==one,'exact_example_holonomy_determinant')
 tr=add(H[0][0],H[1][1]);Fval=add(mul(tr,tr),(Q(-4),Q(0)))
 ck(Fval!=zero,'exact_example_nonclosure')
 examples.append({'rotation_signs':signs,'edge_word':w})
ck(counts[1]==24 and counts[3]==40,'complete_K33_rotation_counts')
for g in range(2,11):
 E=6*g-3;V=4*g-2;N=2*E;P=12*g
 ck(3*V==2*E and V-E+1==2-2*g,'trivalent_one_face_counts')
 ck(Q(P,2*E)*E==Q(P,2),'source_perimeter_factor_two')
 ck(S.Poly(polys[N]**2-4,z).degree()==2*N,'barycenter_constraint_nonzero_polynomial')
print(json.dumps({'status':'PASS','arithmetic':'exact rational, Q(sqrt(3)) and symbolic polynomial controls; requires SymPy','assertions':sum(C.values()),'by_scope':dict(C),'labelled_K33_rotation_choices':64,'one_face_genus_two_choices':24,'three_face_genus_one_choices':40,'one_face_examples':examples,'trace_polynomial_max_degree':114,'scope':'Finite controls verify algebra/combinatorics. Universal nonclosure at algebraic-perimeter barycenters uses credited Hermite-Lindemann, and zero probability uses the proved nontrivial analytic constraint. No full geometric Chapuy solution is claimed.'},indent=2,sort_keys=True))
