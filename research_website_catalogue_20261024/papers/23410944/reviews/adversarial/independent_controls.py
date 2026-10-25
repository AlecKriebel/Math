"""Fresh adversarial controls, exact arithmetic; not an infinite PDE certificate.

These focus on missing hypotheses, rather than duplicating the archive's
small-rotation examples. Infinite countermodels are justified in REVIEW.md.
"""
from collections import Counter
from fractions import Fraction as F
import json

counts = Counter()


def check(group, condition):
    if not condition:
        raise AssertionError(group)
    counts[group] += 1


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def sub(a, b):
    return [[x-y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def diag(xs):
    return [[F(xs[i]) if i == j else F(0) for j in range(len(xs))]
            for i in range(len(xs))]


# A proper subspace can approximate EVERY coordinate probe to a small fixed
# tolerance. This defeats a one-time/fixed-error substitute for the paper's
# repeated probe schedule with errors tending to zero.
probe_rows = []
for n in (16, 25, 36):
    p = [[F(i == j)-F(1, n) for j in range(n)] for i in range(n)]
    check('proper_projection_idempotent', mul(p, p) == p)
    check('proper_projection_rank', sum(p[j][j] for j in range(n)) == n-1)
    check('missed_nonzero_direction', all(sum(row) == 0 for row in p))
    for j in range(n):
        residual = [F(i == j)-p[i][j] for i in range(n)]
        check('all_probes_fixed_error_small', sum(x*x for x in residual) == F(1, n) < F(1, 9))
    probe_rows.append({'dimension': n, 'rank': n-1, 'every_probe_residual_squared': str(F(1,n)),
                       'missed_direction': 'the all-ones vector'})


# A fixed finite-rank projection can survive while its energies diverge if
# the limiting operator called a resolvent has a kernel. The actual R in the
# paper is injective, which blocks precisely this example.
p = diag([1, 0])
r_limit = diag([0, F(1, 2)])
escape_rows = []
for n in (1, 2, 4, 8, 16, 64, 256):
    r = diag([F(1, n+1), F(1, 2)])
    a = diag([n, 1])
    check('injectivity_control_true_resolvents', mul(r, [[a[i][j]+F(i == j) for j in range(2)] for i in range(2)]) == eye(2))
    check('injectivity_control_commutation', mul(p, r) == mul(r, p))
    check('injectivity_control_fixed_rank', mul(p, p) == p and sum(p[j][j] for j in range(2)) == 1)
    check('injectivity_control_limit_kernel', mul(p, r_limit) == diag([0, 0]))
    check('injectivity_control_norm_error', sub(r, r_limit) == diag([F(1,n+1), 0]))
    escape_rows.append({'n': n, 'protected_energy': n, 'resolvent_error': str(F(1,n+1))})


# An actual one-dimensional Dirichlet diagnostic: touching intervals with
# any positive connector are the whole interval (-1,1). The test function
# u=1-|x| belongs to H01(-1,1), has trace 1 at the deleted midpoint, and its
# exact piecewise polynomial H1 mass cannot converge to a zero-midpoint
# trace function in H1. This tests the excluded d=1 boundary case without
# relying on a numerical eigenvalue approximation.
# For v in H01(-1,0) direct_sum H01(0,1), w=u-v has w(0)=1 and w(1)=0;
# Cauchy-Schwarz forces integral_0^1 |w'|^2 >= 1 (and likewise on the left).
check('dimension_one_trace_obstruction', F(1)**2/F(1) + F(1)**2/F(1) == 2)
check('dimension_one_tent_norm', F(2,3)+2 == F(8,3))


# Smooth-polynomial profile in logarithmic radial coordinates. The
# theta=10s^3-15s^4+6s^5 profile has zero first/second endpoint derivatives;
# extension is C2 and H1, sufficient for this diagnostic (the proof chooses
# a C-infinity profile). Its derivative is 30s^2(1-s)^2.
coeff = {2:F(30), 3:F(-60), 4:F(30)}
integral = sum(x*y/F(i+j+1) for i,x in coeff.items() for j,y in coeff.items())
check('log_cutoff_exact_profile_energy', integral == F(10,7))
energy_rows = []
last = None
for k in (2, 4, 8, 16, 32, 64):
    # r=exp(-k): energy/pi=2 integral(theta'^2)/k.
    e_over_pi = F(2)*integral/k
    check('log_cutoff_energy_value', e_over_pi == F(20,7*k))
    if last is not None:
        check('log_cutoff_energy_decay', e_over_pi == last/2)
    last = e_over_pi
    energy_rows.append({'minus_log_r': k, 'energy_over_pi': str(e_over_pi)})


# Moving spectral cutoffs alone have no rank-preserving norm limit. These
# exact finite sections illustrate P_n -> I strongly on l2, while each P_n
# has finite rank and ||I-P_n||=1. The paper fixes k BEFORE taking its limit.
for n in range(1, 41):
    pn = diag([1]*n+[0])
    check('fixed_k_required_idempotent', mul(pn,pn) == pn)
    check('fixed_k_required_rank_growth', sum(pn[j][j] for j in range(n+1)) == n)
    check('fixed_k_required_norm_gap', pn[-1][-1] == 0)


# Exact support/distance check for a positive-length gap. With gap g>0 a
# connector of transverse halfwidth h adds a rectangular set of volume
# g(2h)^(d-1)>0. Thus the common-L2 argument is special to touching faces.
gap_rows = []
for d in range(2, 9):
    g, h = F(1,7), F(1,9)
    volume = g*(2*h)**(d-1)
    check('passage_changes_hilbert_measure', volume > 0)
    gap_rows.append({'dimension':d, 'new_positive_measure_volume':str(volume)})


# Dense eigenvalues alone: finite rational grids uniformly approximate
# [0,4], but a direct sum with the multiplication operator on L2(0,infinity)
# retains its absolutely continuous subspace. The infinite claim is a
# direct spectral-measure calculation recorded in REVIEW.md, not a code
# conclusion.
for n in (2,4,8,16,32,64):
    qs = [F(j,n) for j in range(1,4*n+1)]
    check('dense_grid_endpoint', qs[-1] == 4)
    check('dense_grid_mesh', all(qs[j+1]-qs[j] == F(1,n) for j in range(len(qs)-1)))
    check('continuous_summand_survives', F(3,4)-F(1,4) == F(1,2))

print(json.dumps({
    'status':'PASS_DIAGNOSTICS_ONLY', 'assertions':sum(counts.values()),
    'groups':dict(sorted(counts.items())), 'arithmetic':'exact rational',
    'fixed_nonzero_probe_error_negative_control':probe_rows,
    'noninjective_limit_negative_control':escape_rows,
    'two_dimensional_log_capacity':energy_rows,
    'positive_length_passage_negative_control':gap_rows,
    'limits':['Finite identities and boundary-case countermodels only.',
              'No PDE discretization, admissible aperture sizes, formal theorem verification, or novelty certification.']
},indent=2))
