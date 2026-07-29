#!/usr/bin/env python3
"""Exact checks for agent_n3_triple_skew_reduction.md.

Only Python's standard library and rational arithmetic are used.  Square
roots are cleared throughout by using E_p=sqrt(2) A_p.
"""

from fractions import Fraction as F
from itertools import product


def zero(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    out = zero(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [
        [
            sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def matvec(a, x):
    return [
        sum((a[i][j] * x[j] for j in range(len(x))), F(0))
        for i in range(len(a))
    ]


def kron(a, b):
    return [
        [
            a[i // len(b)][j // len(b[0])]
            * b[i % len(b)][j % len(b[0])]
            for j in range(len(a[0]) * len(b[0]))
        ]
        for i in range(len(a) * len(b))
    ]


def add(a, b, scale=F(1)):
    return [
        [a[i][j] + scale * b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def scale(c, a):
    return [[c * value for value in row] for row in a]


def hs2(a):
    return sum((value * value for row in a for value in row), F(0))


# Integer skew basis E_p=sqrt(2) A_p.
E = [
    [[0, 0, 0], [0, 0, 1], [0, -1, 0]],
    [[0, 0, -1], [0, 0, 0], [1, 0, 0]],
    [[0, 1, 0], [-1, 0, 0], [0, 0, 0]],
]
E = [[[F(x) for x in row] for row in matrix] for matrix in E]
I3 = eye(3)


# Check 2 A_p^dagger A_s = delta_ps I-|s><p| after clearing roots:
# E_p^T E_s = delta_ps I-|s><p|.
for p, s in product(range(3), repeat=2):
    lhs = matmul(transpose(E[p]), E[s])
    rhs = scale(F(int(p == s)), I3)
    rhs[s][p] -= 1
    assert lhs == rhs


# Check sum A_p tensor A_p=(3P_Phi-F)/2.  After multiplying by two,
# the left side is sum E_p tensor E_p.
pairs = list(product(range(3), repeat=2))
K2 = zero(9, 9)
for p in range(3):
    K2 = add(K2, kron(E[p], E[p]))

rhs = zero(9, 9)
for row, (a, b) in enumerate(pairs):
    for col, (c, d) in enumerate(pairs):
        # 3P_Phi has entry one exactly at |aa><cc|.
        rhs[row][col] += F(int(a == b and c == d))
        # Flip has |a,b><b,a|.
        rhs[row][col] -= F(int(a == d and b == c))
assert K2 == rhs


# Exact eigen-decomposition of K=sum A_p tensor A_p=K2/2:
# eigenvalue 1 on Phi, -1/2 on symmetric Phi-perp, +1/2 on skew.
phi = [F(int(a == b)) for a, b in pairs]
skew01 = [F(int((a, b) == (0, 1)) - int((a, b) == (1, 0)))
          for a, b in pairs]
sym01 = [F(int((a, b) == (0, 1)) + int((a, b) == (1, 0)))
         for a, b in pairs]
assert matvec(K2, phi) == [2 * x for x in phi]
assert matvec(K2, skew01) == skew01
assert matvec(K2, sym01) == [-x for x in sym01]
assert hs2(K2) == F(12)  # ||K||_2^2=12/4=3.


# Check the full marginal identity (4) on a nonsymmetric exact tensor.
# Since E_p=sqrt(2)A_p, D_E=2sqrt(2)D_A and hence
# D_E^T D_E=8D_A^dagger D_A.
triples = list(product(range(3), repeat=3))
t = {
    (0, 0, 0): F(1),
    (1, 1, 0): F(2),
    (2, 0, 1): F(-1),
    (0, 2, 2): F(3),
}
D_E = zero(27, 27)
for word, coefficient in t.items():
    local = kron(kron(E[word[0]], E[word[1]]), E[word[2]])
    D_E = add(D_E, local, coefficient)
lhs_marginal = matmul(transpose(D_E), D_E)


def rho_reduced(kept, row_values, col_values):
    """Entry of the unnormalized reduced density of |t><t|."""
    total = F(0)
    missing = [site for site in range(3) if site not in kept]
    for tail in product(range(3), repeat=len(missing)):
        row = [0, 0, 0]
        col = [0, 0, 0]
        for pos, site in enumerate(kept):
            row[site] = row_values[pos]
            col[site] = col_values[pos]
        for pos, site in enumerate(missing):
            row[site] = tail[pos]
            col[site] = tail[pos]
        total += t.get(tuple(row), F(0)) * t.get(tuple(col), F(0))
    return total


norm_t = sum((value * value for value in t.values()), F(0))
rhs_marginal = zero(27, 27)
for row_index, row in enumerate(triples):
    for col_index, col in enumerate(triples):
        value = norm_t * F(int(row == col))
        for site in range(3):
            other = [j for j in range(3) if j != site]
            delta = int(all(row[j] == col[j] for j in other))
            value -= delta * rho_reduced(
                (site,), (row[site],), (col[site],)
            )
        for kept in ((0, 1), (0, 2), (1, 2)):
            missing = next(j for j in range(3) if j not in kept)
            delta = int(row[missing] == col[missing])
            value += delta * rho_reduced(
                kept,
                tuple(row[j] for j in kept),
                tuple(col[j] for j in kept),
            )
        value -= t.get(row, F(0)) * t.get(col, F(0))
        rhs_marginal[row_index][col_index] = value
assert lhs_marginal == rhs_marginal


# Equality tensor D=(1/sqrt(3)) K tensor A_0.
# Its Hilbert--Schmidt norm squared is (1/3)*3*1=1.
# Its operator norm squared is (1/3)*1*(1/2)=1/6.
assert F(1, 3) * F(3) * F(1) == F(1)
assert F(1, 3) * F(1) * F(1, 2) == F(1, 6)


# Cross-marginal equality for
# t=Phi_AB tensor |0>, x=Phi_AB tensor |2>.
a = [F(1, 3), F(1, 3), F(0)]
b = [F(1), F(0), F(0)]
c = F(0)
assert sum(b, F(0)) == F(1, 3) + sum(a, F(0)) + c


# The double-skew normalized equality matrix B=K/sqrt(3) has squared
# singular values 1/3 and 1/12 eight times.
squares = [F(1, 3)] + [F(1, 12)] * 8
assert sum(squares, F(0)) == F(1)
assert sum(squares[:2], F(0)) == F(5, 12)
assert F(1, 3) - F(5, 12) == F(-1, 12)


# Exact algebra in the refined qutrit sign-frame lemma.
# At the worst shape a=b, g=2sqrt(3)-3 and g^2<1/3 is equivalent
# to 62/3<12sqrt(3), whose squared integer form is 3844<3888.
assert 3844 < 3888

# If h denotes g^2 and q is the density weight on the middle
# eigenvector, the purity lower bound is q^2+(1-q)^2/2.  The
# coefficients of
# 2/3*(1+purity_lower)-[1-(1-h)q]
# are 0 +(1/3-h)q +q^2.
constant = F(2, 3) * (1 + F(1, 2)) - 1
linear_without_h = F(2, 3) * (-1) + 1
quadratic = F(2, 3) * F(3, 2)
assert constant == 0
assert linear_without_h == F(1, 3)
assert quadratic == 1

# Global counting in the six Pauli permutations:
# each site-axis pair occurs twice, while the local purity floor on
# the other two qutrits contributes 2/3.
other_purity_floor = 2 * F(1, 3)
assert (
    F(2, 9) + F(2, 3) * other_purity_floor
    == F(2, 3)
)
number_of_permutations = 6
multiplicity_of_site_axis_pair = 2
assert (
    number_of_permutations * F(2, 9) / (2 * multiplicity_of_site_axis_pair)
    == F(1, 3)
)


# Equality-locus joint compensation.  At
# eta_1=eta_2=eta_12=1/3, Q_(2)=a I+b A_L and Q_(3)=c A_L.
eta = F(1, 3)
a_scalar = F(4, 9) * eta
b_two = F(4, 9) * (eta + eta)
c_three = F(8, 9) * eta
q2_takagi = [a_scalar + b_two] + [a_scalar] * 3
qtotal_takagi = [a_scalar + b_two + c_three] + [a_scalar] * 3
assert q2_takagi == [F(4, 9)] + [F(4, 27)] * 3
assert q2_takagi[0] - sum(q2_takagi[1:], F(0)) == 0
assert qtotal_takagi == [F(20, 27)] + [F(4, 27)] * 3
assert qtotal_takagi[0] - sum(qtotal_takagi[1:], F(0)) == F(8, 27)
assert F(2, 9) * (1 - eta - eta) == F(2, 27)


# Arithmetic of the surviving concurrence implication.
assert F(8, 9) * 2 * F(1, 6) == F(8, 27)
assert F(8, 27) > F(2, 9)


# Exact stable-rank deficit counting.  If delta=P+1/3-G, then the
# six frame deficits sum to 4 delta, while 1/6-c=delta/8.
delta = F(7, 60)
stable_deficit = delta / 8
sum_frame_deficits = 4 * delta
assert stable_deficit == sum_frame_deficits / 32
assert F(1, 6) - stable_deficit == (
    1 + (F(37, 30) + F(1, 3) - delta) - F(37, 30)
) / 8


# A rational audit of the lossless per-frame gap decomposition
# R-s=sum_i w_i[(R-r_i)+(r_i-e_i)]+variance/s.
p_frame = [F(1, 2), F(2, 5), F(1, 3)]
z2_frame = [F(1, 5), F(1, 4), F(1, 6)]
e_frame = [F(9, 10), F(4, 5), F(4, 5)]
s_frame = sum(z2_frame, F(0))
r_frame = [F(2, 3) * (1 + p) for p in p_frame]
R_frame = F(2, 9) + F(2, 3) * sum(p_frame, F(0))
w_frame = [z2 / s_frame for z2 in z2_frame]
variance_frame = (
    sum((z2 * e for z2, e in zip(z2_frame, e_frame)), F(0))
    - s_frame * s_frame
)
rhs_frame = sum(
    (
        w
        * ((R_frame - r) + (r - e))
        for w, r, e in zip(w_frame, r_frame, e_frame)
    ),
    F(0),
) + variance_frame / s_frame
assert variance_frame >= 0
assert all(R_frame - r >= 0 for r in r_frame)
assert all(r - e >= 0 for r, e in zip(r_frame, e_frame))
assert R_frame - s_frame == rhs_frame


# Exact local-frame gap formula (S4).
p_local = F(1, 2)
q_local = F(1, 4)
g2_local = F(1, 9)
r_local = F(2, 3) * (1 + p_local)
e_local = 1 - (1 - g2_local) * q_local
purity_residual = (
    p_local - q_local * q_local - (1 - q_local) ** 2 / 2
)
local_gap_sos = (
    F(2, 3) * purity_residual
    + q_local * (q_local + F(1, 3) - g2_local)
)
assert purity_residual >= 0
assert q_local + F(1, 3) - g2_local >= 0
assert r_local - e_local == local_gap_sos


# Takagi deficit splitting (S5), in the positive-concurrence regime.
op2 = F(3, 20)
det_compression = F(7, 50)
residual_takagi = F(1, 50)
triple_concurrence = F(16, 9) * det_compression - residual_takagi
assert triple_concurrence > 0
assert F(8, 27) - triple_concurrence == (
    F(16, 9)
    * ((F(1, 6) - op2) + (op2 - det_compression))
    + residual_takagi
)


# Quantitative corrected-floor compensation on the common-factor
# chart.  The extremal arithmetic gamma=3 tau_i makes the lower
# bound m >= C(Q3)-2/9 sharp.
tau1 = F(1, 6)
tau2 = F(1, 6)
gamma_overlap = F(1, 2)
assert gamma_overlap <= 3 * tau1
assert gamma_overlap <= 3 * tau2
eta12 = (1 - tau1 - tau2 + gamma_overlap) / 4
floor_margin = (tau1 + tau2) / 9
common_chart_c3 = F(8, 9) * eta12
assert floor_margin == common_chart_c3 - F(2, 9)
assert floor_margin >= 0

print("triple-skew reduction checks: exact")
