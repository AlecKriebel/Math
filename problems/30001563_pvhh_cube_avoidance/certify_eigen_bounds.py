#!/usr/bin/env python3
"""Directed interval reconstruction of the CCSS eigencoordinate bounds.
Uses mpmath interval arithmetic plus exact integer/Fraction comparisons.
"""
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import itertools,json,hashlib
mp.iv.dps=60;iv=mp.iv
poly=lambda x:x**4-x**3-2*x*x+2*x-1
roots=[]
for a,b in [(F(169,100),F(17,10)),(F(-151,100),F(-15,10))]:
 assert poly(a)*poly(b)<0
 for _ in range(180):
  c=(a+b)/2
  if poly(a)*poly(c)<=0:b=c
  else:a=c
 roots.append((a,b))
def rat(x):return iv.mpf(x.numerator)/x.denominator
def interval(a,b):return iv.mpf([rat(a).a,rat(b).b])
a,b=[interval(*r) for r in roots];alpha=(1-a-b)/2;mod2=-1/(a*b);imag=iv.sqrt(mod2-alpha**2)
lams=[iv.mpc(a,0),iv.mpc(b,0),iv.mpc(alpha,imag)]
assert abs(lams[0]).a>1 and abs(lams[1]).a>1 and abs(lams[2]).b<1
rows=[]
for z in lams:
 R=[1,z*(z-1),(1+z*(z-1))/z,z-1]
 L=[1,z*(z-1),z-1,(1+z*(z-1))/z]
 norm=iv.sqrt(sum(abs(t)**2 for t in R));den=sum(l*r for l,r in zip(L,R))
 rows.append([norm*t/den for t in L])
S=10**18
def box(v):
 # Endpoints are exact binary mpf values. Convert their tuple to Fraction.
 def frac(t):
  sign,man,exp,bc=t;return F((-1 if sign else 1)*man)*(F(2)**exp)
 lo=frac(v._mpi_[0]);hi=frac(v._mpi_[1]);return [lo.numerator*S//lo.denominator,-((-hi.numerator*S)//hi.denominator)]
coef=[[[*box(z.real)],[*box(z.imag)]] for row in rows for z in row];coef=[coef[i*4:(i+1)*4] for i in range(3)]
def dotbox(row,x,part):
 lo=hi=0
 for c,k in zip(row,x):
  a,b=c[part];lo+=min(a*k,b*k);hi+=max(a*k,b*k)
 return lo,hi
def abs2box(row,x):
 lo2=hi2=0
 for part in [0,1]:
  a,b=dotbox(row,x,part);lo2+=0 if a<=0<=b else min(a*a,b*b);hi2+=max(a*a,b*b)
 return lo2,hi2
C=[F(19032,10000),F(29819,10000),F(2176,1000)]
# ||Q|| <= ||Q||_F = 2, all four columns normalized. Hence norm²(x)<89.
assert 4*(C[0]**2+C[1]**2+2*C[2]**2)<89
U=[];uncertain=0;tested=0
for x in itertools.product(range(-9,10),repeat=4):
 if sum(t*t for t in x)>88:continue
 tested+=1;bounds=[abs2box(row,x) for row in coef]
 if any(lo*C[i].denominator**2>C[i].numerator**2*S*S for i,(lo,hi) in enumerate(bounds)):continue
 if not all(hi*C[i].denominator**2<=C[i].numerator**2*S*S for i,(lo,hi) in enumerate(bounds)):uncertain+=1
 U.append(x)
assert uncertain==0
# Verify expanding-coordinate induction constants, with directed intervals.
C1=2*abs(rows[0][3])/(abs(lams[0])-1);C2=2*abs(rows[1][0]-rows[1][3])/(abs(lams[1])-1)
assert C1.b<rat(C[0]).a and C2.b<rat(C[1]).a
# Explicit D9 set, using source labelled-prefix automaton.
zero=(0,0,0,0);e0=(1,0,0,0);e4=(0,0,0,1)
images=[(0,2),(3,2),(1,),(0,1)];edges=[[(d,zero if j==0 else (e0 if word[0]==0 else e4))for j,d in enumerate(word)]for word in images]
add=lambda a,b:tuple(x+y for x,y in zip(a,b));sub=lambda a,b:tuple(x-y for x,y in zip(a,b));mul=lambda a:(a[0]+a[3],a[2]+a[3],a[0]+a[1],a[1])
states={(a,zero)for a in range(4)}
for _ in range(9):states={(b,add(mul(v),d))for a,v in states for b,d in edges[a]}
D=sorted({v for a,v in states});assert len(D)==301
# Exact squared upper bounds using rational coefficient boxes.
maxsq=max(abs2box(coef[2],sub(a,b))[1]for a in D for b in D)
shortsq=max(abs2box(coef[2],sub(a,b))[1]for a,b in itertools.product([zero,e0,e4],repeat=2))
B3=2*(iv.sqrt(rat(F(maxsq,S*S)))+iv.sqrt(rat(F(shortsq,S*S)))*abs(lams[2])**9/(1-abs(lams[2])))
assert B3.b<rat(C[2]).a
# Lattice exclusion constants via determinant of two complex images.
e=(1,-2,2,-1);f=(1,-1,-1,1)
z=sum(rows[2][i]*e[i]for i in range(4));w=sum(rows[2][i]*f[i]for i in range(4))
det=abs(z.real*w.imag-z.imag*w.real)
assert (det/abs(w)).a>rat(F(149,100)).b
assert (det/abs(z)).a>rat(F(216,100)).b
assert C[2]/F(149,100)<2 and C[2]/F(216,100)<2
short=[]
for m,n in itertools.product(range(-1,2),repeat=2):
 x=tuple(m*a+n*b for a,b in zip(e,f));lo,hi=abs2box(coef[2],x)
 if lo*C[2].denominator**2<=C[2].numerator**2*S*S:short.append(x)
assert set(short)=={zero,e,tuple(-a for a in e)}
for x in short:
 for i in [0,1]:assert abs2box(coef[i],x)[1]*C[i].denominator**2<=C[i].numerator**2*S*S
# Verify the prefix-error maxima that enter the expanding induction.
for i,chosen in [(0,e4),(1,sub(e0,e4))]:
 chosen_abs=abs(sum(rows[i][k]*chosen[k]for k in range(4)))
 for x,y in itertools.product([zero,e0,e4],repeat=2):
  v=sub(x,y)
  if v in [chosen,tuple(-a for a in chosen)]:continue
  assert abs(sum(rows[i][k]*v[k]for k in range(4))).b<chosen_abs.a
stream='\n'.join(','.join(map(str,x))for x in U)+'\n'
p=Path(__file__).parent/'U_CERTIFIED.csv';p.write_bytes(stream.encode())
result={'status':'PASS','method':'mpmath directed interval arithmetic at60 decimal digits; exact integer coefficient boxes at10^-18;180 rational bisections for each real root','bounded_integer_candidates':tested,'U_vectors':len(U),'uncertain_membership_cases':uncertain,'D9_vectors':301,'bounds':[str(x)for x in C],'complex_bound_interval':str(B3),'U_sha256':hashlib.sha256(stream.encode()).hexdigest(),'eigen_coefficient_boxes':coef,'scope':'Outward-rounded reconstruction of the credited CCSS analytic reduction. This is not a new avoidance theorem.'}
print(json.dumps(result,indent=2,sort_keys=True))
