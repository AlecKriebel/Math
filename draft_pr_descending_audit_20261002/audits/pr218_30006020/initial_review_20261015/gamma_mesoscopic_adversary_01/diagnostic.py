#!/usr/bin/env python3
"""Fresh finite-n analytic diagnostics; no Monte Carlo or asymptotic proof.

Only the Python standard library is required. Running this file writes results
beside itself. Sources/audit checkers are not used by this computation.
"""
from pathlib import Path
import itertools
import json
import math


def zeta_even(j):
    exact = {1: math.pi**2/6, 2: math.pi**4/90,
             3: math.pi**6/945, 4: math.pi**8/9450,
             5: math.pi**10/93555}
    if j in exact:
        return exact[j]
    if j >= 28:
        return 1.0  # absolute omission below 2e-17
    return math.fsum(m**(-2*j) for m in range(1, 129))


def coefficients(nmax):
    # n h_n = (1/2) sum_(j=1)^n zeta(2j) h_(n-j).
    h = [1.0] + [0.0]*nmax
    correction = [0.0]+[zeta_even(j)-1.0 for j in range(1, 28)]
    prefix = 1.0
    for n in range(1, nmax+1):
        h[n] = (prefix + math.fsum(correction[j]*h[n-j]
                    for j in range(1, min(n, 27)+1)))/(2*n)
        prefix += h[n]
    return h


def normalized_tails(pmf):
    total = math.fsum(pmf)
    tails = [0.0]*(len(pmf)+1)
    for k in range(len(pmf)-1, -1, -1):
        tails[k] = tails[k+1] + pmf[k]/total
    return tails


def poisson_tails(x, required):
    if x == 0:
        return [1.0]+[0.0]*(required+1)
    last = max(required, math.ceil(x+16*math.sqrt(x+1)+100))
    mode = math.floor(x)
    pmf = [0.0]*(last+1)
    # Only ratios matter after normalization; putting mode=1 avoids underflow.
    pmf[mode] = 1.0
    for k in range(mode, 0, -1):
        pmf[k-1] = pmf[k]*k/x
    for k in range(mode, last):
        pmf[k+1] = pmf[k]*x/(k+1)
    return normalized_tails(pmf)


def binomial_tails(n, p):
    if p <= 0:
        return [1.0]+[0.0]*(n+1)
    if p >= 1:
        return [1.0]*(n+1)+[0.0]
    mode = math.floor((n+1)*p)
    pmf = [0.0]*(n+1)
    pmf[mode] = 1.0
    for k in range(mode, 0, -1):
        pmf[k-1] = pmf[k]*k/(n-k+1)*(1-p)/p
    for k in range(mode, n):
        pmf[k+1] = pmf[k]*(n-k)/(k+1)*p/(1-p)
    return normalized_tails(pmf)


def expected_counts(n, q, h):
    # Gamma integer-shape CDF = upper Poisson tail; beta integer-shape CDF
    # = upper binomial tail with common trial count 2n-1.
    lo_g = poisson_tails(2*q, 2*n)
    hi_g = poisson_tails(4*q, 2*n)
    lo_b = binomial_tails(2*n-1, q/n)
    hi_b = binomial_tails(2*n-1, 2*q/n)
    marked, normalized, unmarked = [], [], []
    for j in range(1, n+1):
        weight = zeta_even(j)/(2*j)*h[n-j]/h[n]
        marked.append(weight*max(0.0, hi_g[2*j]-lo_g[2*j]))
        if j == n:
            prob = float(q/n <= 1 <= 2*q/n)
        else:
            prob = max(0.0, hi_b[2*j]-lo_b[2*j])
        normalized.append(weight*prob)
        if q <= j <= 2*q:
            unmarked.append(weight)
    return {'unmarked_mean':math.fsum(unmarked),
            'gamma_marked_mean':math.fsum(marked),
            'normalized_mean':math.fsum(normalized)}


def partitions(n, low=1):
    if n == 0:
        yield ()
    for j in range(low, n+1):
        for rest in partitions(n-j, j):
            yield (j,)+rest


def falling(k, r):
    ans = 1
    for i in range(r):
        ans *= k-i
    return ans


def check_factorial_formula(h):
    largest = 0.0
    for n in range(1, 13):
        weighted = []
        for parts in partitions(n):
            counts = {j:parts.count(j) for j in set(parts)}
            mass = math.prod((zeta_even(j)/(2*j))**c/math.factorial(c)
                             for j,c in counts.items())
            count = sum(2 <= j <= 4 for j in parts)
            weighted.append((mass,count))
        assert abs(math.fsum(m for m,c in weighted)-h[n]) < 1e-13
        for r in range(1, 4):
            direct = math.fsum(m*falling(c,r) for m,c in weighted)/h[n]
            removed = math.fsum(h[n-sum(js)]/h[n]*math.prod(
                zeta_even(j)/(2*j) for j in js)
                for js in itertools.product(range(2,5), repeat=r)
                if sum(js) <= n)
            largest = max(largest, abs(direct-removed))
            assert abs(direct-removed) < 1e-12
    return largest


def main():
    h = coefficients(16384)
    results = {'interpretation':'Finite-n diagnostics, not an asymptotic proof.',
       'target_window':[1,2], 'poisson_limit_mean':math.log(2)/2,
       'max_factorial_identity_error_n_le_12':check_factorial_formula(h),
       'constants': {'large_shape_tail_c':2*math.log(1.5)-0.5,
        'cutoff_eta':0.6*math.log(1.1)-0.05,
        'non_one_vertex_power':1-0.6*math.log(2)}, 'cases':[]}
    for n in [64,256,1024,4096,16384]:
        slow = math.log(math.log(n+math.exp(math.e)))
        for label,q in [('q_loglog',slow),('q_sqrt',math.sqrt(n)),
                        ('q_n_over_loglog',n/slow)]:
            results['cases'].append({'n':n,'scale':label,'q':q,'q_over_n':q/n,
                'h_n_sqrt_n':h[n]*math.sqrt(n),
                'max_scaled_coefficient_ratio':max(h[n-j]/h[n]/math.sqrt(
                    (n+1)/(n-j+1)) for j in range(n+1)),
                **expected_counts(n,q,h)})
    dst=Path(__file__).with_name('diagnostic_results.json')
    dst.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
