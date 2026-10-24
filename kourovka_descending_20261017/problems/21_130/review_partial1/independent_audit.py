#!/usr/bin/env python3
"""Fresh reproduction of bounded partial certificates; never a universal solver.

No imports from the author/search verifier modules. Does not mutate their files.
"""
from pathlib import Path
from itertools import combinations, permutations, product
from collections import Counter
from fractions import Fraction
from math import comb, factorial, prod
import datetime, hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SNAP = HERE / 'snapshot'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def hcycles(n):
    return [(0,) + p for p in permutations(range(1,n)) if p[0] < p[-1]]

def edges(c):
    return {frozenset((c[i],c[(i+1)%len(c)])) for i in range(len(c))}

def first_moment_and_lll():
    probability=[]; canonical=[]
    for n in range(4,9):
        cs=hcycles(n)
        k=sum({frozenset((0,1)),frozenset((2,3))} <= edges(c) for c in cs)
        need(Fraction(k,len(cs))==Fraction(4,(n-1)*(n-2)), 'pair probability')
        probability.append({'n':n,'cycles':len(cs),'pair_inclusions':k})
    for n in range(4,8):
        modulus=n if n%2 else n+1
        ec={frozenset(e):sum(e)%modulus for e in combinations(range(n),2)}
        targets=[(e,f) for e,f in combinations(ec,2) if ec[e]==ec[f]]
        templates=[(e,f) for e,f in combinations(edges(tuple(range(n))),2) if not e&f]
        T=len(targets); Q=n*(n-3)//2
        need(len(templates)==Q,'template-pair count')
        R=[sum(v in e or v in f for e,f in targets) for v in range(n)]
        event_supports=[]
        for e,f in templates:
            domain=tuple(sorted(e|f))
            for g,h in targets:
                image=tuple(sorted(g|h));maps=0
                for p in permutations(image):
                    d=dict(zip(domain,p))
                    if {frozenset(d[v] for v in e),frozenset(d[v] for v in f)}=={g,h}:
                        event_supports.append((frozenset(domain),frozenset(image)))
                        maps+=1
                need(maps==8,'not eight edge-respecting maps')
        for v in range(n):
            need(sum(v in d for d,i in event_supports)==16*(n-3)*T,'domain support count')
            need(sum(v in i for d,i in event_supports)==8*Q*R[v],'image support count')
        bound=64*(n-3)*T+32*Q*max(R,default=0)
        largest=max((sum(bool(d&e or i&j) for e,j in event_supports) for d,i in event_supports),default=0)
        need(largest<=bound,'closed support-neighborhood bound')
        canonical.append({'n':n,'cyclic_group_order':modulus,'T':T,'Q':Q,'R':R,
                          'canonical_events':len(event_supports),'max_closed_neighborhood':largest,'bound':bound})
    return {'pair_probability':probability,'canonical_counts':canonical}

def det(a):
    if not a:return 1
    # Fraction-free Bareiss elimination, independently from the author's minors.
    b=[r[:] for r in a]; sign=1; previous=1
    for k in range(len(b)-1):
        r=next((r for r in range(k,len(b)) if b[r][k]),None)
        if r is None:return 0
        if r!=k:b[k],b[r]=b[r],b[k];sign=-sign
        pivot=b[k][k]
        for i in range(k+1,len(b)):
            for j in range(k+1,len(b)):
                top=b[i][j]*pivot-b[i][k]*b[k][j]
                need(top%previous==0,'nonexact Bareiss division')
                b[i][j]=top//previous
            b[i][k]=0
        previous=pivot
    return sign*b[-1][-1]

def laplacian():
    reports=[]
    for k in range(1,6):
        examples=cofactors=0;maximum=0
        for pi in permutations(range(k)):
            for sigma in permutations(range(k)):
                out=[[] for _ in range(k)]
                for i in range(k):out[sigma[i]] += [i,pi[i]]
                need(all(sum(v in [x] for r in out for x in r)==2 for v in range(k)),'not balanced')
                reach=[]
                for v in range(k):
                    seen={v};todo=[v]
                    while todo:
                        a=todo.pop()
                        for b in out[a]:
                            if b not in seen:seen.add(b);todo.append(b)
                    reach.append(seen)
                blocks=[];unused=set(range(k))
                while unused:
                    v=min(unused);C={w for w in unused if w in reach[v] and v in reach[w]}
                    blocks.append(sorted(C));unused-=C
                need(all(all(w in C for v in C for w in out[v]) for C in blocks),'intercomponent arc')
                for C in blocks:
                    if len(C)==1:continue
                    m=len(C);loc={v:i for i,v in enumerate(C)}
                    L=[[2*int(i==j)-out[v].count(w) for j,w in enumerate(C)] for i,v in enumerate(C)]
                    for root in C:
                        J=[i for i,v in enumerate(C) if v!=root]
                        co=det([[L[i][j] for j in J] for i in J]);trees=0
                        nonroot=[v for v in C if v!=root]
                        for choices in product((0,1),repeat=m-1):
                            succ={v:out[v][choice] for v,choice in zip(nonroot,choices)}
                            good=True
                            for v in nonroot:
                                seen=set()
                                while v!=root:
                                    if v in seen:good=False;break
                                    seen.add(v);v=succ[v]
                                if not good:break
                            trees+=good
                        need(co==trees and 1<=co<=2**(m-1),'directed cofactor count/bound')
                        maximum=max(maximum,co);cofactors+=1
                if all(len(C)==1 for C in blocks):need(pi==tuple(range(k)),'nonidentity singleton blocks')
                examples+=1
        reports.append({'k':k,'permutation_pairs':examples,'cofactors_compared':cofactors,'max_cofactor':maximum})
    return reports

def vandermonde(a):
    return prod(b-a[i] for j,b in enumerate(a) for i in range(j))

def polynomial_second_grid():
    reports=[]
    for n,expected in ((3,6),(5,980),(7,2292864),(9,87215071680)):
        # The integer grid is deliberately different from (0,1,...,n-1).
        grid=tuple(i*i+i for i in range(n));total=0;nonzero=0
        for c in hcycles(n):
            s=[grid[c[i]]+grid[c[(i+1)%n]] for i in range(n)]
            if len(set(s))<n:continue
            sign=(-1)**sum(c[i]>c[j] for i in range(n) for j in range(i+1,n))
            total += sign*vandermonde(s);nonzero+=1
        # For odd n the sign product is fixed under the 2n dihedral actions.
        numerator=(-1)**comb(n,2)*(2*n)*total
        denominator=vandermonde(grid)
        need(numerator%denominator==0,'nonintegral second-grid coefficient')
        value=numerator//denominator
        need(value==expected,'polynomial coefficient disagreement')
        reports.append({'n':n,'grid':grid,'unoriented_rooted_cycles':factorial(n-1)//2,
                        'nonzero_terms':nonzero,'coefficient':value,'quotient_exact':True})
    return reports

def encoded_sum(a,b,mods):
    answer=0;stride=1
    for m in mods:
        answer+=((a//stride+b//stride)%m)*stride;stride*=m
    return answer

def certificates():
    groups={'C3':(3,),'C5':(5,),'C7':(7,),'C9':(9,),'C3xC3':(3,3),'C11':(11,),'C13':(13,),'C15':(15,)}
    manifest=json.loads((HERE/'REVIEWED_MANIFEST.json').read_text())
    frozen={x['path']:x['sha256'] for x in manifest['files']}
    reports=[]
    for name,mods in groups.items():
        rel='finite_search/exhaustive_order15/'+name+'.jsonl';f=ROOT/rel
        raw=f.read_bytes();sha=hashlib.sha256(raw).hexdigest();need(sha==frozen[rel],'certificate changed since freeze')
        lines=raw.decode().splitlines();header=json.loads(lines[0]);q=prod(mods)
        need(header['moduli']==list(mods) and header['order']==q,'group header')
        histogram=Counter();seen=set()
        for line in lines[1:]:
            r=json.loads(line);m=r['mask'];c=r['cycle'];n=len(c)
            need(type(m)is int and 0<m<2**q and m%2==1 and m not in seen,'subset mask')
            need(all(type(v)is int and 0<=v<q for v in c),'vertex domain')
            need(n>2 and len(set(c))==n and sum(2**v for v in c)==m and c[0]==0,'cyclic enumeration')
            colors=[encoded_sum(c[i],c[(i+1)%n],mods) for i in range(n)]
            need(len(set(colors))==n,'repeated color')
            seen.add(m);histogram[n]+=1
        need(len(seen)==2**(q-1)-q,'wrong complete-domain count')
        need(all(histogram[n]==comb(q-1,n-1) for n in range(3,q+1)),'wrong size coverage')
        # With membership, no duplicates, and exact cardinality this proves full coverage.
        reports.append({'group':name,'order':q,'witnesses':len(seen),'counts':dict(sorted(histogram.items())),'sha256':sha})
    return reports

def trap():
    old=json.loads((SNAP/'switching/local_landscape_result.json').read_text())['strict_improvement_trap']
    c=old['cycle'];E=edges(c);neighbors=set();n=len(c)
    # Independent edge-set construction: replace each disjoint pair by each pairing,
    # then retain connected 2-regular graphs; this also distinguishes the disconnected reconnection.
    for e,f in combinations(E,2):
        if e&f:continue
        a,b=tuple(e);d,h=tuple(f)
        for pairing in ((frozenset((a,d)),frozenset((b,h))),(frozenset((a,h)),frozenset((b,d)))):
            H=(E-{e,f})|set(pairing)
            if len(H)!=n:continue
            adjacency={v:set() for v in c}
            for u,v in H:adjacency[u].add(v);adjacency[v].add(u)
            if any(len(z)!=2 for z in adjacency.values()):continue
            seen={c[0]};todo=[c[0]]
            while todo:
                for v in adjacency[todo.pop()]:
                    if v not in seen:seen.add(v);todo.append(v)
            if len(seen)==n and H!=E:neighbors.add(frozenset(H))
    histogram=Counter(len({sum(e)%7 for e in H}) for H in neighbors)
    need(len(neighbors)==9 and max(histogram)==5,'strict two-opt trap')
    need({frozenset(edges(m['cycle'])) for m in old['moves']}==neighbors,'stored neighbor convention')
    witness=old['rainbow_witness'];need(set(witness)==set(c) and len({sum(e)%7 for e in edges(witness)})==n,'rainbow trap witness')
    return {'neighbors':len(neighbors),'score_histogram':dict(sorted(histogram.items())),'rainbow_witness_valid':True}

def main():
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'bounded partial audit; no full resolution',
            'first_moment_and_lll':first_moment_and_lll(),'laplacian':laplacian(),
            'polynomial_second_grid':polynomial_second_grid(),'finite_certificates':certificates(),'trap':trap(),'passed':True}
    (HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
