#!/usr/bin/env python3
"""Fresh finite boundary checks; no package checker imports or verdict reliance."""
from fractions import Fraction as Q
from itertools import combinations, product
import json


def need(test, why):
    if not test:
        raise RuntimeError(why)


def rank(a, cols):
    rows=[list(map(Q,row)) for row in a]
    pivot=0
    for c in range(cols):
        p=next((r for r in range(pivot,len(rows)) if rows[r][c]),None)
        if p is None:continue
        rows[pivot],rows[p]=rows[p],rows[pivot]
        scale=rows[pivot][c]
        rows[pivot]=[x/scale for x in rows[pivot]]
        for r in range(pivot+1,len(rows)):
            scale=rows[r][c]
            rows[r]=[x-scale*y for x,y in zip(rows[r],rows[pivot])]
        pivot+=1
        if pivot==len(rows):break
    return pivot


def partitions(n):
    def recurse(words):
        if len(words)==n:
            yield tuple(words)
            return
        for k in range(max(words)+2):
            yield from recurse(words+[k])
    if n==1:
        yield (0,)
    else:
        yield from recurse([0])


def matrix(n,edges,p):
    out=[]
    for vertex in range(n):
        for axis in range(len(p[0])):
            row=[]
            for u,v in edges:
                if vertex==u:row.append(p[v][axis]-p[u][axis])
                elif vertex==v:row.append(p[u][axis]-p[v][axis])
                else:row.append(Q(0))
            out.append(row)
    return out


def forest(n,edges):
    parent=list(range(n))
    def root(v):
        while parent[v]!=v:v=parent[v]
        return v
    for u,v in edges:
        a,b=root(u),root(v)
        if a==b:return False
        parent[a]=b
    return True


def run():
    single_checks=forest_checks=0; counts={}
    for n in range(1,6):
        universe=list(combinations(range(n),2)); graph_count=0
        for mask in range(1<<len(universe)):
            es=[e for i,e in enumerate(universe) if mask>>i&1]
            is_forest=forest(n,es)
            if n==5 and not is_forest:continue
            graph_count+=1
            for labels in partitions(n):
                # Distinct blocks are placed on a curved moment-type set in
                # dimension 2 or 3, so this covers arbitrary multiple vertex
                # collisions beyond the collinear one-pair witness.
                for d in (2,3):
                    p=[tuple(Q((b+1)**(a+1)+(a+1)) for a in range(d)) for b in labels]
                    a=matrix(n,es,p)
                    collapse=0
                    for col,(u,v) in enumerate(es):
                        zero=all(row[col]==0 for row in a)
                        need(zero==(labels[u]==labels[v]),'singleton collision equivalence')
                        collapse+=int(zero);single_checks+=1
                    if is_forest:
                        need(len(es)-rank(a,len(es))==collapse,'forest nullity exceeds collapsed freedom')
                        forest_checks+=1
            counts[str(n)]=graph_count
    # Global path/star change and inverse on noncollinear rational placements
    # with multiple collisions and oriented edge changes.
    ambient=0
    P=[(0,0),(1,3),(-2,4),(5,-6)]
    for d in (1,2):
        for labels in partitions(4):
            points=[tuple(Q(x) for x in P[b][:d]) for b in labels]
            q=[points[0],points[1],tuple(x+z-y for x,y,z in zip(points[0],points[1],points[2])),tuple(x+w-z for x,z,w in zip(points[0],points[2],points[3]))]
            inv=[q[0],q[1],tuple(y+z-x for x,y,z in zip(q[0],q[1],q[2])),tuple(y+z+w-2*x for x,y,z,w in zip(q[0],q[1],q[2],q[3]))]
            need(inv==points,'path star inverse')
            pe=[(0,1),(1,2),(2,3)];se=[(0,1),(0,2),(0,3)]
            for (u,v),(a,b) in zip(pe,se):
                need(tuple(points[v][i]-points[u][i] for i in range(d))==tuple(q[b][i]-q[a][i] for i in range(d)),'path star differences')
            ambient+=1
    return {'status':'PASS','arithmetic':'exact fractions.Fraction','graph_counts_by_n':counts,'singleton_multi_collision_checks':single_checks,'forest_full_kernel_dimension_checks':forest_checks,'noncollinear_path_star_inverse_checks':ambient,'limits':'Finite diagnostics only; universal theorem and connectedness follow from the written proof.'}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
