#!/usr/bin/env python3
"""Independent exact controls; verification of literature scope, no proof search."""
from pathlib import Path
import datetime
import hashlib
import json
import sys
import sympy as s

ROOT = Path(__file__).resolve().parent
checks = []


def Eu(u, x):
    D = u.jacobian(x)
    return (D + D.T) / 2


def zero(M):
    assert all(s.simplify(z) == 0 for z in M), M


def cert(name, **detail):
    checks.append({"name": name, "pass": True, **detail})


# Check the exact Saint-Venant entries used in the dimension-independent proof.
d = 5
H = s.MutableDenseMatrix(d, d, lambda i, j: s.Symbol("H" + str(min(i,j)) + str(max(i,j))))
P = s.zeros(d)
P[0,1] = P[1,0] = s.Rational(1,2)
def C(i,j,k,l):
    return P[j,l]*H[i,k] + P[i,k]*H[j,l] - P[j,k]*H[i,l] - P[i,l]*H[j,k]
assert C(0,1,0,1) == -H[0,1]
for j in range(2,d):
    assert C(0,1,0,j) == -H[0,j]/2
    assert C(0,1,1,j) == H[1,j]/2
    for k in range(2,d):
        assert C(0,j,1,k) == H[j,k]/2
cert("explicit_independent_compatibility_entries", dimension=d)
P = s.zeros(d)
P[0,0] = 1
for j in range(1,d):
    for k in range(1,d):
        assert C(0,j,0,k) == H[j,k]
cert("explicit_parallel_compatibility_entries", dimension=d)

# Nonorthogonal change of both domain AND codomain: plain rotation is insufficient.
a, b, c = s.Matrix([2,1,0]), s.Matrix([1,3,0]), s.Matrix([0,0,1])
S = s.Matrix.hstack(a,b,c)
T = S.inv().T
e1,e2 = s.eye(3)[:,0],s.eye(3)[:,1]
zero(T.T*a-e1); zero(T.T*b-e2)
P = (a*b.T+b*a.T)/2
zero(T.T*P*T-(e1*e2.T+e2*e1.T)/2)
y = s.Matrix(s.symbols("y0:3")); x = s.Matrix(s.symbols("x0:3"))
u = s.Matrix([x[0]**2+x[1]*x[2], x[0]*x[1]+x[2]**3, x[1]**2])
sub = dict(zip(x,T*y)); w = T.T*u.subs(sub, simultaneous=True)
zero(Eu(w,y)-T.T*Eu(u,x).subs(sub,simultaneous=True)*T)
R = s.Matrix([[0,2,3],[-2,0,4],[-3,-4,0]])
zero(T.T*R*T+(T.T*R*T).T)
cert("nonorthogonal_congruence_preserves_strain_and_skew", determinant=str(S.det()))

# Literal unnormalized printed (i) would misclassify this rank-one input.
x1,x2 = s.symbols("x1 x2", real=True); x = s.Matrix([x1,x2])
u = s.Matrix([4*x1**3*x2,-x1**4])
P = s.diag(2,0)
lam = 6*x1**2*x2
zero(Eu(u,x)-P*lam)
assert s.diff(lam,x1,x2) == 12*x1
cert("nonunit_collinear_requires_parallel_case", a=[2,0], b=[1,0], coefficient=str(lam))

# Signed smooth coefficient, and dimension-one/zero strain boundary checks.
x = s.Matrix(s.symbols("x0:3")); u = s.Matrix([x[1]*x[2],x[0]*x[2],-x[0]*x[1]])
P = s.zeros(3); P[0,1]=P[1,0]=s.Rational(1,2)
zero(Eu(u,x)-2*x[2]*P)
assert (2*x[2]).subs(x[2],1)>0 and (2*x[2]).subs(x[2],-1)<0
cert("smooth_signed_coefficient", positive=2, negative=-2)
t=s.symbols("t"); assert s.diff(t**5+t,t)==5*t**4+1
cert("dimension_one_nonzero_line_has_arbitrary_derivatives")
zero(Eu(R*x+s.Matrix([1,2,3]),x))
cert("zero_product_rigid_control")

# Distributional signed control: jump sizes determine positive and negative masses.
jumps=[(s.Integer(0),s.Integer(1)),(s.Integer(1),s.Integer(-2))]
assert sum(m for _,m in jumps)==-1 and any(m>0 for _,m in jumps) and any(m<0 for _,m in jumps)
cert("signed_singular_measure_jump_control", jumps=[(str(t),str(m)) for t,m in jumps],
     interpretation="delta on x2=0 minus twice delta on x2=1, tensor remaining Lebesgue coordinates")

# Connected nonconvex domains. Differential assertions verified with arbitrary f;
# flat compact support glues the branches (see mathematical certificate).
f=s.Function("f")
x=s.Matrix([x1,x2])
u=s.Matrix([f(x2),0]); P=s.Matrix([[0,s.Rational(1,2)],[s.Rational(1,2),0]])
zero(Eu(u,x)-s.diff(f(x2),x2)*P)
bridge=s.exp(-1/(1-x2**2))
assert bridge.subs(x2,0)==s.exp(-1)
cert("independent_nonconvex_branch_strain", same_slice_points=[[-2,0],[2,0]],
     value_difference="exp(-1)", domains=[[-3,-1,-2,2],[1,3,-2,2],[-3,3,1,2]])
u=s.Matrix([x2*s.diff(f(x1),x1),-f(x1)])
zero(Eu(u,x)-s.diag(x2*s.diff(f(x1),x1,2),0))
cert("parallel_nonconvex_branch_strain", same_slice_points=[[0,-2],[0,2]],
     value_difference="-exp(-1)", domains=[[-2,2,-3,-1],[-2,2,1,3],[-2,-1,-3,3]])

result = {"pass": True, "head": "ea6b192f7e3bc094b78bbc416bf61c609ffa5b2d",
          "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "python": sys.version, "sympy": s.__version__,
          "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          "checks": checks,
          "limits": "Exact sufficiency/coordinate/type/countercontrols. Dimension-independent smooth necessity is in the accompanying certificate; full BD theorem is primary literature."}
(ROOT / "source_domain_type_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
