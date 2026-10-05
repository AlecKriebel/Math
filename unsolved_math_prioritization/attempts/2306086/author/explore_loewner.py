"""Non-certified exploratory lower-bound search; never an upper bound or proof."""
import json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from scipy.optimize import differential_evolution
z,u=s.symbols('z u')
p=(1-z*z)/(1-2*u*z+z*z)
v=-z*p
vf=s.lambdify((z,u),v,'numpy');v1=s.lambdify((z,u),s.diff(v,z),'numpy');v2=s.lambdify((z,u),s.diff(v,z,2),'numpy')
L=1/z+(u-1)/(z-1)-(u+1)/(z+1)
P=s.lambdify((z,u),s.factor(L+s.diff(L,z)/L),'numpy')
def value(r,params,rtol=1e-9):
 controls=params[:2]; dur=params[2:4]; tail=params[4]
 jet=np.array([1j*r,1+0j,0j])
 for a,t in zip(controls,dur):
  def rhs(t,Y):
   w,d,e=Y;return [vf(w,a),v1(w,a)*d,v2(w,a)*d*d+v1(w,a)*e]
  sol=solve_ivp(rhs,(0,t),jet,method='DOP853',rtol=rtol,atol=rtol*1e-2)
  if not sol.success:raise RuntimeError(sol.message)
  jet=sol.y[:,-1]
 w,d,e=jet
 ps=P(w,tail)*d+e/d
 return abs((1-r*r)*ps+2j*r)
if __name__=='__main__':
 records=[]
 for r in [.3,.45,.5,.7]:
  opt=differential_evolution(lambda a:-value(r,a),[(-1,1)]*2+[(0,2)]*2+[(-1,1)],seed=687,maxiter=35,popsize=6,tol=1e-7,polish=True)
  a=opt.x.tolist(); rec={'r':r,'parameters':a,'value':value(r,a,1e-12),'elementary_lower_bound':max(4*np.sqrt(1-3*r*r/(1+r*r)**2),8*r/(1+r*r)),'certified':False};records.append(rec);print(json.dumps(rec),flush=True)
 Path(__file__).with_name('LOEWNER_EXPLORATION.json').write_text(json.dumps({'status':'non-certified exploratory evidence only','records':records},indent=2)+'\n')
