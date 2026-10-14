#!/usr/bin/env python3
"""Fresh exact adversarial controls; finite checks do not prove universal claims."""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import json

counts = Counter()
def check(value, label):
    if not value:
        raise AssertionError(label)
    counts[label] += 1
def mul(z,w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])
def add(z,w):
    return (z[0]+w[0],z[1]+w[1])
def sub(z,w):
    return (z[0]-w[0],z[1]-w[1])
def dot(z,w):
    return sum((a*b for a,b in zip(z,w)), F(0))
def sq(z):
    return dot(z,z)
def matvec(a,x):
    return [dot(row,x) for row in a]

# Chart necessity from exact pairs of arbitrary stable roots, including boundaries.
for r in [F(0),F(1,7),F(2)]:
 for s in [F(0),F(1,11),F(3)]:
  for p in [F(-2),F(0),F(2,9)]:
   for q in [F(-3,5),F(0),F(4)]:
    root1=(-r,p);root2=(-s,q)
    a=tuple(-u for u in add(root1,root2));b=mul(root1,root2)
    x,y=a;u,v=b
    U=u+y*y/4; V=v-x*y/2
    check(U==r*s+(p-q)**2/4,'closed_chart_U_identity')
    check(V==(r-s)*(p-q)/2,'closed_chart_V_identity')
    check(x*x*U-V*V==r*s*((r+s)**2+(p-q)**2),'closed_chart_exact_slack')
    check(x>=0 and U>=0 and V*V<=x*x*U,'stable_root_chart_membership')

# Dropping U>=0 at the x=0 boundary would falsely include w²-1.
x,U,V=F(0),F(-1),F(0)
check(V*V<=x*x*U and U<0,'squaring_without_nonnegative_rhs_is_false')
check((F(1),F(0))[0]>0,'dropped_edge_condition_has_positive_root')

# The classical normalized quartic boundary and quadratic umbrella are smoothly related.
for a1,a3 in [(F(1,100),F(1,100)),(F(1,80),F(1,100)),(F(2,100),F(1,100))]:
 a2=(a1*a1+a3*a3)/(a1*a3)
 xx=(a1+a3)/2;vv=(a1-a3)/2;uu=(a2-2)/(a2+2)
 check(vv*vv==xx*xx*uu,'quartic_to_umbrella_chart_identity')

# SPD matrices are constructed as A^T A plus a strictly positive diagonal.
# Include high conditioning and coefficient-height cross terms, not diagonal-only metrics.
metric_rows=[]
for d in [4,6,5,7]:
 for exponent in [0,8,40,80]:
  A=[[F((i+1)*(j+2)%7-3,5) for j in range(d)] for i in range(d)]
  A[-1][0]=F(2**exponent)
  height=(d in [5,7]);full=(d in [6,7]);idx=5 if full else 3
  if height:
   A[0][idx]=F(10);A[0][-1]=F(10)
  diag=[F(1,2**exponent) if i%2 else F(2**exponent) for i in range(d)]
  G=[[sum((A[k][i]*A[k][j] for k in range(d)),F(0))+(diag[i] if i==j else F(0)) for j in range(d)] for i in range(d)]
  e=[F(0)]*d;f=[F(0)]*d
  e[2 if full else 0]=F(1);e[4 if full else 2]=F(1);f[idx]=F(1)
  check(dot(e,matvec(G,e))>0,'positive_leading_coefficient_non_diagonal_metric')
  if height:
   check(G[idx][-1]!=0,'actual_coefficient_height_mixing')
  tau=F(1,2**(exponent+4))
  for j in range(1,400):
   t=F(1,2**j);w=[t*t*e[i]+t**3*f[i] for i in range(d)]
   Q=dot(w,matvec(G,w))
   expansion=t**4*(dot(e,matvec(G,e))+2*t*dot(e,matvec(G,f))+t*t*dot(f,matvec(G,f)))
   check(Q==expansion,'exact_SPD_metric_path_expansion')
   if Q-2*tau*t**3<0:
    check(Q>0,'positive_path_norm_at_distance_improvement')
    metric_rows.append({'dimension':d,'conditioning_exponent':exponent,'tau':str(tau),'first_dyadic_t':str(t),'squared_distance_difference':str(Q-2*tau*t**3)})
    break
  else:
   raise AssertionError('no improvement found in stress search')

# Exact adverse curvature at D=0, with positive q and a purely imaginary displacement.
for M in [F(1),F(10),F(10000)]:
 for tau in [F(1,100),F(1,10**6),F(1,10**12)]:
  da=(F(0),tau);db=(-tau*tau/4,F(0));q=(M,F(0))
  check(sub(mul(da,da),tuple(4*x for x in db))==(F(0),F(0)),'zero_discriminant_adverse_curvature')
  deficit=-dot(tuple(-2*x for x in q),db)
  check(deficit==-M*tau*tau/2,'adverse_curvature_sign')
  d2=sq(da)+sq(db)
  check(deficit+M*d2/2==M*tau**4/32,'sharp_M_curvature_slack')
  check(deficit+(M+1)*d2/2>d2/2,'strict_definition_M_plus_one')

out={'status':'PASS','arithmetic':'fractions.Fraction, independent standard-library code',
     'assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),
     'SPD_stress_cases':metric_rows,
     'scope':'Finite independent controls only; no explicit nearest-point tie is computed and no universal theorem is inferred from samples.'}
path=Path(__file__).resolve().parent/'INDEPENDENT_ADVERSARIAL_CONTROLS.json'
path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':out['status'],'assertions':out['assertions'],'counts':out['counts'],'SPD_stress_cases':len(metric_rows)},indent=2,sort_keys=True))
