"""Persist enough digits to replay the near-boundary extreme numerical orbit."""
from pathlib import Path
import runpy,json
root=Path(__file__).resolve().parent
g=runpy.run_path(str(root/"independent_geometry.py"));mp=g['mp']
record,lam,values=g['one_case'](mp.mpf(10),mp.mpf(1),64,31)
record['lambda']=mp.nstr(lam,175)
record['serialized_significant_digits']=175
record['arithmetic_digits']=mp.mp.dps
record['bisection_steps']=540
record['warning']='Numerical resonance record, not interval-arithmetic proof. The broad results retain their original125digit lambda field, insufficient for this extreme replay.'
record['maximum_residuals']={k:mp.nstr(v,15) for k,v in g['metrics'].items()}
(root/'extreme_resonance_record.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
