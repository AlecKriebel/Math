"""Bounded exploratory scan of agonist-only scalar turning points; not a proof."""
import numpy as np, random, json
from pathlib import Path
rng=random.Random(30003741)
frac=1/(1+np.exp(-np.linspace(-24,24,801)))
cases=[]
for N in (5,6,8,12,20,50):
 for i in range(40):
  v=10**rng.uniform(-8,0); b=10**rng.uniform(-8,1); h=10**rng.uniform(-1,2)
  t=h*frac;u=b+v+t
  ps=np.ones_like(t);ds=np.ones_like(t);pps=np.zeros_like(t);dds=np.zeros_like(t)
  oldd=np.zeros_like(t);olddd=np.zeros_like(t)
  for m in range(1,N+1):
   oldp=ps.copy();oldpp=pps.copy()
   pn=u*ps+v*oldd;ppn=ps+u*pps+v*olddd
   dn=ds+pn;ddn=dds+ppn
   oldd,olddd=ds,dds;ps,pps,ds,dds=pn,ppn,dn,ddn
  g=1/t+1/(h-t)+dds/ds-oldpp/oldp
  changes=int(np.sum(g[:-1]*g[1:]<0))
  cases.append({'N':N,'nu_over_phi':v,'b_over_phi':b,'gamma_ST_over_phi':h,'sampled_derivative_sign_changes':changes})
out={'status':'EXPLORATORY_ONLY','seed':30003741,'parameter_sets':len(cases),'sample_points_per_set':len(frac),'max_observed_derivative_sign_changes':max(c['sampled_derivative_sign_changes'] for c in cases),'cases_with_at_least_four_sampled_changes':[c for c in cases if c['sampled_derivative_sign_changes']>=4],'scope':'Numerical grid observations cannot exclude narrow features or prove a global three-root ceiling. Two-ligand models are not included.'}
Path(__file__).resolve().with_name('turning_scan.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
