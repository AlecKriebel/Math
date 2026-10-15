"""Finite exact sanity and fault checks, not a proof or enumeration of the theorem."""
from pathlib import Path
from itertools import product
import hashlib, json, datetime, subprocess
OUT=Path(__file__).resolve().parent

def reduce_word(w):
    s=[]
    for x in w:
        if s and s[-1]==-x:s.pop()
        else:s.append(x)
    return tuple(s)
def inv(w):return tuple(-x for x in reversed(w))
def eval_insert(u,blocks):
    v=[]
    for j,b in enumerate(blocks):
        v.extend(b)
        if j<len(u):v.append(u[j])
    return tuple(v)
def insertion_rhs(u,blocks,wrong=False):
    r=[]
    for j,b in enumerate(blocks):
        p=u[:j];r.extend(b if wrong else p+b+inv(p))
    return reduce_word(r)
blocks=[()]+[w for k in [1,2] for w in product([1,2],repeat=k)]
count=0;proper=0;wrong_witness=None
for m in range(4):
    for u in product([1,2],repeat=m):
        for bs in product(blocks,repeat=m+1):
            lhs=reduce_word(eval_insert(u,bs)+inv(u))
            assert lhs==insertion_rhs(u,bs)
            count+=1;proper+=any(bs)
            if wrong_witness is None and lhs!=insertion_rhs(u,bs,True):wrong_witness={'u':u,'blocks':bs,'correct':lhs,'fault_no_conjugation':insertion_rhs(u,bs,True)}
assert wrong_witness

def pair(x,y,g):
    mask=(1<<g)-1
    return (((x&mask)&(y>>g)).bit_count()+((x>>g)&(y&mask)).bit_count())%2
parity_count=0
for g in range(1,7):
    for x in range(1<<(2*g)):
        assert pair(x,x,g)==0;parity_count+=1

# Oriented ribbon chain: vertex i is the crossing between curves i and i+1.
def ribbon_chain(k):
    darts=[];sigma={};alpha={}
    for i in range(1,k):
        cyclic=[(i,i,1),(i+1,i,1),(i,i,-1),(i+1,i,-1)]
        darts+=cyclic
        sigma.update({x:cyclic[(j+1)%4] for j,x in enumerate(cyclic)})
    for c in range(1,k+1):
        vertices=[i for i in range(1,k) if c in [i,i+1]]
        for j,i in enumerate(vertices):
            nxt=vertices[(j+1)%len(vertices)]
            a=(c,i,1);b=(c,nxt,-1);alpha[a]=b;alpha[b]=a
    assert all(alpha[alpha[d]]==d for d in darts)
    seen=set();b=0
    for d in darts:
        if d not in seen:
            b+=1;x=d
            while x not in seen:seen.add(x);x=sigma[alpha[x]]
    v=k-1;e=len(darts)//2;chi=v-e
    gen=(2-b-chi)//2
    assert 2-2*gen-b==chi
    return {'curves':k,'vertices':v,'edges':e,'boundary_components':b,'genus':gen}
ribbons=[ribbon_chain(k) for k in range(2,13)]
for r in ribbons:
    k=r['curves'];assert r['genus']==k//2 and r['boundary_components']==(1 if k%2==0 else 2)
# Fault check: an intersection graph alone loses ribbon order. Reverse alternating
# pattern at one vertex to noncrossing pairings; the neighborhood topology changes.
def fault_one_crossing():
    cyc=[0,1,2,3];edge={0:2,2:0,1:3,3:1}
    def faces(cyc):
        sig={x:cyc[(j+1)%4] for j,x in enumerate(cyc)};seen=set();n=0
        for x in cyc:
            if x not in seen:
                n+=1
                while x not in seen:seen.add(x);x=sig[edge[x]]
        return n
    return {'alternating_boundary_count':faces([0,1,2,3]),'fault_nonalternating_boundary_count':faces([0,2,1,3])}
ribbon_fault=fault_one_crossing();assert ribbon_fault['alternating_boundary_count']!=ribbon_fault['fault_nonalternating_boundary_count']
# Length/support fault: known even chains already contradict N_g as a length bound.
length_fault=[{'g':g,'support':2*g,'chain_length':4*g*(2*g+1),'coarse_support_bound':(1<<(2*g))*(3*g-2)+1} for g in [1,2,3]]
assert length_fault[0]['chain_length']>length_fault[0]['coarse_support_bound']
# Isolated circular support component requires a 2-valent vertex and is an annulus.
assert ribbon_fault == {'alternating_boundary_count':1,'fault_nonalternating_boundary_count':3}
isolated_circle={'vertices':1,'edges':1,'boundary_components':2,'genus':0}
assert isolated_circle['vertices']-isolated_circle['edges']==2-2*isolated_circle['genus']-isolated_circle['boundary_components']
# Concurrent lines y=j*x can be perturbed to y=j*x+j^2/M. For distinct i,j,
# the crossing is (-[i+j]/M,-i*j/M); sum and product identify the unordered pair,
# so there are no triple crossings. All crossings remain in the small strip.
from fractions import Fraction
multicrossing=[]
for n in range(2,17):
    M=100*n*n
    pts=[(Fraction(-(i+j),M),Fraction(-i*j,M)) for i in range(1,n+1) for j in range(i+1,n+1)]
    assert len(set(pts))==n*(n-1)//2 and all(abs(x)<Fraction(1,10) and abs(y)<Fraction(1,10) for x,y in pts)
    multicrossing.append({'curves':n,'double_crossings':len(pts),'triple_crossings':0})
manifest=json.loads((OUT/'inputs/git/MANIFEST.json').read_text())
checks=[]
for e in manifest['entries']:
    b=(OUT/'inputs/git'/e['file']).read_bytes();ok=len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'];assert ok
    checks.append({'file':e['file'],'verified':ok})
result={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'insertion_cases':count,'proper_insertion_cases':proper,'missing_conjugation_fault_witness':wrong_witness,'mod2_self_pairing_cases':parity_count,'ribbon_chain_sanity':ribbons,'ribbon_order_fault':ribbon_fault,'support_is_not_length_fault':length_fault,'isolated_circle_sanity':isolated_circle,'multicrossing_exact_sanity':multicrossing,'manifest_checks':checks,'limitations':'These finite exact checks catch transcription and encoding faults. They do not prove Higman, surface-orbit finiteness, Dehn-twist identities, or the theorem by enumeration.'}
(OUT/'SANITY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
