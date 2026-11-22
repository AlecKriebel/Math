import numpy as np, itertools, sys, time
from scipy.optimize import minimize
I2=np.eye(2); X=np.array([[0,1],[1,0]],float); Z=np.diag([1.,-1.])
nA=3; nB=3
def party_ops(th, lab0, lab1, n):
    # returns array [x,a,2,2]
    M=np.zeros((2,n,2,2))
    M[0,lab0[0]]+=(I2+Z)/2; M[0,lab0[1]]+=(I2-Z)/2
    O=np.cos(th)*Z+np.sin(th)*X
    M[1,lab1[0]]+=(I2+O)/2; M[1,lab1[1]]+=(I2-O)/2
    return M
labsA=[(l0,l1) for l0 in itertools.product(range(nA),repeat=2) for l1 in itertools.product(range(nA),repeat=2)]
labsB=[(l0,l1) for l0 in itertools.product(range(nB),repeat=2) for l1 in itertools.product(range(nB),repeat=2)]
def pvm_bound(c, ngrid=13):
    ths=np.linspace(0,np.pi,ngrid)
    MA=np.array([[party_ops(t,l[0],l[1],nA) for t in ths] for l in labsA])  # [LA,T,x,a,2,2]
    MB=np.array([[party_ops(t,l[0],l[1],nB) for t in ths] for l in labsB])
    LA,T=MA.shape[:2]; LB=MB.shape[0]
    MAf=MA.reshape(LA*T,2,nA,2,2); MBf=MB.reshape(LB*T,2,nB,2,2)
    # contract c[a,b,x,y] with MB first: KB[k,x,a,2,2]=sum_{y,b} c[a,b,x,y] MB[k,y,b]
    KB=np.einsum('abxy,kybij->kxaij',c,MBf)
    best=-1e9; cands=[]
    for i in range(LA*T):
        ops=np.einsum('xapq,kxaij->kpiqj',MAf[i],KB).reshape(-1,4,4)
        ev=np.linalg.eigvalsh(ops)[:,-1]
        k=np.argmax(ev)
        cands.append((ev[k],i,k))
    cands.sort(reverse=True)
    # refine top candidates
    out=-1e9
    for (v,i,k) in cands[:40]:
        la,ta=divmod(i,T); lb,tb=divmod(k,T)
        def f(p):
            A=party_ops(p[0],labsA[la][0],labsA[la][1],nA); B=party_ops(p[1],labsB[lb][0],labsB[lb][1],nB)
            op=np.einsum('abxy,xapq,ybij->piqj',c,A,B).reshape(4,4)
            return -np.linalg.eigvalsh(op)[-1]
        r=minimize(f,[ths[ta],ths[tb]],method='Nelder-Mead',options={'xatol':1e-10,'fatol':1e-13})
        out=max(out,-r.fun)
    return out
def povm_from(params,n):
    A=params.reshape(n,2,2,2); A=A[...,0]+1j*A[...,1]
    G=np.einsum('aki,akj->aij',A.conj(),A)
    S=G.sum(0); w,v=np.linalg.eigh(S); Si=v@np.diag(w**-0.5)@v.conj().T
    return np.einsum('ij,ajk,kl->ail',Si,G,Si)
def povm_val(p,c):
    pA=p[:2*nA*8].reshape(2,-1); pB=p[2*nA*8:].reshape(2,-1)
    MA=np.array([povm_from(pA[x],nA) for x in range(2)]); MB=np.array([povm_from(pB[y],nB) for y in range(2)])
    op=np.einsum('abxy,xapq,ybij->piqj',c,MA,MB).reshape(4,4)
    op=(op+op.conj().T)/2
    return np.linalg.eigvalsh(op)[-1]
rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)
ntests=int(sys.argv[2]) if len(sys.argv)>2 else 4
for t in range(ntests):
    c=rng.normal(size=(nA,nB,2,2))
    t0=time.time(); pb=pvm_bound(c); t1=time.time()
    best=-1e9
    for rst in range(25):
        p0=rng.normal(size=2*nA*8+2*nB*8)
        r=minimize(lambda p:-povm_val(p,c),p0,method='BFGS',options={'gtol':1e-9,'maxiter':600})
        best=max(best,-r.fun)
    print(f"test {t}: PVM bound {pb:.8f}  POVM search {best:.8f}  diff {best-pb:+.2e}  (t {t1-t0:.0f}s,{time.time()-t1:.0f}s)",flush=True)
