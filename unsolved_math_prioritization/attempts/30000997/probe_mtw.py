"""Numerical diagnostics only: not a proof or certification of off-cut admissibility."""
import numpy as np, json, math
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar
A=.1

def f(x):
 s=np.sin(x); c=np.cos(x); return c*(1+A*c*c*s**4)
def fp(x):
 s=np.sin(x); c=np.cos(x); return -s+A*(-3*c*c*s**5+4*c**4*s**3)
def curv(x):
 z=np.sin(x)**2; return (1+A*(-49*z**3+55*z*z-12*z))/(1+A*(z*z-z**3))
def hessian(x0,v,tol=2e-10):
 v=np.asarray(v); r2=v@v; b=f(x0)*v[1]
 if r2<1e-20:return np.eye(2),{'safe':True,'S':1,'max_x':abs(x0)}
 def ode(t,y):
  x,xd,C,Cd,S,Sd=y; V=r2*curv(x)
  return [xd,b*b*fp(x)/f(x)**3,Cd,-V*C,Sd,-V*S]
 sol=solve_ivp(ode,[0,1],[x0,v[0],1,0,0,1],rtol=tol,atol=tol*.03,max_step=.08)
 C,S=sol.y[2,-1],sol.y[4,-1]
 H=C/S; P=np.eye(2)-np.outer(v,v)/r2
 return np.eye(2)+(H-1)*P,{'safe':bool(sol.success and S>0 and np.max(np.abs(sol.y[0]))<1.569),'S':float(S),'max_x':float(np.max(np.abs(sol.y[0])))}
def tensor(x0,v,h=.002,tol=2e-10):
 e1=np.array([1.,0]); e2=np.array([0.,1.]); matrices={}; infos=[]
 for i,j in [(0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
  matrices[i,j],info=hessian(x0,v+h*(i*e1+j*e2),tol);infos.append(info)
 D11=(matrices[1,0]-2*matrices[0,0]+matrices[-1,0])/h**2
 D22=(matrices[0,1]-2*matrices[0,0]+matrices[0,-1])/h**2
 D12=(matrices[1,1]-matrices[1,-1]-matrices[-1,1]+matrices[-1,-1])/(4*h*h)
 def mtw(theta):
  u=np.array([np.cos(theta),np.sin(theta)]);w=np.array([-u[1],u[0]])
  return float(-u@(D11*w[0]**2+2*D12*w[0]*w[1]+D22*w[1]**2)@u)
 ts=np.linspace(0,np.pi,129);ys=np.array([mtw(t) for t in ts]);ii=np.argmin(ys); t=ts[ii]
 opt=minimize_scalar(mtw,bounds=(t-np.pi/128,t+np.pi/128),method='bounded')
 return {'x0':float(x0),'v':list(map(float,v)),'theta':float(opt.x),'mtw':float(opt.fun),'h':h,'safe_no_conj_poles':all(i['safe'] for i in infos),'minS':min(i['S'] for i in infos)}
if __name__=='__main__':
 best=[]
 for x0 in [0,.25,.5,.75,1,1.25]:
  for r in [.3,.7,1.1,1.5,1.9,2.3,2.7,3.0]:
   for ph in np.linspace(.07,np.pi-.07,15):
    try:
     d=tensor(x0,r*np.array([np.cos(ph),np.sin(ph)]))
     if d['safe_no_conj_poles']:
      best.append(d)
      if d['mtw']<-.01: print(json.dumps(d),flush=True)
    except Exception as e: pass
  print('done x',x0,'best',min((b['mtw'] for b in best),default=0),flush=True)
 best.sort(key=lambda b:b['mtw']);json.dump({'a':A,'disclaimer':'numerical only; minimizing/cut-locus not certified','lowest':best[:30]},open('degenerate_mtw_30000997/NUMERICAL_PROBE.json','w'),indent=2)
