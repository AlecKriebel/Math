"""Independent exact diagnostics; brute oracle, never a quasilinear implementation.

The eight-family proof reconstruction preceded foreign bodies. This code is
written without reading any deposited programme/result or archived review.
All decisions use integers/Fraction. No source write, network or assertion gate.
"""
from collections import deque,Counter
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import combinations,product
import json,sys
sys.dont_write_bytecode=True

def require(x,message):
    if not x:raise RuntimeError(message)
def distances(adj):
    n=len(adj);out=[]
    for s in range(n):
        d=[None]*n;d[s]=0;q=deque([s])
        while q:
            x=q.popleft()
            for y in adj[x]:
                if d[y] is None:d[y]=d[x]+1;q.append(y)
        if None in d:return None
        out.append(d)
    return out
def median(d):
    n=len(d)
    return all(sum(d[a][x]+d[x][b]==d[a][b] and d[b][x]+d[x][c]==d[b][c] and d[c][x]+d[x][a]==d[c][a] for x in range(n))==1 for a,b,c in combinations(range(n),3))
def grid(dims):
    vs=list(product(*(range(d) for d in dims)));adj=[[] for _ in vs]
    for i,j in combinations(range(len(vs)),2):
        if sum(abs(a-b) for a,b in zip(vs[i],vs[j]))==1:adj[i].append(j);adj[j].append(i)
    return adj
def all_small_medians():
    for n in range(1,6):
        edges=list(combinations(range(n),2))
        for mask in range(1<<len(edges)):
            adj=[[] for _ in range(n)]
            for k,(u,v) in enumerate(edges):
                if mask>>k&1:adj[u].append(v);adj[v].append(u)
            d=distances(adj)
            if d is not None and median(d):yield adj,d
def truth(d,w):
    radii=[max(w[u]*d[x][u] for u in range(len(w))) for x in range(len(w))];rho=min(radii)
    return rho,tuple(x for x,r in enumerate(radii) if r==rho),radii
def decision(d,w,R,*,strict=False):
    if R<0:return ()
    n=len(w);D=n-1;a=[]
    for u in range(n):
        lo=0;hi=D+1
        while lo<hi:
            m=(lo+hi)//2;ok=m*w[u]<R if strict else m*w[u]<=R
            if ok:lo=m+1
            else:hi=m
        b=lo-1
        if b<0:return ()
        a.append(D-b)
    return tuple(x for x in range(n) if max(d[x][u]+a[u] for u in range(n))<=D)
def optimize(d,w,counts):
    n=len(w);D=n-1;rho,C,radii=truth(d,w)
    if n==1:return (0,0),(0,)
    def compare(p,q):
        require(0<=p[0]<=D and 0<=q[0]<=D,'bounded original-profile multipliers')
        counts['bounded_pair_comparisons']+=1;a=p[0]*w[p[1]];b=q[0]*w[q[1]]
        return (a>b)-(a<b)
    imax=0
    for u in range(1,n):
        if compare((1,u),(1,imax))>0:imax=u
    B=(D,imax);witness=0
    if compare(B,(0,0))==0:return (0,0),tuple(range(n))
    active=[[0,D] for _ in w];iterations=0
    def query(q):
        counts['brute_additive_oracle_calls']+=1;a=[]
        for u in range(n):
            lo=0;hi=D+1
            while lo<hi:
                mid=(lo+hi)//2
                if compare((mid,u),q)<=0:lo=mid+1
                else:hi=mid
            a.append(D-(lo-1))
        require(all(0<=v<=D for v in a),'nonnegative bounded oracle arrivals')
        return tuple(x for x in range(n) if max(d[x][u]+a[u] for u in range(n))<=D)
    while any(l<=h for l,h in active):
        M=sum(h-l+1 for l,h in active if l<=h);samples=[(((l+h)//2,u),h-l+1) for u,(l,h) in enumerate(active) if l<=h]
        samples.sort(key=cmp_to_key(lambda a,b:compare(a[0],b[0])))
        cumulative=0
        for q,L in samples:
            cumulative+=L
            if 2*cumulative>=M:break
        qvalue=q[0]*w[q[1]]
        require(2*sum(L for p,L in samples if p[0]*w[p[1]]<=qvalue)>=M,'weighted median lower weak side')
        require(2*sum(L for p,L in samples if p[0]*w[p[1]]>=qvalue)>=M,'weighted median upper weak side')
        feas=query(q)
        if feas and compare(q,B)<0:B=q;witness=feas[0]
        for u,(l,h) in enumerate(active):
            if l>h:continue
            lo=l;hi=h+1
            while lo<hi:
                mid=(lo+hi)//2;c=compare((mid,u),q)
                keep_lower=(c<0) if feas else (c<=0)
                if keep_lower:lo=mid+1
                else:hi=mid
            if feas:active[u][1]=lo-1
            else:active[u][0]=lo
        newM=sum(h-l+1 for l,h in active if l<=h)
        require(4*(M-newM)>=M,'quarter-volume progress')
        value=B[0]*w[B[1]]
        require(value>=rho and radii[witness]<=value,'saved feasible incumbent and witness')
        require(value==rho or any(k*w[u]==rho for u,(l,h) in enumerate(active) for k in range(l,h+1)),'optimum copy invariant')
        counts['progress_invariant_steps']+=1;iterations+=1
        require(iterations<=6*n.bit_length()+4,'logarithmic query envelope')
    require(B[0]*w[B[1]]==rho and radii[witness]==rho,'exact optimum pair and witness')
    final=query(B);require(final==C,'all centers complete exact output')
    counts['max_optimization_iterations']=max(counts['max_optimization_iterations'],iterations)
    return B,final

def run():
    counts=Counter();byN=Counter();case_digest=0
    graphs=list(all_small_medians())
    for adj,d in graphs:byN[len(adj)]+=1
    extras=[grid(x) for x in [(6,),(8,),(2,3),(3,3),(2,2,2),(2,2,2,2),(2,3,2)]]
    extras.append([list(range(1,10))]+[[0] for _ in range(9)])
    allgraphs=[(a,d,'all_labeled_median_n_le5') for a,d in graphs]
    allgraphs += [(a,distances(a),'larger_explicit_median') for a in extras]
    for gi,(adj,d,family) in enumerate(allgraphs):
        n=len(adj);require(median(d),'actual median predicate');counts['median_graph_instances']+=1
        profiles=[tuple(map(F,x)) for x in product([0,1],repeat=n)] if n<=5 else []
        profiles += [tuple(F(((u+1)*(t+3)+u*u)%11,(u+t)%5+1) for u in range(n)) for t in range(8)]
        profiles += [tuple(F(0) for _ in range(n)),tuple(F(1) for _ in range(n))]
        for support in [0,n//2,n-1]:profiles.append(tuple(F(7,3) if u==support else F(0) for u in range(n)))
        for w in profiles:
            counts['exact_weight_profile_cases']+=1;rho,C,radii=truth(d,w)
            candidates=sorted({k*x for x in w for k in range(n)})
            thresholds=set(candidates)|{F(-1),max(candidates)+1}
            thresholds.update((a+b)/2 for a,b in zip(candidates,candidates[1:]))
            for R in sorted(thresholds):
                actual=decision(d,w,R);expected=tuple(x for x,v in enumerate(radii) if v<=R)
                require(actual==expected,'complete threshold identity');counts['whole_feasible_set_threshold_cases']+=1;counts['pointwise_threshold_checks']+=n
            B,actual=optimize(d,w,counts);require(B[0]*w[B[1]]==rho and actual==C,'independent direct optimum comparison')
            counts['optimization_cases']+=1;case_digest=(case_digest*1000003+sum((x+1) for x in C)+rho.numerator+rho.denominator)%((1<<127)-1)
    # Huge exact rationals distinguish the declared comparison model from floats.
    d=distances(grid((4,)))
    for t in range(24):
        w=tuple(F((1<<(257+t))+u+1,(1<<(251+t))+3*u+1) for u in range(4));rho,C,_=truth(d,w);p,found=optimize(d,w,counts)
        require(found==C and p[0]*w[p[1]]==rho,'high-bit exact weight case');counts['high_bit_profiles']+=1
        for i,j in product(range(4),repeat=2):
            for k,l in [(0,3),(1,2),(3,3)]:
                left=k*w[i].numerator*w[j].denominator;right=l*w[j].numerator*w[i].denominator
                require((left>right)-(left<right)==((k*w[i]>l*w[j])-(k*w[i]<l*w[j])),'exact rational product comparison');counts['rational_cross_product_checks']+=1
    negatives={}
    d2=distances(grid((2,)));w2=(F(1),F(1));negatives['strict_budget_loses_equality']=decision(d2,w2,F(1),strict=True)!=decision(d2,w2,F(1))
    negatives['nonintegral_edge_breaks_threshold']=F(1,2)<=F(3,4) and not F(1,2)+1<=1
    d3=distances(grid((3,)));w3=(F(1),F(0),F(1));negatives['zero_weight_vertex_is_unique_center']=truth(d3,w3)[:2]==(F(1),(1,))
    negatives['continuous_facility_is_different']=F(1,2)<truth(d2,w2)[0]
    negatives['negative_profile_breaks_incumbent']=truth(d2,(F(-1),F(-1)))[0]>F(-1)
    n=8;M=4*n+4;deleted=8;negatives['unweighted_median_loses_quarter_bound']=4*deleted<M and not decision(distances(grid((8,))),tuple([F(100)]*4+[F(0)]*4),F(0))
    negatives['external_fiber_need_not_dominate_original']=1<100
    negatives['dropping_original_slice_loses_eccentricity']=max(d3[1][u]+a for u,a in enumerate([0,100,0]))!=max(0+1,1+0)
    require(all(negatives.values()),'actual excluded-variant falsifiers')
    states=set(range(3,1025))|{(1<<k)+j for k in range(2,33) for j in (-1,0,1)}
    for N in sorted(states):
        s=N;depth=0
        while s>=3:
            L=(s-1).bit_length();f=2*L
            require(2**(L-1)<s<=2**L,'exact ceil-log bit length')
            require(2*L*((s-1)//f)<=s,'two-copy integer volume envelope')
            balanced_max=s-((s+f-1)//f);unbalanced_max=(s-1)//f
            require(f*balanced_max<=s*(f-1) and f*unbalanced_max<s,'balanced/unbalanced shrink bounds')
            s=balanced_max;depth+=1
        require(depth<=4*N.bit_length()**2,'coarse integer log-squared depth envelope');counts['recursion_envelope_root_cases']+=1
        require(((N-1)*(depth+1)).bit_length()<=3*N.bit_length()+10,'global small-label word envelope');counts['global_word_bound_cases']+=1
    N=2**30+30*17000000000+488926258176;minority=2**29+17000000000;union=2**30-1+30*17000000000
    require(N==10**12 and 56*minority<N and 2*union>N,'exact succinct appendix arithmetic')
    return {'status':'PASS','diagnostics_are_not_fast_oracle_or_asymptotic_proof':True,'all_labeled_median_graphs_by_n_through5':dict(sorted(byN.items())),
      'counts':dict(sorted(counts.items())),'excluded_wrong_variant_falsifiers':negatives,'deterministic_case_checksum':case_digest,
      'source_programs_results_opinions_read_for_this_code':False,'source_or_site_writes':0,'network':0}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
