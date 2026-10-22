"""Validate actual unsealed review records only; no acceptance/action call."""
from pathlib import Path
import datetime,hashlib,json,os,uuid
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012'
A=P/'audits/pr948_30004549';D=A/'preprint';O=A/'reviews/full_package_03'
core=P/'accept_pr948.py';raw=core.read_bytes()
if hashlib.sha256(raw).hexdigest()!='3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823':raise RuntimeError('core pin')
N={'__name__':'_review03_final_schema_only_','__file__':str(core)}
exec(compile(raw,str(core),'exec',dont_inherit=True,optimize=0),N)
f=json.loads((D/'FREEZE.json').read_text());r=json.loads((O/'RESULT.json').read_text())
complete=N['result_schema'](r)
if complete or r['clean_for_preprint'] or r['clean_context']:raise RuntimeError('procedural failure lost')
if r['nonclean_history']['status']!='failed':raise RuntimeError('honest failed-history status')
originals=N['original_check']();times={}
for name in ['AUTHENTICATION_START.json','AUTHENTICATION_END.json']:
 passed,t=N['review_authentication'](json.loads((O/name).read_text()),r['candidate_pins'],f,originals)
 if not passed:raise RuntimeError(name)
 times[name]=t
cold=json.loads((O/'COLD_REPLAY.json').read_text());passed,t=N['review_cold'](cold,r['candidate_pins'],f,D)
if not passed:raise RuntimeError('cold schema')
if not N['utc'](r['started_utc'])<=times['AUTHENTICATION_START.json']<=t<=times['AUTHENTICATION_END.json']<=N['utc'](r['completed_utc']):raise RuntimeError('chronology')
if not N['utc'](r['started_utc'])>N['utc'](json.loads((A/'reviews/full_package_02/RESULT.json').read_text())['completed_utc']):raise RuntimeError('fresh sequential round')
if set(r['inherited_finding_dispositions'])!=N['INHERITED_FINDING_IDS']:raise RuntimeError('all50 exact IDs')
if not all(v['verified'] is True and v['evidence'].strip() for v in r['inherited_finding_dispositions'].values()):raise RuntimeError('individual dispositions')
if not r['prior_issue_resolution']['R948-FULL01-R01']['verified']:raise RuntimeError('priorR01')
counts={'WORKFLOW.json':97,'HISTORY.json':58,'ROOT_FIXES.json':18,'BASE_CONTEXT.json':26,'LIVE_BASE.json':37}
for name,count in counts.items():
 v=json.loads((O/name).read_text())
 if v['status']!='PASS' or v['passed']!=count or v['failed']!=0:raise RuntimeError(name)
profile=json.loads((O/'profile/DEVELOPMENT_RESULTS.json').read_text())
if profile['event_count']!=85 or any('skip' in v.get('outcome','').lower() for v in profile['events']):raise RuntimeError('profile85/0skips')
qa=json.loads((O/'PDF_VISUAL_QA.json').read_text())
if not qa['personally_viewed'] or len(qa['images'])!=5:raise RuntimeError('actual all5page visualQA')
end=json.loads((O/'AUTHENTICATION_END.json').read_text())
if len(end['evidence_files_authenticated'])!=440 or len(end['operations_files'])!=7 or end['workflow_files_authenticated']!=357:raise RuntimeError('fullENDclosure')
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_SCHEMA_FOR_HONEST_NONCLEAN_HISTORY','result_schema':True,'review_authentication_START':True,'review_authentication_END':True,'review_cold':True,'real_original_pins':len(originals),'inherited_dispositions':50,'prior_R01_verified':True,'four_ordered_exact_cold_modes':True,'no_ignored_fields':cold['normalized_fields_ignored']==[],'suite_pass_counts':counts,'profile_cases':85,'profile_skips':0,'all5paper_pages_personally_viewed':True,'review03_eligible_clean':False,'no_candidate_repair_required':True,'real_action_functions_called':False,'core_sha256':hashlib.sha256(raw).hexdigest()}
target=O/'SCHEMA_VALIDATION.json';temp=O/('SCHEMA_VALIDATION.atomic_'+uuid.uuid4().hex+'.tmp')
with temp.open('xb') as s:s.write((json.dumps(record,indent=2)+'\n').encode());s.flush();os.fsync(s.fileno())
if target.exists():raise RuntimeError('existing schema receipt must not be overwritten')
os.replace(temp,target)
print(json.dumps(record))
