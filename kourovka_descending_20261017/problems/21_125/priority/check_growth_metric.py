#!/usr/bin/env python3
"""Exact sanity checks for the source-contract growth-metric example.
The proof for all n is in GROWTH_METRIC_SCOPE.md; this finite check is not a proof
of virtual non-specialness, which is the cited prior theorem of Brady--Soroko.
"""
from pathlib import Path
import hashlib,json

def red(w):
    z=[]
    for x in w:
        if z and z[-1]==-x:z.pop()
        else:z.append(x)
    return tuple(z)
def inv(w):return tuple(-x for x in w[::-1])
def apply(w,images):return red(y for x in w for y in (images[x] if x>0 else inv(images[-x])))
def cyc(w):
    w=red(w)
    while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
    return len(w)
alpha={1:(1,),2:(2,1),3:(3,1,1)}
phi={x:red((2,)+alpha[x]+(-2,)) for x in alpha}
state={x:(x,)for x in alpha}
rows=[]
for n in range(61):
    pn=tuple(x for j in range(n) for x in ((2,)+(1,)*j))
    alpha_n={1:(1,),2:(2,)+(1,)*n,3:(3,)+(1,)*(2*n)}
    assert all(state[x]==red(pn+alpha_n[x]+inv(pn)) for x in state)
    lengths=[len(state[x]) for x in (1,2,3)]
    if n:
        assert lengths[0]==n*n-n+3
        assert max(lengths)<=n*n+3*n+1
        assert [cyc(state[x]) for x in (1,2,3)]==[1,n+1,2*n+1]
    rows.append({'n':n,'basis_word_lengths':lengths,'basis_cyclic_lengths':[cyc(state[x])for x in(1,2,3)]})
    state={x:apply(state[x],phi)for x in state}
result={'status':'PASS','range_n':[0,60],'integer_letter_encoding':{'1':'a','2':'b','3':'c','negative':'inverse'},'phi_images':{str(k):v for k,v in phi.items()},'claims_checked':['direct substitution equals inner-twist formula','exact a-word length for every positive tested n','polynomial upper bound for all three basis images','cyclic lengths differ from actual lengths'],'limitations':['finite sanity checks only; all-n proof required','does not independently establish prior nonembedding theorem','no Hydra conclusion','no originality conclusion'],'rows':rows}
Path(__file__).with_name('growth_metric_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: direct free reduction n=0..60, exact positive-n formulas and metric distinction.')
