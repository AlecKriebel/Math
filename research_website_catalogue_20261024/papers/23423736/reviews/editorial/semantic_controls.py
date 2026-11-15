#!/usr/bin/env python3
"""Small editorial wording-loss controls only, separate from default custody closure."""
from pathlib import Path
import json,copy
E=Path(__file__).resolve().parent
def require(c):
 text=' '.join(' '.join(c[k])if isinstance(c[k],list)else c[k]for k in ['abstract','result','why_it_works','limitations','background','ai_disclosure'])
 clauses=[('fullabstract',c['abstract']==json.loads((E/'public-sections.json').read_bytes())['abstract']),('quantifiers','For every field k, every α∈k and every β∈k with β²≠1'in text),('exactkernel','its kernel is exactly I'in text),('positivepullback','positive pullbacks'in text and'f⋆g=f⊗(σᵐ)⁎g'in text),('RZbroaderroute','Theorem 4.4'in text and'eventual stabilization'in text and'not the only route'in text),('char2boundary','fractions collapse to 1'in text and'are not transferred'in text),('priority','Historical priority remains unresolved'in text),('disclosure','without conventional external human peer review or formal proof-assistant certification'in text),('nofollowup',c['follow_up']is None)]
 return [n for n,ok in clauses if not ok]
def run():
 c=json.loads((E/'configs/publication.json').read_bytes())
 if require(c):raise RuntimeError('currentcopycontractfailure')
 controls=[]
 for name,key,old,new in [('loseentireabstract','abstract',c['abstract'],'An exact quotient.'),('dropallfieldcondition','result','For every field k, every α∈k and every β∈k with β²≠1','For selected generic parameters'),('loseexactkernel','result','its kernel is exactly I','its relations vanish'),('invertpullback','result','f⋆g=f⊗(σᵐ)⁎g','f⋆g=f⊗(σ⁻ᵐ)⁎g'),('loseRZbroaderroute','background','Their broader Theorem 4.4','Their other theorem'),('dropchar2boundary','limitations','fractions collapse to 1','fractions preserve all independent parameters'),('certifypriority','limitations','Historical priority remains unresolved','Historical firstness is established'),('claimhumanreview','ai_disclosure','without conventional external human peer review or formal proof-assistant certification','with conventional external human peer review and formal certification')]:
  v=copy.deepcopy(c)
  if isinstance(v[key],list):v[key]=[s.replace(old,new)for s in v[key]]
  else:v[key]=v[key].replace(old,new)
  failures=require(v)
  if not failures:raise RuntimeError('wordinglosscontrolsurvived '+name)
  controls.append({'deliberate_editorial_loss':name,'rejected_by':failures})
 return {'status':'PASS_SMALL_IN_MEMORY_EDITORIAL_CONTROLS','current_copy_passes':True,'controls_rejected':controls,'count':len(controls),'scientific_campaign_or_native_code_run':False,'writes':False,'network':False,'not_run_by_default_custody_helper':True}
if __name__=='__main__':print(json.dumps(run(),indent=2))
