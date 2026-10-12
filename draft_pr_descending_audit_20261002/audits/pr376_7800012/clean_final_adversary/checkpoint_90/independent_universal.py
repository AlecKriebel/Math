"""Independent controls for universal claims, with all-phase symbolic moments."""
import sympy as s
import itertools,json,pathlib
from collections import Counter
from fractions import Fraction as Q
count=0
def ck(v,label):
 global count
 if not v:raise AssertionError(label)
 count+=1
steps=[(1,0),(0,1),(-1,0),(0,-1)]
for length,want in [(2,{'empty':4}),(4,{'empty':28,'square':8}),(6,{'empty':232,'square':144,'rectangle':24})]:
 classes=Counter();monomials=Counter()
 for word in itertools.product(steps,repeat=length):
  pos=(0,0);boundary=Counter()
  for dx,dy in word:
   end=(pos[0]+dx,pos[1]+dy)
   if dx+dy==1:boundary[(pos,end)]+=1
   else:boundary[(end,pos)]-=1
   pos=end
  if pos!=(0,0):continue
  mono=tuple(sorted((k,v) for k,v in boundary.items() if v));monomials[mono]+=1
  if not mono:classes['empty']+=1
  elif len(mono)==4:classes['square']+=1
  elif len(mono)==6:classes['rectangle']+=1
  else:raise AssertionError(mono)
  ck(all(abs(v)==1 for e,v in mono),'all returning nonempty reduced phases are once-wound simple loops')
 ck(dict(classes)==want,'independent universal arbitrary-edge monomials')
 for mono,mult in monomials.items():
  neg=tuple((k,-v) for k,v in mono);ck(monomials[neg]==mult,'orientation coefficients pair')
 print(json.dumps(dict(stage='moments',length=length,classes=dict(classes),distinct_phase_monomials=len(monomials))),flush=True)
# SOS independently using graph incidence: degree4 and m=2N.
N,S,A,B=s.symbols('N S A B',positive=True)
ck(s.expand((40*N+16*S+12*(A+B-4*N)/2)-(s.Rational(44,3)*N+48/N*(S+N/6)**2+6*(A-8*S**2/N)+6*B))==0,'universal defect SOS')
r=2*s.sqrt(2);M=4*(4+r)
ck(s.simplify(11/(3*r*M**2)-11*(3*s.sqrt(2)-4)/1536)==0,'gap correction normalization')
u=s.symbols('u',nonnegative=True)
ck(s.expand(M**2*(u-r)**2-u**2*(u**2-8)**2).subs(u,r)==0,'top spectral defect equality')
# Norm <=4 suffices: |s(s^2-8)| <= 8s and <=4(4+r)|s-r|.
for k in range(81):
 v=Q(k,20);ck(abs(v*v-8)<=8,'remaining singular bound');ck(v*(v+r)<=M,'top singular bound')
# Independent Harper determinant, no candidate polynomial helper.
z,w,E=s.symbols('z w E');diags=[z+1/z,s.I*z-s.I/z,-z-1/z,-s.I*z+s.I/z]
H=s.diag(*diags)
for i in range(3):H[i,i+1]=H[i+1,i]=1
H[3,0]=w;H[0,3]=1/w
ck(s.expand((E*s.eye(4)-H).det())==E**4-8*E**2+4-z**4-z**-4-w-w**-1,'Harper determinant independently expanded')
t=s.symbols('t');f=s.sqrt(4+s.sqrt(12+2*t))
for k in range(1,9):
 df=s.diff(f,t,k)
 for v in [-2,-1,0,1,2]:ck((-1)**(k-1)*df.subs(t,v)>0,'derivative signs including endpoints')
# Newton-sum root derivative compared to implicit-root trace, Chebyshev polynomial arbitrary c.
x,c=s.symbols('x c')
for n in range(1,9):
 pp=s.Poly(s.chebyshevt(n,x)-c,x);C=s.zeros(n)
 for j in range(1,n):C[j,j-1]=1
 for i in range(n):C[i,n-1]=-pp.nth(i)/pp.LC()
 for m in range(1,n+3):
  lhs=s.diff(s.trace(C**m),c)
  inv=s.invert(pp.diff(),pp);rem=(s.Poly(m*x**(m-1),x)*inv).rem(pp)
  rhs=sum(rem.nth(j)*s.trace(C**j) for j in range(n))
  ck(s.simplify(lhs-rhs)==0,'all-c Chebyshev root derivative identity')
 print(json.dumps(dict(stage='holonomy',n=n,arbitrary_c_identity=True)),flush=True)
# One-edge bound is sharp; all ranks including 0,N give correct endpoints.
A=s.Matrix([[0,1],[1,0]]);P=(s.eye(2)-A)/2
ck(P*P==P and s.trace(P*A)==-1,'sharp boundary constant1')
for L in range(4,100,2):
 for ell in range(4,L+1,2):
  k=L//ell;rem=L*L-k*k*ell*ell
  ck(rem%4==0 and k*k*(ell*ell//4)+rem//4==L*L//4,'leftover exact quarter count')
# Artificial ordered spectra demonstrate unequal allocations can strictly improve at quarter fill.
spec1=[-10,0,1,9];spec2=[-2,-1,1,2];R=2
best=min(sum(spec1[:r])+sum(spec2[:R-r]) for r in range(R+1))
ck(best==sum(sorted(spec1+spec2)[:R]),'union allocation theorem')
spec1=[-10,-9,9,10];spec2=[-2,-1,1,2]
ck(sum(sorted(spec1+spec2)[:2])<spec1[0]+spec2[0],'equal block allocation fails')
print(json.dumps(dict(stage='complete',assertions=count,scope='Universal algebraic controls support written derivations, not unrestricted optimal flux')),flush=True)
