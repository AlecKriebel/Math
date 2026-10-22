"""Independent exact controls for frozen Turns 4 and 5.
No author imports, SymPy, finite matrix interpolation, or search extension.
Sparse formal identities are valid for arbitrary independent diagonal factors.
"""
import itertools as it
import json
from collections import defaultdict, Counter


def norm(p):
    return {m:c for m,c in p.items() if c}


def add(*polys):
    ans=defaultdict(int)
    for p in polys:
        for m,c in p.items(): ans[m]+=c
    return norm(ans)


def scale(p,s): return norm({m:c*s for m,c in p.items()})


def multiply(p,q):
    ans=defaultdict(int)
    for a,c in p.items():
        for b,d in q.items(): ans[tuple(x+y for x,y in zip(a,b))]+=c*d
    return norm(ans)


def mon(indices,n=15):
    v=[0]*n
    for i in indices: v[i]+=1
    return tuple(v)


def sgn(p): return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))


def trace_diff(n):
    # P C^2 Q C^(n-2) minus Q C^2 P C^(n-2), by index walks.
    ans=defaultdict(int)
    for path in it.product(range(3),repeat=n):
        edges=[3*path[j]+path[(j+1)%n] for j in range(n)]
        ans[mon(edges+[9+path[0],12+path[2]])]+=1
        ans[mon(edges+[12+path[0],9+path[2]])]-=1
    return norm(ans)


def alternant():
    ans={}
    # det of rows (P_i,Q_i,1); column-to-row permutation.
    for perm in it.permutations(range(3)):
        ans[mon([9+perm[0],12+perm[1]])]=sgn(perm)
    return ans


def diagonal_adjugate_coefficients():
    # Full F = sum P_i Q_j R_k b_ij b_jk adj(B)_ki.
    # adj(B)_ki = (-1)^(i+k) det B[rows != i, cols != k].
    # Key: b-entry multiplicities (9), followed by diagonal labels (i,j,k).
    full=defaultdict(int)
    for i,j,k in it.product(range(3),repeat=3):
        rows=[r for r in range(3) if r!=i]
        cols=[c for c in range(3) if c!=k]
        for permutation in it.permutations(range(2)):
            edges=[3*i+j,3*j+k]+[3*rows[t]+cols[permutation[t]] for t in range(2)]
            full[(mon(edges,9),(i,j,k))]+=(-1)**(i+k)*sgn(permutation)
    full=norm(full)
    def coefficient(edges):
        key=mon(edges,9)
        return {ijk:c for (b,ijk),c in full.items() if b==key}
    c1=coefficient([1,2,3,6])
    c2=coefficient([0,1,5,6])
    assert c1=={(1,0,1):-1,(1,0,2):1,(2,0,1):1,(2,0,2):-1},c1
    assert c2=={(0,0,1):1,(2,0,0):1,(2,0,1):-1},c2
    swapped={(k,j,i):v for (i,j,k),v in c2.items()}
    diff=add(c2,scale(swapped,-1))
    target={}
    for perm in it.permutations(range(3)):
        target[(perm[0],0,perm[1])]=sgn(perm)
    assert diff==target,(diff,target)
    return full,c1,c2


def equality_patterns(n):
    # Restricted-growth set-partition representatives, no finite integer window.
    def grow(prefix):
        if len(prefix)==n:
            yield tuple(prefix);return
        for value in range(max(prefix,default=-1)+2):
            yield from grow(prefix+[value])
    yield from grow([])


def relabel(p):
    labels={};out=[]
    for a in p:
        if a not in labels: labels[a]=len(labels)
        out.append(labels[a])
    return tuple(out)


def canonical(p): return min(p[i:]+p[:i] for i in range(len(p)))


def deck(p): return Counter(zip(p,p[1:]+p[:1]))


def prove_pattern_control():
    patterns=list(equality_patterns(5));assert len(patterns)==52
    collision_patterns=[]
    for p in patterns:
        # Exhaust every order of this fixed multiset, independent of labels' values.
        matches={canonical(q) for q in set(it.permutations(p)) if deck(q)==deck(p)}
        if len(matches)>1:
            counts=Counter(p)
            assert sorted(counts.values())==[1,1,3]
            repeated=next(x for x,c in counts.items() if c==3)
            s,t=[x for x,c in counts.items() if c==1]
            assert matches=={canonical((repeated,repeated,s,repeated,t)),canonical((repeated,repeated,t,repeated,s))}
            collision_patterns.append(p)
    return len(patterns),len(collision_patterns)


def check_paths():
    target=mon([0,0,1,5,6],9)
    paths=[]
    for p in it.product(range(3),repeat=5):
        if mon([3*p[i]+p[(i+1)%5] for i in range(5)],9)==target: paths.append(p)
    assert len(paths)==5
    base=(0,0,0,1,2)
    assert set(paths)=={base[i:]+base[:i] for i in range(5)}
    return paths


def check_word_rewrite():
    # Formal free products in symbols C,P,Q, keeping all letters distinct.
    w1=('C','C','P','C','C','Q','C')
    w2=('C','C','Q','C','C','P','C')
    t1=('P','C','C','Q','C','C','C')
    t2=('Q','C','C','P','C','C','C')
    assert canonical(w1)==canonical(t1)
    assert canonical(w2)==canonical(t2)


def main():
    alt=alternant()
    cycle={mon([1,5,6]):1,mon([2,7,3]):-1}
    e2={mon([0,4]):1,mon([0,8]):1,mon([4,8]):1,
        mon([1,3]):-1,mon([2,6]):-1,mon([5,7]):-1}
    d3=trace_diff(3);d5=trace_diff(5)
    assert d3==scale(multiply(cycle,alt),-1)
    assert d5==multiply(e2,multiply(cycle,alt))
    assert d5==scale(multiply(e2,d3),-1)
    full,c1,c2=diagonal_adjugate_coefficients()
    patterns,collision_patterns=prove_pattern_control()
    paths=check_paths();check_word_rewrite()
    report={
        'status':'PASS',
        'method':'standard-library sparse integer polynomial arithmetic and cofactor permutations; no author imports or symbolic algebra package',
        'equality_patterns':patterns,
        'exceptional_labeled_partition_patterns':collision_patterns,
        'coefficient_paths':[list(p) for p in paths],
        'cubic_difference_formal_terms':len(d3),
        'quintic_difference_formal_terms':len(d5),
        'cayley_hamilton_and_alternant_signs':'d3 = -cycle*alternant; d5 = e2*cycle*alternant = -e2*d3',
        'generic_adjugate_noncancelled_diagonal_terms':len(full),
        'first_adjugate_coefficient':{'P%d Q%d R%d'%tuple(x+1 for x in k):v for k,v in c1.items()},
        'second_adjugate_coefficient':{'P%d Q%d R%d'%tuple(x+1 for x in k):v for k,v in c2.items()},
        'swapped_second_coefficient_alternant':'PASS',
        'exceptional_word_cyclic_rewrite':'PASS',
        'scope':'All equality patterns and universal formal identities checked; integer-exponent reconstruction and density independently justified in accompanying audit.'
    }
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
