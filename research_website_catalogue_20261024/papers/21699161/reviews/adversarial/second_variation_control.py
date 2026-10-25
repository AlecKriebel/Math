"""Check the decisive Hessian mechanism against a reconstructed physical curve."""
from pathlib import Path
exec(Path('independent_controls.py').read_text().split("results={'timestamp_utc'")[0])
from scipy.optimize import linprog,root
from scipy.linalg import null_space,qr
Hs=[H(np.eye(4)[k]) for k in range(4)]
found=None
for trial in range(600):
    EA,A=local(); EB,B=local();Xi=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));Xi/=np.linalg.norm(Xi)
    if abs(np.linalg.det(Xi))<.1:continue
    P=np.array([[np.trace(A[i]@Xi@B[j].T@Xi.conj().T).real for j in range(4)] for i in range(4)])
    if np.linalg.cond(P)>500:continue
    g=EA.T@J@EA;Q=np.linalg.inv(g);yy=Q@P@r
    D=np.array([[yy[:,j]@h@yy[:,j] for h in Hs] for j in range(5)])
    if np.linalg.matrix_rank(D,tol=1e-8)<2:continue
    fit=linprog(np.zeros(5),A_eq=np.vstack([D.T,np.ones(5)]),b_eq=np.r_[np.zeros(4),1],bounds=[(.001,None)]*5,method='highs')
    if fit.success and np.linalg.norm(D.T@fit.x)<1e-9:found=(trial,P,g,Q,D,fit.x);break
if found is None:
    Path('second-variation-control.json').write_text(json.dumps({'status':'NO_POSITIVE_MULTIPLIER_FIXTURE_FOUND','trials':600})+'\n')
    raise SystemExit('No stationary positive-multiplier fixture found in bounded search')
trial,P,g,Q,D,lam=found;S=P.T@Q@P;Lambda=(r*lam)@r.T
K=null_space(D.T);compat=np.array([(S@((r*K[:,j])@r.T)).reshape(-1) for j in range(K.shape[1])])
Zspace=null_space(compat);quad=np.kron(S,Lambda);vals,vecs=np.linalg.eigh(Zspace.T@quad@Zspace)
assert vals[-1]>1e-8
W=(Zspace@vecs[:,-1]).reshape(4,4)
hcoef=np.linalg.lstsq(D,np.array([-2*r[:,j]@S@W@r[:,j] for j in range(5)]),rcond=None)[0];h=H(hcoef)
dP=P@W+h@Q@P; W-=float(u@dP@u)*np.eye(4);dP=P@W+h@Q@P
qval=float(np.trace(S@W@Lambda@W.T));assert qval>0
Bc=-2*Q@P@Lambda
Jac=np.zeros((6,20))
for j in range(5):
    Jac[j,:16]=(2*np.outer(yy[:,j],r[:,j])).reshape(-1);Jac[j,16:]=-D[j]
Jac[5,:16]=np.outer(u,u).reshape(-1)
tangent=np.r_[dP.reshape(-1),hcoef];assert np.max(abs(Jac@tangent))<1e-8
_,_,piv=qr(Jac,pivoting=True);dependent=piv[:6];free=piv[6:]
z0=np.r_[P.reshape(-1),[g[0,2],g[0,3],g[1,2],g[1,3]]]
def unpack(z):
    pp=z[:16].reshape(4,4); a,b,c,d=z[16:]; e=a+b+c+d-.5
    gg=np.array([[0,.5,a,b],[.5,0,c,d],[a,c,0,e],[b,d,e,0]])
    return pp,gg

def equations(z):
    pp,gg=unpack(z);qq=np.linalg.inv(gg)
    return np.r_[[r[:,j]@pp.T@qq@pp@r[:,j] for j in range(5)],u@pp@u-1]
base=float(np.sum(Bc*P));curves=[]
for step in [-.0002,.0002]:
    z=z0+step*tangent
    def residual(dep):
        zz=z.copy();zz[dependent]=dep;return equations(zz)
    sol=root(residual,z[dependent],tol=1e-11)
    z[dependent]=sol.x;pp,gg=unpack(z);err=np.max(abs(equations(z)))
    gain=float(np.sum(Bc*pp)-base);pred=qval*step*step
    # Reconstruct a Lorentz frame and its positive steered operators.
    # Diagonalization yields a frame, then a boost sends E u to time unit.
    eig,Ue=np.linalg.eigh(gg);order=np.r_[3,0,1,2]
    assert eig[3]>0 and max(eig[:3])<0
    E=np.diag(np.sqrt(abs(eig[order])))@Ue[:,order].T
    if (E@u)[0]<0:E[0]*=-1
    tim=E@u;v=tim[1:];boost=np.eye(4);boost[0,0]=tim[0];boost[0,1:]=-v;boost[1:,0]=-v;boost[1:,1:]+=np.outer(v,v)/(tim[0]+1)
    E=boost@E
    effects=[op(E@r[:,j]) for j in range(5)]
    steered=[op(np.linalg.solve(E.T,pp@r[:,j])/2) for j in range(5)];rho=steered[0]+steered[1]
    xx=np.asarray(sqrtm(rho),complex);xxinv=np.linalg.inv(xx);nb=[(xxinv@s@xxinv.conj().T).T for s in steered]
    born=np.array([[np.trace(effects[i]@xx@nb[j].T@xx.conj().T).real for j in range(4)] for i in range(4)])
    mineig=min(np.linalg.eigvalsh(n).min() for n in effects+nb)
    assert err<1e-10 and gain>0 and abs(gain/pred-1)<.03 and mineig>-1e-9
    assert np.max(abs(born-pp))<1e-10
    curves.append({'step':step,'constraint_residual':float(err),'Bell_gain':gain,'predicted_quadratic_gain':pred,'ratio':gain/pred,'minimum_effect_eigenvalue':float(mineig),'Born_reconstruction_error':float(np.max(abs(born-pp)))})
report={'status':'PASS','fixture_trial':trial,'metric_rank':int(np.linalg.matrix_rank(D)),'positive_multipliers':lam.tolist(),'q':qval,'curves':curves,'scope':'One numerically constructed stationary positive-multiplier fixture and two physical uphill curves; general dimension proof separately reviewed'}
Path('second-variation-control.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
