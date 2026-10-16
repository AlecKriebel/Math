import sys
if not sys.flags.isolated:raise RuntimeError('Use -I')
from pathlib import Path
import copy,datetime,hashlib,json
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';O=A/'reviews/full_package_02';D=A/'preprint';W=A/'reviews/full_package_01'
def h(b):return hashlib.sha256(b).hexdigest()
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
b=(O/'private/authenticated'/P.relative_to(R)/'accept_pr946.py').read_bytes();assert h(b)=='7d8d05fc3b05b249de51851db2eeb1e1d7adeecb774046183ecfb0fe08082e5a'
N={'__name__':'_historical_contract_','__file__':str(P/'accept_pr946.py')};exec(compile(b,N['__file__'],'exec'),N)
manifest=(W/'MANIFEST.json').read_bytes();assert h(manifest)=='2f1a4ba73839b83280e9daba44fbe79e70b52a80761deded5314e0db99c7e834';old=json.loads((W/'RESULT.json').read_bytes())
f=json.loads((D/'FREEZE.json').read_bytes());pin=h((D/'FREEZE.json').read_bytes());context=N['capture_inventory']('dd4e67e75a6271f9fa115095765373acc2e8953884b975a2bc710990826df0c4')
auth=json.loads((O/'AUTHENTICATION_START.json').read_bytes());expected={n:{k:v for k,v in r.items() if k not in ['archive_mode','disk_and_archive_match']} for n,r in auth['originals'].items()}
# Only a synthetic terminal record is supplied in memory to let review_check reach
# and pass its real historical-candidate branch for the actual nonclean round01.
# It is never written to a canonical review file and grants no acceptance.
t=datetime.datetime.now(datetime.timezone.utc);times=[(t+datetime.timedelta(microseconds=i)).isoformat() for i in range(5)]
r=copy.deepcopy(old);r.update(reviewer_agent_id='synthetic_contract_only',started_utc=times[0],completed_utc=times[4],candidate_revision=2,candidate_pins={'freeze':pin,'manifest':f['package_manifest_sha256'],'pdf':f['files']['research_note.pdf']['sha256']},inspected_helper_hashes=f['future_helpers'],required_issues=[],optional_issues=[],clean_for_preprint=True,prior_issue_resolution={x['id']:{'verified':True,'synthetic':True} for x in old['required_issues']+old['optional_issues']})
a1=copy.deepcopy(auth);a1['utc']=times[1];a2=copy.deepcopy(auth);a2['utc']=times[3];c=json.loads((O/'COLD_MODES.json').read_bytes());c.update(utc=times[2],typed_float_policy_verified=True,historical_strict_failure_preserved=True)
payload={'RESULT.json':enc(r),'AUTHENTICATION_START.json':enc(a1),'AUTHENTICATION_END.json':enc(a2),'COLD_REPLAY.json':enc(c),'FULL_AUDIT.md':b'Synthetic terminal contract fixture only.\n','RESEARCH_LOG.md':b'Synthetic fixture; no acceptance.\n'}
m=enc({'files':{n:{'bytes':len(b),'sha256':h(b)} for n,b in payload.items()},'explicit_public_allowlist':sorted(payload)});payload['MANIFEST.json']=m
originalread=N['read_regular']
def read(path,*a,**kw):
 path=Path(path)
 if path.parent==O and path.name in payload:
  b=payload[path.name]
  if kw.get('pin') is not None and kw['pin']!={'bytes':len(b),'sha256':h(b)}:raise RuntimeError('fixture pin')
  return b
 return originalread(path,*a,**kw)
N['read_regular']=read
result,latest=N['review_check'](['01:'+h(manifest),'02:'+h(m)],f,pin,context,expected)
report={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_historical_round01_manifest_sha256':h(manifest),'actual_historical_candidate01_freeze_sha256':old['candidate_pins']['freeze'],'current_core_sha256':h(b),'real_historical_files_authenticated':result[0]['public_files_authenticated'],'real_historical_archive_and_all_seven_old_sources_authenticated':True,'synthetic_latest_round_in_memory_only':True,'production_acceptance_performed':False,'limitations':'This checks current review_check historical branch against actual old artifacts. Synthetic clean terminal contract record is not a review or evidence of resolved findings.'};(O/'HISTORICAL_REVIEW_CONTROLS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
