"""Unimodular certificates for complete normalized local scalar weights."""
from weights_explore import *
from collections import Counter
C=Counter();certs=[]
def ck(v,k):assert v,k;C[k]+=1
specs=[('original',(r,s),[3,10],[138,8,15,16,17,21,23,26,45,48,49,50,53,55,58,135]),('twist',(R,t),[1,3],[138,8,15,17,19,20,23,24,25,29,30,45,48,49,55,135])]
for name,ops,free,rows in specs:
 M=sy.Matrix(matrix(ops,True));ck(M.shape==(141,18),name+'_matrix_shape')
 cols=[i for i in range(18) if i not in free];U=M[rows,cols];ck(U.det()==-1,name+'_unimodular_minor')
 V=-U.inv()*M[rows,free];ck(all(x.q==1 for x in V),name+'_integral_exponents')
 E=sy.zeros(18,2)
 for j,c in enumerate(free):E[c,j]=1
 for i,c in enumerate(cols):
  for j in range(2):E[c,j]=V[i,j]
 ck(M*E==sy.zeros(141,2),name+'_all_relations')
 # Gauge exponents lambda0=A/B,lambda1=B for original;
 # lambda0=Q,lambda1=P for twist.
 lam=sy.Matrix([[1,-1],[0,1],[0,0]]) if name=='original' else sy.Matrix([[0,1],[1,0],[0,0]])
 G=sy.Matrix([[int(u==x)+int(u==y)-int(u==ops[k][3*x+y]//3)-int(u==ops[k][3*x+y]%3) for u in range(3)] for k in [0,1] for x in range(3) for y in range(3)])
 ck(G*lam==E,name+'_tensor_coboundary_formula')
 certs.append({'pair':name,'free_columns':free,'selected_rows':rows,'determinant':int(U.det()),'relation_matrix':[[int(x) for x in row] for row in M.tolist()],'solution_exponents':[[int(x) for x in row] for row in E.tolist()]})
Path(__file__).with_name('turn_4_lattice_certificate.json').write_text(json.dumps(certs,indent=2)+'\n')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'complete_relation_rows_per_pair':141,'unimodular_determinants':[-1,-1],'scope':'Complete normalized scalar whole-crossing weight classifications for two specific three-color welded pairs, over arbitrary coefficient fields or abelian coefficient groups. Not general nonabelian strandwise Q1.'},indent=2))
