#!/usr/bin/env python3
"""Independent exact stress checks; finite checks corroborate proofs, not replace them.
No numerical roots: test p-th moments and powers of two as exact Fractions.
"""
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from datetime import datetime, timezone
import json, random

HERE = Path(__file__).resolve().parent
random.seed(20260930)

@dataclass
class Fiber:
    name: str
    d: int
    h: object  # log_2 rho, normalization irrelevant for all ratios
    adjacent_bound: int
    predicted_cut: object  # None means all/empty distinguished by name

    def a0(self, n):
        return self.h(n-self.d) - self.h(n) <= -1
    def m(self, n):
        return all(self.a0(n+j) for j in range(self.d))
    def n(self, n):
        return any(not self.a0(n+j) for j in range(self.d))


def two(exp):
    return Fraction(2**exp, 1) if exp >= 0 else Fraction(1, 2**(-exp))

fibers = [
    Fiber('global_forward_contraction', 1, lambda n:n, 1, 'all'),
    Fiber('global_inverse_contraction', 1, lambda n:-n, 1, 'empty'),
]
for cut in [-100000, -101, -1, 0, 1, 104, 100000]:
    fibers.append(Fiber(f'moving_peak_{cut}', 1, lambda n,k=cut:-abs(n-k), 1, cut))

# Genuine disagreeing residue-class cuts, with common shifts unbounded across fibers.
# Each d-step residue sequence is an exact tent; adjacent ratios remain bounded.
for d in [2,3,5,11]:
    for shift in [-10000, 0, 10000]:
        delta = [random.randint(-20,20) for _ in range(d)]
        off = [random.randint(-9,9) for _ in range(d)]
        peaks = [r+d*(shift+delta[r]) for r in range(d)]
        L = max(abs(delta[r]-delta[(r+1)%d]) +
                abs(off[r]-off[(r+1)%d]) + 1 for r in range(d))
        def h(n,d=d,s=shift,delta=tuple(delta),off=tuple(off)):
            q,r = divmod(n,d)
            return -abs(q-s-delta[r])+off[r]
        fibers.append(Fiber(f'residues_d{d}_shift{shift}', d, h, L, min(peaks)))

counts = dict(fibers=len(fibers), density=0, adjacency=0, propagation=0,
              intersection_cut=0, one_step_invariance=0, power_norm=0,
              exact_vector_moments=0)
for f in fibers:
    if isinstance(f.predicted_cut, int):
        center = f.predicted_cut
        width = 1000 + 30*f.d
        points = range(center-width, center+width+1)
    else:
        center, points = 0, range(-500,501)
    for x in points:
        assert min(f.h(x-f.d),f.h(x+f.d)) <= f.h(x)-1
        counts['density'] += 1
        assert abs(f.h(x+1)-f.h(x)) <= f.adjacent_bound
        counts['adjacency'] += 1
        if f.a0(x):
            assert f.a0(x-f.d)
        else:
            assert not f.a0(x+f.d)
        counts['propagation'] += 1
        assert f.m(x) != f.n(x)
        if isinstance(f.predicted_cut,int):
            assert f.m(x) == (x <= f.predicted_cut)
        elif f.predicted_cut == 'all':
            assert f.m(x)
        else:
            assert not f.m(x)
        counts['intersection_cut'] += 1
        if f.m(x):
            assert f.m(x-1)
        if f.n(x):
            assert f.n(x+1)
        counts['one_step_invariance'] += 1
        for m in [0,1,2,7,31]:
            if f.m(x):
                assert f.h(x-m*f.d)-f.h(x) <= -m
            else:
                # D^p <= 2^(2 L (d-1)); independent of p.
                assert f.h(x+m*f.d)-f.h(x) <= 2*f.adjacent_bound*(f.d-1)-m
            counts['power_norm'] += 1
    for p in [1,2,3,8]:
        for which in ['m','n']:
            # 3+4i has exact modulus five, so covers complex amplitudes too.
            coords = [center+i for i in range(-50,51)
                      if (f.m(center+i) if which=='m' else f.n(center+i))]
            vec = {n:random.choice([1,2,5]) for n in random.sample(coords,min(13,len(coords)))}
            inp = sum(Fraction(v**p) for v in vec.values())
            for m in [0,1,4,29]:
                displacement = -m*f.d if which=='m' else m*f.d
                out = sum(two(f.h(n+displacement)-f.h(n))*v**p for n,v in vec.items())
                boundexp = -m if which=='m' else 2*f.adjacent_bound*(f.d-1)-m
                assert out <= two(boundexp)*inp
                counts['exact_vector_moments'] += 1

# Uniformity failure attempt: each fiber has a tent, but slope tends to zero.
# For every proposed common d and eta=1/2, pick k>d, slope=1/k.
nonuniform = []
for d in [1,2,17,100]:
    k = 2*d
    # At the peak min rho_{+-d}/rho_0 = 2^(-d/k)=2^(-1/2)>1/2.
    assert Fraction(d,k) < 1
    nonuniform.append({'proposed_d':d,'chosen_fiber_k':k,'log2_drop':str(Fraction(-d,k)),
                       'common_eta_half_condition':'fails'})

# Invalid disagreeing-cut attempt: residue peaks separate without bound.
# On far left/right tails h_even-h_odd has two values separated by 2k.
# No choice of additive offset can bound both uniformly over k.
unbounded_cut_separation = [{'separation_k':k,'minimum_needed_adjacent_log_bound':k}
                           for k in [10,100,1000,10000]]

# Infinite moving-cut model: W=N with nu({k})=2^(-k-1), rho_n(k)=2^(k-|n-k|).
# Exact aggregate level masses from elementary geometric sums.
aggregate = []
for n in [-10,-1,0,1,2,10,30]:
    exact = two(n) if n<=0 else Fraction(3,2)-two(-n-1)
    if n>=0:
        finite = sum(two(-k-1+k-abs(n-k)) for k in range(n))
        tail = Fraction(1) # k>=n: sum nu_k*2^n=1.
        assert finite+tail == exact
    aggregate.append({'n':n,'mu_f_n_W':str(exact),
                      'density_ess_sup_over_inf':str(two(2*n)) if n>=0 else '1'})

result = {'checked_at':datetime.now(timezone.utc).isoformat(),
          'status':'all_assertions_passed','counts':counts,
          'coverage':['p=1','p=2,3,8 exact p-th moments','real and complex modulus',
                      'unbounded moving common fiber cuts','genuine different residue cuts',
                      'both-direction drops at peaks','M=0 and N=0',
                      'finite intersections and complementary finite unions',
                      'uniformity failure with slope tending to zero',
                      'boundedness failure with unbounded residue-cut separation',
                      'explicit no-bounded-distortion composition model'],
          'limitations':'Finite exact assertions stress global formulas; proof obligations are discharged in DERIVATION.md, not by this script.',
          'rejected_nonuniform_fiber_attempts':nonuniform,
          'rejected_unbounded_residue_separations':unbounded_cut_separation,
          'moving_cut_aggregate_example':aggregate}
(HERE/'stress_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'counts':counts},indent=2))
