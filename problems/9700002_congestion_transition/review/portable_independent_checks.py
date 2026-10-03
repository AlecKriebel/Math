#!/usr/bin/env python3
"""Independent review tests. Does not import candidate code or alter frozen input."""
from fractions import Fraction as F
from collections import deque
from itertools import product
from pathlib import Path
import hashlib,json,math,platform
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.stats import gamma

ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
rng=np.random.default_rng(37000029)

def exact_transport(d):
    """Rational Edmonds-Karp, independently implemented."""
    k=len(d); n=2*k+2; s=2*k; z=s+1
    c=[[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(k):
        c[s][i]=F(2*k); c[k+i][z]=F(2*k)
        for j in range(k): c[i][k+j]=F(d[i][j])
    total=F(0)
    while True:
        parent=[-1]*n; parent[s]=s; q=deque([s])
        while q and parent[z]<0:
            u=q.popleft()
            for v in range(n):
                if parent[v]<0 and c[u][v]>0: parent[v]=u; q.append(v)
        if parent[z]<0: return total
        v=z; bottleneck=None
        while v!=s:
            u=parent[v]; bottleneck=c[u][v] if bottleneck is None else min(bottleneck,c[u][v]); v=u
        v=z
        while v!=s:
            u=parent[v]; c[u][v]-=bottleneck; c[v][u]+=bottleneck; v=u
        total+=bottleneck

def lines(x):
    """Enumerate complete source/sink cuts directly by side membership."""
    k=len(x); out=[]
    for side in product([False,True],repeat=2*k):
        base=F(0); slope=F(0)
        for i in range(k):
            if not side[i]: base+=2*k
            if side[k+i]: base+=2*k
            for j in range(k):
                if side[i] and not side[k+j]: base+=1; slope+=x[i][j]
        out.append((base-slope,slope))
    return out

def envelope(ls,t):
    value=min(b+m*t for b,m in ls)
    active=[m for b,m in ls if b+m*t==value]
    return value,min(active),max(active)

def incidence(k):
    """Build tree paths by BFS in an undirected physical tree."""
    N=4*k-1; adj=[[] for _ in range(N)]
    for v in range(1,N):
        p=(v-1)//2; adj[v].append((p,v-1)); adj[p].append((v,v-1))
    a=np.zeros((N-1,k*k))
    for i,j in product(range(k),repeat=2):
        s=2*k-1+i; z=3*k-1+j
        par={s:(None,None)}; q=deque([s])
        while z not in par:
            u=q.popleft()
            for v,e in adj[u]:
                if v not in par: par[v]=(u,e); q.append(v)
        v=z
        while v!=s:
            u,e=par[v]; a[e,i*k+j]=1; v=u
    return a,2*a.sum(axis=1)

def physical(d):
    k=len(d); a,c=incidence(k); flat=np.asarray(d,dtype=float).ravel()
    opt=linprog(-np.ones(k*k),A_ub=a,b_ub=c,bounds=[(0,v) for v in flat],method='highs')
    assert opt.success
    return -opt.fun,opt.x,a,c,flat

checks=[]
input_files=0
for turn in ['turn_01','turn_02']:
    folder=ROOT/'turns'/turn
    manifest=json.loads((folder/'FREEZE_MANIFEST.json').read_text())
    for name,meta in manifest['files'].items():
        data=(folder/name).read_bytes()
        assert len(data)==meta['bytes'] and hashlib.sha256(data).hexdigest()==meta['sha256']
        input_files+=1
checks.append({'name':'Public frozen author inputs verified','files':input_files,'pass':True})

rational_cases=0; breakpoints=0; max_lp_error=0
for flat in product([F(1,4),F(1),F(4)],repeat=4):
    x=[list(flat[:2]),list(flat[2:])]; ls=lines(x)
    for t in [F(1),F(3,2),F(2),F(5,2),F(5)]:
        d=[[1+(t-1)*v for v in row] for row in x]
        v=exact_transport(d); g,_,_=envelope(ls,t)
        assert v==g
        lp,*_=physical(d); max_lp_error=max(max_lp_error,abs(lp-float(v)))
        assert abs(lp-float(v))<1e-8; rational_cases+=1
    # Find actual (not all pairwise) lower-envelope slope-change times.
    intersections={F(1)}
    for b,m in ls:
        for b2,m2 in ls:
            if m!=m2:
                t=(b2-b)/(m-m2)
                if t>1: intersections.add(t)
    ordered=sorted(intersections)
    for idx,t in enumerate(ordered):
        value,right,left=envelope(ls,t)
        if left==right: continue
        eps=min([F(1,100)]+[(t-ordered[idx-1])/3] if idx else [F(1,100)])
        if idx+1<len(ordered): eps=min(eps,(ordered[idx+1]-t)/3)
        vr,_,_=envelope(ls,t+eps)
        assert (vr-value)/eps==right
        if t>1:
            vl,_,_=envelope(ls,t-eps); assert (value-vl)/eps==left
        assert exact_transport([[1+(t-1)*v for v in row] for row in x])==value
        breakpoints+=1
checks.append({'name':'Exact rational max flow, all cuts, independent physical LP, and kink derivatives',
               'rational_flow_cases':rational_cases,'actual_kinks_checked':breakpoints,
               'max_physical_lp_error':max_lp_error,'pass':True})

# Physical edge extrema over the complete optimal face, including one-sided endpoints.
face_cases=0; edge_extrema=0; max_error=0
for k in [2,4,8]:
    a,c=incidence(k)
    x=rng.exponential(size=(k,k))
    max_sum=max(x.sum(0).max(),x.sum(1).max())
    t_low=1+.999*k/max_sum # every offered terminal is strictly slack
    t_high=1+1/x.min() # each entry demand >=2, so y=2 feasible
    for t,kind in [(t_low,'strict_full_demand'),(t_high,'full_capacity_endpoint')]:
        d=1+(t-1)*x; value,y,a,c,flat=physical(d)
        expected=flat.sum() if kind.startswith('strict') else 2*k*k
        assert abs(value-expected)<1e-7
        for e in range(len(c)):
            args=dict(A_ub=a,b_ub=c,A_eq=np.ones((1,k*k)),b_eq=[expected],bounds=[(0,v) for v in flat],method='highs')
            low=linprog(a[e],**args); high=linprog(-a[e],**args)
            assert low.success and high.success
            error=abs(low.fun+high.fun); max_error=max(max_error,error)
            assert error<2e-6
            if kind.startswith('strict'): assert -high.fun<c[e]-1e-7
            else: assert abs(low.fun-c[e])<2e-6
            edge_extrema+=2
        face_cases+=1
checks.append({'name':'All-optimizer edge-load invariance and endpoint phases',
               'face_cases':face_cases,'edge_extrema':edge_extrema,'max_load_range_width':max_error,'pass':True})

# Independent mixed-cut obstruction: every terminal has enough offered demand,
# but a 3-by-2 rectangle cannot meet the transport cut lower bound.
k=4
u=[[F(3),F(3),F(6,5),F(6,5)] for _ in range(3)]+[[F(6,5),F(6,5),F(5),F(5)]]
assert all(sum(r)>8 for r in u) and all(sum(u[i][j] for i in range(k))>8 for j in range(k))
f=exact_transport(u); assert f==F(156,5)<32
x=[[v-1 for v in row] for row in u]
assert envelope(lines(x),F(2))[0]==f
checks.append({'name':'Independent mixed-cut counterexample to row/column-only criterion','throughput':str(f),'capacity':'32','rectangle_area':6,'rectangle_demand':'36/5','required':'8','pass':True})

# Sharp finite critical point and strict spare threshold must not be mislabeled.
for k in [2,4]:
    x=[[F(1)]*k for _ in range(k)]; v,der,_=envelope(lines(x),F(2))
    assert v==2*k*k and der==0
    f,y,a,c,d=physical([[F(2)]*k for _ in range(k)])
    assert np.allclose(a@y,c)
checks.append({'name':'Deterministic tie control: r(2)=0 and spare graph edgeless, not whole','pass':True})

# Inside the window, different optimizers really can have different spare graphs.
# This is an exclusion check, not a counterexample to the claimed outer phases.
d=np.array([[4.,4.],[1.1,1.1]])
f,_,a,c,flat=physical(d)
y1=np.array([2.9,1.1,1.1,1.1]); y2=np.array([2.,2.,1.1,1.1])
assert abs(f-6.2)<1e-9
for y in [y1,y2]:
    assert abs(y.sum()-f)<1e-9 and np.all(y<=flat+1e-9) and np.all(a@y<=c+1e-9)
spare1=(c-a@y1)>1e-8; spare2=(c-a@y2)>1e-8
assert int(spare1.sum())==4 and int(spare2.sum())==5
checks.append({'name':'Critical-time optimizer noninvariance exclusion control',
               'k':2,'t':2,'positive_rate_matrix':[[3,3],[.1,.1]],'throughput':f,
               'optimal_spare_edge_counts':[int(spare1.sum()),int(spare2.sum())],
               'interpretation':'All-optimizer full/edgeless assertion cannot be extended to arbitrary critical-time realizations. Candidate correctly excludes this.',
               'pass':True})

# Verify every positive-cut multiplicity, exact gamma failure probabilities and
# the candidate split majorants. Checks use true thresholds, not author's looser ones.
size_classes=0
for k in range(2,81):
    count=0; small={q:0 for q in range(1,k//2+1)}
    for a in range(k+1):
        for d in range(k+1):
            if a+d<=k: continue
            mult=math.comb(k,a)*math.comb(k,d); count+=mult
            q=min(a,d); ell=k-max(a,d); size_classes+=1
            assert 0<=ell<q and a*d==q*(k-ell)
            assert a*d-k*(a+d-k)==(k-a)*(k-d)>=0
            if q<=k//2: small[q]+=mult; assert a*d>=q*k/2
            else: assert a*d>k*k/4
    assert count==(4**k-math.comb(2*k,k))//2
    for q,m in small.items(): assert m<=2*q*k**(2*q)
exact_union=[]
for k,delta in [(2,.2),(4,.5),(8,.9),(16,.25),(32,.7)]:
    union=0.; loose_union=0.; c=math.log1p(delta)-delta/(1+delta)
    for a in range(1,k+1):
        for d in range(1,k+1):
            if a+d<=k:continue
            threshold=(2*k*(a+d-k)-a*d)/(1+delta)
            prob=0 if threshold<=0 else float(gamma.cdf(threshold,a*d))
            bound=math.exp(-c*a*d)
            assert prob<=bound+1e-14
            mult=math.comb(k,a)*math.comb(k,d)
            union+=mult*prob; loose_union+=mult*bound
    exact_union.append({'k':k,'delta':delta,'sum_exact_cut_failure_probabilities':union,'sum_chernoff_bounds':loose_union})
for delta in np.geomspace(1e-5,.99999,1000):
    lower=math.log1p(delta)-delta/(1+delta)
    upper=delta/(1-delta)+math.log1p(-delta)
    assert lower+1e-16>=delta*delta/8 and upper+1e-16>=delta*delta/2
checks.append({'name':'All-cut combinatorics, actual gamma tails, Chernoff constants',
               'size_classes_checked':size_classes,'exact_union_diagnostics':exact_union,'pass':True})

# Explicit finite admissibility threshold along the candidate's power-of-two sequence.
ks=[2**p for p in range(1,22)]
first=next(k for k in ks if 8*math.sqrt(math.log(k)/k)<1)
assert first==512
checks.append({'name':'First admissible family member for advertised delta<1','k':first,'H':10,'N':4*first-1,'pass':True})

report={'review_seed':37000029,'independent_of_author_code':True,'python':platform.python_version(),
        'numpy':np.__version__,'scipy':scipy.__version__,'all_assertions_passed':True,'checks':checks,
        'scope':'Numerical checks supplement the separate proof/source audit; they do not establish probability asymptotics or novelty.'}
(OUT/'PORTABLE_INDEPENDENT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
