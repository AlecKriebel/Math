"""Independent reflection checks; finite high-precision diagnostics only."""
import json
import mpmath as mp
from reflection_geometry import periodic_lambda,sample
results=[]
for aa in ['1.0001','2','10']:
 for N,tau in [(3,1),(5,2),(7,3)]:
  a=mp.mpf(aa);b=mp.mpf(1);lam=periodic_lambda(a,b,N,tau)
  phases=[sample(a,b,N,tau,mp.mpf(r),lam) for r in ['0','0.2']]
  for z in phases:
   assert z['primitive'] and mp.mpf(z['beta_squared'])>0
   assert min(mp.mpf(v) for v in z['signed_areas_Aplus_Aprimeplus_Aminus_Aprimeminus'])>0
   assert mp.mpf(z['checks']['min_outer_det'])>0
   for name,res in z['checks'].items():
    if name!='min_outer_det':assert mp.mpf(res)<mp.mpf('1e-65'),(aa,N,tau,name,res)
  ratios=[mp.mpf(z['ratios'][k]) for z in phases for k in ['prime_to_original_plus','prime_to_original_minus']]
  assert max(ratios)-min(ratios)<mp.mpf('1e-65')*(1+max(ratios))
  results.extend(phases)
print(json.dumps({'status':'PASS','precision_dps':mp.mp.dps,'samples':len(results),'families':len(results)//2,'max_residuals':{k:mp.nstr(max(mp.mpf(z['checks'][k]) for z in results),12) for k in results[0]['checks'] if k!='min_outer_det'},'scope':'Finite NONINTERVAL reflection/projection checks independent of canonical Jacobi coordinates; not a universal proof or certified error bound.'},indent=2))
