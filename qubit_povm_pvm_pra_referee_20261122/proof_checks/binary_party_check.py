import numpy as np, itertools, scipy.linalg as sl
from scipy.optimize import linprog
rng=np.random.default_rng(5)
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]]); sz=np.diag([1.,-1.]).astype(complex); I2=np.eye(2,dtype=complex)
def randunit():
    v=rng.normal(size=3); return v/np.linalg.norm(v)
def dot(v): return v[0]*sx+v[1]*sy+v[2]*sz
def rand_povm(n):
    A=[rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)) for _ in range(n)]
    G=[a.conj().T@a for a in A]; S=sum(G); Si=np.linalg.inv(sl.sqrtm(S))
    return [Si@g@Si for g in G]
def run(nout):
    X=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)); rho=X@X.conj().T; rho/=np.trace(rho).real
    b=[randunit(),randunit()]; B=[dot(b[0]),dot(b[1])]
    M=[rand_povm(nout),rand_povm(nout)]
    def steer(Mm):
        T=(np.kron(Mm,I2)@rho).reshape(2,2,2,2); return np.einsum('ijik->jk',T)
    def PhiB(s): return np.array([np.trace(s).real,np.trace(s@B[0]).real,np.trace(s@B[1]).real])
    basis=[I2,B[0],B[1]]
    Gm=np.array([PhiB(x) for x in basis]).T     # PhiB of basis elements as columns
    def lift(v):
        cfs=np.linalg.solve(Gm,v); return sum(c*x for c,x in zip(cfs,basis))
    rays=[[],[]]   # (operator, label)
    target=np.zeros((2,nout,3))
    for x in range(2):
        for a in range(nout):
            v=PhiB(steer(M[x][a])); target[x,a]=v
            Lv=lift(v); w,U=np.linalg.eigh(Lv)
            assert w.min()>-1e-10
            for k in range(2):
                rays[x].append((w[k]*np.outer(U[:,k],U[:,k].conj()),a))
    # candidate circuits
    cols=[]; info=[]
    n0=len(rays[0]); n1=len(rays[1])
    for i,ip in itertools.combinations(range(n0),2):
        for j,jp in itertools.combinations(range(n1),2):
            vecs=np.array([PhiB(rays[0][i][0]),PhiB(rays[0][ip][0]),-PhiB(rays[1][j][0]),-PhiB(rays[1][jp][0])]).T
            ns=sl.null_space(vecs)
            if ns.shape[1]!=1: continue
            c=ns[:,0]
            if np.all(c>1e-9) or np.all(c<-1e-9):
                c=np.abs(c); col=np.zeros(n0+n1); col[i]=c[0]; col[ip]=c[1]; col[n0+j]=c[2]; col[n0+jp]=c[3]
                cols.append(col); info.append((i,ip,j,jp,c))
    Aeq=np.array(cols).T; beq=np.ones(n0+n1)
    res=linprog(np.zeros(len(cols)),A_eq=Aeq,b_eq=beq,bounds=(0,None),method='highs')
    if not res.success: return ("LP infeasible",len(cols))
    # build the mixture and verify behavior
    def prob(rho_,Ma,Nb): return np.trace(rho_@np.kron(Ma,Nb)).real
    Nb=[[(I2+B[y])/2,(I2-B[y])/2] for y in range(2)]
    p_orig=np.array([[[[prob(rho,M[x][a],Nb[y][bb]) for bb in range(2)] for a in range(nout)] for y in range(2)] for x in range(2)])
    p_mix=np.zeros_like(p_orig); wsum=0
    for wgt,(i,ip,j,jp,c) in zip(res.x,info):
        if wgt<1e-13: continue
        R=[wgt*c[0]*rays[0][i][0],wgt*c[1]*rays[0][ip][0]]; Sx=[wgt*c[2]*rays[1][j][0],wgt*c[3]*rays[1][jp][0]]
        Om=R[0]+R[1]; assert np.allclose(Om,Sx[0]+Sx[1],atol=1e-9)
        Omi=np.linalg.inv(sl.sqrtm(Om)); tr=np.trace(Om).real; wsum+=tr
        psi=(np.kron(I2,sl.sqrtm(Om/tr))@np.array([1,0,0,1.])); rb=np.outer(psi,psi.conj())
        P0=[(Omi@r_@Omi).T for r_ in R]; P1=[(Omi@s_@Omi).T for s_ in Sx]
        for Pp in P0+P1: assert np.allclose(Pp@Pp,Pp,atol=1e-7) and abs(np.trace(Pp).real-1)<1e-7
        labs=[[rays[0][i][1],rays[0][ip][1]],[rays[1][j][1],rays[1][jp][1]]]
        for x,PP in enumerate([P0,P1]):
            for k in range(2):
                for y in range(2):
                    for bb in range(2):
                        p_mix[x,y,labs[x][k],bb]+=tr*prob(rb,PP[k],Nb[y][bb])
    return ("ok",len(cols),"weights sum",round(wsum,10),"max err",np.abs(p_mix-p_orig).max())
for nout in [2,3,4,5]:
    for t in range(3): print(nout,run(nout))
