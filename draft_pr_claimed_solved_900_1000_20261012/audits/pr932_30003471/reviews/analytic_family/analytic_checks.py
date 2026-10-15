"""Exact finite checks of conventions and estimates, not a test of the index theorem."""
from pathlib import Path
import json, hashlib, datetime
import sympy as s
I=s.I
p=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-I],[I,0]]),s.Matrix([[1,0],[0,-1]])]
c=[-I*x for x in p]
w=[x.T for x in c]
Z=s.zeros(2); E=s.eye(2)
x=s.symbols('x0:4'); X=s.Matrix(2,2,x)
def md(m): return [[str(s.simplify(v)) for v in m.row(k)] for k in range(m.rows)]
def null_dim(exprs):
 M,_=s.linear_eq_to_matrix([v for m in exprs for v in m],x)
 return 4-M.rank()
cliff=all(c[a]*c[b]+c[b]*c[a]==(-2*E if a==b else Z) for a in range(3) for b in range(3))
# Column-major vec(A) gives vec(L A R)=(R^T tensor L)vec(A).
chi=-s.kronecker_product(c[1].T,c[2])
L=s.kronecker_product(E,I*c[2]*c[0])
B=s.kronecker_product((2*c[0]).T,c[0])+s.kronecker_product((3*c[1]).T,c[1])
b_eigs={str(k):v for k,v in B.eigenvals().items()}
# Exact boundary defect weight integral on planar sector of angle gamma.
d=s.symbols('delta',positive=True); gamma=s.symbols('gamma',positive=True)
# integral_{d^2}^{d} gamma/(r log(d)^2)dr = gamma/abs(log d) for 0<d<1.
log_formula=s.simplify((s.log(d)-s.log(d**2))/s.log(d)**2)
out={
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Finite exact controls only; the proofs of Fredholmness, homotopy invariance and compactness are audited separately.',
 'clifford_relations':cliff,
 'column_representation_volume_c1c2c3':md(c[0]*c[1]*c[2]),
 'row_coefficient_array_volume_omega1omega2omega3_under_standard_column_multiplication':md(w[0]*w[1]*w[2]),
 'correct_constant_plus_kernel_dimension':null_dim([a*X-X*a for a in c]),
 'correct_constant_minus_kernel_dimension':null_dim([a*X+X*a for a in c]),
 'wrong_untransposed_omega_column_plus_kernel_dimension':null_dim([c[a]*X-X*w[a] for a in range(3)]),
 'constant_ball_identity_chiI':all(-a*E*a==E for a in c),
 'chi_self_adjoint':chi.conjugate().T==chi,
 'chi_squared_identity':chi*chi==s.eye(4),
 'boundary_symbol_anticommutator_zero':L*chi+chi*L==s.zeros(4),
 'stable_plus_symbol_dimension':len((L-s.eye(4)).nullspace()),
 'boundary_symbol_and_chi_plus_intersection_dimension':4-s.Matrix.vstack(L-s.eye(4),chi-s.eye(4)).rank(),
 'model_boundary_B_eigenvalues_for_singular_values_2_3':b_eigs,
 'model_boundary_B_operator_norm':max(abs(k) for k in B.eigenvals()),
 'exact_annulus_integral_divided_by_sector_angle':str(log_formula),
 'annulus_formula_assumption':'0<delta<1; equals 1/abs(log(delta))',
}
out['all_expected_checks_pass']=(cliff and out['correct_constant_plus_kernel_dimension']==1 and out['correct_constant_minus_kernel_dimension']==0 and out['wrong_untransposed_omega_column_plus_kernel_dimension']==0 and out['constant_ball_identity_chiI'] and out['chi_self_adjoint'] and out['chi_squared_identity'] and out['boundary_symbol_anticommutator_zero'] and out['stable_plus_symbol_dimension']==2 and out['boundary_symbol_and_chi_plus_intersection_dimension']==0 and out['model_boundary_B_operator_norm']==5)
# Convert exact integers to native JSON scalars without eval.
def default(v):
 if isinstance(v,s.Integer):return int(v)
 return str(v)
R=Path(__file__).resolve().parent
(R/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2,default=default)+'\n')
print(json.dumps(out,indent=2,default=default))
