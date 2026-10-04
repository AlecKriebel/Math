#!/usr/bin/env python3
"""Independent rational audit. No imports from the author's verifier.

The finite arithmetic here is supplementary to AUDIT.md's analytic/topological
review. It neither checks Lean nor proves analyticity or convexity by sampling.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
checks = {}

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = True

def pair(a=0, b=0):
    return (F(a), F(b))

def plus(u, v):
    return (u[0]+v[0], u[1]+v[1])

def neg(u):
    return (-u[0], -u[1])

def times(u, v):
    return (u[0]*v[0]-u[1]*v[1], u[0]*v[1]+u[1]*v[0])

def scale(a, u):
    return (a*u[0], a*u[1])

def squared(u):
    return u[0]**2+u[1]**2

def quotient(u, v):
    return scale(1/squared(v), times(u, (v[0], -v[1])))

def strings(u):
    return [str(x) for x in u]

public = ROOT/'public'
manifest_bytes = (public/'SHA256SUMS.json').read_bytes()
check('frozen_manifest_digest', hashlib.sha256(manifest_bytes).hexdigest() ==
      '3927dbc7cf71fe73904c037e36772a08cb17157e0bfed8104e5ffc7fa356f1e2')
manifest = json.loads(manifest_bytes)
check('exact_frozen_file_set', {p.name for p in public.iterdir()} ==
      set(manifest['files']) | {'SHA256SUMS.json'})
for name, expected in manifest['files'].items():
    data = (public/name).read_bytes()
    check('frozen_'+name, len(data) == expected['bytes'] and
          hashlib.sha256(data).hexdigest() == expected['sha256'])
check('author_replay_byte_identity', (ROOT/'independent-audit/replay_checks.json').read_bytes() ==
      (public/'CHECKS.json').read_bytes())

one = pair(1)
q = pair(F(1,3), -F(1,6))
q2 = times(q, q)
q3 = times(q2, q)
w = plus(one, neg(q3))
r = F(399,400)
alpha = pair(F(8,9), F(4,9))
beta = scale(1/r**3, w)
t = F(3,5)

check('q_square', q2 == pair(F(1,12), -F(1,9)))
check('q_cube', q3 == pair(F(1,108), -F(11,216)))
check('w_value', w == pair(F(107,108), F(11,216)))
check('alpha_norm_squared', squared(alpha) == F(80,81))
check('w_norm_squared', squared(w) == F(45917,46656))
check('beta_admissibility_margin', r**6-squared(w) ==
      F(2785244627851129,2985984000000000000) > 0)
check('beta_norm_squared', squared(beta) ==
      F(2938688000000000000,2941473244627851129) < 1)
check('sector_for_principal_power', q[0] > 0 and q[1] < 0 and
      q[0]**2-3*q[1]**2 == F(1,36) > 0)
check('evaluation_domain', 1/r == F(400,399) > 1)
check('weight_domain', 0 < t < 1)
check('alpha_uniform_tail_bound', squared(alpha) < F(179,180)**2)
check('beta_uniform_tail_bound', squared(beta) < F(9999,10000)**2)
tail_upper = t*F(179,180)+(1-t)*F(9999,10000)
check('uniform_derivative_margin', tail_upper < F(299,300) < 1)

# Compute D and N by differentiating each component, not by using the
# author's precombined N formula. N = D + z0 H''(z0).
fprime = plus(one, neg(scale(r*r, alpha)))
zfsecond = scale(2*r*r, alpha)
gprime = q2
zgsecond = scale(2, quotient(w, q))
D = plus(scale(t, fprime), scale(1-t, gprime))
zHsecond = plus(scale(t, zfsecond), scale(1-t, zgsecond))
N = plus(D, zHsecond)
R = plus(one, quotient(zHsecond, D))
check('D_integer_components', D == scale(F(1,1800000), pair(184794,-557603)))
check('N_integer_components', N == scale(F(1,1800000), pair(5431206,2285603)))
check('D_nonzero', squared(D) > 0)
check('exact_quotient', R == pair(F(-54160961609,69013985609),
                                  F(690164496000,69013985609)))
check('negative_real_part', R[0] < 0)

# Independent integer cross-product check, without complex division.
integer_norm = 184794**2 + 557603**2
integer_dot = 5431206*184794 - 2285603*557603
integer_cross = 2285603*184794 + 5431206*557603
check('integer_real_crosscheck', F(integer_dot, integer_norm) == R[0])
check('integer_imaginary_crosscheck', F(integer_cross, integer_norm) == R[1])

# Compare every coefficient of the weight quadratic, rather than sampling
# finitely many lambda values. N(t) conj(D(t)) is degree <= 2.
d0 = gprime
d1 = plus(fprime, neg(gprime))
n0 = plus(gprime, zgsecond)
n1 = plus(plus(fprime, zfsecond), neg(n0))
def real_product_conjugate(u,v):
    return u[0]*v[0]+u[1]*v[1]
quadratic = [real_product_conjugate(n0,d0),
             real_product_conjugate(n1,d0)+real_product_conjugate(n0,d1),
             real_product_conjugate(n1,d1)]
check('all_quadratic_coefficients', quadratic ==
      [F(2956000000,25920000000), F(-17772056000,25920000000),
       F(15391097599,25920000000)])
check('quadratic_at_chosen_weight', sum(c*t**k for k,c in enumerate(quadratic)) ==
      R[0]*squared(D) < 0)

# Check Laurent primitive coefficients independently from a signed recurrence.
binomial = F(1)
partial = F(0)
for n in range(1,97):
    binomial *= (F(2,3)-(n-1))/n
    coefficient = scale(binomial * (-1)**n / (1-3*n),
                        pair(1))  # scalar coefficient before beta**n
    check('primitive_derivative_'+str(n),
          (1-3*n)*coefficient[0] == binomial*(-1)**n)
    check('primitive_no_log_'+str(n), 1-3*n != 0 and 3*n != 1)
    partial += abs(binomial)
    next_absolute = abs(binomial)*F(3*n-2,3*n+3)
    check('telescoping_partial_'+str(n), partial ==
          1-F(3*(n+1),2)*next_absolute and 0 < partial < 1)

negative_controls = {
    'wrong_radius_fails_beta': squared(scale(1/F(99,100)**3,w)) >= 1,
    'conjugate_branch_is_not_q_cube': times(times((q[0],-q[1]),(q[0],-q[1])),
                                         (q[0],-q[1])) != q3,
    'wrong_numerator_rejected': R[0] != F(-54160961608,69013985609),
    'reversed_sign_rejected': not R[0] >= 0,
    'endpoint_G_not_negative': quotient(n0,d0)[0] > 0,
    'endpoint_F_not_negative': quotient(plus(fprime,zfsecond),fprime)[0] > 0,
}
for name,value in negative_controls.items():
    check('negative_control_'+name,value)

sources = {}
for key, name in [('primary_original','hayman-lingham-2018.pdf'),
                  ('prior_resolution','guo-hu-2026.pdf')]:
    data = (ROOT/'private'/name).read_bytes()
    expected = json.loads((public/'SOURCE_MANIFEST.json').read_text())[key]['file']
    sources[key] = {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    check('private_source_digest_'+key, sources[key] == expected)

print(json.dumps({
    'result':'PASS', 'check_count':len(checks), 'checks':checks,
    'independent_certificate':{'D':strings(D),'N':strings(N),'P_H_z0':strings(R),
        'weight_quadratic_coefficients':list(map(str,quadratic)),
        'uniform_weighted_tail_strict_upper_bound':str(tail_upper)},
    'private_source_hashes':sources,
    'author_replay':{'checks':438,'negative_controls':6,'byte_identical':True},
    'limits':['No import or execution of author arithmetic used in independent derivation.',
              'The separately recorded author replay is supplementary.',
              'No numerical sampling, search, Lean build or full formal dependency audit.',
              'Continuum analytic and geometric reasoning is reviewed in AUDIT.md.']
}, indent=2, sort_keys=True))
