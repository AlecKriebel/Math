#!/usr/bin/env python3
"""Exact bounded controls for AMR-011-0023. No third-party libraries or data."""
from collections import deque
from fractions import Fraction
import json, sys


def z_neighbors(v): return (v-1,v+1)
def z2_neighbors(v):
    x,y=v
    return ((x-1,y),(x+1,y),(x,y-1),(x,y+1))
def tree_neighbors(v,q=2):
    h,m=v
    return ((h+1,m//q),)+tuple((h-1,q*m+i) for i in range(q))
def grandfather_neighbors(v,q=2):
    h,m=v
    return tree_neighbors(v,q)+((h+2,m//(q*q)),)+tuple((h-2,q*q*m+i) for i in range(q*q))
def dl_neighbors(v,p=2,q=3):
    h,m,n=v
    return tuple((h+1,m//p,q*n+j) for j in range(q))+tuple((h-1,p*m+i,n//q) for i in range(p))

def ball(neighbors,root,r):
    dist={root:0}; queue=deque([root])
    while queue:
        v=queue.popleft()
        if dist[v]==r: continue
        for w in neighbors(v):
            if w not in dist: dist[w]=dist[v]+1;queue.append(w)
    return dist

def boundary(neighbors,A):
    return set(w for v in A for w in neighbors(v))-set(A)

def deficit(neighbors,A,dist):
    return sum(dist[w] for w in boundary(neighbors,A))-len(A)

class Flow:
    def __init__(self,n): self.g=[[] for _ in range(n)];self.arcs=[]
    def add(self,u,v,c):
        a=[v,c,len(self.g[v])]; b=[u,0,len(self.g[u])]
        self.g[u].append(a); self.g[v].append(b);self.arcs.append((u,v,c,a))
    def run(self,s,t):
        result=0
        while True:
            level=[-1]*len(self.g);level[s]=0;q=deque([s])
            while q:
                u=q.popleft()
                for v,c,_ in self.g[u]:
                    if c and level[v]<0:level[v]=level[u]+1;q.append(v)
            if level[t]<0:break
            it=[0]*len(self.g)
            def dfs(u,f):
                if u==t:return f
                while it[u]<len(self.g[u]):
                    e=self.g[u][it[u]];v,c,rev=e
                    if c and level[v]==level[u]+1:
                        z=dfs(v,min(f,c))
                        if z:e[1]-=z;self.g[v][rev][1]+=z;return z
                    it[u]+=1
                return 0
            while True:
                f=dfs(s,10**40)
                if not f:break
                result+=f
        seen={s};q=deque([s])
        while q:
            u=q.popleft()
            for v,c,_ in self.g[u]:
                if c and v not in seen:seen.add(v);q.append(v)
        assert t not in seen
        cut=sum(c for u,v,c,_ in self.arcs if u in seen and v not in seen)
        balance=[0]*len(self.g)
        for u,v,c,a in self.arcs:
            f=c-a[1];assert 0<=f<=c
            balance[u]-=f;balance[v]+=f
        assert all(z==0 for i,z in enumerate(balance) if i not in (s,t))
        assert -balance[s]==balance[t]==result==cut
        return result,seen

def minimize(neighbors,U,dist):
    """Return exact minimum of sum_boundary d(b,x)-|A| over A subset U."""
    U=sorted(U);W=sorted(set(U)|boundary(neighbors,U))
    av={v:i for i,v in enumerate(U)}; zv={v:len(U)+i for i,v in enumerate(W)}
    s=len(U)+len(W);t=s+1;f=Flow(t+1)
    baseline=sum(dist[v]+1 for v in U);infinite=baseline+1
    for v in U:
        f.add(s,av[v],dist[v]+1)
        for w in set(neighbors(v))|{v}:f.add(av[v],zv[w],infinite)
    for w in W:f.add(zv[w],t,dist[w])
    flow,seen=f.run(s,t);A={v for v in U if av[v] in seen}
    value=flow-baseline
    assert deficit(neighbors,A,dist)==value
    return {'vertices':len(U),'closed_neighborhood':len(W),'flow':flow,
            'baseline':baseline,'minimum_deficit':value,'minimizer_size':len(A),
            'flow_cut_and_conservation_verified':True}

def brute(neighbors,U,dist):
    U=list(U);best=10**9;checks=0
    for mask in range(1<<len(U)):
        A={v for i,v in enumerate(U) if mask>>i&1}
        best=min(best,deficit(neighbors,A,dist));checks+=1
    return best,checks

def run():
    models=[('integer_line',z_neighbors,0,7),('square_lattice',z2_neighbors,(0,0),6),
            ('binary_grandfather',grandfather_neighbors,(0,0),4),
            ('DL_2_3',dl_neighbors,(0,0,0),5),
            ('DL_3_4',lambda v:dl_neighbors(v,3,4),(0,0,0),4)]
    out={'scope':'Finite-support checks only; no general nonunimodular theorem is certified.',
         'models':[],'brute_force_comparisons':[],'negative_controls':[]}
    for name,ng,root,R in models:
        dist=ball(ng,root,R+1)
        # The neighbor oracle describes the infinite graph, never a cropped graph.
        for v in dist:
            nv=ng(v);assert len(nv)==len(set(nv)) and v not in nv
            assert all(v in ng(w) for w in nv)
        rows=[]
        for r in range(R+1):
            U={v for v,d in dist.items() if d<=r}
            res=minimize(ng,U,dist);res['support_radius']=r
            assert res['minimum_deficit']==0
            rows.append(res)
        small={v for v,d in dist.items() if d<=1}
        best,count=brute(ng,small,dist)
        assert best==rows[1]['minimum_deficit']
        out['brute_force_comparisons'].append({'model':name,'subsets':count,'minimum_deficit':best})
        out['models'].append({'model':name,'checks':rows})
    # A finite cycle is transitive but not infinite: taking all vertices fails.
    cycle=lambda v:((v-1)%7,(v+1)%7)
    dist=ball(cycle,0,7);res=minimize(cycle,set(range(7)),dist)
    best,count=brute(cycle,set(range(7)),dist)
    assert res['minimum_deficit']==best==-7
    out['negative_controls'].append({'model':'finite_C7','result':res,'subsets':count})
    # The one-sided infinite ray satisfies the diameter boundary estimate but
    # fails the target; this is a failed-inference control, not a transitive example.
    ray=lambda v:tuple(w for w in (v-1,v+1) if w>=0)
    A=set(range(5));B=boundary(ray,A);assert B=={5}
    assert len(A)==(max(A)-min(A)+1)*len(B)
    assert sum(abs(5-v) for v in B)-len(A)==-5
    out['negative_controls'].append({'model':'infinite_ray','basepoint':5,'A_size':5,'diameter':4,'boundary_size':1,'deficit':-5,'diameter_bound_holds':True})
    # Attach one leaf at each vertex of the binary oriented tree. This graph
    # has vertex expansion at least 1/3 but the singleton leaf fails the target.
    def hairy(v):
        h,m,t=v
        if t:return ((h,m,0),)
        return tuple((a,b,0) for a,b in tree_neighbors((h,m)))+((h,m,1),)
    A={(0,0,1)};assert boundary(hairy,A)=={(0,0,0)}
    out['negative_controls'].append({'model':'tree_with_one_leaf_per_vertex','A_size':1,'boundary_size':1,'basepoint_is_unique_boundary_vertex':True,'deficit':-1,'scope':'nontransitive positive-expansion failed-inference control'})
    # An infinite disjoint union of triangles is transitive but not connected.
    # The complete component A has empty boundary; the literal disconnected reading fails.
    out['negative_controls'].append({'model':'disjoint_union_of_K3','A_size':3,'boundary_size':0,'deficit':-3})
    # A finite path retains geodesic structure but is not vertex-transitive/infinite.
    path=lambda v:tuple(w for w in (v-1,v+1) if 0<=w<=6)
    dist=ball(path,0,7);res=minimize(path,set(range(7)),dist)
    assert res['minimum_deficit']==-7
    out['negative_controls'].append({'model':'finite_path_7','result':res})
    # Modular mass-transport correction: one grandparent, q^2 grandchildren.
    out['modular_controls']=[]
    for q in (2,3,4):
        outgoing=1;incoming=q*q;weight=Fraction(1,q*q)
        assert incoming*weight==outgoing and incoming!=outgoing
        out['modular_controls'].append({'q':q,'outgoing':outgoing,'incoming':incoming,'tilt':str(weight),'weighted_incoming':str(incoming*weight)})
    # Exact tree boundary inequality checks for every subset of a radius-one ball.
    ng=lambda v:tree_neighbors(v,2);root=(0,0);U=list(ball(ng,root,1));n=0
    for mask in range(1,1<<len(U)):
        A={v for i,v in enumerate(U) if mask>>i&1}
        assert len(boundary(ng,A))>=len(A)+2;n+=1
    out['tree_boundary_control_subsets']=n
    # Direct geodesic interval inequality with both path endpoints outside A.
    n=0
    for length in range(2,12):
        for mask in range(1,1<<(length-1)):
            A={i+1 for i in range(length-1) if mask>>i&1}
            l=min(A)-1;r=max(A)+1
            for b in range(-2,length+3):
                assert len(A)<=abs(b-l)+abs(b-r)-1;n+=1
    out['geodesic_interval_checks']=n
    return out

if __name__=='__main__':
    sys.setrecursionlimit(100000)
    result=run()
    print(json.dumps(result,indent=2,sort_keys=True))
