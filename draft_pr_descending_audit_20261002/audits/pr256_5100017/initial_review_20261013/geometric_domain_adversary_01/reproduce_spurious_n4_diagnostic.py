"""Forensic reproduction of an initially mistaken near-d=0 regime diagnostic.
This intentionally applies a star zero-circle rule to an approximate N4 closure.
It is not an admissible exact counterexample and does not test a true zero circle.
"""
import json
from pathlib import Path
import geometric_audit as g
m=g.m;m.mp.dps=80
a=m.mpf('1.8');b=m.mpf(1);N=4
lo=m.mpf('1e-70');hi=1-lo
for _ in range(240):
    mid=(lo+hi)/2
    if g.orbit(a,b,mid,N,0)[-1]>2*m.pi:hi=mid
    else:lo=mid
L=(lo+hi)/2
H=(a*a+b*b)/2;e=(a*a-b*b)/2;d=1-L*(1/(a*a)+1/(b*b));F=H*d+2*L
assert d<0
rho=m.sqrt(-2*F/d)
P=g.orbit(a,b,L,N,0)[0]
S0=g.direct(P,a,b,m.mpf(0),m.mpf(0))[0]
actual=g.direct(P,a,b,rho,m.mpf(0))[0]
G=2*F+d*rho*rho
res=(actual-S0*G/(2*F))/(1+abs(S0)+abs(actual))
result={'status':'EXPECTED_DIAGNOSTIC_FAILURE','mp_digits':m.mp.dps,'approximate_lambda':m.nstr(L,80),'lambda_error_against_exact_four_period_value':m.nstr(L-a*a*b*b/(a*a+b*b),25),'spurious_negative_d':m.nstr(d,25),'fictitious_radius':m.nstr(rho,25),'S0':m.nstr(S0,25),'direct_signed_area_at_fictitious_circle_point':m.nstr(actual,25),'normalized_area_formula_residual':m.nstr(res,25),'original_bad_branch':'if d<0: add sqrt(-2F/d) as an exact zero-circle point','why_it_is_not_a_counterexample':'The computed lambda is merely an approximate closure parameter, while exact least-period four has d=0. Its O(1e-74) closure/parameter error is amplified by a fictitious M of size O(1e37). The theorem assumes exact closure, and no true exceptional circle exists for N=4.','correction':'Use the exact algebraic N4 classification d=0; in finite diagnostics do not classify tiny sign noise near that known boundary as a genuine star regime. The corrected independent controls separate |d|<1e-45 from d<-1e-45 and use ordinary finite M in the N4 boundary control.'}
Path('SPURIOUS_N4_DIAGNOSTIC.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
