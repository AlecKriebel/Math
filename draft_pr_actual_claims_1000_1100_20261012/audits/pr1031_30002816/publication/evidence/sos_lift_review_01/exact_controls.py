#!/usr/bin/env python3
"""Exact controlled adversarial checks; no SDP solver or floating arithmetic."""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import datetime, hashlib, json
BASE=Path(__file__).resolve().parent

def det(a):
 n=len(a); total=F(0)
 for s in permutations(range(n)):
  inv=sum(s[i]>s[j] for i in range(n) for j in range(i+1,n))
  term=F(-1 if inv%2 else 1)
  for i in range(n): term*=a[i][s[i]]
  total+=term
 return total

def principal(a):
 return {','.join(map(str,inds)):det([[a[i][j] for j in inds] for i in inds]) for k in range(1,len(a)+1) for inds in combinations(range(len(a)),k)}

def rank(a):
 a=[[F(x) for x in row] for row in a]; lead=0
 for j in range(len(a[0])):
  ids=[i for i in range(lead,len(a)) if a[i][j]]
  if not ids: continue
  i=ids[0];a[lead],a[i]=a[i],a[lead]
  d=a[lead][j];a[lead]=[x/d for x in a[lead]]
  for i in range(len(a)):
   if i!=lead:
    d=a[i][j];a[i]=[x-d*y for x,y in zip(a[i],a[lead])]
  lead+=1
  if lead==len(a):break
 return lead

def add(*polys):
 out={}
 for p in polys:
  for m,c in p.items():out[m]=out.get(m,F(0))+c
 return {m:c for m,c in out.items() if c}

def scale(p,c):return {m:v*c for m,v in p.items() if v*c}
def mul(p,q):
 out={}
 for m,c in p.items():
  for n,d in q.items():
   o=tuple(x+y for x,y in zip(m,n));out[o]=out.get(o,F(0))+c*d
 return {m:c for m,c in out.items() if c}

def poly_det(a):
 n=len(a);out={};nvars=len(next(iter(a[0][0])))
 for s in permutations(range(n)):
  inv=sum(s[i]>s[j] for i in range(n) for j in range(i+1,n))
  term={(0,)*nvars:F(-1 if inv%2 else 1)}
  for i in range(n):term=mul(term,a[i][s[i]])
  out=add(out,term)
 return out

checks=[]
def check(name,condition,evidence):
 if not condition:raise AssertionError(name)
 checks.append({'name':name,'passed':True,'evidence':evidence})

# Circle: a rational interior moment satisfies PSD exactly.
x=(F(1,2),F(1,3));M=[[F(1),*x],[x[0],F(1,2),F(0)],[x[1],F(0),F(1,2)]]
mins=principal(M)
check('rational_circle_moment_psd_trace',all(v>=0 for v in mins.values()) and sum(M[i][i] for i in range(3))==2,{'principal_minors':mins,'projection':x,'trace':2,'sphere_moment':1-M[1][1]-M[2][2]})

# Every circle support has an affine SOS; verify rational unit direction exactly.
c=(F(3,5),F(4,5)); P=[[F(i==j)-c[i]*c[j] for j in range(2)] for i in range(2)]
pts=[c,tuple(-v for v in c),(F(1),F(0)),(F(0),F(1)),(F(-1),F(0))]
vals=[]
for p in pts:
 phi=sum(ci*pi for ci,pi in zip(c,p));sos=F(1,2)*sum((pi-ci)**2 for ci,pi in zip(c,p))
 psi=[sum(P[i][j]*p[j] for j in range(2)) for i in range(2)]
 vals.append({'p':p,'phi':phi,'affine_sos':sos,'completion':phi**2+sum(v*v for v in psi)})
 assert sos==1-phi and phi**2+sum(v*v for v in psi)==1
assert sum(v*v for v in c)==1
assert all(sum(P[i][k]*P[k][j] for k in range(2))==P[i][j] for i in range(2) for j in range(2))
assert all(sum(P[i][j]*c[j] for j in range(2))==0 for i in range(2))
check('sphere_affine_sos_and_completion',True,{'samples':vals,'rational_orthogonal_projector':P,'P_squared_equals_P':True,'P_c_zero':True,'c_norm_squared':1})

# Full vanishing constraints cannot be replaced by only the sphere constraint.
axisM=[[F(1),F(0),F(1)],[F(0),F(0),F(0)],[F(1),F(0),F(1)]]
check('omitted_real_ideal_constraint_detected',all(v>=0 for v in principal(axisM).values()) and axisM[1][1]+axisM[2][2]==1 and axisM[0][2]==1,{'X':['(1,0)','(-1,0)'],'sphere_only_point':'(0,1)','rank_one_psd':True,'missing_constraint':'p2=0','support_l':'p2','support_delta':0,'invalid_support_value':-1})

# Symmetric six-point example has only the sphere relation in degree <=2.
hexpts=[(F(1),F(0)),(F(3,5),F(4,5)),(F(3,5),F(-4,5))]
hexpts+= [tuple(-v for v in p) for p in hexpts.copy()]
E=[[F(1),p[0],p[1],p[0]**2,p[0]*p[1],p[1]**2] for p in hexpts]
rr=rank(E)
check('six_point_full_J2_dimension',rr==5,{'evaluation_rank':rr,'polynomial_dimension':6,'J2_dimension':1,'J2_basis':'1-p1^2-p2^2'})
# For delta=4/5, t=p2, this degree-two-SOS evaluates delta-t on all X.
a=F(4,5);h0={(0,):F(1),(2,):-F(25,16)};hm={(2,):F(25,32),(1,):-F(5,8)}
SOS=add(scale(mul(h0,h0),F(4,5)),scale(mul(hm,hm),F(8,5)))
remainder=add({(0,):a,(1,):-F(1)},scale(SOS,-1))
expected={(1,):-F(1),(2,):F(15,8),(3,):F(25,16),(4,):-F(375,128)}
assert remainder==expected
for p in hexpts:
 t=p[1];ev=lambda poly:sum(v*t**m[0] for m,v in poly.items())
 assert ev(remainder)==0
check('higher_degree_SOS_does_not_force_first_moment_exactness',True,{'X':hexpts,'l':'p2','delta':a,'T_point':'(0,1)','delta_minus_l_at_T_point':a-1,'weighted_square_polynomials':[h0,hm],'weights':[F(4,5),F(8,5)],'difference_degree':4,'difference_polynomial':remainder,'vanishes_on_X':True})

# Nonclosed projected spectrahedron: shows why the trace bound was checked.
seq=[]
for k in (1,2,10,100):
 A=[[F(1,k),F(1)],[F(1),F(k)]]
 assert all(v>=0 for v in principal(A).values())
 seq.append({'x':F(1,k),'y':k,'determinant':det(A)})
check('nonclosed_projection_without_trace_bound',True,{'spectrahedron':'[[x,1],[1,y]] >= 0','projection':'x>0','excluded_limit':0,'sequence':seq})

# Published Choi polynomial: independent symbolic nonnegativity certificate.
# Phase cancellation makes 2x2 minors and determinant functions of |xi|^2.
a={(1,0,0):F(1)};b={(0,1,0):F(1)};g={(0,0,1):F(1)}
d1=add(a,scale(g,2));d2=add(b,scale(a,2));d3=add(g,scale(b,2))
det_expected={(2,1,0):F(4),(0,2,1):F(4),(1,0,2):F(4),(1,1,1):F(4)}
det_actual=add(mul(mul(d1,d2),d3),scale(mul(d1,mul(b,g)),-1),scale(mul(d2,mul(a,g)),-1),scale(mul(d3,mul(a,b)),-1),scale(mul(mul(a,b),g),-2))
minors=[add(mul(d1,d2),scale(mul(a,b),-1)),add(mul(d1,d3),scale(mul(a,g),-1)),add(mul(d2,d3),scale(mul(b,g),-1))]
assert det_actual==det_expected and all(v>=0 for p in minors for v in p.values())
check('Choi_complex_nonnegative_principal_minors',True,{'diagonal_polynomials':[d1,d2,d3],'two_by_two_minors':minors,'determinant':det_actual,'variables':'a=|x1|^2, b=|x2|^2, g=|x3|^2'})
G=[[F(1 if i==j else -1) for j in range(3)] for i in range(3)]
check('Choi_real_nonSOS_forced_Gram_block',det(G)==-4,{'forced_principal_Gram_block':G,'determinant':det(G),'negative_vector':[1,1,1],'quadratic_value':sum(sum(row) for row in G),'excluded_bilinear_monomials':['x1*y3','x2*y1','x3*y2']})

def serialize(v):
 if isinstance(v,F):return str(v)
 if isinstance(v,dict):return {str(k):serialize(w) for k,w in v.items()}
 if isinstance(v,(list,tuple)):return [serialize(w) for w in v]
 return v
out={'schema':'independent-controlled-exact-checks-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arithmetic':'fractions.Fraction; all exact','checks':serialize(checks),'passed':all(c['passed'] for c in checks),'boundary':'Controlled examples and a Choi constituent check; not a numerical certificate for C_4,12 and not a reproving of Fawzi Theorem 2.'}
(BASE/'EXACT_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':out['passed'],'checks':len(checks),'output':'EXACT_CONTROLS.json'}))
