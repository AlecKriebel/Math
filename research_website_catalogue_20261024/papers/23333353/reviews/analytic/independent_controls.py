"""Own exact finite/boundary controls; all-state proof is in DERIVATIONS.md."""
import sympy as S
import itertools,json
I=S.eye(4);p=S.diag(0,0,1,1);q=S.diag(0,1,0,1);basis=S.Matrix.hstack(S.ones(4,1),p.diagonal().T,q.diagonal().T,(p*q).diagonal().T)
assert basis.det()!=0 and S.Matrix.hstack(S.ones(4,1),p.diagonal().T,q.diagonal().T).rank()==3
records=[];word_checks=0
for t in [S.Rational(0),S.Rational(1,2),S.Rational(16,25),S.Rational(1)]:
 r=S.zeros(4);r[0,0]=1-t;r[3,3]=t;r[0,3]=r[3,0]=S.sqrt(t*(1-t));assert r*r==r and S.trace(r)==1 and r.rank()==1
 phi=lambda a:S.trace(r*a)
 for i in range(4):
  e=S.zeros(4);e[i,i]=1;assert phi(e)==([1-t,0,0,t][i])
 for length in range(1,9):
  for labels in itertools.product([0,1],repeat=length):
   m=I
   for j in labels:m=m*([p,q][j])
   assert phi(m)==t;word_checks+=1
 E=S.zeros(4);E[0,3]=1;e00=S.diag(1,0,0,0)
 assert phi(e00*E)-phi(E*e00)==S.sqrt(t*(1-t))
 records.append({'t':str(t),'density_matrix':[[str(v) for v in row] for row in r.tolist()],'rank':r.rank(),'classical_correlation_minus_product':str(t-t*t),'nontrace_witness':str(phi(e00*E)-phi(E*e00))})
# Equality graph from P_iOmega=Q_jOmega, i!=j.
graph=[]
for n in range(1,7):
 vertices=[('P',i) for i in range(n)]+[('Q',i) for i in range(n)];adj={v:set() for v in vertices}
 for i in range(n):
  for j in range(n):
   if i!=j:adj['P',i].add(('Q',j));adj['Q',j].add(('P',i))
 unseen=set(vertices);cc=[]
 while unseen:
  todo=[next(iter(unseen))];seen=set(todo)
  for v in todo:
   for z in adj[v]-seen:seen.add(z);todo.append(z)
  unseen-=seen;cc.append(sorted(seen))
 assert len(cc)==(2 if n<=2 else 1);graph.append({'copies':n,'components':cc})
# Exact two-copy negativecontrol: an extreme invariant quotientstate, but not infinite.
chars=[[(1,0),(0,1)],[(0,1),(1,0)]]
for length in range(1,9):
 for labs in itertools.product([0,1],repeat=length):
  vals=[]
  for c in chars:
   vals.append(S.prod(c[0][0] if j==0 else c[1][1] for j in labs))
  assert sum(vals)/S.Integer(2)==S.Rational(1,2)
assert chars[0][::-1]==chars[1]
assert S.Rational(sum(c[0][0]*c[0][1] for c in chars),2)==0
# LaurentpositiveextensionwouldrequirePSDGram[[0,1],[1,b]], impossibleforallb.
b=S.symbols('b',real=True);det=S.det(S.Matrix([[0,1],[1,b]]));assert det==-1
# FiniteS3averagingillustratestheC*extensionargument: pureuniformvectorstateextends
# theuniqueinvariantdiagonalstate; averaging preservesdiagonalrestriction.
base=S.Matrix([[S.Rational(1,3)]*3]*3);assert base*base==base and base.rank()==1
for perm in itertools.permutations(range(3)):
 U=S.zeros(3)
 for i,j in enumerate(perm):U[j,i]=1
 assert U*base*U.T==base
# Maintracial-upstairsvariantcannotmeetforcedsame-copyproductmoment.
assert S.trace(p*q)/4==S.Rational(1,4)!=S.Rational(1,2)
print(json.dumps({'status':'own_exact_controls_passed','basis_determinant':str(basis.det()),'B_C_intersection_dimension':1,'matrix_state_controls':records,'finite_word_checks':word_checks,'equality_graph_controls':graph,'two_copy_control_crosslaw_moment':'1/2','two_copy_samecopy_pq_moment':'0 != original1/2','two_copy_extremality_scope':'provedbyinvariantquotientfaceargument, notbyfiniteenumeration','Laurent_Gram_determinant_for_all_b':str(det),'finite_S3_invariant_extension_rank':1,'tracial_upstairs_samecopy_pq':'1/4 incompatiblewithforced1/2','limits':'Exactfinite/matrix/symboliccontrols; do notestablishinfiniteallword/allstateprooforpriority.'},indent=2))
