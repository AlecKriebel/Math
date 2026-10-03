#!/usr/bin/env python3
"""Independent finite algebra/invariant checks; universal proof stays written.
Does not import either author's or earlier reviewers' implementations.
"""
from collections import Counter
from itertools import permutations
import hashlib, json, random, stat
from pathlib import Path

P = Path(__file__).resolve().parent.parent/'preprint_v1'
S = lambda i,e=1: (('s',i,e),)
V = lambda i: (('v',i,1),)
checks = 0
cover = Counter()
def check(ok, why):
    global checks
    if not ok: raise AssertionError(why)
    checks += 1
def inverse(w): return tuple((t,i,-e if t=='s' else 1) for t,i,e in reversed(w))
def shift(w): return tuple((t,i+1,e) for t,i,e in w)
def padded(n,w): return (n,w) if n%2==0 else (n+1,w+S(n))
def admissible(n,w):
    return n>=1 and all(1<=i<n and (t,e) in (('s',1),('s',-1),('v',1)) for t,i,e in w)
def classical_count(n,w):
    # Compose linear Fox-color transformations, then solve (A-I)x=0 over F3.
    mat = [[int(i==j) for j in range(n)] for i in range(n)]
    for t,i,e in w:
        check(t=='s','Fox domain')
        a,b = mat[i-1][:],mat[i][:]
        if e==1: mat[i-1],mat[i] = [(2*x-y)%3 for x,y in zip(a,b)],a
        else: mat[i-1],mat[i] = b,[(2*y-x)%3 for x,y in zip(a,b)]
    kernel = [[(mat[i][j]-int(i==j))%3 for j in range(n)] for i in range(n)]
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank,n) if kernel[i][col]),None)
        if pivot is None: continue
        kernel[rank],kernel[pivot] = kernel[pivot],kernel[rank]
        c = 1 if kernel[rank][col]==1 else 2
        kernel[rank] = [(c*x)%3 for x in kernel[rank]]
        for i in range(n):
            if i==rank: continue
            c = kernel[i][col]
            kernel[i] = [(x-c*y)%3 for x,y in zip(kernel[i],kernel[rank])]
        rank += 1
    return 3**(n-rank)
def ordered_matrix(n,w):
    # Independent union-find of actual closure connections, not permutation cycles.
    labels = list(range(n)); events = []
    for t,i,e in w:
        left,right = labels[i-1:i+1]
        if t=='s': events.append((left,right,e) if e==1 else (right,left,e))
        labels[i-1],labels[i] = right,left
    parents = list(range(n))
    def find(i):
        while parents[i]!=i:
            parents[i] = parents[parents[i]]; i=parents[i]
        return i
    for position,top_label in enumerate(labels): parents[find(position)] = find(top_label)
    roots = sorted({find(i) for i in range(n)})
    membership = [roots.index(find(i)) for i in range(n)]
    mat = [[0]*len(roots) for _ in roots]
    for a,b,e in events:
        a,b = membership[a],membership[b]
        if a!=b: mat[a][b] += e
    return tuple(tuple(row) for row in mat)
def canonical_matrix(mat):
    # Include isolated components and allow only simultaneous component relabeling.
    n=len(mat)
    return min(tuple(mat[p[i]][p[j]] for i in range(n) for j in range(n))
               for p in permutations(range(n)))
def patterns(kind,n,a,b,g=()):
    if kind=='C': return (n,b),(n,a+b+inverse(a))
    if kind=='BC': return (n,b+S(n-1)),(n,a+b+inverse(a)+S(n-1))
    if kind=='T': return (n,b+S(n-1)),(n,b+g)
    if kind=='D': return (n,b),(n+2,b+g+S(n+1))
    if kind=='R': return (n,a+S(n-1,-1)+b+S(n-1)),(n,a+V(n-1)+b+V(n-1))
    if kind=='L': return (n,shift(a)+S(1,-1)+shift(b)+S(1)),(n,shift(a)+V(1)+shift(b)+V(1))
    if kind=='BR': return (n,a+S(n-2,-1)+b+S(n-2)+S(n-1)),(n,a+V(n-2)+b+V(n-2)+S(n-1))
    if kind=='BL': return (n,shift(a)+S(1,-1)+shift(b)+S(1)+S(n-1)),(n,shift(a)+V(1)+shift(b)+V(1)+S(n-1))
    raise ValueError(kind)
rng = random.Random(935071)
def word(k,length,virtual):
    if k==0: return ()
    alphabet = [z for i in range(1,k+1) for z in S(i)+S(i,-1)+(V(i) if virtual else ())]
    return tuple(rng.choice(alphabet) for _ in range(length))

manifest_bytes = (P/'PACKAGE_MANIFEST.json').read_bytes()
check(hashlib.sha256(manifest_bytes).hexdigest()=='2be2e6795505f3acf54bc02203a5df0d5b51885515c72ddd7c0bf85056ced2b3','reviewed manifest')
manifest = json.loads(manifest_bytes)
actual = sorted(str(p.relative_to(P)) for p in P.rglob('*') if p.is_file())
check(actual==sorted([r['path'] for r in manifest['files']]+['PACKAGE_MANIFEST.json']),'whole 19-file scope')
for row in manifest['files']:
    path=P/row['path']; body=path.read_bytes()
    check(path.is_file() and not path.is_symlink(),'regular file')
    check(len(body)==row['bytes'] and hashlib.sha256(body).hexdigest()==row['sha256'],'whole input bytes')
    check(format(stat.S_IMODE(path.stat().st_mode),'04o')==row['mode'],'whole mode')

for virtual in (False,True):
    for n in (2,4,6):
        for kind in ('C','BC','T','D')+(('R','L','BR','BL') if virtual else ()):
            if kind in ('BR','BL') and n==2: continue
            limit={'C':n-1,'BC':n-2,'T':n-2,'D':n-1,'R':n-2,'L':n-2,'BR':n-3,'BL':n-3}[kind]
            for length in (0,1,3,7):
                a,b=word(limit,length,virtual),word(limit,7-length,virtual)
                gs=[()] if kind not in ('T','D') else [S(n-1 if kind=='T' else n,e) for e in (1,-1)]+([V(n-1 if kind=='T' else n)] if virtual else [])
                for g in gs:
                    pair=patterns(kind,n,a,b,g)
                    check(all(admissible(m,w) and m%2==0 for m,w in pair),'valid even endpoints')
                    matrices=[ordered_matrix(m,w) for m,w in pair]
                    check(canonical_matrix(matrices[0])==canonical_matrix(matrices[1]),'ordered invariant '+kind)
                    if not virtual: check(classical_count(*pair[0])==classical_count(*pair[1]),'Fox invariant '+kind)
                    cover[('virtual_' if virtual else 'classical_')+kind]+=1
                    if kind=='D':
                        # Both signs at the added last crossing, realized by the valid T.
                        for e in (1,-1):
                            third=(n+2,b+g+S(n+1,e))
                            check(ordered_matrix(*pair[1])==ordered_matrix(*third),'double-sign ordered invariant')
                            if not virtual: check(classical_count(*pair[0])==classical_count(*third),'double-sign Fox invariant')

# Enumerate literal parity lifts independently of the package implementation.
lifted=0
for m in range(1,10):
    for virtual in (False,True):
        for length in (0,1,4):
            a,b=word(m-1,length,virtual),word(m-1,4-length,virtual)
            n=m+m%2
            old=((m,b),(m,a+b+inverse(a)))
            check(tuple(padded(*x) for x in old)==patterns('BC' if m%2 else 'C',n,a,b),'conjugation lift'); lifted+=1
            for g in [S(m),S(m,-1)]+([V(m)] if virtual else []):
                old=((m,b),(m+1,b+g))
                check(tuple(padded(*x) for x in old)==patterns('T' if m%2 else 'D',n,(),b,g),'stabilization lift'); lifted+=1
            if virtual and m>=2:
                a,b=word(m-2,length,True),word(m-2,4-length,True)
                for side in ('R','L'):
                    old=patterns(side,m,a,b)
                    check(tuple(padded(*x) for x in old)==patterns(('B'+side) if m%2 else side,n,a,b),'exchange lift'); lifted+=1

fox=[classical_count(2,S(1)*3),classical_count(2,S(1)),classical_count(2,S(1,-1))]
check(fox==[9,3,3],'T boundary countercontrol')
right=[ordered_matrix(2,S(1)*2),ordered_matrix(2,S(1)+V(1)+S(1)+V(1))]
check(right==[((0,1),(1,0)),((0,2),(0,0))],'R witness exact entries')
check(canonical_matrix(right[0])!=canonical_matrix(right[1]),'R witness modulo relabeling')
buffer=[ordered_matrix(4,S(2)*2+S(3)),ordered_matrix(4,S(2)+V(2)+S(2)+V(2)+S(3))]
check(canonical_matrix(buffer[0])!=canonical_matrix(buffer[1]),'BR witness modulo relabeling')
check(len(ordered_matrix(1,()))==1 and len(ordered_matrix(2,()))==2,'false idle padding')
for m in range(1,31):
    check(padded(m,())[0]==2*((m+1)//2),'height round-up')
    if m%2==0: check(padded(m,())==(m,()),'even endpoint fixed exactly')

print(json.dumps({'status':'PASS_INDEPENDENT_BOUNDED_INVARIANTS','checks':checks,
    'scheme_cases':dict(sorted(cover.items())),'literal_lifts':lifted,
    'Fox3_witness':fox,'ordered_R_witness':right,'ordered_BR_witness':buffer,
    'reviewed_package_files':len(actual),'manifest_sha256':hashlib.sha256(manifest_bytes).hexdigest(),
    'limitations':['Not a link-equivalence oracle','Finite samples do not replace the universal proof',
        'Imported Markov theorems not independently reproved','No priority absence or publication assertion']},sort_keys=True,indent=2))
