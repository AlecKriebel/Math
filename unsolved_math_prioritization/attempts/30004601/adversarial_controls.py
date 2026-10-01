#!/usr/bin/env python3
"""Additional post-freeze author controls, separate from the reviewed proof.
These rational flags corroborate, not establish, genericity.
"""
import sympy as s,json
x,y,z,w=s.symbols('x y z w');vs=[x,y,z,w]
L=[x,y,x-y,x-2*y,z,w,x+z+w];Q=s.prod(L);f=[s.diff(Q,v) for v in vs]
assert s.expand(sum(v*p for v,p in zip(vs,f))-7*Q)==0
assert s.Matrix([[a.coeff(v) for v in vs] for a in L]).rank()==4
assert all(s.Poly(p,*vs).total_degree()==6 for p in f)
def exps(n,d):
 if n==1:yield(d,);return
 for i in range(d+1):
  for tail in exps(n-1,d-i):yield(i,)+tail

def hf(P,V,d):
 e=s.Poly(P[0],*V).total_degree();C=list(exps(len(V),d));M=[]
 for p in P:
  for a in exps(len(V),d-e):
   q=s.Poly(p*s.prod(v**k for v,k in zip(V,a)),*V);M.append([q.coeff_monomial(c) for c in C])
 rank=s.Matrix(M).rank();return len(C)-rank

def good_forms(V,F):
 rows=[s.Matrix([[a.coeff(v) for v in V]]) for a in F]
 return all(a.rank()==1 for a in rows) and all(a.col_join(b).rank()==2 for i,a in enumerate(rows) for b in rows[i+1:])
results=[]
for A,B,C,D,E in [(1,2,3,2,3),(-2,1,4,3,5),(3,-2,1,5,7)]:
 wv=A*x+B*y+C*z;zv=D*x+E*y
 g3=[s.expand(p.subs(w,wv)) for p in f];g2=[s.expand(p.subs(z,zv)) for p in g3]
 forms3=[s.expand(a.subs(w,wv)) for a in L];forms2=[s.expand(a.subs(z,zv)) for a in forms3]
 assert good_forms([x,y,z],forms3) and good_forms([x,y],forms2)
 assert s.Matrix([[1,0,0],[0,0,1],[A,B,C]]).det()!=0
 h3=[hf(g3,[x,y,z],d) for d in [6,7]];h2=[hf(g2,[x,y],d) for d in [6,7,8]]
 assert h3==[24,24] and h2==[3,1,0]
 results.append({'flag':[A,B,C,D,E],'H3_6_7':h3,'H2_6_7_8':h2,'genericity_role':'control only; analytic proof supplies universal open-set ranks'})
# A coincident z,w restriction must not be treated as generic.
assert not good_forms([x,y,z],[a.subs(w,z) for a in L])
# Restriction of ambient Jacobian is strictly larger than Jacobian of restriction.
q3=s.expand(Q.subs(w,x+2*y+3*z));jq3=[s.diff(q3,v) for v in [x,y,z]]
grad3_h6=hf(jq3,[x,y,z],6);assert grad3_h6==25
jac2=[s.expand(p.subs(z,2*x+3*y)) for p in jq3]
grad3_h7=hf(jq3,[x,y,z],7);grad2_h7=hf(jac2,[x,y],7)
assert (grad3_h6,grad3_h7,grad2_h7)==(25,27,2)
assert grad3_h6-grad3_h7+grad2_h7==0
# Six-plane neighboring example has cutoff6, so failure of injectivity at6
# alone is not a strict-bound counterexample.
Q6=x*y*(x-y)*z*w*(x+z+w);f6=[s.diff(Q6,v) for v in vs]
p6=[s.expand(p.subs(w,x+2*y+3*z)) for p in f6];b6=[s.expand(p.subs(z,2*x+3*y)) for p in p6]
assert hf(b6,[x,y],5)>0 and hf(b6,[x,y],6)==0
out={'flags':results,'nongeneric_duplicate_factor_flag_rejected':True,'restricted_arrangement_Jacobian':{'H3_6':grad3_h6,'H3_7':grad3_h7,'H2_7':grad2_h7,'kernel_degree6to7':0,'ambient_section_H3_6':24},'six_plane_control':{'binary_cutoff':6,'note':'Noninjectivity at the cutoff is not a strict degree-bound violation'},'characteristic':'All calculations over Q; no extension to characteristic7 is asserted'}
print(json.dumps(out,indent=2))
