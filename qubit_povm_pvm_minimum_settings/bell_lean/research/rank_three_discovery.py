#!/usr/bin/env python3
"""Optional floating-point discovery experiment, NOT verification evidence.

Requires NumPy, which is not needed by the exact checker. A finite-difference
Hessian suggests sparse rational coupled directions. The certified final
identities are recomputed separately in scripts/semantic_audit.py --suite saddle.
Floating-point output may vary by platform. No source proof is certified here.
"""
import numpy as np
from itertools import combinations
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
U=.6*I+.8j*X
rho=np.zeros((4,4),complex);rho[1,1]=rho[2,2]=.5;rho[1,2]=rho[2,1]=-.5
F=np.array([[-9/10,-2,6/5,2/5],[-2/25,-9/10,6/25,-38/25],[6/25,6/5,-68/25,14/25],[-38/25,2/5,14/25,28/25]])
def su(v):
 a,b,c=v;n=1+a*a+b*b+c*c;w=(1-a*a-b*b-c*c)/n;x=2*a/n;y=2*b/n;z=2*c/n
 return np.array([[w+1j*x,y+1j*z],[-y+1j*z,w-1j*x]])
def tri(t,q):
 pts=[(1,0),((1-t*t)/(1+t*t),2*t/(1+t*t)),((1-q*q)/(1+q*q),2*q/(1+q*q))]
 A=np.array([[1,1,1],[p[0] for p in pts],[p[1] for p in pts]]);ww=np.linalg.solve(A,np.array([1.,0,0]))
 return [ww[j]*(I+pts[j][0]*X+pts[j][1]*Y) for j in range(3)]
def score(v):
 S=I+(v[0]+1j*v[1])*X+(v[2]+1j*v[3])*Y+(v[4]+1j*v[5])*Z
 S=np.kron(S,I);R=S@rho@S.conj().T;R/=np.trace(R)
 Ua=su(v[6:9]);Ub=U@su(v[11:14]);TA=tri(2+v[9],-2+v[10]);TB=tri(2+v[14],-2+v[15])
 A=[(I+Z)/2,(I-Z)/2,*[Ua@m@Ua.conj().T for m in TA[:2]]]
 B=[U@(I+Z)/2@U.conj().T,U@(I-Z)/2@U.conj().T,*[Ub@m@Ub.conj().T for m in TB[:2]]]
 return float(sum(F[i,j]*np.trace(R@np.kron(A[i],B[j])).real for i in range(4) for j in range(4)))
z=np.zeros(16);base=score(z);h=1e-4;D=np.eye(16)*h
H=np.zeros((16,16))
for i in range(16):
 H[i,i]=(score(D[i])+score(-D[i])-2*base)/h**2
 for j in range(i):
  H[i,j]=H[j,i]=(score(D[i]+D[j])+score(-D[i]-D[j])-score(D[i]-D[j])-score(-D[i]+D[j]))/(4*h*h)
print('eigs',np.linalg.eigvalsh(H));
for k in [2,3,4]:
 best=(-np.inf,None,None)
 for ix in combinations(range(16),k):
  ee,vv=np.linalg.eigh(H[np.ix_(ix,ix)])
  if ee[-1]>best[0]:best=(ee[-1],ix,vv[:,-1])
 print('best',k,best)
 if best[0]>1e-3:
  vec=np.zeros(16);v=best[2]/np.max(np.abs(best[2]));vec[list(best[1])]=np.round(v*10)/10
  print('rational direction',vec,'hessian',vec@H@vec,'score .01',score(vec*.01),'score -.01',score(-vec*.01));break
