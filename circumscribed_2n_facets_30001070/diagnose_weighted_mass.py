"""Small floating-point diagnostics; these are neither certificates nor an exhaustive search."""
import numpy as np
from scipy.optimize import minimize
from scipy.spatial import ConvexHull
import json
rng=np.random.default_rng(1070)
out=[]
for n in [3,4,5,6]:
 best=None;allactive=0;attempts=30
 for trial in range(attempts):
  V=rng.normal(size=(2*n,n)); V/=np.linalg.norm(V,axis=1)[:,None]
  Z=np.column_stack([V,np.ones(2*n)])
  def f(p):
   M=Z.T@(p[:,None]*Z);sgn,ld=np.linalg.slogdet(M)
   if sgn<=0:return 1e9,np.zeros(2*n)
   inv=np.linalg.inv(M)
   return -ld,-np.einsum('ij,jk,ik->i',Z,inv,Z)
  r=minimize(f,np.full(2*n,1/(2*n)),jac=True,method='SLSQP',bounds=[(1e-10,1)]*(2*n),constraints={'type':'eq','fun':lambda p:p.sum()-1,'jac':lambda p:np.ones(2*n)},options={'ftol':1e-11,'maxiter':300})
  if not r.success or min(r.x)<1e-6:continue
  p=r.x; ctr=p@V;W=V-ctr;C=W.T@(p[:,None]*W);eig,E=np.linalg.eigh(C);U=W@E@np.diag(1/np.sqrt(n*eig))@E.T
  normerr=max(abs(np.sum(U*U,axis=1)-1))
  if normerr>1e-5:continue
  allactive+=1;facets=ConvexHull(U).simplices
  mass=max(p[F].sum() for F in facets)
  rho=min(-ConvexHull(U).equations[:,-1])
  d={'trial':trial,'max_facet_probability_mass':float(mass),'centered_inradius':float(rho),'target_inradius':float(1/np.sqrt(n)),'unit_norm_error':float(normerr),'p':p.tolist(),'U':U.tolist()}
  if best is None or mass<best['max_facet_probability_mass']:best=d
 out.append({'n':n,'attempts':attempts,'accepted_all_contact_cases':allactive,'smallest_observed_max_facet_probability_mass':None if best is None else best['max_facet_probability_mass'],'best':best})
print(json.dumps({'diagnostic_only':True,'random_seed':1070,'results':out},indent=2))
