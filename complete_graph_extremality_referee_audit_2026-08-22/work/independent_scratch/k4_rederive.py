"""Independent symbolic reconstruction of the two weighted-K4 families.

No delivered implementation is imported or executed.  Orbit transitions are
generated directly from death--Birth competition in two vertex classes.
"""

import sympy as sp


r, x, y = sp.symbols("r x y")


def transitions(p, q, alpha, beta, gamma, i, j):
    """Return state-changing (new_count, probability) pairs."""
    n = p + q
    out = []
    if i < p:
        mutant = i * alpha + j * gamma
        resident = (p - i - 1) * alpha + (q - j) * gamma
        probability = sp.cancel(sp.Rational(p - i, n) * r * mutant / (r * mutant + resident))
        if probability != 0:
            out.append(((i + 1, j), probability))
    if i > 0:
        mutant = (i - 1) * alpha + j * gamma
        resident = (p - i) * alpha + (q - j) * gamma
        probability = sp.cancel(sp.Rational(i, n) * resident / (r * mutant + resident))
        if probability != 0:
            out.append(((i - 1, j), probability))
    if j < q:
        mutant = j * beta + i * gamma
        resident = (q - j - 1) * beta + (p - i) * gamma
        probability = sp.cancel(sp.Rational(q - j, n) * r * mutant / (r * mutant + resident))
        if probability != 0:
            out.append(((i, j + 1), probability))
    if j > 0:
        mutant = (j - 1) * beta + i * gamma
        resident = (q - j) * beta + (p - i) * gamma
        probability = sp.cancel(sp.Rational(j, n) * resident / (r * mutant + resident))
        if probability != 0:
            out.append(((i, j - 1), probability))
    return out


def build_lumped_system(p, q, alpha, beta, gamma):
    states = [(i, j) for i in range(p + 1) for j in range(q + 1)
              if (i, j) not in ((0, 0), (p, q))]
    index = {state: z for z, state in enumerate(states)}
    M = sp.zeros(len(states))
    rhs = sp.zeros(len(states), 1)
    row_sums = []
    for state in states:
        row = index[state]
        change = transitions(p, q, alpha, beta, gamma, *state)
        total = sp.cancel(sum(probability for _, probability in change))
        row_sums.append(total)
        M[row, row] = total
        for new, probability in change:
            if new == (p, q):
                rhs[row] += probability
            elif new != (0, 0):
                M[row, index[new]] -= probability
    Dinv = sp.diag(*[1 / total for total in row_sums])
    return states, M, rhs, sp.simplify(Dinv * M), sp.simplify(Dinv * rhs)


def fixation_from_system(p, q, states, M, rhs):
    solution = M.inv(method="DM") * rhs
    index = {state: z for z, state in enumerate(states)}
    rho = sp.cancel(
        (p * solution[index[(1, 0)]] + q * solution[index[(0, 1)]]) / (p + q)
    )
    return solution, rho


baseline = 3 * r**2 / (4 * (r**2 + r + 1))


# 1+3 family.
states13, M13, rhs13, M13_cond, rhs13_cond = build_lumped_system(1, 3, 0, x, 1)
print("k4_13_matrix_built", flush=True)
solution13, rho13 = fixation_from_system(1, 3, states13, M13, rhs13)
delta13 = sp.cancel(rho13 - baseline)
F13 = (
    2*r**4*x**2 + 2*r**4*x + 11*r**3*x**2 + 14*r**3*x + 3*r**3
    + 21*r**2*x**2 + 29*r**2*x + 12*r**2
    + 16*r*x**2 + 22*r*x + 8*r + 4*x**2 + 5*x + 1
)
P13 = (
    8*x**2*(x+1)*(r**6+1)
    + (6*x**4+36*x**3+46*x**2+16*x)*(r**5+r)
    + (27*x**4+73*x**3+85*x**2+59*x+12)*(r**4+r**2)
    + (42*x**4+90*x**3+106*x**2+66*x+24)*r**3
)
assert sp.cancel(
    delta13 + 3*r**2*(r-1)*(x-1)**2*F13 /
    (4*(r**2+r+1)*P13)
) == 0
print("k4_13_identity=PASS", flush=True)


# 2+2 family.  Determine which natural holding-free convention realizes the
# stated determinant certificate by its independently checkable signature:
# P22 = 128 L22 det(M22), a polynomial with 123 positive integer monomials.
states22, M22_raw, rhs22_raw, M22_cond, rhs22_cond = build_lumped_system(2, 2, x, y, 1)
print("k4_22_matrix_built", flush=True)
L22 = (
    (2*r+x)*(2*r+y)*(r*x+2)*(r*y+2)*(r+x+1)*(r+y+1)
    *(r*x+r+1)*(r*y+r+1)
)

det_raw = sp.cancel(M22_raw.det(method="domain-ge"))
det_cond = sp.cancel(M22_cond.det(method="domain-ge"))
candidates = {
    "raw": sp.cancel(128 * L22 * det_raw),
    "conditional": sp.cancel(128 * L22 * det_cond),
}
P22 = None
matrix22 = None
rhs22 = None
for name, candidate in candidates.items():
    if sp.denom(candidate) != 1:
        print(f"k4_22_{name}_candidate=nonpolynomial", flush=True)
        continue
    poly = sp.Poly(candidate, x, y, r)
    coeffs = poly.coeffs()
    signature = len(poly.terms()), all(c.is_Integer and c > 0 for c in coeffs)
    print(f"k4_22_{name}_candidate_signature={signature}", flush=True)
    if signature == (123, True):
        P22 = sp.expand(candidate)
        matrix22 = M22_raw if name == "raw" else M22_cond
        rhs22 = rhs22_raw if name == "raw" else rhs22_cond
        convention = name

assert P22 is not None
print(f"k4_22_determinant_convention={convention}", flush=True)

solution22, rho22 = fixation_from_system(2, 2, states22, matrix22, rhs22)
delta22 = sp.cancel(rho22 - baseline)
H22 = sp.cancel(
    -delta22 * 4 * (r**2+r+1) * P22 / (r**2 * (r-1))
)
assert sp.denom(H22) == 1
assert sp.cancel(
    delta22 + r**2*(r-1)*H22 / (4*(r**2+r+1)*P22)
) == 0
assert sp.expand(H22 - H22.xreplace({x: y, y: x})) == 0
print("k4_22_rational_identity=PASS", flush=True)
print("k4_22_H_monomials=", len(sp.Poly(H22, x, y, r).terms()), flush=True)

# Convert symmetric H22(x,y,r) to elementary symmetric variables, then to the
# paper's g=sqrt(xy), d=(sqrt(x)-sqrt(y))^2, t=r-1 coordinates.
sym_expr, remainder, mapping = sp.symmetrize(H22, [x, y], formal=True)
assert remainder == 0
s_xy, p_xy = [item[0] for item in mapping]
g, d, t = sp.symbols("g d t")
H_gdt = sp.expand(sym_expr.subs({s_xy: d + 2*g, p_xy: g**2, r: t+1}))

R0 = (
    (2*g**2+2*g)*t**4 + (g**3+10*g**2+21*g+6)*t**3
    + (3*g**3+26*g**2+61*g+38)*t**2
    + (4*g**3+32*g**2+80*g+64)*t
    + 2*g**3+16*g**2+40*g+32
)
C0 = 2*t*(g-1)**2*(g+1)*(t+1)*R0
C1 = (
    2*(g**4+4*g**3-2*g**2+4*g+1)*t**6
    + (11*g**4+108*g**3+76*g**2+60*g+17)*t**5
    + 2*(40*g**4+288*g**3+393*g**2+176*g+19)*t**4
    + (16*g**5+331*g**4+1704*g**3+2766*g**2+1360*g+39)*t**3
    + 2*(28*g**5+337*g**4+1426*g**3+2399*g**2+1378*g+12)*t**2
    + 2*(g+2)*(32*g**4+263*g**3+722*g**2+661*g+2)*t
    + 24*g*(g+2)*(g+4)*(g**2+4*g+5)
)
C2 = (
    2*(g**2+1)*t**6 + 3*(9*g**2+26*g+5)*t**5
    + 2*(18*g**3+120*g**2+321*g+44)*t**4
    + 2*(2*g**4+105*g**3+525*g**2+1071*g+170)*t**3
    + (14*g**4+474*g**3+2201*g**2+3648*g+689)*t**2
    + 2*(8*g**4+240*g**3+1080*g**2+1587*g+331)*t
    + 6*(g**4+30*g**3+133*g**2+186*g+40)
)
C3 = (
    13*t**5 + (6*g**2+48*g+107)*t**4
    + (35*g**2+312*g+357)*t**3
    + (79*g**2+744*g+608)*t**2
    + (80*g**2+768*g+529)*t + 6*(5*g**2+48*g+31)
)
C4 = 6*t**4 + 39*t**3 + 93*t**2 + 96*t + 36
assert sp.expand(H_gdt - (C0+C1*d+C2*d**2+C3*d**3+C4*d**4)) == 0
assert sp.expand((g**4+4*g**3-2*g**2+4*g+1) - ((g**2-1)**2+4*g*(g**2+1))) == 0
print("k4_22_g_d_t_certificate=PASS", flush=True)

# Exact rational, independently generated full 14-state subset-chain checks.
def full_chain_rho(weights, fitness):
    vertices = range(4)
    states = [frozenset(v for v in vertices if mask & (1 << v))
              for mask in range(1, 15)]
    index = {S: z for z, S in enumerate(states)}
    Q = sp.zeros(14)
    bvec = sp.zeros(14, 1)
    for S in states:
        row = index[S]
        for target in vertices:
            mw = sum(weights[source, target] for source in S if source != target)
            rw = sum(weights[source, target] for source in vertices if source not in S and source != target)
            pm = sp.cancel(fitness*mw/(fitness*mw+rw))
            for mutant, probability in ((True, pm), (False, 1-pm)):
                new = set(S)
                (new.add if mutant else new.discard)(target)
                new = frozenset(new)
                prob = probability / 4
                if len(new) == 4:
                    bvec[row] += prob
                elif len(new) != 0:
                    Q[row, index[new]] += prob
    h = (sp.eye(14)-Q).inv() * bvec
    return sum(h[index[frozenset((i,))]] for i in vertices) / 4


for xv, yv, rv in ((sp.Rational(2), sp.Rational(5), sp.Rational(7, 3)),
                    (sp.Rational(1, 2), sp.Rational(3), sp.Rational(2))):
    weights22 = {}
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            if {i, j} == {0, 1}:
                weights22[i, j] = xv
            elif {i, j} == {2, 3}:
                weights22[i, j] = yv
            else:
                weights22[i, j] = sp.Rational(1)
    direct = full_chain_rho(weights22, rv)
    assert direct == rho22.subs({x: xv, y: yv, r: rv})

for xv, rv in ((sp.Rational(2), sp.Rational(7, 3)),
                (sp.Rational(1, 3), sp.Rational(2))):
    weights13 = {}
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            weights13[i, j] = xv if i != 0 and j != 0 else sp.Rational(1)
    direct = full_chain_rho(weights13, rv)
    assert direct == rho13.subs({x: xv, r: rv})

print("k4_full_subset_chain_crosschecks=PASS")

