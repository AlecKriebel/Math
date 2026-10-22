import sympy as s,random,json
rng=random.Random(30001199);count=0;eligible=0

def ck(x):
 global count
 assert x
 count+=1

def ns(M):
 v=M.nullspace();return s.Matrix.hstack(*v) if v else s.zeros(M.cols,0)
def comp(x,y):
 A,B,L,C=x;D,E,M,F=y
 return A.row_join(-B*F).col_join((E*C).row_join(D)),s.diag(L,M),s.diag(C,F)
def sim(src,tgt):
 A,L,C=src;D,M,F=tgt;n=A.rows;m=D.rows;AA=s.diag(A,D);E=C.row_join(-F);W=ns(E);V=s.zeros(n,M.cols).col_join(M)
 for _ in range(n+m+1):
  ann=ns(W.row_join(V).T).T;W2=ns(E.col_join(ann*AA))
  if W2.cols==W.cols:W=W2;break
  W=W2
 WV=W.row_join(V);U=L.col_join(s.zeros(m,L.cols))
 return W[:n,:].rank()==n and WV.row_join(U).rank()==WV.rank(),W

def rand2():
 A=s.Matrix(2,2,[rng.choice([-1,0,1]) for _ in range(4)]);B=s.Matrix([rng.choice([-1,0,1]),rng.choice([-1,0,1])]);L=rng.choice([s.zeros(2,1),s.Matrix([1,0]),s.Matrix([0,1])]);return A,B,L,s.Matrix([[1,0]])
for trial in range(10):
 q1=(s.Matrix([[rng.choice([-1,0,1])]]),s.Matrix([[rng.choice([-1,0,1])]]),s.ones(1,1),s.ones(1,1));q2=rand2();target=comp(q1,q2)
 p2s=[q2]+[rand2() for _ in range(4)]
 for p2 in p2s:
  ok,R2=sim(comp(q1,p2),target)
  if not ok:continue
  for _ in range(3):
   p1=rand2();ok1,R1=sim(comp(p1,q2),target);ck(ok1)
   # Main tuple order: p1(2),p2(2),q1(1),q2(2).
   T=s.zeros(6,7);T[0,4]=1;T[1,2]=1;T[2,3]=1;T[3,4]=1;T[4,5]=1;T[5,6]=1
   graph=s.Matrix([[-1,0,0,0,1,0,0]])
   R=ns(graph.col_join(ns(R2.T).T*T))
   src=comp(p1,p2);A,L,C=src;D,M,F=target;AA=s.diag(A,D);V=s.zeros(4,M.cols).col_join(M);U=L.col_join(s.zeros(3,L.cols));RV=R.row_join(V)
   ck(R[:4,:].rank()==4);ck((C.row_join(-F))*R==s.zeros(2,R.cols));ck(RV.row_join(AA*R).rank()==RV.rank());ck(RV.row_join(U).rank()==RV.rank())
   okmain,_=sim(src,target);ck(okmain);eligible+=1
print(json.dumps({'status':'PASS','exact_assertions':count,'rational_eligible_main_cases':eligible,'observation_assumption':'C_Q1 injective; C_Q2 may have kernel','scope':'Exact finite controls of the explicit one-injective-specification proof, not a universal search or a full solution.'},indent=2))
