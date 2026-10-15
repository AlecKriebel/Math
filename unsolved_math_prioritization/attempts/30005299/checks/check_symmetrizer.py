#!/usr/bin/env python3
"""Exact fixed-representation symmetrizer and false-negative certificate."""
import sympy as s,json
from pathlib import Path
p=Path(__file__).resolve().parent
record=json.loads((p/'representation_counterexample.json').read_text())
x=s.symbols('x0:4');A=[s.Matrix(a) for a in record['symmetric_slices']]
M=s.Matrix.hstack(*(a*s.Matrix(x) for a in A));u=s.symbols('u0:16');U=s.Matrix(4,4,u)
def linear_test(M):
 expr=[]
 for j in range(4):
  T=U*M[:,j].jacobian(x)
  expr += [T[i,k]-T[k,i] for i in range(4) for k in range(i+1,4)]
 return s.linear_eq_to_matrix(expr,u)[0]
def cert(L,rank):
 rows=list(L.T.rref()[1]);cols=list(L[rows,:].rref()[1]);B=L.extract(rows,cols);det=B.det();assert len(rows)==len(cols)==rank and det!=0
 return {'matrix':L.tolist(),'rank':rank,'minor_rows':rows,'minor_columns':cols,'minor_determinant':str(det),'nullspace':[list(v) for v in L.nullspace()]}
L=linear_test(M);T=linear_test(M.T)
assert L*s.Matrix(list(s.eye(4)))==s.zeros(24,1)
assert len(L.nullspace())==1 and len(T.nullspace())==0
assert M.det().subs(dict(zip(x,[1,0,0,0])))==-12
assert s.expand(M.det()-M.T.det())==0
Q=[(s.Matrix(x).T*a*s.Matrix(x))[0]/2 for a in A]
assert s.Matrix(4,4,lambda i,j:s.diff(Q[j],x[i]))==M
out={'status':'PASS','symmetric_slices':record['symmetric_slices'],'quadrics':[str(q.expand()) for q in Q],'determinant_at_1000':-12,'jacobian_test':cert(L,15),'transpose_test':cert(T,16),'scope':'The transpose represents exactly the same Weddle quartic, but its left-right equivalence class has no integrable representative. This does not certify smoothness of this example.'}
(p/'SYMMETRIZER_CERTIFICATE.json').write_text(json.dumps(out,indent=2,default=int)+'\n');print({k:out[k] for k in ['status','determinant_at_1000','scope']});print('minors',out['jacobian_test']['minor_determinant'],out['transpose_test']['minor_determinant'])
