from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as sp
R=Path('/mnt/data/k3p_identifiability_final')
# Fourier inversion / CT convention.
c,g,t=sp.symbols('c g t', positive=True)
p0=(1+c+g+t)/4;pC=(1+c-g-t)/4;pG=(1-c+g-t)/4;pT=(1-c-g+t)/4
assert sp.simplify(p0+pC+pG+pT-1)==0
assert sp.simplify(p0+pC-pG-pT-c)==0
assert sp.simplify(p0-pC+pG-pT-g)==0
assert sp.simplify(p0-pC-pG+pT-t)==0
A,B,C=sp.symbols('A B C', positive=True) # rates for C,G,T substitutions
ce=sp.exp(-2*(B+C));ge=sp.exp(-2*(A+C));te=sp.exp(-2*(A+B))
assert sp.simplify(sp.log(ce/(ge*te))/4-A)==0
assert sp.simplify(sp.log(ge/(ce*te))/4-B)==0
assert sp.simplify(sp.log(te/(ce*ge))/4-C)==0
# Serial subdivision residual numerators.
r=sp.symbols('r', positive=True)
residual_margins=[sp.factor(1+c/r-g/r-t/r),sp.factor(1-c/r+g/r-t/r),sp.factor(1-c/r-g/r+t/r)]
assert residual_margins==[(c-g+r-t)/r,(-c+g+r-t)/r,(-c-g+r+t)/r]
# Anchor exponent matrices, one sector and all three sectors.
anchors={};
for d in range(3,13):
 pairs=[(0,1),(0,2),(1,2)]+[(0,j) for j in range(3,d)]
 M=sp.zeros(d,d)
 for i,(u,v) in enumerate(pairs):M[i,u]=1;M[i,v]=1
 det=int(M.det());rank=M.rank();assert rank==d and abs(det)==2
 B3=sp.diag(M,M,M);assert B3.rank()==3*d and abs(int(B3.det()))==8
 anchors[d]={'pairs':[[u+1,v+1] for u,v in pairs],'one_sector_determinant':det,'one_sector_rank':rank,'three_sector_determinant':int(B3.det()),'three_sector_rank':3*d}
# Product descriptor submersion: each sector product has nonzero partials.
x=sp.symbols('x0:6', positive=True)
prod=sp.prod(x);partials=[sp.diff(prod,z) for z in x]
assert all(sp.simplify(v-sp.prod(x[:i]+x[i+1:]))==0 for i,v in enumerate(partials))
# Concrete exact sanity points for D3+ and CT, subdivision and gluing.
examples=[]
for triple in [(F(1,2),F(2,5),F(1,3)),(F(2,7),F(3,10),F(1,4))]:
 cc,gg,tt=triple
 assert min(triple)>0 and max(triple)<1
 assert 1+cc-gg-tt>0 and 1-cc+gg-tt>0 and 1-cc-gg+tt>0
 R0=max(cc,gg,tt,gg+tt-cc,cc+tt-gg,cc+gg-tt);rr=(1+R0)/2
 rem=(cc/rr,gg/rr,tt/rr)
 for z in ((rr,rr,rr),rem):
  Cc,Gg,Tt=z;assert 0<Cc<1 and 0<Gg<1 and 0<Tt<1;assert 1+Cc-Gg-Tt>0 and 1-Cc+Gg-Tt>0 and 1-Cc-Gg+Tt>0
 assert tuple(rr*z for z in rem)==triple
 examples.append({'triple':list(map(str,triple)),'R':str(R0),'r':str(rr),'residual':list(map(str,rem))})
cert={'schema':'k3p-model-domain-bridge-v1','inverse_fourier':[str(p0),str(pC),str(pG),str(pT)],'ct_spectrum':[str(ce),str(ge),str(te)],'ct_rate_inverse':['log(c/(g*t))/4','log(g/(c*t))/4','log(t/(c*g))/4'],'subdivision_residual_margins':[str(x) for x in residual_margins],'anchors':anchors,'examples':examples,'conclusions':{'principal_domain':'exact positive-eigenvalue component of strict stochastic K3P cone','ct_domain':'c>g*t, g>c*t, t>c*g','incidence_rank':'3d for an unmarked degree-d component','no_sector_permutation':'state labels C,G,T are fixed observable coordinate labels'}}
(R/'software/certificates/k3p_model_domain_bridge.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
print('K3P_MODEL_DOMAIN_AND_BRIDGE_EXACT_PASS')
