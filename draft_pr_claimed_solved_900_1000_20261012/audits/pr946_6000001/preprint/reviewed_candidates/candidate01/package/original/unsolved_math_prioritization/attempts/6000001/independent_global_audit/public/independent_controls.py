#!/usr/bin/env python3
"""Independent algebraic controls for the frozen statistical embedding proof.

Written without importing or inspecting the candidate's verification program.
Finite algebraic controls supplement, and do not replace, the mathematical audit.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
checks = []

def record(name, assertions, details):
    checks.append({"name": name, "passed": True, "assertions": assertions, "details": details})

def zero(v):
    assert s.simplify(v) == 0, v

# 1. All smooth scalar metric and cubic data in dimension one.
t = s.symbols('t', real=True)
g = s.Function('g')(t)
c = s.Function('c')(t)
gam = (s.diff(g,t)-c)/2
q = s.diff(g,t)+gam
f = s.Matrix([1,t,t*t,t**3])
a = s.Matrix([g*t*t/2-q*t**3/6, -g*t+q*t*t/2, g/2-q*t/2, q/6])
phi = -a
for expression in [a.dot(f), a.dot(f.diff(t)), a.dot(f.diff(t,2))-g,
                   a.dot(f.diff(t,3))-q, phi.dot(f.diff(t)),
                   f.diff(t).dot(phi.diff(t))-g,
                   f.diff(t,2).dot(phi.diff(t))-gam,
                   f.diff(t).dot(phi.diff(t,2))-(s.diff(g,t)+c)/2]:
    zero(expression)
E1 = s.Matrix.vstack(*[f.diff(t,k).T for k in range(4)])
assert s.factor(E1.det()) == 12
assert E1[:,0:3].rank() == 3
record('arbitrary_smooth_one_dimensional_data',10,
       'Exact identities hold for unspecified smooth g(t) and c(t); induced connection ordering is checked. Cubic features have determinant 12, while degree at most two fails 3-jet surjectivity.')

# 2. Full nonlinear coordinate change for a nonconstant two-dimensional metric.
x,y,u,v = s.symbols('x y u v', real=True)
xs = [x,y]; us = [u,v]
h = [u+v*v,v+u*u]
J = s.Matrix(h).jacobian(us)
metric = s.Matrix([[2+x*x,x*y],[x*y,3+y*y]])
Cs = [1+x,y,x-y,2+x*y]
def C(i,j,k): return Cs[i+j+k]
def Q(i,j,k):
    return (s.diff(metric[j,k],xs[i])+s.diff(metric[i,k],xs[j])+s.diff(metric[i,j],xs[k])-C(i,j,k))/2
sub = {x:h[0],y:h[1]}
metric_u = J.T*metric.subs(sub)*J
ncheck = 0
for a1,b1,c1 in itertools.product(range(2),repeat=3):
    transformed_c = sum(J[i,a1]*J[j,b1]*J[k,c1]*C(i,j,k).subs(sub)
                        for i,j,k in itertools.product(range(2),repeat=3))
    ordinary_q = (s.diff(metric_u[b1,c1],us[a1])+s.diff(metric_u[a1,c1],us[b1])
                  +s.diff(metric_u[a1,b1],us[c1])-transformed_c)/2
    chain_q = sum(J[i,a1]*J[j,b1]*J[k,c1]*Q(i,j,k).subs(sub)
                  for i,j,k in itertools.product(range(2),repeat=3))
    chain_q += sum(metric[i,j].subs(sub)*(
        s.diff(h[i],us[a1],us[b1])*J[j,c1]
        +s.diff(h[i],us[a1],us[c1])*J[j,b1]
        +s.diff(h[i],us[b1],us[c1])*J[j,a1])
        for i,j in itertools.product(range(2),repeat=2))
    zero(s.expand(ordinary_q-chain_q)); ncheck += 1
# At origin Q_001 picks up 6: Q is not a tensor.
extra = sum(metric[i,j].subs({x:0,y:0})*(
    s.diff(h[i],u,u)*s.diff(h[j],v)+s.diff(h[i],u,v)*s.diff(h[j],u)
    +s.diff(h[i],u,v)*s.diff(h[j],u)).subs({u:0,v:0})
    for i,j in itertools.product(range(2),repeat=2))
assert extra == 6
record('nonlinear_two_dimensional_jet_coordinate_change',ncheck+1,
       'All eight third-jet entries obey the scalar chain rule for x=u+v^2, y=v+u^2. A nonzero inhomogeneous term rejects the incorrect tensor-only transformation.')

# 3. Surjectivity from one common finite ambient polynomial feature space.
e = [x+x*x*y,y+x*y*y,x*x+y**3,x*y,x**3-y*y]
exponents = [a for a in itertools.product(range(4),repeat=5) if sum(a)<=3]
features = [s.prod(e[i]**a[i] for i in range(5)) for a in exponents]
indices = [(a,b) for a in range(4) for b in range(4-a)]
E = s.Matrix([[s.diff(F,x,a,y,b).subs({x:0,y:0}) for F in features] for a,b in indices])
assert len(features)==56 and E.shape==(10,56) and E.rank()==10
R = E.T*(E*E.T).inv()
assert E*R == s.eye(10)
record('ambient_polynomial_three_jet_surjectivity',4,
       'A nonlinear immersion into R^5 supplies 56 cubic-or-lower features and rank 10 scalar 3-jets; its exact Gram right inverse is checked.')

# 4. Positivity: exact Schur complement, no boundedness premise.
A = s.Matrix([[2,1],[1,3]])
B = s.Matrix([[1,-2,3],[4,1,-1]])
tau = s.trace(A.inv())*sum(z*z for z in B)
lam = 1+tau
H = A.row_join(B).col_join(B.T.row_join(2*lam*s.eye(3)))
for k in range(1,6): assert H[:k,:k].det()>0
S = 2*lam*s.eye(3)-B.T*A.inv()*B
lower = S-(2+tau)*s.eye(3)
for k in range(1,4):
    for subset in itertools.combinations(range(3), k):
        assert lower.extract(subset,subset).det() >= 0
Avar = 1/(1+t*t); Bvar=t; tauvar=(1+t*t)*t*t
zero(s.factor(2*Avar*(1+tauvar)-Bvar**2)-(t*t+2/(1+t*t)))
assert (2*Avar-Bvar**2).subs(t,2) < 0
record('normal_correction_and_noncompact_positivity',14,
       'Exact positive principal minors and the stated Schur bound pass. A varying correction works for all t, while the same example defeats a fixed normal coefficient at t=2.')

# 5. Dual connection flatness and torsion.
psi = s.exp(x)+s.exp(y)+(x+y)**2/2
G = s.hessian(psi,(x,y))
connections = [G.inv()*G.diff(w) for w in (x,y)]
curvature = connections[1].diff(x)-connections[0].diff(y)+connections[0]*connections[1]-connections[1]*connections[0]
for z in curvature: zero(z)
for k in range(2): zero(connections[0][k,1]-connections[1][k,0])
# Negative scope control: curvature-flat alone does not imply torsion-free.
Gbad = s.diag(1,s.exp(2*x))
conn_bad = [Gbad.inv()*Gbad.diff(w) for w in (x,y)]
Rbad = conn_bad[1].diff(x)-conn_bad[0].diff(y)+conn_bad[0]*conn_bad[1]-conn_bad[1]*conn_bad[0]
assert Rbad == s.zeros(2)
assert conn_bad[0][1,1]-conn_bad[1][1,0] == 2
record('dual_flatness_and_torsion_scope',8,
       'A nonconstant positive Hessian has flat torsion-free dual connection. The metric diag(1,exp(2x)) is a negative scope control: its standard-connection dual is curvature-flat but has nonzero torsion.')

# 6. Check identity of the exact frozen object and integrity of its inventory.
expected_proof='a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2'
expected_manifest='7df56d745e4c57a30d0303388b1adda3e52d1c99190d2f96fe50b6d616b1cf3f'
assert hashlib.sha256((ROOT/'public/PROOF.md').read_bytes()).hexdigest()==expected_proof
assert hashlib.sha256((ROOT/'public/MANIFEST.json').read_bytes()).hexdigest()==expected_manifest
manifest=json.loads((ROOT/'public/MANIFEST.json').read_text())
for filename,meta in manifest['files'].items():
    data=(ROOT/'public'/filename).read_bytes()
    assert len(data)==meta['bytes']
    assert hashlib.sha256(data).hexdigest()==meta['sha256']
record('frozen_proof_and_packet_identity',2+2*len(manifest['files']),
       'Proof and externally supplied manifest hashes match; every original manifest entry matches its actual byte count and digest. No candidate verification program was executed or read.')

result={"verdict":"PASS", "control_groups":len(checks), "assertions":sum(c['assertions'] for c in checks),
        "sympy_version":s.__version__, "frozen_proof_sha256":expected_proof,
        "frozen_manifest_sha256":expected_manifest,
        "limits":"These are exact algebraic and integrity controls. The noncompact global existence, smooth bundle and tubular arguments are assessed in the mathematical audit, not proved by finite tests.",
        "checks":checks}
(OUT/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
