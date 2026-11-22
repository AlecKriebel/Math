import numpy as np, scipy.linalg as sl, mpmath as mp
exec(open('curve_check.py').read().split("# ---- reconstruction test")[0])
P=P0; g=g0; Q=np.linalg.inv(g); S=P.T@Q@P
y=[Q@P@rj for rj in r]
def Phi(yv): return np.array([yv[2]*(yv[0]+yv[3]),yv[3]*(yv[0]+yv[2]),yv[2]*(yv[1]+yv[3]),yv[3]*(yv[1]+yv[2])])
Dm=np.array([2*Phi(yy) for yy in y]); K=sl.null_space(Dm.T)
print("sv D",np.linalg.svd(Dm,compute_uv=False))
lam=K[:,0]; alpha=0.37
Lam=sum(lam[j]*np.outer(r[j],r[j]) for j in range(5)); Bc=alpha*np.outer(u,u)-2*Q@P@Lam
def analytic_jac(P,g):
    Q=np.linalg.inv(g); Jm=np.zeros((6,20))
    for j in range(5):
        yj=Q@P@r[j]
        Jm[j,:16]=(2*np.outer(yj,r[j])).reshape(16)
        for k in range(4):
            e=np.zeros(4); e[k]=1; Jm[j,16+k]=-yj@Hmat(e)@yj
    Jm[5,:16]=np.outer(u,u).reshape(16)
    return Jm
Ja=analytic_jac(P,g)
print("analytic vs fd jac:",np.abs(Ja-jac(z0)).max())
def project(z):
    for it in range(100):
        c=cons(z)
        if np.abs(c).max()<1e-15: break
        Jm=analytic_jac(z[:16].reshape(4,4),gmat(z[16:])); z=z-np.linalg.lstsq(Jm,c,rcond=None)[0]
    return z
def Lc(z): return np.sum(Bc*z[:16].reshape(4,4))
for trial in range(3):
    W=rng.normal(size=(4,4)); Gd=S.T@Lam.T; W=W-np.sum(W*Gd)/np.sum(Gd*Gd)*Gd
    rhs=np.array([-2*r[j]@S@W@r[j] for j in range(5)])
    hv=np.linalg.lstsq(Dm,rhs,rcond=None)[0]; H=Hmat(hv)
    tt=-(u@(P@W+H@Q@P)@u); W=W+tt*np.eye(4); dP=P@W+H@Q@P
    tan=np.r_[dP.reshape(16),hv]; nrm=np.linalg.norm(tan); tan/=nrm; W/=nrm
    print("trial",trial,"|tan| before scaling",nrm,"kernel resid",np.abs(Ja@tan).max(), "grad L . tan", Bc.reshape(16)@tan[:16])
    qW=np.trace(S@W@Lam@W.T)
    for ts in [1e-2,3e-3,1e-3,3e-4]:
        zp=project(z0+ts*tan); zm=project(z0-ts*tan)
        d2=(Lc(zp)-2*Lc(z0)+Lc(zm))/ts**2; d1=(Lc(zp)-Lc(zm))/(2*ts)
        print("   ts",ts,"d1",d1,"d2 fd",d2,"2q(W)",2*qW)
