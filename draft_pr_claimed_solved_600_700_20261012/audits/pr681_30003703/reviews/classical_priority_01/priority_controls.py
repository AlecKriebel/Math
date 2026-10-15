"""Exact source-specialization and anti-conflation controls; no author imports/writes."""
import json
from collections import defaultdict
from sympy import Matrix, symbols, expand, eye

def add(a,b,scale=1):
 d=defaultdict(int,a)
 for w,c in b.items():d[w]+=scale*c
 return {w:c for w,c in d.items() if c}
def mul(a,b):
 d=defaultdict(int)
 for u,c in a.items():
  for v,e in b.items():d[u+v]+=c*e
 return {w:c for w,c in d.items() if c}
def lie(a,b):return add(mul(a,b),mul(b,a),-1)
def lp(x,y,z):return lie(lie(lie(x,y),lie(x,z)),x)
def fil(z,w,x,y):return add(lie(z,lie(lie(w,x),lie(w,y))),lie(w,lie(lie(z,w),lie(x,y))),-1)
def matbr(a,b):return a*b-b*a
def mp(x,y,z):return matbr(matbr(matbr(x,y),matbr(x,z)),x)
def zero(m):return all(expand(v)==0 for v in m)
def gm(prefix):return Matrix(2,2,symbols(prefix+'0:4'))
def groupbr(a,b):return a*b*a.inv()*b.inv()

def run():
 checks={}
 X,Y,Z,W=({c:1} for c in 'XYZW')
 p=lp(X,Y,Z);q=lp(X,Y,lie(X,Y));f=fil(W,W,X,Y)
 checks['Burde_Filippov_z_equals_w_exactly_negative_P']=f=={w:-c for w,c in lp(W,X,Y).items()}
 checks['P_nonzero_free_and_homogeneous5']=bool(p) and all(len(w)==5 for w in p) and p.get('XXYXZ')==-1
 checks['Q_nonzero_free_and_homogeneous6']=bool(q) and all(len(w)==6 for w in q) and q.get('XXXYXY')==1
 checks['unrestricted_Filippov_polynomial_not_free_identity']=bool(fil(Z,W,X,Y))
 a,b,c,d=map(gm,['a','b','c','d'])
 u=matbr(a,b);v=matbr(a,c);t=a.trace()
 checks['untraced_CH_XU_plus_UX_equals_traceX_U']=zero(a*u+u*a-t*u)
 checks['untraced_CH_XV_plus_VX_equals_traceX_V']=zero(a*v+v*a-t*v)
 checks['P_vanishes_for_12_generic_M2_entries']=zero(mp(a,b,c))
 checks['Q_vanishes_for_8_generic_M2_entries']=zero(mp(a,b,matbr(a,b)))
 checks['Filippov_four_variable_identity_M2']=zero(matbr(c,matbr(matbr(d,a),matbr(d,b)))-matbr(d,matbr(matbr(c,d),matbr(a,b))))
 H=Matrix([[1,0],[0,-1]]);E=Matrix([[0,1],[0,0]]);F=Matrix([[0,0],[1,0]])
 inner=matbr(matbr(H,E),matbr(H,F))
 checks['removing_final_bracket_does_not_vanish']=not zero(inner)
 checks['replacing_repeated_final_X_by_E_does_not_vanish']=not zero(matbr(inner,E))
 A=Matrix([[1,1],[0,1]]);B=Matrix([[1,0],[1,1]]);C=Matrix([[2,1],[1,1]])
 gw=groupbr(groupbr(groupbr(A,B),groupbr(A,C)),A)
 checks['Lie_identity_is_not_an_exact_SL2_group_law']=gw!=eye(2) and gw.det()==1
 if not all(checks.values()):raise RuntimeError({k:v for k,v in checks.items() if not v})
 return {'status':'PASS','count':len(checks),'checks':checks,'free_P_terms':len(p),'free_Q_terms':len(q),'nontrivial_SL2_group_word':[[str(v) for v in row] for row in gw.tolist()],'boundary':'Exact source map and polynomial controls; not novelty evidence.'}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
