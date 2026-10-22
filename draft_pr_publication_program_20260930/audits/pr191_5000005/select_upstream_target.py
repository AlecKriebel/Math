"""Authenticate the exact imported target only; no prior triage opinion is adopted."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math');p=R/'unsolved_math_prioritization/cache/problems.json';b=p.read_bytes();sha=hashlib.sha256(b).hexdigest()
if sha!='04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf':raise RuntimeError('Pinned upstream full file changed')
j=json.loads(b);found=[]
def scan(x):
 if isinstance(x,dict):
  if str(x.get('id'))=='5000005' and x.get('problem_number')=='AMR-049-0005':found.append(x)
  else:
   for z in x.values():scan(z)
 elif isinstance(x,list):
  for z in x:scan(z)
scan(j)
if len(found)!=1:raise RuntimeError('Target identity not unique')
full=found[0];selected={k:full[k] for k in ['id','problem_number','title','statement','background','proposed_by','proposed_year'] if k in full}
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'upstream_repository':'ulamai/UnsolvedMath','immutable_revision':'37e53eabe540fb458758e198be61634bd02ee008','full_file_bytes':len(b),'full_file_sha256':sha,'selected_target':selected,'upstream_open_status_and_research_triage_not_adopted_as_present_facts':True,'scope':'Problem statement/provenance selected; priority and imported prior report not evaluated at this step.'}
q=A/'ROOT_EXACT_UPSTREAM_TARGET_01.json'
if q.exists():raise RuntimeError('Do not overwrite target receipt')
q.write_text(json.dumps(out,indent=2)+'\n');q.chmod(0o444);print(json.dumps(out,indent=2))
