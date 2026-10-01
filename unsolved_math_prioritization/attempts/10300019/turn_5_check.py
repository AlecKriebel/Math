"""Exact holonomy-orbit and failed-interpolation diagnostics."""
from fractions import Fraction as Q
from collections import Counter
import json
C=Counter()
f=lambda t:t/(2-t)
def tn(n):return 1/(1+Q(2)**n)
for n in range(-100,101):
 assert f(tn(n))==tn(n+1);C['shift_holonomy']+=1
 assert 0<tn(n+1)<tn(n)<1;C['ordered_compact_orbit']+=1
for n in range(1,101):
 assert tn(n)<Q(1,2)**n and 1-tn(-n)<Q(1,2)**n;C['endpoint_limits_bound']+=1
F=lambda t:(t*t+t)/2
G=lambda t:(t**4+t)/2
x=Q(1,2)
assert F(G(x))==Q(369,2048) and G(F(x))==Q(1617,8192);C['exact_compositions']+=1
assert F(G(x))-G(F(x))==Q(-141,8192);C['commutator_nonzero']+=1
X=[Q(i,100) for i in range(101)]
for u in [Q(i,20) for i in range(21)]:
 H=lambda t:(1-u)*t*t+u*t
 for a,b in zip(X,X[1:]):assert H(a)<H(b);C['homeomorphism_path_strict_order']+=1
assert f(Q(0))==0 and f(Q(1))==1;C['fixed_endpoints']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Exact orbit/interpolation identities. No-full-support-measure, normal suspension realization and general source limitations are analytical statements, not inferred from finite sampling.'},indent=2))
