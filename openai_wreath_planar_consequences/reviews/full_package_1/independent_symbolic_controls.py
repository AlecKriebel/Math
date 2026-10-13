"""Exact, separately derived Laurent and normalization consistency controls.
Not a global sign or group existence certificate. Standard-library only.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,datetime,hashlib
# Pair (a,b) denotes a+b*i*sqrt(3). It is a field under the following rules.
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def mul(x,y):return (x[0]*y[0]-3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def conj(x):return (x[0],-x[1])
def pmul(a,b):
 out={}
 for j,x in a.items():
  for k,y in b.items():out[j+k]=add(out.get(j+k,(Q(0),Q(0))),mul(x,y))
 return {j:x for j,x in out.items() if x!=(0,0)}
# c=cos(pi*(s-2)/6), w=exp(i*pi*s/6), r=exp(-i*pi/3).
r=(Q(1,2),Q(-1,2));t=mul(r,r)
a={2:t,0:(Q(-1),Q(0)),-2:conj(t)} # 4c^2-3
b={0:(Q(1),Q(0)),1:(-r[0],-r[1]),-1:(-r[0],r[1])} # 1-2c
poly=pmul(pmul(a,a),pmul(b,b))
expected=[(Q(5),Q(0)),(Q(-1),Q(1)),(Q(1),Q(1)),(Q(-2),Q(0)),(Q(-1,2),Q(1,2)),(Q(-1),Q(-1)),(Q(1),Q(0))]
assert all(poly[j]==expected[j] for j in range(7))
assert all(poly[-j]==conj(expected[j]) for j in range(1,7))
# Inverse reconstruction bound and strict continuum margins, all exact fractions.
finite=max(Q(32)+(1+Q(37,10))*Q(11,100)*32/(1-Q(687,1000)),(1+Q(37,10))/(1-Q(687,1000)))
assert finite<90
residual_error=2*(91*Q(11,10**8)+2540*(Q(229,100)*Q(5,10**10)+Q(17,1000)*Q(32,10**9)))
assert residual_error==Q(715003,25000000000) and residual_error<Q(3,10**5)
margin=Q(11,1000)*Q(68,100)-Q(6,1000)/2
assert margin==Q(448,100000)>0
# Both Schur-complement signs cancel eta^2 in the cross term; the tail gain is tiny.
tail_defect=Q(5,10**10)*(1+90*28)
assert tail_defect<1
finite_coefficient=90+2521*90*Q(5,10**10)/(1-tail_defect)
tail_coefficient=Q(2521)/(1-tail_defect)
assert finite_coefficient<91 and tail_coefficient<2540
out={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_INDEPENDENT_EXACT_SYMBOLIC_CONTROLS','P_Laurent_coefficients_verified':13,'finite_inverse_bound':str(finite),'exact_coefficient_error':str(residual_error),'global_tail_margin':str(margin),'whole_inverse_finite_coefficient':str(finite_coefficient),'whole_inverse_tail_coefficient':str(tail_coefficient),'scope':'Algebraic identities and rational consistency margins only; not the finite matrix/residual/Bernstein integrals, infinite proof, or probabilistic group construction.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix('.receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
