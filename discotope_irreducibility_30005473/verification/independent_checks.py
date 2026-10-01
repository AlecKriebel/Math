#!/usr/bin/env python3
"""Independent exact sanity checks for PR 9; no source snapshot writes.

Dependencies: Python 3, sympy==1.14.0, mpmath==1.3.0.
These checks supplement, and do not prove, the candidate's general analytic theorem.
"""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone
from itertools import combinations
import sympy as s

ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT / 'source_snapshot'
hashes_before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in SNAPSHOT.iterdir() if p.is_file()}
out = {
    'utc': datetime.now(timezone.utc).isoformat(),
    'python': platform.python_version(),
    'sympy': s.__version__,
    'mpmath': __import__('mpmath').__version__,
    'head': 'a29887ed0e341851d02fa992c26500d4089267be',
    'source_snapshot_sha256': hashes_before,
}

# Independent derivation: regard the summed x-coordinates as two auxiliaries.
# Circle identities give T=2ab, with no use of u,r,t or square-root elimination.
a,b,X,Y,Z = s.symbols('a b X Y Z')
P = (X**2+Y**2+Z**2-5)**2-4*(4-Y**2)*(1-Z**2)
C1 = a*a+Y*Y-4
C2 = b*b+Z*Z-1
T = X*X+Y*Y+Z*Z-5
assert s.expand(T.subs(X,a+b) - 2*a*b - C1-C2) == 0
assert s.expand(P.subs(X,a+b)-((C1+C2)**2+4*a*b*(C1+C2)
                   +4*a*a*C2+4*b*b*C1-4*C1*C2)) == 0
aux = s.groebner([C1,C2,X-a-b], a,b,X,Y,Z)
assert aux.reduce(P)[1] == 0
eliminants = [g.as_expr() for g in aux.polys if not (g.as_expr().has(a) or g.as_expr().has(b))]
assert len(eliminants) == 1 and s.expand(eliminants[0]-P) == 0
out['auxiliary_circle_derivation'] = {
    'identity': 'T=2ab+C1+C2; P is an explicit polynomial combination of C1,C2',
    'elimination_basis': [str(v) for v in eliminants],
    'e3_separating_value': str(P.subs({X:0,Y:0,Z:1})),
}
assert P.subs({X:0,Y:0,Z:1}) == 16

# Audit the original rational substitution independently, including denominator.
u,v,w,r,t = s.symbols('u v w r t')
rat = s.cancel(P.subs({X:2*u/r+u/t,Y:2*v/r,Z:w/t}))
numerator,denominator = s.fraction(rat)
relations = [r*r-u*u-v*v,t*t-u*u-w*w]
gb = s.groebner(relations,r,t,u,v,w)
quotients,remainder = gb.reduce(numerator)
assert remainder == 0
assert s.expand(numerator-sum(q*g.as_expr() for q,g in zip(quotients,gb.polys))) == 0
assert s.factor(denominator) == r**4*t**4
out['rational_denominator_audit'] = {
    'denominator': str(s.factor(denominator)),
    'numerator_remainder': str(remainder),
    'quotient_certificate': [str(q) for q in quotients],
    'basis': [str(g.as_expr()) for g in gb.polys],
    'scope': 'identity for r*t != 0; candidate real regular normals give r,t>0',
}

# Exact rational-direction samples include u1=0 with both denominators nonzero.
samples = [(1,2,3),(0,1,1),(3,4,4),(-3,4,-4),(3,-4,-4)]
sample_values = []
for uvw in samples:
    uu,vv,ww = map(s.Integer,uvw)
    rr=s.sqrt(uu**2+vv**2); tt=s.sqrt(uu**2+ww**2)
    point = [2*uu/rr+uu/tt,2*vv/rr,ww/tt]
    assert s.simplify(P.subs(dict(zip([X,Y,Z],point)))) == 0
    sample_values.append({'normal':list(uvw),'exposed_point':[str(z) for z in point]})
out['nongeneric_regular_normal_edge_samples'] = sample_values

# The GP perturbation mechanism with arbitrary rational unit targets on each
# killed disc, rather than the original script's single coordinate target.
eye=s.eye(5); e=[eye[:,i] for i in range(5)]
A=[s.Matrix.hstack(e[0],e[1]),s.Matrix.hstack(e[2],e[3]),
   s.Matrix.hstack(e[0]+e[2]+e[4],e[1]+e[3]+2*e[4])]
ranks={}
for k in range(1,4):
    for J in combinations(range(3),k):
        rank=s.Matrix.hstack(*(A[j] for j in J)).rank()
        assert rank==min(5,2*k)
        ranks[','.join(str(j+1) for j in J)]=rank
targets=[s.Matrix([s.Rational(3,5),s.Rational(4,5)]),
         s.Matrix([s.Rational(5,13),s.Rational(12,13)])]
normal=e[4]
perturb=s.Matrix.vstack(*targets,s.Matrix([0]))
eps=s.symbols('eps',positive=True)
for j in [0,1]:
    assert (targets[j].T*targets[j])[0]==1
    assert A[j].T*normal == s.zeros(2,1)
    assert A[j].T*perturb == targets[j]
    q=A[j].T*(normal+eps*perturb)
    p=A[j]*q/s.sqrt((q.T*q)[0])
    assert s.simplify(p-A[j]*targets[j])==s.zeros(5,1)
    qnegative=A[j].T*(normal-eps*perturb)
    pnegative=A[j]*qnegative/s.sqrt((qnegative.T*qnegative)[0])
    assert s.simplify(pnegative+A[j]*targets[j])==s.zeros(5,1)
q3=A[2].T*(normal+eps*perturb)
p3=A[2]*q3/s.sqrt((q3.T*q3)[0])
limit3=p3.applyfunc(lambda z:s.limit(z,eps,0,dir='+'))
expected=A[2]*s.Matrix([1,2])/s.sqrt(5)
assert s.simplify(limit3-expected)==s.zeros(5,1)
out['gp_arbitrary_unit_target_perturbation']={
    'subset_ranks':ranks,'targets':[[str(z) for z in q] for q in targets],
    'normal':[str(z) for z in normal],'perturbation':[str(z) for z in perturb],
    'third_summand_limit':[str(z) for z in limit3],
    'negative_epsilon': 'killed-summand limit flips sign; positive epsilon is essential',
}

# Recheck the dual-map prescription with non-orthonormal ellipse parametrizations.
# Setting w equal to the target vectors would be incorrect for these A_j.
ellipses=[s.Matrix.hstack(e[0],e[0]+2*e[1]),
          s.Matrix.hstack(e[2]+e[3],3*e[2]-e[3]),A[2]]
for k in range(1,4):
    for J in combinations(range(3),k):
        assert s.Matrix.hstack(*(ellipses[j] for j in J)).rank()==min(5,2*k)
concat=s.Matrix.hstack(*ellipses[:2])
chosen=s.Matrix.vstack(*targets)
general_solution=concat.T.gauss_jordan_solve(chosen)
elliptic_w=general_solution[0].subs({z:0 for z in general_solution[1]})
assert concat.T*elliptic_w==chosen
for j in [0,1]:
    q=ellipses[j].T*(normal+eps*elliptic_w)
    p=ellipses[j]*q/s.sqrt((q.T*q)[0])
    assert s.simplify(p-ellipses[j]*targets[j])==s.zeros(5,1)
out['gp_nonorthonormal_ellipse_perturbation']={
    'transpose_rank':concat.T.rank(),
    'perturbation':[str(z) for z in elliptic_w],
    'killed_support_points':[[str(z) for z in ellipses[j]*targets[j]] for j in [0,1]],
    'scope':'surjective transpose is used correctly without orthonormality',
}

# Distinct rank-one failure: the two support branches have distinct circle ideals.
aa=s.symbols('aa',positive=True)
Cp=(X-aa)**2+Y**2-1
Cm=(X+aa)**2+Y**2-1
assert s.expand(Cm-Cp)==4*aa*X
assert s.simplify(Cp.subs({X:aa+1,Y:0}))==0
assert s.simplify(Cm.subs({X:aa+1,Y:0}))==4*aa*(aa+1)
assert s.simplify(Cm.subs({X:-aa-1,Y:0}))==0
assert s.simplify(Cp.subs({X:-aa-1,Y:0}))==4*aa*(aa+1)
out['rank_one_stadium']={
    'branch_circle_polynomials':[str(Cp),str(Cm)],
    'difference':str(s.expand(Cm-Cp)),
    'scope':'each real open semicircle is Zariski dense in its smooth complex conic; a>0 gives distinct components',
}

# Source script inspected before this invocation: imports/expressions/assertions/
# stdout only, no network or file writes. Reproduce with -B from review directory.
completed=subprocess.run([sys.executable,'-B',str(SNAPSHOT/'checks.py')],
                         cwd=ROOT,capture_output=True,text=True,check=False)
(ROOT/'checks_rerun.stdout.json').write_text(completed.stdout)
(ROOT/'checks_rerun.stderr.txt').write_text(completed.stderr)
assert completed.returncode==0, completed.stderr
out['source_script_rerun']={'returncode':completed.returncode,
                          'stdout_artifact':'checks_rerun.stdout.json',
                          'stderr_artifact':'checks_rerun.stderr.txt'}
hashes_after={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
              for p in SNAPSHOT.iterdir() if p.is_file()}
assert hashes_before==hashes_after
out['snapshot_unchanged']=True
out['status']='All independent exact checks and the inspected source script passed'
print(json.dumps(out,indent=2))
