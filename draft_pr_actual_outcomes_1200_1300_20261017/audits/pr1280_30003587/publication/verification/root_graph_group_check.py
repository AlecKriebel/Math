"""Fresh deterministic finite diagnostics, not an operator-algebra proof.

Only Python standard library. Checks remain active under -O and -OO.
"""
from collections import deque
from fractions import Fraction
from itertools import product
from math import gcd, lcm
import json, random

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def distances(n, edges, base=0):
    dist={base:0}; paths={base:()}; q=deque([base])
    while q:
        u=q.popleft()
        for i,(s,t) in enumerate(edges):
            if s==u and t not in dist:
                dist[t]=dist[u]+1; paths[t]=paths[u]+(i,); q.append(t)
    require(len(dist)==n,'Generated graph not strongly reachable')
    return dist,paths

def matmul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def cycles(n,edges):
    answer=[]
    for b in range(n):
        def extend(v,seen,path):
            for i,(s,t) in enumerate(edges):
                if s!=v: continue
                if t==b: answer.append(path+(i,))
                elif t>b and t not in seen: extend(t,seen|{t},path+(i,))
        extend(b,{b},())
    return answer

def return_check(n,edges):
    dist,_=distances(n,edges)
    d=0
    for u,v in edges: d=gcd(d,dist[u]+1-dist[v])
    require(d>0,'Period must be positive')
    require(all((dist[v]-dist[u]-1)%d==0 for u,v in edges),'Cyclic classes fail')
    a=[[0]*n for _ in range(n)]
    for u,v in edges: a[u][v]+=1
    b=[[int(i==j) for j in range(n)] for i in range(n)]
    for _ in range(d): b=matmul(b,a)
    cls=[v for v in range(n) if dist[v]%d==0]
    ret=[[b[u][v] for v in cls] for u in cls]
    require(sum(map(sum,ret))>=2,'Return graph unexpectedly a single loop')
    power=[[int(i==j) for j in range(len(cls))] for i in range(len(cls))]
    primitive=False
    for _ in range((len(cls)-1)**2+1):
        power=matmul(power,ret)
        power=[[int(x>0) for x in row] for row in power]
        if all(all(row) for row in power): primitive=True;break
    require(primitive,'Return block not primitive within standard exponent bound')
    return d,len(cls)

def group_check(n,edges,mods,labels):
    den=lcm(*mods); group=list(product(*(range(m) for m in mods)))
    _,paths=distances(n,edges)
    cyc=cycles(n,edges)
    signatures={}; potentials={}; kernel=[]
    for g in group:
        phase=[sum(a*b*(den//m) for a,b,m in zip(label,g,mods))%den for label in labels]
        q=[sum(phase[i] for i in paths[v])%den for v in range(n)]
        sig=tuple((q[u]+phase[i]-q[v])%den for i,(u,v) in enumerate(edges))
        closed=all(sum(phase[i] for i in c)%den==0 for c in cyc)
        require(closed==(not any(sig)),'Cycle/potential criteria disagree')
        signatures[g]=sig;potentials[g]=q
        if closed: kernel.append(g)
    def add(g,h): return tuple((a+b)%m for a,b,m in zip(g,h,mods))
    for g in group:
        for h in group:
            z=add(g,h)
            require(potentials[z]==[(a+b)%den for a,b in zip(potentials[g],potentials[h])], 'Vertex unitary representation fails')
            require(signatures[z]==tuple((a+b)%den for a,b in zip(signatures[g],signatures[h])), 'Untwisted action law fails')
        for k in kernel:
            require(signatures[add(g,k)]==signatures[g],'Quotient signature not well defined')
    require(len(set(signatures.values()))*len(kernel)==len(group),'Quotient retains a nontrivial inner class')
    return len(group),len(kernel),len(cyc)

def main():
    rng=random.Random(30003587)
    graphs=[]
    # Deliberately periodic multigraphs, including one-vertex return blocks.
    for d in range(1,10):
        for rep in range(3):
            widths=[rng.randint(1,3) for _ in range(d)]
            if d==1 and widths==[1]: widths=[2]
            classes=[];offset=0
            for w in widths: classes.append(list(range(offset,offset+w)));offset+=w
            edges=[(u,v) for j,c in enumerate(classes) for u in c for v in classes[(j+1)%d]]
            if all(w==1 for w in widths): edges.append(edges[0])
            graphs.append((offset,edges))
    # Random strongly connected graphs with a guaranteed branching vertex.
    for n in range(2,11):
        for rep in range(12):
            edges=[(i,(i+1)%n) for i in range(n)]
            edges.extend((u,v) for u in range(n) for v in range(n) if rng.random()<.12)
            if len(edges)==n: edges.append((0,1))
            graphs.append((n,edges))
    periods={}; return_sizes={}
    for n,edges in graphs:
        d,k=return_check(n,edges)
        periods[str(d)]=periods.get(str(d),0)+1
        return_sizes[str(k)]=return_sizes.get(str(k),0)+1
    # Exact noncyclic character arithmetic; simple cycles exhaust closed-walk phase conditions.
    small=[(2,[(0,1),(0,1),(1,0)]),(3,[(0,1),(1,2),(2,0),(0,0)]),(4,[(0,1),(1,2),(2,3),(3,0),(0,1)]),(2,[(0,0),(0,1),(1,0),(1,1)])]
    cases=elements=0; kernel_sizes={}
    for mods in [(2,2),(2,4),(3,3),(2,2,2),(6,)]:
        for n,edges in small:
            for rep in range(40):
                labels=[tuple(rng.randrange(m) for m in mods) for _ in edges]
                size,ks,_=group_check(n,edges,mods,labels)
                cases+=1;elements+=size;kernel_sizes[str(ks)]=kernel_sizes.get(str(ks),0)+1
    # Outside the diagonal hypothesis, commuting inner automorphisms need not have fixed implementers.
    x=[[0,1],[1,0]]; z=[[1,0],[0,-1]]
    require(matmul(x,z)==[[-a for a in row] for row in matmul(z,x)],'Pauli obstruction fixture lost anticommutation')
    require(matmul(x,matmul(z,x))==[[-a for a in row] for row in z],'Pauli conjugation fixture fails')
    return {'status':'PASS','seed':30003587,'return_graph_cases':len(graphs),'period_histogram':periods,'return_class_size_histogram':return_sizes,'finite_abelian_phase_cases':cases,'group_elements_checked':elements,'inner_kernel_size_histogram':kernel_sizes,'outside_hypothesis_pauli_obstruction':'verified exact anticommutation; simultaneous fixed algebra is scalar by direct 2x2 calculation','limitations':'Finite diagnostics only. No representation or finite matrix test verifies a C*-algebra approximation theorem. Published inputs and the all-size proof must be checked mathematically.'}

if __name__=='__main__': print(json.dumps(main(),indent=2,sort_keys=True))
