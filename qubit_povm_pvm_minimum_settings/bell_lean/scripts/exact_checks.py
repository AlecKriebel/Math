#!/usr/bin/env python3
"""Independent exact algebra/regression checks. This is NOT a Lean kernel check.

Requires SymPy. Writes an auditable JSON report and the full 36-entry witness
probability table. A failed identity raises an exception and exits nonzero.
"""
from __future__ import annotations

import csv
import hashlib
import itertools
import json
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "exact_checks.json"
checks: list[dict[str, object]] = []
started = time.monotonic()
REPORT.parent.mkdir(exist_ok=True)
REPORT.write_text(json.dumps({"all_checks_passed":False,"status":"in_progress",
                            "lean_kernel_checked":False},indent=2)+"\n")

def record_failure(exc_type, exc_value, traceback) -> None:
    REPORT.write_text(json.dumps({"all_checks_passed":False,"status":"failed",
        "lean_kernel_checked":False,"error":str(exc_value),
        "completed_checks":checks,"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+"\n")
    sys.__excepthook__(exc_type, exc_value, traceback)

sys.excepthook=record_failure


def zero(name: str, expression: object) -> None:
    t = time.monotonic()
    if isinstance(expression, s.MatrixBase):
        residuals = [s.simplify(s.expand(v)) for v in expression]
        passed = all(v == 0 for v in residuals)
    else:
        residuals = [s.simplify(s.expand(expression))]
        passed = residuals[0] == 0
    if not passed:
        raise AssertionError(f"{name}: nonzero residual {residuals}")
    checks.append({"name": name, "kind": "exact_identity", "passed": True,
                   "seconds": round(time.monotonic()-t, 6)})


def fact(name: str, condition: bool, kind: str = "exact_finite_check") -> None:
    if condition is not True and condition is not s.true:
        raise AssertionError(f"{name}: condition was {condition!r}")
    checks.append({"name": name, "kind": kind, "passed": True})


R = s.Rational
sqrt2 = s.sqrt(2)
I = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Z = s.diag(1, -1)
M = [s.Matrix([[16, -4], [-4, 1]])/25,
     s.Matrix([[1, -4], [-4, 16]])/25,
     s.Matrix([[8, 8], [8, 8]])/25]
G = [s.Matrix([[R(4, 5), -R(1, 5)], [0, 0]]),
     s.Matrix([[R(1, 5), -R(4, 5)], [0, 0]]),
     s.Matrix([[R(2, 5), R(2, 5)], [R(2, 5), R(2, 5)]])]
for j in range(3):
    zero(f"auxiliary_gram_{j}", G[j].H*G[j]-M[j])
    zero(f"auxiliary_rank_one_{j}", M[j].det())
    zero(f"auxiliary_scaled_idempotence_{j}", M[j]*M[j]-s.trace(M[j])*M[j])
zz, xxpolar = s.symbols("polar_z polar_x", real=True)
polar=s.Matrix([[1+zz,xxpolar],[xxpolar,1-zz]])/2
zero("polar_idempotence_defect_universal", polar*polar-polar-(zz**2+xxpolar**2-1)*I/4)
zero("polar_complement_universal", polar+polar.subs({zz:-zz,xxpolar:-xxpolar})-I)
zero("auxiliary_normalization", sum(M, s.zeros(2))-I)
fact("auxiliary_not_projective", M[0]*M[0] != M[0])

rho = s.Matrix([[R(1,2),0,0,R(1,2)], [0,0,0,0],
                [0,0,0,0], [R(1,2),0,0,R(1,2)]])
state_gram = s.Matrix([[R(1,2),0,0,R(1,2)], [R(1,2),0,0,R(1,2)]])
zero("state_gram", state_gram.H*state_gram-rho)
zero("state_normalization", s.trace(rho)-1)
zero("state_purity", rho*rho-rho)

AA = [(Z+X)/sqrt2, (Z-X)/sqrt2]
BB = [Z, X]
alice = [[(I+A)/2, (I-A)/2, s.zeros(2)] for A in AA]+[M]
bob = [[(I+B)/2, (I-B)/2] for B in BB]
for x, A in enumerate(AA):
    zero(f"alice_observable_unitary_{x}", A*A-I)
for y, B in enumerate(BB):
    zero(f"bob_observable_unitary_{y}", B*B-I)
for x in range(2):
    for a in range(2):
        zero(f"alice_binary_gram_{x}_{a}", alice[x][a].H*alice[x][a]-alice[x][a])
for y in range(2):
    for b in range(2):
        zero(f"bob_binary_gram_{y}_{b}", bob[y][b].H*bob[y][b]-bob[y][b])

p = {(x,y,a,b): s.simplify(s.trace(rho*s.kronecker_product(alice[x][a],bob[y][b])))
     for x,y,a,b in itertools.product(range(3),range(2),range(3),range(2))}
fact("all_36_probabilities_nonnegative", all(v.is_nonnegative is True for v in p.values()))
for x,y in itertools.product(range(3),range(2)):
    zero(f"normalization_{x}_{y}", sum(p[x,y,a,b] for a in range(3) for b in range(2))-1)
for x,a in itertools.product(range(3),range(3)):
    zero(f"no_signaling_A_{x}_{a}", sum(p[x,0,a,b]-p[x,1,a,b] for b in range(2)))
for y,b in itertools.product(range(2),range(2)):
    for x in (1,2):
        zero(f"no_signaling_B_{x}_{y}_{b}", sum(p[x,y,a,b]-p[0,y,a,b] for a in range(3)))

def corr(x: int, y: int) -> s.Expr:
    return s.simplify(sum(((-1) if a == 1 else 1)*((-1) if b == 1 else 1)*p[x,y,a,b]
                          for a in range(3) for b in range(2)))

for x,y,sign in [(0,0,1),(0,1,1),(1,0,1),(1,1,-1)]:
    zero(f"correlation_{x}_{y}", corr(x,y)-sign*sqrt2/2)
for name, key in [("00",(2,0,0,0)),("11",(2,0,1,1)),("20",(2,1,2,0))]:
    zero(f"auxiliary_probability_{name}", p[key]-R(8,25))
score = 10*(corr(0,0)+corr(0,1)+corr(1,0)-corr(1,1)) + R(3,5)*p[2,0,0,0] + R(3,5)*p[2,0,1,1] + R(4,5)*p[2,1,2,0]
lower = 20*sqrt2+R(16,25)
upper = 20*sqrt2+R(3,5)+(4+3*sqrt2)/250
zero("witness_Bell_value", score-lower)
zero("exact_gap_identity", lower-upper-3*(2-sqrt2)/250)
fact("gap_positive_exact", (lower-upper).is_positive is True)

W = [R(3,20)*(I+Z), R(3,20)*(I-Z), (I+X)/5]
Gamma = R(8,25)*I+R(2,25)*X
slack_grams = [s.Matrix([[R(1,10),R(4,10)]]*2),
               s.Matrix([[R(4,10),R(1,10)]]*2),
               s.Matrix([[R(1,5),-R(1,5)]]*3)]
for j in range(3):
    zero(f"dual_slack_gram_{j}", slack_grams[j].H*slack_grams[j]-(Gamma-W[j]))
    zero(f"dual_complementarity_{j}", (Gamma-W[j])*M[j])
zero("dual_trace_value", s.trace(Gamma)-R(16,25))
zero("primal_discrimination_value", sum(s.trace(W[j]*M[j]) for j in range(3))-R(16,25))
generic0=s.Matrix(2,2,s.symbols("u0:4",real=True))
generic1=s.Matrix(2,2,s.symbols("v0:4",real=True))
genericN=[generic0,generic1,I-generic0-generic1]
slack_vectors=[s.Matrix([1,4]),s.Matrix([4,1]),s.Matrix([1,-1])]
slack_weights=[R(1,50),R(1,50),R(3,25)]
slack_value=sum(slack_weights[j]*(slack_vectors[j].T*genericN[j]*slack_vectors[j])[0] for j in range(3))
zero("ideal_weak_duality_linear_certificate_universal",
     R(16,25)-sum(s.trace(W[j]*genericN[j]) for j in range(3))-slack_value)
for i,j in itertools.combinations(range(3),2):
    diff=W[i]-W[j]
    trace_norm=s.sqrt(s.trace(diff)**2-4*diff.det())
    fact(f"ideal_pair_opposite_eigenvalue_signs_{i}_{j}", diff.det() <= 0)
    zero(f"ideal_pair_score_{i}_{j}", (s.trace(W[i])+s.trace(W[j])+trace_norm)/2-R(3,5))

eta,x,y,r,q,u,k,t=s.symbols("eta x y r q u k t", real=True)
D=(-1+eta*(3*x-4*y))**2+24*(1-eta**2)*(1-r)
H=8-3*x-4*y
cert=2*eta*(eta*(8*(1-y)*(4-3*x)+12*(1-r))+(q-1)*H+8*(1-y))
zero("robust_square_identity_universal", (q+eta*H)**2-D-(q**2-(25-24*r))-cert)
zero("u_robust_square", (5+8*u)**2-(25+24*u)-8*u*(7+8*u))
zero("deficit_one", (1-u**2/2)**2-(1-u**2)-u**4/4)
zero("deficit_four", (2-u**2/4)**2-(4-u**2)-u**4/16)
zero("complete_square", k**2/40-(k*t-10*t**2)-(k-20*t)**2/40)
zero("kappa_square", (R(2,5)*(1+sqrt2)*s.sqrt(sqrt2))**2-(16+12*sqrt2)/25)
zero("strengthened_family_Cauchy_identity", (500*t+4*eta)**2+(4*t-500*eta)**2-(500**2+4**2)*(t**2+eta**2))
fact("strengthened_comparison_square_certificate", 64*7813 > 500**2*2)

# Lorentz / projective-fiber polynomial identities.
a,b,c,d=s.symbols("a b c d", real=True)
e=a+b+c+d-R(1,2)
g=s.Matrix([[0,R(1,2),a,b],[R(1,2),0,c,d],[a,c,0,e],[b,d,e,0]])
rays=[s.eye(4)[:,i] for i in range(4)]+[s.Matrix([1,1,-1,-1])]
uvec=s.Matrix([1,1,0,0])
zero("binary_circuit", rays[0]+rays[1]-uvec)
zero("ternary_circuit", rays[2]+rays[3]+rays[4]-uvec)
for j,v in enumerate(rays):
    zero(f"coefficient_ray_null_{j}", (v.T*g*v)[0])
zero("metric_normalization", (uvec.T*g*uvec)[0]-1)
raymatrix=s.Matrix.hstack(*rays)
fact("circuit_rank", raymatrix.rank()==4)
zero("circuit_kernel_vector", raymatrix*s.Matrix([1,1,-1,-1,-1]))
outermatrix=s.Matrix.hstack(*[s.Matrix(16,1,list(v*v.T)) for v in rays])
fact("five_outer_products_independent", outermatrix.rank()==5)

xx=s.Matrix(s.symbols("x0:4", real=True))

def phi(v: s.Matrix) -> s.Matrix:
    return s.Matrix([v[2]*(v[0]+v[3]),v[3]*(v[0]+v[2]),
                     v[2]*(v[1]+v[3]),v[3]*(v[1]+v[2])])

def invpoly(v: s.Matrix) -> s.Matrix:
    det=v[0]*v[3]-v[1]*v[2]
    return s.Matrix([(v[0]-v[1])*(v[0]-v[2])*(v[1]-v[3]),
                     (v[2]-v[3])*(v[0]-v[2])*(v[1]-v[3]),
                     det*(v[0]-v[2]),det*(v[1]-v[3])])

omega=xx[2]*xx[3]*(xx[2]-xx[3])*(xx[0]-xx[1])**2
zero("generic_inverse_universal", invpoly(phi(xx))-omega*xx)
zero("inverse_homogeneous_universal", invpoly(t*xx)-t**3*invpoly(xx))
for j,v in enumerate(rays):
    zero(f"base_line_Phi_zero_{j}", phi(t*v))
v=s.Matrix([-1,-1,t,1])
zero("cross_x2", (v.T*g*v)[0]-(1-2*(b+d))*(1-t))
v=s.Matrix([-1,-1,1,t])
zero("cross_x3", (v.T*g*v)[0]-(1-2*(a+c))*(1-t))

A,B,U,V,pp,qq=s.symbols("A B U V p q", real=True)
N01=1+2*A*pp+2*B*qq+2*(A+B-R(1,2))*pp*qq
R01=V*pp*(1+qq)-U*qq*(1+pp)
N23=pp*qq+2*A*pp+2*B*qq+2*(A+B-R(1,2))
R23=V*(pp+1)-U*(qq+1)
zero("resultant01_universal", s.resultant(N01,R01,pp)+(qq+1)*(V+qq*(U*(2*A-1)+2*V*B)))
zero("resultant23_universal", s.resultant(N23,R23,pp)+(qq+1)*(U*qq+2*U*A+2*V*B-V))
zero("exception01_base_factor", N01.subs(qq,-1)-(1-2*B)*(1+pp))
zero("exception23_base_factor", N23.subs(qq,-1)-(2*A-1)*(1+pp))
zero("coefficient_obstruction01", 2*B*(2*A+2*(A+B-R(1,2))*qq)-2*(A+B-R(1,2))*(1+2*B*qq)-(2*A-1)*(2*B-1))
zero("coefficient_obstruction23", 2*B*(qq+2*A)-(2*B*qq+2*(A+B-R(1,2)))-(2*A-1)*(2*B-1))

# General symbolic, rather than sampled, 4-dimensional Hessian square completion.
def symmetric_matrix(prefix: str) -> s.Matrix:
    syms={(i,j):s.Symbol(f"{prefix}{i}{j}", real=True) for i in range(4) for j in range(i,4)}
    return s.Matrix(4,4,lambda i,j:syms[min(i,j),max(i,j)])
Q=symmetric_matrix("Q")
Hm=symmetric_matrix("H")
z=s.Matrix(s.symbols("z0:4", real=True))
dx=z+Hm*Q*xx
hessian=(dx.T*Q*dx-2*dx.T*Q*Hm*Q*xx+xx.T*Q*Hm*Q*Hm*Q*xx-z.T*Q*z)[0]
zero("inverse_Hessian_square_completion_general_4d", hessian)

# Universal symbolic transport identities.
c01,c02,c12,d0,d1,tt=s.symbols("c01 c02 c12 d0 d1 t", real=True)
C=s.Matrix([[0,c01,c02],[c01,0,c12],[c02,c12,0]])
F=s.Matrix([[0,c01/2+tt,c02/2+d0-tt],
            [c01/2-tt,0,c12/2+d1+tt],
            [c02/2-d0+tt,c12/2-d1-tt,0]])
ds=[d0,d1,-d0-d1]
a0=[sum(C[i,j] for j in range(3))/2-ds[i] for i in range(3)]
b0=[sum(C[i,j] for j in range(3))/2+ds[i] for i in range(3)]
zero("transport_skew_complement", C-F-F.T)
for i in range(3):
    zero(f"transport_row_identity_{i}",sum(F[i,j] for j in range(3))-b0[i])
    zero(f"transport_column_identity_{i}",sum(F[j,i] for j in range(3))-a0[i])

# Boundary-inclusive exact rational regressions of the max-endpoint algorithm.
regressions=0
N=8
for edge01_count in range(N+1):
  for edge02_count in range(N+1-edge01_count):
    edges=[Fraction(edge01_count,2*N),Fraction(edge02_count,2*N),
           Fraction(N-edge01_count-edge02_count,2*N)]
    cc=[[Fraction(0),edges[0],edges[1]],
        [edges[0],Fraction(0),edges[2]],
        [edges[1],edges[2],Fraction(0)]]
    for signs in itertools.product((-1,0,1),repeat=3):
      f01=signs[0]*edges[0]/2
      f02=signs[1]*edges[1]/2
      f12=signs[2]*edges[2]/2
      ff=[[0,f01,f02],[-f01,0,f12],[-f02,-f12,0]]
      ref=[[cc[i][j]/2+ff[i][j] for j in range(3)] for i in range(3)]
      aa=[sum(ref[i][j] for i in range(3)) for j in range(3)]
      bb=[sum(row) for row in ref]
      dd=[(bb[i]-aa[i])/2 for i in range(3)]
      lo=[-edges[0]/2,dd[0]-edges[1]/2,-dd[1]-edges[2]/2]
      hi=[edges[0]/2,dd[0]+edges[1]/2,-dd[1]+edges[2]/2]
      chosen=max(lo)
      assert chosen<=min(hi), {"edges":edges,"lower":lo,"upper":hi}
      f01=chosen
      f02=dd[0]-chosen
      f12=dd[1]+chosen
      flow=[[0,edges[0]/2+f01,edges[1]/2+f02],
            [edges[0]/2-f01,0,edges[2]/2+f12],
            [edges[1]/2-f02,edges[2]/2-f12,0]]
      assert all(0<=flow[i][j]<=cc[i][j] for i,j in itertools.product(range(3),repeat=2))
      assert [sum(row) for row in flow]==bb
      assert [sum(flow[i][j] for i in range(3)) for j in range(3)]==aa
      assert sum(aa)==sum(bb)==Fraction(1,2)
      mix={(x,y,a,b):Fraction(0) for x,y,a,b in itertools.product(range(2),range(2),range(3),range(3))}
      for branch,i,j in itertools.product(range(2),range(3),range(3)):
          weight=flow[i][j] if branch==0 else cc[i][j]-flow[i][j]
          a_out=[branch,i]
          b_out=[1-branch,j]
          for x,y in itertools.product(range(2),repeat=2):
              mix[x,y,a_out[x],b_out[y]]+=weight
      for x,y,a,b in mix:
          if x==0 and y==0:
              target=Fraction(1,2) if (a,b) in ((0,1),(1,0)) else Fraction(0)
          elif x==0:
              target=aa[b] if a==0 else bb[b] if a==1 else Fraction(0)
          elif y==0:
              target=aa[a] if b==0 else bb[a] if b==1 else Fraction(0)
          else:
              target=cc[a][b]
          assert mix[x,y,a,b]==target
      regressions+=1
fact("transport_boundary_regressions",regressions==1215,"exact_rational_regression_suite")
fact("all_transport_mixture_blocks",regressions*36==43740,"exact_rational_regression_suite")

(ROOT/"reports").mkdir(exist_ok=True)
with (ROOT/"reports"/"witness_probabilities.csv").open("w", newline="") as file:
    writer=csv.writer(file)
    writer.writerow(["alice_input","bob_input","alice_output","bob_output","exact_probability"])
    for key,value in sorted(p.items()):
        writer.writerow([*key,str(value)])

expected="1a408e9d98f5166e8ffa6adf607413132facb51fa6f8d3108843b5f0280f2c66"
paper=ROOT/"source"/"paper_july2026_library.pdf"
actual=hashlib.sha256(paper.read_bytes()).hexdigest()
fact("paper_hash_matches_v1_1_0_release",actual==expected)
report={
  "tool":"Python / SymPy; NOT Lean",
  "python_version":platform.python_version(),
  "sympy_version":s.__version__,
  "lean_kernel_checked":False,
  "full_paper_formalized":False,
  "scope":"Concrete strategy, universal algebraic identities, and rational transport regressions only",
  "check_count":len(checks),
  "transport_regression_instances":regressions,
  "transport_probability_entries_compared":regressions*36,
  "all_checks_passed":True,
  "elapsed_seconds":round(time.monotonic()-started,3),
  "source_pdf_sha256":actual,
  "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  "lean_source_hashes":{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()
                         for f in sorted(ROOT.rglob("*.lean")) if ".lake" not in f.parts},
  "checks":checks,
}
REPORT.write_text(json.dumps(report,indent=2)+"\n")
print(f"PASS: {len(checks)} exact algebra/finite checks; {regressions} rational transport regressions")
print("Lean kernel verification: NOT RUN. Full-paper formalization: INCOMPLETE.")
print(f"Report: {REPORT}")
