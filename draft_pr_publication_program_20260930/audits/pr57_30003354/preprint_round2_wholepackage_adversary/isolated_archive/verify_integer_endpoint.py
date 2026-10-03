"""Portable PR57 exact finite diagnostics; Python 3.9+, standard library only.

Adapted from the previously independently reviewed geometric Taylor controls,
with bounded logarithm/Beltrami numerator controls and rational reconstruction
controls derived from the independently reviewed endpoint operator checks.
This author preparation adds no independent-review credit. The script writes
only deterministic JSON to stdout. Finite controls supplement the manuscript;
they do not prove the universal estimates or complete geometric theorem.
SPDX-License-Identifier: MIT
"""
from fractions import Fraction as F
import json
from math import factorial, comb


def const(c): return {(0, 0): F(c)} if c else {}
def add(a, b):
    out = dict(a)
    for key, value in b.items(): out[key] = out.get(key, F(0)) + value
    return {key: value for key, value in out.items() if value}
def scale(a, c): return {key: value * F(c) for key, value in a.items() if value * F(c)}
def mul(a, b):
    out = {}
    for (i, j), av in a.items():
        for (k, l), bv in b.items():
            if i + j + k + l <= 2:
                key = (i + k, j + l)
                out[key] = out.get(key, F(0)) + av * bv
    return {key: value for key, value in out.items() if value}
def lap(a): return 2 * (a.get((2, 0), F(0)) + a.get((0, 2), F(0)))




def poly_add(a,b):
    out=dict(a)
    for m,c in b.items():out[m]=out.get(m,F(0))+c
    return {m:c for m,c in out.items() if c}


def poly_derivative(a,axis):
    out={}
    for m,c in a.items():
        if m[axis]:
            v=list(m);v[axis]-=1;out[tuple(v)]=c*m[axis]
    return out


def poly_shift(a,axis,power=1,coefficient=1):
    out={}
    for m,c in a.items():
        v=list(m);v[axis]+=power;out[tuple(v)]=c*coefficient
    return out


def quotient_numerator_derivative(P,power,axis):
    # D(P/s^(2*power)) has numerator s^2 DP-2*power*x_axis*P.
    dp=poly_derivative(P,axis)
    first={}
    for i in range(3):first=poly_add(first,poly_shift(dp,i,2))
    return poly_add(first,poly_shift(P,axis,1,-2*power))

def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled: do not use Python -O or PYTHONOPTIMIZE.')
    one = const(1); x = {(1, 0): F(1)}; y = {(0, 1): F(1)}
    controls = []
    # J=[[2,1],[0,3]], so F(u,v)=(u/2-v/6,v/3).
    Jinv = [[F(1,2), F(-1,6)], [F(0), F(1,3)]]
    A = [[sum(Jinv[i][k]*Jinv[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
    wrong_A = [[sum(Jinv[k][i]*Jinv[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    H = [[F(2), F(3)], [F(3), F(4)]]
    correct = sum(A[i][j]*H[i][j] for i in range(2) for j in range(2))
    wrong = sum(wrong_A[i][j]*H[i][j] for i in range(2) for j in range(2))
    Fx = add(scale(x, F(1,2)), scale(y, F(-1,6))); Fy = scale(y, F(1,3))
    composed = add(add(mul(Fx, Fx), scale(mul(Fx, Fy), 3)), scale(mul(Fy, Fy), 2))
    direct = lap(composed)
    assert direct == correct == F(2,3) and wrong == F(5,9) and wrong != correct
    controls.append({'control': 'nonorthogonal affine Laplacian principal matrix order',
                     'direct_composition': str(direct), 'J_inverse_J_inverse_transpose': str(correct),
                     'wrong_reversed_order': str(wrong)})

    # Solve F(t)+F(t)^2=t through the quadratic jet, without a square-root derivative formula.
    inverse_jet = add(x, scale(mul(x, x), -1))
    assert add(inverse_jet, mul(inverse_jet, inverse_jet)) == x
    assert inverse_jet[(2,0)] * 2 == -2
    controls.append({'control': 'nonlinear inverse-map first-order drift', 'inverse_second_derivative_at_origin': '-2'})

    # Around scaled point (-1,0), let X=-1+x, Y=y, Q=1+X^2+Y^2.
    X = add(const(-1), x); Q = add(add(one, mul(X, X)), mul(y, y))
    delta = add(scale(Q, F(1,2)), const(-1))  # Q=2(1+delta).
    delta2 = mul(delta, delta)
    log_Q_without_constant = add(delta, scale(delta2, F(-1,2)))
    inverse_Q = scale(add(add(one, scale(delta, -1)), delta2), F(1,2))
    radial_squared = add(Q, const(-1))
    Hjet = add(log_Q_without_constant, scale(mul(radial_squared, inverse_Q), F(1,2)))
    Mjet = mul(X, Hjet)
    # The omitted log2 times X is affine and has zero Laplacian.
    assert lap(Mjet) == F(-7,2)
    controls.append({'control': 'uncorrected r1 logarithmic curvature leading jet',
                     'scaled_point': '(-1,0)', 'laplacian_Re_M': str(lap(Mjet))})
    sqrt_Q_div_sqrt2 = add(add(one, scale(delta, F(1,2))), scale(delta2, F(-1,8)))
    assert lap(sqrt_Q_div_sqrt2) == F(3,4)
    controls.append({'control': 'convex radius correction leading jet',
                     'scaled_point': '(-1,0)', 'laplacian_sqrt_Q_div_sqrt2': '3/4',
                     'laplacian_sqrt_Q': '3*sqrt(2)/4', 'necessary_pointwise_K_threshold': '7*sqrt(2)/3'})

    # For r1 the exact first f_z jet is 1+2 c z, c=epsilon log rho=-1.
    real_fz = add(one, scale(x, -2)); imag_fz = scale(y, -2)
    squared_norm = add(mul(real_fz, real_fz), mul(imag_fz, imag_fz))
    norm_delta = add(squared_norm, const(-1))
    hjet = scale(add(norm_delta, scale(mul(norm_delta, norm_delta), F(-1,2))), F(1,2))
    assert hjet[(1,0)] == -2 and hjet.get((0,1), 0) == 0 and lap(hjet) == 0
    controls.append({'control': 'critical conformal-factor first jet at normalization point',
                     'gradient_h': ['-2', '0'], 'harmonic_quadratic_jet_laplacian': '0',
                     'gradient_background_and_convex_correction_at_origin': ['0', '0']})

    # Full regularized-log numerator degree and l1 coefficient bounds, in
    # explicit finite orders. The recurrence identity and all-order estimates
    # remain mathematical arguments in the paper.
    recurrence_checks = []
    for j in range(1, 8):
        for a in range(j+1):
            axis = 0 if a else 1
            initial = (1,0,0) if axis == 0 else (0,1,0)
            P = {initial:F(1)}
            variables = [0]*(a-1)+[1]*(j-a) if a else [1]*(j-1)
            for k, v in enumerate(variables, 1):
                P = quotient_numerator_derivative(P, k, v)
            assert P and all(sum(m)==j for m in P)
            norm = sum(abs(c) for c in P.values())
            assert norm <= 5**(j-1)*factorial(j-1)
            recurrence_checks.append({'order':j,'x_derivatives':a,'coefficient_l1':str(norm),'bound':str(5**(j-1)*factorial(j-1))})
    beltrami_checks = []
    for r in range(1,9):
        d = r+2
        for k in range(r+1):
            for a in range(k+1):
                for component in [0,1]:
                    Q = {}
                    for iy in range(d+1):
                        phase = iy % 4
                        if phase % 2 == component:
                            sign = 1 if phase in [0,1] else -1
                            Q[(d-iy,iy,0)] = F(sign*comb(d,iy),2)
                    for j,v in enumerate([0]*a+[1]*(k-a)):
                        Q = quotient_numerator_derivative(Q,j+1,v)
                    assert all(sum(m)==d+k for m in Q)
                    beltrami_checks.append([r,k,a,component])
    reconstructions = []
    for p,q,c,d in [(1,0,0,0),(2,1,1,-1),(3,-2,-1,2),(2,3,1,1),(4,1,-2,1),(1,2,0,-1)]:
        p,q,c,d=map(F,[p,q,c,d]); norm=p*p+q*q
        mr=(c*p+d*q)/norm;mi=(d*p-c*q)/norm
        tensor=[[(1+mr)**2+mi*mi,2*mi],[2*mi,(1-mr)**2+mi*mi]]
        jacobian=[[p+c,-q+d],[q+d,p-c]]
        gram=[[sum(jacobian[a][i]*jacobian[a][j] for a in range(2)) for j in range(2)] for i in range(2)]
        assert all(norm*tensor[i][j]==gram[i][j] for i in range(2) for j in range(2))
        reconstructions.append({'fz':[str(p),str(q)],'fbarz':[str(c),str(d)],'norm_fz_squared':str(norm)})
    result = {'schema':'integer-endpoint-finite-exact-diagnostics/v1',
              'status':'PASS_FINITE_EXACT_DIAGNOSTICS',
              'arithmetic':'standard-library Fraction; exact polynomial and degree-two Taylor algebra',
              'geometric_controls':controls,'geometric_control_count':len(controls),
              'logarithm_recurrence_controls':recurrence_checks,
              'logarithm_recurrence_control_count':len(recurrence_checks),
              'Beltrami_degree_controls':beltrami_checks,
              'Beltrami_degree_control_count':len(beltrami_checks),
              'rational_metric_reconstruction_controls':reconstructions,
              'rational_metric_reconstruction_control_count':len(reconstructions),
              'finite_controls_are_not_universal_proof':True,
              'global_cutoff_curvature_completeness_and_priority_not_certified':True,
              'new_independent_review_credit':0}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__': main()
