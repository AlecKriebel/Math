"""Adversarial exact checks; builds literal reactions and imports no project code."""
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
import json
import sympy as S

Q = S.Rational
lam, s = S.symbols('lambda s')
OUT = Path(__file__).resolve().parent
result = {'target': '953c836a12b9d9d474521feb4a96e218c1155203',
          'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'checks': {}}


def require(value, label):
    if not value:
        raise RuntimeError(label)


def reaction_matrix(m, a, b):
    n = m + 1
    def complex_(entries):
        x = S.zeros(n, 1)
        for i, v in entries.items():
            x[i] = v
        return x
    pairs = [(complex_({}), complex_({0: 1}))]
    for i in range(1, m - 2):
        pairs.append((complex_({0: 1, i: 1}), complex_({0: 1, i + 1: 1})))
    pairs += [(complex_({0: 1, m - 2: 1}), complex_({m - 1: 2})),
              (complex_({m - 1: 2}), complex_({1: 1})),
              (complex_({m: 2}), complex_({0: 1, m - 1: 1})),
              (complex_({0: 1, m - 1: 1}), complex_({m: 2}))]
    require(all(sum(y) <= 2 and sum(z) <= 2 for y, z in pairs), 'binary complexes')
    Y = S.Matrix.hstack(*(y for y, _ in pairs))
    G = S.Matrix.hstack(*(z-y for y, z in pairs))
    flux = S.Matrix([a] * m + [b, b])
    c = S.Matrix([0] + [4] * (m-2) + [2, 1])
    require(G * flux == S.zeros(n, 1), 'positive flux balance')
    require(c.T * G == S.zeros(1, m+2), 'conservation')
    require(G.rank() == m, 'stoichiometric rank')
    return G * S.diag(*flux) * Y.T, c


def hurwitz_gaps(M):
    coeff = M.charpoly(lam).all_coeffs()
    degree = M.rows
    # Classical Hurwitz matrix, independently from principal-block arguments.
    H = S.Matrix(degree, degree,
                 lambda i,j: coeff[2*j-i+1] if 0 <= 2*j-i+1 <= degree else 0)
    return [H[:k, :k].det() for k in range(1, degree+1)]


count = 0
gap_count = 0
for m in range(3, 8):
    for a, b in ((Q(2,3), Q(5,7)), (Q(3,5), Q(6,5))):
        A, _ = reaction_matrix(m, a, b)
        h = [Q(i+1, i+2) if i % 2 else Q((i+2)**2, i+1) for i in range(m+1)]
        J = A * S.diag(*h)
        for size in range(1, m):
            for I in combinations(range(m+1), size):
                gaps = hurwitz_gaps(J.extract(I, I))
                require(all(g > 0 for g in gaps), f'principal Hurwitz m={m},I={I},a={a},b={b}')
                count += 1
                gap_count += len(gaps)
result['checks']['direct_principal_hurwitz'] = {'matrices': count,
    'strict_exact_Hurwitz_determinants': gap_count, 'm': [3,4,5,6,7],
    'flux_pairs': [['2/3','5/7'], ['3/5','6/5']],
    'mechanism': 'exact characteristic polynomial and every Hurwitz determinant; no SCC import'}
print('Exact principal-block Hurwitz checks:', count, flush=True)

omissions = 0
boundary = []
for m in range(3, 13):
    a, b = Q(7,5), Q(2,3)
    A, c = reaction_matrix(m, a, b)
    h = [Q(i+2, i+1) for i in range(m+1)]
    J = A * S.diag(*h)
    for omit in range(m+1):
        I = [i for i in range(m+1) if i != omit]
        observed = (-1)**m * J.extract(I,I).det()
        if omit == m:
            expected = -2*a**(m-1)*b*S.prod(h[:m])
        elif 1 <= omit <= m-2:
            expected = 16*a**(m-1)*b*h[m]*S.prod(h[i] for i in range(m) if i != omit)
        else:
            expected = S.Integer(0)
        require(observed == expected, f'omission m={m}, omit={omit}')
        omissions += 1
    for T in [Q(1,2), S.Integer(1), S.Integer(2)]:
        # hZ=1 and h_i=8*(m-2)/T makes the exact boundary parameter T(H)=T.
        h0 = [S.Integer(1)] + [8*(m-2)/T]*(m-2) + [S.Integer(1)]*2
        J0 = A * S.diag(*h0)
        cp = S.Poly(J0.charpoly(lam).as_expr(), lam)
        zero_order = min(monom[0] for monom, coeff in cp.terms() if coeff)
        require(J0.rank() == m, 'boundary geometric multiplicity one')
        require(zero_order == (2 if T == 1 else 1), 'boundary algebraic multiplicity')
        require(S.sign(cp.nth(1)) == S.sign(T-1), 'boundary linear coefficient sign')
        require(all(cp.nth(k) > 0 for k in range(2, m+2)), 'boundary all higher coefficients positive')
        boundary.append({'m': m, 'T': str(T), 'zero_multiplicity': zero_order})
result['checks']['exact_omission_identities'] = omissions
result['checks']['conservation_boundary_cases'] = boundary
print('Exact omission and conservation-boundary checks:', omissions, len(boundary), flush=True)

J2 = S.Matrix([[1, -1], [2, -2]])
n2 = []
for ds in [(1,4),(1,2),(2,1)]:
    D = S.diag(*ds)
    chi = (lam*S.eye(2)+s*D-J2).det().expand()
    beta1 = chi.subs(lam,0).expand().coeff(s,1)
    require(S.expand(S.diff(chi,lam) - (2*lam+s*sum(ds)+1)) == 0, 'n=2 positive spectral derivative')
    n2.append({'D': ds, 'characteristic': str(chi), 'beta1': str(beta1),
               'positive_threshold': str(-beta1/S.prod(ds)) if beta1 < 0 else None})
result['checks']['n2_three_signs'] = n2

# A valid general-theorem matrix that is homogeneously wave-unstable.  This
# explicitly tests that neither positive real eigenvalues nor beta1 alone
# should be mistaken for a full Hurwitz certificate.
J4 = -S.eye(4)
J4[1,0] = J4[2,1] = J4[3,2] = 1
J4[0,3] = 31
J4[2,0] = J4[3,1] = Q(-15,31)
require(J4.det() == 0, 'wave-scope determinant zero')
aminors = {}
for size in range(1,4):
    aminors[size] = [(-1)**size*J4.extract(I,I).det()
                     for I in combinations(range(4),size)]
require(all(x > 0 for size in [1,2] for x in aminors[size]), 'wave-scope lower minors')
require(sum(aminors[3]) > 0, 'wave-scope omission sum')
cp4 = J4.charpoly(lam).as_expr().factor()
q4 = S.cancel(cp4 / lam)
require(q4 == lam**3+4*lam**2+6*lam+34, 'wave-scope cubic')
qshift = S.Poly(q4.subs(lam,lam+Q(1,10)),lam)
_, ca, cb, cc = qshift.all_coeffs()
require(ca > 0 and cb > 0 and cc > 0 and ca*cb-cc < 0, 'wave pair after positive damping')
result['checks']['general_theorem_wave_scope'] = {'J': [[str(x) for x in row] for row in J4.tolist()],
    'signed_minors': {str(k): [str(x) for x in v] for k,v in aminors.items()},
    'characteristic': str(cp4), 'D': 'I_4', 's': '1/10',
    'shifted_cubic': str(qshift.as_expr()), 'shifted_Routh_gap': str(ca*cb-cc),
    'interpretation': 'Valid theorem hypotheses, positive beta1, no positive real eigenvalue, but nonreal unstable pair. Confirms stated limitation.'}
print('n=2 sign cases and exact nonreal-instability scope witness: PASS', flush=True)

contrast_cases = 0
for nu in [1,2,3,4,10,97,997,10007]:
    kappa = 1/S.sqrt(3) if nu == 1 else S.sqrt(5)/2
    L0, L1 = kappa/S.sqrt(nu), Q(90*nu,90*nu+1)
    require(L0 < L1, 'nonempty L interval')
    for L in [L0, (L0+L1)/2, L1]:
        m = nu+2
        # Monotonic K means only the two interior endpoints can be extrema.
        h_first = (91*nu-1)/(91*nu*L)
        h_last = 90*nu/((90*nu+1)*L)
        d_first = 1/(91*nu*L)
        d_last = 1/((90*nu+1)*L)
        require(S.simplify(h_first-h_last) >= 0 and S.simplify(h_last-1) >= 0, 'H extrema')
        require(S.simplify(d_last-d_first) >= 0, 'D interior ordering')
        require(S.simplify(Q(1,7)-d_last) > 0, 'interior D below all boundary D')
        chiD, chiH = Q(23,63)/d_first, h_first
        require(S.simplify(chiD*chiH-Q(23,63)*(91*nu-1)) == 0, 'contrast product')
        require(S.simplify(chiD-chiH) > 0, 'diffusion contrast dominates')
        require(S.simplify(chiD*chiH-8*nu) > 0, 'strict universal bound respected')
        contrast_cases += 1
result['checks']['contrast_extrema_cases'] = contrast_cases
result['status'] = 'PASS'
(OUT/'EXACT_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
print('Contrast endpoint/interior cases:', contrast_cases, flush=True)
print('PASS', flush=True)
