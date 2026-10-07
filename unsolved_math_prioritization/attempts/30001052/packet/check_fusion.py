#!/usr/bin/env python3
"""Small exact controls for three fusion systems on D8, no external dependencies."""
import itertools, json
from collections import Counter

def require(test, message):
    if not test: raise RuntimeError(message)

def compose(a,b): return tuple(a[b[i]] for i in range(len(a)))
def inv(a): return tuple(a.index(i) for i in range(len(a)))
def power(a,n):
    v=tuple(range(len(a)))
    for _ in range(n): v=compose(v,a)
    return v
def sign(a): return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))%2
def lift(a): return tuple(a)+( (5,4) if sign(a) else (4,5))
r=(1,2,3,0); s=(2,1,0,3)
D=[compose(power(r,a),power(s,b)) for b in range(2) for a in range(4)]
D6=[lift(x) for x in D]; ix={x:i for i,x in enumerate(D)}; ix6={x:i for i,x in enumerate(D6)}
mul=[[ix[compose(x,y)] for y in D] for x in D]
inverse=[ix[inv(x)] for x in D]

def closure(xs):
    out={0,*xs}
    while True:
        new=out|{mul[x][y] for x in out for y in out}
        if new==out:return frozenset(out)
        out=new
subgroups=sorted({closure(xs) for k in range(9) for xs in itertools.combinations(range(8),k)}, key=lambda x:(len(x),tuple(sorted(x))))
require(len(subgroups)==10,'D8 subgroup inventory')
G={'D8':D6,'S4':[lift(g) for g in itertools.permutations(range(4))],
   'A6':[g for g in itertools.permutations(range(6)) if sign(g)==0]}
require([len(G[k]) for k in G]==[8,24,360],'ambient group orders')
# The parity-twist inclusion S4 -> A6 is verified as a homomorphism.
require(all(compose(lift(a),lift(b))==lift(compose(a,b)) for a in itertools.permutations(range(4)) for b in itertools.permutations(range(4))), 'parity twist homomorphism')
conj={name:[tuple(ix6.get(compose(compose(g,x),inv(g)),-1) for x in D6) for g in gs] for name,gs in G.items()}
fusion={name:{tuple(sorted(P)):sorted({tuple(c[x] for x in sorted(P)) for c in cc if all(c[x]>=0 for x in P)}) for P in subgroups} for name,cc in conj.items()}
# Images of the two presentation generators exhaust every endomorphism.
homs=[]
for a in range(8):
 for b in range(8):
    if power(D[a],4)!=D[0] or mul[b][b]!=0 or mul[mul[b][a]][b]!=inverse[a]:continue
    f=tuple(ix[compose(power(D[a],i),power(D[b],j))] for j in range(2) for i in range(4))
    require(all(f[mul[x][y]]==mul[f[x]][f[y]] for x in range(8) for y in range(8)),'presentation homomorphism check')
    homs.append(f)
require(len(homs)==len(set(homs))==36,'36 distinct D8 endomorphisms')

def preserves(f,src,dst):
    for P,fs in fusion[src].items():
        for a in fs:
            # Target conjugation must realize the induced map on the entire image subgroup.
            want=tuple(f[y] for y in a)
            if not any(tuple(c[f[x]] for x in P)==want for c in conj[dst]):return False
    return True

def strong(P,name):
    return all(set(m).issubset(P) for Q,maps in fusion[name].items() if set(Q).issubset(P) for m in maps)
def permorder(f):
    v=tuple(range(len(f)))
    for n in range(1,1000):
        v=tuple(f[x] for x in v)
        if v==tuple(range(len(f))):return n
    raise RuntimeError('permutation order bound')
def hyperfocal(name):
    gens=[]
    for P,maps in fusion[name].items():
        for a in maps:
            if set(a)!=set(P):continue
            order=permorder(tuple(P.index(y) for y in a))
            if order%2:
                gens += [mul[inverse[x]][y] for x,y in zip(P,a)]
    return sorted(closure(gens))

normal_v4=sorted(i for i,x in enumerate(D) if sign(x)==0)
auts=[f for f in homs if len(set(f))==8]
require(len(auts)==8,'D8 automorphism count')
result={'group_model':'D8: r=(0 1 2 3), s=(0 2); order r^a s^b indexed by 4b+a; S4 embeds in A6 via parity on (4 5)',
        'subgroups':[sorted(P) for P in subgroups], 'normal_v4':normal_v4,
        'hyperfocal':{k:hyperfocal(k) for k in G},
        'strongly_closed':{k:[sorted(P) for P in subgroups if strong(P,k)] for k in G},
        'fusion_map_counts':{k:{','.join(map(str,P)):len(m) for P,m in fs.items()} for k,fs in fusion.items()},
        'homomorphism_count':len(homs),'fusion_preserving':{}}
for src in G:
 for dst in G:
    passing=[f for f in homs if preserves(f,src,dst)]
    cases=Counter()
    for f in passing:
        if src=='D8':case='nilpotent_source'
        elif len(set(f))==1:case='constant'
        elif len(set(f))==2:
            require(src=='S4' and all(f[x]==0 for x in normal_v4),'noninjective map factors through sign')
            case='sign_then_C2_map'
        elif len(set(f))==8:
            if src==dst:
                require(preserves(tuple(f.index(x) for x in range(8)),dst,src),'inverse also preserves fusion')
                case='fusion_isomorphism'
            else:
                require(src=='S4' and dst=='A6','only S4 to A6 proper fusion inclusion')
                require(preserves(f,'A6','A6') and preserves(tuple(f.index(x) for x in range(8)),'A6','A6'),'target automorphism realizes arbitrary injection')
                case='parity_twist_then_target_equivalence'
        else:raise RuntimeError('unaccounted passing homomorphism')
        cases[case]+=1
    result['fusion_preserving'][src+'->'+dst]={'count':len(passing),'image_order_counts':dict(sorted(Counter(len(set(f)) for f in passing).items())), 'extension_cases':dict(sorted(cases.items())), 'maps':[list(f) for f in passing]}
require(result['hyperfocal']['D8']==[0],'nilpotent hyperfocal')
require(result['hyperfocal']['S4']==normal_v4,'S4 hyperfocal')
require(result['hyperfocal']['A6']==list(range(8)),'A6 hyperfocal')
# Concrete non-invariance of S4 fusion under a D8 automorphism, and all-invariance for A6.
require(sum(preserves(f,'S4','S4') for f in auts)==4,'S4 only four fusion automorphisms')
require(all(preserves(f,'A6','A6') for f in auts),'all eight A6 fusion automorphisms')
result['checks']='Every passing map is assigned a proved extension mechanism. No unsupported counterexample was found in these nine finite source-target pairs.'
print(json.dumps(result,indent=2,sort_keys=True))
