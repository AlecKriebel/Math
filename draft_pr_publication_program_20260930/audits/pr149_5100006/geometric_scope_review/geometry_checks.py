#!/usr/bin/env python3
"""Independent real-geometry diagnostics; exact deductions are in REPORT.md.

No submitted verifier, result, or review is imported. mpmath 1.3.0 is a locally
installed arithmetic dependency only. These are numerical diagnostics, not proofs.
"""
from pathlib import Path
import sys, json, math, hashlib, datetime
sys.path.insert(0, str(Path(__file__).resolve().parent / 'deps'))
import mpmath as mp
mp.mp.dps = 80


def fmt(x): return mp.nstr(x, 18)
def norm(v): return mp.sqrt(sum(z*z for z in v))
def distance(p,q): return norm([p[j]-q[j] for j in range(2)])
def dot(p,q): return sum(p[j]*q[j] for j in range(2))
def sub(p,q): return [p[j]-q[j] for j in range(2)]
def add(p,q): return [p[j]+q[j] for j in range(2)]

rows=[]
phases=['0','0.137','0.5','0.999999','1.731','3.999999']
for kstr in ['0.001','0.2','0.6','0.99']:
 k=mp.mpf(kstr); alpha=mp.mpf(1); beta=mp.sqrt(1-k*k); c=k
 K=mp.ellipk(k*k)
 sn=lambda u:mp.ellipfun('sn',u,k*k)
 cn=lambda u:mp.ellipfun('cn',u,k*k)
 dn=lambda u:mp.ellipfun('dn',u,k*k)
 for N in [6,10,14,18,22,26]:
  for tau in range(1,N//2):
   if math.gcd(tau,N)!=1: continue
   v=2*K*tau/N; delta=2*v; a=dn(v)/cn(v); b=beta/cn(v)
   def P(u): return [-a*sn(u),b*cn(u)]
   def Q(u): return [-alpha*sn(u),beta*cn(u)]
   axes=abs(a*a-b*b-c*c)
   tangent=reflection=antipodal=focal_formula=mp.mpf(0)
   plus=[];minus=[];paired=[]
   for ph in phases:
    u=mp.mpf(ph)*K; points=[P(u+j*delta) for j in range(N)]
    dp=[];dm=[]
    for j,p in enumerate(points):
     q=Q(u+(j+mp.mpf('0.5'))*delta)
     for endpoint in [p,points[(j+1)%N]]:
      tangent=max(tangent,abs(endpoint[0]*q[0]/alpha**2+endpoint[1]*q[1]/beta**2-1))
     prev=points[(j-1)%N]; nxt=points[(j+1)%N]
     ep=sub(prev,p); en=sub(nxt,p); ep=[z/norm(ep) for z in ep]; en=[z/norm(en) for z in en]
     normal=[p[0]/a**2,p[1]/b**2]; normal=[z/norm(normal) for z in normal]
     tangent_at_p=[-normal[1],normal[0]]
     reflection=max(reflection,abs(dot(add(ep,en),tangent_at_p)))
     antipodal=max(antipodal,norm(add(p,points[(j+N//2)%N])))
     directp=distance(p,[c,0]); directm=distance(p,[-c,0])
     focal_formula=max(focal_formula,abs(directp-(a-c*p[0]/a)),abs(directm-(a+c*p[0]/a)))
     dp.append(directp);dm.append(directm)
    plus.append(mp.fprod(dp));minus.append(mp.fprod(dm))
    paired.append(mp.fprod(a*a-c*c*sn(u+j*delta)**2 for j in range(N//2)))
   product_spread=(max(plus)-min(plus))/plus[0]
   focus_equality=max(abs(x-y)/plus[0] for x,y in zip(plus,minus))
   pairing_equality=max(abs(x-y)/plus[0] for x,y in zip(plus,paired))
   residuals=[axes,tangent,reflection,antipodal,focal_formula,product_spread,focus_equality,pairing_equality]
   assert max(residuals)<mp.mpf('1e-65'), (kstr,N,tau,residuals)
   rows.append({'k':kstr,'N':N,'tau':tau,'star':tau>1,'a':fmt(a),'b':fmt(b),'diagnostic_product':fmt(plus[0]),'max_residual':fmt(max(residuals))})

# Exact constructions independently derived in REPORT.md.
a=mp.sqrt(15);b=mp.sqrt(7);c=mp.sqrt(8)
tri=[[a,0],[-3*a/4,mp.mpf(7)/4],[-3*a/4,-mp.mpf(7)/4]]
mirror=[[-x,-y] for x,y in tri]
products=[mp.fprod(distance(p,[c,0]) for p in vertices) for vertices in [tri,mirror]]
exact_products=[15*a/2+3*c,15*a/2-3*c]
assert max(abs(x-y) for x,y in zip(products,exact_products))<mp.mpf('1e-65')
assert abs(products[0]**2-products[1]**2-90*a*c)<mp.mpf('1e-65')

# Same 4-caustic for rhombus and coordinate rectangle: falsifies dropping parity.
alpha=a*a/mp.sqrt(a*a+b*b); beta=b*b/mp.sqrt(a*a+b*b)
rhombus=[[a,0],[0,b],[-a,0],[0,-b]]
rectangle=[[alpha,beta],[-alpha,beta],[-alpha,-beta],[alpha,-beta]]
four=[mp.fprod(distance(p,[c,0]) for p in vertices) for vertices in [rhombus,rectangle]]
assert abs(four[0]-105)<mp.mpf('1e-65')
assert abs(four[1]-mp.mpf(11025)/121)<mp.mpf('1e-65')
result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'diagnostic_only':True,'mpmath_version':mp.__version__,'precision_digits':mp.mp.dps,'primitive_cases':len(rows),'phases_per_case':len(phases),'primitive_case_results':rows,'repeated_odd_control':{'outer_axes_squared':[15,7],'caustic_axes_squared':['135/16','7/16'],'primitive_product_values':[fmt(x) for x in products],'repeated_six_product_values':[fmt(x*x) for x in products],'exact_repeated_difference':'90 sqrt(15) sqrt(8) = 180 sqrt(30)'},'N_divisible_by_four_control':{'outer_axes_squared':[15,7],'caustic_axes_squared':['225/22','49/22'],'rhombus_product':'105','rectangle_product':'11025/121'}}
Path('geometry_check_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'primitive_cases':len(rows),'phases_per_case':len(phases),'max_residual':max(mp.mpf(row['max_residual']) for row in rows).__str__(),'exact_control_repeated6_difference':result['repeated_odd_control']['exact_repeated_difference'],'all_diagnostics_passed':True},indent=2))
