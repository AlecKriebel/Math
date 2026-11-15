"""Bounded exact falsifiers; mathematical proof is in INITIAL/DERIVATIONS.
No source changes; no package builders; no claim of a fast BDH implementation.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from collections import Counter
import hashlib, importlib.util, json, random, time
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
SUPPLIED=HERE.parents[1]/'sources/attempts/20261115T022501Z/published-source/weighted_centers_verification'

def threshold(d,w,R):
    if R<0:return []
    D=len(w)-1
    # Binary search only bounded index multiples, no floor/division.
    b=[]
    for z in w:
        lo,hi=0,D+1
        while hi-lo>1:
            mid=(lo+hi)//2
            if mid*z<=R:lo=mid
            else:hi=mid
        b.append(lo)
    return [x for x in range(len(w)) if all(d[x][u]+D-b[u]<=D for u in range(len(w)))]

def solve(d,w,counts):
    n=len(w);D=n-1
    actual=[max(w[u]*d[x][u] for u in range(n)) for x in range(n)]
    opt=min(actual);B=D*max(w);witness=0
    lo=[0]*n;hi=[D]*n
    while (M:=sum(max(0,h-l+1) for l,h in zip(lo,hi))):
        assert B==opt or any(any(k*w[u]==opt for k in range(lo[u],hi[u]+1)) for u in range(n))
        mids=sorted((w[u]*((lo[u]+hi[u])//2),hi[u]-lo[u]+1) for u in range(n) if lo[u]<=hi[u])
        # Alternate between the two admissible weighted-median choices at a tie.
        choices=[q for q,_ in mids if 2*sum(L for a,L in mids if a<=q)>=M and 2*sum(L for a,L in mids if a>=q)>=M]
        q=choices[counts['queries']%len(choices)]
        feasible=threshold(d,w,q)
        assert feasible==[x for x,r in enumerate(actual) if r<=q]
        if feasible and q<B:B=q;witness=feasible[-1]
        for u in range(n):
            # Reference pruning deliberately scans rather than sharing budget search.
            keep=[k for k in range(lo[u],hi[u]+1) if (k*w[u]<q if feasible else k*w[u]>q)]
            lo[u],hi[u]=(keep[0],keep[-1]) if keep else (1,0)
        after=sum(max(0,h-l+1) for l,h in zip(lo,hi))
        assert 4*after<=3*M
        counts['queries']+=1
    assert B==opt and actual[witness]==B
    centers=threshold(d,w,B)
    assert centers==[x for x,r in enumerate(actual) if r==opt]
    vals=sorted({k*z for z in w for k in range(n)})
    for R in [F(-1)]+vals+[(a+b)/2 for a,b in zip(vals,vals[1:])]+[vals[-1]+1]:
        assert threshold(d,w,R)==[x for x,r in enumerate(actual) if r<=R]
        counts['complete_threshold_vectors']+=1
    counts['profiles']+=1
    return {'optimum':str(B),'centers':centers,'radii':list(map(str,actual))}

def run():
    start=datetime.now(timezone.utc).isoformat();tick=time.monotonic();counts=Counter();digest=hashlib.sha256();rng=random.Random(11820261115)
    metrics=[]
    for dims in [(1,),(2,),(3,),(4,),(2,2),(2,3),(2,2,2),(2,2,2,2),(3,3)]:
        pts=list(product(*(range(t) for t in dims)))
        d=[[sum(abs(a-b) for a,b in zip(x,y)) for y in pts] for x in pts]
        metrics.append((str(dims),d))
    metrics.append(('nonmedian-triangle',[[0,1,1],[1,0,1],[1,1,0]]))
    boundaries={}
    for name,d in metrics:
        n=len(d)
        profiles=list(product([F(0),F(2,7),F(5)],repeat=n)) if n<=4 else [[F(rng.randrange(8),rng.randrange(1,10)) for _ in range(n)] for _ in range(24)]
        profiles.extend([[F(0)]*n,[F(1)]*n,[F(0)]*(n-1)+[F(1,2**257+1)],[F(2**521+3,5) if i%2 else F(1,2**509+9) for i in range(n)]])
        for w in profiles:
            out=solve(d,w,counts);digest.update(json.dumps([name,list(map(str,w)),out],sort_keys=True).encode())
        counts['metric_families']+=1
    for w in [(1,0,1),(1,0,2),(0,0,7)]:
        boundaries[str(w)]=solve([[0,1,2],[1,0,1],[2,1,0]],list(map(F,w)),counts)
    # Exhaust every eligible weighted median and both outcomes on arbitrary rows.
    cat=[()] + [r for L in range(1,6) for r in combinations_with_replacement((0,1,4),L)]
    for rows in product(cat,repeat=2):
        M=sum(map(len,rows))
        if not M:continue
        mids=[(r[(len(r)-1)//2],len(r)) for r in rows if r]
        for q in set(a for a,L in mids):
            if 2*sum(L for a,L in mids if a<=q)>=M and 2*sum(L for a,L in mids if a>=q)>=M:
                assert 4*sum(sum(x<q for x in r) for r in rows)<=3*M
                assert 4*sum(sum(x>q for x in r) for r in rows)<=3*M
                counts['abstract_pivot_two_outcome_checks']+=2
    # Integer-only child-volume and maximum-child checks for every s in a bounded range.
    for s in range(3,4097):
        L=(s-1).bit_length();f=2*L;minor=(s-1)//f
        assert 2*L*minor<=s
        for child in (minor, s-(s+f-1)//f):
            assert child*f<=s*(f-1)
        counts['integer_recursion_parameter_checks']+=1
    N=10**12;ell=30;t=17_000_000_000;q=1<<ell;z=N-q-ell*t;minor=q//2+t;union=q-1+ell*t
    tay=sum((F(7)**j)/__import__('math').factorial(j) for j in range(12))
    assert tay>1000 and z==488926258176 and 56*minor<N and 2*union>N
    witness={'N':N,'cube_dimension':ell,'leaves_at_unit_vertices':t,'leaves_at_zero':z,'minority':minor,'56_times_minority':56*minor,'minority_union':union,'duplicated_volume':2*union,'Taylor_0_to_11_e7_lower_bound':str(tay),'new_integer_f':2*(N-1).bit_length()}
    # Meaningful bounded reuse after complete inspection: no main(), no file writes.
    p=SUPPLIED/'reviews/oracle01/controls.py'
    spec=importlib.util.spec_from_file_location('deposited_oracle_controls',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    core=8;edges=[(u,u^(1<<j)) for u in range(core) for j in range(3) if u<u^(1<<j)]
    for v in range(8,88):edges.append((0,v))
    for i,base in enumerate((1,2,4)):
        for v in range(88+2*i,90+2*i):edges.append((base,v))
    adj=m.graph_from_edges(94,edges)
    profiles=[[0]*94,[0]*94,[0]*94,[(37*i)%94 for i in range(94)]]
    profiles[1][7]=93;profiles[2][0]=93
    for w in profiles:m.morse(adj,w)
    reused={'source_path':str(p),'SHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'new_graph_n':94,'profiles':len(profiles),'statistics':dict(m.STATS),'did_not_call_main_or_full_campaign':True}
    assert m.STATS['unbalanced_calls'] and m.STATS['max_wide_ladder']==3 and m.STATS['dominance_calls']
    return {'status':'PASS','UTC_started':start,'UTC_completed':datetime.now(timezone.utc).isoformat(),'seconds':time.monotonic()-tick,'statistics':dict(counts),'case_digest_SHA256':digest.hexdigest(),'explicit_boundaries':boundaries,'succinct_volume_witness':witness,'bounded_deposited_function_reuse':reused,'limitations':['Exact finite falsifiers supplement the proofs; they do not prove a universal or asymptotic theorem.','No fast general median-graph oracle is implemented or benchmarked.','No giant succinct graph was allocated.']}

if __name__=='__main__': print(json.dumps(run(),indent=2,sort_keys=True))
