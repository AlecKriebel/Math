"""Fresh exact real/imaginary polynomial-ring oracle, no package imports."""
from fractions import Fraction as F
from math import factorial,comb
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
Z=(F(0),F(0));ONE=(F(1),F(0))
def pair(x,y=0):return (F(x),F(y))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def sub(a,b):return add(a,neg(b))
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,k):return (a[0]*k,a[1]*k)
def norm(a):return a[0]**2+a[1]**2
def div(a,b):return scale(mul(a,(b[0],-b[1])),1/norm(b))
def power(a,n):
 out=ONE
 for _ in range(n):out=mul(out,a)
 return out
def total(v):
 out=Z
 for a in v:out=add(out,a)
 return out
def poly_product(a,b):
 out=[Z]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]=add(out[i+j],mul(x,y))
 return out
def shift(c,alpha):
 out=[Z]*len(c)
 for k,v in enumerate(c):
  for j in range(k+1):out[j]=add(out[j],scale(mul(v,power(neg(alpha),k-j)),comb(k,j)))
 return out
def at(c,n,alpha):return total(scale(mul(v,power(alpha,k-n)),factorial(k)//factorial(k-n)) for k,v in enumerate(c) if k>=n)
def construct(m,alpha,q,eta,variant='correct'):
 a=[];b=[];old=[];hits=0
 # Design input via independent polynomial oracle so each boundary branch is forced.
 desired=[Z,pair(eta/4,eta/4),pair(eta),pair(-eta),pair(0,eta),pair(2*eta),pair(10**12,-10**10)]
 for k in range(14):
  n=k+m;A=scale(q[m],factorial(n)//factorial(k))
  cross=at(poly_product(q,[scale(v,F(1,factorial(i))) for i,v in enumerate(b)]),n,Z)
  a.append(div(sub(desired[k%len(desired)],cross),A))
  usedA=q[m] if variant=='drop_factorial' else A
  usedcross=Z if variant=='drop_cross' else cross
  S=add(mul(usedA,a[k]),usedcross)
  c=Z if norm(S)>=eta*eta or variant=='omit_correction' else div(sub(pair(eta),S),usedA)
  b.append(add(a[k],c))
  actual=at(poly_product(q,[scale(v,F(1,factorial(i))) for i,v in enumerate(b)]),n,Z)
  if norm(actual)<eta*eta:raise ValueError('barrier failed')
  if norm(c)*norm(A)>4*eta*eta:raise ValueError('correction bound failed')
  centered=poly_product(q,[scale(v,F(1,factorial(i))) for i,v in enumerate(b)])
  # Compute the product again after independently expanding both factors globally.
  globalproduct=poly_product(shift(q,alpha),shift([scale(v,F(1,factorial(i))) for i,v in enumerate(b)],alpha))
  for j in range(n+1):
   if at(globalproduct,j,alpha)!=at(centered,j,Z):raise ValueError('global-coordinate oracle disagrees')
   if j<m and at(globalproduct,j,alpha)!=Z:raise ValueError('low multiplicity order nonzero')
  for j,v in enumerate(old):
   if at(globalproduct,j+m,alpha)!=v:raise ValueError('future correction changed past')
  old.append(actual);hits+=1
 return hits
cases=0;steps=0
for m in [1,2,3,5]:
 for alpha in [Z,pair(F(2,3),F(-3,7))]:
  for leading in [ONE,pair(F(1,10**24),F(-1,10**22)),pair(10**24,-10**25)]:
   for degree in [m,m+3]:
    q=[Z]*(degree+1);q[m]=leading
    for j in range(m+1,degree+1):q[j]=pair((-1)**j*10**8,F(1,j+1))
    for eta in [F(1),F(1,10**18)]:steps+=construct(m,alpha,q,eta);cases+=1
mutants=[]
q=[Z,Z,pair(F(1,3),F(-2,5)),pair(3,-2),pair(-7,5)]
for v in ['omit_correction','drop_factorial','drop_cross']:
 try:construct(2,pair(F(2,3),F(1,2)),q,F(1,100),v)
 except ValueError as e:mutants.append({'actual_altered_algorithm':v,'rejected':str(e)})
 else:raise RuntimeError('mutant accepted '+v)
# Exact radial boundary tests at n=t^2-1, so ell_n=1/t is rational.
clipcases=0
for t in [1,2,10,10**12]:
 ell=F(1,t)
 for phase in [ONE,pair(-1),pair(0,1),pair(F(3,5),F(4,5))]:
  for radius in [F(0),ell/100,ell,2*ell,F(10**100)]:
   beta=scale(phase,radius);gamma=beta if radius>=ell else scale(phase,ell)
   if norm(gamma)<ell*ell or norm(sub(gamma,beta))>ell*ell:raise RuntimeError('radial clipping failed')
   clipcases+=1
report={'status':'PASS','fixed_polynomial_cases':cases,'recursion_steps':steps,'radial_zero_small_boundary_huge_complex_cases':clipcases,'executed_algorithm_mutations_rejected':mutants,'inputs_imported_from_candidate':False,'arithmetic':'Fraction pairs; ordinary polynomial multiplication, shift then direct global differentiation','limits':'Finite coefficient identities and fault sensitivity only. No finite sample establishes hypercyclicity, density, infinite escape, probability one, or priority.'}
(HERE/'independent_algebra.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
