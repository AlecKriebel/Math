from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
import json,cmath,itertools
R=Path(__file__).resolve().parent
# Real polynomials in t, represented by exact coefficient tuples.
def trim(p):
 p=list(p)
 while len(p)>1 and p[-1]==0:p.pop()
 return tuple(p)
def plus(p,q):return trim(tuple((p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q)))))
def scale(a,p):return trim(tuple(a*x for x in p))
def times(p,q):
 r=[F(0)]*(len(p)+len(q)-1)
 for i,x in enumerate(p):
  for j,y in enumerate(q):r[i+j]+=x*y
 return trim(r)
def cp(z,w):return plus(z[0],w[0]),plus(z[1],w[1])
def cm(z,w):return plus(times(z[0],w[0]),scale(-1,times(z[1],w[1]))),plus(times(z[0],w[1]),times(z[1],w[0]))
def cs(a,z):return scale(a,z[0]),scale(a,z[1])
zero=(F(0),); one=(F(1),); t=(F(0),F(1)); t2=times(t,t); t3=times(t2,t); t4=times(t2,t2)
i=(zero,one); lam=(zero,scale(-1,t)); other=(scale(-1,t2),t)
assert cp(lam,other)==(scale(-1,t2),zero)
assert cm(lam,other)==(t2,t3)
conj_den=(t2,scale(2,t))
n=[scale(-1,t),scale(F(-1,2),t2),scale(F(-1,2),t),one]
N=[scale(F(1,2),t3),scale(-1,t2),*n]
monic=[lam,cm(i,lam),(one,zero),i]
full=[cm(lam,lam),cm(i,cm(lam,lam)),*monic]
for dirs,ns in [(monic,n),(full,N)]:
 for d,q in zip(dirs,ns):assert cs(-1,cm(d,conj_den))[0]==scale(2,times(t,q))
w=[t2,zero,t2,t3]
assert plus(plus(times(w[0],w[0]),times(w[2],w[2])),times(w[3],w[3]))==plus(scale(2,t4),times(t3,t3))
# Exact zero-set controls, testing both signs of imaginary q and positive real q.
curvature=[]
for M in [F(1),F(7,3),F(10**6)]:
 for tau in [F(1,10),F(1,1000),F(1,10**12)]:
  for qr,qi,ar,ai in [(M,0,0,tau),(0,M,tau,-tau),(0,-M,tau,tau)]:
   ar,ai,qr,qi=map(F,(ar,ai,qr,qi)); a2r=ar*ar-ai*ai;a2i=2*ar*ai
   br,bi=a2r/4,a2i/4; norm2=ar*ar+ai*ai+br*br+bi*bi
   # alpha(0)=0 and alpha(a,a^2/4)=-Re(a)/2 exactly.
   linear=-ar/2-2*qr*br-2*qi*bi
   deficit=-ar/2-linear
   assert deficit+(M/2)*norm2>=0
   strict=deficit+((M+1)/2)*norm2
   assert strict>=norm2/2 and strict>0
   curvature.append({'M':str(M),'tau':str(tau),'q':[str(qr),str(qi)],'a':[str(ar),str(ai)],'needed_curvature':str(-2*deficit/norm2),'strict_extra_margin':str(strict)})
# Root-generated rational chart check independently of discriminant formula.
stable_root_cases=0
for r1,r2,im1,im2 in itertools.product([F(0),F(-1,100),F(-3)], [F(0),F(-1,100),F(-3)], [F(-2),F(0),F(2)], [F(-2),F(0),F(2)]):
 ar,ai=-(r1+r2),-(im1+im2)
 br,bi=r1*r2-im1*im2,r1*im2+r2*im1
 U,V=br+ai*ai/4,bi-ar*ai/2
 assert ar>=0 and U>=0 and V*V<=ar*ar*U
 stable_root_cases+=1
# Floating reverse controls are supplementary only, exact edge checks are above.
chart_grid=0
for x,U,V in itertools.product(range(-4,5),range(-4,5),range(-4,5)):
 d=cmath.sqrt(x*x-4*(U+1j*V)); alpha=max((-x+d).real/2,(-x-d).real/2)
 chart=(x>=0 and U>=0 and V*V<=x*x*U)
 assert chart==(alpha<=1e-12)
 chart_grid+=1
out={'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','symbolic_polynomial_derivatives':10,'symbolic_root_identities':2,'rational_zero_set_curvature_cases':len(curvature),'rational_stable_root_chart_cases':stable_root_cases,'floating_reverse_integer_grid_cases':chart_grid,'curvature_rows':curvature,'limitations':'Symbolic identities exact for all real t. Root and zero-set controls exact rational. Reverse chart grid supplementary floating controls only. Universal metric/projection/function claims separately reviewed analytically; no minimizer pair or interval-certified numerics asserted.'}
(R/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='curvature_rows'},indent=2))
