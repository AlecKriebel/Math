#!/usr/bin/env python3
"""Independent bounded audit. Run from any directory; no author code is imported.

Reconstructs support orbits by two permutation generators; rejects cycles by
leaf removal; constructs canonical coefficients by anchored incidence propagation.
Rebuilds the full polynomial equations with their leading support factors and
computes saturation via Rabinowitsch elimination with exact QQ Groebner bases.
Only the claimed per-case outcomes, not the author's intermediate rounds, are
read from verification.json for comparison.
"""
from collections import deque, Counter
from functools import reduce
from itertools import product, permutations
from math import gcd
from pathlib import Path
import hashlib, json
import sympy as s

ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT.parent/'public'
FAMILIES=[(2,(0,1)),(3,(0,1,2)),(3,(0,2,1)),(4,(0,1,2,3)),(4,(0,2,1,3))]

def orbits(n,b):
    unseen=set(product(range(1,n),repeat=3)); result=[]
    while unseen:
        todo=[min(unseen)]; orbit=set(todo)
        while todo:
            a,c,d=todo.pop()
            for u in [(c,b[d],b[a]),(b[c],b[a],b[d])]:
                if u not in orbit: orbit.add(u); todo.append(u)
        assert orbit<=unseen
        result.append(sorted(orbit)); unseen-=orbit
    return result

def graph(n,edges):
    adj=[set() for _ in range(2*n)]
    for u,v in edges: adj[u].add(n+v);adj[n+v].add(u)
    work=[set(a) for a in adj]; leaves=deque(i for i,a in enumerate(work) if len(a)==1)
    while leaves:
        u=leaves.popleft()
        if len(work[u])!=1: continue
        v=work[u].pop();work[v].remove(u)
        if len(work[v])==1: leaves.append(v)
    return adj if not any(work) else None

def build(n,b,bits,obs):
    support={(0,j,j) for j in range(n)}|{(i,0,i) for i in range(n)}|{(i,b[i],0) for i in range(n)}
    for bit,o in zip(bits,obs):
        if bit: support.update(o)
    graphs=[]
    for k in range(n):
        g=graph(n,[(i,j) for a,j,i in support if a==k])
        if g is None: return None
        graphs.append(g)
    zero=(0,)*n
    A={};B={}
    for i,j,k in product(range(n),repeat=3):
        values=[0]*(2*n)
        if (k,j,i) in support:
            # Anchor on the opposite side of the source's chosen cut.
            anchor=i if (k!=0 and j==0) else n+j
            assigned={anchor:0}; todo=[anchor]
            while todo:
                u=todo.pop()
                for v in graphs[k][u]:
                    delta=int({u,v}=={i,n+j})
                    candidate=delta-assigned[u]
                    if v in assigned: assert assigned[v]==candidate
                    else: assigned[v]=candidate;todo.append(v)
            for u,value in assigned.items(): values[u]=value
        A[i,j,k]=tuple(values[:n]);B[i,j,k]=tuple(values[n:])
        for a,l,t in support:
            if a==k: assert values[t]+values[n+l]==int(t==i and l==j)
    C={(i,j,k):tuple(x+y for x,y in zip(A[i,b[j],k],B[i,b[j],k])) for i,j,k in product(range(n),repeat=3)}
    for t in product(range(n),repeat=3):
        if t not in support: assert C[t]==zero
    q=[tuple(int(i==j) for j in range(n)) for i in range(n)]
    monomials=[(i,j) for i in range(n) for j in range(i,n)]
    index={m:k for k,m in enumerate(monomials)}
    def times(a,c):
        v=[0]*len(monomials)
        for i,ai in enumerate(a):
            for j,cj in enumerate(c):
                v[index[tuple(sorted((i,j)))]]+=ai*cj
        return v
    equations=set()
    def add(*terms):
        v=[sum(term[k] for term in terms) for k in range(len(monomials))]
        if not any(v): return
        divisor=reduce(gcd,v)
        if next(x for x in v if x)!=abs(next(x for x in v if x)): divisor=-divisor
        equations.add(tuple(x//divisor for x in v))
    def neg(v): return [-x for x in v]
    def lin(*terms): return tuple(sum(term[k] for term in terms) for k in range(n))
    def scale(k,v): return tuple(k*x for x in v)
    for i in range(n): add(times(q[0],lin(q[i],scale(-1,q[b[i]]))))
    for a,c,d in product(range(n),repeat=3):
        # Source six expressions, independently transcribed.
        for u,v,w in [(c,b[d],b[a]),(b[d],a,b[c]),(b[c],b[a],b[d]),(b[a],d,c),(d,b[c],a)]:
            add(times(C[a,c,d],q[d]),neg(times(C[u,v,w],q[w])))
        add(times(q[0],lin(C[a,c,d],scale(-1,C[b[c],b[a],b[d]]))))
    for i,j in product(range(n),repeat=2):
        add(times(q[0],lin(C[i,j,0],scale(-int(i==b[j]),q[i]))))
        add(times(q[i],q[j]),*[neg(times(C[i,j,k],q[k])) for k in range(n)])
    for i,j,k,l in product(range(n),repeat=4):
        add(*[times(C[i,j,t],C[t,k,l]) for t in range(n)],*[neg(times(C[i,t,l],C[j,k,t])) for t in range(n)])
    for i,j,k,x,y,z in product(range(n),repeat=6):
        # Retain the leading polynomial, including zero factors on nonedges.
        if C[z,y,x]==zero: continue
        W1=lin(*[scale(A[j,k,z][t],C[t,i,x]) for t in range(n)],*[scale(B[j,k,z][t],C[t,i,y]) for t in range(n)])
        W2=lin(*[scale(A[b[i],j,b[x]][t],C[t,b[k],b[y]]) for t in range(n)],*[scale(B[b[i],j,b[x]][t],C[t,b[k],z]) for t in range(n)])
        W3=lin(*[scale(A[k,b[i],y][t],C[t,b[j],b[z]]) for t in range(n)],*[scale(B[k,b[i],y][t],C[t,b[j],b[x]]) for t in range(n)])
        add(times(C[z,y,x],lin(W1,scale(-1,W2))))
        add(times(C[z,y,x],lin(W1,scale(-1,W3))))
    symbols=s.symbols('d1:'+str(n)); qsymbols=(s.Integer(1),)+symbols
    E=[sum(v[k]*qsymbols[i]*qsymbols[j] for k,(i,j) in enumerate(monomials)) for v in sorted(equations)]
    H=[sum(v[j]*qsymbols[j] for j in range(n)) for v in set(q)|{C[t] for t in support}]
    return symbols,E,H,support

def reduced_basis(E,x):
    return s.groebner(E,*x,order='lex',domain=s.QQ)

def saturate(E,H,x):
    initial=reduced_basis(E,x)
    if list(initial)==[s.Integer(1)]: return initial, 'unit before localization'
    factors=set()
    for h in H:
        h=s.expand(initial.reduce(h)[1])
        if h==0: return reduced_basis([1],x), 'support factor in ideal'
        if h.free_symbols:
            h=s.Poly(h,*x,domain=s.QQ).monic().as_expr();factors.add(h)
    if not factors: return initial, 'all support factors units modulo ideal'
    t=s.Symbol('_inverse')
    G=reduced_basis(list(initial)+[1-t*s.prod(sorted(factors,key=str))],(t,)+x)
    elimination=[p for p in G if not p.has(t)]
    J=reduced_basis(elimination,x)
    return J,'Rabinowitsch elimination'

def main():
    claimed=json.loads((PUBLIC/'verification.json').read_text())
    expected={(c['rank'],tuple(c['involution']),c['bits']):c for c in claimed['cases']}
    output={'method':'Independent support/graph/equation reconstruction; full-factor QQ Groebner saturation via Rabinowitsch elimination','sympy_version':s.__version__,'cases':[],'families':[]}
    for n,b in FAMILIES:
        obs=orbits(n,b);summary={'rank':n,'involution':b,'patterns':2**len(obs),'forests':0,'nonempty':0,'empty':0};classes=set();dims=Counter()
        for bits in product((0,1),repeat=len(obs)):
            built=build(n,b,bits,obs)
            if built is None: continue
            summary['forests']+=1
            key=(n,b,''.join(map(str,bits)));c=expected.pop(key)
            x,E,H,support=built
            J,method=saturate(E,H,x)
            generators=list(J)
            if generators==[s.Integer(1)]:
                assert c['disposition']=='empty',key
                summary['empty']+=1
                dimension=None
            else:
                assert c['disposition']=='affine_open',key
                promised=[s.sympify(p,locals={str(v):v for v in x}) for p in c['affine_generators']]
                assert generators==list(reduced_basis(promised,x)),(key,generators,promised)
                assert all(s.Poly(p,*x).total_degree()==1 for p in generators),key
                assert all(J.reduce(h)[1]!=0 for h in H),key
                assert J.reduce(1+sum(x))[1]!=0,key
                dimension=len(x)-len(generators)
                assert dimension==c['dimension'],key
                dims[str(dimension)]+=1;summary['nonempty']+=1
                keys=[]
                for perm in permutations(range(1,n)):
                    p=(0,)+perm
                    if all(p[b[i]]==b[p[i]] for i in range(n)):
                        keys.append(tuple(sorted(tuple(p[i] for i in u) for u in support)))
                classes.add(min(keys))
            output['cases'].append({'rank':n,'involution':b,'bits':key[2],'saturated_generators':list(map(str,generators)),'dimension':dimension,'saturation_method':method,'distinct_full_polynomials':len(E)})
        summary['nonempty_label_classes']=len(classes);summary['dimensions']=dict(sorted(dims.items()));output['families'].append(summary)
        print(json.dumps(summary),flush=True)
    assert not expected
    output['status']='PASS';output['cases_checked']=len(output['cases'])
    payload=json.dumps(output,indent=2,sort_keys=True)+'\n';(ROOT/'independent_results.json').write_text(payload)
    print(json.dumps({'status':'PASS','cases':len(output['cases']),'sha256':hashlib.sha256(payload.encode()).hexdigest()}),flush=True)
if __name__=='__main__': main()
