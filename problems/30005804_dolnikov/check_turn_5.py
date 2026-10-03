"""Exact rational controls and a finite certificate for the rejected square lemma."""
from margin_geometry import *
from exact_geometry import masks
from random import Random
from functools import lru_cache
import json,sys
from pathlib import Path
from hashlib import sha256

rng=Random(580405)
assertions=0; cases=0; incidences=0; chosen=[0,0,0]
def ck(v):
    global assertions
    assertions+=1
    assert v

shapes=[[(0,0),(2,0),(0,2)],[(0,0),(3,0),(2,2),(0,1)],
        [(0,0),(2,0),(3,1),(1,3),(0,2)],[(0,0),(2,0),(2,2),(0,2)]]
parameters=[]
for raw in shapes:
    K=list(map(pt,raw)); D=difference(K)
    N,f,g,basis=normalize(K)
    for p in K: ck(g(f(p))==p)
    ck(longest_horizontal(N)[0]==1)
    ck(longest_horizontal(hull([(y,x) for x,y in N]))[0]==1)
    for lam in [F(1,5),F(1,2),F(3,4)]:
        lower,P=rectangle(N,lam)
        ck(row_span([x for x,y in P])==lam)
        ck(row_span([y for x,y in P])==1-lam)
        for _ in range(35):
            # A lattice in lambda*D; 0 remains an admissible point for B and C.
            U=[pt((lam*F(x,4),lam*F(y,4))) for x in range(-12,13)
               for y in range(-12,13)
               if inside(pt((F(x,4),F(y,4))),D)]
            A=rng.sample(U,rng.randrange(1,min(12,len(U))+1))
            Bpool=[b for b in U if all(inside((sub(a,b)[0]/lam,sub(a,b)[1]/lam),D) for a in A)]
            B=rng.sample(Bpool,rng.randrange(1,min(12,len(Bpool))+1))
            Cpool=[c for c in U if all(inside((sub(a,c)[0]/lam,sub(a,c)[1]/lam),D) for a in A+B)]
            C=rng.sample(Cpool,rng.randrange(1,min(12,len(Cpool))+1))
            colors=[A,B,C]; rng.shuffle(colors)
            i,Q,_=margin_piercing(K,colors,lam)
            chosen[i]+=1; ck(len(Q)<=3)
            for t in colors[i]:
                ck(any(inside(sub(q,t),K) for q in Q)); incidences+=1
            cases+=1
    parameters.append({'vertices':len(K),'basis':[[str(x) for x in p] for p in basis]})

# Ensure all three pigeonhole choices are tested, including different wide axes.
K=list(map(pt,[(0,0),(1,0),(1,1),(0,1)]))
base=[list(map(pt,[(-F(3,4),0),(F(3,4),0)])),
      list(map(pt,[(0,-F(3,4)),(0,F(3,4))])), [pt((0,0))]]
for j in range(3):
    colors=base[j:]+base[:j]
    i,Q,_=margin_piercing(K,colors,F(3,4)); chosen[i]+=1
    ck(all(any(inside(sub(q,t),K) for q in Q) for t in colors[i]))
ck(all(chosen))

# Finite witness to failure of the unsupported unit-square-cover lemma.
K=list(map(pt,[(F(1,2),0),(0,F(1,2)),(-F(1,2),0),(0,-F(1,2))]))
T=sorted({pt((F(i,4),F(j,4))) for i in range(5) for j in range(5)
          if i in (0,4) or j in (0,4)})
polys=[[(x+a,y+b) for x,y in K] for a,b in T]
coverage=masks(polys)
maximal=[a for a in coverage if not any(a!=b and a&b==a for b in coverage)]
bybit=[[a for a in maximal if a>>i&1] for i in range(len(T))]
@lru_cache(None)
def tau(S):
    if not S: return 0
    i=(S&-S).bit_length()-1
    return 1+min(tau(S&~a) for a in bybit[i])
ck(len(T)==16); ck(tau((1<<len(T))-1)==4)
D=difference(K);ck(not inside(pt((1,1)),D))
# Return a positive four-cover as well as the exact lower-bound recurrence.
S=(1<<len(T))-1; Q=[]
while S:
    i=(S&-S).bit_length()-1
    M=next(m for m in bybit[i] if tau(S&~m)==tau(S)-1)
    Q.append(coverage[M]); S &= ~M
ck(len(Q)==4)
ck(all(any(inside(sub(q,t),K) for q in Q) for t in T))
encode=lambda p:[str(x) for x in p]
cert={'body_vertices':list(map(encode,K)), 'boundary_points':list(map(encode,T)),
      'maximal_coverage_masks':[{'mask':m,'point':encode(coverage[m])} for m in sorted(maximal)],
      'optimal_cover':list(map(encode,Q)), 'minimum_cover_number':4,
      'scope':'Counterexample to the normalized square-cover lemma only; not to Dolnikov'}
b=(json.dumps(cert,indent=2,sort_keys=True)+'\n').encode()
p=Path(__file__).resolve().parent/'SQUARE_COVER_BARRIER.json'
if '--emit' in sys.argv: p.write_bytes(b)
ck(p.read_bytes()==b)
print(json.dumps({'assertions':assertions,'margin_configurations':cases,
                  'piercing_incidences':incidences,'chosen_colors':chosen,
                  'normalizations':parameters,'square_barrier':{'boundary_points':len(T),
                  'exact_cover_number':4,'maximal_masks':len(maximal),'dp_states':tau.cache_info().currsize,'certificate_sha256':sha256(b).hexdigest()},
                  'scope':'Exact finite controls; analytic factor-3/4 theorem and barrier proof in TURN_5.md; original unresolved'},
                 indent=2,sort_keys=True))
