# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Alec Kriebel
"""Exact finite diagnostics. The universal written proof remains primary."""
from fractions import Fraction as F
from collections import defaultdict, deque
import itertools, json

def need(ok,msg):
    if not ok: raise RuntimeError(msg)

def edge(a,b):return tuple(sorted((a,b)))
def neigh(v):
    x,y=v
    return [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
def strong(a,b):
    return (all(x>=1 for x in a) and all(x>=1 for x in b) or
            all(x<=-1 for x in a) and all(x<=-1 for x in b))
def bfs(adj,start):
    d={start:0};todo=deque([start])
    while todo:
        x=todo.popleft()
        for y in adj[x]:
            if y not in d:d[y]=d[x]+1;todo.append(y)
    return d

def dual_boundary(c,drop_bottom=False):
    need((0,0) in c,'corner missing')
    adj=defaultdict(set);cross={}
    for a in c:
        for b in neigh(a):
            if min(b)<0 or b in c:continue
            u,v=edge(a,b);x,y=u
            if u[0]!=v[0]:d,e=(2*x+1,2*y-1),(2*x+1,2*y+1)
            else:d,e=(2*x-1,2*y+1),(2*x+1,2*y+1)
            if drop_bottom and (d[1]==-1 or e[1]==-1):continue
            adj[d].add(e);adj[e].add(d);cross[edge(d,e)]=edge(a,b)
    return adj,cross

def dual_check(c,drop_bottom=False):
    adj,cross=dual_boundary(c,drop_bottom)
    bottom=[v for v in adj if v[1]==-1]
    need(len(bottom)%2==1,'bottom endpoint parity')
    for v,n in adj.items():
        if -1 in v:need(len(n)==1,'boundary degree')
        else:need(len(n) in (2,4),'interior parity')
    # Find an actual simple dual path, not a chosen exterior-boundary tour.
    path=None
    for s in bottom:
        parent={s:None};todo=deque([s]);end=None
        while todo:
            x=todo.popleft()
            if x[0]==-1:end=x;break
            for y in adj[x]:
                if y not in parent:parent[y]=x;todo.append(y)
        if end is not None:
            path=[]
            while end is not None:path.append(end);end=parent[end]
            path.reverse();break
    need(path is not None,'no bottom-left path')
    need(len(path)==len(set(path)),'path not simple')
    need(all(-1 not in v for v in path[1:-1]),'internal boundary vertex')
    m=len(path)-1;i=(path[0][0]-1)//2;j=(path[-1][1]-1)//2
    need(m>=i+j+2>=2,'dual distance bound')
    primal=[cross[edge(a,b)] for a,b in zip(path,path[1:])]
    need(len(set(primal))==m,'distinct crossed bonds')
    return max(map(len,adj.values())),m

def series_check(use_or=False):
    # Triangle with independent paths of lengths 1,2,3 and shared endpoints.
    lengths=[1,2,3];pairs=[(0,1),(1,2),(0,2)];paths=[];bonds=[];fresh=3
    for L,(u,v) in zip(lengths,pairs):
        seq=[u]+list(range(fresh,fresh+L-1))+[v];fresh+=L-1
        ids=[]
        for a,b in zip(seq,seq[1:]):ids.append(len(bonds));bonds.append((a,b))
        paths.append(ids)
    p=F(2,5);law=defaultdict(F);compared=0
    for bits in itertools.product((0,1),repeat=len(bonds)):
        actual=defaultdict(set);coarse=defaultdict(set)
        for state,(u,v) in zip(bits,bonds):
            if state:actual[u].add(v);actual[v].add(u)
        states=[]
        for ids,(u,v) in zip(paths,pairs):
            state=any(bits[i] for i in ids) if use_or else all(bits[i] for i in ids)
            states.append(int(state))
            if state:coarse[u].add(v);coarse[v].add(u)
        law[tuple(states)]+=p**sum(bits)*(1-p)**(len(bits)-sum(bits))
        for u,v in pairs:
            need((v in bfs(actual,u))==(v in bfs(coarse,u)),'series connectivity')
            compared+=1
    for states,prob in law.items():
        want=F(1)
        for state,L in zip(states,lengths):want*=p**L if state else 1-p**L
        need(prob==want,'joint coarse independence/power law')
    return {'actual_bonds':len(bonds),'configurations':2**len(bonds),
            'original_pair_connectivity_comparisons':compared,'coarse_states':len(law)}

def metric_check(far_projection=False):
    originals=list(itertools.product(range(-2,4),repeat=2));inside=set(originals)
    adj=defaultdict(set);image={};chain_samples=[];fresh=0
    def orig(v):return ('o',v[0],v[1])
    for v in originals:image[orig(v)]=v
    for a in originals:
        for b in [(a[0]+1,a[1]),(a[0],a[1]+1)]:
            if b not in inside:continue
            L=1 if strong(a,b) else 100
            seq=[orig(a)]
            for k in range(1,L):
                v=('i',fresh,k);seq.append(v)
                image[v]=a if (k<=L//2)!=far_projection else b
                if fresh<5 and k in (1,49,50,51,99):chain_samples.append(v)
            seq.append(orig(b));fresh+=1
            for u,v in zip(seq,seq[1:]):adj[u].add(v);adj[v].add(u)
    need(max(map(len,adj.values()))==4,'maximum degree')
    need(all(len(adj[v])==2 for v in image if v[0]=='i'),'private chain degrees')
    def l1(a,b):return sum(abs(x-y) for x,y in zip(a,b))
    need(all(l1(image[u],image[v])<=1 for u in adj for v in adj[u]),'image edge Lipschitz')
    samples=[orig(v) for v in originals]+chain_samples;pairs_checked=0
    for u in samples:
        distances=bfs(adj,u)
        need(distances[orig(image[u])]<=50,'projection distance exceeds fifty')
        for v in samples:
            d=distances[v];coarse=l1(image[u],image[v])
            need(coarse<=d<=100*coarse+100,'global-constant metric check')
            pairs_checked+=1
    return {'vertices':len(adj),'sampled_pairs':pairs_checked,'actual_edges':sum(map(len,adj.values()))//2}

def canonical_weak_paths():
    count=0;furthest=0;longest=0
    for n in range(1,101):
        base=[(1,n)]+[(0,j) for j in range(n,-2,-1)]+[(-1,-1)]
        for path in [base,[(y,x) for x,y in base]]:
            need(len(path)==len(set(path)),'weak path not simple')
            need(len(path)-1==n+3,'all-start distance')
            need(all(b in neigh(a) and not strong(a,b) for a,b in zip(path,path[1:])),'weak path eligibility')
            need(all(x<=-1 for x in path[-1]),'weak path target')
            count+=1;furthest=max(furthest,*path[0]);longest=max(longest,len(path)-1)
    return {'checked':count,'furthest_start_coordinate':furthest,'largest_attained_distance':longest}

def bridge_bound(p,length):
    r=3*p**length
    need(r<1,'bridge series does not converge')
    return F(8,3)*r**4/(1-r)**2

def constants():
    z=F(3,10);failure=F(4,3)*z*z*(2-z)/(1-z)**2;survival=1-failure
    p=F(19,20);q=p**100;cap=F(8,3)*F(3,32)**4/(1-F(3,32))**2
    lower=survival**2*(1-cap);margin=lower-F(1,3)
    need(failure==F(102,245) and survival==F(143,245),'Peierls constants')
    need(q<F(1,32) and (1/p)**20>=1+F(20,19)>2,'strict subdivision inequality')
    need(cap==F(27,107648),'bridge cap')
    need(lower==F(2200741829,6461571200) and margin==F(140654287,19384713600)>0,'strict final margin')
    # Exact finite partial sum plus the actual infinite tail, not a cutoff claim.
    partial=sum((F(4,3)*m*z**m for m in range(2,12)),F(0))
    tail=F(4,3)*z**12*(12-11*z)/(1-z)**2
    need(partial+tail==failure and tail>0,'Peierls tail')
    r=3*q
    start_partial=F(8,3)/(1-r)*sum((r**(n+3) for n in range(1,9)),F(0))
    start_tail=F(8,3)*r**12/(1-r)**2
    need(start_partial+start_tail==bridge_bound(p,100) and start_tail>0,'all-start bridge tail')
    return {'survival_lower':str(survival),'weak_bridge_upper_strict':str(cap),
            'nonuniqueness_lower_strict':str(lower),'margin_above_one_third':str(margin)}

def main():
    sites=list(itertools.product(range(3),range(4)));rest=[v for v in sites if v!=(0,0)]
    tested=0;degree_four=False;disconnected=False;longest=0
    for bits in itertools.product((0,1),repeat=len(rest)):
        c={(0,0)}|{v for v,keep in zip(rest,bits) if keep}
        deg,m=dual_check(c);degree_four|=deg==4;longest=max(longest,m);tested+=1
        adj={v:set(neigh(v))&c for v in c};disconnected|=len(bfs(adj,(0,0)))<len(c)
    need(degree_four and disconnected,'boundary case coverage')
    weak_paths=canonical_weak_paths()
    controls={}
    def rejected(name,fun):
        try:fun()
        except RuntimeError:controls[name]='rejected';return
        raise RuntimeError('false control survived '+name)
    rejected('omit_bottom_dual_crossings',lambda:dual_check({(0,0)},True))
    rejected('drop_corner_precondition',lambda:dual_check({(1,1)}))
    rejected('replace_series_AND_by_OR',lambda:series_check(True))
    rejected('map_internal_vertices_to_far_endpoint',lambda:metric_check(True))
    rejected('all_interior_dual_degrees_are_two',lambda:need(not degree_four,'degree-four witness'))
    rejected('corner_cluster_must_be_connected_for_parity',lambda:need(not disconnected,'disconnected-set witness'))
    rejected('unsubdivided_weak_parameter_has_convergent_path_sum',lambda:bridge_bound(F(19,20),1))
    rejected('finite_start_cutoff_covers_every_bridge',lambda:need(weak_paths['furthest_start_coordinate']<=8,'actual distant weak path'))
    # A shared bond creates dependence, whereas shared endpoints above do not.
    p=F(2,5)
    worlds=[(0,1-p),(1,p)]
    marginal=sum((w for bit,w in worlds if bit),F(0))
    joint=sum((w for bit,w in worlds if bit and bit),F(0))
    rejected('overlapping_bond_sets_remain_independent',lambda:need(joint==marginal*marginal,'enumerated shared-bond joint law'))
    print(json.dumps({'status':'PASS','dual_sets':tested,'degree_four_and_disconnected_sets_checked':True,
          'largest_selected_dual_path':longest,'series':series_check(),'metric':metric_check(),
          'explicit_all_weak_paths':weak_paths,'rational_constants':constants(),
          'negative_controls':controls,'scope':'Finite exact diagnostics only; infinite paths/events and universal metric claims rest on written proof. No priority certificate.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
