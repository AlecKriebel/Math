#!/usr/bin/env python3
"""Check the PR126 substitution into the published BKL n=3 band relation.
This is a verification artifact, not evidence of historical first application.
No assert statements: false input remains rejected under python -O.
"""
import datetime, hashlib, json, os
from pathlib import Path

def check(condition, label):
    if not condition:
        raise RuntimeError(label)

def mul(x,y):
    return tuple(tuple(sum(x[i][k]*y[k][j] for k in range(2)) for j in range(2)) for i in range(2))

def inv(x):
    check(x[0][0]*x[1][1]-x[0][1]*x[1][0] == 1, "SL2 determinant")
    return ((x[1][1],-x[0][1]),(-x[1][0],x[0][0]))

def power(x,n):
    out=((1,0),(0,1))
    for unused in range(n): out=mul(out,x)
    return out

A=((3,1),(2,1)); B=((1,-2),(-1,3)); C=((8,-11),(3,-4))
X=((0,1),(-1,0)); Y=((-2,-1),(3,1))
check(power(X,2)==((-1,0),(0,-1)), "source X squared")
check(power(Y,3)==((1,0),(0,1)), "source Y cubed")
check(mul(X,Y)==A and mul(Y,X)==B, "source pair binding")
check(mul(mul(A,B),inv(A))==C, "BKL definition binding")
check(mul(mul(inv(B),A),B)==C, "equivalent conjugate binding")
common=mul(A,B)
check(common==mul(C,A)==mul(B,C), "published band relation images")

# Each step replaces exactly one adjacent pair with an equal pair from
# BKL Eq.(8), after a32->a, a21->b, a31->c: ab=ca=bc.
relation={"ab","ca","bc"}
chains=[
    ["aba","bca","bab"],
    ["aca","aab"], ["cac","abc","aab"],
    ["bcb","abb"], ["cbc","cab","abb"],
]
def step_ok(old,new):
    if len(old)!=len(new): return False
    for i in range(len(old)-1):
        if old[i:i+2] in relation and new[i:i+2] in relation:
            if old[:i]==new[:i] and old[i+2:]==new[i+2:]: return True
    return False
for chain in chains:
    for old,new in zip(chain,chain[1:]): check(step_ok(old,new), "invalid rewrite")
check(not step_ok("aba","aaa"), "false rewriting control must fail")
wrong=mul(mul(inv(A),B),A)
check(wrong != C, "wrong orientation control unexpectedly equal")
check(not (mul(A,B)==mul(wrong,A)==mul(B,wrong)), "wrong band binding must fail")
for i,x in enumerate((A,B,C)):
    inv(x)
    check(x[0][0]+x[1][1]==4, "hyperbolic source image trace")
    for y in (A,B,C)[i+1:]:
        check(x != y and mul(x,y)!=mul(y,x), "distinct image / noncommuting")
        check(mul(mul(x,y),x)==mul(mul(y,x),y), "pairwise image braid")

result={
    "schema":"pr126-published-band-substitution-check/v1",
    "UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "actual_operator_PID":os.getpid(),
    "original_head":"a1df84a64fa96d53f3a8c6fec9db8bc48bd1533c",
    "published_source":"Birman-Ko-Lee (1998), definition Eq.(4) p.325; Proposition2.1 Eq.(8) p.327",
    "substitution":{"sigma2":"A","sigma1":"B","a32":"A","a21":"B","a31":"C"},
    "band_relation_images":common,
    "symbolic_rewrite_chains":chains,
    "all_checks_passed":True,
    "negative_controls":["false word substitution rejected","opposite-conjugation band-generator binding rejected"],
    "proof_limits":"Finite matrices confirm source binding; symbolic equalities and cancellation prove arbitrary-group consequence. No first-application priority is inferred.",
    "original_effort":"1/5", "new_central_proof_search_turns":0,
}
print(json.dumps(result,indent=2))
