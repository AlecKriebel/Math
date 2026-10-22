#!/usr/bin/env python3
"""Fresh rational tests; the analytic review carries all continuum/time claims."""
from fractions import Fraction as F
from pathlib import Path
from math import comb
import json,sys
R=Path(__file__).resolve().parent
counts={}
def need(c,m):
 if not c:raise ValueError(m)
def d2(a,b):return sum((x-y)**2 for x,y in zip(a,b))
def wins(zi,zj,di,dj,a,b):return zi**(2*a)*dj**b>=zj**(2*a)*di**b
sites=[(F(1,5),F(1,4)),(F(3,4),F(1,3)),(F(2,5),F(4,5))];h=F(1,16);K=4*h*h
squared=[d2(sites[i],sites[j]) for i,j in [(0,1),(0,2),(1,2)]]
need(squared==[F(557,1800),F(137,400),F(49,144)],'distances')
det=(sites[1][0]-sites[0][0])*(sites[2][1]-sites[0][1])-(sites[1][1]-sites[0][1])*(sites[2][0]-sites[0][0]);need(det==F(343,1200),'determinant')
need(K==F(1,64) and K*K==F(1,4096) and 1-2*K*K==F(2047,2048),'constants')
# Geometries unlike the literal witness: collinear, square contact, six-site field.
scenarios=[('collinear',[(F(1,4),F(1,2)),(F(1,2),F(1,2)),(F(3,4),F(1,2))],F(1,32)),('square_boundary_contact',[(F(1,10),F(1,10)),(F(4,5),F(7,10))],F(1,10)),('six_sites',[(F(i,5),F(j,4)) for i in (1,2,4) for j in (1,3)],F(1,64))]
for label,x,h0 in scenarios:
 for i,site in enumerate(x):
  need(all(h0<=v<=1-h0 for v in site),'geometry interior')
  need(all(d2(site,other)>=8*h0*h0 for j,other in enumerate(x) if i!=j),'geometry separation')
 c=0
 for a,b in [(2,5),(3,8),(5,12)]:
  for i in range(len(x)):
   for s in [F(2,7),F(3,11),F(1,103)]:
    zi=s**b;z=[F(0)]*len(x);z[i]=zi;others=[j for j in range(len(x)) if i!=j];den=sum((r+1)**2 for r in range(len(others)))
    for rank,j in enumerate(others,1):z[j]=(1-zi)*rank*rank/den
    need(sum(z)==1 and min(z)>0,'state')
    for u,v in [(F(-1),F(1)),(F(1),F(-1)),(F(3,7),F(-2,9)),(F(0),F(0))]:
     y=(x[i][0]+h0*s**a*u,x[i][1]+h0*s**a*v)
     need(all(0<=w<=1 for w in y),'point in square')
     for j in others:need(wins(zi,z[j],d2(y,x[i]),d2(y,x[j]),a,b),'all competitor win');c+=1
 counts[label+'_hard_comparisons']=c
# Exact polynomial identity for different scalar exponents p=1-1/m.
polys=0
for m in (2,3,4,5,7):
 for u0 in (F(1,1000),K,F(2,3)):
  a=u0-K
  # b(v)=(K+a v)^m; vprime=-v/m.
  deriv=[-F(k,m)*F(comb(m,k))*K**(m-k)*a**k for k in range(m+1)]
  rhs=[F(0)]+[-a*F(comb(m-1,k-1))*K**(m-k)*a**(k-1) for k in range(1,m+1)]
  need(deriv==rhs,'Bernoulli polynomial identity')
  for v in (F(0),F(1,7),F(5,9),F(1)):
   B=K+(u0-K)*v;need(B>0 and B**m>=min(K**m,u0**m),'comparison bracket')
  polys+=1
counts['scalar_polynomial_identities']=polys
# Regularity identity at corner ties, equal weights, close sites, interior test points.
grad=0
for a,b in [(sites[0],sites[1]),((F(1,4),F(1,3)),(F(3,4),F(2,3))),((F(1,2),F(1,2)),(F(1,2)+F(1,2**25),F(1,2)))]:
 corner_lambda=d2((F(0),F(0)),a)/d2((F(0),F(0)),b)
 for lam in [F(1),F(999999999,10**9),F(1000000001,10**9),corner_lambda,F(1,10**10)]:
  for y in [(F(0),F(0)),(F(1),F(1)),(F(2,7),F(5,9))]:
   value=d2(y,a)-lam*d2(y,b);g=[2*((1-lam)*y[k]-a[k]+lam*b[k]) for k in (0,1)]
   need(sum(v*v for v in g)==4*(lam*d2(a,b)+(1-lam)*value),'gradient identity')
   if value==0:need(sum(v*v for v in g)>0,'zero-level regularity')
   grad+=1
counts['gradient_identities']=grad
# Quantitative open box, checked by interval inequalities rather than a finite positional grid.
eps=F(1,1000);need(all(h+eps<u<1-h-eps for x in sites for u in x),'openbox boundary')
initial=(F(1,6),F(1,3),F(1,2));need(sum(initial)==1 and min(initial)-eps>F(1,16384),'relative-simplex initial box keeps positive common lower')
# Initial perturbations are explicitly intersected with sum z=1. Positivity then forces each z<1.
need(all(u+eps<1 for u in initial),'relative initial box upper bound')
lo=[]
for i,j in [(0,1),(0,2),(1,2)]:
 low=sum(max(abs(sites[i][k]-sites[j][k])-2*eps,F(0))**2 for k in (0,1));need(low>8*h*h,'openbox separation');lo.append(str(low))
pmax=F(42,79);need(F(19,10)>1 and F(79,10)>2*F(21,10),'openbox parameters');need(14*(1-pmax)>6,'common lower exponent')
# Negative controls expose indispensable hypotheses and wrong extrapolations.
controls=[]
x=[(F(1,4),F(1,2)),(F(3,8),F(1,2)),(F(3,4),F(1,2))];y=(F(1,2),F(1,2));z=[F(1,100),F(1,10**6),F(989999,10**6)]
need(sum(z)==1 and wins(z[0],z[1],d2(y,x[0]),d2(y,x[1]),1,4) and not wins(z[0],z[2],d2(y,x[0]),d2(y,x[2]),1,4),'nearest-only negative')
controls.append('Nearest rival comparison can pass while a farther high-weight rival wins.')
need(K*F(1,4096)-F(1,4096)<0,'critical sign');controls.append('p=1 lower scalar field is negative; no asymptotic persistence follows.')
need(F(1,10**8)<K*K,'small start');controls.append('Initial-independent bound K^2 at t=0 fails for an allowed smaller initial coordinate.')
# Perturb the analytical gradient identity by dropping its essential lambda.
a,b=sites[:2];lam=F(2);y=(F(0),F(0));f=d2(y,a)-lam*d2(y,b);g=sum((2*((1-lam)*y[k]-a[k]+lam*b[k]))**2 for k in (0,1));need(g!=4*(d2(a,b)+(1-lam)*f),'wrong gradient control');controls.append('Dropping the lambda factor from the gradient identity is detected.')
out={'status':'PASS','optimized':bool(sys.flags.optimize),'counts':counts,'witness':{'squared_distances':list(map(str,squared)),'determinant':str(det),'K':str(K),'lower':str(K*K),'upper':str(1-2*K*K)},'interval_box':{'position_supnorm_radius':str(eps),'alpha_interval':['19/10','21/10'],'beta_interval':['79/10','81/10'],'relative_initial_radius':str(eps),'distance_lower_bounds':lo,'p_upper_bound':str(pmax),'common_all_time_lower':'1/16384','common_all_time_upper':'8191/8192','justification':'The exact interval inequalities preserve theorem hypotheses; min original initial weights minus eps exceeds common lower, and 14(1-pmax)>6 gives L^(1-p)<=K. This certifies hypotheses of the written analytic theorem, not sampled trajectories.'},'negative_controls':controls,'limitation':'Finite rational identities/comparisons do not prove universal inclusion, area regularity, time evolution, convergence, or priority.'}
(R/('EXACT_OPTIMIZED.json' if sys.flags.optimize else 'EXACT_NORMAL.json')).write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':'PASS','counts':counts,'negative_controls':len(controls)}))
