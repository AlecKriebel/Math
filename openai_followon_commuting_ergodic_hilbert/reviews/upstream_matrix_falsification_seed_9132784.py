import numpy as np
rng=np.random.default_rng(9132784)
def herm(n):
 a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));return (a+a.conj().T)/2
def gram(n,r):
 a=rng.normal(size=(r,n))+1j*rng.normal(size=(r,n));return a.conj().T@a
def b(P,K):
 w,U=np.linalg.eigh(P); scale=max(1.,np.max(w)); p=np.maximum(w,0); q=np.sqrt(p); Z=U.conj().T@K@U; den=q[:,None]+q[None,:]
 keep=(p[:,None]>1e-10*scale)&(p[None,:]>1e-10*scale)
 return 1.5*np.sum(np.abs(Z[keep])**2/den[keep]).real
def op(A):return np.linalg.norm(A,2)
maxrat=[0.,0.,0.]
for trial in range(1500):
 ns=[rng.integers(1,6) for _ in range(3)]
 W=[];D=[];cost=[]
 for v in range(3):
  X=rng.normal(size=(ns[v],ns[(v+1)%3]))+1j*rng.normal(size=(ns[v],ns[(v+1)%3]));
  if trial%5==0:X[:,1:]=0
  W.append(X); D.append(herm(ns[v]))
 for v in range(3):
  R=np.column_stack((W[v],W[(v-1)%3].conj().T));cost.append(b(R.conj().T@R,R.conj().T@D[v]@R))
 tau=np.trace(D[0]@W[0]@D[1]@W[1]@D[2]@W[2]);rhs=5/3*max(op(d) for d in D)*sum(cost)
 rat=abs(tau)/rhs if rhs else 0;maxrat[0]=max(maxrat[0],rat)
 if rat>1+1e-8:raise RuntimeError(('mixed',trial,rat))
 n=rng.integers(1,8);P=gram(n,n);extra=gram(n,n);Q=P+extra;K=herm(n)
 rat=b(Q,K)/b(P,K);maxrat[1]=max(maxrat[1],rat)
 if rat>1+1e-8:raise RuntimeError(('order',trial,rat))
 Ts=[gram(n,n) for _ in range(3)];Ks=[herm(n) for _ in range(3)];wt=rng.dirichlet(np.ones(3));avgT=sum(t*w for t,w in zip(Ts,wt));avgK=sum(k*w for k,w in zip(Ks,wt));rhs=sum(b(t,k)*w for t,k,w in zip(Ts,Ks,wt));rat=b(avgT,avgK)/rhs;maxrat[2]=max(maxrat[2],rat)
 if rat>1+1e-8:raise RuntimeError(('convexity',trial,rat))
print('1500 trials each; max lhs/rhs ratios mixed, order, convexity:',maxrat)
