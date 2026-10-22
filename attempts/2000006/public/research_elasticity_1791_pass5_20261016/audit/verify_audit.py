#!/usr/bin/env python3
"""Independent auxiliary algebra and frozen-chain controls, not a benchmark proof."""
import hashlib
import json
from pathlib import Path
import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PASS = HERE.parent
checks = []

def check(name, condition, kind="exact algebra"):
    assert bool(condition), name
    checks.append({"name": name, "kind": kind, "passed": True})

def zero(name, expression):
    if isinstance(expression, S.MatrixBase):
        check(name, all(S.simplify(x) == 0 for x in expression))
    else:
        check(name, S.simplify(expression) == 0)

def colon(A, B):
    return sum(x*y for x, y in zip(A, B))

t = S.symbols("t", real=True)
F = S.Matrix(3, 3, S.symbols("f0:9"))
A = S.Matrix(3, 3, S.symbols("a0:9"))
J, j = F.det(), A.det()
M1, M2 = colon(F.cofactor_matrix(), A), colon(A.cofactor_matrix(), F)
path = ((1-t)*F+t*A).det()
zero("full compatible determinant Bernstein polynomial", S.expand(path-((1-t)**3*J+t*(1-t)**2*M1+t**2*(1-t)*M2+t**3*j)))
zero("first mixed derivative", S.expand(S.diff(path, t).subs(t, 0)-M1+3*J))
zero("reversal of mixed coefficients", S.expand(path.subs(t, 1-t)-((1-t)*A+t*F).det()))
secant = ((1-t)**-6-1)/t
zero("integrable upper secant expansion", secant-sum((1-t)**-k for k in range(1, 7)))
zero("secant bound 126 at one half", secant.subs(t, S.Rational(1, 2))-126)
zero("limiting coupled barrier source six", S.limit(secant, t, 0)-6)
u = S.Matrix(S.symbols("u0:3")); v = S.Matrix(S.symbols("v0:3"))
rank1 = F+u*v.T
zero("rank-one first mixed coefficient", S.expand(colon(F.cofactor_matrix(), rank1)-2*J-rank1.det()))
zero("rank-one second mixed coefficient", S.expand(colon(rank1.cofactor_matrix(), F)-J-2*rank1.det()))
zero("rank-one residual source two", 6-2*2-2)
ss, qq = S.symbols("ss qq", positive=True)
radial = S.diag(ss, ss, ss*qq)
zero("radial divergent mixed-moment formula", S.trace(radial.cofactor_matrix())/radial.det()**3-ss**-7*(1+2*qq)/qq**3)
zero("radial mixed-moment power", 2-7*S.Rational(1, 2)+S.Rational(3, 2))
zero("positive-energy Young coefficient", 1+S.Rational(5, 6)-S.Rational(11, 6))
bad = S.diag(-2, -S.Rational(1, 2), 1)
zero("positive determinant does not enforce first mixed sign", S.trace(bad.cofactor_matrix())+S.Rational(3, 2))
zero("positive determinant does not enforce second mixed sign", S.trace(bad)+S.Rational(3, 2))
check("mixed-sign diagnostic remains orientation preserving", bad.det() == 1)

K, Ke, d, lam, kap, C0 = S.symbols("K Ke d lam kap C0", positive=True)
zero("inverse barrier first variation sign", S.diff(d*((1-t)*K+t*Ke)**3, t).subs(t, 0)-3*d*K**2*(Ke-K))
zero("compensated determinant threshold", 3*d*((kap**2+C0/(3*d))-kap**2)-C0)
g1, g2, g3 = S.symbols("g1 g2 g3", real=True)
e1 = S.Matrix([1, 0, 0]); grad = S.Matrix([g1, g2, g3])
At = S.eye(3)+t*e1*grad.T
kt = 1+t*g1
zero("triangular determinant", At.det()-kt)
zero("triangular inverse", At.inv()-(S.eye(3)-t/kt*e1*grad.T))
Ft = S.Matrix([[2, 1, 0], [0, 3, 1], [1, 0, 2]])
zero("finite material cofactor transport", (Ft*At.inv()).cofactor_matrix()-(Ft.cofactor_matrix()+t*(Ft.cofactor_matrix()*grad)*e1.T)/kt)
a, b, c, sh = S.symbols("a b c sh", positive=True)
shear = S.eye(3)+sh*e1*S.Matrix([[0, 1, 0]])
B = shear.T*shear; tr = S.trace(B)
cof_norm2 = colon(shear.cofactor_matrix(), shear.cofactor_matrix())
U = 6*a*tr**2*B+3*b*S.sqrt(cof_norm2)*(tr*B-B*B)+2*c*S.eye(3)
zero("shear norm agreement", cof_norm2-tr)
zero("signed shear first-cost coefficient", -U[0, 1]+(6*a*(3+sh**2)**2+3*b*S.sqrt(3+sh**2))*sh)

m, alpha2, alpha3, beta, delta = S.symbols("m alpha2 alpha3 beta delta", positive=True)
total = m+alpha2+alpha3
gamma = total-3
zero("whole-density barrier normalization", 2*gamma+6*(m-1)-2*(total+3*m-6))
zero("strain-normalized barrier exponent", -2*gamma-6*(m-1)-2*(6-total-3*m))
zero("balance gives zero barrier exponent", (2*(6-total-3*m)).subs(alpha3, 6-4*m-alpha2))
zero("annular strain-integral exponent", 3+6*(m-1)-(6*m-3))
zero("annular barrier-integral exponent", 3-2*gamma-(9-2*total))
zero("three equal balanced weights force m one", (total+3*m-6).subs({alpha2:m, alpha3:m})-6*(m-1))
zero("scalar removable-puncture flux exponent", 2+5*(m-1)-(5*m-3))
zero("scalar spherical critical coefficient", (m*(5*m-3)).subs(m, S.Rational(3, 5)))
C, p2, p3, q2, q3 = S.symbols("C p2 p3 q2 q3", real=True)
critical = S.Matrix([[C*m, 0, 0], [1, p2, q2], [2, p3, q3]])
zero("critical angular determinant wedge coefficient", critical.det()-C*m*(p2*q3-q2*p3))
r, q = S.symbols("r q", positive=True)
gam = 2*m+beta-3
zero("critical-axis pure-barrier stress gap", (4*m+beta-5)-(2*m-2-3*gam)-4*gam)
angle = 1-q*q*r**(-2*m)
angular = r**gam*(1-angle)*(m+(beta-3*m)*angle)
fiber = q*q*((beta-2*m)*r**(beta-3)-(beta-3*m)*q*q*r**(beta-2*m-3))
zero("critical-axis fiber determinant", S.powsimp(angular-fiber, force=True))
zero("critical-axis exceptional second coefficient", ((beta-3*m)*(beta-2*m-3)).subs(beta, 3)-6*m*(m-1))
zero("critical-axis exceptional gamma violates finite energy", gam.subs({m:1, beta:3})-2)
theta, eps = S.symbols("theta eps", positive=True)
zero("polar concentration primitive", S.diff(-1/(2*(theta**2+eps)), theta)-theta/(theta**2+eps)**2)
check("subcritical repaired example parameter signs", all(x>0 for x in [S.Rational(3,5)-S.Rational(1,2), 2-2*S.Rational(3,5), 2*S.Rational(3,5)+2-3, 3-2*S.Rational(1,5)-S.Rational(1,4), 6-(5*S.Rational(3,5)+2)]))

for rank, H, Bdiag, answer in [(1,S.diag(-2,-1,1),S.diag(1,0,0),-1),(2,S.diag(-2,1,-1),S.diag(1,1,0),-2)]:
    check(f"universal rank-{rank} obstruction uses positive input", H.det()>0)
    zero(f"universal rank-{rank} output sign", (S.eye(3)+Bdiag*H).det()-answer)
check("invertible mixed graph can be singular", (S.eye(3)+S.diag(-1,-1,1)).det()==0)
L = S.log(S.E/r)
p = L**S.Rational(2,3)
zero("critical scalar pressure derivative", S.diff(p,r)+S.Rational(2,3)/(r*L**S.Rational(1,3)))
qf = S.Function("qf")(r)
zero("radial pressure tensor integrating factor", S.diff(r*r*qf,r)/r**2-S.diff(qf,r)-2*qf/r)
zero("formal critical determinant", p**(-S.Rational(1,2))-L**(-S.Rational(1,3)))
alpha, T = S.symbols("alpha T", positive=True)
zero("non-Dini product exponent", -2*alpha+1-alpha-(1-3*alpha))
zero("logarithmic endpoint exponent", (1-3*alpha).subs(alpha,S.Rational(1,3)))
zero("critical tensor asymptotic via derivative quotient", S.limit((S.Rational(2,3)*r*L**(-S.Rational(1,3)))/S.diff(r*r*L**(-S.Rational(1,3)),r),r,0)-S.Rational(1,3))

target = ROOT/"recovery_elasticity_1791_20261015/formulation_gate/RESEARCH_TARGET.md"
check("frozen target bytes and hash", len(target.read_bytes())==5042 and hashlib.sha256(target.read_bytes()).hexdigest()=="66006f5870581093313e1906c245c009c6738a2845b5fa674da03eb934baf8f9", "integrity")

def entries(value):
    if isinstance(value, dict):
        if "path" in value and "sha256" in value:
            yield value
        for child in value.values():
            yield from entries(child)
    elif isinstance(value, list):
        for child in value:
            yield from entries(child)

prior=[]
for number in range(1,5):
    manifest=ROOT/f"research_elasticity_1791_pass{number}_20261016/audit/AUDIT_MANIFEST.json"
    records=list(entries(json.loads(manifest.read_text())))
    for record in records:
        data=(ROOT/record["path"]).read_bytes()
        assert hashlib.sha256(data).hexdigest()==record["sha256"],record["path"]
        if "bytes" in record:
            assert len(data)==record["bytes"],record["path"]
    check(f"sealed pass-{number} manifest entries unchanged", len(records)>0, "integrity")
    prior.append({"pass":number,"bound_entries_verified":len(records),"manifest_sha256":hashlib.sha256(manifest.read_bytes()).hexdigest()})
check("all 85 prior manifest entries verified",sum(x["bound_entries_verified"] for x in prior)==85,"integrity")
source=json.loads((PASS/"literature/SOURCE_INSPECTION_MANIFEST.json").read_text())["new_source"]
check("new primary-source inspection limitations preserved",source["local_pdf_retrieved"] is False and source["pdf_sha256"] is None and source["visual_inspection"] is False,"metadata control")
repro=json.loads((HERE/"REPRODUCTION_CHECKS.json").read_text())
check("independent exact mirror output byte-identical",repro["exact"]["byte_identical_output"] and repro["exact"]["stdout"]["total_exact_checks"]==201 and repro["exact"]["stdout"]["prior_quadrature_checks"]==14,"execution control")
check("independent positivity mirror output byte-identical",repro["positivity"]["byte_identical_output"] and repro["positivity"]["symbolic_check_count"]==28,"execution control")

result={"problem":"E-6322","pass":5,"purpose":"Independent auxiliary algebra, negative controls and frozen-chain integrity; analytical proofs reviewed separately.","total_checks":len(checks),"checks":checks,"prior_manifest_verification":prior,"prior_bound_entries_verified":sum(x["bound_entries_verified"] for x in prior),"benchmark_proved":False,"benchmark_counterexample":False,"terminal_status":"UNSOLVED 5/5"}
(HERE/"AUDIT_CHECKS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"passed":True,"total_checks":len(checks),"prior_bound_entries_verified":result["prior_bound_entries_verified"]},indent=2))
