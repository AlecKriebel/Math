"""One independent non-proof illustration replay using Gauss cosine projection.
Uses Radau instead of the archived BDF and differentiates the original model.
"""
from pathlib import Path
import json,datetime,hashlib
import numpy as np
from scipy.integrate import solve_ivp
import sympy as s
from independent_controls import model,profile
here=Path(__file__).resolve().parent
data=here.parents[1]/'sources/published-source/Exact_Diffusion_Design_Data_v1.0.11'
m=3; K=16; N=4*K+1; mu=.02; tf=13000.
x,f,A,B,c=model(m); r,D,ell=profile(m)
rf=np.array(r,dtype=float).ravel(); df=np.diag(np.array(D,dtype=float)); ef=np.array(ell,dtype=float).ravel(); cf=np.array(c,dtype=float).ravel()
forcing=-B(r,r)/4; aa=A.copy(); rr=forcing.copy(); aa[m,:]=c.T; rr[m]=0
w0=aa.inv()*rr; w2=(A-4*D).inv()*forcing
cubic=float((ell.T*(B(r,w0)+B(r,w2)/2))[0]/(ell.T*r)[0]); eta=float((ell.T*D*r)[0]/(ell.T*r)[0])
pred=np.sqrt(-eta*mu/cubic)
grid=(np.arange(N)+.5)*np.pi/N
E=np.cos(np.outer(np.arange(K+1),grid)); P=E*(2/N); P[0]/=2
fun=s.lambdify(tuple(x),f,'numpy')
jfs=[[s.lambdify(tuple(x),s.diff(f[ii],x[jj]),'numpy') for jj in range(m+1)] for ii in range(m+1)]
initial=np.zeros((m+1,K+1));initial[:,0]=1;initial[:,1]=.92*pred*rf
def rhs(t,state):
    C=state.reshape(m+1,K+1); X=C@E
    F=np.asarray(fun(*X),dtype=float).reshape(m+1,N)
    return (F@P.T-(1-mu)*df[:,None]*(np.arange(K+1)**2)[None,:]*C).ravel()
def jac(t,state):
    X=state.reshape(m+1,K+1)@E
    out=np.zeros(((m+1)*(K+1),(m+1)*(K+1)))
    for ii in range(m+1):
        for jj in range(m+1):
            values=np.broadcast_to(jfs[ii][jj](*X),(N,))
            block=(P*values[None,:])@E.T
            if ii==jj:block-=np.diag((1-mu)*df[ii]*np.arange(K+1)**2)
            out[ii*(K+1):(ii+1)*(K+1),jj*(K+1):(jj+1)*(K+1)]=block
    return out
direction=np.linspace(-.2,.2,initial.size)
fd=(rhs(0,initial.ravel()+1e-5*direction)-rhs(0,initial.ravel()-1e-5*direction))/(2e-5)
assert np.max(abs(fd-jac(0,initial.ravel())@direction))<1e-7
print('Independent quadrature Jacobian directional control passed',flush=True)
sol=solve_ivp(rhs,(0,tf),initial.ravel(),method='Radau',jac=jac,rtol=1e-10,atol=1e-12,t_eval=[0,tf])
assert sol.success
C=sol.y[:,-1].reshape(m+1,K+1)
amp=float(ef@C[:,1]/(ef@rf))
arch=json.loads((data/'simulations/parameters_m3_mu0p02_K16_base.json').read_text())
archprofile=np.genfromtxt(data/'simulations/profile_m3_mu0p02_K16_base.csv',delimiter=',',skip_header=1)
Xs=C@np.cos(np.outer(np.arange(K+1),archprofile[:,0]))
error=float(np.max(abs(Xs-archprofile[:,1:].T)))
mass=float(abs(cf@C[:,0]-cf@initial[:,0])); minimum=float(Xs.min())
assert abs(amp-arch['measured_amplitude'])<1e-7
assert error<1e-7 and mass<1e-10 and minimum>0
result={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Radau + exact-to-roundoff midpoint cosine quadrature, 65 quadrature nodes, 16 retained modes','m':m,'mu':mu,'tfinal':tf,'success':sol.success,'nfev':sol.nfev,'amplitude':amp,'archived_BDF_amplitude':arch['measured_amplitude'],'profile_max_abs_difference':error,'constant_mode_mass_drift':mass,'minimum_concentration':minimum,'final_modal_rhs_inf':float(np.max(abs(rhs(tf,sol.y[:,-1])))),'limitation':'Finite unvalidated numerical replay; not a proof of the infinite-dimensional theorem or a rigorous truncation bound.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(here/'independent-simulation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
