"""Deterministic identity checks; not an exhaustive proof of the conjecture."""
from collections import Counter
from fractions import Fraction as F
from itertools import product, permutations
import json
results=[]
for p in (5,7):
    tested=0
    for c in product(range(4), repeat=p):
        if c[0]!=0: continue # Enough for regression, not claimed full search.
        n=Counter(c); D=sum(v*(v-1) for v in n.values()); counts=Counter(); P=T=W=H=0
        for a in range(p):
            for d in range(1,p):
                v=[c[(a+j*d)%p] for j in range(4)]
                counts[tuple(sorted(Counter(v).values(),reverse=True))]+=1
                P+=sum(v[i]==v[j] and v[k]==v[l] for i,j,k,l in ((0,1,2,3),(0,2,1,3),(0,3,1,2)))
                T+=sum(len({v[j] for j in range(4) if j!=omit})==1 for omit in range(4))
                W+=len(set(v))==1
                for mask in (1,2,3):
                    H+=(-1)**sum((z&mask).bit_count() for z in v)
        R=counts[(1,1,1,1)]
        assert R==p*(p-1)-6*D+P+2*T-6*W
        assert 4*R==p*(p-1)+H-4*P+8*W
        tested+=1
    results.append({'p':p,'colorings_tested':tested,'count_and_walsh_identities':'passed'})
p=10007
n=[p//4+(i<p%4) for i in range(4)]
ks=list({k for k in product(range(5),repeat=4) if sum(k)==4 and k!=(1,1,1,1)})
types={tuple(sorted(k,reverse=True)) for k in ks}
type_weights={(2,1,1,0):F(59,100),(2,2,0,0):F(35,100),(3,1,0,0):F(5,100),(4,0,0,0):F(1,100)}
weights={k:type_weights[tuple(sorted(k,reverse=True))]/sum(tuple(sorted(l,reverse=True))==tuple(sorted(k,reverse=True)) for l in ks) for k in ks}
Q=[[F(n[i]*(n[j]-(i==j)),p*(p-1)) for j in range(4)] for i in range(4)]
Delta=[[x-F(1,16) for x in row] for row in Q]
for i in range(4):
    for j in range(i+1,4):
        k=tuple(3*(h==i)+(h==j) for h in range(4)); weights[k]+=4*Delta[i][j]
    k=tuple(4*(h==i) for h in range(4)); weights[k]+=Delta[i][i]-2*sum(Delta[i][j] for j in range(i+1,4))
assert sum(weights.values())==1 and min(weights.values())>0
assert all(sum(w*F(k[i]*(k[j]-(i==j)),12) for k,w in weights.items())==Q[i][j] for i in range(4) for j in range(4))
results.append({'p':p,'exact_pair_marginal_construction':'passed','minimum_count_vector_weight':str(min(weights.values()))})
print(json.dumps(results,indent=2))
