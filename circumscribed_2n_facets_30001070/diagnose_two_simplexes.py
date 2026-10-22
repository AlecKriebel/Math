"""Bounded floating-point probe of a nonsymmetric centered ten-point family in R5."""
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
import json
n=5;J=np.ones((n,n))/n
j,k=np.indices((n,n));d=j-k

def config(p):
 t1,t2,z=p
 Q=(1+2*np.cos(2*np.pi*d/n+t1)+2*np.cos(4*np.pi*d/n+t2))/n
 a=np.sqrt(n*(1-z)/(n-1));b=np.sqrt(n*z);H=a*np.eye(n)+(b-a)*J
 return np.vstack([np.eye(n),-Q])@H

def objective(p):
 U=config(p)
 return -float(np.min(-ConvexHull(U).equations[:,-1]))

best=(1e10,None);grid=[];counts=[];best_non_cross=None
for t1 in np.linspace(0,np.pi,5):
 for t2 in np.linspace(0,np.pi,5):
  for z in [1/5,1/4,3/11,1/3,1/2]:
   p=[float(t1),float(t2),float(z)];v=objective(p);grid.append((v,p))
   count=len(ConvexHull(config(p)).simplices);counts.append(count)
   if count>32 and (best_non_cross is None or v<best_non_cross[0]):best_non_cross=(v,p,count)
   if v<best[0]:best=(v,p)
starts=[grid[i][1] for i in np.linspace(0,len(grid)-1,9,dtype=int)]
opts=[]
for p in starts:
 r=minimize(objective,p,method='Powell',bounds=[(-np.pi,np.pi),(-np.pi,np.pi),(.05,.85)],options={'maxfev':400,'maxiter':25,'xtol':1e-6,'ftol':1e-7})
 opts.append({'initial':p,'final':r.x.tolist(),'rho':float(-r.fun),'evaluations':r.nfev,'optimizer_success':bool(r.success)})
 if r.fun<best[0]:best=(float(r.fun),r.x.tolist())
U=config(best[1]);H=ConvexHull(U)
print(json.dumps({'diagnostic_only':True,'dimension':n,'point_count':2*n,'grid_evaluations':len(grid),'maximum_triangulated_facet_count_in_grid':max(counts),'best_more_than32_triangulated_facets':best_non_cross,'local_search_runs':opts,'total_local_search_evaluations':sum(x['evaluations'] for x in opts),'best_parameters':best[1],'best_centered_inradius':-best[0],'conjectured_maximum':float(1/np.sqrt(n)),'best_unit_norm_error':float(max(abs(np.sum(U*U,axis=1)-1))),'best_center_error':float(np.linalg.norm(U.sum(axis=0))),'best_facet_count':len(H.simplices),'certified_counterexample':False},indent=2))
