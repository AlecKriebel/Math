#!/usr/bin/env python3
"""Own offline exact mechanism checks; finite controls do not prove all ranks."""
import hashlib
import itertools as it
import json
import pathlib
import sys
from fractions import Fraction as F

BASE = pathlib.Path(__file__).resolve().parent


def need(x, msg):
    if not x:
        raise RuntimeError(msg)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def mm(a, b):
    return tuple(tuple(sum(x*y for x,y in zip(row,col)) for col in zip(*b)) for row in a)


def eye(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def det(a):
    a = [[F(x) for x in row] for row in a]
    value = F(1)
    for i in range(len(a)):
        k = next((k for k in range(i,len(a)) if a[k][i]), None)
        if k is None:
            return F(0)
        if k != i:
            a[k],a[i] = a[i],a[k]
            value = -value
        pivot = a[i][i]
        value *= pivot
        for j in range(i+1,len(a)):
            ratio = a[j][i]/pivot
            a[j] = [x-ratio*y for x,y in zip(a[j],a[i])]
    return value


def diagram(kind, n):
    size = n if kind == 'A' else n+1
    a = [[2 if i == j else 0 for j in range(size)] for i in range(size)]
    def edge(i,j,ij=-1,ji=-1):
        a[i][j],a[j][i] = ij,ji
    if kind == 'A':
        if n == 2:
            edge(0,1,-2,-2)
        else:
            for i in range(n): edge(i,(i+1)%n)
    elif kind == 'B':
        edge(0,2);edge(1,2)
        for i in range(2,n): edge(i,i+1)
        edge(n-1,n,-1,-2)
        if n == 2: edge(0,2,-1,-2)
    elif kind == 'C':
        for i in range(n): edge(i,i+1)
        edge(0,1,-1,-2);edge(n-1,n,-2,-1)
    elif kind == 'D':
        edge(0,2);edge(1,2)
        for i in range(2,n-2): edge(i,i+1)
        edge(n-2,n-1);edge(n-2,n)
    return a


def permutation(size, swaps=()):
    p = list(range(size))
    for i,j in swaps:p[i],p[j] = p[j],p[i]
    return p


def cases():
    # Inputs transcribed from GH author-copy §§6.3–6.6 EO WORDS, independently
    # of the submitted table of orbit SUPPORTS. Parameter ranges are diagnostics.
    for n in [2,3,4,5,6,8,11]:
        yield 'A_split', 'A', n, 0, [(i+1)%n for i in range(n)], [[]]
        yield 'A_unitary', 'A', n, 0, [(1-i)%n for i in range(n)], [[]]+[[0]+list(range(n-1,n-l,-1)) for l in range(1,(n-1)//2+1)]
    for n in [2,3,4,5,7,10]:
        theta = permutation(n+1,[(0,1)])
        yield 'B_v0', 'B', n, 0, theta, [[]]+[[0]+list(range(2,l+1)) for l in range(1,n)]
        chain = [list(range(n,n-l,-1)) for l in range(1,n)]
        yield 'B_vn', 'B', n, n, theta, [[]]+chain
        yield 'B_fork', 'B', n, n, permutation(n+1), [[]]+chain+[chain[-1]+[1],chain[-1]+[0]]
        yield 'C_chain', 'C', n, 0, permutation(n+1), [[]]+[list(range(l)) for l in range(1,n+1)]
    for n in [4,5,6,8,11]:
        chain = [[0]+list(range(2,l+1)) for l in range(1,n-1)]
        yield 'D_chain', 'D', n, 0, permutation(n+1,[(0,1),(n-1,n)]), [[]]+chain
        yield 'D_fork', 'D', n, 0, permutation(n+1,[(0,1)]), [[]]+chain+[chain[-1]+[n-1],chain[-1]+[n]]
    yield 'A3_omega2', 'A', 4, 0, [2,3,0,1], [[],[0]]
    yield 'A3_fork', 'A', 4, 0, [2,1,0,3], [[],[0],[0,1],[0,3]]
    yield 'C2_v0', 'C', 2, 0, [2,1,0], [[],[0]]
    yield 'C2_v1', 'C', 2, 1, [2,1,0], [[],[1]]
    yield 'C2_fork', 'C', 2, 1, [0,1,2], [[],[1],[1,2],[1,0]]


def orbit_closure(subset, theta):
    out = set(subset)
    while True:
        new = out | {theta[i] for i in out}
        if new == out:return out
        out = new


def support_controls():
    rows = set();param = 0;supports = 0;pairs = 0;fork_rows = set();records = []
    for name,kind,n,v,theta,words in cases():
        rows.add(name);param += 1;a = diagram(kind,n);size = len(a);S = set(range(size));K = S-{v}
        need(all(a[i][j] == a[theta[i]][theta[j]] for i in S for j in S),'diagram automorphism')
        reflections = []
        for i in S:
            m = [list(row) for row in eye(size)]
            for j in S:m[i][j] -= a[i][j]
            reflections.append(tuple(map(tuple,m)))
        allP = []
        for word in words:
            P = orbit_closure(word,theta);allP.append(P);supports += 1
            need(P < S and (not P or v in P),'proper support and omitted vertex')
            representatives = [orbit_closure({i},theta) for i in word]
            need(len(word) == len({tuple(sorted(z)) for z in representatives}),'one representative per orbit')
            x = eye(size);xi = eye(size)
            for i in word:x = mm(x,reflections[i])
            for i in reversed(word):xi = mm(xi,reflections[i])
            need(mm(x,xi) == eye(size),'word inverse')
            need(all(all(xi[i][k] >= 0 for i in S) for k in K),'left K minimal')
            # Direct simple-root conjugation and iterative stable-subset pruning.
            mapping = {}
            for j in K:
                col = [x[i][theta[j]] for i in S]
                nz = [i for i in S if col[i]]
                if len(nz) == 1 and abs(col[nz[0]]) == 1:mapping[j] = nz[0]
            I = set(K)
            while True:
                new = {j for j in I if mapping.get(j) in I}
                if new == I:break
                I = new
            Sigma = ({j for j in S-P if any(a[j][i] for i in P)} if P else orbit_closure({v},theta))
            Q = S-P-Sigma
            need(I == Q,'direct invariant-subset calculation differs from corrected Q')
            need({theta[j] for j in Q} == Q and Q <= K,'theta-stable Q contained in K')
            need(all(a[j][i] == 0 for j in Q for i in P),'P/Q commute')
            need(bool(Sigma) and P|Q < S,'spherical proper R')
            if P:
                vertices = sorted(P)
                xtheta = [[x[i][theta[j]] for j in vertices] for i in vertices]
                need(det([[int(i == j)-xtheta[i][j] for j in range(len(P))] for i in range(len(P))]) != 0,'twisted Coxeter fixed vector')
                comps=[];remaining=set(P)
                while remaining:
                    comp={min(remaining)}
                    while True:
                        new=comp|{j for j in P if any(a[j][i] for i in comp)}
                        if new==comp:break
                        comp=new
                    comps.append(comp);remaining-=comp
                images = set();comp=set(comps[0])
                while tuple(sorted(comp)) not in images:
                    images.add(tuple(sorted(comp)));comp={theta[i] for i in comp}
                need(len(images)==len(comps),'component transitivity')
        need(len({tuple(sorted(z)) for z in allP}) == len(words),'support determines EO word')
        for P in allP:
            for P2 in allP:
                if P==P2 or not P2 <= P:
                    pairs += 1
                    sig2=({j for j in S-P2 if any(a[j][i] for i in P2)} if P2 else orbit_closure({v},theta))
                    if sig2 & P:
                        fork_rows.add(name)
                        need(len(S-P)==len(S-P2)==1 and not P<=P2 and not P2<=P,'only incomparable terminal forks')
                        start=next(iter(S-P));reach={start}
                        while True:
                            new=reach|{j for j in P2 if any(a[j][i] for i in reach)}
                            if new==reach:break
                            reach=new
                        need(start in P2 and v in reach,'fork path inside P2')
        records.append({'row':name,'parameter':n,'EO_words':words,'supports':[sorted(z) for z in allP]})
    need(len(rows)==13,'all thirteen rows')
    need(fork_rows=={'B_fork','D_fork','A3_fork','C2_fork'},'exact four fork rows')
    return dict(row_families=13,parameter_instances=param,supports=supports,ordered_support_pairs=pairs,fork_rows=sorted(fork_rows),source_case_digest=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest())


def affine_geometry():
    def add(a,b):return tuple(x+y for x,y in zip(a,b))
    def scale(k,a):return tuple(k*x for x in a)
    def sub(a,b):return add(a,scale(-1,b))
    def theta(x):return (1-x[0]-x[1]-x[2],x[2],x[1])
    def q(x):return scale(F(1,2),add(x,theta(x)))
    def s(i,x):
        if i==0:return add(x,scale(1-sum(x),(1,0,1)))
        roots={1:(2,-1,0),2:(-1,2,-1),3:(0,-1,2)}
        return sub(x,scale(x[i-1],roots[i]))
    def act(word,x):
        for i in reversed(word):x=s(i,x)
        return x
    metric=((F(3,4),F(1,2),F(1,4)),(F(1,2),F(1),F(1,2)),(F(1,4),F(1,2),F(3,4)))
    def inner(x,y):return sum(x[i]*metric[i][j]*y[j] for i in range(3) for j in range(3))
    vertices=[(0,0,0),(1,0,0),(0,1,0),(0,0,1)];b=(F(1,4),)*3;bp=(F(1,2),0,0);lam=(-1,1,1)
    need(theta(theta(b))==b and q(b)==b and theta(bp)==bp,'fixed apartment')
    need(b[0]+b[1]==bp[0]+bp[1]==F(1,2),'literal all-wall counterexample')
    need(sub(theta(add(b,lam)),theta(b))==lam and lam[0]+lam[1]==0,'fixed coroot direction parallel to wall')
    folds=[(0,1,0),(2,3,2)];words=[()]
    for length in range(1,13):
        for first in [0,1]:words.append(tuple(z for k in range(length) for z in folds[(first+k)%2]))
    pair_count=0;largest=F(0);vertex_count=0
    for p in vertices:
        images=set(act(w,p) for w in words);vertex_count += len(images)
        need(len({q(x) for x in images})==len(images),'projected-vertex injectivity')
        for sign in [-1,1]:
            direction=scale(sign,lam);pairs=list(it.combinations(images,2));exception=[]
            for u,v in pairs:
                slope=inner(direction,sub(u,v));need(slope!=0,'finite separation slope')
                c=inner(sub(u,p),sub(u,p))-inner(sub(v,p),sub(v,p));exception.append(c/(2*slope))
            N=max([F(0)]+exception).__floor__()+1;largest=max(largest,max([F(0)]+exception))
            for u,v in pairs:
                for n in [N,N+1]:
                    du=sub(sub(u,scale(n,direction)),p);dv=sub(sub(v,scale(n,direction)),p)
                    need(inner(du,du)!=inner(dv,dv),'distance separation')
                pair_count+=1
    return dict(folded_elements=len(words),distinct_vertex_images_summed_over_four_types=vertex_count,oriented_pairs=pair_count,largest_exceptional_N=str(largest),literal_escape_rejected=True)


def subword_controls():
    n=5;identity=tuple(range(n));perms=list(it.permutations(range(n)))
    def mul(a,b):return tuple(a[b[i]] for i in range(n))
    gens=[]
    for i in range(n-1):s=list(identity);s[i],s[i+1]=s[i+1],s[i];gens.append(tuple(s))
    words={identity:()};queue=[identity]
    for w in queue:
        for i,s in enumerate(gens):
            z=mul(w,s)
            if z not in words:words[z]=words[w]+(i,);queue.append(z)
    bruhat={}
    for w,word in words.items():
        below={identity}
        for i in word:below |= {mul(z,gens[i]) for z in tuple(below)}
        bruhat[w]=below
    count=0
    for start in range(n-1):
        for end in range(n-1):
            step=1 if end>=start else -1;path=tuple(range(start,end+step,step));t=identity
            for i in path:t=mul(t,gens[i])
            for w in perms:
                if t not in bruhat[w]:continue
                for y in perms:
                    if start in words[y]:continue
                    need(t in bruhat[mul(y,w)],'path subword survival under W_P')
                    count+=1
    return dict(finite_type='A4',group_elements=120,path_survival_tests=count)


def folded_gallery_controls():
    n=4;identity=tuple(range(1,n+1))
    generators=[(0,2,3,5),(2,1,3,4),(1,3,2,4),(1,2,4,3)]
    def at(w,i):
        quotient,residue=divmod(i-1,n)
        return w[residue]+n*quotient
    def product(a,b):return tuple(at(a,i) for i in b)
    def inverse(w):
        out=[None]*n
        for i,v in enumerate(w,1):
            quotient,residue=divmod(v-1,n)
            out[residue]=i-n*quotient
        return tuple(out)
    def length(w):return sum(abs((w[j]-w[i])//n) for i in range(n) for j in range(i+1,n))
    def from_word(word):
        w=identity
        for s in word:w=product(w,generators[s])
        return w
    need(all(length(s)==1 and product(s,s)==identity for s in generators),'affine simple generators')
    folds=[(0,1,0),(2,3,2)];count=0
    for l in range(13):
        for first in ([0] if l==0 else [0,1]):
            word=tuple(i for k in range(l) for i in folds[(k+first)%2]);z=from_word(word)
            need(length(z)==3*l and product(z,inverse(z))==identity,'folded/ambient weighted length')
            # Translation in the fixed coroot line, with either chamber direction.
            suitable=[]
            for sign in [-1,1]:
                for N in [20,21]:
                    t=(1,2+4*sign*N,3,4-4*sign*N)
                    if length(product(inverse(z),t))==length(z)+length(t):suitable.append((sign,N))
            need(any(all((sign,N) in suitable for N in [20,21]) for sign in [-1,1]),'rational chamber extension stays ambient reduced')
            count+=1
    return dict(folded_elements=count,rational_simple_ambient_length=3,large_translation_tests=4*count)


def central_boundaries():
    def det2(a):return (a[0]*a[3]-a[1]*a[2])%3
    def proj(a):
        lead=next(x for x in a if x);inverse=1 if lead==1 else 2
        return tuple(x*inverse%3 for x in a)
    gl=[a for a in it.product(range(3),repeat=4) if det2(a)]
    pgl={proj(a) for a in gl};image={proj(a) for a in gl if det2(a)==1}
    need(len(pgl)==24 and len(image)==12 and proj((2,0,0,1)) not in image,'adjoint-surjectivity negative control')
    # Equal reduced-building coordinates do not erase discrete central/torsion labels.
    labels=list(it.product(range(-3,4),range(2)))
    need(len(labels)==14 and len(set(labels))==14 and len({x for x,t in labels})==7,'full Kottwitz label retention')
    need(len({(x,t) for x,t in labels if x==0})==2,'torsion cannot be real-vector erased')
    separated=0
    for g,h in it.permutations(labels,2):
        inv_at_g=((h[0]-g[0]),(h[1]-g[1])%2)
        need(inv_at_g!=(0,0),'rank-zero coset evaluation must separate distinct points')
        separated+=1
    return dict(PGL2_F3=24,SL2_projective_image=12,central_torsion_labels=14,rank_zero_point_pairs_separated=separated)


def authenticate():
    need(sha(BASE/'INPUT_BINDING.json')=='5152fccf894dc5b8c1a45b2367e7d9e23eae7fd288136f0f3fee6cb0aebca4bc','frozen ten-input binding')
    binding=json.loads((BASE/'INPUT_BINDING.json').read_text())
    need(binding['head']=='cf2b59973f90d821ccd91c7f5ac306a97551d400' and len(binding['files'])==10,'immutable head closure')
    for e in binding['files']:
        b=(BASE/e['local']).read_bytes()
        need(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'PR byte pin')
        need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha1'],'PR Git blob')
    m=json.loads((BASE/'private/pr_source/PUBLIC_MANIFEST.json').read_text())
    for e in m['files']:
        f=BASE/'private/pr_source'/e['path'];need(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'PR public manifest')
    history=json.loads((BASE/'private/PRIMARY_RETRIEVAL_01.json').read_text())
    need(len(history)==8 and len({e['file'] for e in history})==8,'eight distinct primary PDFs')
    expected=json.loads((BASE/'private/pr_source/SOURCE_VERIFICATION.json').read_text())['sources']
    for e in history:
        need(e.get('status')==200 and sha(BASE/'private'/e['file'])==e['sha256'],'fresh source retrieval')
        need(any(e['sha256']==s['retrieval']['sha256'] and e['bytes']==s['retrieval']['bytes'] for s in expected),'historical source exact version')
    return dict(PR_blobs=10,PR_nonself_manifest_entries=9,exact_fresh_primary_PDFs=len(history))


def package_check():
    manifest=json.loads((BASE/'MANIFEST.json').read_text())
    actual={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file()}
    need(actual=={e['path'] for e in manifest['entries']}|{'MANIFEST.json','SEAL_CHECK.json'},'closed package membership')
    for e in manifest['entries']:
        p=BASE/e['path']
        need(p.resolve().is_relative_to(BASE) and not p.is_symlink(),'local regular evidence')
        need(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'closed artifact pin: '+e['path'])
    return dict(entries=len(manifest['entries']),manifest_sha256=sha(BASE/'MANIFEST.json'))


def main():
    if '--self-test-failure' in sys.argv:need(False,'deliberate rejected diagnostic')
    out=dict(status='PASS_EXACT_FINITE_CONTROLS_NOT_INFINITE_PROOF',optimize=sys.flags.optimize,checker_sha256=sha(pathlib.Path(__file__).resolve()),inputs=authenticate(),classified_supports=support_controls(),projected_vertices=affine_geometry(),folded_galleries=folded_gallery_controls(),path_subwords=subword_controls(),central_boundaries=central_boundaries(),network_calls=0,external_mutations=0)
    if '--verify-package' in sys.argv:out['closed_package']=package_check()
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':main()
