#!/usr/bin/env python3
"""Independent exact controls; no author/checker imports, no third-party data."""
import datetime, fractions, itertools, json, math, pathlib, platform, sys
from fractions import Fraction as F

BASE = pathlib.Path(__file__).resolve().parent
assertions = 0

def check(condition, message):
    global assertions
    assertions += 1
    if not condition:
        raise AssertionError(message)

def multiplicity(elements):
    coeff = [1]
    for n in elements:
        old = coeff
        coeff = old + [0] * n
        for s, v in enumerate(old):
            coeff[s+n] += v
    return max(coeff), coeff

def direct(elements):
    counts = {}
    for bits in itertools.product((0, 1), repeat=len(elements)):
        s = sum(x*b for x,b in zip(elements, bits))
        counts[s] = counts.get(s, 0) + 1
    return max(counts.values())

def enumerate_control(D):
    accum = {q: {"moment": F(0), "weight": F(0), "weighted_S": F(0), "pigeonhole": F(0)} for q in (1,2,3,4)}
    total = F(0)
    max_m = 0
    by_N = {}
    for bits in itertools.product((0,1), repeat=D-1):
        B = [1] + [n for n,b in zip(range(2,D+1), bits) if b]
        product_odds = math.prod(n-1 for n in B if n > 1)
        prob = F(1, D*product_odds)
        direct_prob = F(1)
        for n,b in zip(range(2,D+1), bits):
            direct_prob *= F(1,n) if b else F(n-1,n)
        check(prob == direct_prob, f"configuration product D={D} B={B}")
        M, coeff = multiplicity(B)
        N,S = len(B),sum(B)
        check(sum(coeff) == 2**N, "all subsets counted")
        check(coeff == coeff[::-1], "complement symmetry")
        check(M*(S+1) >= 2**N, "pigeonhole")
        check(1 <= M <= 2**N, "trivial limits")
        if D <= 10:
            check(M == direct(B), "direct enumeration independently agrees")
        total += prob
        by_N[N] = by_N.get(N,F(0)) + prob
        max_m = max(max_m,M)
        for q in accum:
            weight = prob * (2**q)**N
            accum[q]["moment"] += prob*M**q
            accum[q]["weight"] += weight
            accum[q]["weighted_S"] += weight*S
            accum[q]["pigeonhole"] += weight/F(S+1)**q
    check(total == 1, "configuration probabilities sum exactly to one")
    rows=[]
    for q,v in accum.items():
        t=2**q
        Z=math.prod(F(n+t-1,n) for n in range(1,D+1))
        tilted_S=sum((F(t*n,n+t-1) for n in range(1,D+1)),F(0))
        jensen=Z/(1+tilted_S)**q
        coarse=Z/F(1+t*D)**q
        check(v["weight"] == Z,"partition function")
        check(v["weighted_S"] == Z*tilted_S,"tilted mean exact identity")
        check(v["moment"] >= v["pigeonhole"] >= jensen >= coarse,"exact moment inequality chain")
        if q==2:
            check(Z == F((D+1)*(D+2)*(D+3),6),"q2 telescope")
        rows.append({"q":q,"exact_E_Mq":str(v["moment"]),"exact_Z":str(Z),"exact_tilted_E_S":str(tilted_S),"exact_pigeonhole_expectation":str(v["pigeonhole"]),"exact_jensen_lower":str(jensen),"exact_coarse_lower":str(coarse),"moment_to_coarse_ratio":float(v["moment"]/coarse)})
    return {"D":D,"configurations":2**(D-1),"total_probability":str(total),"max_realized_M":max_m,"rows":rows,"count_distribution":{str(k):str(v) for k,v in by_N.items()}}

def edge_controls():
    for B in ([],[1],[7],[1,2],[1,2,3],[1,2,4,8],[2,5,7,12],[1,3,6,9,12]):
        M,c=multiplicity(B)
        check(M==direct(B),"edge DP/direct match")
        check(M*(sum(B)+1)>=2**len(B),"edge pigeonhole")
    # Refute a reverse multiplicative bound: disjoint singleton components
    # each have maximum 1, but their union [1,2,3] has maximum 2.
    check(multiplicity([1,2,3])[0] == 2,"cross-component collision")
    check(math.prod(multiplicity([n])[0] for n in [1,2,3]) == 1,"singleton components")
    # Tail-to-moment controls are exact with D and integer exponents.
    rows=[]
    for D in (4,16,256,65536):
        r,s,q=1,2,2
        rare=F(1,D**r)
        mean=(1-rare)+rare*D**(s*q)
        check(mean >= D**3,"polynomial moment despite rare peaks")
        rows.append({"D":D,"rare_probability":str(rare),"E_Y2":str(mean),"E_log_Y":float(rare*s*math.log(D)),"P_nonzero_log_normalized":str(rare)})
    # Explicit logarithmic uniform-integrability counterexample:
    # Y_D = D^D with probability 1/D, else 1. Then normalized log Y_D
    # tends to zero in probability but its expectation grows without bound.
    ui_rows=[]
    for D in (4,16,256,65536):
        z_on_rare=D*math.log(D)/math.log(math.log(D))
        ui_rows.append({"D":D,"rare_probability":str(F(1,D)),"lognormalized_on_rare":z_on_rare,"E_lognormalized":z_on_rare/D})
    return {"raw_moment_counterexample":rows,"log_UI_counterexample":ui_rows}

def main():
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    results=[enumerate_control(D) for D in (1,2,3,4,5,6,8,10,12,14)]
    edges=edge_controls()
    output={"started_utc":start,"ended_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"python":sys.version,"platform":platform.platform(),"independent_of_author_code":True,"exact_assertions":assertions,"cutoff_results":results,"controls":edges,"interpretation":"Finite controls check identities and counterexamples only; universal proofs and infinite probability conclusions are in the written review."}
    (BASE/"INDEPENDENT_CONTROLS.json").write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({"exact_assertions":assertions,"cutoffs":[x["D"] for x in results],"configurations":sum(x["configurations"] for x in results),"success":True},indent=2))

if __name__=="__main__":
    main()
