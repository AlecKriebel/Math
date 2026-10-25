#!/usr/bin/env python3
"""Fresh exact original-chain/union-dual/marked-phase interfaces.
Uses only the independent forward checker, not supplied code.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,itertools,time
import sympy as s
from fresh_forward_controls import fixation,J
pop=lambda x:bin(x).count('1')
R=s.Rational;checks=[];details={};start=time.time()
def check(x,label):
 if not x:raise AssertionError(label)
 checks.append(label)
def stat(K):
 d=K.rows;M=K.T-s.eye(d);M[d-1,:]=s.ones(1,d);v=s.zeros(d,1);v[d-1]=1
 return (M.inv(method='DM')*v).T
for n,which in [(3,'complete'),(3,'directed'),(4,'directed')]:
 full=(1<<n)-1;states=list(range(1,full));idx={b:i for i,b in enumerate(states)}
 if which=='complete':P=J(n)
 else:
  W=s.Matrix(n,n,lambda v,u:0 if v==u else 2+(3*v+7*u+u*v)%11);P=s.Matrix(n,n,lambda v,u:W[v,u]/sum(W[v,j] for j in range(n)))
 # Fair-geometric burst set distribution by subset Mobius inversion.
 burst={}
 for v in range(n):
  legal=full^(1<<v)
  for B in range(1,full+1):
   if B&~legal:continue
   value=s.S.Zero;D=B
   while True:
    p=sum((P[v,i] for i in range(n) if D>>i&1),s.S.Zero)
    value+=(-1)**(pop(B)-pop(D))*p/(2-p)
    if D==0:break
    D=(D-1)&B
   burst[v,B]=value
  check(sum(q for (vv,B),q in burst.items() if vv==v)==1,f'burst normalized {n}{which}{v}')
 U=s.zeros(len(states));active_current={}
 for A in states:
  for v in range(n):
   if not A>>v&1:U[idx[A],idx[A]]+=R(1,n);continue
   for (vv,B),prob in burst.items():
    if vv==v:U[idx[A],idx[(A&~(1<<v))|B]]+=prob/n
 pi=stat(U);m=sum(pi[idx[A]]*pop(A) for A in states)
 rho,h,T=fixation(P)
 check(rho==m/n,f'coverage mean {n}{which}')
 for S in range(full+1):
  cov=sum(pi[idx[A]] for A in states if A&S)
  orig=0 if S==0 else (1 if S==full else h[S-1]);check(cov==orig,f'coverage all sets {n}{which}{S}')
 # Rectangular channels are constructed by literal sampling/coin operations.
 Z=[(C,v) for v in range(n) for C in range(full+1) if not C>>v&1];Y=[z for z in Z if z[0]];zi={z:i for i,z in enumerate(Z)};yi={z:i for i,z in enumerate(Y)}
 Achan=s.zeros(len(Z),len(Y));Rchan=s.zeros(len(Y),len(Z))
 for C,v in Z:
  for i in range(n):
   if i!=v:Achan[zi[C,v],yi[C|(1<<i),v]]+=P[v,i]
 for B,v in Y:
  Rchan[yi[B,v],zi[B,v]]+=R(1,2)
  for w in range(n):
   if B>>w&1:Rchan[yi[B,v],zi[B&~(1<<w),w]]+=R(1,2*pop(B))
 K=Rchan*Achan;M=Achan*Rchan;nu=stat(K);lam=nu*Rchan
 check(nu*K==nu and lam*M==lam,f'both phase stationary {n}{which}')
 check(nu*s.Matrix([R(1,pop(B)) for B,v in Y])==s.Matrix([[1/m]]),f'inverse mean {n}{which}')
 sig=s.zeros(1,len(Z));eta=s.zeros(1,len(Y))
 for C,v in Z:
  AV=C|1<<v
  sig[zi[C,v]]=pi[idx[AV]] if AV in idx else 0
 for S in states:
  for v in range(n):
   if S>>v&1:
    for (vv,B),prob in burst.items():
     if vv==v:eta[yi[(S&~(1<<v))|B,v]]+=pi[idx[S]]*prob
 check(eta/m==nu,f'marked current nu {n}{which}')
 for C,v in Z:
  e=eta[yi[C,v]] if C else 0
  check((sig[zi[C,v]]+e)/(2*m)==lam[zi[C,v]],f'marked current lambda {n}{which}{C}{v}')
 if which=='complete':
  N=n-1
  check(all(nu[j]==R(pop(B),n*N*2**(N-1)) for j,(B,v) in enumerate(Y)),'complete labelled active stationary law')
 details[str(n)+which]={'rho':str(rho),'mean':str(m),'union_states':len(states),'pre_states':len(Z),'post_states':len(Y)}
 print('dual',n,which,flush=True)
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','checks':len(checks),'labels':checks,'details':details,'seconds':time.time()-start,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite exact original subset chain vs geometric Mobius union dual; full coverage, rectangular phase stationarity and marked current laws on positive nonreversible examples. Not a finite extrapolation.'}
Path(__file__).with_name('fresh_dual_results.json').write_text(json.dumps(result,indent=2)+'\n');print({'status':'PASS','checks':len(checks)})
