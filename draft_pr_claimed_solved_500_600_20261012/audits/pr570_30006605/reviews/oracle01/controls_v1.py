#!/usr/bin/env python3
"""Independent exact finite falsification controls, not the fast implementation."""
from collections import deque,Counter
from fractions import Fraction as F
from itertools import combinations,product
from datetime import datetime,timezone
from decimal import Decimal,localcontext
from pathlib import Path
import json,hashlib,time

STATS=Counter()

def distances(adj):
    out=[]
    for s in range(len(adj)):
        d=[-1]*len(adj);d[s]=0;q=deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if d[v]<0:d[v]=d[u]+1;q.append(v)
        if min(d)<0:return None
        out.append(d)
    return out

def median(d):
    for a,b,c in combinations(range(len(d)),3):
        if sum(d[a][z]+d[z][b]==d[a][b] and d[b][z]+d[z][c]==d[b][c] and d[c][z]+d[z][a]==d[c][a] for z in range(len(d)))!=1:return False
    return True

def radii(d,w):return [max(F(d[x][u])*w[u] for u in range(len(w))) for x in range(len(w))]

def additive_feasible(d,w,R):
    n=len(w);D=n-1
    if R<0:return []
    # Deliberately scan all integer bounds; independent from binary search.
    a=[D-max(k for k in range(D+1) if k*w[u]<=R) for u in range(n)]
    assert all(type(x) is int and 0<=x<=D for x in a)
    E=[max(d[x][u]+a[u] for u in range(n)) for x in range(n)]
    return [x for x in range(n) if E[x]<=D]

def implicit_search(d,w):
    n=len(w);r=radii(d,w);opt=min(r)
    if n==1:return F(0),[0]
    D=n-1;B=D*max(w);witness=0
    if B==0:return B,list(range(n))
    bounds=[[0,D] for _ in w];it=0
    while (M:=sum(max(0,h-l+1) for l,h in bounds)):
        before=[k*w[u] for u,(l,h) in enumerate(bounds) for k in range(l,h+1)]
        assert B==opt or opt in before
        mids=sorted(((l+h)//2*w[u],h-l+1) for u,(l,h) in enumerate(bounds) if l<=h)
        cum=0
        for q,L in mids:
            cum+=L
            if 2*cum>=M:break
        assert 2*sum(L for v,L in mids if v<=q)>=M
        assert 2*sum(L for v,L in mids if v>=q)>=M
        feasible=additive_feasible(d,w,q)
        assert feasible==[x for x in range(n) if r[x]<=q]
        if feasible and q<B:B=q;witness=feasible[0]
        for u,(l,h) in enumerate(bounds):
            # Use exact linear filtering, independently of binary bound searches.
            keep=[k for k in range(l,h+1) if (k*w[u]<q if feasible else k*w[u]>q)]
            bounds[u]=[min(keep),max(keep)] if keep else [1,0]
        after=sum(max(0,h-l+1) for l,h in bounds)
        assert 4*after<=3*M
        assert r[witness]<=B
        STATS['pivot_checks']+=1;it+=1
    assert B==opt
    STATS['max_search_iterations']=max(STATS['max_search_iterations'],it)
    return B,additive_feasible(d,w,B)

def check_profile(d,w,all_thresholds=True):
    w=tuple(map(F,w));r=radii(d,w);opt=min(r)
    if all_thresholds:
        vals=sorted({k*x for x in w for k in range(len(w))})
        probes=[F(-1)]+vals+[(x+y)/2 for x,y in zip(vals,vals[1:])]+[max(vals)+1]
        for R in probes:
            assert additive_feasible(d,w,R)==[x for x in range(len(w)) if r[x]<=R]
            STATS['threshold_vector_checks']+=1
    B,centers=implicit_search(d,w)
    assert B==opt and centers==[x for x in range(len(w)) if r[x]==opt]
    STATS['profiles']+=1


def all_small():
    graphs={}
    for n in range(1,6):
        edges=list(combinations(range(n),2));count=Counter()
        for mask in range(1<<len(edges)):
            adj=[[] for _ in range(n)]
            for i,(u,v) in enumerate(edges):
                if mask>>i&1:adj[u].append(v);adj[v].append(u)
            d=distances(adj)
            if d is None:continue
            count['connected']+=1;ismed=median(d)
            if ismed:count['median']+=1
            if n<=4:
                weights=[F(0),F(1,7),F(1),F(10)]
            elif ismed:
                weights=[F(0),F(1,3),F(5)]
            else:continue
            for w in product(weights,repeat=n):check_profile(d,w,all_thresholds=n<=3)
        graphs[n]=dict(count)
    return graphs


def graph_from_edges(n,edges):
    a=[[] for _ in range(n)]
    for u,v in edges:a[u].append(v);a[v].append(u)
    return a

# Reproduce the repaired BDH mechanism with brute structural preprocessing.
# Its runtime is deliberately not the theorem's claimed runtime.
def morse(adj,w):
    master=distances(adj);w=list(w)
    def recurse(V,omega,depth=0):
        N=len(V);STATS['morse_calls']+=1;STATS['morse_depth']=max(STATS['morse_depth'],depth)
        if N<=2:return {x:max(master[x][y]+omega[y] for y in V) for x in V}
        Vset=set(V);classes={}
        for x in V:
            for y in adj[x]:
                if y not in Vset or x>y:continue
                H=frozenset(z for z in V if master[z][x]<master[z][y]);K=frozenset(Vset-H)
                key=min(tuple(sorted(H)),tuple(sorted(K)))
                classes[key]=(set(H),set(K))
        f=4*(N-1).bit_length() # 4 ceil(log_2 N), exact integer
        for H,K in classes.values():
            if f*min(len(H),len(K))>=N:
                STATS['balanced_calls']+=1
                left=recurse(sorted(H),omega,depth+1);right=recurse(sorted(K),omega,depth+1)
                out={}
                for P,Q,A,B in ((H,K,left,right),(K,H,right,left)):
                    for x in P:
                        gate=min(Q,key=lambda z:master[x][z])
                        assert all(master[x][z]==master[x][gate]+master[gate][z] for z in Q)
                        out[x]=max(A[x],master[x][gate]+B[gate])
                assert out=={x:max(master[x][y]+omega[y] for y in V) for x in V}
                return out
        STATS['unbalanced_calls']+=1
        v0=min(V,key=lambda x:sum(master[x][y] for y in V))
        assert sum(sum(master[x][y] for y in V)==sum(master[v0][y] for y in V) for x in V)==1
        val=max(master[v0][y]+omega[y] for y in V)
        umax=v0 if omega[v0]==val else next(y for y in V if master[v0][y]+omega[y]==val)
        if umax==v0:
            STATS['dominance_calls']+=1
            return {x:master[x][v0]+omega[v0] for x in V}
        cuts=[]
        for H,K in classes.values():
            if v0 in H:H,K=K,H
            if umax in H and any(y in H for y in adj[v0]):cuts.append(H)
        STATS['max_wide_ladder']=max(STATS['max_wide_ladder'],len(cuts))
        assert cuts
        G=set(V);slices=[]
        for H in cuts:
            S=G&H;rest=G-S;assert S and rest
            assert f*len(S)<N
            stars=dict(omega)
            for x in S:
                fiber=[z for z in rest if master[z][x]==min(master[z][y] for y in S)]
                if fiber:stars[x]=max(master[x][z]+omega[z] for z in fiber)
            slices.append((G.copy(),S,recurse(sorted(S),omega,depth+1),recurse(sorted(S),stars,depth+1)))
            G=rest
        assert 2*sum(len(S) for _,S,_,_ in slices)<=N
        out={x:master[x][v0]+val for x in G}
        for Gi,S,A,B in reversed(slices):
            for x in S:out[x]=max(A[x],B[x])
            for x in Gi-S:
                gate=min(S,key=lambda z:master[x][z])
                out[x]=max(out[x],master[x][gate]+A[gate])
        assert out=={x:max(master[x][y]+omega[y] for y in V) for x in V}
        return out
    out=recurse(list(range(len(adj))),dict(enumerate(w)))
    assert out=={x:max(master[x][y]+w[y] for y in range(len(w))) for x in range(len(w))}
    return out


def source_branch_controls():
    # A 3-cube with 400 leaves at 000: median by gated one-vertex tree attachments.
    core=8;leaves=400;n=core+leaves
    edges=[(x,x^(1<<i)) for x in range(core) for i in range(3) if x<x^(1<<i)]
    edges += [(0,x) for x in range(core,n)]
    adj=graph_from_edges(n,edges)
    profiles=[]
    profiles.append([0]*n)
    a=[0]*n;a[0]=2*n;profiles.append(a) # dominance including exact ties below
    a=[0]*n;a[0]=n;a[7]=n-3;profiles.append(a)
    a=[0]*n;a[7]=n;profiles.append(a) # ladder of size three and both fiber calls
    a=[(x*37)%n for x in range(n)];profiles.append(a)
    for w in profiles:morse(adj,w)
    # balanced tiny cube cases, with zero, equal and asymmetric values.
    for d in (1,2,3,4):
        n=1<<d;adj=graph_from_edges(n,[(x,x^(1<<i)) for x in range(n) for i in range(d) if x<x^(1<<i)])
        for w in ([0]*n,list(range(n)),[n-1]*n):morse(adj,w)
    return {'explicit_profiles':len(profiles)+12,'largest_n':core+leaves,'scope':'Brute-force structural implementation of repaired algorithm; no asymptotic implementation validation.'}


def log_base_counterexample():
    # Succinct finite graph: Q_30, t pendant leaves at each e_i,
    # and s leaves at 0. All inherited Theta cuts plus singleton leaf cuts.
    # Decimal ln and a wide interval certify strict inequalities robustly.
    n=10**12;ell=30;q=1<<ell
    with localcontext() as ctx:
        ctx.prec=80
        ln=Decimal(n).ln();bound=Decimal(n)/(2*ln)
        t=int(bound)-(q//2)-1;s=n-q-ell*t
        minority=q//2+t;union=q-1+ell*t
        assert s>=0 and Decimal(minority)<bound
        assert ell>ln and 2*union>n
        return {'n':n,'cube_dimension':ell,'cube_vertices':q,'leaves_at_each_unit_vector':t,'leaves_at_zero':s,'each_core_cut_minority':minority,'natural_log_threshold_approx':str(bound),'union_of_wide_ladder_minorities':union,'duplicated_slice_volume':2*union,'claimed_volume_upper_bound':n,'verified_strict_violation':True,'mechanism':'Give cube antipode omega=n and all other vertices omega=0, yielding unique u_max at the antipode; the wide ladder consists of all 30 cube classes. Pendant-leaf attachment preserves medianity. Every cut is natural-log-unbalanced but two copies of all slices contain more than n vertices.'}


def main():
    started=datetime.now(timezone.utc).isoformat();tick=time.monotonic()
    small=all_small();branch=source_branch_controls();counter=log_base_counterexample()
    result={'started_at_utc':started,'completed_at_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':round(time.monotonic()-tick,3),'status':'all_assertions_passed','small_graphs_by_n':small,'counts':dict(STATS),'source_branch_controls':branch,'literal_v1_volume_counterexample':counter,'limitations':['No implementation of linear-time Theta/halfspace preprocessing.','No runtime experiment certifies an asymptotic theorem.','Classical median structural theorems are relied on, not formally proved.'],'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path('CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
