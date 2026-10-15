#!/usr/bin/env python3
"""Exact post-seal adversarial controls, distinct from the submitted controls.

These finite symbolic controls falsify potential mistakes in the universal proof;
they are not the proof of the original universal statement or its priority.
Run with existing /usr/bin/python3 and SymPy 1.14.0. No numerical tolerances.
"""
from pathlib import Path
import itertools
import json
import hashlib
import sympy as s

n = 6
x = s.symbols('x0:6')
zero = dict.fromkeys(x, 0)
checks = {}


def check(label, condition):
    assert bool(condition), label
    checks[label] = 'PASS'


triples = list(itertools.product(range(n), repeat=3))


def tensor(f):
    return {ijk: s.diff(f, *(x[j] for j in ijk)) for ijk in triples}


def trace(a):
    return [sum(a[(j, j, k)] for j in range(n)) for k in range(n)]


def dot(a, b):
    return sum(a[q] * b[q] for q in triples)


def qform(a, b):
    return dot(a, b) - sum(u*v for u, v in zip(trace(a), trace(b)))


# All 56 homogeneous cubic monomials, not merely harmonic examples.
groups = [[x[i]**3] + [x[i]*x[j]**2 for j in range(n) if j != i]
          for i in range(n)]
distinct = [x[i]*x[j]*x[k] for i, j, k in itertools.combinations(range(n), 3)]
basis = sum(groups, []) + distinct
check('full_symmetric_cubic_dimension', len(basis) == 56 and len(set(basis)) == 56)
tensors = [tensor(f) for f in basis]
gram = s.Matrix(56, 56, lambda i, j: qform(tensors[i], tensors[j]))
lam = s.symbols('lam')
for i in range(n):
    b = gram[6*i:6*i+6, 6*i:6*i+6]
    check(f'block_{i}_characteristic_polynomial',
          s.expand(b.charpoly(lam).as_expr() - (lam-12)**4*(lam**2+8*lam-720)) == 0)
for i in range(56):
    for j in range(56):
        if i < 36 and j < 36:
            expected = (0 if i == j and i % 6 == 0 else
                        8 if i == j else
                        -12 if i//6 == j//6 and (i % 6 == 0 or j % 6 == 0) else
                        -4 if i//6 == j//6 else 0)
        else:
            expected = 6 if i == j else 0
        check(f'gram_entry_{i}_{j}', gram[i, j] == expected)
check('gram_nondegenerate', gram.det() == (-720*12**4)**6 * 6**20)
# Each six-dimensional block has four positive 12 eigenvalues and one root of
# each sign of lam^2+8lam-720; the remaining twenty eigenvalues are 6.
check('exact_inertia_positive_50_negative_6',
      6*(4+1)+20 == 50 and 6*1 == 6 and -720 < 0)

# Orthogonal trace projection for every basis tensor. This also challenges the
# invalid shortcut that every cubic would have the harmonic positive witness.
for aidx, a in enumerate(tensors):
    tau = trace(a)
    v = [z/s.Integer(n+2) for z in tau]
    p = {q: sum(v[q[h]] if q[(h+1) % 3] == q[(h+2) % 3] else 0
                for h in range(3)) for q in triples}
    h = {q: a[q]-p[q] for q in triples}
    check(f'projection_{aidx}_harmonic', all(z == 0 for z in trace(h)))
    check(f'projection_{aidx}_orthogonal', dot(h, p) == 0)
    check(f'projection_{aidx}_norm',
          s.simplify(dot(p, p) - 3*s.Integer(n+2)*sum(z*z for z in v)) == 0)
    check(f'projection_{aidx}_q_split',
          s.simplify(qform(a, a) - dot(h, h)
                     - s.Integer(n+2)*(1-n)*sum(z*z for z in v)) == 0)

selected = [
    ('harmonic_submitted', x[0]*x[1]*x[2], x[0]*x[1]*x[2], 24),
    ('nonharmonic_positive', x[0]**2*x[1], x[0]**2*x[1], 32),
    ('nonharmonic_zero', x[0]**3, x[0]**3, 0),
    ('nonharmonic_cross_negative', x[0]**3, x[0]*x[1]**2, -48),
    ('pure_trace_negative', x[0]*sum(z*z for z in x),
     x[0]*sum(z*z for z in x), -640),
    ('independent_harmonic_direction', x[0]*x[1]*x[2], x[0]*x[1]*x[3], 0),
]
jet_values = {}
for label, f, psi, expected in selected:
    a, b = tensor(f), tensor(psi)
    direct = 4*dot(a, b)
    adjoint = 4*sum(u*v for u, v in zip(trace(a), trace(b)))
    check(label+'_tensor_defect', direct-adjoint == expected)
    jet_values[label] = {'linearization': int(direct), 'adjoint': int(adjoint),
                         'defect': int(direct-adjoint)}

# Full coordinate Frechet derivatives and adjoints on nonharmonic and mixed
# lower-jet backgrounds, using six tensor components and three active variables.
z = x[:3]
vfun = s.Function('v')(*z)
t = s.symbols('t')


def grad(u):
    return [s.diff(u, w) for w in z]


def lap(u):
    return sum(s.diff(u, w, 2) for w in z)


def schouten(u):
    du = grad(u)+[s.S.Zero]*3
    norm = sum(w*w for w in du)
    return s.Matrix(6, 6, lambda i, j:
                    -(s.diff(u, z[i], z[j]) if i < 3 and j < 3 else 0)
                    + du[i]*du[j] - (norm/2 if i == j else 0))


def C(u):
    return s.expand(sum(a*a for a in schouten(u)))


def div_density(u, c):
    return s.expand(lap(c)-4*sum(a*b for a, b in zip(grad(u), grad(c)))-4*c*lap(u))


def coefficients(d):
    atoms = sorted(d.atoms(s.Derivative), key=str)+[vfun]
    dummy = s.symbols('j:'+str(len(atoms)))
    poly = s.Poly(d.xreplace(dict(zip(atoms, dummy))), *dummy)
    assert poly.total_degree() <= 1
    return {atom: s.expand(poly.coeff_monomial(j)) for atom, j in zip(atoms, dummy)}


def apply(coeff, psi, adjoint=False):
    result = s.S.Zero
    for atom, a in coeff.items():
        variables = atom.variables if isinstance(atom, s.Derivative) else ()
        if adjoint:
            term = a*psi
            for w in variables:
                term = -s.diff(term, w)
        else:
            term = a*(s.diff(psi, *variables) if variables else psi)
        result += term
    return s.expand(result)


for label, f, psi, expected in selected[:4]:
    d = s.expand(s.diff(div_density(f+t*vfun, C(f+t*vfun)), t).subs(t, 0))
    coeff = coefficients(d)
    direct = apply(coeff, psi).subs(zero)
    adjoint = apply(coeff, psi, True).subs(zero)
    check(label+'_full_coordinate_derivative', direct == jet_values[label]['linearization'])
    check(label+'_full_coordinate_adjoint', adjoint == jet_values[label]['adjoint'])
    check(label+'_full_coordinate_defect', direct-adjoint == expected)

# At an arbitrary polynomial background with nonzero lower jets, verify the
# operator itself, not only its value at a specially flat point.
f = z[0]+z[1]**2+z[0]*z[1]*z[2]
p = schouten(f)
df = grad(f)
trp = s.trace(p)
delta_c = s.expand(-2*sum(p[i, j]*s.diff(vfun, z[i], z[j])
                          for i in range(3) for j in range(3))
                   +4*sum(p[i, j]*df[i]*s.diff(vfun, z[j])
                           for i in range(3) for j in range(3))
                   -2*trp*sum(a*b for a, b in zip(df, grad(vfun))))
dc_direct = s.expand(s.diff(C(f+t*vfun), t).subs(t, 0))
check('full_nonflat_background_delta_C', s.expand(delta_c-dc_direct) == 0)
d = s.expand(s.diff(div_density(f+t*vfun, C(f+t*vfun)), t).subs(t, 0))
# Delta_g(Tv)dV = -(1/2) div_0(grad(delta_C)-4 delta_C grad f).
metric_formula = s.expand(-4*sum(s.diff(C(f)*s.diff(vfun, w), w) for w in z)
                         +sum(s.diff(s.diff(delta_c, w)-4*delta_c*s.diff(f, w), w)
                              for w in z))
check('full_nonflat_background_density_operator', s.expand(d-metric_formula) == 0)

# Independent Euler-Lagrange check for the asserted local primitive and then
# exact symmetry of its full density linearization at the same nonflat metric.
def U(u):
    return -lap(u)-2*sum(w*w for w in grad(u))


F = -U(f+t*vfun)**3/s.Integer(3)
variation = s.expand(s.diff(F, t).subs(t, 0))
euler = apply(coefficients(variation), s.S.One, True)
jdensity = div_density(f, s.expand(U(f)**2))
check('Delta_J_squared_local_primitive_full_background', s.expand(euler-jdensity) == 0)
dj = s.expand(s.diff(div_density(f+t*vfun, s.expand(U(f+t*vfun)**2)), t).subs(t, 0))
cj = coefficients(dj)
check('Delta_J_squared_density_linearization_self_adjoint',
      s.expand(apply(cj, vfun)-apply(cj, vfun, True)) == 0)

result = {'status': 'PASS', 'exact_assertions': len(checks), 'failed': 0,
          'sympy_version': s.__version__, 'cubic_basis_size': 56,
          'cubic_defect_inertia': {'positive': 50, 'negative': 6, 'zero': 0},
          'jet_values': jet_values,
          'operator_identity_checked_at_nonzero_lower_jets': True,
          'J_squared_primitive_and_full_operator_symmetry_checked': True,
          'checks': checks,
          'scope': 'Exact finite falsification controls; universal proof is separately reconstructed.',
          'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('FRESH_CONTROL_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))
