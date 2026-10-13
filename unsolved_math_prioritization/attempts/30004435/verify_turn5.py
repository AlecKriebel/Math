from fractions import Fraction as F
from math import factorial,comb
import json
checks=0;beta_pairs=0;rotation_steps=0

def check(x):
 global checks
 assert x;checks+=1

def beta(a,b):return F(factorial(a-1)*factorial(b-1),factorial(a+b-1))
for N in range(1,26):
 for k in range(N+1):
  pk=comb(N,k)*beta(k+1,N-k+1);check(pk==F(1,N+1))
  check(beta(k+2,N-k+1)/beta(k+1,N-k+1)==F(k+1,N+2))
 defect=F(0);total=F(0)
 for k in range(N+1):
  for l in range(N+1):
   p=comb(N,k)*comb(N,l)*beta(k+l+1,2*N-k-l+1);total+=p;defect+=p*F(k-l,N+2)**2;beta_pairs+=1
 check(total==1);check(defect==F(N,3*(N+2)**2))
 # Direct integral of the squared estimation error summed over counts.
 mse=F(0)
 for k in range(N+1):
  mse+=comb(N,k)*(F(k,N)**2*beta(k+1,N-k+1)-2*F(k,N)*beta(k+2,N-k+1)+beta(k+3,N-k+1))
 check(mse==F(1,6*N))
# Exact ordered quadratic field Q(sqrt2): pairs a+b sqrt2.
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def neg(x):return(-x[0],-x[1])
def sub(x,y):return add(x,neg(y))
def mulint(x,n):return(x[0]*n,x[1]*n)
def sign(x):
 a,b=x
 if b==0:return (a>0)-(a<0)
 if a==0:return (b>0)-(b<0)
 if a>0 and b>0:return 1
 if a<0 and b<0:return -1
 d=a*a-2*b*b
 return ((d>0)-(d<0)) if a>0 else -((d>0)-(d<0))
def le(x,y):return sign(sub(y,x))>=0
def fl(x):
 a,b=x;lo=min(a+b,a+2*b).__floor__()-1;hi=max(a+b,a+2*b).__ceil__()+1
 while lo+1<hi:
  m=(lo+hi)//2
  if sign(sub(x,(F(m),F(0))))>=0:lo=m
  else:hi=m
 return lo
def frac(x):return sub(x,(F(fl(x)),F(0)))
zero=(F(0),F(0));one=(F(1),F(0));alpha=(F(-1),F(1))
def symbol(U,k):return fl(add(U,mulint(alpha,k+1)))-fl(add(U,mulint(alpha,k)))
widths=[]
for a in range(17):
 U=(F(a,17),F(0));lowF=lowP=zero;highF=highP=one;forward=backward=0
 for n in range(1,257):
  t=frac(mulint(alpha,n));q=fl(mulint(alpha,n));threshold=sub(one,t)
  forward+=symbol(U,n-1);backward+=symbol(U,-n)
  check(forward==fl(add(U,mulint(alpha,n))));check(backward==-fl(sub(U,mulint(alpha,n))))
  fbit=forward-q;pbit=backward-q;check(fbit in [0,1] and pbit in [0,1]);check(fbit==int(le(threshold,U)));check(pbit==int(not le(t,U)))
  if fbit:
   if le(lowF,threshold):lowF=threshold
  elif le(threshold,highF):highF=threshold
  if pbit:
   if le(t,highP):highP=t
  elif le(lowP,t):lowP=t
  check(le(lowF,U) and le(U,highF));check(le(lowP,U) and le(U,highP));rotation_steps+=1
 check(le(sub(highF,lowF),(F(1,100),F(0))));check(le(sub(highP,lowP),(F(1,100),F(0))))
 widths.append({'phase':str(U[0]),'forward_width':[str(x) for x in sub(highF,lowF)],'past_width':[str(x) for x in sub(highP,lowP)]})
 for m in range(-8,9):
  V=frac(add(U,mulint(alpha,m)))
  check(all(symbol(V,k)==symbol(U,m+k) for k in range(-5,6)))
print(json.dumps(dict(assertions=checks,beta_joint_count_pairs=beta_pairs,rotation_reconstruction_steps=rotation_steps,rotation_final_exact_widths=widths,scope='Exact controls for the proved conditional-law mixture theorem and binary irrational-rotation reconstruction; the general method request remains unresolved.'),indent=2,sort_keys=True))
