#!/usr/bin/env python3
"""Independent exact symbolic controls. Never edits the frozen public package.

Checks all three affine charts, using polynomial identities and constant minors;
finite nilpotent examples and mutation controls are additional diagnostics only.
Dependency: SymPy. This does not establish global projectivity/Fano/Picard facts.
"""
import hashlib
import itertools
import json
import pathlib
import platform
import subprocess
import sympy as s

BASE = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = BASE / 'public'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
expected = {
    'SHA256SUMS': '1045335b31828dd4034b3bcbbac98d6c5f57d3adf4c43381ac7e2c354b097950',
    'REPORT.md': '505b4f2643830e4547222d8cf8f7cc406eac07a6ebceede059174ba20127ad95',
}
assert all(sha(PUBLIC / name) == digest for name, digest in expected.items())
for line in (PUBLIC / 'SHA256SUMS').read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    assert sha(PUBLIC / name.strip()) == digest
old = json.loads(subprocess.check_output(['python3', '-B', str(PUBLIC / 'check.py')], text=True))
assert old == json.loads((PUBLIC / 'control-results.json').read_text())

A = s.diag(2, -1, -1)
H = s.diag(0, 1, -1)
def E(i,j):
    M = s.zeros(3)
    M[i,j] = 1
    return M
W = [H, E(1,2), E(2,1)]
U = [E(0,1), E(0,2), E(1,0), E(2,0)]
basis = [A] + W + U
vec = lambda M: s.Matrix(list(M))
comm = lambda M,N: M*N-N*M
zero = s.zeros(3)
X = s.Matrix.hstack(*[vec(M) for M in basis])
assert X.rank() == 8
left_inverse = (X.T * X).inv() * X.T
def coords(M):
    c = s.simplify(left_inverse * vec(M))
    assert s.simplify(X*c-vec(M)) == s.zeros(9,1)
    return c

def quotient_coords(M, pivot, parameters):
    c = coords(M)
    # Subtract c_A A and c_pivot B; B_pivot = 1 on this chart.
    c = c - c[0] * s.Matrix([1,0,0,0,0,0,0,0])
    bp = s.Matrix([0]+parameters+[0]*4)
    c = s.simplify(c - c[1+pivot] * bp)
    return s.Matrix([c[i] for i in range(1,8) if i != 1+pivot])

x,y,z = s.symbols('x y z')
B = x*H+y*W[1]+z*W[2]
assert comm(A,B) == zero
assert B*B == s.diag(0,x*x+y*z,x*x+y*z)
right_bracket = s.Matrix.hstack(*[coords(comm(D,A))[4:,0] for D in U])
assert right_bracket == s.diag(-3,-3,3,3)
assert right_bracket.det() == 81
assert s.Matrix.hstack(*[vec(comm(A,D)) for D in U]) == -s.Matrix.hstack(*[vec(comm(D,A)) for D in U])

charts=[]
for pivot,name in enumerate(['x','y','z']):
    par=[x,y,z]
    par[pivot]=s.Integer(1)
    Bc=sum((t*M for t,M in zip(par,W)),s.zeros(3))
    other=[i for i in range(3) if i!=pivot]
    Q=[W[i] for i in other]+U
    # Tangent equation for the abelian-plane locus: [a,B]+[A,b]=0.
    J=s.Matrix.hstack(*[coords(comm(q,Bc)) for q in Q],
                      *[coords(comm(A,q)) for q in Q])
    # Two varying-B directions and the four infinitesimal conjugations.
    C=s.Matrix.hstack(*[
        s.Matrix.vstack(quotient_coords(a,pivot,par),quotient_coords(b,pivot,par))
        for a,b in [(zero,W[i]) for i in other]+[(comm(D,A),comm(D,Bc)) for D in U]
    ])
    assert s.simplify(J*C) == s.zeros(8,6)
    # Rows b_block (2) and a_offblock (4) give a constant invertible minor.
    frame_minor=s.factor(C.extract([6,7,2,3,4,5],list(range(6))).det())
    assert frame_minor == 81
    # Constant rank-six Jacobian minor: two block-a columns plus four offblock-b.
    # The two suitable block rows depend only on the normalized chart.
    rows=([2,3] if pivot==0 else [1,2] if pivot==1 else [1,3])+[4,5,6,7]
    jac_minor=s.factor(J.extract(rows,[0,1,8,9,10,11]).det())
    assert jac_minor in [324,-324,162,-162]
    # Entire image is in span of two block commutator columns and U: rank <= 6.
    assert J.rank()==6
    charts.append({'chart':name+'=1','normal_plus_tangent_frame_minor':int(frame_minor),
                   'abelian_tangent_jacobian_minor':int(jac_minor),
                   'grassmannian_tangent_dimension':12,'abelian_tangent_dimension':6,
                   'polynomial_action_tangency_identity':True})

# Dense nilpotent boundary: B(u,v) has (x,y,z)=(uv,-u^2,v^2).
u,v,t=s.symbols('u v t')
Bn=u*v*H-u*u*W[1]+v*v*W[2]
assert Bn*Bn==zero
# One explicit regular-semisimple degeneration to E_23; all nonzero nilpotent
# sl_2 elements are conjugate up to scalar, and the all-charts proof is stronger.
Bt=W[1]+t*H
assert s.factor((Bt*Bt)[1,1])==t*t
assert Bt.subs(t,0)==W[1]

samples=[(0,1,0),(0,0,1),(1,1,-1),(s.I,1,1),(2,-4,1)]
for xyz in samples:
    Bb=sum((c*M for c,M in zip(xyz,W)),s.zeros(3))
    assert Bb*Bb==zero and Bb!=zero
    assert s.Matrix.hstack(vec(A),vec(Bb),*[vec(comm(D,A)) for D in U]).rank()==6

# Negative controls intentionally break hypotheses or use invalid fields.
assert comm(W[1],A)==zero # block conjugation cannot be certified by A-evaluation
assert all(int(q)%3==0 for q in list(right_bracket)) # characteristic 3 fails
assert s.Matrix.hstack(vec(A),vec(zero)).rank()==1 # zero B is not a plane
for lam in [0,1,2,-1]:
    Al=s.diag(2*lam,-lam,-lam)
    assert s.Matrix.hstack(*[vec(comm(D,Al)) for D in U]).rank()==(0 if lam==0 else 4)

print(json.dumps({
 'status':'PASS','python':platform.python_version(),'sympy':s.__version__,
 'frozen_hashes':expected,'frozen_manifest_payloads_verified':7,
 'original_controls_reproduced_exactly':True,
 'all_projective_charts':charts,'symbolic_nilpotent_conic_check':True,
 'explicit_complex_nilpotent_samples':len(samples),
 'right_bracket_D_A_determinant':81,
 'negative_controls':['block fields fail fixed-A test','characteristic 3 degeneracy',
                      'zero B does not define a plane','zero A eliminates rank four'],
 'scope_limit':'Global smoothness, Fano index and Picard group remain cited theorems.'
},indent=2))
