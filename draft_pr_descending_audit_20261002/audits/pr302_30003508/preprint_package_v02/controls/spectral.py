#!/usr/bin/env python3
"""Independent algebra and countercontrols; no imported candidate test code."""
import datetime, hashlib, json, math, os, pathlib, sys
import sympy as s

here = pathlib.Path(__file__).resolve().parent
tests = []
def require(name, condition, detail):
    assert condition, name
    tests.append({"name": name, "status": "PASS", "detail": detail})

x, y = s.symbols("x y", real=True)
mu = 2 * (1+x) / 3
z = (2*x + x*x) / 3
S = 1 / mu
require("normalized_nonconstant_density", s.integrate(mu, (x, 0, 1)) == 1,
        "μ=2(1+x)/3, z=(2x+x²)/3 maps [0,1] to [0,1].")
require("coordinate_jacobian", s.diff(z, x) == mu,
        "S=1/μ turns μ⁻¹∂x(S∂x) into ∂z².")
for k in range(1, 7):
    u = s.cos(k*s.pi*z)
    Lu = s.diff(S*s.diff(u, x), x)/mu
    require("nonconstant_density_eigen_PDE_%d" % k,
            s.simplify(Lu + (k*s.pi)**2*u) == 0,
            "Exact conormal Neumann eigenfunction cos(kπz), ν=−k²π².")
    require("nonconstant_density_flux_%d" % k,
            s.simplify((S*s.diff(u, x)).subs(x, 0)) == 0 and
            s.simplify((S*s.diff(u, x)).subs(x, 1)) == 0,
            "Both conormal endpoint fluxes vanish.")
    jet = s.Matrix([s.diff(u, x, 2), s.diff(u, x)])
    theta = s.Matrix([S, s.diff(S, x)])
    require("one_dimensional_identification_%d" % k,
            s.simplify((jet.dot(theta)) + (k*s.pi)**2*mu*u) == 0,
            "The RHS is ν μ u, not ν u; θ contains S and S′.")

mu_x = 2*(1+x)/3
mu_y = (1+2*y)/2
zx = (2*x+x*x)/3
zy = (y+y*y)/2
rho = mu_x*mu_y
matS = s.diag(3*rho/mu_x**2, 5*rho/mu_y**2)
divS = s.Matrix([s.diff(matS[0,0],x)+s.diff(matS[0,1],y),
                 s.diff(matS[1,0],x)+s.diff(matS[1,1],y)])
theta2 = s.Matrix([matS[0,0], matS[1,1], matS[0,1], divS[0], divS[1]])
for a, b in [(0,0),(1,0),(0,1),(1,1),(2,1),(1,2),(2,2)]:
    u = s.cos(a*s.pi*zx)*s.cos(b*s.pi*zy)
    jet = s.Matrix([s.diff(u,x,2),s.diff(u,y,2),2*s.diff(u,x,y),s.diff(u,x),s.diff(u,y)])
    nu = -(3*a*a+5*b*b)*s.pi**2
    require("anisotropic_unknown_density_%d_%d" % (a,b),
            s.simplify(jet.dot(theta2)-nu*rho*u) == 0,
            "Exact separable coordinate model, unequal diffusivities3,5; rectangle is only a local algebra control, not a smooth-domain theorem example.")

for d in [2,3,4]:
    xx = s.symbols("x0:%d" % d)
    V = s.Matrix(d,d,lambda i,j: (i+1)*xx[j] + (j+1)*xx[i] + (1 if i==j else 0))
    ten = s.eye(d) + V*V.T
    fn = sum((i+1)*xx[i]**3 for i in range(d)) + sum(xx[i]*xx[j]*(i+j+1) for i in range(d) for j in range(i+1,d))
    hv = [s.diff(fn,xx[i],2) for i in range(d)] + [2*s.diff(fn,xx[i],xx[j]) for i in range(d) for j in range(i+1,d)] + [s.diff(fn,v) for v in xx]
    tv = [ten[i,i] for i in range(d)] + [ten[i,j] for i in range(d) for j in range(i+1,d)] + [sum(s.diff(ten[i,j],xx[i]) for i in range(d)) for j in range(d)]
    divergence = sum(s.diff(sum(ten[i,j]*s.diff(fn,xx[j]) for j in range(d)),xx[i]) for i in range(d))
    require("general_nonconstant_SPD_tensor_jet_d%d" % d,
            s.expand(sum(a*b for a,b in zip(hv,tv))-divergence) == 0,
            "S=I+VVᵀ is nonconstant SPD with off-diagonal terms; doubled mixed Hessian convention verified.")

v = s.Matrix([1,2,3,4])
Q = s.eye(4)-2*v*v.T/(v.dot(v))
J = s.Matrix([[2,3,-1,5],[1,0,4,-2],[3,-2,1,1]])
uv = s.Matrix([[2,-1,3,4]])
require("rational_orthogonal_basis", Q.T*Q == s.eye(4), "Exact rational Householder basis.")
for idx, eigs in enumerate([
    [s.Rational(3,5),s.Rational(3,5),0,-s.Rational(1,3)],
    [s.Rational(1,10**8),s.Rational(7,10),s.Rational(6,5),0],
    [s.Rational(3,5)-s.Rational(1,10**6),s.Rational(3,5)+s.Rational(1,10**6),-s.Rational(1,10**8),0],
]):
    D = s.diag(*eigs)
    g = s.diag(*[t*t if t>0 else 0 for t in eigs])
    h = s.diag(*[t*t*s.log(t) if t>0 else 0 for t in eigs])
    B = J*D*Q.T
    e = uv*D*Q.T
    opg, oph = Q*g*Q.T,Q*h*Q.T
    explicitA = sum((t**4*J[:,i]*J[:,i].T for i,t in enumerate(eigs) if t>0),s.zeros(3))
    explicitb = sum((t**4*s.log(t)*J[:,i]*uv[0,i] for i,t in enumerate(eigs) if t>0),s.zeros(3,1))
    require("functional_calculus_A_case%d" % idx,
            B*opg*B.T == explicitA,
            "Includes exact repeated, zero, negative, tiny positive and greater-than-one empirical eigenvalues.")
    require("functional_calculus_b_case%d" % idx,
            (B*oph*e.T-explicitb).applyfunc(s.simplify) == s.zeros(3,1),
            "κ from each outer factor gives κ⁴logκ; zero/negative modes contribute exactly zero.")

R = s.eye(4)
R[0,0],R[0,1],R[1,0],R[1,1] = s.Rational(3,5),-s.Rational(4,5),s.Rational(4,5),s.Rational(3,5)
D = s.diag(s.Rational(3,5),s.Rational(3,5),0,-s.Rational(1,3))
g = s.diag(s.Rational(3,5)**2,s.Rational(3,5)**2,0,0)
require("repeated_eigenspace_rotation", R*D*R.T == D and R*g*R.T == g,
        "Orthogonal rotation in the repeated eigenspace leaves T and functional sums invariant.")

# Local jets at the center of the square for five Neumann Laplace modes.
# The corners exclude this square from the theorem; this tests exact pointwise algebra only.
cols = []
for a,b in [(2,0),(0,2),(1,1),(1,0),(0,1)]:
    u=s.cos(a*s.pi*x)*s.cos(b*s.pi*y)
    cols.append(s.Matrix([s.diff(u,x,2),s.diff(u,y,2),2*s.diff(u,x,y),s.diff(u,x),s.diff(u,y)]).subs({x:s.Rational(1,2),y:s.Rational(1,2)}))
jets=s.Matrix.hstack(*cols)
require("finite_full_jet_matrix_at_symmetry_point", s.simplify(jets.det()) != 0,
        "At center, even axial modes supply diagonal Hessians, odd-odd supplies mixed Hessian, odd axial modes supply gradients; multiplicities do not destroy excitation.")

# Ridge identity and its limiting bias are exact algebra, not a numerical conditioning claim.
a0,l0=s.symbols("a0 l0", positive=True)
th=s.symbols("theta", real=True)
est=a0*th/(a0+l0)
require("ridge_error_identity", s.simplify(est-th + l0*th/(a0+l0)) == 0,
        "For fixed positive coercivity, λ→0 suffices; no relationship to an estimation rate is needed.")
require("ridge_fixed_coercivity_limit", s.limit(est,l0,0,dir="+")==th,
        "No coefficient-uniform coercivity or finite-sample conditioning guarantee is inferred.")

# Countercontrol for the deliberately stronger deterministic hypotheses.
n=s.symbols("n",positive=True,integer=True)
opnorm=s.pi/n
secondrow=n*s.sqrt(s.pi)
require("H_to_H_does_not_imply_H_to_C2", s.limit(opnorm,n,s.oo)==0 and s.limit(secondrow,n,s.oo)==s.oo,
        "On (0,2π), rank-one kernel n⁻¹cos(nx)cos(ny) has op normπ/n while its second-derivative row norm is n√π. This is excluded by TURN_1 hypothesis3.")

require("g_h_continuity_at_zero", s.limit(x*x*s.log(x),x,0,dir="+")==0,
        "h(0)=0; no log of a zero or negative value is taken.")

runtime=[]
seen=set()
for module in list(sys.modules.values()):
    name=getattr(module,"__file__",None)
    if name:
        p=pathlib.Path(name).resolve()
        if p.is_file() and str(p) not in seen:
            seen.add(str(p));b=p.read_bytes()
            runtime.append({"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"launch_mode":oct(p.stat().st_mode&0o777)})
result={"status":"PASS_INDEPENDENT_EXACT_ALGEBRA_AND_EXCLUDED_COUNTERCONTROL",
        "utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"pid":os.getpid(),
        "argv":sys.argv,"cwd":os.getcwd(),"executable":sys.executable,"python":sys.version,
        "sympy":s.__version__,"checks":len(tests),"tests":tests,
        "limits":"Finite exact controls do not prove elliptic regularity, stochastic convergence, priority, or source scope."}
(here/"INDEPENDENT_CONTROLS_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
(here/"RUNTIME_MODULE_INVENTORY.json").write_text(json.dumps(sorted(runtime,key=lambda v:v["path"]),indent=2)+"\n")
print(json.dumps(result,indent=2))
