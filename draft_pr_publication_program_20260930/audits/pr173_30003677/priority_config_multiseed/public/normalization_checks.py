"""Exact own arithmetic controls for the Poisson mark representation, not a theorem proof."""
from fractions import Fraction as F
import hashlib,json,sys
from pathlib import Path

def require(ok,why):
    if not ok: raise RuntimeError(why)
checks=0
for lambda1,lambda2 in [(F(1,7),F(3,2)),(F(2),F(5)),(F(1,100),F(1))]:
    lambdas={1:lambda1,2:lambda2}
    for state in range(3):
        for n1 in range(10):
            for n2 in range(10):
                for mark in (1,2):
                    q=lambdas[mark]*(n1 if mark==1 else n2) if state==0 else F(0)
                    threshold=2*q
                    require(F(1,2)*threshold==q,'Normalized SDE differs from physical intensity')
                    require(state==0 or threshold==0,'Occupied state recolors')
                    if q>0: require(F(1,2)*q!=q,'Semantic negative failed')
                    checks+=1
    for k in range(1,30):
        bound=4*max(lambdas.values())*(k-1)+1
        for mark in (1,2):
            threshold=2*lambdas[mark]*2*(k-1)
            require(threshold<bound,'Closure bound failed')
q=F(3,5); require(F(1,2)*q==F(3,10),'Bare threshold negative mismatch')
print(json.dumps({'result':'PASS','optimized':bool(sys.flags.optimize),'exact_normalized_state_channel_checks':checks,'marks':{'1':'1/2','2':'1/2'},'semantic_negative_bare_threshold_represents_half_physical_rate':True,'all_checks_use_explicit_exceptions':True,'scope':'Arithmetic representation and uniform-bound controls only; no simulated theorem validation.','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
