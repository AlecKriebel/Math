#!/usr/bin/env python3
"""Independent finite diagnostics. No imports from the author certificate."""
import itertools as it
import json
import math
from collections import Counter
from functools import lru_cache


def need(test, text):
    if not test:
        raise RuntimeError(text)


def hpoly(f):
    n = len(f)
    polynomial = [0] * (n + 1)
    # Expand each (t-1)^r by repeated polynomial multiplication.
    for j, count in enumerate([1] + f):
        term = [count]
        for _ in range(n-j):
            nxt = [0] * (len(term)+1)
            for k, a in enumerate(term):
                nxt[k] -= a
                nxt[k+1] += a
            term = nxt
        for k, a in enumerate(term):
            polynomial[k] += a
    return polynomial[::-1]


def modified_h(f):
    d = len(f)-1
    h = hpoly(f)
    result = h[:]
    alternating = 0
    for k in range(1,d+1):
        beta = 0 if k == 1 else math.comb(d,k-1)
        alternating = beta - alternating
        result[k] -= math.comb(d+1,k)*alternating
    result[-1] = 1
    return result


def orbit(vs,q):
    # Minimize over EVERY anchor, rather than the author's first-vertex normal form.
    return min((sum(a)%q,tuple(sorted(tuple(x-y for x,y in zip(v,a)) for v in vs))) for a in vs)


def lift(key):
    residue, offsets = key
    return tuple((v[0]+residue,)+v[1:] for v in offsets)


@lru_cache(maxsize=None)
def lower_keys(key,q):
    vs=lift(key)
    return frozenset((size,orbit(face,q)) for size in range(1,len(vs)+1)
                     for face in it.combinations(vs,size))


def f2_rank(columns):
    # Sparse-set elimination, distinct from the author's integer-bit pivots.
    basis={}
    for c in columns:
        v=set(c)
        while v:
            p=min(v)
            if p not in basis:
                basis[p]=v
                break
            v.symmetric_difference_update(basis[p])
    return len(basis)


def quotient(d,q):
    levels=[set() for _ in range(d+1)]
    for residue in range(q):
        for order in it.permutations(range(d)):
            v=[residue]+[0]*(d-1)
            simplex=[tuple(v)]
            for i in order:
                v[i]+=1;simplex.append(tuple(v))
            for k in range(1,d+2):
                for face in it.combinations(simplex,k):
                    need(len({sum(v)%q for v in face})==k,'nonembedded cell')
                    levels[k-1].add(orbit(face,q))
    levels=[sorted(x) for x in levels]
    idx=[{x:i for i,x in enumerate(xs)} for xs in levels]
    boundaries=[[]]
    for k,level in enumerate(levels):
        columns=[]
        for cell in level:
            vs=lift(cell)
            # Explicit subset-incidence equivalence verifies the whole Boolean interval.
            subsets={}
            for size in range(1,k+2):
                for inds in it.combinations(range(k+1),size):
                    key=orbit(tuple(vs[i] for i in inds),q)
                    need(key in idx[size-1],'missing lower face')
                    need((size,key) not in subsets,'noninjective lower interval')
                    subsets[size,key]=frozenset(inds)
            need(len(subsets)==2**(k+1)-1,'bad Boolean interval')
            for (usize,upper),us in subsets.items():
                lowers=lower_keys(upper,q)
                for lower,ls in subsets.items():
                    need((lower in lowers)==(ls<=us),'Boolean incidence mismatch')
            if k:
                columns.append({idx[k-1][orbit(face,q)] for face in it.combinations(vs,k)})
        if k:boundaries.append(columns)
    for k in range(2,d+1):
        for c in boundaries[k]:
            v=set()
            for i in c:v.symmetric_difference_update(boundaries[k-1][i])
            need(not v,'boundary square')
    ridge=Counter(x for c in boundaries[d] for x in c)
    need(set(ridge)==set(range(len(levels[d-1]))) and set(ridge.values())=={2},'ridge multiplicity')
    f=[len(x) for x in levels]
    ranks=[0]+[f2_rank(c) for c in boundaries[1:]]+[0]
    betti=[f[k]-ranks[k]-ranks[k+1] for k in range(d+1)]
    need(betti==[math.comb(d,k) for k in range(d+1)],'homology mismatch')
    hd=modified_h(f)
    need(f[-1]==q*math.factorial(d),'facet volume count')
    need(hd==hd[::-1] and min(hd)>=0,'modified h constraints')
    need(f[-1]==math.comb(2*d,d)+sum(hd[1:-1]),'homological facet identity')
    return {'dimension':d,'index':q,'f_vector':f,'h_double_prime':hd,'betti_mod_2':betti,
            'cell_count':sum(f),'boundary_squared_zero':True,'ridge_incidence_two':True,'boolean_intervals':True}


def colored_dipole_control():
    d=3;q=4
    tetra=set()
    for r in range(q):
        for order in it.permutations(range(d)):
            v=[r,0,0];vs=[tuple(v)]
            for a in order:v[a]+=1;vs.append(tuple(v))
            tetra.add(orbit(vs,q))
    tetra=sorted(tetra);ridges={}
    for i,t in enumerate(tetra):
        for tri in it.combinations(lift(t),3):
            key=orbit(tri,q);color=next(iter(set(range(4))-{sum(v)%4 for v in tri}))
            ridges.setdefault((key,color),[]).append(i)
    graph={i:{} for i in range(len(tetra))}
    for (_,c),owners in ridges.items():
        need(len(owners)==2,'dual ridge owner count')
        a,b=owners;graph[a][c]=b;graph[b][c]=a
    def comps(g,omit):
        unseen=set(g);out=[]
        while unseen:
            component={unseen.pop()};todo=list(component)
            while todo:
                v=todo.pop()
                for c,w in g[v].items():
                    if c!=omit and w in unseen:unseen.remove(w);component.add(w);todo.append(w)
            out.append(component)
        return out
    need(all(len(comps(graph,c))==1 for c in range(4)),'starting graph not contracted')
    original={v:dict(a) for v,a in graph.items()}
    u=0;c=0;x=len(graph);y=x+1;graph[x]={c:y};graph[y]={c:x}
    for color in range(1,4):
        neighbor=graph[u][color]
        graph[u][color]=x;graph[x][color]=u
        graph[neighbor][color]=y;graph[y][color]=neighbor
    components=[comps(graph,c) for c in range(4)]
    need([len(v) for v in components]==[2,1,1,1],'expanded color components')
    need(not any(x in comp and y in comp for comp in components[0]),'not a dipole')
    for v,adj in graph.items():
        need(set(adj)==set(range(4)),'not a colored matching graph')
        for c,w in adj.items():need(w!=v and graph[w][c]==v,'bad matching symmetry')
    for c in range(1,4):
        a=graph[x][c];b=graph[y][c];graph[a][c]=b;graph[b][c]=a
    del graph[x];del graph[y]
    need(graph==original,'dipole cancellation failed exact restoration')
    return {'original_facets':24,'expanded_facets':26,'expanded_color_deleted_components':[2,1,1,1],
            'expanded_vertices':5,'recovered_graph_exactly':True,
            'scope':'One explicit inverse/cancellation diagnostic; the universal reduction relies on the audited dipole theorem.'}


def main():
    arithmetic=0
    for d in range(1,151):
        corrections=[]
        for k in range(1,d+1):
            s=sum((-1)**(k-1-j)*math.comb(d,j) for j in range(1,k))
            need(s==math.comb(d-1,k-1)-(-1)**(k-1),'alternating sum')
            corrections.append(math.comb(d+1,k)*s);arithmetic+=1
        need(1+(-1)**(d+1)+sum(corrections)==math.comb(2*d,d),'constant term identity');arithmetic+=1
    # Enumerate by facet count first and all vertex counts permitted by h''_1.
    candidates=[]
    for F in range(1,24):
        for v in range(4,30):
            f=[v,v+F,2*F,F];hd=modified_h(f)
            if min(hd)<0 or hd!=hd[::-1]:continue
            if v==4:continue # external contracted theorem, not a numerical proof
            candidates.append({'f_vector':f,'h_double_prime':hd})
    need(candidates==[{'f_vector':[5,27,44,22],'h_double_prime':[1,1,0,1,1]},
                     {'f_vector':[5,28,46,23],'h_double_prime':[1,1,1,1,1]}],'candidate set')
    facets=list(it.combinations(range(5),4));triangles=list(it.combinations(range(5),3))
    columns=[{i for i,t in enumerate(triangles) if set(t)<=set(f)} for f in facets]
    cycles=[]
    for bits in it.product(range(2),repeat=5):
        out=set()
        for bit,col in zip(bits,columns):
            if bit:out.symmetric_difference_update(col)
        if not out:cycles.append(list(bits))
    need(cycles==[[0]*5,[1]*5],'actual boundary matrix parity kernel')
    # Exact rational sign experiment uses w_1,...,w_d=e_i and w_0=-(1,...,1).
    sign_cases=[]
    for d in range(1,11):
        good=sum(all(s==signs[0] for s in signs) for signs in it.product((-1,1),repeat=d+1))
        need(good==2,'sign probability')
        sign_cases.append({'dimension':d,'successful_signs':good,'total_signs':2**(d+1)})
    products=0
    for p in range(1,31):
        for q in range(1,31):
            need(math.comb(p+q,p)*math.factorial(p+1)*math.factorial(q+1)-math.factorial(p+q+1)==math.factorial(p+q)*p*q,'product');products+=1
    examples=[quotient(d,d+1) for d in range(1,6)]
    extra_examples=[quotient(2,4),quotient(3,5)]
    rejected=[]
    for d in range(1,6):
        try:quotient(d,d)
        except RuntimeError as e:
            need(str(e)=='nonembedded cell','wrong invalid quotient diagnostic');rejected.append(d)
        else:raise RuntimeError('invalid quotient accepted')
    return {'status':'PARTIAL_UNRESOLVED','universal_factorial_bound_proved':False,
            'independent_arithmetic_checks':arithmetic,'independent_product_checks':products,
            'colored_dipole_control':colored_dipole_control(),'candidates':candidates,'boundary_delta4_kernel':cycles,'random_sign_controls':sign_cases,
            'quotients':examples,'additional_quotients':extra_examples,'nonregular_quotients_rejected':rejected,
            'scope':'Finite independent diagnostics; imported theorems and geometric proofs are audited in prose.'}

if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
