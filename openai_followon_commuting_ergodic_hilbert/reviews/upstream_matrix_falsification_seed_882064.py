import numpy as np
rng=np.random.default_rng(882064)
def H(n):
 X=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));return (X+X.conj().T)/2
def b(P,K):
 p,U=np.linalg.eigh(P);keep=p>1e-11*max(1.,np.max(p));p=p[keep];U=U[:,keep];Z=U.conj().T@K@U;den=np.sqrt(p[:,None])+np.sqrt(p[None,:]);return float(1.5*np.sum(abs(Z)**2/den).real)
ordmax=0.;jmax=0.;cubmax=0.
for t in range(1000):
 n=6;r=(t%5)+1;R=rng.normal(size=(r,n))+1j*rng.normal(size=(r,n));P=R.conj().T@R;K=R.conj().T@H(r)@R;B=rng.normal(size=(3,n))+1j*rng.normal(size=(3,n));a=1.+rng.random()*9;Q=P/a+B.conj().T@B
 ratio=b(Q,K)/b(P,K)/np.sqrt(a);ordmax=max(ordmax,ratio)
 assert ratio<=1+1e-7
 # Common support is a random r-dimensional subspace of ambient 6-space.
 U=np.linalg.qr(rng.normal(size=(n,r))+1j*rng.normal(size=(n,r)))[0];Ts=[];Ks=[]
 for j in range(4):
  X=rng.normal(size=(r,r))+1j*rng.normal(size=(r,r));Ts.append(U@(X.conj().T@X)@U.conj().T);Ks.append(U@H(r)@U.conj().T)
 w=rng.dirichlet(np.ones(4));ratio=b(sum(x*y for x,y in zip(Ts,w)),sum(x*y for x,y in zip(Ks,w)))/sum(b(x,y)*z for x,y,z in zip(Ts,Ks,w));jmax=max(jmax,ratio);assert ratio<=1+1e-7
 # Standalone signed cubic matrix test, with arbitrary Hermitian D.
 m=rng.normal(size=n);m[t%n]=0;q=abs(m);D=H(n);den=q[:,None]+q[None,:];wt=np.zeros_like(den);mask=den>0;wt[mask]=(q[:,None]**2*q[None,:]**2)[mask]/den[mask];Q0=np.sum(wt*abs(D)**2);tr=np.trace((D*m[None,:])@(D*m[None,:])@(D*m[None,:]));rhs=5*np.linalg.norm(D,2)*Q0;ratio=abs(tr)/rhs;cubmax=max(cubmax,ratio);assert ratio<=1+1e-7
print('1000 trials each; max ratios singular-support order, common proper-support averaging, arbitrary signed cubic:',ordmax,jmax,cubmax)
# Scalar boundary identity and homogeneous scaling.
for p in [1e-20,1e-8,1.,1e8,1e20]:
 k=2.;lhs=.75*k*k/np.sqrt(p);rhs=b(np.array([[p]]),np.array([[k]])) if p>1e-11 else 'below numerical support threshold; use exact scalar formula'
 print('scalar',p,'exact cost',lhs,'numerical',rhs)
