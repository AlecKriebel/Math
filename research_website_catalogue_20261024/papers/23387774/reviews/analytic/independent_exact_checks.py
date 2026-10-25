#!/usr/bin/env python3
"""Own finite exact controls; no deposited/foreign source program execution."""
from fractions import Fraction as F
from itertools import product, permutations
from math import factorial, comb
from pathlib import Path
from datetime import datetime, timezone
import json

E = Path(__file__).resolve().parent


def falling(n, r):
    ans = 1
    for k in range(r): ans *= n-k
    return ans
def rising(n, r):
    ans = 1
    for k in range(r): ans *= n+k
    return ans
def compositions(n):
    if n == 0: yield (); return
    for j in range(1, n+1):
        for rest in compositions(n-j): yield (j,)+rest
def prod(values):
    ans = F(1)
    for v in values: ans *= v
    return ans


def assembly_checks():
    # Generic rational positive weights, deliberately different from zeta weights:
    # the algebraic identity must hold independently of analytic zeta asymptotics.
    N = 7; a = [F(0)]+[F(1, 2*j)+F(1, 3*j*j) for j in range(1, N+1)]
    h = [F(1)]
    for n in range(1, N+1): h.append(sum(j*a[j]*h[n-j] for j in range(1,n+1))/n)
    factorial_checks = marked_checks = labelled_count = 0
    no_conditioning_rejected = False
    for n in range(1, N+1):
        rows = []
        for c in compositions(n):
            weight = prod(a[j] for j in c)/factorial(len(c))
            rows.append((c, weight))
        assert sum(w for c,w in rows) == h[n]
        for rs in product(range(3), repeat=min(3,n)):
            R = sum((j+1)*r for j,r in enumerate(rs))
            direct = sum(w*prod(falling(c.count(j+1),r) for j,r in enumerate(rs)) for c,w in rows)/h[n]
            independent = prod(a[j+1]**r for j,r in enumerate(rs))
            expected = independent*h[n-R]/h[n] if R <= n else F(0)
            assert direct == expected
            no_conditioning_rejected |= R <= n and direct != independent
            factorial_checks += 1
        probabilities = [F(0)]+[F(j+1,j+3) for j in range(1,n+1)]
        for r in range(1,4):
            direct = F(0)
            for c,w in rows:
                pgf = [F(1)]
                for j in c:
                    p = probabilities[j]; new = [F(0)]*(len(pgf)+1)
                    for m,v in enumerate(pgf): new[m] += v*(1-p); new[m+1] += v*p
                    pgf = new
                direct += w*sum(p*falling(m,r) for m,p in enumerate(pgf))/h[n]
            expected = F(0)
            for js in product(range(1,n+1),repeat=r):
                R = sum(js)
                if R <= n: expected += h[n-R]/h[n]*prod(a[j]*probabilities[j] for j in js)
            assert direct == expected
            marked_checks += 1
        # A separate labelled-permutation enumeration checks the cycle factor j.
        weights = F(0)
        for sigma in permutations(range(n)):
            seen = set(); lengths = []
            for i in range(n):
                if i in seen: continue
                j = i; length = 0
                while j not in seen: seen.add(j); length += 1; j = sigma[j]
                lengths.append(length)
            weights += prod(j*a[j] for j in lengths)
            labelled_count += 1
        assert weights/factorial(n) == h[n]
    assert no_conditioning_rejected
    return {'generic_positive_rational_weight_sizes':list(range(1,N+1)),
            'composition_normalizations':N,'factorial_identity_cases':factorial_checks,
            'independently_marked_PGF_factorial_cases':marked_checks,
            'labelled_permutations_independently_enumerated':labelled_count,
            'cycle_factor_and_conditioning_match':True,
            'unconditioned_Poisson_negative_control_rejected':True}


def beta_integral(a,b):
    # Expand (1-x)^(b-1), then integrate monomials on [0,1].
    return sum(F((-1)**k*comb(b-1,k),a+k) for k in range(b))
def simplex_integral(alpha):
    if len(alpha)==1: return F(1)
    return beta_integral(alpha[0],sum(alpha[1:]))*simplex_integral(alpha[1:])
def dirichlet_checks():
    count = 0; wrong_shapes_rejected = False
    for n in range(1,7):
        for js in compositions(n):
            if len(js)>3: continue
            alpha = [2*j for j in js]; total = 2*n
            closed = F(prod(factorial(x-1) for x in alpha),factorial(total-1))
            assert simplex_integral(alpha) == closed
            assert prod(F(factorial(2*j-1),factorial(2*j)) for j in js) == prod(F(1,2*j) for j in js)
            for powers in product(range(3),repeat=len(js)):
                integral = simplex_integral([x+p for x,p in zip(alpha,powers)])/closed
                exact = prod(rising(x,p) for x,p in zip(alpha,powers))/rising(total,sum(powers))
                assert integral == exact
                if len(js)>1 and sum(powers)>1:
                    wrong = prod(rising(x,p) for x,p in zip(js,powers))/rising(n,sum(powers))
                    wrong_shapes_rejected |= wrong != exact
                count += 1
    assert wrong_shapes_rejected
    return {'simplex_mass_and_moment_cases':count,'at_most_three_components':True,
            'monomial_factorial_cancellation_yields_1_over_2j':True,
            'Gamma_2j_total_2n_matches_Dirichlet':True,
            'halved_shapes_control_rejected':True}


def D(g,k):
    return F(factorial(6*g-5-2*k)*2**(2*k-3),factorial(g-k)*factorial(3*g-3-k)*3**(g-k)) if k>=2 else F(factorial(6*g-7),2*factorial(g-1)*factorial(3*g-4)*3**(g-1))
def log_bounds(x,terms=12):
    t=(x-1)/(x+1)
    lower=2*sum(t**(2*k+1)/F(2*k+1) for k in range(terms))
    upper=lower+2*t**(2*terms+1)/((2*terms+1)*(1-t*t))
    return lower,upper
def prefactor_cutoff_checks():
    count=0
    for g in range(2,26):
        for k in range(1,min(g,8)):
            formula=F(12*(g-k)*(3*g-3-k),(6*g-5-2*k)*(6*g-6-2*k))
            assert D(g,k+1)/D(g,k)==formula
            count+=1
    ln11lo,ln11hi=log_bounds(F(11,10));ln2lo,ln2hi=log_bounds(F(2));ln9lo,ln9hi=log_bounds(F(9,4));ln15lo,ln15hi=log_bounds(F(3,2))
    eta_lower=F(3,5)*ln11lo-F(1,20)
    assert eta_lower>F(1,220)
    assert F(11,10)<F(8,7)
    assert F(3,5)*ln2hi<1
    assert F(3,5)*ln9hi<1
    assert 2*ln15lo-F(1,2)>0 and ln2hi<1
    return {'exact_prefactor_ratio_cases':count,'genus_range':[2,25],
            'cutoff_eta_strictly_greater_than_1_over_220_certified':True,
            't_11_over_10_within_8_over_7':True,
            'low_k_range_and_multivertex_exponent_eventually_valid':True,
            'Gamma_tail_exponents_positive':True,
            'logarithm_certification':'Exact rational atanh-series lower/upper remainder bounds, twelve terms; no floating inequalities.'}


def run_checks():
    return {'assemblies':assembly_checks(),'Dirichlet':dirichlet_checks(),
            'prefactors_and_cutoff':prefactor_cutoff_checks(),'all_pass':True}


if __name__=='__main__':
    result={'utc':datetime.now(timezone.utc).isoformat(),'arithmetic':'Python Fraction and finite combinatorial enumeration',**run_checks(),
            'scope':'Meaningful finite algebra/transcription diagnostics only. They do not prove geometric imports, all-genus estimates, arbitrary intermediate rates or historical priority.'}
    (E/'independent-exact-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
