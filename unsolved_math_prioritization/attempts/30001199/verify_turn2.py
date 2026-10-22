import sympy as s,random,json
rng=random.Random(21199);checks=0;cases=0;nontrivial=0;full_kernel=0

def ck(x):
 global checks
 assert x
 checks+=1

def ns(M):
 b=M.nullspace();return s.Matrix.hstack(*b) if b else s.zeros(M.cols,0)
def invariant(A,L,C):
 W=ns(C)
 for _ in range(A.rows+1):
  W2=ns(C.col_join(ns(W.row_join(L).T).T*A))
  if W.cols==W2.cols:return W2
  W=W2
 raise AssertionError('no stabilization')
def inspan(V,W):return V.row_join(W).rank()==V.rank()

for n in range(1,5):
 for trial in range(35):
  A=s.Matrix(n,n,[rng.choice([-1,0,1]) for _ in range(n*n)])
  L=s.Matrix(n,1,[rng.choice([0,0,1]) for _ in range(n)])
  B=s.Matrix(n,1,[rng.choice([-1,0,1]) for _ in range(n)])
  C=s.Matrix(1,n,[rng.choice([0,0,1]) for _ in range(n)])
  N=invariant(A,L,C);k=N.cols;P=ns(N.T).T;q=P.rows
  ck(C*N==s.zeros(1,k));ck(inspan(N.row_join(L),A*N))
  if k:
   nontrivial+=1
   coeff=(N.row_join(-L)).gauss_jordan_solve(A*N)[0]
   coeff=coeff.subs({v:0 for v in coeff.free_symbols})
   KN=coeff[k:,:]
   rows=list(N.T.rref()[1]);E=s.zeros(k,n)
   for j,i in enumerate(rows):E[j,i]=1
   left=(E*N).inv()*E;K=KN*left
  else:K=s.zeros(L.cols,n)
  ck(inspan(N,(A+L*K)*N))
  cols=list(P.rref()[1]);J=s.zeros(n,q)
  if q:
   E=s.zeros(n,q)
   for j,i in enumerate(cols):E[i,j]=1
   J=E*(P*E).inv()
  ck(P*J==s.eye(q));AA=P*(A+L*K)*J;BB=P*B;LL=P*L;CC=C*J
  ck(AA*P==P*(A+L*K));ck(CC*P==C)
  R=s.eye(n).col_join(P);AD=s.diag(A,AA);V1=L.col_join(s.zeros(q,L.cols));V2=s.zeros(n,LL.cols).col_join(LL)
  ck(R[:n,:].rank()==n);ck(R[n:,:].rank()==q)
  ck(inspan(R.row_join(V2),AD*R));ck(inspan(R.row_join(V1),AD*R))
  ck(inspan(R.row_join(V2),V1));ck(inspan(R.row_join(V1),V2))
  ck(inspan(R,B.col_join(BB)));ck((C.row_join(-CC))*R==s.zeros(1,n))
  ck(invariant(AA,LL,CC).cols==0)
  if k==ns(C).cols:
   full_kernel+=1;ck(CC.rank()==q)
  cases+=1
# Explicit 2-state controlled-kernel example and the blocked double integrator.
A=s.Matrix([[0,1],[-2,3]]);L=s.Matrix([1,0]);C=s.Matrix([[1,0]]);K=s.Matrix([[0,-1]]);N=s.Matrix([0,1])
ck((A+L*K)*N==3*N);ck(invariant(A,L,C).cols==1)
ck(invariant(s.Matrix([[0,1],[0,0]]),s.zeros(2,1),C).cols==0)
print(json.dumps({'status':'PASS','exact_assertions':checks,'rational_quotient_cases':cases,'nontrivial_output_nulling_subspaces':nontrivial,'whole_kernel_cases':full_kernel,'scope':'Finite exact controls verify disturbance-feedback quotient identities, both simulation directions and the zero-nulling quotient. Universal scope follows from TURN_2.md, not finite testing.'},indent=2))
