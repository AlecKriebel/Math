#!/usr/bin/env python3
"""Finite controls from full-path transition probabilities; no candidate imports."""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
import json
import sys

fault = sys.argv[1] if len(sys.argv) > 1 else "none"
receipts = []
def require(label, truth, **facts):
    rec = {"label": label, "pass": bool(truth), **facts}
    receipts.append(rec)
    print(json.dumps(rec, sort_keys=True), flush=True)
    assert truth, label

def full_law(N):
    result = {}
    for path in product((0, 1), repeat=N+1):
        weight = Q(1, 2)
        for k in range(N):
            p = Q(1, k+2)
            if fault == "shift_reset":
                p = Q(1, 2)
            weight *= p if path[k] != path[k+1] else 1-p
        result[path] = weight
    return result

def marginal(law, indices):
    out = defaultdict(Q)
    for path, w in law.items():
        out[tuple(path[k] for k in indices)] += w
    return dict(out)

for N in range(0, 9):
    law = full_law(N)
    require("full_mass", sum(law.values()) == 1, N=N)
    require("last_fair", sum(w for x,w in law.items() if x[N]) == Q(1,2), N=N)
    for start in range(N+1):
        window = marginal(law, range(start,N+1))
        r = N-start
        constants = {(0,)*(r+1), (1,)*(r+1)}
        target = {x:Q(1,2) for x in constants}
        tv = sum(abs(w-target.get(x,Q(0))) for x,w in window.items())/2
        expected = Q(r,N+1)
        if fault == "window_index" and r:
            expected = Q(r,N+2)
        require("coherent_window_tv", tv == expected, N=N, start=start,
                measured=str(tv), expected=str(expected))
    for m in range(N):
        mass = defaultdict(Q)
        moment = defaultdict(Q)
        for x,w in law.items():
            prefix = x[:m+1]
            mass[prefix] += w
            moment[prefix] += (2*x[N]-1)*w
        rho = Q(m*(m+1),N*(N+1))
        if fault == "correlation_index":
            rho = Q((m+1)*(m+2),N*(N+1))
        for prefix in sorted(mass):
            require("all_history_conditional_moment",
                    moment[prefix] == (2*prefix[-1]-1)*rho*mass[prefix],
                    N=N,m=m,prefix=prefix, measured=str(moment[prefix]))
        optimum = sum(abs(v) for v in moment.values())
        extremal_mean = sum((2*x[-1]-1)*w for x,w in mass.items())
        require("sharp_fair_finite_joining_bound",
                optimum == rho and extremal_mean == 0,
                N=N,m=m,optimal_correlation=str(optimum))

# This specific stationarity assertion is false: source permits nonstationary X.
if fault == "stationary":
    law = full_law(2)
    require("X_joint_stationary", marginal(law,(0,1)) == marginal(law,(1,2)))

# Fixed-n maximal marginal coupling exists, but one fixed B cannot follow n and 2n.
for n in range(1,21):
    rho=Q(n*(n+1),2*n*(2*n+1))
    q=(1-rho)/2
    require("two_time_no_single_B", q == Q(3*n+1,4*(2*n+1)) and q >= Q(1,3),
            n=n,mismatch=str(q),joining_lower_bound=str(q/2))
    for s in range(0,12):
        q=Q(0) if s==0 else (1-Q(n*(n+1),(n+s)*(n+s+1)))/2
        require("dependent_offset_union_ingredient",
                q <= Q(s,n+s+1) <= Q(s,n+1), n=n,s=s,mismatch=str(q))
for length in range(1,8):
    weights=[Q(1,2**(j+1)) for j in range(length)]
    for x in product((0,1),repeat=length):
        for b in (0,1):
            D=sum(w*(a!=b) for w,a in zip(weights,x))
            I=(x[0]!=b)*sum(weights)
            bound=sum(weights[j]*(x[j]!=x[0]) for j in range(length))
            require("arbitrary_B_metric_pointwise",abs(D-I)<=bound,length=length,x=x,b=b)
print(json.dumps({"status":"PASS","checks":len(receipts),"fault":fault,
    "scope":"Finite coherent path, sharp finite-history joining and metric checks only. Universal infinite joinings require the written density argument."}))

