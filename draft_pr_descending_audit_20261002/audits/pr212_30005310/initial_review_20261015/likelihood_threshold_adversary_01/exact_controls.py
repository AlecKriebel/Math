#!/usr/bin/env python3
"""Independent exact controls. Writes only exact_controls_results.json beside this file.

Analytic probability, convexity, and neighborhood arguments are in REPORT.md.
No floating-point ranks, optimizers, simulations, or external services are used.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as s

HERE = Path(__file__).parent
counts = Counter()
def check(label, condition):
    if not condition:
        raise AssertionError(label)
    counts[label] += 1

def stats(T, tied=False):
    diag = [T[i, i] for i in range(8)]
    return (([diag[0] + diag[1]] + diag[2:]) if tied else diag) + [
        T[i, j] for i in range(4) for j in range(4, 8)]

def in_model(T, tied=False):
    return (all(T[i, j] == 0 for part in (range(4), range(4, 8))
                for i in part for j in part if i != j)
            and (not tied or T[0, 0] == T[1, 1]))

# Reconstruct both linear concentration spaces and the off-diagonal factor 2.
sx = s.symbols('s0:36')
S = s.zeros(8)
p = 0
for i in range(8):
    for j in range(i, 8):
        S[i, j] = S[j, i] = sx[p]
        p += 1
kd = s.symbols('d0:8')
ke = s.symbols('e0:16')
K = s.diag(*kd)
for p, (i, j) in enumerate((i, j) for i in range(4) for j in range(4, 8)):
    K[i, j] = K[j, i] = ke[p]
check('singleton_trace_statistic_pairing', s.expand(s.trace(S*K) - sum(
    S[i, i]*kd[i] for i in range(8)) - 2*sum(S[i,j]*ke[4*i+j-4]
    for i in range(4) for j in range(4, 8))) == 0)
Kt = K.subs(kd[1], kd[0])
check('tied_trace_statistic_pairing', s.expand(s.trace(S*Kt)
    - (S[0,0]+S[1,1])*kd[0] - sum(S[i,i]*kd[i] for i in range(2,8))
    - 2*sum(S[i,j]*ke[4*i+j-4] for i in range(4) for j in range(4,8))) == 0)
check('identity_feasible_both_models', in_model(s.eye(8), True))

X = s.zeros(8, 2)
for i in range(4):
    X[i,0] = 1
    X[i+4,1] = 1
T = X*X.T
check('rank_two_witness', X.rank() == T.rank() == 2)
check('witness_is_diag_J4_J4', T == s.diag(s.ones(4), s.ones(4)))
for tied in (False, True):
    check('statistics_match_identity', stats(T,tied) == stats(s.eye(8),tied))
    check('positive_scatter_scaling_preserves_match',
          stats(T/2,tied) == stats(s.eye(8)/2,tied))

# An exactly rank-three preimage also defeats a hidden exact-rank restriction.
Z3 = s.zeros(8,3)
for i in range(4):
    Z3[i, 0 if i % 2 == 0 else 2] = 1
    Z3[i+4,1] = 1
check('exact_rank_three_preimage_of_PD_statistics',
      Z3.rank() == 3 and stats(Z3*Z3.T) == stats(s.eye(8))
      and stats(Z3*Z3.T,True) == stats(s.eye(8),True))

# A PD completion need not itself have a concentration matrix in the model.
P = s.eye(8)
P[0,1] = P[1,0] = s.Rational(1,4)
for k in range(1,9):
    check('arbitrary_matching_completion_PD', P[:k,:k].det() > 0)
check('arbitrary_PD_completion_matches_both_statistics',
      stats(P) == stats(T) and stats(P,True) == stats(T,True))
check('arbitrary_PD_completion_inverse_outside_model',
      P.inv()[0,1] == -s.Rational(4,15) and not in_model(P.inv())
      and not in_model(P.inv(),True))

eps = s.Rational(1,100)
diag_lower = (1-eps)**2
cross_upper = 2*eps*(1+eps)
margin = diag_lower-4*cross_upper
check('rational_diagonal_lower', diag_lower == s.Rational(9801,10000))
check('rational_cross_upper', cross_upper == s.Rational(202,10000))
check('rational_PD_margin', margin == s.Rational(8993,10000) and margin > 0)
corner_cross = []
corner_minor = []
for a,b,c,d in product((-eps,eps), repeat=4):
    corner_cross.append(abs((1+a)*c+b*(1+d)))
    corner_minor.append((1+a)*(1+d)-b*c)
check('cross_bound_all_multiaffine_extrema', max(corner_cross) == cross_upper)
check('rank_two_all_multiaffine_extrema', min(corner_minor) == 1-2*eps)
check('positive_sample_rank_two_minor', 1-2*eps == s.Rational(49,50) > 0)

# Boundary-aware one-sample obstruction, with every model equality checked.
xx = s.Matrix(s.symbols('x1:9'))
v = s.zeros(8,1)
v[2] = xx[4]
v[4] = -xx[2]
Omega1 = v*v.T
check('one_sample_ray_annihilates_all_data_symbolically', Omega1*xx == s.zeros(8,1))
check('one_sample_ray_obeys_all_tied_constraints', in_model(Omega1,True))
check('one_sample_ray_norm_nonzero_except_two_zero_entries',
      s.trace(Omega1) == xx[2]**2+xx[4]**2)
zero_case = s.zeros(8)
zero_case[2,2] = 1
check('both_endpoint_zero_ray_model_constraints', in_model(zero_case,True))
check('both_endpoint_zero_ray_annihilates',
      zero_case*xx.subs({xx[2]:0,xx[4]:0}) == s.zeros(8,1))
check('one_sample_principal_minor_identically_zero',
      s.det(s.Matrix([[xx[2]**2,xx[2]*xx[4]],
                      [xx[2]*xx[4],xx[4]**2]])) == 0)

# Additional exact data cases inside the entire analytically proved open box.
for q in range(1,9):
    Y = X.copy()
    for i in range(8):
        for j in range(2):
            Y[i,j] += s.Rational(((13*i+7*j+q)%17)-8,1000)
    YY = Y*Y.T
    M = s.diag(*[YY[i,i] for i in range(8)])
    for i in range(4):
        for j in range(4,8):
            M[i,j] = M[j,i] = YY[i,j]
    check('interior_data_rank_two', Y.rank() == 2)
    check('interior_matching_statistics_both_models',
          stats(M) == stats(YY) and stats(M,True) == stats(YY,True))
    for i in range(8):
        check('interior_exact_dominance_margin',
              M[i,i]-sum(abs(M[i,j]) for j in range(8) if j != i) >= margin)
    for k in range(1,9):
        check('interior_exact_Sylvester_PD', M[:k,:k].det() > 0)

# Specialized independent MLT(K4,4) = 4 proof controls.
def outer_coefficient(U,V):
    k = U.cols
    return s.Matrix([[U[a,i]*U[a,j] for a in range(4)] +
                     [-V[b,i]*V[b,j] for b in range(4)]
                     for i in range(k) for j in range(i,k)])

# Three observations: a positive sparse-PSD stress persists on an open data set.
H = s.Matrix([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2
U3 = s.eye(4)[:,:3]
V3 = H*U3
C3 = outer_coefficient(U3,V3)
piv3 = list(C3.rref()[1])
C3minor = C3[:,piv3]
check('Hadamard_orthogonal', H.T*H == s.eye(4))
check('three_sample_same_column_Gram', U3.T*U3 == V3.T*V3 == s.eye(3))
check('three_sample_positive_kernel_weights', C3*s.ones(8,1) == s.zeros(6,1))
check('three_sample_six_independent_conditions', C3minor.det() != 0 and C3.rank() == 6)
Omega3 = s.Matrix.vstack(s.Matrix.hstack(s.eye(4),-H.T),
                         s.Matrix.hstack(-H,s.eye(4)))
F3 = s.Matrix.vstack(s.eye(4),-H)
check('three_sample_stress_PSD_factorization', Omega3 == F3*F3.T)
check('three_sample_stress_nonzero_rank_four', Omega3.rank() == 4)
check('three_sample_stress_in_singleton_model', in_model(Omega3))
check('three_sample_stress_annihilates_data',
      Omega3*U3.col_join(V3) == s.zeros(8,3))
check('three_sample_stress_ray_determinant',
      s.expand((s.eye(8)+s.symbols('t')*Omega3).det()-(1+2*s.symbols('t'))**4) == 0)

# Four observations: a polynomial exceptional set contains all nonzero stresses.
U4 = s.eye(4)
V4 = s.eye(4)
for i in range(4):
    V4[i,(i+1)%4] = 2
C4 = outer_coefficient(U4,V4)
rowpiv4 = list(C4.T.rref()[1])
det4 = C4[rowpiv4,:].det()
check('four_sample_blocks_invertible', U4.det() == 1 and V4.det() == -15)
check('four_sample_outerproducts_linearly_independent', C4.rank() == 8 and det4 != 0)
M = min(k for k in range(1,9) if k*(k+1)//2 >= 8)
check('credited_theorem_formula_specialization', M == 4 and min(M,5) == 4)

results = {
    'status': 'PASS_EXACT',
    'program_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'assertions': sum(counts.values()),
    'categories': dict(counts),
    'epsilon': str(eps), 'PD_margin_unscaled_scatter': str(margin),
    'rank_two_minor_lower_bound': str(1-2*eps),
    'completion_inverse_forbidden_12_entry': str(P.inv()[0,1]),
    'MLT_three_sample_C_shape': list(C3.shape),
    'MLT_three_sample_C': [[str(x) for x in C3.row(i)] for i in range(C3.rows)],
    'MLT_three_sample_pivot_columns_zero_based': piv3,
    'MLT_three_sample_minor_determinant': str(C3minor.det()),
    'MLT_three_sample_H': [[str(x) for x in H.row(i)] for i in range(4)],
    'MLT_four_sample_C_shape': list(C4.shape),
    'MLT_four_sample_minor_rows_zero_based': rowpiv4,
    'MLT_four_sample_minor_determinant': str(det4),
    'MLT_four_sample_V_determinant': str(V4.det()),
    'numeric_simulation': False,
    'scope': 'Likelihood/probability controls and a specialized independent singleton K4,4 MLT proof; no overall source-scope, ideal-family, historical-priority, or publication verdict.'
}
(HERE/'exact_controls_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
