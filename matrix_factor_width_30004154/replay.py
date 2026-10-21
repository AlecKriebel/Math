def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

"""Independent rational audit; does not import the author's verification code."""
import json
from itertools import combinations
import sympy as s
R=s.Rational
B=s.Matrix([[1,R(1,2)],[1,-R(1,2)],[1,R(3,4)],[1,-R(3,4)]])
Q=B*B.T
M=s.Matrix([[3247,-881,-2481,-561],[-881,3247,-561,-2481],[-2481,-561,2447,-81],[-561,-2481,-81,2447]])
Y=M/2704
mins=[Y.extract(S,S).det() for j in range(1,4) for S in combinations(range(4),j)]
expected=[R(3247,2704)]*2+[R(2447,2704)]*2+[R(903,676),R(331,1352),R(1411,1352),R(1411,1352),R(331,1352),R(553,676),R(15,676),R(15,676),R(115,676),R(115,676)]
require(mins==expected and min(mins)>0, 'Certificate validation failed at original line 12')
require(s.trace(Y*Q)==-R(1,4), 'Certificate validation failed at original line 13')
Bp=(B.T*B).inv()*B.T
require(Y==2*(s.eye(4)-B*Bp)+Bp.T*s.diag(-1,R(3,4))*Bp, 'Certificate validation failed at original line 15')
# Row-normalized Gram nonzero eigenvalues, using rational B^T D^{-1} B.
G=B.T*s.diag(*[1/Q[i,i] for i in range(4)])*B
require(G==s.diag(R(72,25),R(28,25)), 'Certificate validation failed at original line 18')
Qpd=Q+s.eye(4)/1000
require(s.trace(Y*Qpd)==-R(12781,52000), 'Certificate validation failed at original line 20')
require(all(Qpd[:j,:j].det()>0 for j in range(1,5)), 'Certificate validation failed at original line 21')
require(all(Q[i,j]>0 for i in range(4) for j in range(4)), 'Certificate validation failed at original line 22')
# Every off-diagonal of positive entrywise normalization strictly decreases:
require(all(Qpd[i,i]*Qpd[j,j]>Q[i,i]*Q[j,j] for i in range(4) for j in range(i)), 'Certificate validation failed at original line 24')

def rays(X,k):
    X=s.Matrix([list(X.row(i)) for i in range(X.rows) if any(X.row(i))])
    N=X.rows
    if k>=N: return None
    result={}
    for i in range(N):
        a,b=X.row(i); v=s.Matrix([-b,a]); nz=next(x for x in v if x)
        v=v/nz
        if sum(x!=0 for x in X*v)<=k: result[tuple(v)]=v
    return list(result.values())

def feasible_small(X,k):
    rs=rays(X,k)
    if rs is None: return True,2
    target=s.Matrix([1,0,1])
    for m in [1,2,3]:
        for ss in combinations(rs,m):
            A=s.Matrix.hstack(*[s.Matrix([v[0]**2,v[0]*v[1],v[1]**2]) for v in ss])
            if A.rank()!=m: continue
            sol=s.linsolve((A,target))
            if sol and any(all(c>=0 for c in x) for x in sol): return True,m
    return False,None
require(feasible_small(B,3)==(False,None), 'Certificate validation failed at original line 48')
X=s.Matrix([[0,1],[2,-1],[2,1],[1,1]])
vs=[s.Matrix(v) for v in [(1,0),(1,2),(1,-2)]]
cs=[R(3,4),R(1,8),R(1,8)]
require(sum((c*v*v.T for c,v in zip(cs,vs)),s.zeros(2))==s.eye(2), 'Certificate validation failed at original line 52')
require(sum((c*(X*v)*(X*v).T for c,v in zip(cs,vs)),s.zeros(4))==X*X.T, 'Certificate validation failed at original line 53')
require(feasible_small(X,3)==(True,3), 'Certificate validation failed at original line 54')
require(feasible_small(X,2)==(False,None), 'Certificate validation failed at original line 55')
# Zero rows must not count, and multiplicity must count.
Xp=s.Matrix([[1,0]]*3+[[0,1]]*2+[[1,1]]+[[0,0]]*2)
require(feasible_small(Xp,4)==(True,2), 'Certificate validation failed at original line 58')
require(feasible_small(Xp,3)==(False,None), 'Certificate validation failed at original line 59')
# General symbolic Schur identity has coefficient 1/2; exact samples.
for k in range(3,12):
    v=s.Matrix([1]+[1]*(k-1)+[0]*(k-1)); w=s.Matrix([1]+[0]*(k-1)+[1]*(k-1))
    A=v*v.T+w*w.T
    S=A[1:,1:]-A[1:,:1]*A[:1,1:]/A[0,0]
    z=s.Matrix([1]*(k-1)+[-1]*(k-1))
    require(S==z*z.T/2 and S.rank()==1 and len(z)==2*k-2>k, 'Certificate validation failed at original line 66')
# Explicit symmetric construction, positive and negative boundary values.
for n in range(3,9):
    for k in range(2,n+1):
        for c,d in [(R(1),R(n-1,k-1)),(-R(1),R(n-1))]:
            block=s.ones(k)*c/s.binomial(n-2,k-2)
            for i in range(k): block[i,i]=d/s.binomial(n-1,k-1)
            require(all(e>=0 for e in block.eigenvals()), 'Certificate validation failed at original line 73')
            total=s.zeros(n)
            for S in combinations(range(n),k):
                for i in range(k):
                    for j in range(k): total[S[i],S[j]]+=block[i,j]
            require(total==s.eye(n)*(d-c)+s.ones(n)*c, 'Certificate validation failed at original line 78')
print(json.dumps({'result':'PASS','dual_principal_minors':[str(x) for x in mins], 'pairing':str(s.trace(Y*Q)), 'PD_pairing':str(s.trace(Y*Qpd)), 'normalized_nonzero_eigenvalues':[str(G[i,i]) for i in range(2)], 'positive_example_min_terms':3, 'zero_parallel_edge_case':'PASS','Schur_exact_samples':'k=3..11','symmetric_boundary_samples':'n=3..8, k=2..n'},indent=2))
# All-k repeated-row family: independent exact samples; universal proof in AUDIT.md.
for k in range(3,31):
    n=k+1; p=(n+1)//2; q=n//2
    require(q>=2 and p+R(7,25)*q==n-R(18,25)*q<k, 'Certificate validation failed at original line 83')
    A=s.Matrix([[1,R(3,4)]]*p+[[1,-R(3,4)]]*q)
    require(A.rank()==2, 'Certificate validation failed at original line 85')
    require(feasible_small(A,k)==(False,None), 'Certificate validation failed at original line 86')
print('PASS: all-k repeated-row family exact samples k=3..30.')
