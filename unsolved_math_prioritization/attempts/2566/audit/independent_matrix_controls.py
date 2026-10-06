#!/usr/bin/env python3
"""Independent audit control: canonical projective matrices, no imports of release checker."""
from itertools import product
from collections import Counter
import json
p=7
I=(1,0,0,1)
def canonical(m):
    k=next(x for x in m if x)
    s=pow(k,-1,p)
    return tuple(x*s%p for x in m)
def det(m):
    a,b,c,d=m
    return (a*d-b*c)%p
def multiply(x,y):
    a,b,c,d=x; e,f,g,h=y
    return canonical(((a*e+b*g)%p,(a*f+b*h)%p,(c*e+d*g)%p,(c*f+d*h)%p))
def inverse(m):
    a,b,c,d=m
    return canonical((d,(-b)%p,(-c)%p,a))
G=tuple(sorted({canonical(m) for m in product(range(p),repeat=4) if det(m)}))
lookup={g:i for i,g in enumerate(G)}
table=[[lookup[multiply(g,h)] for h in G] for g in G]
e=lookup[I]
inv=[lookup[inverse(g)] for g in G]
def closure(generators):
    S={e}; Q=[e]
    for x in Q:
        for g in generators:
            y=table[g][x]
            if y not in S:
                S.add(y); Q.append(y)
    return frozenset(S)
N=frozenset(i for i,g in enumerate(G) if det(g) in {1,2,4})
orders=[len(closure([i])) for i in range(len(G))]
r=next(i for i in range(len(G)) if orders[i]==8)
s=next(i for i in range(len(G)) if orders[i]==2 and table[table[i][r]][i]==inv[r] and i not in closure([r]))
H=closure([r,s]); A=H&N
outside_orders=Counter(len(closure([r,s,x])) for x in range(len(G)) if x not in H)
# Enumerate the full interval [A,N], not merely one-generator extensions of A.
subgroups={A}; queue=[A]
for U in queue:
    for x in N-U:
        V=closure([*U,x])
        if V not in subgroups:
            subgroups.add(V); queue.append(V)
pi_groups={U for U in subgroups if len(U)%7!=0}
max_pi=[U for U in pi_groups if not any(U<V for V in pi_groups)]
conjugate=lambda U,g:frozenset(table[table[inv[g]][x]][g] for x in U)
assert len(G)==336 and len(N)==168 and len(H)==16 and len(A)==8
assert all(conjugate(N,g)==N for g in range(len(G)))
assert outside_orders=={336:320}
assert sorted(map(len,max_pi))==[24,24]
assert conjugate(max_pi[0],r)==max_pi[1]
# Independent affine-permutation model of the odd Frobenius control.
F={tuple((pow(2,b,p)*x+a)%p for x in range(p)) for a in range(p) for b in range(3)}
C={tuple(pow(2,b,p)*x%p for x in range(p)) for b in range(3)}
def pm(u,v): return tuple(u[v[x]] for x in range(p))
def pinv(u): return tuple(u.index(x) for x in range(p))
normalizer={u for u in F if {pm(pm(pinv(u),v),u) for v in C}==C}
assert len(F)==21 and len(C)==3 and normalizer==C
report={'representation':'PGL(2,7) canonical 2x2 matrices modulo scalars; full overgroup interval enumerated',
'G_order':len(G),'N_order':len(N),'H_order':len(H),'A_order':len(A),'r_matrix':G[r],'s_matrix':G[s],
'outside_extension_order_histogram':dict(outside_orders),'all_overgroup_interval_orders':dict(Counter(map(len,subgroups))),
'pi_overgroup_interval_orders':dict(Counter(map(len,pi_groups))),'maximal_pi_overgroups':len(max_pi),'outer_generator_swaps_two':True,
'frobenius_representation':'affine permutations x -> 2^b*x+a on F7','frobenius_order':len(F),'complement_order':len(C),'normalizer_order':len(normalizer)}
print(json.dumps(report,indent=2,sort_keys=True))
