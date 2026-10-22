"""Independent finite verification of the revised colored-C4 dependency.
No files/network/process actions; exact rational arithmetic, stdout only.
"""
import json
import sympy as s


def stats(X):
    S = X * X.T
    return s.Matrix([s.trace(S), S[0, 2], S[0, 3], S[1, 2], S[1, 3]])


xs = s.symbols('x0:8')
X = s.Matrix(4, 2, xs)
point = s.eye(2).col_join(2*s.eye(2))
J = stats(X).jacobian(xs).subs(dict(zip(xs, list(point))))
pivots = J.rref()[1]
minor = J[:, list(pivots)].det()
assert len(pivots) == 5 and minor != 0

alpha = s.symbols('alpha', real=True)
C = s.Matrix(2, 2, s.symbols('c0:4', real=True))
K = (alpha*s.eye(2)).row_join(C).col_join(C.T.row_join(alpha*s.eye(2)))
z = s.Matrix(s.symbols('z0:4', real=True))
D = s.diag(1, 1, -1, -1)
h = (z.T*D*z)[0]
assert s.expand((z.T*D*K*z)[0] - alpha*h) == 0
assert h.subs({z[0]: 1, z[1]: 0, z[2]: 0, z[3]: 0}) == 1
# Thus Kz=0 implies alpha*h=0; outside h=0, alpha=0.
# A PSD matrix with zero diagonal is zero by its 2-square principal minors.
u, v, w = s.symbols('u v w', real=True)
assert s.Matrix([[0, u], [u, 0]]).det() == -u*u
one = s.Matrix(4, 1, list(z))
assert s.Matrix([[stats(one)[1], stats(one)[2]],
                 [stats(one)[3], stats(one)[4]]]).det().expand() == 0
q = s.symbols('q0:4')
assert s.Matrix(2, 2, q).det() != 0
witness = s.Matrix([2, 0, 0, 0])
assert stats(witness) == stats(s.eye(4))
print(json.dumps({'schema': 'pr212-root-colored-C4-exact-dependency-check-v1',
 'status': 'PASS', 'coloring': 'one vertex class; four singleton cross edges',
 'vertex_order': 'bipartition [0,1] and [2,3]',
 'Jacobian_shape': list(J.shape), 'Jacobian_rank': len(pivots),
 'minor_columns_zero_based': list(pivots), 'minor_determinant': str(minor),
 'nonzero_I1_relation': 'cross00*cross11-cross01*cross10',
 'stress_identity': 'z^T D K z = alpha*(zL^T*zL-zR^T*zR)',
 'bad_data_contained_in_nonzero_polynomial_zero_set': str(h),
 'real_rank1_identity_statistics_witness': [2, 0, 0, 0],
 'proof_scope': 'finite identities; quantified PSD/probability proof in note',
 'coordinate_normalization': 'edge entries; twice-edge convention is invertible scaling'},
 sort_keys=True, indent=2))
