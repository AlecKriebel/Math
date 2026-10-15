from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
A=Path(__file__).resolve().parent
utc=datetime.now(timezone.utc).isoformat()
p=A/'ROOT_SOURCE_ONLY_BASELINE.md'
j={'utc':utc,'stage':'BEFORE_PR329_MATHEMATICAL_CONTENT_EXPOSURE',
   'baseline':{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},
   'source_capture':json.loads((A/'ROOT_SOURCE_CAPTURE.json').read_text()),
   'root_prior_source_payload_embedded_research_summary_exposure':True,
   'independence_limit':'Root source retrieval included embedded prior research summary; no PR mathematical prose or inherited reviewers yet opened.',
   'original_turn_count':'1/5','workflow_percent':8,'mathematical_verification_percent':0,
   'no_readiness_or_priority_certificate':True}
(A/'ROOT_SOURCE_BASELINE_FREEZE.json').write_text(json.dumps(j,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc+' — Frozen original-source claim and falsifiable boundary tests before PR mathematics. Imported payload embedded prior summary was seen and explicitly disclosed; source-only subagents will retain independent exposure. Workflow8%, mathematical verification0%.\n')
print(json.dumps(j,indent=2))
