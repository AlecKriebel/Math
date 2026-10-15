#!/usr/bin/env python3
"""Independent exact finite checks. They do not establish the infinite theorem."""
import hashlib, itertools, json, pathlib, sys
from fractions import Fraction
from datetime import datetime, timezone
sys.dont_write_bytecode = True
OUT = pathlib.Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1047_30004909/root_reproduction')
def require(condition, message):
    if not condition:
        raise RuntimeError(message)
def emit(obj):
    print(json.dumps(obj, sort_keys=True), flush=True)
def card(mask):
    return mask.bit_count()
def exact_basis_exchange(bases):
    pool = set(bases)
    for left in bases:
        for right in bases:
            for e in range(max(1, (left | right).bit_length())):
                eb = 1 << e
                if (left & ~right) & eb:
                    if not any(((left & ~eb) | (1 << j)) in pool for j in range(right.bit_length()) if (right & ~left) & (1 << j)):
                        return False
    return True

def rank_from_bases(n, bases):
    return tuple(max(card(s & b) for b in bases) for s in range(1 << n))

def validate_rank_axioms(n, ranks):
    require(ranks[0] == 0, 'rank(empty) failure')
    for s in range(1 << n):
        require(isinstance(ranks[s], int) and 0 <= ranks[s] <= card(s), 'rank bounds failure')
        for t in range(1 << n):
            require((s & ~t) != 0 or ranks[s] <= ranks[t], 'rank monotonicity failure')
            require(ranks[s]+ranks[t] >= ranks[s|t]+ranks[s&t], 'rank submodularity failure')

def exhaustive_matroids(n):
    seen = set()
    counts = {}
    candidates = 0
    for R in range(n+1):
        possible_bases = tuple(sum(1 << e for e in c) for c in itertools.combinations(range(n), R))
        accepted = 0
        for family_mask in range(1, 1 << len(possible_bases)):
            candidates += 1
            bases = tuple(b for j,b in enumerate(possible_bases) if family_mask & (1 << j))
            if not exact_basis_exchange(bases):
                continue
            ranks = rank_from_bases(n, bases)
            validate_rank_axioms(n, ranks)
            require(ranks[-1] == R, 'basis rank mismatch')
            require(ranks not in seen, 'duplicate bases-to-ranks representation')
            seen.add(ranks)
            accepted += 1
            yield R, ranks
        counts[R] = accepted
    emit({'type':'enumeration_receipt','n':n,'basis_family_candidates':candidates,'matroids_by_rank':counts,'distinct_rank_functions':len(seen)})

def sqrt_factor_squared(n, ranks):
    if any(ranks[1 << i] == 0 for i in range(n)):
        return None
    return max(max(Fraction(ranks[s]**2,card(s)),Fraction(card(s),ranks[s]**2)) for s in range(1,1 << n))

def rational_values(n,m):
    return tuple(Fraction(0) if s==0 else Fraction(m+card(s)-1,m) for s in range(1 << n))

def rational_factor(n, ranks, values):
    if any(ranks[1 << i] == 0 for i in range(n)):
        return None
    return max(max(Fraction(ranks[s])/values[s],values[s]/ranks[s]) for s in range(1,1 << n))

def fraction_json(v):
    return {'numerator':v.numerator,'denominator':v.denominator}

require(OUT.is_dir(), 'missing scoped output directory')
started=datetime.now(timezone.utc).isoformat()
emit({'type':'start','utc':started,'method':'enumerate every nonempty equal-size basis family and enforce basis exchange; independently validate integer rank axioms; exact Fraction comparisons','no_original_replay':True,'finite_scope':{'all_matroids_n':'1..5','uniform_sqrt_n':'1..200','uniform_rational_m':'1..30'}})
results=[]
for n in range(1,6):
    best={}
    matroid_count=0
    loopless_count=0
    rational_best={}
    m = {1:1,4:2}.get(n)
    values = rational_values(n,m) if m else None
    for R,ranks in exhaustive_matroids(n):
        matroid_count += 1
        factor=sqrt_factor_squared(n,ranks)
        if factor is None:
            continue
        loopless_count+=1
        envelope=max(Fraction(R),Fraction(n,R*R))
        require(factor>=envelope, 'all-matroid sqrt envelope violated')
        require(factor**3>=n, 'sqrt sixth-root obstruction violated')
        best[R]=min(best.get(R,factor),factor)
        if m:
            rational=rational_factor(n,ranks,values)
            rat_envelope=max(Fraction(m*R,m+R-1),Fraction(m*m+m-1,m*R))
            require(rational>=rat_envelope, 'all-matroid rational envelope violated')
            require(rational*rational+rational>=m, 'rational quadratic obstruction violated')
            require(2*rational*rational>=m, 'rational weakened obstruction violated')
            rational_best[R]=min(rational_best.get(R,rational),rational)
    for R in range(1,n+1):
        require(best[R] == max(Fraction(R),Fraction(n,R*R)), 'integer-rank sqrt optimum mismatch')
        if m:
            require(rational_best[R] == max(Fraction(m*R,m+R-1),Fraction(m*m+m-1,m*R)), 'integer-rank rational optimum mismatch')
    row={'n':n,'matroids':matroid_count,'loopless_matroids':loopless_count,'sqrt_best_factor_squared_by_rank':{R:fraction_json(v) for R,v in best.items()}}
    if m:
        row['rational_m']=m
        row['rational_best_factor_by_rank']={R:fraction_json(v) for R,v in rational_best.items()}
    results.append(row)
    emit({'type':'exhaustive_result',**row})

sqrt_count=0
for n in range(1,201):
    for R in range(1,n+1):
        actual=max(max(Fraction(min(k,R)**2,k),Fraction(k,min(k,R)**2)) for k in range(1,n+1))
        expected=max(Fraction(R),Fraction(n,R*R))
        require(actual==expected, 'uniform sqrt cardinality envelope mismatch')
        require(actual**3>=n, 'uniform sqrt sixth root bound mismatch')
        sqrt_count+=1
# A separate exact cube sweep, without enumerating subsets or irrational roots.
for m in range(1,101):
    n=m**3
    actual=max(Fraction(m),Fraction(n,m*m))
    require(actual==m and actual**3==n, 'cube sharpness failure')
emit({'type':'uniform_sqrt_sweep','rank_size_pairs':sqrt_count,'n_min':1,'n_max':200,'cube_m_min':1,'cube_m_max':100,'status':'PASS'})

# Direct radical-free checks of sqrt set-pair submodularity. For set pairs,
# a+c=i+u, so comparing the squared sums reduces exactly to ac>=iu.
sqrt_submodular_pairs=0
for n in range(0,9):
    for s in range(1<<n):
        for t in range(1<<n):
            a,c,i,u=card(s),card(t),card(s&t),card(s|t)
            require(a+c==i+u and a*c>=i*u, 'sqrt direct pair submodularity failure')
            sqrt_submodular_pairs+=1
emit({'type':'sqrt_direct_submodular_pairs','set_pairs':sqrt_submodular_pairs,'n_min':0,'n_max':8,'comparison':'nonnegative radical sums squared; equal total cardinality and product inequality','status':'PASS'})

rational_count=0
for m in range(1,31):
    n=m*m
    # For cardinality functions the increment test entails all set-pair inequalities;
    # verify it with exact values, including the boundary k=0.
    h=[Fraction(0)]+[Fraction(m+k-1,m) for k in range(1,n+1)]
    deltas=[h[k+1]-h[k] for k in range(n)]
    require(h[1]==1 and all(d>=0 for d in deltas), 'rational normalization/monotonicity failure')
    require(all(deltas[k]>=deltas[k+1] for k in range(n-1)), 'rational diminishing increments failure')
    for R in range(1,n+1):
        actual=max(max(Fraction(min(k,R))/h[k],h[k]/min(k,R)) for k in range(1,n+1))
        expected=max(Fraction(m*R,m+R-1),Fraction(m*m+m-1,m*R))
        require(actual==expected, 'uniform rational cardinality envelope mismatch')
        require(actual*actual+actual>=m and 2*actual*actual>=m, 'rational lower bounds failure')
        rational_count+=1
# Direct all-pair rational set-function inequality checks for m=1,2,3.
submodular_pairs=0
for m in range(1,4):
    n=m*m
    h=rational_values(n,m)
    for s in range(1<<n):
        for t in range(1<<n):
            require(h[s]+h[t]>=h[s|t]+h[s&t], 'rational direct pair submodularity failure')
            submodular_pairs+=1
emit({'type':'uniform_rational_sweep','rank_size_pairs':rational_count,'m_min':1,'m_max':30,'direct_submodular_set_pairs':submodular_pairs,'status':'PASS'})

# Fault-sensitive semantic controls: these alter actual mathematical premises,
# rather than making line-by-line copies of the submitted algebra.
controls=[]
# Without the lower comparison, the free matroid uniformly dominates sqrt.
require(all(k<=k*k for k in range(1,18)), 'upper-only free matroid control')
controls.append({'mutation':'delete lower comparison','witness':'free matroid on n=17, alpha=1; sqrt(k)<=k for all k','universal_obstruction_survives':False})
# Without the upper comparison, a rank-one uniform matroid works at alpha one.
require(all(1<=k for k in range(1,18)), 'lower-only rank-one control')
controls.append({'mutation':'delete upper comparison','witness':'U_(1,17), alpha=1; 1<=sqrt(k) for all nonempty sets','universal_obstruction_survives':False})
# A scaled rank is outside the target class and can beat the ordinary sixth-root bound.
# n=16,R=4,c=1/sqrt(2),alpha=sqrt(2), while ordinary lower n^(1/6)>sqrt(2).
# Squared ratios are r^2/(2k),2k/r^2, and must be <=2.
require(all(Fraction(min(k,4)**2,2*k)<=2 and Fraction(2*k,min(k,4)**2)<=2 for k in range(1,17)), 'scaled-rank modified-model control')
require(2**3<16, 'scaled alpha violates ordinary sixth-root bound')
controls.append({'mutation':'allow positive scaling of rank','witness':'n=16, scaled U_(4,16) by 1/sqrt(2), alpha=sqrt(2); alpha^6=8<16','ordinary_sixth_root_bound_survives':False,'note':'a finite scope-sensitivity control only; no modified universal theorem claimed'})
# Nonuniform ordinary rank refutes a hidden uniformity shortcut.
parallel_rank=rank_from_bases(3,(0b101,0b110))
validate_rank_axioms(3,parallel_rank)
require(parallel_rank[0b011]==1 and min(2,card(0b011))==2, 'nonuniform counterexample failed')
controls.append({'mutation':'infer r(S)=min(|S|,R) for every matroid','witness':'rank-two n=3 bases {1,3},{2,3}; r({1,2})=1 but uniform rank=2','inference_valid':False})
# An additive constant is forbidden by empty normalization and singleton values.
controls.append({'mutation':'drop singleton normalization','witness':'f identically zero and rank-zero matroid satisfy both inequalities for every alpha>0','normalization_role':'necessary to force nonloops/alpha>=1 in the present proofs'})
for control in controls:
    emit({'type':'semantic_control',**control})
completed=datetime.now(timezone.utc).isoformat()
summary={'status':'PASS','started_utc':started,'completed_utc':completed,'exact_arithmetic':'integer/Fraction; square-root factors checked by exact squares','exhaustive_results':results,'uniform_sqrt_rank_size_pairs':sqrt_count,'uniform_rational_rank_size_pairs':rational_count,'direct_rational_submodular_set_pairs':submodular_pairs,'direct_sqrt_submodular_set_pairs':sqrt_submodular_pairs,'semantic_controls':controls,'finite_evidence_only':True,'no_original_executable_or_replay':True,'checker_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
(OUT/'CHECKER_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
emit({'type':'completed','utc':completed,'status':'PASS','finite_evidence_only':True})
