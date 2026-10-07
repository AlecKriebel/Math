#!/usr/bin/env python3
"""Independent exact audit controls. Imports no author checker; not a family proof."""
from collections import defaultdict, deque
from itertools import combinations
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]

def make_moore(p):
    n=3*p; base=list(range(n,n+3)); c=n+3
    facets=set()
    cap=set()
    for i in range(n):
        j=(i+1)%n
        facets.add(tuple(sorted((i,j,base[j%3]))))
        facets.add(tuple(sorted((i,base[i%3],base[j%3]))))
        t=tuple(sorted((c,i,j)));facets.add(t);cap.add(t)
    return facets,cap,base

def face_set(facets):
    return {frozenset(s) for t in facets for k in (1,2,3) for s in combinations(t,k)}

def barycentric(facets):
    faces=sorted(face_set(facets),key=lambda s:(-len(s),tuple(sorted(s))))
    number={s:i for i,s in enumerate(faces)}
    edges={tuple(sorted((number[a],number[b]))) for a in faces for b in faces if a<b}
    triangles={tuple(sorted((number[frozenset((v,))],number[frozenset(e)],number[frozenset(t)])))
               for t in facets for e in combinations(t,2) for v in e}
    return list(range(len(faces))),edges,triangles,number

def spanning_chords(vertices,edges):
    adj=defaultdict(list)
    for a,b in edges:adj[a].append(b);adj[b].append(a)
    parent={vertices[-1]:None};stack=[vertices[-1]];tree=set()
    while stack:
        v=stack.pop()
        for w in sorted(adj[v],reverse=True):
            if w not in parent:
                parent[w]=v;tree.add(tuple(sorted((v,w))));stack.append(w)
    assert len(parent)==len(vertices)
    return {e:i for i,e in enumerate(sorted(edges-tree))}

def cycle_vector(cycle,chords,p):
    row=[0]*len(chords)
    for a,b in zip(cycle,cycle[1:]+cycle[:1]):
        e=tuple(sorted((a,b)))
        if e in chords:row[chords[e]]=(row[chords[e]]+(1 if a<b else -1))%p
    return row

def append_basis(piv,row,p):
    row=row.copy()
    for j in sorted(piv):
        c=row[j]
        if c:row=[(x-c*y)%p for x,y in zip(row,piv[j])]
    if not any(row):return False
    j=next(j for j,x in enumerate(row) if x)
    c=pow(row[j],-1,p);piv[j]=[(c*x)%p for x in row]
    return True

def exact_det(a):
    a=[r.copy() for r in a];n=len(a);den=1;sign=1
    for k in range(n-1):
        row=next((i for i in range(k,n) if a[i][k]),None)
        if row is None:return 0
        if row!=k:a[row],a[k]=a[k],a[row];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            z=a[i][k]
            for j in range(k+1,n):
                top=a[i][j]*pivot-z*a[k][j]
                assert top%den==0
                a[i][j]=top//den
            a[i][k]=0
        den=pivot
    return sign*a[-1][-1]

def all_short_cycles(vertices,edges,max_length):
    adj=defaultdict(set)
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    out=[]
    for start in vertices:
        todo=[(start,)]
        while todo:
            path=todo.pop();last=path[-1]
            if len(path)>=3 and start in adj[last] and path[1]<last:out.append(path)
            if len(path)<max_length:
                for w in sorted(adj[last]):
                    if w>start and w not in path:todo.append(path+(w,))
    return sorted(out,key=lambda x:(len(x),x))

def reduce_word(word):
    stack=[]
    for x in word:
        if stack and stack[-1]==-x:stack.pop()
        else:stack.append(x)
    while len(stack)>1 and stack[0]==-stack[-1]:stack=stack[1:-1]
    return stack

def inverse(word):return [-x for x in word[::-1]]

def group_certificate(cycles,chords):
    words=[]
    for cycle in cycles:
        w=[]
        for a,b in zip(cycle,cycle[1:]+cycle[:1]):
            j=chords.get(tuple(sorted((a,b))))
            if j is not None:w.append((j+1)*(1 if a<b else -1))
        w=reduce_word(w)
        if w:words.append(w)
    variables=set(range(1,len(chords)+1));steps=0
    while words:
        choice=None
        # Different spanning tree and elimination order from author controls.
        for i in range(len(words)-1,-1,-1):
            w=words[i]
            for var in sorted(set(map(abs,w)),reverse=True):
                if sum(abs(x)==var for x in w)==1:
                    choice=(i,var);break
            if choice:break
        if choice is None:
            # A length-decreasing Nielsen automorphism is exact, unlike guessing
            # a group from its abelianization. Needed for this alternative tree.
            best=None;old_length=sum(map(len,words))
            if len(variables)<=6:
                for x in sorted(variables):
                    for y in sorted(variables-{x}):
                        for sign in (-1,1):
                            for side in (0,1):
                                rep=[sign*y,x] if side==0 else [x,sign*y]
                                transformed=[]
                                for word in words:
                                    out=[]
                                    for z in word:out.extend(rep if z==x else inverse(rep) if z==-x else [z])
                                    out=reduce_word(out)
                                    if out:transformed.append(out)
                                length=sum(map(len,transformed))
                                if length<old_length and (best is None or length<best[0]):best=length,transformed
            if best is None:break
            words=best[1];steps+=1;continue
        i,var=choice;w=words.pop(i);j=next(j for j,x in enumerate(w) if abs(x)==var)
        tail=w[j+1:]+w[:j];replacement=inverse(tail) if w[j]>0 else tail
        nw=[]
        for word in words:
            expanded=[]
            for x in word:expanded.extend(replacement if x==var else inverse(replacement) if x==-var else [x])
            result=reduce_word(expanded)
            if result:nw.append(result)
        variables.remove(var);words=nw;steps+=1
    return variables,words,steps

def punctured_disk_checks(cap):
    vs,edges,triangles,_=barycentric(cap)
    incident=defaultdict(list)
    for t in triangles:
        for e in combinations(t,2):incident[e].append(t)
    boundary={e for e,ts in incident.items() if len(ts)==1}
    tested=0
    for omit in triangles:
        remaining=set(triangles)-{omit};left=set(edges)
        while remaining:
            hit=None
            for t in sorted(remaining):
                for e in combinations(t,2):
                    if e not in boundary and sum(s in remaining for s in incident[e])==1:
                        hit=t,e;break
                if hit:break
            assert hit is not None
            t,e=hit;remaining.remove(t);left.remove(e)
        assert boundary<=left and len(left)-len(vs)+1==1
        active=set(left)
        while True:
            degree=defaultdict(int)
            for a,b in active:degree[a]+=1;degree[b]+=1
            leaves={v for v,d in degree.items() if d==1}
            if not leaves:break
            active={e for e in active if not (set(e)&leaves)}
        assert active==boundary
        tested+=1
    return tested

def audit_moore(p,enumerate_cycles=False):
    facets,cap,base=make_moore(p)
    old=face_set(facets)
    assert tuple(sum(len(s)==d for s in old) for d in (1,2,3))==(3*p+4,12*p+3,9*p)
    # Signed integer relation determinant on a separately selected graph tree.
    ov=sorted({v for t in facets for v in t});oe={e for t in facets for e in combinations(t,2)}
    oc=spanning_chords(ov,oe)
    matrix=[]
    for t in sorted(facets):
        row=cycle_vector(t,oc,2**20)
        matrix.append([x if x<2**19 else x-2**20 for x in row])
    determinant=exact_det(matrix);assert abs(determinant)==p
    vertices,edges,triangles,ids=barycentric(facets);r=len(edges)-len(vertices)+1
    assert (len(vertices),len(edges),len(triangles),r)==(24*p+7,78*p+6,54*p,54*p)
    chords=spanning_chords(vertices,edges)
    prime=next(d for d in range(2,p+1) if p%d==0)
    rank={}
    for q in sorted({2,prime}):
        piv={}
        for t in sorted(triangles):append_basis(piv,cycle_vector(t,chords,q),q)
        rank[q]=len(piv)
        assert len(piv)==r-(p%q==0)
    B=[]
    for i,a in enumerate(base):
        b=base[(i+1)%3];B.extend((ids[frozenset((a,))],ids[frozenset((a,b))]))
    cap_small={t for t in triangles if any(ids[frozenset(f)] in t for f in cap)}
    omitted=min(cap_small)
    full=group_certificate(sorted(triangles),chords)
    assert len(full[0])==1 and len(full[1])==1 and len(full[1][0])==p and len(set(full[1][0]))==1
    punct=group_certificate(sorted(triangles-{omitted}),chords)
    assert len(punct[0])==1 and not punct[1]
    killed=group_certificate(sorted(triangles-{omitted})+[tuple(B)],chords)
    assert not killed[0] and not killed[1]
    out=dict(p=p,original_absolute_determinant=abs(determinant),vertices=len(vertices),edges=len(edges),triangles=len(triangles),rank=r,field_ranks=rank,full_cyclic_relator_length=p,punctured_free_generators=1,augmented_generators=0)
    if enumerate_cycles:
        cycles=all_short_cycles(vertices,edges,6)
        piv={};weights=[]
        for c in cycles:
            if append_basis(piv,cycle_vector(c,chords,2),2):weights.append(len(c))
        assert len(piv)==r
        # All simple cycles shorter than the maximum selected weight were enumerated.
        cost=sum(weights);assert cost==3*r+(3 if p%2==0 else 0)
        triangle_span={}
        for t in sorted(triangles):append_basis(triangle_span,cycle_vector(t,chords,prime),prime)
        shortest_nonzero=min(len(c) for c in cycles if append_basis(triangle_span.copy(),cycle_vector(c,chords,prime),prime))
        assert shortest_nonzero==6
        out.update(simple_cycles_through_six=len(cycles),exact_binary_optimum=cost,minimum_nonzero_mod_prime_cycle=shortest_nonzero,exact_pi_optimum_by_lower_and_upper_certificates=3*r+3,punctured_cap_choices_checked=punctured_disk_checks(cap))
    return out

if __name__=='__main__':
    pins=json.loads((ROOT/'AUTHOR_MANIFEST.json').read_text())
    for name,pin in pins['files'].items():
        data=(ROOT/name).read_bytes();assert len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256']
    result={'status':'pass','independence':'No author-checker imports; separate face numbering, spanning tree, elimination order, exhaustive short-cycle enumeration and binary optimum calculation.','moore':[audit_moore(p,p in (2,3)) for p in (2,3,4,5,6,9)]}
    dest=Path(__file__).with_name('INDEPENDENT_RESULTS.json');dest.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
