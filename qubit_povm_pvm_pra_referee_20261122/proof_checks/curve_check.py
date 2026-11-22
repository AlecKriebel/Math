import numpy as np, scipy.linalg as sl
rng=np.random.default_rng(3)
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]]); sz=np.diag([1.,-1.]).astype(complex); I2=np.eye(2,dtype=complex)
paulis=[I2,sx,sy,sz]; J=np.diag([1.,-1,-1,-1])
def coords(Xm): return np.array([np.real(np.trace(Xm@p))/2 for p in paulis])
def op(x): return sum(x[i]*paulis[i] for i in range(4))
def randunit():
    v=rng.normal(size=3); return v/np.linalg.norm(v)
def residual_party():
    n=randunit(); E1=(I2+op(np.r_[0,n]))/2; E2=I2-E1
    v=[randunit(),randunit()]; v.append(-(rng.uniform(.3,1)*v[0]+rng.uniform(.3,1)*v[1])); v[2]/=np.linalg.norm(v[2])
    w=np.linalg.svd(np.array(v).T)[2][-1]; w=np.abs(w); w=2*w/w.sum()
    return [E1,E2]+[w[i]*(I2+op(np.r_[0,v[i]]))/2 for i in range(3)]
r=[np.eye(4)[i] for i in range(4)]+[np.array([1.,1,-1,-1])]; u=np.array([1.,1,0,0]); R5=np.array(r).T
EA=residual_party(); EB=residual_party()
FA=np.array([coords(E) for E in EA[:4]]).T
g0=FA.T@J@FA
Xi=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)); Xi/=np.sqrt(np.trace(Xi.conj().T@Xi).real); psi=Xi.reshape(4)
P0=np.array([[np.real(psi.conj()@np.kron(EA[i],EB[j])@psi) for j in range(4)] for i in range(4)])
def gmat(v):
    a,b,c,d=v; e=a+b+c+d-.5
    return np.array([[0,.5,a,b],[.5,0,c,d],[a,c,0,e],[b,d,e,0.]])
def Hmat(v):
    da,db,dc,dd=v; s=da+db+dc+dd
    return np.array([[0,0,da,db],[0,0,dc,dd],[da,dc,0,s],[db,dd,s,0.]])
v0=np.array([g0[0,2],g0[0,3],g0[1,2],g0[1,3]])
def cons(z):
    P=z[:16].reshape(4,4); g=gmat(z[16:]); 
    return np.array([(P@rj)@np.linalg.solve(g,P@rj) for rj in r]+[u@P@u-1])
def jac(z,h=1e-6):
    Jm=np.zeros((6,20))
    for i in range(20):
        e=np.zeros(20); e[i]=h; Jm[:,i]=(cons(z+e)-cons(z-e))/(2*h)
    return Jm
z0=np.r_[P0.reshape(16),v0]
print("cons at ref:",np.abs(cons(z0)).max(), "rank Jac",np.linalg.matrix_rank(jac(z0)))
def project(z):
    for it in range(50):
        c=cons(z)
        if np.abs(c).max()<1e-14: break
        Jm=jac(z); z=z-np.linalg.lstsq(Jm,c,rcond=None)[0]
    return z
# ---- reconstruction test at a nearby constraint point
z1=project(z0+1e-2*rng.normal(size=20)); P=z1[:16].reshape(4,4); g=gmat(z1[16:])
print("cons at new:",np.abs(cons(z1)).max(), "dist",np.linalg.norm(z1-z0))
# frame E_A with E^T J E = g and E u = e0
w,V=np.linalg.eigh(g)  # one positive
# construct via Gram-Schmidt: u, then 3 vectors in u-perp
basis=[u]
cand=[np.eye(4)[i] for i in range(4)]
ortho=[]
for c_ in cand:
    v=c_-(c_@g@u)*u
    for o in ortho: v=v-(v@g@o)/(o@g@o)*o
    n=-(v@g@v)
    if n>1e-9: ortho.append(v/np.sqrt(n))
    if len(ortho)==3: break
B=np.column_stack([u]+ortho)   # B^T g B = J
print("B^T g B = J:",np.allclose(B.T@g@B,J))
E=np.linalg.inv(B)             # E^T J E = g, E u = e0
print("E^T J E = g:",np.allclose(E.T@J@E,g),"E u:",np.round(E@u,12))
Aeff=[op(E@rj) for rj in r]
print("Alice effects eig min:",[np.linalg.eigvalsh(a).min().round(12) for a in Aeff],"ranks",[np.linalg.matrix_rank(a,tol=1e-9) for a in Aeff], "sums",np.allclose(Aeff[0]+Aeff[1],I2),np.allclose(sum(Aeff[2:]),I2))
Sj=[op(0.5*np.linalg.solve(E.T,P@rj)) for rj in r]
print("steered eig min:",[np.linalg.eigvalsh(s).min().round(12) for s in Sj],"ranks",[np.linalg.matrix_rank(s,tol=1e-9) for s in Sj])
rhoA=Sj[0]+Sj[1]; print("rhoA consistent:",np.allclose(rhoA,sum(Sj[2:])),"trace",np.trace(rhoA).real,"eigs",np.linalg.eigvalsh(rhoA))
Xi2=sl.sqrtm(rhoA); Xi2i=np.linalg.inv(Xi2)
Nj=[(Xi2i@s@Xi2i.conj().T).T for s in Sj]
print("Bob eig min:",[np.linalg.eigvalsh(n).min().round(12) for n in Nj],"sums",np.allclose(Nj[0]+Nj[1],I2),np.allclose(sum(Nj[2:]),I2))
psi2=Xi2.reshape(4)
tab=np.array([[np.real(psi2.conj()@np.kron(Aeff[i],Nj[j])@psi2) for j in range(5)] for i in range(5)])
print("reconstructed table matches r^T P r:",np.abs(tab-R5.T@P@R5).max(), " state norm",np.linalg.norm(psi2))

# ---- second-derivative identity test at a stationary point of a synthetic objective
P=P0; g=g0; Q=np.linalg.inv(g); S=P.T@Q@P
y=[Q@P@rj for rj in r]
def Phi(yv): return np.array([yv[2]*(yv[0]+yv[3]),yv[3]*(yv[0]+yv[2]),yv[2]*(yv[1]+yv[3]),yv[3]*(yv[1]+yv[2])])
Dm=np.array([2*Phi(yy) for yy in y])       # 5x4
K=sl.null_space(Dm.T)                      # ker D^T
print("rank D",np.linalg.matrix_rank(Dm),"dim K",K.shape[1])
lam=K[:,0]; alpha=0.37
Lam=sum(lam[j]*np.outer(r[j],r[j]) for j in range(5))
Bc=alpha*np.outer(u,u)-2*Q@P@Lam
# tangent: choose W compatible: Tr(S W Lam)=0, then solve H, normalize
W=rng.normal(size=(4,4)); 
# enforce compatibility by subtracting component along gradient S^T Lam^T -> Tr(S W Lam)=<W, S^T Lam^T>
Gd=S.T@Lam.T; W=W-np.sum(W*Gd)/np.sum(Gd*Gd)*Gd
rhs=np.array([-2*r[j]@S@W@r[j] for j in range(5)])
hv,res,rk,sv=np.linalg.lstsq(Dm,rhs,rcond=None); print("solve residual",np.abs(Dm@hv-rhs).max())
H=Hmat(hv)
tt=-(u@(P@W+H@Q@P)@u); W=W+tt*np.eye(4)
dP=P@W+H@Q@P
tan=np.r_[dP.reshape(16),hv]
print("tangent in kernel:",np.abs(jac(z0)@tan).max())
def Lc(z): return np.sum(Bc*z[:16].reshape(4,4))
ts=3e-3
zp=project(z0+ts*tan); zm=project(z0-ts*tan)
# make sure projected curve has tangent tan: use minimal-norm projection, so displacement = ts*tan + O(ts^2)
d1=(Lc(zp)-Lc(zm))/(2*ts); d2=(Lc(zp)-2*Lc(z0)+Lc(zm))/ts**2
qW=np.trace(S@W@Lam@W.T)
print("first derivative ~0:",d1,"  second derivative fd:",d2," 2q(W):",2*qW)
