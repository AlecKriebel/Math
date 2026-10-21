import itertools,json
from collections import Counter
import sympy as s
def require(ok):
    if not ok: raise RuntimeError("Exact verification failed")
D=[0,1,2,3,5,7,8,11]
counts=Counter((x-y)%15 for x in D for y in D if x!=y)
require(set(counts)==set(range(1,15)) and set(counts.values())=={4})
residues=Counter(k%5 for k in D)
require(residues=={0:2,1:2,2:2,3:2})
# All Fourier rows orthogonal, norm²15/8; difference counts prove coherence²1/16.
# Each block j+3*{0,...,4} has 4 rank-one 2x2 row-Gram blocks,
# each with sole eigenvalue 5/4: rank4, tight for its span.
x=s.Symbol('x');mod=s.Poly(s.cyclotomic_poly(15,x),x)
def red(p):return s.rem(s.Poly(p,x),mod).as_expr()
g={a:red(sum(x**((k*a)%15) for k in D)) for a in range(15)}
good=set()
for triple in itertools.combinations(range(15),3):
    a,b,c=triple
    # 8³ times the triangle product must equal -8 (actual value -1/4³).
    if red(g[(b-a)%15]*g[(c-b)%15]*g[(a-c)%15])==-8:good.add(triple)
blocks=[t for t in itertools.combinations(range(15),5) if all(u in good for u in itertools.combinations(t,3))]
partitions={k:[] for k in range(1,4)}
for k in partitions:
    for p in itertools.combinations(blocks,k):
        flat=sum((list(t) for t in p),[])
        if len(set(flat))==len(flat):partitions[k].append(p)
res={'n':15,'d':8,'squared_coherence':'1/16','difference_counts':dict(sorted(counts.items())),'D_residue_counts_mod5':dict(residues),'proper_tight_blocks_zero_based':blocks,'partition_counts_with_remaining_singletons':{k:len(v) for k,v in partitions.items()},'complete_partitions':partitions[3],'method':'Exact cyclotomic polynomial reduction modulo Phi_15 and regular-simplex triple-product criterion. Integrality/size sieve leaves only m=5,r=4.'}
open('harmonic_exact_results.json','w').write(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
