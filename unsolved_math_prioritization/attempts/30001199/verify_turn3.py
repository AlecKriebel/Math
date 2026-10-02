"""Exact matrix controls for the full nilpotent-coupling argument."""
import sympy as s,random,json
rng=random.Random(31199);checks=0;cases=0;nonzeroK=0;maxindex=0

def ck(x):
 global checks
 assert x
 checks+=1

def ns(M):
 b=M.nullspace();return s.Matrix.hstack(*b) if b else s.zeros(M.cols,0)
def contains(V,W):return V.row_join(W).rank()==V.rank()
def invariant(A,L,C):
 W=ns(C)
 for _ in range(A.rows+1):
  X=ns(C.col_join(ns(W.row_join(L).T).T*A))
  if X.cols==W.cols:return X
  W=X
 raise AssertionError

def comp(x,y):
 A,B,L,C=x;D,E,M,F=y
 return A.row_join(-B*F).col_join((E*C).row_join(D)),s.diag(L,M),s.diag(C,F)
def graphcheck(src,tgt,T):
 A,L,C=src;D,M,F=tgt;n=A.rows;m=D.rows;R=s.eye(n).col_join(T);V=s.zeros(n,M.cols).col_join(M);U=L.col_join(s.zeros(m,L.cols));RV=R.row_join(V)
 ck(T.cols==n and T.rows==m);ck(R[:n,:].rank()==n);ck(C==F*T);ck(contains(RV,s.diag(A,D)*R));ck(contains(RV,U))

def fixture(p1,p2,q1,q2,F,E,H,J):
 global cases,nonzeroK,maxindex
 A1,B1,L1,C1=q1;A2,B2,L2,C2=q2;n1=A1.rows;n2=A2.rows;k1=p1[0].rows;k2=p2[0].rows
 ck(invariant(A1,L1,C1).cols==0);ck(invariant(A2,L2,C2).cols==0)
 Tprem1=F.row_join(E).col_join(s.zeros(n2,k1).row_join(s.eye(n2)))
 Tprem2=s.eye(n1).row_join(s.zeros(n1,k2)).col_join(H.row_join(J))
 target=comp(q1,q2);graphcheck(comp(p1,q2),target,Tprem1);graphcheck(comp(q1,p2),target,Tprem2)
 ck(C1*F==p1[3]);ck(C1*E==s.zeros(C1.rows,n2));ck(C2*H==s.zeros(C2.rows,n1));ck(C2*J==p2[3])
 ck(contains(L1,E*L2));ck(contains(L2,H*L1))
 W1=E*A2-A1*E+(B1-F*p1[1])*C2
 W2=H*A1-A2*H+(J*p2[1]-B2)*C1
 ck(contains(L1,W1));ck(contains(L2,W2))
 K=E*H;D=E*(B2-J*p2[1]);ck(C1*K==s.zeros(C1.rows,n1));ck(contains(L1,K*L1));ck(contains(L1,K*A1-A1*K-D*C1))
 ck(K**max(1,n1)==s.zeros(n1));index=next(j for j in range(1,max(1,n1)+1) if K**j==s.zeros(n1));maxindex=max(maxindex,index)
 if K!=s.zeros(n1):nonzeroK+=1
 S=sum((K**j for j in range(max(1,n1))),s.zeros(n1));ck(S*(s.eye(n1)-K)==s.eye(n1));ck((s.eye(n1)-K)*S==s.eye(n1));ck(contains(L1,S*L1))
 T1=S*(F.row_join(E*J));T2=H*T1+s.zeros(n2,k1).row_join(J);T=T1.col_join(T2)
 ck(T1==F.row_join(s.zeros(n1,k2))+E*T2);ck(T2==H*T1+s.zeros(n2,k1).row_join(J))
 src=comp(p1,p2);graphcheck(src,target,T)
 As,Ls,Cs=src;f=As.row_join(Ls);nd=Ls.cols;a1=(A1*T1-B1*C2*T2).row_join(s.zeros(n1,nd));a2=(A2*T2+B2*C1*T1).row_join(s.zeros(n2,nd))
 r1=F*f[:k1,:]+E*a2-a1;r2=H*a1+J*f[k1:,:]-a2
 ck(contains(L1,r1));ck(contains(L2,r2))
 v1=S*(r1+E*r2);v2=r2+H*v1
 ck(contains(L1,v1));ck(contains(L2,v2));ck(v1-E*v2==r1);ck(v2-H*v1==r2)
 ck(T*f==(a1+v1).col_join(a2+v2));cases+=1

# Arbitrarily long chain family: K=-lower_shift**2; nilpotence need not be index1.
for r in range(1,11):
 A=s.zeros(r);E0=s.zeros(r)
 for i in range(r-1):A[i,i+1]=1;E0[i+1,i]=1
 C=s.zeros(1,r);C[0,0]=1;L=s.zeros(r,1);L[r-1,0]=1
 q=(A,s.zeros(r,1),L,C);p=(s.zeros(1),s.ones(1),s.zeros(1),s.ones(1));F=s.zeros(r,1);F[0,0]=1
 fixture(p,p,q,q,F,-E0,E0,F)
 ck((-E0**2)**((r+1)//2)==s.zeros(r))
 if r>=3:ck((-E0**2)**(((r+1)//2)-1)!=s.zeros(r))

# Random two-state systems: all source disturbances are nontrivial, and both
# specification observation maps have kernels but zero maximal nulling spaces.
for _ in range(100):
 def qsys():
  A=s.Matrix([[rng.randrange(-2,3),rng.choice([-2,-1,1,2])],[rng.randrange(-2,3),rng.randrange(-2,3)]]);B=s.Matrix([rng.randrange(-2,3),rng.randrange(-2,3)]);return A,B,s.Matrix([0,1]),s.Matrix([[1,0]])
 def psys():
  return s.Matrix(2,2,[rng.randrange(-2,3) for _ in range(4)]),s.Matrix([rng.randrange(-2,3),rng.randrange(-2,3)]),s.Matrix([0,rng.choice([-2,-1,1,2])]),s.Matrix([[1,0]])
 q1,q2,p1,p2=qsys(),qsys(),psys(),psys()
 a,b=q1[0],q2[0];f,g=p1[0],p2[0]
 F=s.Matrix([[1,0],[(f[0,0]-a[0,0])/a[0,1],f[0,1]/a[0,1]]]);E=s.Matrix([[0,0],[(q1[1][0]-p1[1][0])/a[0,1],0]])
 J=s.Matrix([[1,0],[(g[0,0]-b[0,0])/b[0,1],g[0,1]/b[0,1]]]);H=s.Matrix([[0,0],[(p2[1][0]-q2[1][0])/b[0,1],0]])
 fixture(p1,p2,q1,q2,F,E,H,J)

# Zero-dimensional quotient specifications, including one-sided and two-sided
# zero state spaces. These are genuine boundary cases of output-nulling quotients.
q0=(s.zeros(0),s.zeros(0,1),s.zeros(0,1),s.zeros(1,0))
p0=(s.ones(1),s.ones(1),s.ones(1),s.zeros(1))
qscalar=(s.zeros(1),s.ones(1),s.ones(1),s.ones(1))
pscalar=(s.ones(1),s.ones(1),s.ones(1),s.ones(1))
fixture(p0,p0,q0,q0,s.zeros(0,1),s.zeros(0),s.zeros(0),s.zeros(0,1))
fixture(p0,pscalar,q0,qscalar,s.zeros(0,1),s.zeros(0,1),s.zeros(1,0),s.ones(1))

# Negative control: without zero-nulling reduction, the other algebraic
# conditions alone do not imply nilpotence.
K=s.diag(0,1);A=s.zeros(2);C=s.Matrix([[1,0]]);L=s.zeros(2,1)
ck(C*K==s.zeros(1,2));ck(K*A-A*K==s.zeros(2));ck(invariant(A,L,C).cols==1);ck(K**2==K and K!=s.zeros(2))
print(json.dumps({'status':'PASS','exact_assertions':checks,'full_matrix_fixtures':cases,'fixtures_with_nonzero_nilpotent_cycle':nonzeroK,'largest_nilpotence_index_checked':maxindex,'random_fixtures_with_nonzero_implementation_disturbances':100,'negative_control_without_zero_nulling':True,'zero_dimensional_boundary_fixtures':2,'scope':f'Exact finite matrix identities verify the entire construction on {cases} fixtures, including both premises, nilpotence, full initial graphs and simultaneous disturbances. The universal proof is in TURN_3.md.'},indent=2))
