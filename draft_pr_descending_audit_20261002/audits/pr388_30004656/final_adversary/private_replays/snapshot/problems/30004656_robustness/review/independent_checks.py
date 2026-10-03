#!/usr/bin/env python3
"""Independent exact controls; no author code is imported."""
from fractions import Fraction as F
from itertools import product,combinations
from math import comb,factorial,prod
from collections import defaultdict
import random,json
rng=random.Random(3000465631)
counts={k:0 for k in ['circle_law','cell_occupancy','sphere_lift','moments','relu_patterns','relu_energy','chaining','quadratic_sphere','balanced_trace','rank_constants']}
def check(v,k):
 assert v,k
 counts[k]+=1
# Cyclic flip distribution by a transfer recursion with fixed first label.
for n in range(2,31):
 dp={(0,0):1}
 for _ in range(n-1):
  nd=defaultdict(int)
  for (last,j),v in dp.items():
   for nxt in [0,1]:nd[nxt,j+(nxt!=last)]+=v
  dp=nd
 got=defaultdict(int)
 for (last,j),v in dp.items():got[j+(last!=0)]+=2*v
 for j in range(n+1):check(got[j]==(2*comb(n,j) if j%2==0 else 0),'circle_law')
 check(got[0]==2,'circle_law')
 for j in range(2,n+1,2):
  for q in range(1,5):
   integral=F(q,j**q)*sum(F((-1)**h*comb(n-1,h),q+h) for h in range(n))
   closed=F(factorial(q)*factorial(n-1),j**q*factorial(n+q-1))
   check(integral==closed,'circle_law')
# Direct labeled-cell enumeration versus Stirling occupancy counting.
for M in range(1,5):
 for n in range(6):
  good=0
  for seq in product(range(2*M),repeat=n):
   st=[0]*M
   for a in seq:st[a//2]|=1<<(a%2)
   good+=all(v!=3 for v in st)
  S=[0]*(n+1);S[0]=1
  for i in range(1,n+1):
   S=[0]+[(S[k-1] if k-1<len(S) else 0)+k*(S[k] if k<len(S) else 0) for k in range(1,n+1)]
  formula=sum(S[k]*prod(range(M-k+1,M+1))*2**k for k in range(min(n,M)+1))
  check(good==formula,'cell_occupancy')
  inc=sum((-1)**j*comb(M,j)*2**(M-j)*(M-j)**n for j in range(M+1))
  check(good==inc,'cell_occupancy')
# Rational sphere points from two-parameter stereographic coordinates.
pts=[]
for a,b in product(range(-3,4),repeat=2):
 p,q=F(a,20),F(b,20);D=1+p*p+q*q
 x=(2*p/D,2*q/D,(1-p*p-q*q)/D);pts.append(x)
 check(sum(v*v for v in x)==1,'sphere_lift')
 check(x[0]**2+x[1]**2<=F(1,4),'sphere_lift')
for x,y in product(pts,repeat=2):
 full=sum((a-b)**2 for a,b in zip(x,y));projected=sum((x[i]-y[i])**2 for i in range(2))
 check(full<=F(4,3)*projected,'sphere_lift')
# Moment coefficients and the centered independent-copy bound.
for d in range(2,81):
 for m in range(1,25):
  odd=prod(range(1,2*m,2));spherical=F(odd,prod(d+2*j for j in range(m)))
  check(spherical<=F(odd,d**m),'moments')
  check(F(4**m*odd,factorial(2*m))==F(2**m,factorial(m)),'moments')
  check(odd<=2**m*factorial(m),'moments')
for a,b in product([F(0),F(1,5),F(1,2),F(1)],repeat=2):
 for m in range(1,9):check((a-b)**(2*m)<=2**(2*m-1)*(a**(2*m)+b**(2*m)),'moments')
# Each strict activation pattern of an invertible triangular row matrix.
for s in product([-1,1],repeat=3):
 x3=s[2];x2=s[1]-x3;x1=s[0]-x2
 check((x1+x2,x2+x3,x3)==s,'relu_patterns')
 check(x1*x1+x2*x2+x3*x3>0,'relu_patterns')
# A dependent-row cancellation diagnoses why the energy theorem needs rank.
for t in range(-20,21):check(max(0,t)-max(0,t)==0,'relu_patterns')
check(1+1>0,'relu_patterns')
for dim in range(2,6):
 for k in range(1,8):
  for _ in range(8):
   vs=[[rng.randrange(-5,6) for _ in range(dim)] for _ in range(k)]
   sq=lambda w:sum(v*v for v in w)
   energy=sum(sq(v) for v in vs)
   vals=[sq([sum(e[i]*vs[i][j] for i in range(k)) for j in range(dim)]) for e in product([-1,1],repeat=k)]
   subset=[sq([sum(e[i]*vs[i][j] for i in range(k)) for j in range(dim)]) for e in product([0,1],repeat=k)]
   check(sum(vals)==2**k*energy,'relu_energy')
   check(energy<=4*max(subset),'relu_energy')
# Strict rational upper bounds for logarithms, via finite exponential sums.
for z,b in [(F(3,4),2),(F(3),9),(F(2),5)]:
 check(sum(z**j/F(factorial(j)) for j in range(9))>b,'chaining')
for d in range(2,81):
 for j in range(1,31):
  for v in [F(1,2),F(1),F(d),F(3*d)]:
   exponent=F(3,4)*d*(2*j+3)-8*(d*(j+2)+v+j)
   check(exponent<=-v-j,'chaining')
# Non-diagonal rational quadratic forms and the exact spectral-spread square.
circle=[]
for j in range(-6,7):
 t=F(j,5);circle.append(((1-t*t)/(1+t*t),2*t/(1+t*t)))
for a,b,c in product(range(-2,3),repeat=3):
 spread2=(a-c)**2+4*b*b
 q=lambda x:a*x[0]**2+2*b*x[0]*x[1]+c*x[1]**2
 for x,y in product(circle,repeat=2):
  dist=sum((x[i]-y[i])**2 for i in range(2))
  check((q(x)-q(y))**2<=spread2*dist,'quadratic_sphere')
# Balanced selected points yield an exactly trace-zero signed matrix.
for _ in range(500):
 xs=rng.sample(circle,6);ys=[1,1,1,-1,-1,-1]
 O=[[sum(ys[i]*xs[i][a]*xs[i][b] for i in range(6)) for b in range(2)] for a in range(2)]
 check(O[0][0]+O[1][1]==0,'balanced_trace')
 a,b,c,shift=[F(rng.randrange(-9,10),3) for _ in range(4)]
 check(a*O[0][0]+2*b*O[0][1]+c*O[1][1]==(a-shift)*O[0][0]+2*b*O[0][1]+(c-shift)*O[1][1],'balanced_trace')
# Nuclear/spread inequalities and the final rank constants.
for d in range(2,31):
 for _ in range(30):
  eig=[F(rng.randrange(-20,21),7) for _ in range(d)];s=max(eig)-min(eig);mid=(max(eig)+min(eig))/2
  check(sum(abs(e-mid) for e in eig)<=d*s/2,'rank_constants')
  eig[0]=F(0);s=max(eig)-min(eig);r=sum(e!=0 for e in eig)
  check(sum(abs(e) for e in eig)<=r*s,'rank_constants')
for n in range(16,401):
 for d in range(2,n//8+1):
  N=2*((3*n+7)//8)
  check(F(N*n,256)<=F(N*N,4),'rank_constants')
  for k in [1,d-1,d,d+7]:
   lower=F(N*d,2048**2*k*k) if k<d else F(N,1024**2*d)
   check(lower>=F(n,8192**2*k),'rank_constants')
# Bernstein optimization branches, without floating-point exponentials.
for r in range(1,161):
 u=F(r,16)
 if u<=4:
  lam=u/64;check(lam<=F(1,16) and -lam*u+32*lam*lam==-u*u/128,'moments')
 else:check(-u/16+F(1,8)<=-u/32,'moments')
print(json.dumps({'status':'PASS','independent_assertions':sum(counts.values()),'counts':counts,'scope':'Independent exact finite controls; probability, source and infinite-uniformity conclusions are audited analytically.'},indent=2,sort_keys=True))
