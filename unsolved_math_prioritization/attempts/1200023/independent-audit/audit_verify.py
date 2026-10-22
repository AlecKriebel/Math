#!/usr/bin/env python3
"""Independent, portable audit of AMR-011-0023. Standard library only.
Usage: python3 -B audit_verify.py /path/to/frozen/rank638-1200023 > results.json
No original input is changed. No network, private data, or source text required.
"""
from collections import deque
from itertools import combinations, product
from pathlib import Path
import hashlib, importlib.util, json, subprocess, sys, zipfile
sys.dont_write_bytecode = True
EXPECTED_TREE='06b401911f19d2483353f6d5957359f593f856d0cf24a36b51d32a04efbd1fba'
EXPECTED_ZIP='3f4ac5aa460f57ed75bd55423c536ac7f6edc528c06fa35aefac1883e66efb93'

def bfs(ng,root,r=None):
    d={root:0}; q=deque([root])
    while q:
        v=q.popleft()
        if d[v]==r: continue
        for w in ng(v):
            if w not in d: d[w]=d[v]+1;q.append(w)
    return d

def outer(ng,A): return set().union(*(set(ng(v)) for v in A))-set(A) if A else set()
def subsets(U):
    U=list(U)
    for mask in range(1<<len(U)): yield {v for i,v in enumerate(U) if mask>>i&1}
def objective(ng,A,c): return sum(c[w] for w in outer(ng,A))-len(A)
def direct(ng,U,c): return min(objective(ng,A,c) for A in subsets(U))

def cut_solver(ng,U,c):
    """Edmonds-Karp, deliberately separate from the submitted Dinic implementation."""
    U=list(U);W=set(U)|outer(ng,U);a={v:i+2 for i,v in enumerate(U)}
    z={v:i+2+len(U) for i,v in enumerate(sorted(W))}; n=2+len(U)+len(W)
    residual=[{} for _ in range(n)];arcs=[];K=sum(c[v]+1 for v in U)
    def add(u,v,cap):
        assert cap>=0 and v not in residual[u]
        residual[u][v]=cap;residual[v][u]=0;arcs.append((u,v,cap))
    for v in U:
        add(0,a[v],c[v]+1)
        for w in set(ng(v))|{v}: add(a[v],z[w],K+1)
    for w in W: add(z[w],1,c[w])
    total=0
    while True:
        pred={0:None};q=deque([0])
        while q and 1 not in pred:
            u=q.popleft()
            for v,cap in residual[u].items():
                if cap>0 and v not in pred: pred[v]=u;q.append(v)
        if 1 not in pred:break
        delta=None;v=1
        while v!=0:
            u=pred[v];delta=residual[u][v] if delta is None else min(delta,residual[u][v]);v=u
        v=1
        while v!=0:
            u=pred[v];residual[u][v]-=delta;residual[v][u]+=delta;v=u
        total+=delta
    reachable=set(pred);cut=sum(cap for u,v,cap in arcs if u in reachable and v not in reachable)
    balance=[0]*n
    for u,v,cap in arcs:
        f=cap-residual[u][v];assert 0<=f<=cap
        balance[u]-=f;balance[v]+=f
    assert total==cut==balance[1]==-balance[0]
    assert all(balance[i]==0 for i in range(2,n))
    A={v for v in U if a[v] in reachable}
    assert objective(ng,A,c)==total-K
    return total-K

# A regular tree as a distinguished one-sided spine with rooted branches.
# (k, ()) is spine level k>=0. Off-spine tails record a unique child path.
# At positive spine levels child 0 leads to the preceding spine vertex;
# the other q-1 children start side branches. At level 0 all q children branch.
def parent(v):
    k,tail=v
    return (k,tail[:-1]) if tail else (k+1,())
def children(v,q):
    k,tail=v
    if tail or k==0:return tuple((k,tail+(i,)) for i in range(q))
    return ((k-1,()),)+tuple((k,(i,)) for i in range(1,q))
def tneighbors(v,q):return (parent(v),)+children(v,q)
def height(v):return v[0]-len(v[1])
def coord(v,q):
    k,tail=v;m=0
    for i in tail:m=q*m+i
    return (height(v),m)
def gneighbors(v,q=2):
    return tneighbors(v,q)+(parent(parent(v)),)+tuple(x for u in children(v,q) for x in children(u,q))
def dneighbors(v,p,q):
    x,y=v
    return tuple((parent(x),w) for w in children(y,q))+tuple((w,parent(y)) for w in children(x,p))
def dcoord(v,p,q):
    x,y=v;h,m=coord(x,p);h2,n=coord(y,q);assert h+h2==0
    return (h,m,n)

def main(root):
    root=Path(root);s=root/'submission';receipt=json.loads((root/'AUTHOR_FREEZE_RECEIPT.json').read_text())
    files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(s.iterdir()) if p.is_file()}
    tree=hashlib.sha256(''.join(n+'\0'+h+'\n' for n,h in sorted(files.items())).encode()).hexdigest()
    assert files==receipt['submission_file_sha256'] and sorted(files)==sorted(receipt['publication_allowlist'])
    assert len(files)==12 and tree==receipt['submission_tree_sha256']==EXPECTED_TREE
    archive=root/receipt['archive_filename'];data=archive.read_bytes()
    assert hashlib.sha256(data).hexdigest()==receipt['archive_sha256']==EXPECTED_ZIP
    assert len(data)==receipt['archive_bytes']==18470
    with zipfile.ZipFile(archive) as z:
        assert sorted(z.namelist())==sorted(files)
        assert all(z.read(n)==(s/n).read_bytes() for n in z.namelist())
    replay=subprocess.check_output([sys.executable,'-B',str(s/'verify.py')]);assert replay==(s/'CONTROL_RESULTS.json').read_bytes()
    manifest=subprocess.check_output([sys.executable,'-B',str(s/'verify_manifest.py')]).decode().strip()
    spec=importlib.util.spec_from_file_location('submission_verify',s/'verify.py');orig=importlib.util.module_from_spec(spec);spec.loader.exec_module(orig)
    reported=json.loads(replay)
    out={'target':'1200023 / AMR-011-0023','frozen_tree_sha256':tree,'frozen_archive_sha256':EXPECTED_ZIP,'file_count':len(files),'archive_bytes':len(data),'replay_byte_identical':True,'submitted_manifest_result':manifest,'independent_networks':[],'alternative_oracles':[]}
    models=[('integer_line',lambda x:(x-1,x+1),0,7),('square_lattice',lambda v:((v[0]-1,v[1]),(v[0]+1,v[1]),(v[0],v[1]-1),(v[0],v[1]+1)),(0,0),6),('binary_grandfather',gneighbors,(0,()),4),('DL_2_3',lambda v:dneighbors(v,2,3),((0,()),(0,())),5),('DL_3_4',lambda v:dneighbors(v,3,4),((0,()),(0,())),4)]
    original_ng=[orig.z_neighbors,orig.z2_neighbors,orig.grandfather_neighbors,orig.dl_neighbors,lambda v:orig.dl_neighbors(v,3,4)]
    transforms=[lambda v:v,lambda v:v,lambda v:coord(v,2),lambda v:dcoord(v,2,3),lambda v:dcoord(v,3,4)]
    for i,(name,ng,b,R) in enumerate(models):
        d=bfs(ng,b,R+1);convert=transforms[i];ng0=original_ng[i];d0=bfs(ng0,convert(b),R+1)
        assert len({convert(v) for v in d})==len(d)
        assert {convert(v):dv for v,dv in d.items()}==d0
        for v in d:
            assert set(map(convert,ng(v)))==set(ng0(convert(v)))
        out['alternative_oracles'].append({'model':name,'radius':R+1,'vertices':len(d),'complete_neighbor_sets_and_distances_match':True})
        for r in range(R+1):
            U={v for v,dv in d.items() if dv<=r};value=cut_solver(ng,U,d)
            assert value==reported['models'][i]['checks'][r]['minimum_deficit']==0
            assert len(U)==reported['models'][i]['checks'][r]['vertices']
            out['independent_networks'].append({'model':name,'radius':r,'vertices':len(U),'minimum_deficit':value,'edmonds_karp_flow_cut_conservation':True})
    # Exhaustive cut identity on every connected labelled simple graph of order <=4,
    # every allowed support (including empty and disconnected), and every basepoint.
    graphs=networks=subset_evaluations=0
    for n in range(1,5):
        edges=list(combinations(range(n),2))
        for mask in range(1<<len(edges)):
            adj=[set() for _ in range(n)]
            for i,(u,v) in enumerate(edges):
                if mask>>i&1:adj[u].add(v);adj[v].add(u)
            ng=lambda v:adj[v]
            if len(bfs(ng,0))!=n:continue
            graphs+=1
            for b in range(n):
                c=bfs(ng,b)
                for U in subsets(range(n)):
                    expected=direct(ng,U,c)
                    assert cut_solver(ng,U,c)==expected==orig.minimize(ng,U,c)['minimum_deficit']
                    networks+=1;subset_evaluations+=1<<len(U)
    out['all_small_graph_cut_identities']={'connected_labelled_graphs':graphs,'orders':[1,2,3,4],'all_supports_and_basepoints':True,'networks':networks,'direct_subset_objectives':subset_evaluations,'submitted_and_independent_flow_agree':True}
    # General nonnegative weights exercise cancellation, multiple zeros and closed neighborhoods.
    ng=lambda v:((v-1)%4,(v+1)%4);weighted=weighted_subsets=0
    for weights in product(range(3),repeat=4):
        c=dict(enumerate(weights))
        for U in subsets(range(4)):
            expected=direct(ng,U,c)
            assert expected==cut_solver(ng,U,c)==orig.minimize(ng,U,c)['minimum_deficit']
            weighted+=1;weighted_subsets+=1<<len(U)
    out['nonnegative_weight_cut_identities']={'graph':'C4','weights_per_vertex':[0,1,2],'all_supports':True,'networks':weighted,'direct_subset_objectives':weighted_subsets}
    # Off-center supports: every subset of small balls, with b inside, on boundary,
    # and farther outside the support, using infinite-graph BFS rather than cropping.
    offcenter=offsubsets=0
    for name,ng,b,R in models:
        support=set(bfs(ng,b,1));ambient=bfs(ng,b,3)
        bases=[b]+[next(v for v,dv in ambient.items() if dv==r) for r in (1,2,3)]
        for base in bases:
            required=support|outer(ng,support);c=bfs(ng,base,5)
            assert required<=c.keys()
            val=cut_solver(ng,support,c);assert val==direct(ng,support,c)==0
            offcenter+=1;offsubsets+=1<<len(support)
    out['offcenter_infinite_graph_controls']={'networks':offcenter,'direct_subset_objectives':offsubsets,'basepoint_distances_from_support_center':[0,1,2,3],'all_minimum_deficits':0}
    # All finite subsets of small regular-tree balls; A need not be connected.
    count=0
    for q,r in [(2,2),(3,1),(4,1)]:
        ng=lambda v:tneighbors(v,q);U=set(bfs(ng,(0,()),r))
        for A in subsets(U):
            if not A:continue
            assert len(outer(ng,A))>=(q-1)*len(A)+2;count+=1
    out['independent_tree_boundary_controls']={'q_and_radii':[[2,2],[3,1],[4,1]],'nonempty_subsets':count}
    out['scope']='PASS for frozen conservative unsolved research packet. No finite experiment proves a universal nonunimodular theorem.'
    return out

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit(__doc__)
    print(json.dumps(main(sys.argv[1]),indent=2,sort_keys=True))
