#!/usr/bin/env python3
"""Exercise falsifiable controls by changing one identity in memory at a time.
No original, verifier, manuscript, or source file is modified.
"""
from pathlib import Path
import json,sys
sys.dont_write_bytecode=True
p=Path(__file__).with_name('independent_verify.py');s=p.read_text()
cases={
 'input_binding':("'sources/SOURCE_READY.json':'1e18","'sources/SOURCE_READY.json':'2e18"),
 'primitive_CDF_weight':("check(D==1-F((p-1)*P,R),'eventual CDF identity')","check(D==1-F(p*P,R),'eventual CDF identity')"),
 'unclipped_ramp':('return max(F(0),min(F(1),2*t-1))','return 2*t-1'),
 'exceptional_normalization':('DD=F(D*R+included,R+e)','DD=F(D*R+included,R)'),
 'indicator_omits_theta':('indicator=F(ph[n],n)*sum','indicator=sum'),
 'quadratic_norm_is_p':("rem==[1 if k==n//2 else p]","rem==[p]"),
 'moving_endpoint_excluded':("check(D==1,'moving endpoint equals one')","check(D==0,'moving endpoint equals one')"),
}
out=[]
for name,(old,new) in cases.items():
 if s.count(old)!=1:raise RuntimeError('mutation location not unique: '+name)
 env={'__file__':str(p),'__name__':'diagnostic_mutation'}
 exec(compile(s.replace(old,new),str(p),'exec'),env)
 try:env['main']()
 except RuntimeError as err:out.append({'mutation':name,'status':'REJECTED','failing_control':str(err)})
 else:raise RuntimeError('invalid identity was accepted: '+name)
print(json.dumps({'status':'PASS','scope':'Seven deliberately false identities rejected; no source writes.','cases':out},indent=2))
