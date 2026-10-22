import numpy as np,sys,json
from scipy.integrate import solve_ivp
from scipy.optimize import root
sys.path.insert(0,'degenerate_mtw_30000997')
from probe_mtw import f,fp,tensor

def endpoint(x0,v):
 v=np.asarray(v);b=f(x0)*v[1]
 def ode(t,y):
  x,xd,lon=y
  return [xd,b*b*fp(x)/f(x)**3,b/f(x)**2]
 sol=solve_ivp(ode,[0,1],[x0,v[0],0],rtol=3e-11,atol=1e-12,max_step=.06)
 return sol.y[[0,2],-1]

def candidates(q):
 x0=q['x0'];v=np.array(q['v']);goal=endpoint(x0,v);print('target',x0,v,goal,flush=True);ans=[]
 def residual(v):
  try:
   e=endpoint(x0,v);return [e[0]-goal[0],(e[1]-goal[1]+np.pi)%(2*np.pi)-np.pi]
  except:return [10,10]
 for ph in np.linspace(-np.pi+.07,np.pi-.07,35):
  rr=root(residual,3*np.array([np.cos(ph),np.sin(ph)]),tol=1e-8,options={'maxfev':65})
  if rr.success and np.linalg.norm(residual(rr.x))<1e-7 and np.linalg.norm(rr.x)<3.5:
   if not any(np.linalg.norm(rr.x-a['v'])<1e-4 for a in ans):
    d={'v':list(rr.x),'length':float(np.linalg.norm(rr.x)),'residual':list(residual(rr.x))};ans.append(d);print('found',d,flush=True)
 ans.sort(key=lambda d:d['length'])
 return {'source_latitude':x0,'original_v':list(v),'original_length':float(np.linalg.norm(v)),'endpoint':list(goal),'candidate_geodesics':ans,'disclaimer':'shooting numerics, not certified minimizers'}
if __name__=='__main__':
 qs=json.load(open('degenerate_mtw_30000997/NUMERICAL_PROBE.json'))['lowest'][:2]
 out=[]
 for q in qs:out.append(candidates(q))
 json.dump(out,open('degenerate_mtw_30000997/MINIMIZER_PROBE.json','w'),indent=2)
