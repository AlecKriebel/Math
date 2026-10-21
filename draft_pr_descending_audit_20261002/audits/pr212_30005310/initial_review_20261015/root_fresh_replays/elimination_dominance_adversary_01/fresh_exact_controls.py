#!/usr/bin/env python3
"""Independent exact algebra controls, authored before reading submitted checkers.
No imports from or writes to submitted material. SymPy is corroboration of the
written symbolic proof, not a substitute for its universal ideal implications.
"""
from pathlib import Path
from itertools import combinations
import datetime,hashlib,json
import sympy as s
OUT=Path(__file__).parent
checks=[]
def test(name,condition,detail=None):
    if not bool(condition): raise AssertionError(name)
    checks.append({'name':name,'pass':True,**({'detail':detail} if detail is not None else {})})
def outputs(X):
    return s.Matrix([sum(X[i,k]**2 for k in range(4)) for i in range(8)]+[sum(X[i,k]*X[4+j,k] for k in range(4)) for i in range(4) for j in range(4)])
def differential(X,Z):
    return s.Matrix([2*sum(X[i,k]*Z[i,k] for k in range(4)) for i in range(8)]+[sum(Z[i,k]*X[4+j,k]+X[i,k]*Z[4+j,k] for k in range(4)) for i in range(4) for j in range(4)])
def jacobian(X):
    columns=[]
    for i in range(8):
        for k in range(4):
            Z=s.zeros(8,4);Z[i,k]=1
            columns.append(differential(X,Z))
    return s.Matrix.hstack(*columns)
def lift(y):
    a=y[:4]; c=y[4:8]; H=s.Matrix(4,4,list(y[8:24]));D=s.zeros(4,4)
    for i in range(4):D[i,i]=a[i]/2
    for j in range(4):
        k=(j+1)%4
        D[j,k]=(V*H)[j,j]-(a[j]+a[k]+c[j])/2
    E=H.T-V*D.T
    return D.col_join(E)
V=s.zeros(4,4)
for j in range(4):V[j,j]=1;V[j,(j+1)%4]=1
X0=s.eye(4).col_join(V)
y=s.Matrix(s.symbols('y0:24'))
Z=lift(y)
res=differential(X0,Z)-y
for i,v in enumerate(res):test(f'all_output_right_inverse_{i}',s.expand(v)==0)
R=s.Matrix.hstack(*[s.Matrix(lift(s.eye(24)[:,i])).reshape(32,1) for i in range(24)])
J=jacobian(X0)
test('full_JR_identity',J*R==s.eye(24))
test('singleton_jacobian_rank',J.rank()==24)
piv=J.rref()[1];det=J[:,list(piv)].det()
test('singleton_nonzero_square_minor',det!=0,{'columns':list(piv),'determinant':str(det)})
P=s.zeros(23,24);P[0,0]=P[0,1]=1
for i in range(1,23):P[i,i+1]=1
L=s.zeros(24,23);L[0,0]=1
for i in range(1,23):L[i+1,i]=1
test('tie_projection_has_explicit_section',P*L==s.eye(23))
test('tied_JRL_identity',P*J*R*L==s.eye(23))
Jt=P*J;pivt=Jt.rref()[1];dett=Jt[:,list(pivt)].det()
test('tied_jacobian_rank',Jt.rank()==23)
test('tied_nonzero_square_minor',dett!=0,{'columns':list(pivt),'determinant':str(dett)})
Psi=outputs(X0+Z)-outputs(X0)-y
for i,q in enumerate(Psi):
    poly=s.Poly(s.expand(q),*y)
    test(f'restricted_polynomial_only_quadratic_{i}',all(sum(m)==2 for m,c in poly.terms() if c!=0))
# Explicit statistic-relation ideal membership telescope, generic B and T.
B=s.Matrix(4,4,s.symbols('b0:16'));T=s.Matrix(4,4,s.symbols('t0:16'))
telescope=0
for j in range(4):
    columns=[T[:,k] if k<j else T[:,k]-B[:,k] if k==j else B[:,k] for k in range(4)]
    telescope+=s.Matrix.hstack(*columns).det(method='domain-ge')
test('determinant_statistic_relation_telescope',s.expand(T.det()-B.det()-telescope)==0)
test('cross_determinant_nonzero_polynomial',T.det().subs({T[i,j]:int(i==j) for i in range(4) for j in range(4)})==1)
G=X0*X0.T
all5=0
for rows in combinations(range(8),5):
    for cols in combinations(range(8),5):
        test(f'gram5minor_{rows}_{cols}',G.extract(rows,cols).det()==0)
        all5+=1
test('all_full5minors_checked',all5==3136)
test('singular_V_rank3',V.rank()==3)
test('rank_X0_4_despite_singular_V',X0.rank()==4)
Xi=s.eye(4).col_join(s.eye(4))
test('rank4_Gram_crossdet_can_be_one',(Xi*Xi.T)[:4,4:8].det()==1)
test('singular_V_not_needed',G[:4,4:8].det()==0)
test('zero_point_differential_rank0',jacobian(s.zeros(8,4)).rank()==0)
test('identity_blocks_differential_rank20',jacobian(Xi).rank()==20)
# Principal-only replacements give a different set: explicit real controls.
for k in (4,5):
    A=s.eye(8)*(1+s.Rational(1,k-1))-s.ones(8)*s.Rational(1,k-1)
    test(f'principal_only_{k}_matrix_has_rank8',A.rank()==8)
    for rows in combinations(range(8),k):test(f'principal_only_{k}_{rows}',A.extract(rows,rows).det()==0)
    rows=list(range(k));cols=list(range(k-1))+[k]
    test(f'principal_only_{k}_nonprincipal_minor_nonzero',A.extract(rows,cols).det()!=0,{'rows':rows,'columns':cols,'determinant':str(A.extract(rows,cols).det())})
# Actual rank-2 preimage for the asserted positive-definite intersection.
Xstar=s.Matrix([[1,0]]*4+[[0,1]]*4)
Sstar=Xstar*Xstar.T
statS=lambda A:s.Matrix([A[i,i] for i in range(8)]+[A[i,4+j] for i in range(4) for j in range(4)])
test('rank2_preimage',Sstar.rank()==2)
test('identity_statistics_have_PSD_rank2_preimage',statS(Sstar)==statS(s.eye(8)))
test('tied_identity_statistics_same',P*statS(Sstar)==P*statS(s.eye(8)))
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sympy_version':s.__version__,'checks_passed':len(checks),'failed':0,'singleton_jacobian_shape':list(J.shape),'singleton_jacobian_rank':24,'singleton_kernel_dimension':8,'tied_jacobian_shape':list(Jt.shape),'tied_jacobian_rank':23,'all_5_by_5_full_minors_evaluated_at_Gram_point':all5,'independent_derivation_sha256':hashlib.sha256((OUT/'INDEPENDENT_DERIVATION.md').read_bytes()).hexdigest(),'checks':checks}
(OUT/'FRESH_EXACT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
