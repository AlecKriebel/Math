import numpy as np, scipy.linalg as sl
rng=np.random.default_rng(7)
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]]); sz=np.diag([1.,-1.]).astype(complex); I2=np.eye(2,dtype=complex)
paulis=[I2,sx,sy,sz]
J=np.diag([1.,-1,-1,-1])
def coords(Xm): return np.array([np.real(np.trace(Xm@p))/2 for p in paulis])
def op(x): return sum(x[i]*paulis[i] for i in range(4))
def randunit():
    v=rng.normal(size=3); return v/np.linalg.norm(v)
def residual_party():
    n=randunit()
    E1=(I2+op(np.r_[0,n]))/2; E2=I2-E1
    # random rank-one ternary POVM: weights w_i, unit vectors with sum w_i n_i =0, sum w_i=2
    while True:
        v=[randunit() for _ in range(3)]
        A=np.array(v).T  # 3x3
        # solve A w = 0 with w>0: null vector exists only if coplanar; make coplanar
        v[2]=-(rng.uniform(.3,1)*v[0]+rng.uniform(.3,1)*v[1]); v[2]/=np.linalg.norm(v[2])
        A=np.array(v).T
        u_,s_,vt=np.linalg.svd(A); w=vt[-1]
        if np.all(w>0) or np.all(w<0):
            w=np.abs(w); w=2*w/w.sum(); break
    Es=[w[i]*(I2+op(np.r_[0,v[i]]))/2 for i in range(3)]
    return [E1,E2]+Es
r=[np.eye(4)[i] for i in range(4)]+[np.array([1.,1,-1,-1])]
u=np.array([1.,1,0,0])
EA=residual_party(); EB=residual_party()
assert np.allclose(EA[0]+EA[1],I2) and np.allclose(sum(EA[2:]),I2)
FA=np.array([coords(E) for E in EA[:4]]).T; FB=np.array([coords(E) for E in EB[:4]]).T
g=FA.T@J@FA; h=FB.T@J@FB
print("g=\n",np.round(g,4)); a,b,c,d,e=g[0,2],g[0,3],g[1,2],g[1,3],g[2,3]
print("normal form: g12=",g[0,1]," e - (a+b+c+d-1/2) =",e-(a+b+c+d-.5), "sig eig",np.linalg.eigvalsh(g))
print("ineq:",a,b,c,d,e,a+b,c+d,a+c,b+d)
Xi=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)); Xi/=np.sqrt(np.trace(Xi.conj().T@Xi).real)
psi=Xi.reshape(4)
def prob(E,N): return np.real(psi.conj()@np.kron(E,N)@psi)
P=np.array([[prob(EA[i],EB[j]) for j in range(4)] for i in range(4)])
full=np.array([[prob(EA[i],EB[j]) for j in range(5)] for i in range(5)])
R5=np.array(r).T
print("table = r_i^T P r_j:",np.allclose(full,R5.T@P@R5))
L=np.array([coords(Xi@p.T@Xi.conj().T) for p in paulis]).T
print("P=2 EA^T L EB:",np.allclose(P,2*FA.T@L@FB),"L^TJL=|det|^2J:",np.allclose(L.T@J@L,abs(np.linalg.det(Xi))**2*J))
Q=np.linalg.inv(g)
print("P^T Q P = 4|det|^2 h:",np.allclose(P.T@Q@P,4*abs(np.linalg.det(Xi))**2*h))
F=[ (P@rj)@Q@(P@rj) for rj in r]; print("incidences:",np.round(F,12), "uPu",u@P@u)
S=P.T@Q@P
print("r_j S u >0:",[rj@S@u for rj in r])
# dF and D2F check by finite differences
def Hmat(v):
    da,db,dc,dd=v; s=da+db+dc+dd
    return np.array([[0,0,da,db],[0,0,dc,dd],[da,dc,0,s],[db,dd,s,0.]])
def Fj(P_,g_,j): 
    x=P_@r[j]; return x@np.linalg.solve(g_,x)
Wm=rng.normal(size=(4,4)); hv=rng.normal(size=4); H=Hmat(hv)
dP=P@Wm+H@Q@P
y=[Q@P@rj for rj in r]
def Phi(yv): return np.array([yv[2]*(yv[0]+yv[3]),yv[3]*(yv[0]+yv[2]),yv[2]*(yv[1]+yv[3]),yv[3]*(yv[1]+yv[2])])
t=1e-4
for j in range(5):
    fp=Fj(P+t*dP,g+t*H,j); fm=Fj(P-t*dP,g-t*H,j); f0=Fj(P,g,j)
    d1=(fp-fm)/(2*t); d2=(fp-2*f0+fm)/t**2
    d1f=2*r[j]@S@Wm@r[j]+y[j]@H@y[j]
    d2f=2*(P@Wm@r[j])@Q@(P@Wm@r[j])
    print(j+1,"dF fd/formula",d1,d1f," D2F fd/formula",d2,d2f," yHy vs 2 hv.Phi:",y[j]@H@y[j],2*hv@Phi(y[j]))
print("y_j g-null:",[yy@g@yy for yy in y])
# inertia of q(W)=Tr(S W Lam W^T) with random positive lambda
lam=rng.uniform(.5,2,5); Lam=sum(lam[j]*np.outer(r[j],r[j]) for j in range(5))
Qf=np.zeros((16,16))
basis=[]
for i in range(16):
    Wb=np.zeros(16); Wb[i]=1; basis.append(Wb.reshape(4,4))
for i in range(16):
    for k in range(16):
        Qf[i,k]=0.5*(np.trace(S@basis[i]@Lam@basis[k].T)+np.trace(S@basis[k]@Lam@basis[i].T))
ev=np.linalg.eigvalsh(Qf); print("inertia:",(ev>1e-9).sum(),(ev<-1e-9).sum())
# rank of D at this random point
Dm=np.array([2*Phi(yy) for yy in y]); print("rank D:",np.linalg.matrix_rank(Dm), "sing vals",np.linalg.svd(Dm,compute_uv=False))
# sign claim: y_j future (u^T g y_j = u^T P r_j)
print("u g y_j:",[u@g@yy for yy in y],"marg",[u@P@rj for rj in r])
