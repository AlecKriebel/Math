#!/usr/bin/env python3
"""New source/certificate adversarial controls. Standard library only.

Analytic claims are in CERTIFICATE_DERIVATION.md. Counts below are finite
regression/falsification controls, not universal proof. No submitted file changes.
"""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from itertools import permutations, product
from collections import Counter
from math import factorial
import datetime, hashlib, importlib.util, json, os, subprocess, sys, time

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
SRC=HERE.parent/'submitted/unsolved_math_prioritization/attempts/9700040'
spec=importlib.util.spec_from_file_location('audit_target',SRC/'stationary_law.py')
target=importlib.util.module_from_spec(spec);spec.loader.exec_module(target)
C=Counter(); rows=[]

def ck(ok,category):
    assert ok,category
    C[category]+=1

def terms(x,N): return [x**n/factorial(n) for n in range(N+1)]
def independent_tail(x,N):
    if N<0 or N+2<=x:raise ValueError('invalid cutoff')
    return x**(N+1)/factorial(N+1)*(N+2)/(N+2-x)
def limits(x,N,W):
    T=sum(terms(x,N));R=independent_tail(x,N)
    return W/(T+R),(W+R)/(T+R),R/(T+R)
def choose(x,eps):
    if x<=0 or eps<=0:raise ValueError('positive rational x and tolerance required')
    N=max(0,x.numerator//x.denominator-1)
    while N+2<=x or limits(x,N,Q(0))[2]>eps:N+=1
    return N

# Extremize both unknown tails on a dense exact grid, including all boundaries.
for T,R in product((Q(1),Q(2,7),Q(31)),(Q(1,1000),Q(8,3),Q(89))):
    for wi,ei,fi in product(range(9),repeat=3):
        W=T*wi/8;E=R*ei/8;F=E*fi/8;P=(W+F)/(T+E)
        lo=W/(T+R);hi=(W+R)/(T+R)
        ck(lo<=P<=hi,'unknown_tail_information_class')
        ck(0<=lo<=hi<=1,'universal_interval_probability_range')
    ck((T*Q(3,8))/(T+R)==(T*Q(3,8)+0)/(T+R),'lower_extremum_attained_at_E_R_F_0')
    ck((T*Q(3,8)+R)/(T+R)==1-(T-T*Q(3,8))/(T+R),'upper_extremum_attained_at_E_R_F_R')

# Pointwise algebra and all-cutoff monotonicity, with x just below tail gates.
for x in sorted(set(Q(a,b) for a in range(1,40) for b in (1,2,5,7))):
    prev=None
    for N in range(65):
        if N+2<=x:continue
        aa=terms(x,N);T=sum(aa);R=independent_tail(x,N);k=N+2
        nextR=independent_tail(x,N+1);a=x**(N+1)/factorial(N+1)
        ck((T+R)-(T+a+nextR)==a*x*x/(k*(k-x)*(k+1-x)),'exact_enlarged_normalizer_decrease_identity')
        ck(nextR/R==x*(k+1)*(k-x)/(k*k*(k+1-x)),'exact_tail_ratio_identity')
        ck(nextR<R,'tail_bound_strictly_decreases')
        for mode in range(4):
            # Four infinite, predetermined admissible w_n sequences.
            w=lambda n: Q(n%2) if mode==0 else Q(1,n+1) if mode==1 else Q(int(n<=3)) if mode==2 else Q(1)
            W=sum((q*w(n) for n,q in enumerate(aa)),Q(0))
            lo,hi,width=limits(x,N,W)
            ck(hi-lo==width,'exact_interval_width')
            if prev is not None:
                old=prev[mode];ck(old[0]<=lo<=hi<=old[1],'nested_endpoints_for_admissible_sequence')
        prev=[limits(x,N,sum((q*(Q(n%2) if mode==0 else Q(1,n+1) if mode==1 else Q(int(n<=3)) if mode==2 else Q(1)) for n,q in enumerate(aa)),Q(0))) for mode in range(4)]
        partial=sum((x**n/factorial(n) for n in range(N+1,N+21)),Q(0))
        ck(partial<R,'twenty_omitted_terms_below_geometric_tail')

cutoffs=[]
for x,eps in product((Q(1,100),Q(1),Q(7,3),Q(19,2),Q(101,2)),(Q(1,10),Q(1,10**12),Q(1,10**40))):
    N=choose(x,eps);width=limits(x,N,Q(0))[2]
    ck(N+2>x and width<=eps,'effective_cutoff_terminates_on_rational_grid')
    if N and N+1>x:ck(limits(x,N-1,Q(0))[2]>eps,'selected_cutoff_is_first_admissible')
    cutoffs.append({'x':str(x),'tolerance':str(eps),'N':N,'width':str(width)})

# Direct LIS dynamic program; no tableau/determinant or patience identity.
def lis(sequence):
    d=[]
    for j,a in enumerate(sequence):d.append(1+max((d[i] for i in range(j) if sequence[i]<a),default=0))
    return max(d,default=0)
def compositions(n,m):
    if m==1:yield (n,);return
    for a in range(n+1):
        for tail in compositions(n-a,m-1):yield (a,)+tail
@lru_cache(None)
def permutation_prefix_histogram(n):
    hist=Counter()
    for p in permutations(range(n)):
        hist[tuple(lis(p[:j]) for j in range(n+1))]+=1
    return hist
def direct_coefficients(xs,rs,N):
    ds=tuple(x-y for x,y in zip(xs,(Q(0),)+xs[:-1]));out=[]
    for n in range(N+1):
        value=Q(0)
        for alloc in compositions(n,len(xs)):
            ends=[];s=0
            for d in alloc:s+=d;ends.append(s)
            count=sum(c for ll,c in permutation_prefix_histogram(n).items() if all(ll[t]<r for t,r in zip(ends,rs)))
            factor=Q(count,factorial(n))
            for d,delta in zip(alloc,ds):factor*=delta**d/factorial(d)
            value+=factor
        out.append(value)
    return out

queries=[((Q(1,4),Q(5,6),Q(7,3)),rs) for rs in ((2,3,4),(4,2,3),(3,1,4),(1,4,2),(2,2,2),(4,3,2))]
queries += [((Q(1,3),Q(5,3)),rs) for rs in ((1,2),(3,2),(2,4),(8,8))]
coefficients=[]
for xs,rs in queries:
    expected=direct_coefficients(xs,rs,6);got=target.raw_by_size(xs,rs,6)
    for n,(a,b) in enumerate(zip(expected,got)):ck(a==b,'author_coefficients_vs_direct_permutation_LIS')
    coefficients.append({'x':list(map(str,xs)),'indices':rs,'N':6,'independent_coefficients':list(map(str,expected)),'all_match':got==expected})
    for n,w in enumerate(got):ck(0<=w<=xs[-1]**n/factorial(n),'direct_coefficients_below_unconstrained_mass')

# Consistency under inserting an unused intermediate threshold, and recovery
# of complete joint CDF coefficients on a common final Poisson rectangle.
xs=(Q(1,4),Q(5,6),Q(7,3));rs=(2,3,2);N=6
base=target.raw_by_size((xs[0],xs[2]),(rs[0],rs[2]),N)
with_unused=target.raw_by_size(xs,(rs[0],N+1,rs[2]),N)
for a,b in zip(base,with_unused):ck(a==b,'unused_intermediate_threshold_marginalizes_consistently')
ie=[Q(0)]*(N+1)
for bits in product((0,1),repeat=3):
    selected=[j for j,b in enumerate(bits) if b]
    qx=tuple(xs[j] for j in selected);qr=tuple(rs[j] for j in selected)
    if not selected or selected[-1]!=2:qx+=(xs[-1],);qr+=(N+1,)
    raw=target.raw_by_size(qx,qr,N)
    for n,w in enumerate(raw):ie[n]+=(-1)**len(selected)*w
direct_cdf=[]
for n in range(N+1):
    value=Q(0)
    for alloc in compositions(n,3):
        ends=[];s=0
        for d in alloc:s+=d;ends.append(s)
        count=sum(c for ll,c in permutation_prefix_histogram(n).items() if all(ll[t]>=r for t,r in zip(ends,rs)))
        factor=Q(count,factorial(n))
        for d,delta in zip(alloc,(xs[0],xs[1]-xs[0],xs[2]-xs[1])):factor*=delta**d/factorial(d)
        value+=factor
    direct_cdf.append(value)
    ck(ie[n]==value,'joint_CDF_inclusion_exclusion_vs_direct_LIS_count')
cdf_receipt={'x':list(map(str,xs)),'indices':rs,'N':N,'inclusion_exclusion_coefficients':list(map(str,ie)),
             'direct_coefficients':list(map(str,direct_cdf)),'unused_intermediate_threshold_matches':base==with_unused}

# Query canonicalization with repeated/nonpositive thresholds and arbitrary order.
def normalize(xs,rs):
    if len(xs)!=len(rs) or any(type(r) is not int or r<=0 for r in rs):raise ValueError('invalid query')
    q={}
    for x,r in zip(map(Q,xs),rs):
        if x>0:q[x]=min(r,q.get(x,r))
    ss=tuple(sorted(q));return ss,tuple(q[x] for x in ss)
base_x=(Q(0),Q(-1),Q(1,2),Q(1,2),Q(2));base_r=(7,1,4,2,3)
canonical=normalize(base_x,base_r)
ck(canonical==((Q(1,2),Q(2)),(2,3)),'repeated_threshold_minimum_index')
for p in permutations(range(5)):
    ck(normalize(tuple(base_x[j] for j in p),tuple(base_r[j] for j in p))==canonical,'query_order_invariance_after_normalization')
ck(normalize((Q(0),Q(-3)),(1,2))==((),()),'all_nonpositive_queries_reduce_to_probability_one')

# Exact determinant dimension and direct skew-tableau Young-lattice path counts.
@lru_cache(None)
def independent_parts(n,cap=10**6):
    if n==0:return ((),)
    return tuple((a,)+p for a in range(1,min(n,cap)+1) for p in independent_parts(n-a,a))
def contained(lam,mu):return all((lam[i] if i<len(lam) else 0)>=m for i,m in enumerate(mu))
@lru_cache(None)
def paths(lam,mu):
    if not contained(lam,mu):return 0
    if lam==mu:return 1
    ans=0
    for j in range(len(mu)+1):
        q=list(mu)+( [0] if j==len(mu) else [] )
        if j and q[j]>=q[j-1]:continue
        q[j]+=1
        q=tuple(q)
        if contained(lam,q):ans+=paths(lam,q)
    return ans
shapes=[p for n in range(7) for p in independent_parts(n)]
for lam in shapes:
    for mu in shapes:
        if not contained(lam,mu):continue
        d=sum(lam)-sum(mu)
        for t in (Q(0),Q(3,7),Q(2)):
            expected=Q(paths(lam,mu),factorial(d))*t**d
            for dim in (None,max(len(lam),len(mu))+1):
                ck(target.D(lam,mu,t,dim)==expected,'determinants_vs_forward_Young_lattice_count')
            ck(target.D(target.transpose(lam),target.transpose(mu),t)==expected,'transpose_vs_forward_Young_lattice_count')

# Input and presentation controls preserve observed exception details.
invalid=[('empty',(),(),0),('mismatch',(Q(1),),(1,2),2),('zero',(Q(0),),(1,),2),
         ('negative',(Q(-1),),(1,),2),('repeated',(Q(1),Q(1)),(2,3),2),
         ('descending',(Q(2),Q(1)),(2,3),2),('index_zero',(Q(1),),(0,),2),
         ('index_float',(Q(1),),(1.0,),2),('cutoff_negative',(Q(1,2),),(1,),-1),
         ('tail_equality',(Q(2),),(1,),0),('tail_below_gate',(Q(3),),(1,),0)]
bad=[]
for name,xs,rs,N in invalid:
    try:target.enclosure(xs,rs,N)
    except Exception as e:bad.append({'case':name,'exception':type(e).__name__,'message':str(e)});ck(True,'documented_domain_invalid_input_rejected')
    else:raise AssertionError(name)
accepted_bool=target.enclosure((Q(1),),(True,),1)
ck(accepted_bool==target.enclosure((Q(1),),(1,),1),'python_bool_is_accepted_as_integer_index')

display=[]
for N in (18,200):
    cert=target.enclosure((Q(1),),(1,),N)
    lo,hi=cert['lower'],cert['upper'];fl,fu,fw=map(float,(lo,hi,cert['width']))
    display.append({'x':'1','index':1,'N':N,'exact_width_positive':cert['width']>0,
        'exact_width':str(cert['width']),'display_lower':fl,'display_upper':fu,'display_width':fw,
        'lower_float_is_above_exact_lower':Q.from_float(fl)>lo,
        'upper_float_is_below_exact_upper':Q.from_float(fu)<hi,
        'display_endpoints_equal':fl==fu})
ck(display[-1]['display_width']==0 and display[-1]['exact_width_positive'],'binary64_width_underflow_is_display_only')

# Three actual local Python/CLI limit reproductions, in separate fresh processes.
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
limit_code={
 'recursion':"import stationary_law as s; s.partitions(1000,max_part=1,max_length=1000)",
 'fraction_string_digit_limit':"from fractions import Fraction; print(str(Fraction(10**5000+1,3)))",
 'evaluator_cli_digit_limit':None}
resource=[]
for name,code in limit_code.items():
    if code is None:cmd=[sys.executable,str(SRC/'stationary_law.py'),'--x','1','--indices','1','--cutoff','1600']
    else:cmd=[sys.executable,'-c',code]
    runenv={**env,'PYTHONPATH':str(SRC)}
    run=subprocess.run(cmd,cwd=HERE,env=runenv,capture_output=True,text=True,timeout=30)
    resource.append({'case':name,'returncode':run.returncode,'stderr':run.stderr,'stdout':run.stdout,
                     'stdout_sha256':hashlib.sha256(run.stdout.encode()).hexdigest()})
    ck(run.returncode!=0,'local_runtime_limit_reproduced')

receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
         'python_version':sys.version,'python_recursionlimit':sys.getrecursionlimit(),
         'python_integer_string_digit_limit':sys.get_int_max_str_digits(),
         'exact_assertions':sum(C.values()),'categories':dict(C),'effective_cutoffs':cutoffs,
         'coefficient_controls':coefficients,'full_joint_CDF_and_consistency_control':cdf_receipt,'invalid_query_results':bad,
         'display_controls':display,'resource_limit_controls':resource,
         'observed_cache_sizes':{'D':target.D.cache_info()._asdict(),'partitions':target.partitions.cache_info()._asdict()},
         'scope':'Finite exact controls plus actual runtime limits. Universal certificate proof, source scope, and applicability are in the authored derivations/report.'}
    # Full exact receipt, not just a success count.
(HERE/'CONTROL_RECEIPTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','exact_assertions':receipt['exact_assertions'],'categories':dict(C),
                  'resource_limits_reproduced':len(resource),'receipt':'CONTROL_RECEIPTS.json'},indent=2))
