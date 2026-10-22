"""Floating-point regression checks of authored identities, not a proof."""
import json
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(1829)

def phi(M,h):
    n=M.shape[0]; Z=np.zeros((2*n,2*n)); Z[:n,:n]=M; Z[:n,n:]=np.eye(n)
    return expm(h*Z)[:n,n:]

def ksl(U,S,V,A,B,C,h):
    m,r=U.shape; n=V.shape[0]; B0=V.T@B@V
    # Exact linear affine K subflow through vectorized exponential.
    MK=np.kron(np.eye(r),A)+np.kron(B0.T,np.eye(m)); k0=(U@S).reshape(-1,order='F'); c=(C@V).reshape(-1,order='F')
    K=(expm(h*MK)@k0+phi(MK,h)@c).reshape(m,r,order='F')
    U1,Sh=np.linalg.qr(K); A1=U1.T@A@U1; D=U1.T@C@V
    MS=-np.kron(np.eye(r),A1)-np.kron(B0.T,np.eye(r))
    St=(expm(h*MS)@Sh.reshape(-1,order='F')-phi(MS,h)@D.reshape(-1,order='F')).reshape(r,r,order='F')
    ML=np.kron(np.eye(r),B.T)+np.kron(A1,np.eye(n))
    L=(expm(h*ML)@(V@St.T).reshape(-1,order='F')+phi(ML,h)@(C.T@U1).reshape(-1,order='F')).reshape(n,r,order='F')
    return U1@L.T,U1,K

rows=[]
for i in range(24):
    m,n,r=4,3,2
    U=np.linalg.qr(rng.normal(size=(m,r)))[0]; V=np.linalg.qr(rng.normal(size=(n,r)))[0]
    S=np.diag([1,10.**(-(i%9))])
    AA=rng.normal(size=(m,m)); BB=rng.normal(size=(n,n)); A=-AA@AA.T; B=-BB@BB.T
    C=rng.normal(size=(m,n)); h=[.001,.01,.1][i%3]
    Y=U@S@V.T
    yl,_,_=ksl(U,S,V,A,B,np.zeros((m,n)),h)
    exact=expm(h*A)@Y@expm(h*B)
    # Right affine endpoint is projection of the exact full endpoint.
    yr,ur,_=ksl(U,S,V,np.zeros((m,m)),B,C,h)
    xr=Y@expm(h*B)+C@phi(B,h)
    # Left affine endpoint and conditional local bound.
    yy,uu,K=ksl(U,S,V,A,np.zeros((n,n)),C,h)
    P=uu@uu.T; Q=np.eye(n)-V@V.T; a=uu.T@A@uu
    ident=K@V.T+uu@phi(a,h)@uu.T@C@Q
    x=expm(h*A)@Y+phi(A,h)@C
    eps=np.linalg.norm((np.eye(m)-P)@C@Q,'fro')
    gamma=np.linalg.norm((np.eye(m)-P)@A@uu,2)
    bound=h*eps+h*h*gamma*np.linalg.norm(C,'fro')/2
    rows.append({'trial':i,'linear_exactness_error':float(np.linalg.norm(yl-exact)),
      'right_identity_error':float(np.linalg.norm(yr-ur@ur.T@xr)),
      'left_identity_error':float(np.linalg.norm(yy-ident)),
      'left_local_error':float(np.linalg.norm(yy-x)), 'left_bound':float(bound),
      'bound_pass':bool(np.linalg.norm(yy-x)<=bound+1e-12)})
assert all(x['bound_pass'] for x in rows)
assert max(max(x['linear_exactness_error'],x['right_identity_error'],x['left_identity_error']) for x in rows)<1e-10
print(json.dumps({'seed':1829,'checks':rows,'all_pass':True},indent=2))
