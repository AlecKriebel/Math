"""Independent finite attacks on canonical label cells, repair, and cancellation.

Reconstructed from the pinned primary TeX, not a prior audit or candidate code.
Exact matching-set linear identities are tested for arbitrary function values.
"""
from collections import Counter, deque
from itertools import product
from pathlib import Path
import datetime, hashlib, json, random

OUT = Path(__file__).resolve().parent
stats = Counter()
rng = random.Random(1130307)

def edge(u,v,l): return (min(u,v),max(u,v),l)

def zero(c): return {k:v for k,v in c.items() if v}

def dist(adj,a,b):
    q=deque([(a,0)]); seen={a}
    while q:
        x,d=q.popleft()
        if x==b:return d
        for y in adj[x]-seen:
            seen.add(y);q.append((y,d+1))
    raise AssertionError('Disconnected tree')

def audit(labels, adj, high=False):
    m=len(labels)
    S=[{labels[(i-1)%m], labels[i]} for i in range(m)]
    O=[frozenset(edge(i,(i+1)%m,labels[i]) for i in range(b,m,2)) for b in range(2)]
    chord_cache={}
    def choose(s): return max(s) if high else min(s)
    def ext(arc):
        dr=1 if (arc[1]-arc[0])%m==1 else -1
        ans=[arc[-1]]
        while ans[-1]!=arc[0]:ans.append((ans[-1]+dr)%m)
        return ans
    def good(a):return len(a)==2 or bool(S[a[1]]&S[a[-2]])
    def chord(a):
        u,v=a[0],a[-1];key=tuple(sorted((u,v)))
        if key not in chord_cache:
            common=S[u]&S[v];assert common
            if (u+1)%m==v:l=labels[u]
            elif (v+1)%m==u:l=labels[v]
            else:l=choose(common)
            chord_cache[key]=edge(u,v,l)
        return chord_cache[key]
    def through(a):
        return frozenset(edge(a[i],a[i+1],labels[a[i]] if (a[i]+1)%m==a[i+1] else labels[a[i+1]]) for i in range(0,len(a)-1,2))
    def interior(a):
        return frozenset(edge(a[i],a[i+1],labels[a[i]] if (a[i]+1)%m==a[i+1] else labels[a[i+1]]) for i in range(1,len(a)-1,2))
    def closed(a):return interior(a)|{chord(a)}
    def repair(a):return edge(a[1],a[-2],choose(S[a[1]]&S[a[-2]]))
    def repaired(a):
        if len(a)==2:return frozenset()
        return (through(a)-{next(iter(through(a)&{edge(a[0],a[1],labels[a[0]] if (a[0]+1)%m==a[1] else labels[a[1]])})),
                             edge(a[-2],a[-1],labels[a[-2]] if (a[-2]+1)%m==a[-1] else labels[a[-1]])})|{repair(a)}
    cells=[]
    def recurse(arc):
        s=len(arc)-1
        if s==1:return
        assert s%2==1 and S[arc[0]]&S[arc[-1]]
        P=choose(S[arc[0]]&S[arc[-1]])
        a=[labels[arc[i]] if (arc[i]+1)%m==arc[i+1] else labels[arc[i+1]] for i in range(s)]
        exterior=ext(arc)
        if good(exterior):
            if P not in a:
                assert a[0]==a[-1]
                P=a[0]
            odd=[i for i in range(1,s,2) if a[i]==P]
            if odd:p1=odd[0];p2=p1+1;stats['good_exterior_case_a']+=1
            elif a.index(P)>0:p2=a.index(P);p1=p2-1;stats['good_exterior_case_b']+=1
            elif max(i for i,x in enumerate(a) if x==P)<s-1:
                p1=max(i for i,x in enumerate(a) if x==P)+1;p2=p1+1;stats['good_exterior_case_c']+=1
            else:p1=1;p2=s-1;stats['good_exterior_case_d']+=1
        else:
            stats['bad_exterior_cells']+=1
            if P in S[exterior[-2]]:
                arc=list(reversed(arc));exterior=ext(arc);a=list(reversed(a));stats['bad_exterior_reversals']+=1
            assert P not in S[exterior[-2]] and a[0]==P
            if a[-1]==P:p1=1;p2=s-1;stats['bad_exterior_both_boundaries']+=1
            else:
                t=max(i for i,x in enumerate(a) if x==P)+1
                assert a[t]==a[-1]
                if t%2==0:p1=1;p2=t;stats['bad_exterior_even_t']+=1
                else:p1=t;p2=s-1;stats['bad_exterior_odd_t']+=1
        assert 0<p1<p2<s and p1%2==1 and p2%2==0
        arcs=[arc[:p1+1],arc[p1:p2+1],arc[p2:],exterior]
        for q in arcs:
            assert (len(q)-1)%2==1 and S[q[0]]&S[q[-1]]
        g=[good(q) for q in arcs]
        assert (g[0] and g[2]) or (g[1] and g[3])
        for b in range(2):
            if all(len(arcs[i])>2 for i in (b,b+2)):
                assert g[1-b] and g[3-b]
        cells.append(arcs)
        for q in arcs[:3]:recurse(q)
    recurse(list(range(m)))
    assert len(cells)==(m-2)//2
    all_sides=Counter(tuple(sorted((a[0],a[-1]))) for cell in cells for a in cell)
    assert sum(v==2 for v in all_sides.values())==(m-4)//2
    assert sum(v==1 for v in all_sides.values())==m and all(v in (1,2) for v in all_sides.values())
    def perfect(A):
        covered=Counter(v for e in A for v in e[:2])
        assert len(A)==m//2 and len(covered)==m and all(covered[v]==1 for v in range(m))
    def expr(A,B):return Counter({A:1,B:-1}) if A!=B else Counter()
    def conversion(a):
        b=next(b for b in range(2) if through(a)<=O[b])
        H=(O[b]-through(a))|closed(a)
        perfect(H)
        return b,H,expr(O[b],H)
    D=expr(O[0],O[1]);total=Counter()
    for arcs in cells:
        stats['cells_checked']+=1
        patterns=[through(a) for a in arcs];ints=[interior(a) for a in arcs]
        chords=[chord(a) for a in arcs]
        side_orientation=[conversion(a)[0] for a in arcs]
        P=[i for i,b in enumerate(side_orientation) if b==0]
        Q=[i for i,b in enumerate(side_orientation) if b==1]
        assert len(P)==len(Q)==2 and (P[0]-P[1])%4==2
        switched=[]
        for pair in (P,Q):
            A=frozenset().union(*ints)|{chords[i] for i in pair}
            perfect(A);switched.append(A)
        delta=expr(*switched)
        gains=Counter()
        for i,a in enumerate(arcs):
            gains.update({k:(1 if i in P else -1)*v for k,v in conversion(a)[2].items()})
        errors=[]
        for b,pair in enumerate((P,Q)):
            y,x=pair
            A1=conversion(arcs[y])[1]
            A2=(A1-patterns[x])|closed(arcs[x]);perfect(A2)
            E=expr(A1,A2)
            E.subtract(conversion(arcs[x])[2]);errors.append(E)
            if len(arcs[x])==2 or len(arcs[y])==2:assert not zero(E)
            if len(arcs[x])>2 and len(arcs[y])>2:
                stats['error_encodings_checked']+=1
                other=Q if b==0 else P
                B0=O[1-b]|{chords[x],chords[y]}
                for i in other:
                    B0=(B0-patterns[i])|repaired(arcs[i])
                B1=(B0-closed(arcs[y]))|patterns[y]
                for A,B in ((O[b],B0),(A1,B1)):
                    perfect(A);perfect(B);assert closed(arcs[x])<=B
                    old=Counter(O[0])+Counter(O[1]);new=Counter(A)+Counter(B)
                    add=new-old;drop=old-new
                    assert sum(add.values())==sum(drop.values())<=4
        rhs=delta.copy();rhs.update(gains);rhs.update(errors[0]);rhs.subtract(errors[1])
        assert zero(rhs)==zero(D)
        term=delta.copy();term.update(errors[0]);term.subtract(errors[1]);total.update(term)
        pair=next(pair for pair in (P,Q) if all(good(arcs[i]) for i in pair))
        B=frozenset().union(*(repaired(a) if i in pair else through(a) for i,a in enumerate(arcs)))
        perfect(B)
        old=Counter(O[0])+Counter(O[1]);new=Counter(switched[0])+Counter(B)
        add=new-old;drop=old-new
        assert sum(add.values())==sum(drop.values())<=4
        stats['switch_encodings_checked']+=1
        local=chords[:]
        for a in arcs:
            t=through(a)
            local.extend([edge(a[0],a[1],labels[a[0]] if (a[0]+1)%m==a[1] else labels[a[1]]),edge(a[-2],a[-1],labels[a[-2]] if (a[-2]+1)%m==a[-1] else labels[a[-1]])])
            if good(a) and len(a)>2:local.append(repair(a))
        diameter=max(dist(adj,x[2],y[2]) for x in local for y in local)
        assert diameter<=6
        stats['maximum_observed_local_label_distance']=max(stats['maximum_observed_local_label_distance'],diameter)
    assert zero(total)==zero(D)
    stats['cycles_checked']+=1

trees=[{0:set()}, {0:{1},1:{0}}, {0:{1},1:{0,2},2:{1}},
       {0:{1},1:{0,2},2:{1,3},3:{2}}, {0:{1,2,3},1:{0},2:{0},3:{0}}]
def walks(adj,m):
    for first in adj:
        stack=[(first,)]
        while stack:
            a=stack.pop()
            if len(a)==m:
                if a[0]==a[-1] or a[0] in adj[a[-1]]:yield a
            else:
                stack.extend(a+(x,) for x in sorted(adj[a[-1]]|{a[-1]}))

for adj in trees:
    for m in (4,6,8):
        for labels in walks(adj,m):audit(labels,adj,bool(stats['cycles_checked']%2))
stats['exhaustive_cycles']=stats['cycles_checked']
for case in range(2000):
    n=rng.randrange(2,9)
    adj={i:set() for i in range(n)}
    for i in range(1,n):
        j=rng.randrange(i);adj[i].add(j);adj[j].add(i)
    m=rng.randrange(6,25)*2
    # A closed walk made by an arbitrary walk followed by its reverse,
    # with occasional repeats; split recursion sees long nested excursions.
    half=[rng.randrange(n)]
    for _ in range(m//2-1):half.append(rng.choice(sorted(adj[half[-1]]|{half[-1]})))
    labels=half+list(reversed(half))
    audit(labels,adj,bool(case%2))
stats['random_cycles']=stats['cycles_checked']-stats['exhaustive_cycles']
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'status':'all asserted exact checks passed','statistics':dict(stats),
         'scope':'Finite supporting evidence, not a proof or an upstream FPRAS implementation.',
         'seed':1130307,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'INDEPENDENT_CELL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
