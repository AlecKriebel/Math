from pathlib import Path
import datetime, hashlib,json,runpy,sys
R=Path(__file__).resolve().parent;A=R.parents[1];V=R/'deployed/audits/pr1280_30003587/publication/verification/verify.py'
def binding(p):b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(v,m):
 if not v:raise RuntimeError(m)
v=runpy.run_path(str(V));s=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text());v['authenticate_snapshot'](A/'submitted',s)
current_matches_original=all((A/'submitted'/Path(e['path']).name).read_bytes()==(A/'current_edition'/Path(e['path']).name).read_bytes() for e in s['files'])
require(sum(e['bytes'] for e in s['files'])==74387,'Submitted original byte total drift')
print(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimization':sys.flags.optimize,'pr':1280,'problem_id':30003587,'snapshot':binding(A/'SUBMITTED_SNAPSHOT.json'),'files':s['files'],'file_count':9,'original_bytes':74387,'current_matches_original_at_observation':current_matches_original,'portable_verifier':binding(V),'scope':'Actual frozen originals only; current/original equality is an observation, not a current-edition requirement or permanent current binding. No mathematical or priority acceptance, new metadata, compile, package or publication approval.'},indent=2))
