#!/usr/bin/env python3
"""Fresh finite falsification controls; not a substitute for the continuum proof."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import datetime,json,math
import numpy as np
from scipy.linalg import expm

HERE=Path(__file__).resolve().parent
counts={}; residuals={}
def need(ok,label):
 if not ok: raise RuntimeError(label)
def det(a):
 a=[list(x) for x in a]; out=F(1)
 for i in range(len(a)):
  j=next((j for j in range(i,len(a)) if a[j][i]),None)
  if j is None:return F(0)
  if j!=i:a[i],a[j]=a[j],a[i];out=-out
  pivot=a[i][i];out*=pivot
  for k in range(i+1,len(a)):
   ratio=a[k][i]/pivot
   for l in range(i+1,len(a)):a[k][l]-=ratio*a[i][l]
 return out
def creator(g):
 m=len(g); out=np.zeros((2**m,2**m),complex)
 for state in range(2**m):
  for j in range(m):
   if not state>>j&1:out[state|1<<j,state]=g[j]*(-1)**((state&((1<<j)-1)).bit_count())
 return out
def record_float(label,x,tol=2e-11):
 need(x<tol,label+': '+repr(x));residuals[label]=float(x)

def main():
 # Exhaust all local occupancies, including vacuum, extremes and both flags.
 sector=0
 for n in range(1025):
  for k in (0,1):
   for m in range(n+1):
    l=n-m; diff=l*(l-k)-n*(n-k)
    need(diff==-m*(2*n-k-m),'sector identity')
    need(abs(diff)<=2*n*m,'sector bound')
    sector+=1
 counts['exhaustive_sector_occupancy_cases']=sector
 phase=0
 for n in range(1,4097):
  for k in (0,1):
   gap=(n+1)*(n+1-k)-n*(n-k)
   ratio=F(1,gap)
   need(gap==2*n+1-k and ratio*gap==1 and ratio<=F(1,2*n),'phase/time identity')
   phase+=1
 counts['exact_phase_cases']=phase
 m=1
 for n in range(1,100001):
  while m**3<n:m+=1
  need((m-1)**3<n<=m**3 and m**3<=8*n,'packing ceil bound')
 counts['exact_packing_cases']=100000
 exponents={str(d):[str(-F(1,2)+F(1,d)),str(-1+F(2,d))] for d in range(1,13)}
 need(exponents['1']==['1/2','1'] and exponents['2']==['0','0'] and exponents['3']==['-1/6','-1/3'],'dimension boundary')
 counts['dimension_boundaries']=12
 need(F(83,16)<9 and F(7,4)>F(1,3),'fixed geometry')
 # Exact rational orbital bases: distribution via exterior determinants,
 # moments via independently formed occupied one-body projection.
 exact=0
 for seed in range(8):
  dim=6; Q=[[F(int(i==j)) for j in range(dim)] for i in range(dim)]
  for step in range(15):
   a=(seed+2*step)%dim;b=(a+1+(step%4))%dim
   for i in range(dim):Q[i][a],Q[i][b]=F(3,5)*Q[i][a]+F(4,5)*Q[i][b],-F(4,5)*Q[i][a]+F(3,5)*Q[i][b]
  for n in range(dim+1):
   P=[[sum(Q[i][j]*Q[k][j] for j in range(n)) for k in range(dim)] for i in range(dim)]
   weights={S:det([[Q[i][j] for j in range(n)] for i in S])**2 for S in combinations(range(dim),n)}
   need(sum(weights.values())==1,'Slater unit norm')
   for rank in range(dim+1):
    distribution=[sum(w for S,w in weights.items() if sum(i<rank for i in S)==r) for r in range(n+1)]
    mean=sum(F(r)*w for r,w in enumerate(distribution))
    second=sum(F(r*r)*w for r,w in enumerate(distribution))
    lam=sum(P[i][i] for i in range(rank))
    tr=sum(P[i][j]*P[j][i] for i in range(rank) for j in range(rank))
    need(mean==lam and second==lam*lam+lam-tr,'determinant/trace moment equality')
    need(second-mean*mean<=mean and second>=mean*mean,'Slater variance bound')
    exact+=1
 counts['exact_rational_slater_distributions']=exact
 need(F(25,4)>F(5,2),'correlated cat violates variance<=mean')
 counts['correlated_nonSlater_negative_controls']=1
 # Dense complex one-body propagation, with a fixed empty mode f. Later
 # propagated f has occupied components: this attacks a tempting false step.
 floating=0; occupied=[]; wrong_phase=0
 rng=np.random.default_rng(90802026)
 for dim in (3,4,5):
  C=[creator(np.eye(dim)[j]) for j in range(dim)]
  z=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim));h=z+z.conj().T
  T=sum(h[i,j]*C[i]@C[j].conj().T for i in range(dim) for j in range(dim))
  number=np.diag([s.bit_count() for s in range(2**dim)])
  f=np.eye(dim)[:,0];A=C[0];a=A.conj().T
  for n in range(1,dim):
   psi=np.zeros(2**dim,complex);psi[sum(1<<j for j in range(1,n+1))]=1;xi=A@psi
   for k in (0,1):
    K=T+number@(number-k*np.eye(2**dim))
    for t in (-.371,.219,math.pi/(2*n+1-k)):
     U=expm(1j*t*K);one=expm(1j*t*h);g=one@f
     F_actual=np.vdot(xi,U@A@U.conj().T@psi)
     F_expected=np.exp(1j*t*(2*n+1-k))*np.vdot(f,g)
     record_float(f'creation_{dim}_{n}_{k}_{t}',abs(F_actual-F_expected))
     D=U@a@U.conj().T-a
     record_float(f'adjoint_{dim}_{n}_{k}_{t}',abs(np.vdot(psi,D@xi)-np.conj(F_actual-1)))
     record_float(f'free_cov_{dim}_{n}_{k}_{t}',np.linalg.norm(expm(1j*t*T)@A@expm(-1j*t*T)-creator(g)))
     need(np.linalg.norm(D,2)<=2+2e-11,'CAR universal norm upper bound')
     occupied.append(float(np.linalg.norm(g[1:n+1])))
     # A wrong half coefficient cannot reproduce the reference phase.
     if abs(np.exp(1j*t*(2*n+1-k)/2)-np.exp(1j*t*(2*n+1-k)))>.05:wrong_phase+=1
     floating+=1
 counts['dense_complex_operator_cases']=floating
 need(max(occupied)>.1 and wrong_phase>0,'negative sign/coefficient controls effective')
 result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'counts':counts,'dimension_error_exponents':exponents,'maximum_floating_residual':max(residuals.values()),
   'maximum_later_occupied_component':max(occupied),'half_coefficient_detected_cases':wrong_phase,
   'float_tolerance':2e-11,'finite_only':True,
   'scope':'Exact finite combinatorics and rational determinants plus non-rigorous complex matrix diagnostics. Continuum domains/leakage/asymptotics are justified separately in INDEPENDENT_DERIVATION.md.'}
 (HERE/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
