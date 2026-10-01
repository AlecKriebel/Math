"""Exact controls for the descending-cluster algorithm; no imported author code."""
from fractions import Fraction
from itertools import combinations,product
import json

def sign(x):return (x>0)-(x<0)
def compare(p,q,terms):
    assert p>q>0
    ts={}
    for e,a in terms:ts[e]=ts.get(e,0)+a
    ts=sorted(((e,a) for e,a in ts.items() if a),reverse=True)
    if not ts:return 0,{'width':0,'merges':0,'cuts':0,'resets':0}
    A=sum(abs(a) for e,a in ts);B=A.bit_length();Q=(q-1).bit_length()
    c=1
    while p**c<2*q**c:c+=1
    v,R=ts[0];W=0;maxW=0;merges=cuts=resets=0
    for e,a in ts[1:]:
        d=v-e
        if R==0:R=a;W=0;v=e;resets+=1;continue
        if d>=c*(B+Q*W+1):cuts+=1;return sign(R),{'width':maxW,'merges':merges,'cuts':cuts,'resets':resets}
        R=R*p**d+a*q**(W+d);W+=d;v=e;merges+=1;maxW=max(maxW,W)
        assert abs(R)<=A*p**W
        bound=c*(B+1)*sum((1+c*Q)**j for j in range(len(ts)-1))
        assert W<bound
    return sign(R),{'width':maxW,'merges':merges,'cuts':cuts,'resets':resets}

count=0;max_width=0;cuts=0;resets=0
for p,q in ((2,1),(3,2),(5,3),(5,4),(9,4)):
    alpha=Fraction(p,q)
    for m in range(1,5):
        for exps in combinations(range(7),m):
            for cs in product((-2,-1,1,2),repeat=m):
                val=sum((a*alpha**e for a,e in zip(cs,exps)),Fraction(0))
                out,stats=compare(p,q,list(zip(exps,cs)))
                assert out==sign(val)
                count+=1;max_width=max(max_width,stats['width']);cuts+=stats['cuts'];resets+=stats['resets']
# Gaps given by huge binary integers: exact zero blocks must be skipped.
E=10**100
large=[]
for p,q in ((3,2),(5,4),(2,1)):
    cases=[([(0,1),(E,-p),(E+1,q)],1), ([(0,-1),(E,-p),(E+1,q)],-1), ([(0,-p),(1,q),(E,-p),(E+1,q)],0), ([(0,-1),(E,1)],1)]
    for terms,want in cases:
        got,stats=compare(p,q,terms);assert got==want;count+=1
        large.append({'p':p,'q':q,'answer':got,**stats})
# Exact form of a worst-case *bound*, not an assertion of actual worst-case inputs.
for c in range(1,8):
    for Q in range(0,5):
        for B in range(1,9):
            W=0
            for m in range(1,12):
                W=(1+c*Q)*W+c*(B+1)
                assert W==c*(B+1)*sum((1+c*Q)**j for j in range(m));count+=1
print(json.dumps({'status':'PASS','exact_assertions_and_instances':count,'finite_test_max_expanded_width':max_width,'finite_test_gap_cuts':cuts,'finite_test_zero_resets':resets,'large_gap_cases':large,'limitations':'Checks the proved fixed-base FPT algorithm and the integer-base polynomial branch. It does not prove polynomial dependence on the variable term count for noninteger rational bases.'},indent=2))
