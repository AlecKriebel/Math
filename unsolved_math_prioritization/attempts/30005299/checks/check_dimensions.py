#!/usr/bin/env python3
"""Exact characteristic-zero rank lower bounds certified by minors modulo 101."""
import sympy as s,json,random,itertools
from pathlib import Path
p=Path(__file__).resolve().parent;x=s.symbols('x0:4');X=s.Matrix(x);prime=101
A=[s.Matrix(a) for a in json.loads((p/'representation_counterexample.json').read_text())['symmetric_slices']]
M=s.Matrix.hstack(*(a*X for a in A))
def monomials(d):
 return [(a,b,c,d-a-b-c) for a in range(d,-1,-1) for b in range(d-a,-1,-1) for c in range(d-a-b,-1,-1)]
def polydict(f):return s.Poly(s.expand(f),*x).as_dict()
def matrix_of(polys,d):
 basis=monomials(d);ds=[polydict(f) for f in polys]
 return [[int(f.get(m,0)) for f in ds] for m in basis]
def rankcert(a):
 B=[[int(z)%prime for z in row] for row in a];nr=len(B);nc=len(B[0]);ids=list(range(nr));r=0;cols=[];rows=[];detsign=1;pivot_product=1
 for c in range(nc):
  pivot=next((j for j in range(r,nr) if B[j][c]),None)
  if pivot is None:continue
  if pivot!=r:B[pivot],B[r]=B[r],B[pivot];ids[pivot],ids[r]=ids[r],ids[pivot];detsign=-detsign
  val=B[r][c];pivot_product=pivot_product*val%prime;inv=pow(val,-1,prime);B[r]=[z*inv%prime for z in B[r]]
  for j in range(r+1,nr):
   v=B[j][c]
   if v:B[j]=[(a-v*b)%prime for a,b in zip(B[j],B[r])]
  cols.append(c);rows.append(ids[r]);r+=1
  if r==nr:break
 # Re-evaluate the chosen original submatrix determinant independently by modular elimination.
 C=[[a[i][j]%prime for j in cols] for i in rows];det=1
 for c in range(r):
  pivot=next(j for j in range(c,r) if C[j][c]);
  if pivot!=c:C[pivot],C[c]=C[c],C[pivot];det=-det
  v=C[c][c];det=det*v%prime;iv=pow(v,-1,prime)
  for j in range(c+1,r):
   f=C[j][c]*iv%prime
   for k in range(c,r):C[j][k]=(C[j][k]-f*C[c][k])%prime
 assert det%prime!=0
 return {'rows':nr,'columns':nc,'rank_mod_101':r,'minor_rows':rows,'minor_columns':cols,'minor_determinant_mod_101':det%prime}
co=M.cofactor_matrix(); polys=[]
for j in range(4):
 for a in range(4):
  for b in range(a,4):
   vec=s.zeros(4,1);vec[a]+=x[b]
   if a!=b:vec[b]+=x[a]
   polys.append(sum(co[i,j]*vec[i] for i in range(4)))
W=matrix_of(polys,4);cw=rankcert(W);assert cw['rank_mod_101']==25
print('Weddle derivative',cw['rank_mod_101'],flush=True)
rng=random.Random(5300);G=[s.eye(4),s.diag(1,2,3,4),s.Matrix(4,4,lambda i,j:rng.choice([-3,-2,-1,1,2,3])),s.Matrix(4,4,lambda i,j:rng.randrange(-3,4))]
N=sum((x[i]*G[i] for i in range(4)),s.zeros(4));cN=N.cofactor_matrix();gp=[cN[i,j]*x[k] for i in range(4) for j in range(4) for k in range(4)]
D=matrix_of(gp,4);cd=rankcert(D);assert cd['rank_mod_101']==34
print('General determinant derivative',cd['rank_mod_101'],flush=True)
# Certify smoothness of the Weddle example: degree-nine Jacobian ideal is all forms.
f=s.expand(M.det());grad=[s.diff(f,z) for z in x];basis6=monomials(6);basis9=monomials(9);lookup={v:i for i,v in enumerate(basis9)};J=[[0]*(4*len(basis6)) for _ in basis9]
for a,g in enumerate(grad):
 for b,mu in enumerate(basis6):
  for nu,val in polydict(g).items():J[lookup[tuple(u+v for u,v in zip(mu,nu))]][a*len(basis6)+b]=int(val)
cj=rankcert(J);assert cj['rank_mod_101']==len(basis9)==220
print('Smoothness Macaulay matrix',cj['rank_mod_101'],flush=True)
out={'status':'PASS','prime':prime,'method':'A nonzero minor modulo 101 is a nonzero integer minor, hence a characteristic-zero rank lower bound. Written universal upper bounds complete the dimension argument.','weddle_derivative':cw,'general_determinant_derivative':cd,'general_determinant_coefficient_matrices':[a.tolist() for a in G],'weddle_smoothness_degree9_jacobian':cj,'affine_image_dimensions':{'weddle':25,'general_determinantal':34},'projective_image_dimensions':{'weddle':24,'general_determinantal':33},'smooth_example_quartic':str(f)}
(p/'DIMENSION_CERTIFICATES.json').write_text(json.dumps(out,indent=2,default=int)+'\n');print(json.dumps({k:out[k] for k in ['status','affine_image_dimensions','projective_image_dimensions']},indent=2))
