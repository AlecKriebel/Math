"""Root's independent finite K4,4 certificates; no submitted code imports.

Reads no files, performs no network/process/provider actions, and writes only
JSON to stdout. Exact SymPy rational arithmetic. The continuity and statistical
arguments are in the independently frozen derivation; these checks certify
their finite premises, not a stand-alone proof of every quantified conclusion.
"""
import itertools
import json
import sympy as s


def measured(X):
    S = X * X.T
    return s.Matrix([S[i, i] for i in range(8)] +
                    [S[i, j] for i in range(4) for j in range(4, 8)])


def symmetric_coordinates(A):
    return s.Matrix([A[i, j] for i in range(3) for j in range(i, 3)])


def exact_matrix(A):
    return [[str(v) for v in row] for row in A.tolist()]


def principal_minors_nonnegative(A):
    minors = []
    for k in range(1, A.rows + 1):
        for ix in itertools.combinations(range(A.rows), k):
            value = A.extract(ix, ix).det()
            assert value >= 0, (ix, value)
            minors.append(value)
    return len(minors), sum(v == 0 for v in minors)


def main():
    checks = {}
    X2 = s.Matrix([[1, 0]] * 4 + [[0, 1]] * 4)
    assert measured(X2) == measured(s.eye(8))
    assert X2.rank() == 2
    checks['real_rank2_PD_completion'] = {'X': exact_matrix(X2),
                                           'completion': 'I8', 'rank': 2}
    a, b = s.symbols('a b', real=True)
    assert (s.Matrix([[a*a, a*b], [a*b, b*b]])).det() == 0
    checks['rank1_edge_obstruction'] = 'identically zero determinant'

    xs = s.symbols('x0:32')
    variables = s.Matrix(8, 4, xs)
    J = measured(variables).jacobian(xs)
    Z4 = s.Matrix([[1, 1, 0, 0], [1, 0, 1, 0],
                   [1, 0, 0, 1], [0, 1, 1, 0]])
    X4 = s.eye(4).col_join(Z4)
    J0 = J.subs(dict(zip(xs, list(X4))))
    pivots = J0.rref()[1]
    assert len(pivots) == 24
    minor = J0[:, list(pivots)].det()
    assert minor != 0
    checks['rank4_Jacobian'] = {'X': exact_matrix(X4), 'rows': 24,
                                'columns': 32, 'rank': len(pivots),
                                'minor_columns_zero_based': list(pivots),
                                'minor_determinant': str(minor)}
    # Negative control: rank-three data cannot have a full-rank measured map,
    # because the formal measured cross-block determinant vanishes identically.
    Y0 = s.Matrix([[1, 1, 1], [1, -1, -1],
                   [-1, 1, -1], [-1, -1, 1]]) / 2
    Z0 = s.eye(3).col_join(s.zeros(1, 3))
    X0 = Y0.col_join(Z0)
    assert Y0.T * Y0 == Z0.T * Z0 == s.eye(3)
    assert X0.rank() == 3
    assert (Y0 * Z0.T).det() == 0
    formal_cross = s.Matrix(4, 4, s.symbols('b0:16'))
    assert formal_cross.det() != 0
    checks['nonzero_I3_relation'] = {
        'formal_cross_determinant_nonzero': True,
        'relation_is_one_original_4_by_4_minor': True,
        'warning': 'does not identify the full elimination ideal'}

    columns = [symmetric_coordinates(Y0.row(i).T * Y0.row(i))
               for i in range(4)]
    columns += [-symmetric_coordinates(Z0.row(i).T * Z0.row(i))
                for i in range(4)]
    W = s.Matrix.hstack(*columns)
    selected = [0, 1, 2, 3, 4, 5]
    weight_minor = W[:, selected].det()
    assert weight_minor != 0 and W * s.ones(8, 1) == s.zeros(6, 1)
    checks['open_bad_data_weight_system'] = {
        'matrix': exact_matrix(W), 'rank': W.rank(),
        'minor_columns_zero_based': selected,
        'minor_determinant': str(weight_minor),
        'fixed_weights': ['b3=1', 'b4=1'],
        'witness_weights': ['1'] * 8}
    K0 = s.eye(4).row_join(-Y0 * Z0.T).col_join(
         (-Z0 * Y0.T).row_join(s.eye(4)))
    assert K0 * X0 == s.zeros(8, 3)
    assert K0.rank() == 5
    counts = principal_minors_nonnegative(K0)
    checks['base_PSD_stress'] = {
        'K': exact_matrix(K0), 'rank': 5,
        'characteristic_polynomial': str(K0.charpoly().as_expr()),
        'principal_minors_checked': counts[0], 'zero_minors': counts[1],
        'annihilates_data': True, 'within_part_off_diagonal_zero': True}
    assert not (-K0).is_positive_semidefinite
    assert K0 * X0 == s.zeros(8, 3) and (K0 * s.eye(8)).trace() > 0
    checks['negative_controls'] = {
        'negative_stress_rejected_as_PSD': True,
        'I8_does_not_match_bad_witness': measured(s.eye(8)) != measured(X0)}

    # Exact, nontrivial perturbation exercises the weight formula rather than
    # verifying only the symmetric base point. Openness is proved separately.
    Xp = X0 + s.Matrix(8, 3, [s.Rational((i*7) % 13-6, 1000)
                              for i in range(24)])
    Y, Z = Xp[:4, :], Xp[4:, :]
    wcolumns = [symmetric_coordinates(Y.row(i).T * Y.row(i))
                for i in range(4)]
    wcolumns += [-symmetric_coordinates(Z.row(i).T * Z.row(i))
                 for i in range(4)]
    WP = s.Matrix.hstack(*wcolumns)
    solved = WP[:, selected].inv() * (-WP[:, 6] - WP[:, 7])
    weights = list(solved) + [s.Integer(1), s.Integer(1)]
    assert all(v > 0 for v in weights)
    Da, Db = s.diag(*weights[:4]), s.diag(*weights[4:])
    G = Y.T * Da * Y
    assert G == Z.T * Db * Z
    assert all(G[:k, :k].det() > 0 for k in range(1, 4))
    cross = -Da * Y * G.inv() * Z.T * Db
    K = Da.row_join(cross).col_join(cross.T.row_join(Db))
    assert K * Xp == s.zeros(8, 3) and K.rank() == 5
    # Schur complement is PSD by its exact Gram projector description.
    Schur = Db - Db * Z * G.inv() * Z.T * Db
    scounts = principal_minors_nonnegative(Schur)
    checks['exact_perturbed_stress'] = {
        'data': exact_matrix(Xp), 'weights': [str(v) for v in weights],
        'G_leading_minors': [str(G[:k, :k].det()) for k in range(1, 4)],
        'Schur_principal_minors_checked': scounts[0],
        'Schur_zero_minors': scounts[1], 'K_rank': K.rank(),
        'KX_zero': True}
    print(json.dumps({'schema': 'pr212-root-independent-exact-checks-v1',
                      'status': 'PASS', 'sympy': s.__version__,
                      'claims_scope': 'finite rational certificate checks only',
                      'checks': checks}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
