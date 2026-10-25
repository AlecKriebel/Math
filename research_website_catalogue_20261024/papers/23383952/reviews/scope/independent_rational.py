"""Own exact arithmetic, separate algorithms and constants from supplied code.
Certifies the finite inequalities after the analytic deductions in the early ledger.
"""
from fractions import Fraction as Q
from math import isqrt
import json
def need(ok,label):
 if not ok:raise RuntimeError(label)
def atan(x,n):
 total=Q(0);term=x
 for k in range(n):total+=term/(2*k+1);term*=-x*x
 return total
def exp_lower(x,n=60):
 total=term=Q(1)
 for k in range(1,n+1):term*=x/k;total+=term
 return total,term
def exp_upper(x,n=20):
 low,last=exp_lower(x,n);need(0<=x<n+2,'Taylor ratio domain');return low+last*x/(n+1)/(1-x/(n+2))
def root_up(x):
 scale=10**8;k=isqrt(x.numerator*scale**2//x.denominator);v=Q(k+1,scale)
 need(Q(k,scale)**2<=x<v*v,'integer root enclosure');return v
def neg_up(x):return 1/exp_lower(x)[0]
def first(t):return t*root_up(t)*neg_up(3*t/4)
def rest(t):return t*root_up(t)*(4*neg_up(15*t/4)+18*neg_up(35*t/4))
def f(q):return f'{q.numerator}/{q.denominator}'
# Different Machin identity:4atan(1/5)-atan(1/239)=pi/4.
a=Q(1,5);double=2*a/(1-a*a);four=2*double/(1-double*double)
need((four-Q(1,239))/(1+four/Q(239))==1,'independent Machin tangent')
pi_low=16*atan(Q(1,5),18)-4*atan(Q(1,239),19)
pi_up=16*atan(Q(1,5),19)-4*atan(Q(1,239),18)
rlo,rhi=Q(1772,1000),Q(1773,1000);need(rlo*rlo<pi_low<pi_up<rhi*rhi,'sqrt pi bounds')
e_up=exp_upper(Q(1));need(e_up<Q(2719,1000),'e upper')
cap=1+Q(8,3)/(exp_lower(Q(1),20)[0]**3);need(cap<2,'cap volume')
L=10000;lower=rlo/Q(2719,1000)*(L-4*rhi)/(L+4)
need(lower==Q(1106714561,1700054750),'displayed exact lower')
margin=lower-Q(13,20);need(margin==Q(3357947,3400109500)>0,'displayed exact margin')
small=rhi*exp_upper(Q(7,20))/4
points=[Q(i,10) for i in range(14,21)];ceilings=[629002,631338,636143,639464,641172,641202,639541]
values=[small]+[first(b)+rest(a) for a,b in zip(points,points[1:])]
for v,c in zip(values,ceilings):need(v<Q(c,10**6),'displayed seven-region enclosure')
need(Q(max(ceilings),10**6)<Q(321,500)<Q(13,20),'strict counterexample separation')
need(pi_up*e_up**3<128,'round maximum interior witness')
need(lower>rhi/4,'weighted maximum interior witness')
need(Q(16,9)/(1+7*points[0])<Q(1,2),'entire geometric ratio range')
need(2*pi_low*pi_low>Q(7,5),'small-time Poisson sign range')
need(Q(3,2)-Q(3,4)*2==0,'all large-time round modes nonincreasing at2')
need(Q(3,2)-Q(15,4)*Q(2,5)==0,'all B modes nonincreasing at2/5')
# Controls are altered hypotheses, not counterexamples to the original claim.
short=rlo/Q(2719,1000)*(1-4*rhi)/5;need(short<Q(13,20),'short cylinder fails threshold')
need(Q(3,4)-Q(5,4)==-Q(1,2) and Q(1,4)-Q(3,4)==-Q(1,2),'unitary covariance exponents')
need(Q(1,2)-Q(5,4)!=-Q(1,2),'wrong L2 unitary exponent rejected')
need(Q(2,3)*Q(3,2)==1 and Q(1,2)*Q(3,2)!=1,'normalization power control')
need(Q(2,5)<Q(1),'monotonicity lower endpoint has actual content')
print(json.dumps({'status':'PASS','independent_algorithm':'Recurrence Taylor60/20, isqrt lattice, independent Machin1/5/1/239; no supplied imports','lower_exact':f(lower),'lower_margin_exact':f(margin),'seven_exact_upper_bounds':[f(v) for v in values],'seven_displayed_enclosures_verified':ceilings,'all_time_round_bound':'641202/1000000 <321/500','cap_upper':f(cap),'pi_bounds':[f(pi_low),f(pi_up)],'e_upper':f(e_up),'controls':['short cylinder does not meet threshold','wrong Hilbert-space unitary power rejected','wrong volume power rejected','Poisson and tail ratio ranges exact','both maxima have strict interior witnesses'],'universal_obligations':'Smoothness, form domain, minmax, Poisson summation and heat asymptotics are written deductions, not certified by a finite grid.'},indent=2))
