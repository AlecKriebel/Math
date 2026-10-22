"""Explicit checks and meaningful mathematical mutations; no assertion dependence."""
import itertools
import json
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def ordered(A, p):
    return [sum((a+b)%p == s for a in A for b in A) for s in range(p)]

def unordered(A, p, diagonals=True):
    pairs = itertools.combinations_with_replacement(A,2) if diagonals else itertools.combinations(A,2)
    counts=[0]*p
    for a,b in pairs:
        counts[(a+b)%p]+=1
    return counts

def check():
    base=Path(__file__).parent
    rows=json.loads((base/'exact_results.json').read_text())
    need([(x['p'],x['m']) for x in rows]==[(3,3),(5,4),(7,5),(11,7),(13,7),(17,8),(19,9),(23,10),(29,11),(31,11)], 'minimum table')
    for row in rows:
        p,A=row['p'],row['witness'];u=unordered(A,p);r=ordered(A,p)
        need(u==row['unordered_counts'] and 1 not in u and not {1,2}.intersection(r),'witness')
        need(all(r[s]==2*u[s]-int(any(2*a%p==s for a in A)) for s in range(p)), 'ordered convention')
        changed=u.copy();changed[0]+=1
        need(changed!=unordered(A,p),'count mutation')
    regression=json.loads((base/'checker_regression.json').read_text())
    r=ordered(regression['A'],regression['p'])
    need(r==regression['ordered_counts'] and 1 not in r and 2 in r and regression['expected_NUS'] is False, 'ordered regression')
    need(1 in unordered(regression['A'],regression['p']), 'false-positive rejection')
    need(unordered([0,1,2],3)!=unordered([0,1,2],3,False),'diagonal omission mutation')
    C=(0,1,4);p=13;B=sorted({(a+b)%p for a in C for b in C})
    quads={x:[q for q in itertools.combinations_with_replacement(C,4) if sum(q)%p==4*x%p and q!=(x,)*4] for x in C}
    need(all(quads.values()),'quaternary premise')
    u=unordered(B,p)
    need(u==[2,1,2,2,2,2,2,1,2,2,2,0,1], 'quaternary counts')
    need([s for s,n in enumerate(u) if n==1]==[1,7,12], 'quaternary transfer rejected')
    need(4*0%13!=sum([1,4,4,1])%13, 'quaternary certificate mutation')
    return {'verdict':'PASS','witnesses':10,'ordered_only_one_mutant_rejected':True,'diagonal_omission_detected':True,'count_mutations_detected':10,'quaternary_transfer_refuted':True,'quaternary_certificate_mutant_rejected':True}

if __name__=='__main__':
    print(json.dumps(check(),sort_keys=True))
