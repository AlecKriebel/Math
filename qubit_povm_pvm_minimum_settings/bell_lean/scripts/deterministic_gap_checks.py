#!/usr/bin/env python3
"""Independent polynomial checks; NOT a Lean build or physical-geometry proof."""
from pathlib import Path
import hashlib
import json
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
u=s.Matrix([1,1,0,0])
rays=[s.eye(4)[:,i] for i in range(4)]+[s.Matrix([1,1,-1,-1])]
resets=[s.Matrix([[1,0,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]]),
        s.Matrix([[0,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]),
        s.Matrix([[1,0,1,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]]),
        s.Matrix([[1,0,0,1],[0,1,0,1],[0,0,0,0],[0,0,0,0]]),
        s.diag(1,1,0,0)]
# All bilinear forms with the five null rays, including nonsymmetric forms.
q01,q02,q03,q10,q12,q13,q20,q21,q23,q30,q31 = s.symbols(
    'q01 q02 q03 q10 q12 q13 q20 q21 q23 q30 q31', real=True)
q32=q02+q03+q12+q13+q20+q21+q30+q31-q01-q10-q23
B=s.Matrix([[0,q01,q02,q03],[q10,0,q12,q13],[q20,q21,0,q23],[q30,q31,q32,0]])
lam=s.symbols('lambda0:5',real=True)
alpha=s.symbols('alpha',real=True)
ell=s.Matrix(1,4,s.symbols('ell0:4',real=True))
checks=[]

def eq(name,left,right):
    delta=left-right
    terms=list(delta) if isinstance(delta,s.MatrixBase) else [delta]
    if not all(s.expand(x)==0 for x in terms):raise AssertionError(name)
    checks.append(name)

def compatibility(W):return sum(lam[j]*(rays[j].T*B*W*rays[j])[0] for j in range(5))
def score(W):return alpha*(ell*W*u)[0]-2*compatibility(W)
for j,r in enumerate(rays):eq(f'null-{j}',(r.T*B*r)[0],0)
for j,T in enumerate(resets):
    eq(f'unit-{j}',T*u,u)
    eq(f'idempotent-{j}',T*T,T)
    for k,r in enumerate(rays):
        expected=u if j==k else (s.zeros(4,1) if (j<2)==(k<2) else r)
        eq(f'ray-{j}-{k}',T*r,expected)
    eq(f'compatibility-{j}',compatibility(T),lam[j]*(rays[j].T*B*u)[0])
    eq(f'gap-{j}',score(s.eye(4))-score(T),2*lam[j]*(rays[j].T*B*u)[0])
# The independent generic table identity includes the unused third binary label.
P=s.Matrix(4,4,s.symbols('P0:16',real=True))
effects=[[rays[0],rays[1],s.zeros(4,1)],[rays[2],rays[3],rays[4]]]
def p(W,x,y,aa,bb):return (effects[x][aa].T*P*W*effects[y][bb])[0]
for j,T in enumerate(resets):
    reset_input,reset_label=(0,j) if j<2 else (1,j-2)
    for x in range(2):
        for y in range(2):
            for aa in range(3):
                for bb in range(3):
                    expected=(sum(p(s.eye(4),x,1-reset_input,aa,z) for z in range(3))
                              if bb==reset_label else 0) if y==reset_input else p(s.eye(4),x,y,aa,bb)
                    eq(f'table-{j}-{x}-{y}-{aa}-{bb}',p(T,x,y,aa,bb),expected)
wrong=resets[0].T
if s.expand(score(s.eye(4))-score(wrong)-2*lam[0]*(rays[0].T*B*u)[0])==0:
    raise AssertionError('Transpose mutation was not rejected')
report={'status':'passed','universal_polynomial_identities':len(checks),
    'base_identities':50,'table_identities':180,
    'bilinear_form_domain':'arbitrary real bilinear forms satisfying all five null-ray constraints, without a symmetry assumption','rejected_transpose_mutations':1,
    'checks':checks,'lean_kernel_checked':False,
    'scope':'Finite polynomial identities. Physical stationarity, tangent integration, and global equality are not checked.',
    'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'lean_source_sha256':hashlib.sha256((ROOT/'Bell/DeterministicGap.lean').read_bytes()).hexdigest()}
assert report['universal_polynomial_identities']==report['base_identities']+report['table_identities']
(ROOT/'reports/session_20260910/deterministic_gap_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
