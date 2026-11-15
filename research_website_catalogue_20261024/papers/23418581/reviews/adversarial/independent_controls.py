"""Independent rational-module coefficient diagnostics, created before native code/results."""
from math import comb
from itertools import product
import json

checks = 0

def ck(ok, description):
    global checks
    checks += 1
    if not ok:
        raise RuntimeError(description)

def action(m, i, lower, p):
    ans = {}
    limit = i if lower else m-i
    for a in range(limit+1):
        c = comb(limit, a) % p
        if c:
            ans[(i-a if lower else i+a, a)] = c
    return ans

def reach(m, start, p):
    seen, work = {start}, [start]
    while work:
        i = work.pop()
        for low in (False, True):
            for (j, a), c in action(m, i, low, p).items():
                if j not in seen:
                    seen.add(j)
                    work.append(j)
    return seen

def invariant(m, indices, p):
    return all(j in indices for i in indices for low in (False,True)
               for j, a in action(m, i, low, p))

def rank(rows, p):
    a = [[x % p for x in r] for r in rows]
    k = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(k,len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        inv = pow(a[k][col], p-2, p)
        a[k] = [(z*inv) % p for z in a[k]]
        for i in range(len(a)):
            if i != k and a[i][col]:
                c = a[i][col]
                a[i] = [(x-c*y) % p for x,y in zip(a[i],a[k])]
        k += 1
        if k == len(a):
            break
    return k

profiles = []
for p in (3,5,7,11,13):
    r, m, d = 2*p-1, 2*p-3, p-3
    full = set(range(r+1))
    for i in full:
        ck(reach(r, i, p) == full, 'all monomial generated rational submodule of Sym^(2p-1)')
    support = set(range(p-2)) | set(range(p, m+1))
    missing = set(range(m+1)) - support
    ck(missing == {p-2,p-1}, 'two quotient weights')
    ck({i for i in range(m+1) if comb(m,i) % p} == support, 'binomial support')
    ck(invariant(m,support,p), 'Frobenius-image invariant under all polynomial coefficients')
    for i in support:
        ck(reach(m,i,p) == support, 'W has no proper rational monomial submodule')
    for i in missing:
        ck(reach(m,i,p) == set(range(m+1)), 'any outside monomial generates all B')
    ck(not invariant(m,missing,p), 'torus-complement is not rational-GL2-invariant')
    ck(action(m,p-2,True,p)[(0,p-2)] == 1, 'nonsplitting coefficient exactly1')
    for i in missing:
        j = next(x for x in missing if x != i)
        ck(any(t == j and a > 0 and c == p-1 for low in (False,True)
               for (t,a),c in action(m,i,low,p).items()), 'both quotient coefficient connections')
    # Compare the Frobenius tensor action to the actual symmetric power coefficient by coefficient.
    for q in (0,1):
        for c in range(d+1):
            i = q*p+c
            for low in (False,True):
                expected = {}
                for optional in (0,1):
                    if optional and ((low and q==0) or (not low and q==1)):
                        continue
                    first = (q-1 if low else q+1) if optional else q
                    for a in range((c if low else d-c)+1):
                        coeff = comb(c if low else d-c,a) % p
                        if coeff:
                            idx = first*p + (c-a if low else c+a)
                            expected[(idx,optional*p+a)] = coeff
                ck(action(m,i,low,p) == expected, 'Frobenius tensor intertwiner exact polynomial coefficients')
    # Distinct top/socle weights after determinant twisting, including p3 equal dimensions.
    socle_weights = {(m-i+1,i+1) for i in support}
    top_weights = {(p,p-1),(p-1,p)}
    ck(socle_weights.isdisjoint(top_weights), 'top/socle labels distinguished by exact torus weights')
    counts = None
    if p <= 7:
        closed = []
        for mask in range(1 << (m+1)):
            subset = {i for i in range(m+1) if mask >> i & 1}
            if invariant(m,subset,p):
                closed.append(subset)
        ck(closed == [set(),support,set(range(m+1))] or
           (len(closed)==3 and all(s in closed for s in [set(),support,set(range(m+1))])),
           'all rational monomial submodules exactly0/W/B')
        counts = len(closed)
    profiles.append({'p':p,'simple_symmetric_dimension':r+1,'B_dimension':m+1,'W_dimension':len(support),
                     'quotient_dimension':len(missing),'enumerated_closed_subspaces':counts})

# Independent permutation-augmentation coefficient checks, with exhaustive p3 vectors and binary-basis p5 vectors.
augmentation = []
for p in (3,5):
    r = 2*p-1
    choices = range(p) if p==3 else range(2)
    tested = 0
    for leading in product(choices, repeat=r-1):
        v = list(leading) + [(-sum(leading)) % p]
        ck(sum(v) % p == 0, 'actual augmentation vector')
        if not any(v):
            continue
        pair = next(((i,j) for i in range(r) for j in range(i+1,r) if v[i] != v[j]),None)
        ck(pair is not None, 'nonzero augmentation vector cannot be constant when p does not divide r')
        i,j = pair
        w = list(v)
        w[i],w[j] = w[j],w[i]
        diff = [(a-b) % p for a,b in zip(v,w)]
        ck(diff[i] == (v[i]-v[j]) % p and diff[j] == (v[j]-v[i]) % p and
           all(diff[k]==0 for k in range(r) if k not in pair), 'transposition extracts exact pair difference')
        tested += 1
    rows=[]
    for i in range(r):
        for j in range(i+1,r):
            v=[0]*r;v[i]=1;v[j]=p-1;rows.append(v)
    ck(rank(rows,p)==r-1, 'difference orbit spans full augmentation module')
    augmentation.append({'p':p,'r':r,'nonzero_vectors':tested,'dimension':r-1})

# Essential boundary controls: dimension coincidence is not equal torus character; the p2 local nonsplitting mechanism disappears.
ck(profiles[0]['W_dimension']==profiles[0]['quotient_dimension']==2, 'p3 equal-dimension boundary exercised')
ck(reach(1,0,2)=={0,1} and reach(1,1,2)=={0,1}, 'p2 B=Sym1 is simple; odd-prime extension not asserted')
ck(all(sum([1]*r) % p == 0 for p,r in [(3,3),(5,5)]), 'excluded p-dividing-r augmentation constant-line countercontrol')
print(json.dumps({'independent_checks':checks,'profiles':profiles,'augmentation':augmentation,
                  'mechanism':'formal polynomial-coefficient operators plus exact torus-weight submodule graph, not finite-group evaluation',
                  'universal_proof_inferred_from_finite_checks':False,'supplied_scientific_imports_or_execution':0,
                  'network':0,'writes':0},indent=2))
