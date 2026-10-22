#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
import json
checks=0

def ck(x):
 global checks
 assert x
 checks+=1
threshold_cases=0
for d in range(2,41):
 for q in range(1,16):
  r=F(1,d**q);t=F(1,2**q);s=F((d+1)**q,(2*d)**q)
  R=(1-r)/(d-r);S=(1-s)/(1+(d-1)*t-s)
  ck(0<R<1 and 0<S<1)
  ck((1-s)*(d-r)-(1-r)*(1+(d-1)*t-s)==(d-1)*(1-t-s+t*r))
  if q==1:ck(R==S==F(1,d+1))
  else:ck(S>R)
  for k in range(21):
   p=F(k,20);rv=p*d+(1-p)*r;sv=p*(1+(d-1)*t)+(1-p)*s
   ck((rv>1)==(p>R));ck((sv>1)==(p>S))
   ck(rv==p+(1-p)*r+p*(d-1))
   ck(sv==p+(1-p)*s+p*(d-1)*t)
  threshold_cases+=1
ck(F(1,2)*2+F(1,2)*F(1,4)==F(9,8))
ck(F(1,2)*F(5,4)+F(1,2)*F(9,16)==F(29,32))
ck(F(9,20)*2+F(11,20)*F(1,4)==F(83,80))
ck(F(7,4)**2>3 and F(3,2)**2>2)
ck(F(9,20)+(33*F(7,4)+18*F(3,2))/160==F(627,640)<1)
ck(482<22**2 and 691>26**2)
# Triangular 2x2 nuclear norm squared = trace(B*B)+2|det B|.
for n in range(101):
 p=F(n,100)
 Rblock2=F(1,4)+(1-p)**2/4+p*p/4+p/2
 Sblock2=F(9,16)+3*(1-p)**2/16+p*p/16+3*p/8
 ck(Rblock2==(1+p*p)/2)
 ck(Sblock2==(3+p*p)/4)
 ck(((3+p*p)>(2-p)**2)==(p>F(1,4)))
 ck(((1+p*p)>2*(1-p)**2)==(p*p-4*p+1<0))
# Qubit tetrahedral SIC Gram, represented by Pauli coordinates.
# Normalized tester rows are (sqrt(3), n1,n2,n3)/sqrt(8), n_j=+/-1.
rows=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
for a in range(3):ck(sum(x[a] for x in rows)==0)
for a,b in product(range(3),repeat=2):ck(sum(x[a]*x[b] for x in rows)==4*int(a==b))
ck(F(4*3,8)==F(3,2));ck(F(4,8)==F(1,2))
# Exact lower dual bound for diagonal blocks on rational l2 unit vectors.
points=[]
for n in range(21):
 t=F(n,20);points.append(((1-t*t)/(1+t*t),2*t/(1+t*t)))
for a,b,c in product(points,repeat=3):
 ck(a[0]*b[0]*c[0]+a[1]*b[1]*c[1]<=1)
# Pauli correlation matrix of eta_p from its explicit density matrix.
def add(A,B):return [[A[i][j]+B[i][j] for j in range(len(A))] for i in range(len(A))]
def kron(A,B):return [[A[i//len(B)][j//len(B)]*B[i%len(B)][j%len(B)] for j in range(len(A)*len(B))] for i in range(len(A)*len(B))]
# Use an exact Gaussian pair for the Y terms, checking via Y tensor Y explicitly.
I=[[1,0],[0,1]];X=[[0,1],[1,0]];Z=[[1,0],[0,-1]]
YY=[[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]]
for n in range(31):
 p=F(n,30)
 rho=[[F(0) for j in range(4)] for i in range(4)]
 rho[0][0]=F(1,2);rho[1][1]=(1-p)/2;rho[3][3]=p/2;rho[0][3]=rho[3][0]=p/2
 coeff=add(kron(I,I),[[(1-p)*z for z in row] for row in kron(Z,I)])
 coeff=add(coeff,[[p*z for z in row] for row in kron(Z,Z)])
 coeff=add(coeff,[[p*z for z in row] for row in kron(X,X)])
 coeff=add(coeff,[[-p*z for z in row] for row in YY])
 for i,j in product(range(4),repeat=2):ck(rho[i][j]==coeff[i][j]/4)
 ck(sum(rho[i][i] for i in range(4))==1)
 # Nontrivial 00/11 block has nonnegative principal minors.
 ck(rho[0][0]>=0 and rho[3][3]>=0 and rho[0][0]*rho[3][3]-rho[0][3]**2>=0)
print(json.dumps({'exact_assertions':checks,'even_GHZ_threshold_cases':threshold_cases,'three_qubit_R_lower':'83/80','three_qubit_S_strict_upper':'627/640','four_qubit_exact_values':['9/8','29/32'],'reverse_example_parameter':'4/15','complex_projective_certificates_in_written_proof':True,'numerical_nuclear_norm_optimization_used':False},indent=2))
