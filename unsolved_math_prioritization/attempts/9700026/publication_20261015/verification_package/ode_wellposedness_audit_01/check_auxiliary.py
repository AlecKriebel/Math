#!/usr/bin/env python3
"""Exact arithmetic checks of ODE auxiliary identities, not a proof of area regularity."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(ok, msg):
    if not ok:
        raise RuntimeError(msg)


def norm2(v):
    return sum(x*x for x in v)


def sub(a,b):
    return tuple(x-y for x,y in zip(a,b))


def gradient_identity(a,b,y,t):
    aa, bb = sub(y,a), sub(y,b)
    f = norm2(aa)-t*norm2(bb)
    grad = tuple(2*(u-t*v) for u,v in zip(aa,bb))
    lhs = norm2(grad)
    rhs = 4*(t*norm2(sub(a,b))+(1-t)*f)
    return lhs == rhs


scenarios = {
    "ordinary": ((F(1,5),F(1,4)), (F(3,4),F(1,3))),
    "collinear": ((F(1,4),F(1,2)), (F(3,4),F(1,2))),
    "close_sites": ((F(1,2),F(1,2)), (F(500001,1000000),F(1,2))),
    "near_boundary": ((F(1,1000000),F(1,1000000)), (F(999999,1000000),F(1,1000000))),
}
weights = [F(1,10**12), F(1,64), F(1,2), F(999999,1000000),
           F(1), F(1000001,1000000), F(2), F(64), F(10**12)]
y_values = [(F(i,4),F(j,4)) for i in range(5) for j in range(5)]
identity_count = 0
for name,(a,b) in scenarios.items():
    require(a != b, "sites must differ")
    for t in weights:
        for y in y_values:
            require(gradient_identity(a,b,y,t), "gradient identity failed: "+name)
            identity_count += 1

# Validate the uniform whole-strip gradient deduction with exact inequalities.
strip_cases = 0
for name,(a,b) in scenarios.items():
    d2=norm2(sub(a,b))
    for m,M in [(F(1,64),F(64)),(F(999999,1000000),F(1000001,1000000)),(F(1),F(1))]:
        H=max(F(1),abs(1-m),abs(1-M))
        eps=m*d2/(2*H)
        for t in [m,(m+M)/2,M]:
            for f in [-eps,F(0),eps]:
                require(4*(t*d2+(1-t)*f) >= 2*m*d2,"strip gradient lower bound failed")
                strip_cases += 1

# Pairwise test changes imply a strip inclusion. The grid only checks algebra;
# the proof in REPORT.md handles all y and all nearby weights.
sign_change_cases = 0
for a,b in scenarios.values():
    for t in weights:
        for s in weights:
            for y in y_values:
                f=norm2(sub(y,a))-t*norm2(sub(y,b))
                g=norm2(sub(y,a))-s*norm2(sub(y,b))
                require(abs(f-g) <= 2*abs(t-s),"parameter perturbation bound failed")
                if (f <= 0) != (g <= 0):
                    require(abs(f) <= 2*abs(t-s),"changed sign not in strip")
                    sign_change_cases += 1

# Rational witness constants. These do not numerically integrate a trajectory.
sites=[(F(1,5),F(1,4)),(F(3,4),F(1,3)),(F(2,5),F(4,5))]
z=[F(1,6),F(1,3),F(1,2)]
h=F(1,16)
p=F(1,2)
K=4*h*h
lower=K*K
require(sum(z)==1 and all(v>lower for v in z),"initial-state condition failed")
require(all(min(*a,*(1-x for x in a))>h for a in sites),"square interior condition failed")
d2s=[norm2(sub(sites[i],sites[j])) for i in range(3) for j in range(i+1,3)]
require(all(d>8*h*h for d in d2s),"site separation condition failed")
require(K==F(1,64) and lower==F(1,4096),"comparison constants failed")
require(1-2*lower==F(2047,2048),"upper bound failed")

# Natural zero-state extension can have nonuniqueness when p<1.
# At t=lambda<=1/64 in the two-site horizontal example, disk center displacement
# <=1/126 and radius<=4/63. These rational bounds put the disk strictly inside Q.
require(F(1,4)-F(1,126)-F(4,63)>0,"small disk left containment failed")
require(F(1,4)+F(4,63)<1,"small disk right containment failed")
require(F(1,2)-F(4,63)>0 and F(1,2)+F(4,63)<1,"small disk vertical containment failed")

manifest_path=ROOT/'SOURCE_MANIFEST.json'
manifest_bytes=manifest_path.read_bytes()
manifest=json.loads(manifest_bytes)
require(hashlib.sha256(manifest_bytes).hexdigest()=="b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b","source manifest pin failed")
require(len(manifest['files'])==40,"source member count failed")
verified_inputs=[]
for relative in ['author/PROOF.md','audit_a/AUDIT_REPORT.md','audit_a/ACCEPTANCE.json','review_b/REVIEW_B.md','review_b/ACCEPTANCE_B.json']:
    entry=next(x for x in manifest['files'] if x['path']==relative)
    data=(ROOT/'source'/relative).read_bytes()
    digest=hashlib.sha256(data).hexdigest()
    require(len(data)==entry['bytes'] and digest==entry['sha256'],"input pin failed: "+relative)
    verified_inputs.append({'path':relative,'bytes':len(data),'sha256':digest})

result={
    'schema':'pr880-ode-auxiliary-checks-v1',
    'result':'PASS',
    'exact_gradient_identities':identity_count,
    'exact_whole_strip_gradient_cases':strip_cases,
    'exact_pairwise_sign_change_cases':sign_change_cases,
    'geometric_scenarios':list(scenarios),
    'lambda_cases':[str(x) for x in weights],
    'witness_squared_distances':[str(x) for x in d2s],
    'witness_lower_bound':str(lower),
    'witness_upper_bound':str(1-2*lower),
    'verified_inputs':verified_inputs,
    'limitations':'Finite algebra checks corroborate identities and rational constants only. They do not prove area regularity, ODE continuation, or all-time persistence; REPORT.md supplies those analytic arguments. No floating-point simulation is used.'
}
(HERE/'AUXILIARY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['verified_inputs','lambda_cases']},indent=2))
