from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json,datetime
R=Path(__file__).resolve().parent
count=0
def check(b):
 global count
 count+=1
 if not b:raise ValueError('independent algebraic check failed')
def basis(n):return [[Q(i==j) for i in range(n)] for j in range(n)]
def add(x,y):return [a+b for a,b in zip(x,y)]
def sub(x,y):return [a-b for a,b in zip(x,y)]
def sl(x,y):
 h,e,f=x;H,E,F=y;return [e*F-f*E,2*(h*E-e*H),2*(f*H-h*F)]
def action(a,v):h,e,f=a;x,y=v;return [h*x+e*y,f*x-h*y]
def src(x,y):return sl(x[:3],y[:3])+sub(action(x[:3],y[3:]),action(y[:3],x[3:]))
def tgt(x,y):return sl(x[:3],y[:3])+[0,0]
def mul(x,y):return [0,0,0]+action(x[:3],y[3:])
def rank(cols):
 a=[list(x) for x in zip(*cols)];r=0
 for j in range(len(a[0])):
  p=next((i for i in range(r,len(a)) if a[i][j]),None)
  if p is None:continue
  a[r],a[p]=a[p],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
  for i in range(len(a)):
   if i!=r:v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
E=basis(5)
for x,y in product(E,repeat=2):
 check(sub(mul(x,y),mul(y,x))==sub(src(x,y),tgt(x,y)))
 for z in E:
  check(mul(src(x,y),z)==sub(mul(x,mul(y,z)),mul(y,mul(x,z))))
  check(mul(x,tgt(y,z))==add(tgt(mul(x,y),z),tgt(y,mul(x,z))))
  check(add(src(x,src(y,z)),add(src(y,src(z,x)),src(z,src(x,y))))==[0]*5)
check(rank([src(x,y) for x,y in product(E,repeat=2)])==5)
traces=[sum(src(x,E[j])[j] for j in range(5)) for x in E];check(traces==[0]*5)
for x,y in product(E[3:],repeat=2):check(src(x,y)==[0]*5)
# Manuscript's explicit nonunimodular source, H,E,Z basis.
def solv(x,y):return [0,2*(x[0]*y[1]-x[1]*y[0]),0]
def j1(x):return [x[0],x[1],0]
def j2(x):return [0,0,x[2]]
for x,y in product(basis(3),repeat=2):
 check(j1(solv(x,y))==sl(j1(x),j1(y)));check(j2(solv(x,y))==sl(j2(x),j2(y)))
check(rank([sub(j1(x),j2(x)) for x in basis(3)])==3)
traceH=sum(solv(basis(3)[0],basis(3)[j])[j] for j in range(3));check(traceH==2)
# Coefficientwise determinant identity for arbitrary 2x2 p=(a,b;c,d).
zero=(0,0,0,0)
def poly(i=None):return {zero:1} if i is None else {tuple(int(k==i) for k in range(4)):1}
def pa(x,y):
 z=x.copy()
 for k,v in y.items():z[k]=z.get(k,0)+v
 return {k:v for k,v in z.items() if v}
def pm(x,y):
 z={}
 for k,v in x.items():
  for l,w in y.items():
   t=tuple(a+b for a,b in zip(k,l));z[t]=z.get(t,0)+v*w
 return {k:v for k,v in z.items() if v}
def scale(c,x):return {k:c*v for k,v in x.items() if c*v}
a,b,c,d=map(poly,range(4));ad=pm(a,d);bc=pm(b,c);d2=pm(d,d)
# first two columns h,e components: (ad+bc,2bd), (cd,d²), last column -F
actual=scale(-1,pa(pm(pa(ad,bc),d2),scale(-2,pm(pm(c,d),pm(b,d)))))
expected=scale(-1,pm(d2,pa(ad,scale(-1,bc))));check(actual==expected)
# Zero and opposite products on semisimple target check sign/boundary exactly.
for neg in (False,True):
 for x,y,z in product(basis(3),repeat=3):
  source=lambda u,v:scale_vec(-1 if neg else 1,sl(u,v))
  prod=lambda u,v:scale_vec(-1,sl(u,v)) if neg else [Q(0)]*3
  # definitions below are ordinary vector arithmetic; no subject code is used.
  def scale_vec(k,v):return [k*a for a in v]
  check(sub(prod(x,y),prod(y,x))==sub(source(x,y),sl(x,y)))
  check(prod(source(x,y),z)==sub(prod(x,prod(y,z)),prod(y,prod(x,z))))
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','exact_conditions':count,'independent_no_subject_code_imported':True,'perfect_nonsemisimple_reductive_target_boundary':{'dimension':5,'derived_rank':5,'traces':list(map(str,traces)),'abelian_ideal_dimension':2},'nonunimodular_boundary':{'homomorphisms':True,'difference_rank':3,'trace_ad_H':str(traceH),'coefficientwise_det':'-d^2(ad-bc)','SL2_restriction':'-d^2; nonzero at identity, vanishes for d=0'},'scope':'Exact supplementary examples and polynomial identities; not a finite proof of the global theorem.'}
(R/'INDEPENDENT_MATH_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
