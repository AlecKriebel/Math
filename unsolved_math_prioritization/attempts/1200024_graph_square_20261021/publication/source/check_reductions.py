#!/usr/bin/env python3
"""Exact finite circuit diagnostics. Python >=3.10, standard library; MIT.
Two-terminal branches and actual induced exhaustions are built from binary
words, then globally reduced by rational star-mesh elimination. Written
all-depth recurrences/contraction prove the infinite limit, not these examples.
"""
from fractions import Fraction as F
from itertools import product, combinations
import json

def require(test, why):
    if not test:
        raise RuntimeError(why)
def vertices(depth):
    return [w for n in range(depth+1) for w in product((0,1),repeat=n)]
def add(a,x,y,c=F(1)):
    if x == y:
        return
    a.setdefault(x,{})[y] = a.setdefault(x,{}).get(y,F(0))+c
    a.setdefault(y,{})[x] = a.setdefault(y,{}).get(x,F(0))+c
def reduce_network(a, retain):
    # Eliminate actual vertices, never identify distinct boundary terminals.
    eliminate = sorted(set(a)-set(retain),key=lambda v:(len(v) if isinstance(v,tuple) else -1,repr(v)),reverse=True)
    for v in eliminate:
        nei = list(a[v].items())
        total = sum((c for _,c in nei),F(0))
        require(total > 0, "connected eliminated vertex")
        for (x,cx),(y,cy) in combinations(nei,2):
            add(a,x,y,cx*cy/total)
        for x,_ in nei:
            del a[x][v]
        del a[v]
    return a
def branch(m):
    W = vertices(m);a = {x:{} for x in W}
    a["a"]={};a["b"]={}
    def up(w):
        if w == "a":
            return "b"
        return w[:-1] if w else "a"
    for w in W:
        for v in [up(w),up(up(w))]:
            add(a,w,v)
    require(sum(len(x) for x in a.values())//2 == 2*len(W), "branch edges")
    r = reduce_network(a,["a","b"])
    return len(W)+2,r["a"]["b"]
def induced(n):
    W = vertices(2*n);a = {w:{} for w in W}
    for w in W:
        if w:
            add(a,w,w[:-1])
        if len(w)>=2:
            add(a,w,w[:-2])
    t = [(0,)*n,(0,)*(n-1),(0,)*(n-2)]
    r = reduce_network(a,t)
    return len(W),(r[t[0]][t[1]],r[t[1]][t[2]],r[t[0]][t[2]])
def recurrences(n):
    c = [F(1)]
    for _ in range(2*n):
        c.append(1+2*c[-1]/(1+c[-1]))
    a = {m:1+c[m-1]/(1+c[m-1]) for m in range(1,2*n+1)}
    u = a[2*n-1]
    for j in range(n-2,0,-1):
        u = a[n+j]+u/(1+u)
    return c[n],u,F(1)
def run():
    branches=[];k=F(1,2)
    for m in range(4):
        count,actual = branch(m)
        require(actual == k, "branch recurrence at depth"+str(m))
        branches.append({"depth":m,"vertices":count,"conductance":str(actual)})
        k = (1+2*k)/(2+2*k)
    exhaustions=[]
    for n in [2,3]:
        count,actual = induced(n)
        require(actual == recurrences(n), "actual induced-network reduction")
        A,B,unit = actual
        require(unit == 1, "unmodified skip edge")
        R1=1/(A+B/(1+B));R2=1/(1+A*B/(A+B))
        exhaustions.append({"n":n,"vertices":count,"triangle":[str(v) for v in actual],
                            "R_parent":str(R1),"R_grandparent":str(R2)})
    require(exhaustions[0]["R_parent"] == "27/80" and
            exhaustions[0]["R_grandparent"] == "121/240", "n2 concrete values")
    require(exhaustions[1]["triangle"] == ["12/5","6236/2669","1"],"n3 concrete triangle")
    require(F(1,1)/F(1,2) == 2, "free two-edge series resistance")
    return {"status":"PASS","branches":branches,"induced_exhaustions":exhaustions,
            "maximum_vertices":max(x["vertices"] for x in exhaustions),
            "method":"Binary-word graph construction; exact global star-mesh elimination.",
            "limits":"Finite interface diagnostics only. Main paper proves the all-depth "
                     "identities and uniform-contraction free limits."}
if __name__ == "__main__":
    print(json.dumps(run(),sort_keys=True,indent=2))
