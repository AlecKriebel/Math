#!/usr/bin/env python3
"""Independent audit controls; do not import or execute the submitted check module.

Finite arithmetic supplements the written proof audit. It is not a solution of
any unbounded odd-characteristic sparse-support problem.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform
import sys
import sympy as S

HERE = Path(__file__).resolve().parent
PUBLIC = HERE.parent / 'public'
x, y = S.symbols('x y')
A, B = x**4 + 1, x**3 + x**2 + x
f = A*(y**2+1) + B*y
q, r, t = x*x-x+1, 2*x*x+3*x+2, 2*x**4-x**3-x*x-x+2
checks = 0

def require(statement):
    global checks
    checks += 1
    assert statement

def modzero(expr, p):
    return S.Poly(expr, x, y, modulus=p).is_zero

require(S.expand(B*B-4*A*A+q*r*t)==0)
require(S.expand(r-2*q-5*x)==0)
require(S.expand(t-(2*x*x+x-2)*q-4*(1-x))==0)
require(S.resultant(A, B, x)==1)
require(S.resultant(q, r, x)==25)
require(S.resultant(q, t, x)==16)
require(S.discriminant(q,x)==-3)
require(modzero(B*B-4*A*A+(x+1)**2*(x*x+1)*sum(x**j for j in range(5)), 3))
require(modzero(B*B-4*A*A-(x*x+1)*(x+1)**2*q*q,5))
require(S.simplify(x**4*f.subs(x,1/x)-f)==0)
require(S.simplify(y**2*f.subs(y,1/y)-f)==0)
W = A*(y+1)
require(modzero(W*W+B*W+A*B-A*f,2))
require(modzero(S.diff(f,x)-y*(x*x+1),2))
require(modzero(S.diff(f,y)-B,2))
require(modzero((x*x+1)+(x*x+x+1)-x,2))

primes=list(S.primerange(2,102))
for p in primes:
    require(S.degree(S.gcd(S.Poly(A,x,modulus=p),S.Poly(B,x,modulus=p)))==0)
    if p!=2:
        _, factors = S.factor_list(B*B-4*A*A, x, modulus=p)
        require(any(m%2 for factor,m in factors))

# Enumerate the entire abstract graph class used in the proof, not a coordinate box.
# Four distinct edges, two of each orientation, at most one edge of each
# orientation incident at a vertex. Include isolated vertices.
graphs=Counter()
for n in (4,5,6):
    for edges in combinations(list(combinations(range(n),2)),4):
        for horizontal in combinations(range(4),2):
            colors=[int(i in horizontal) for i in range(4)]
            incident=[[] for _ in range(n)]
            for i,(u,v) in enumerate(edges):
                incident[u].append((v,colors[i]));incident[v].append((u,colors[i]))
            if any(len({color for _,color in e})!=len(e) for e in incident):
                continue
            unseen=set(range(n));components=[]
            while unseen:
                stack=[unseen.pop()]; component=set(stack)
                while stack:
                    for v,_ in incident[stack.pop()]:
                        if v in unseen:
                            unseen.remove(v);component.add(v);stack.append(v)
                components.append(component)
            cycles=[c for c in components if all(len(incident[v])==2 for v in c)]
            if cycles:
                require(len(cycles)==1 and len(cycles[0])==4)
                require(all(len(c)==1 for c in components if c != cycles[0]))
                graphs[f'{n}_vertices_cycle']+=1
            else:
                require(len(components)==n-4 and len(components)<=2)
                graphs[f'{n}_vertices_forest']+=1

# Independent dense-array convolution and base-p projective enumeration in the
# SAME author-declared boxes. No assertion of an unbounded search.
F_terms=((0,0),(4,0),(0,2),(4,2),(1,1),(2,1),(3,1))
searches=[]
for p,dx,dy in ((2,4,2),(3,3,1),(5,2,1),(7,2,1)):
    positions=[(i,j) for j in range(dy+1) for i in range(dx+1)]
    n=len(positions); width=dx+5; height=dy+3
    hist=Counter()
    for first in range(n):
        for encoded in range(p**(n-first-1)):
            coeffs=[0]*n;coeffs[first]=1
            for idx in range(first+1,n):
                coeffs[idx]=encoded%p;encoded//=p
            out=[0]*(width*height)
            for coefficient,(i,j) in zip(coeffs,positions):
                for a,b in F_terms:
                    out[(j+b)*width+i+a]+=coefficient
            hist[sum(v%p!=0 for v in out)]+=1
    require(sum(hist.values())==(p**n-1)//(p-1))
    require(min(hist)==7)
    expected=json.loads((PUBLIC/'control-results.json').read_text())['bounded_sparse_multiples']['results'][len(searches)]
    require(dict(sorted(hist.items()))=={int(k):v for k,v in expected['support_histogram'].items()})
    searches.append({'prime':p,'x_degree':dx,'y_degree':dy,'projective_multipliers':sum(hist.values()),'minimum_support':min(hist),'histogram':dict(sorted(hist.items()))})

# Laurent differences include negative exponents. q=x^2+x+1 implies x^3=1,
# and y^2+1 implies y^4=1; retain all four quotient basis coefficients.
laurent_cases=0;vanish=0
for p in (3,5,7,11,13):
    for a in range(-30,31):
        xr=((1,0),(0,1),(-1,-1))[a%3]
        for b in range(-18,19):
            br=b%4; sign=1 if br<2 else -1; parity=br%2
            for c in range(1,p):
                coefficients=[0,0,0,0]
                coefficients[parity*2]=sign*xr[0]
                coefficients[parity*2+1]=sign*xr[1]
                coefficients[0]+=c
                actual=all(v%p==0 for v in coefficients)
                expected=(a%3==0 and b%2==0 and c==(-pow(-1,b//2,p))%p)
                require(actual==expected)
                laurent_cases+=1;vanish+=actual

out={'audit_scope':'independent finite controls, unchanged submitted boxes; no fresh proof-search approach',
'checks_passed':checks,'environment':{'python':sys.version,'platform':platform.platform(),'sympy':S.__version__},
'symbolic_resultants':{'resultant_A_B':1,'resultant_q_r':25,'resultant_q_t':16,'discriminant_q':-3},
'prime_samples':primes,'entire_abstract_four_edge_graph_class':dict(sorted(graphs.items())),
'bounded_sparse_replay':searches,'laurent_congruence_cases':laurent_cases,'laurent_congruence_vanishing':vanish,
'submitted_manifest_sha256':hashlib.sha256((PUBLIC/'SHA256SUMS').read_bytes()).hexdigest(),
'submitted_proof_sha256':hashlib.sha256((PUBLIC/'PROOF.md').read_bytes()).hexdigest()}
(HERE/'independent-results.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('environment','bounded_sparse_replay')},sort_keys=True,indent=2))
