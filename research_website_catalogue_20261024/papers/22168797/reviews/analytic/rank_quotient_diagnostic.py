from pathlib import Path
import sys,json
from fractions import Fraction
R=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/22168797/sources/published-source/K2P_SAME_Reproducibility_Package_v1.0.5-r1/k2p_same_reproducibility_v1.0.5-r1')
sys.path.insert(0,str(R/'package/referee/k2p_offline_sweep_portable/atlas'))
import k2p_atlas_core as a

def ranks(rec):
 d=a.model_descriptor_fast2(rec.graph);e,l=a.default_exact_point(d)
 J=a.descriptor_jacobian(d,e,l);q=a.eval_descriptor(d,e,l);w=a.coordinate_weights(d.k)
 T=[[q[i]*x for x in w[i]] for i in range(len(q))]
 r=a.exact_rank_pivots(J)[0];t=a.exact_rank_pivots(T)[0];rt=a.exact_rank_pivots([x+y for x,y in zip(J,T)])[0]
 return dict(raw=r,torus=t,full=rt,quotient=rt-t,k=d.k,core=rec.core_id,repair=rec.repair_index,words=rec.words)
out=[]
for r in [a.source_supports()[2],a.relabel_record((a.target_completions(4,True)+a.target_completions(4,False))[85],(2,0,1,3))]:
 row=ranks(r);out.append(row);print(json.dumps(row),flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
