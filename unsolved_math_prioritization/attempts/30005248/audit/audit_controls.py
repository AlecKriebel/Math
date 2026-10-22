#!/usr/bin/env python3
"""Portable, standard-library audit controls. Never writes the input bundle.

Usage: python audit_controls.py --bundle ../public --output audit_controls.json
The source PDFs are deliberately not needed or included. These finite controls
support the accompanying proof audit; they do not prove asymptotic theorems.
"""
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, ceil
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, subprocess, sys, tempfile

COUNTS = Counter()
NEGATIVE_CONTROLS = []

def require(name, condition):
    if not condition:
        raise AssertionError(name)
    COUNTS[name] += 1

def reject(name, false_condition):
    require('negative_controls_reject', not false_condition)
    NEGATIVE_CONTROLS.append(name)

def compositions(n, s):
    if s == 1:
        yield (n,)
    else:
        for k in range(n+1):
            for tail in compositions(n-k, s-1):
                yield (k,) + tail

def multinomial_mass(counts, ps):
    c = factorial(sum(counts))
    for k in counts:
        c //= factorial(k)
    return c * prod(p**k for p, k in zip(ps, counts))

def prod(xs):
    ans = F(1)
    for x in xs:
        ans *= x
    return ans

def bern(n, p):
    return [F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1)]

def endpoint_lrt(n, p, q):
    b0, b1 = bern(n,p), bern(n,q)
    bits = [int(y>x) for x,y in zip(b0,b1)]
    return (sum(x*bit for x,bit in zip(b0,bits)),
            sum(y*(1-bit) for y,bit in zip(b1,bits)), bits)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parent.parent/'public')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if args.output and (args.output.resolve() == args.bundle.resolve() or args.bundle.resolve() in args.output.resolve().parents):
        raise ValueError("The output must be outside the frozen input bundle")
    expected = json.loads(Path(__file__).with_name('FROZEN_INPUTS.json').read_text())
    before = {}
    for name, digest in expected['sha256'].items():
        before[name] = hashlib.sha256((args.bundle/name).read_bytes()).hexdigest()
        require('frozen_input_hashes', before[name] == digest)
    require('exact_allowlist', set(p.name for p in args.bundle.iterdir() if p.is_file()) == set(before))

    # Replay only in a temporary directory: the author script writes beside itself.
    with tempfile.TemporaryDirectory(prefix='functional-audit-') as tmp:
        p = Path(tmp)/'verify_exact.py'
        p.write_bytes((args.bundle/'verify_exact.py').read_bytes())
        result = subprocess.run([sys.executable,str(p)],check=True,capture_output=True,text=True,timeout=120)
        replay = json.loads(result.stdout)
        require('author_replay_exact_match', replay == json.loads((args.bundle/'verification.json').read_text()))
        require('author_replay_assertion_count', replay['total_assertions'] == 16459)

    # Direct probability-space calculation, not the author's likelihood-kernel sum.
    # Includes the untested a=1 zero-probability boundary and a=0 control.
    mutation_witness = None
    for s in (2,4,6):
        d=s//2
        signs=list(product((-1,1),repeat=d))
        for n in range(1,7):
            states=list(compositions(n,s))
            for a in (F(0),F(1,4),F(2,3),F(1)):
                laws=[]
                for z in signs:
                    ps=tuple(v for zz in z for v in ((1+a*zz)/s,(1-a*zz)/s))
                    require('mixture_component_normalization',sum(ps)==1 and min(ps)>=0)
                    laws.append([multinomial_mass(c,ps) for c in states])
                mix=[sum(xs)/len(signs) for xs in zip(*laws)]
                base=[multinomial_mass(c,[F(1,s)]*s) for c in states]
                require('direct_mixture_normalization',sum(mix)==sum(base)==1)
                chi=sum((x-y)**2/y for x,y in zip(mix,base))
                tv=sum(abs(x-y) for x,y in zip(mix,base))/2
                overlap=sum(F(comb(d,j),2**d)*(1+2*a*a*F(d-2*j,s))**n for j in range(d+1))-1
                require('direct_mixture_vs_overlap',chi==overlap)
                require('direct_mixture_tv_bound',4*tv**2<=chi)
                t=F(n*n,s)*a**4
                if t<1:
                    require('direct_mixture_geometric_bound',chi<=t/(1-t))
                if t<=F(1,16):
                    require('direct_mixture_small_signal',chi<=F(1,15))
                if s==2 and n==2 and a==F(1,4):
                    bad=sum(F(comb(d,j),2**d)*(1+a*a*F(d-2*j,s))**n for j in range(d+1))-1
                    mutation_witness=(chi,bad)
    reject('drop_factor_two_in_mixture_kernel', mutation_witness[0]==mutation_witness[1])

    # Poisson/count experiment identity after cancelling the common exp(-lambda).
    for ps in ((F(1,3),F(2,3)),(F(0),F(1,4),F(3,4))):
        for lam in (F(1,2),F(1),F(7,2)):
            for total in range(7):
                for counts in compositions(total,len(ps)):
                    independent=prod((lam*p)**k/factorial(k) for p,k in zip(ps,counts))
                    conditional=lam**total/factorial(total)*multinomial_mass(counts,ps)
                    require('poisson_multinomial_factorization',independent==conditional)

    # Generic independent random-size coupling, the algebra behind both transfers.
    # Finite rational N laws are sufficient to exercise the bounded-loss step;
    # exponential Poisson tail bounds are audited analytically in the report.
    for m in range(1,9):
        weights=[F(1,2**j) for j in range(2*m+2)]
        norm=sum(weights); weights=[x/norm for x in weights]
        for p in (F(0),F(1,8),F(1,2),F(1)):
            target=2*(1-p)
            risks=[target**2]+[4*p*(1-p)/j for j in range(1,len(weights))]
            fixed_risk=risks[m]
            forward=sum(w*(fixed_risk if j>=m else target**2) for j,w in enumerate(weights))
            require('poisson_to_fixed_coupling_direction',forward<=fixed_risk+4*sum(weights[:m]))
            random_risk=sum(w*r for w,r in zip(weights,risks))
            backward=sum(w*(risks[j] if j<=m else target**2) for j,w in enumerate(weights))
            require('fixed_to_poisson_coupling_direction',backward<=random_risk+4*sum(weights[m+1:]))

    # Local Bernoulli parameter choices: rational square-root subfamilies.
    for m in (1,2,3,4,8,16):
        n=m*m
        for j in (1,2,4,8,12,16):
            r=F(j,32)**2
            h=min(r,F(j,32*m))/8
            p0=r/2
            p1=p0+h
            require('boundary_local_pair_in_domain',0<p0<p1<=r<=F(1,4))
            chi_one=h*h/(p0*(1-p0))
            require('boundary_local_information_budget',n*chi_one<=F(1,24))
            require('boundary_local_product_chi', (1+chi_one)**n-1<=F(1,23))
            h=min(r,F(1,m))/8
            require('interior_local_pair_in_domain',F(1,2)+h<=F(1,2)+r)
            require('interior_local_information_budget',4*n*h*h<=F(1,16))

    # Exact square-root family, independently recomputing product affinity on counts.
    params=[]
    for u in (F(0),F(1,1000),F(1,40),F(1,20),F(1,10),F(1,5),F(3,10),F(2,5)):
        r=2*u/(1+u*u); s=(1-u*u)/(1+u*u)
        params.append((r*r,r,s))
    for (p,r,s),(q,t,u) in product(params,repeat=2):
        if not 0<=p<q<=F(1,2): continue
        gap=q-p; affinity=r*t+s*u; h2=1-affinity
        require('hellinger_exact_rationalization',2*h2==gap**2/(r+t)**2+gap**2/(s+u)**2)
        require('hellinger_two_sided_constants',gap**2/(8*q)<=h2<=gap**2/q)
        for n in (1,2,3,5,8,13):
            b0,b1=bern(n,p),bern(n,q)
            product_affinity=sum(F(comb(n,k))*(r*t)**k*(s*u)**(n-k) for k in range(n+1))
            e0,e1,bits=endpoint_lrt(n,p,q)
            tv=sum(abs(x-y) for x,y in zip(b0,b1))/2
            require('endpoint_lrt_monotone',bits==sorted(bits))
            require('endpoint_lrt_sum_is_optimal',e0+e1==1-tv)
            require('count_affinity_tensorization',product_affinity==affinity**n)
            require('endpoint_sum_affinity',e0+e1<=product_affinity)
            require('endpoint_tv_affinity',tv*tv<=1-product_affinity**2)
            require('endpoint_tv_linear',tv*tv<=2*n*h2)

    # Composite errors for every count threshold, including p>1/2 alternatives.
    for n in range(1,13):
        grid=[F(j,16) for j in range(17)]
        pmfs=[bern(n,p) for p in grid]
        for threshold in range(n+2):
            rejection=[sum(b[threshold:]) for b in pmfs]
            require('all_thresholds_stochastically_monotone',rejection==sorted(rejection))
            for low,high in ((0,1),(2,4),(5,8)):
                require('composite_null_endpoint',max(rejection[:low+1])==rejection[low])
                require('composite_alternative_endpoint',max(1-x for x in rejection[high:])==1-rejection[high])

    # A simple rational upper budget, 9 > 8 log 3, with actual endpoint tests.
    require('rational_upper_budget_exponential',sum(F(9,8)**k/factorial(k) for k in range(9))>3)
    for p,q in ((F(0),F(1,2)),(F(0),F(1,4)),(F(1,4),F(1,2)),(F(1,8),F(3,8)),(F(1,4),F(3,8)),(F(3,8),F(1,2))):
        rate=q/(q-p)**2
        n=ceil(9*rate)
        e0,e1,_=endpoint_lrt(n,p,q)
        require('sample_complexity_constructive_upper',max(e0,e1)<=F(1,3))
        for n in (1,2,3,4,8,16,32):
            b0,b1=bern(n,p),bern(n,q)
            tv=sum(abs(x-y) for x,y in zip(b0,b1))/2
            require('sample_complexity_necessary_lower',tv<F(1,3) or n>=rate/18)

    # Scale-free critical-gap algebra, x=sqrt(n*nu); n cancels exactly.
    for x in [F(j,16) for j in range(257)]+[F(100),F(10000)]:
        for c in (F(1,100),F(1,8),F(1),F(4),F(16)):
            ratio=c*c*(x+1)**2/(x*x+c*(x+1))
            require('critical_gap_sufficient_algebra',ratio>=c*c/(1+c))
            if c<=1:
                require('critical_gap_necessary_algebra',ratio<=4*c)

    # Deterministic reconstruction at a different grid, with a stronger delta bound.
    for k in range(1,9):
        delta=F(1,k)
        for z in range(3*k+1):
            target=F(z,3*k)
            for bits in product((0,1),repeat=k):
                errors=sum(bit if target<=j*delta else 1-bit if target>=(j+1)*delta else 0
                           for j,bit in enumerate(bits))
                require('grid_reconstruction_stronger_bound',abs(delta*sum(bits)-target)<=delta+delta*errors)

    # Pointwise inequalities imply expectation bounds without distributional assumptions.
    grid=[F(j,8) for j in range(9)]
    for nu in grid[:-1]:
        for outer in [x for x in grid if x>nu]:
            delta=outer-nu
            for target in grid:
                if not (target<=nu or target>=outer): continue
                for estimate in grid:
                    rejected=estimate>=nu+delta/2
                    error=int((target<=nu and rejected) or (target>=outer and not rejected))
                    require('estimator_test_absolute',error<=2*abs(estimate-target)/delta)
                    require('estimator_test_squared',error<=4*(estimate-target)**2/delta**2)

    # Sensitivity controls catch common invalid generalizations and endpoint mistakes.
    p=F(99,100)**2; q=F(1); h2=F(1,100)
    reject('extend_hellinger_upper_bound_past_half',h2<=(q-p)**2/q)
    e0,e1,_=endpoint_lrt(1,F(0),F(1,2))
    reject('sum_error_two_thirds_implies_each_one_third',not(e0+e1<=F(2,3)) or max(e0,e1)<=F(1,3))
    n=100; gap=F(1,100*n)
    reject('drop_one_over_n_boundary_gap',1-(1-gap)**n>=F(1,3))
    # At nu=.49 and n=1, even the maximum admissible gap .01 is untestable.
    b0,b1=bern(1,F(49,100)),bern(1,F(1,2))
    endpoint_tv=sum(abs(x-y) for x,y in zip(b0,b1))/2
    reject('unqualified_critical_gap_at_truncated_endpoint',endpoint_tv>=F(1,3))
    # A point mass has B_n=1, so log n <= C log B_n is impossible for n>1.
    n=16; b=F(1); c=2
    reject('theorem_four_eligible_point_reference',n<=b**c)
    # A test at a single threshold cannot locate all values on the same side.
    first,second=F(1,4),F(1,2)
    null_radius=F(3,4)
    same_perfect_test_outputs=(int(first>null_radius)==int(second>null_radius))
    reject('single_threshold_exact_reconstruction',not same_perfect_test_outputs or first==second)

    for name,digest in before.items():
        require('frozen_inputs_unchanged_after_run',hashlib.sha256((args.bundle/name).read_bytes()).hexdigest()==digest)
    out={
        'status':'PASS_WITH_SCOPE_LIMITS',
        'arithmetic':'Python fractions.Fraction, exact rational arithmetic',
        'author_replay_assertions':replay['total_assertions'],
        'independent_control_assertions':sum(COUNTS.values()),
        'checks':dict(sorted(COUNTS.items())),
        'negative_controls_rejected':NEGATIVE_CONTROLS,
        'input_files_unchanged':True,
        'scope':'Finite controls and frozen-input integrity only. Analytical proof and source review are in AUDIT_REPORT.md. No literature-exhaustiveness, priority, novelty, or complete-resolution certificate.'
    }
    text=json.dumps(out,indent=2)+'\n'
    if args.output: args.output.write_text(text)
    print(text,end='')

if __name__=='__main__':
    main()
