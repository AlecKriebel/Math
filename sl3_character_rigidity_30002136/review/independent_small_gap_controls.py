"""Fresh exact small-gap controls: formal cofactor permutations and closed paths.
Audit only; no word-pair search outside the submitted special families.
"""
from itertools import permutations, product
from collections import Counter, defaultdict
import json

def sign(t):return (-1)**sum(t[i]>t[j] for i in range(len(t)) for j in range(i+1,len(t)))
def clean(c):return {m:n for m,n in c.items() if n}
def cycle(t):return min(t[i:]+t[:i] for i in range(len(t)))
def edges(states):return tuple(sorted((states[i],states[(i+1)%len(states)]) for i in range(len(states))))
def deck(t):return tuple(sorted((t[i],t[(i+1)%len(t)]) for i in range(len(t))))

def adjugate_two():
    # tr(P B Q adj(B)): adj(B)[j,i] deletes row i and column j.
    actual=Counter()
    for i,j in product(range(3),repeat=2):
        rows=[r for r in range(3) if r!=i]
        cols=[c for c in range(3) if c!=j]
        for perm in permutations(range(2)):
            mon=tuple(sorted([(i,j)]+[(rows[k],cols[perm[k]]) for k in range(2)]))
            actual[(mon,i,j)]+=(-1)**(i+j)*sign(perm)
    expected=Counter()
    for perm in permutations(range(3)):
        mon=tuple(sorted(enumerate(perm)))
        for i in range(3):expected[(mon,i,perm[i])]+=sign(perm)
    assert clean(actual)==clean(expected)
    return len(clean(actual))

def low_gap_tests():
    grid=(-1000003,-17,-1,0,1,29,1000003)
    counts={}
    for k in (2,3):
        seen={}
        for t in product(grid,repeat=k):
            co=Counter()
            # Closed paths for the determinant-corrected swap or 3-cycle.
            targets={0:1,1:0,2:2} if k==2 else {0:1,1:2,2:0}
            for start in range(3):
                state=start; ex=[0,0]; coef=1
                for p in t:
                    if state==0:ex[0]+=p
                    elif state==1:ex[1]+=p
                    else:ex[0]-=p;ex[1]-=p
                    if k==2 and state==2:coef=-coef
                    state=targets[state]
                assert state==start
                co[tuple(ex)]+=coef
            sig=(sum(t),tuple(sorted(clean(co).items())))
            assert sig not in seen or seen[sig]==cycle(t)
            seen[sig]=cycle(t)
        counts[str(k)]=len(grid)**k
    # Nontrivial common shifts really do survive the 3-cycle specialization.
    def three(t):
        p,q,r=t;return Counter([(p-r,q-r),(r-q,p-q),(q-p,r-p)])
    assert three((1,2,3))==three((8,9,10)) and sum((1,2,3))!=sum((8,9,10))
    # Four-letter deck reconstruction is independent of numerical magnitudes.
    seen={}
    for t in product(range(4),repeat=4):
        sig=deck(t)
        assert sig not in seen or seen[sig]==cycle(t)
        seen[sig]=cycle(t)
    wanted=tuple(sorted([(0,0),(0,1),(1,2),(2,0)]))
    paths=[s for s in product(range(3),repeat=4) if edges(s)==wanted]
    assert len(paths)==4 and {cycle(s) for s in paths}=={(0,0,1,2)}
    # Reconstruct ordered nonzero mixed-sign gaps via transposition and cycle.
    nz=tuple(x for x in grid if x)
    seen={}
    for p,q in product(nz,repeat=2):
        trans=tuple(sorted(Counter([(p,q,0),(q,p,0),(0,0,p+q)]).items()))
        cyclic=tuple(sorted(Counter([(p,q,0),(0,p,q),(q,0,p)]).items()))
        sig=(p+q,trans,cyclic)
        assert sig not in seen or seen[sig]==(p,q)
        seen[sig]=(p,q)
    return {'large_magnitude_gap_formula_and_reconstruction_cases':counts,
            'three_cycle_common_shift_negative_control':'PASS',
            'four_gap_equality_assignments':4**4,'four_gap_contributing_paths':len(paths),
            'mixed_two_ordered_gap_cases':len(nz)**2}

if __name__=='__main__':
    print(json.dumps({'status':'PASS','formal_mixed_two_cofactor_terms':adjugate_two(),
        'controls':low_gap_tests(),'scope':'Finite falsification controls plus formal generic adjugate identity; all-integer proofs are in the audit.'},indent=2))
