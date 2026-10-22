#!/usr/bin/env python3
"""Independent oracles and analytic-bound controls for the repaired implementation."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,hashlib,json,random
root=Path(__file__).parent
spec=importlib.util.spec_from_file_location('submitted_algorithm',root/'author_replay/algorithm.py')
alg=importlib.util.module_from_spec(spec);spec.loader.exec_module(alg)
counts={}
def ck(name,ok):
    assert ok,name
    counts[name]=counts.get(name,0)+1

# Independent interval oracle: enumerate geometric endpoint pairs and count input
# values directly. It knows nothing about convolution or run masks.
def interval_oracle(a):
    best=[None]*len(a)
    for lo in set(a):
        for hi in set(a):
            if lo>hi:continue
            positions=[j for j,x in enumerate(a) if lo<=x<=hi]
            k=len(positions)
            candidate=(hi-lo,positions[0],positions[-1])
            if best[k-1] is None or candidate<best[k-1]:best[k-1]=candidate
    return best
interval_runs=0
for runs in range(1,5):
    for multiplicities in product(range(1,4),repeat=runs):
        for spacing in (0,1):
            values=[F(2*j*j+3*j,7) if spacing else F(j) for j in range(runs)]
            a=[v for v,m in zip(values,multiplicities) for _ in range(m)]
            a=[F(10**35)+F(3,11)*x for x in a]
            expected=interval_oracle(a)
            for d in (None,2,4,7):
                got=alg.shortest_exact_intervals(a,d);interval_runs+=1
                ck('interval_oracle',got==expected)
                for k,item in enumerate(got,1):
                    if item is not None:
                        width,j,i=item
                        ck('actual_interval_count',sum(a[j]<=x<=a[i] for x in a)==k)
                        ck('endpoint_width',width==a[i]-a[j])
            # Multiplicity-run sums characterize feasibility independently.
            feasible=set()
            for l in range(runs):
                for r in range(l,runs):feasible.add(sum(multiplicities[l:r+1]))
            ck('feasible_count_set',{k for k,x in enumerate(expected,1) if x is not None}==feasible)

rng=random.Random(9153800014);convolution_runs=0
for N in range(1,18):
    fixtures=[([F(0)]*N,[F(0)]*N),
              ([F(i%3-1) for i in range(N)],[F(1-i%3) for i in range(N)]),
              ([F(rng.randrange(-8,9),rng.randrange(1,5)) for _ in range(N)],
               [F(rng.randrange(-8,9),rng.randrange(1,5)) for _ in range(N)])]
    for A,B in fixtures:
        bound=max(map(abs,A+B))+1
        expected=[min((A[i]+B[h-i],i) for i in range(h+1)) for h in range(N)]
        for d in (1,2,5,N+1):
            got=alg.minplus_prefix(A,B,bound,d);convolution_runs+=1
            ck('prefix_value_and_witness',got==expected)
        # Independently check equations(4)-(5), padded blocks and exact report count.
        if N<=8:
            for d in (1,2,3,5):
                S=10*bound
                av=lambda i:A[i] if 0<=i<N else S
                bv=lambda i:B[i] if 0<=i<N else S
                reports=0
                for r in range(0,N,d):
                    for shift in range(-N+1,N):
                        costs=[(av(r+t)+bv(shift-t),t) for t in range(d)]
                        winners=[]
                        for delta in range(d):
                            dominates=all((av(r+delta)-av(r+t),delta-t)<=(bv(shift-t)-bv(shift-delta),0) for t in range(d))
                            ck('lex_dominance_equivalence',dominates==(costs[delta]==min(costs)))
                            if dominates:winners.append(delta)
                        ck('one_report_per_block_shift',winners==[min(costs)[1]])
                        reports+=len(winners)
                ck('total_report_count',reports==((N+d-1)//d)*(2*N-1))
                ck('padding_gap',S-bound>2*bound)

# Inclusive ties crossing the median, as well as zero-dimensional and monochrome
# cases. All labels are unique, so repeated reporting cannot be hidden by a set.
dominance_runs=0
for dimension in range(7):
    for nr,nb in [(0,0),(0,19),(19,0),(1,1),(8,9),(9,8),(17,18)]:
        for fixture in range(3):
            pts=[]
            for label in range(nr+nb):
                color=int(label>=nr)
                coords=tuple((F(0),0) if fixture==0 else
                             (F((label+3*j)%4), (label+j)%2) if fixture==1 else
                             (F(rng.randrange(-4,5),3),rng.randrange(-2,3))
                             for j in range(dimension))
                pts.append((coords,color,label))
            rng.shuffle(pts)
            oracle={(r[2],b[2]) for r in pts for b in pts if r[1]==0 and b[1]==1 and
                    all(r[0][j]<=b[0][j] for j in range(dimension))}
            got=alg.dominance_pairs(pts,dimension);dominance_runs+=1
            ck('dominance_exact_set',set(got)==oracle)
            ck('dominance_no_duplicate_report',len(got)==len(oracle))

# Exact arithmetic certificates used by the analytic complexity proof.
ck('recurrence_contraction',17**5<32*15**4)
for size in range(17,1001):
    ck('rounded_half_bound',F((size+1)//2,size)<=F(17,32))
for exponent in range(1,257):
    for N in (2**exponent-1,2**exponent,2**exponent+1):
        d=max(1,(N.bit_length()-1)//16)
        ck('dimension_growth',16**(4*d)<=16**4*N)
        ck('lower_order_term_absorption',d**4<=N and d**3<=N)
for R in (F(0),F(1,10**30),F(7,3),F(10**60)):
    M=3*R+1
    ck('masked_sentinel_gap',M-R>R and M>0)
# Shared-list reporting avoids recursive per-output forwarding. This is a
# source-level control, not a runtime benchmark.
code=(root/'author_replay/algorithm.py').read_text()
ck('direct_leaf_reporting','yield from' not in code and 'output.append((r[2], b[2]))' in code)
out={'problem_id':3800014,'status':'PASS_INDEPENDENT_CORRECTNESS_AND_BOUND_CONTROLS',
     'assertions':sum(counts.values()),'groups':counts,'interval_runs':interval_runs,
     'convolution_runs':convolution_runs,'dominance_runs':dominance_runs,
     'proof_sha256':hashlib.sha256((root/'author_replay/KNOWN_ALGORITHM.md').read_bytes()).hexdigest(),
     'algorithm_sha256':hashlib.sha256((root/'author_replay/algorithm.py').read_bytes()).hexdigest(),
     'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'limits':'Finite exact tests and analytic-bound certificates only; asymptotic complexity is established in REVIEW.md, not by timings. Exact real-RAM scope, not arbitrary-size bit-time or a polynomial exponent saving.'}
print(json.dumps(out,indent=2,sort_keys=True))
