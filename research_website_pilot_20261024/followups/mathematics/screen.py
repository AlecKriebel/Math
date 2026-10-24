"""Exploratory finite free networks only; not a theorem or a certificate."""
from itertools import combinations
import json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu


def graph(radius, types):
    n = 1 + 3 * (2 ** radius - 1)
    outward = [None] + [0 if i <= 3 else (i - 2)//2 for i in range(1,n)]
    ray = {0}
    k = 1
    while k < n:
        ray.add(k)
        k = 2*k+2
    parent = [(1 if i == 0 else 2*i+2) if i in ray else outward[i] for i in range(n)]
    children = [[] for _ in range(n)]
    for i,p in enumerate(parent):
        if p < n:
            children[p].append(i)
    adj = [set() for _ in range(n)]
    for v in range(n):
        for a,b in types:
            z=v; previous=None
            for _ in range(a):
                previous,z=z,parent[z]
                if z >= n: break
            if z >= n: continue
            current=[z]
            for level in range(b):
                current=[w for u in current for w in children[u]
                         if not (level == 0 and a > 0 and w == previous)]
            for w in current:
                if w != v:
                    adj[v].add(w); adj[w].add(v)
    return adj


def square(adj):
    return [(set.union(a, *(adj[x] for x in a)) - {i}) for i,a in enumerate(adj)]


def root_degree(adj):
    n=len(adj)
    row=[]; col=[]; val=[]
    for i,a in enumerate(adj):
        if i:
            row.append(i-1);col.append(i-1);val.append(len(a))
            for j in a:
                if j:
                    row.append(i-1);col.append(j-1);val.append(-1)
    matrix=coo_matrix((val,(row,col)),shape=(n-1,n-1)).tocsc()
    lu=splu(matrix)
    targets=sorted(adj[0])
    rhs=np.zeros((n-1,len(targets)))
    for k,t in enumerate(targets):rhs[t-1,k]=1
    answer=lu.solve(rhs)
    return {'vertices':n,'root_degree':len(targets),
            'finite_free_sum':sum(answer[t-1,k] for k,t in enumerate(targets))}


if __name__=='__main__':
    families={
        'tree':[(0,1)],
        'grandparent':[(0,1),(0,2)],
        'uncle':[(0,1),(1,2)],
        'cousin':[(0,1),(2,2)],
        'skip3':[(0,1),(0,3)],
        'skip3_sibling':[(0,1),(0,3),(1,1)],
        'skip4':[(0,1),(0,4)],
        'uncle_sibling':[(0,1),(1,2),(1,1)],
    }
    results=[]
    for name,types in families.items():
        for radius in (6,8):
            a=graph(radius,types)
            record={'family':name,'types':types,'radius':radius,
                    'base':root_degree(a),'square':root_degree(square(a))}
            results.append(record)
            print(json.dumps(record),flush=True)
    with open('screen-results.json','w') as f:json.dump(results,f,indent=2)
