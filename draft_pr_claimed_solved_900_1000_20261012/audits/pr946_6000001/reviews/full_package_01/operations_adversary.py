import sys
if not sys.flags.safe_path:raise SystemExit('safe startup')
import pathlib,json,hashlib,datetime,copy
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';W=A/'reviews/full_package_01';SOURCE=P/'accept_pr946.py'
b=SOURCE.read_bytes()
if hashlib.sha256(b).hexdigest()!='c9dc84ce258488ce9929fba2b2e7cc3a19077a3cf52d9fac1cea0c9798ab9ad8':raise ValueError('core pin')
N={'__name__':'_review_adversary_core_','__file__':str(SOURCE)};exec(compile(b,str(SOURCE),'exec'),N)
# No real command, network, or mutation boundary may execute in this test.
def forbidden(*a,**k):raise RuntimeError('Forbidden external boundary')
N['run']=forbidden;N['blob']=forbidden;N['remote_main']=forbidden
F=json.loads((A/'preprint/FREEZE.json').read_text());FP=hashlib.sha256((A/'preprint/FREEZE.json').read_bytes()).hexdigest()
AUTH=json.loads((W/'AUTHENTICATION_START.json').read_text()); expected={k:{x:v for x,v in p.items() if x not in ['archive_mode','disk_and_archive_match']} for k,p in AUTH['originals'].items()}
fix=W/'private/chain_fixture';(fix/'reviews').mkdir(parents=True,exist_ok=True);N['A']=fix
N['archive_check']=lambda *a,**k:{'payload_files':219,'zip_members':220}
def encode(j):return (json.dumps(j,indent=2)+'\n').encode()
def fp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
specs=[]
for number in range(1,4):
 folder=fix/'reviews'/f'full_package_{number:02d}';folder.mkdir(exist_ok=True)
 ts=[f'2026-10-15T0{number}:00:0{i}+00:00' for i in range(5)]
 auth=copy.deepcopy(AUTH);auth['utc']=ts[1]
 endauth=copy.deepcopy(AUTH);endauth['utc']=ts[3]
 cold=json.loads((W/'COLD_REPLAY.json').read_text());cold['utc']=ts[2]
 result={'pr':946,'problem_id':'6000001','original_pr_head':N['HEAD'],'reviewer_agent_id':'synthetic_'+str(number),'clean_context':True,'full_reproducer_completed':True,'started_utc':ts[0],'completed_utc':ts[4],'candidate_revision':1,'candidate_pins':{'freeze':FP,'manifest':F['package_manifest_sha256'],'pdf':F['files']['research_note.pdf']['sha256']},'inspected_helper_hashes':F['future_helpers'],'required_issues':[] if number<3 else [{'id':'LATER-REQUIRED','summary':'Synthetic unresolved required issue'}],'optional_issues':[],'clean_for_preprint':number<3,'mathematical_remaining_gap_for_stated_theorem':None,'strongest_verified_theorem':'Synthetic guard fixture only, not an actual proof verdict.','prior_issue_resolution':{}}
 data={'RESULT.json':encode(result),'AUTHENTICATION_START.json':encode(auth),'AUTHENTICATION_END.json':encode(endauth),'COLD_REPLAY.json':encode(cold),'FULL_AUDIT.md':b'Synthetic evidence only.\n','RESEARCH_LOG.md':b'Synthetic log only.\n'}
 for name,raw in data.items():(folder/name).write_bytes(raw)
 m=encode({'files':{k:fp(v) for k,v in data.items()},'explicit_public_allowlist':sorted(data)});(folder/'MANIFEST.json').write_bytes(m);specs.append(f'{number:02d}:'+hashlib.sha256(m).hexdigest())
# The directory contains three sealed sequential canonical review rounds.
accepted=N['review_check'](specs[:2],F,FP,{},expected)
full_rejected=False
try:N['review_check'](specs,F,FP,{},expected)
except RuntimeError as e:full_rejected='latest complete review' in str(e)
if len(accepted[0])!=2 or not full_rejected:raise RuntimeError('reproducer failed')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'DEFECT_REPRODUCED','id':'FP01-OPS-001','case':'later_sealed_adverse_review_omitted_from_supplied_prefix','canonical_round_directories':['full_package_01','full_package_02','full_package_03'],'supplied_rounds':[1,2],'prefix_accepted':True,'all_three_rounds_rejected':full_rejected,'omitted_required_id':'LATER-REQUIRED','external_actions':0,'core_sha256':hashlib.sha256(b).hexdigest(),'impact':'review_check accepts an earlier clean prefix despite a later sealed canonical round with unresolved required findings; it never inventories canonical review directories.'}
(W/'OPERATIONS_ADVERSARY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
# Mandatory schema fields must not be optional for reviews pinned to current freeze.
folder=fix/'reviews/full_package_02'
base_result=(folder/'RESULT.json').read_bytes();base_cold=(folder/'COLD_REPLAY.json').read_bytes()
schema_cases=[]
for case in ['missing_candidate_revision','wrong_candidate_revision','missing_normalized_fields_ignored']:
 jr=json.loads(base_result);jc=json.loads(base_cold)
 if case=='missing_candidate_revision':jr.pop('candidate_revision')
 elif case=='wrong_candidate_revision':jr['candidate_revision']=999
 else:jc.pop('normalized_fields_ignored')
 (folder/'RESULT.json').write_bytes(encode(jr));(folder/'COLD_REPLAY.json').write_bytes(encode(jc))
 m=json.loads((folder/'MANIFEST.json').read_text())
 for name in m['files']:m['files'][name]=fp((folder/name).read_bytes())
 raw=encode(m);(folder/'MANIFEST.json').write_bytes(raw)
 changed_specs=[specs[0],'02:'+hashlib.sha256(raw).hexdigest()]
 got=N['review_check'](changed_specs,F,FP,{},expected)
 schema_cases.append({'case':case,'invalid_schema_accepted':len(got[0])==2})
(folder/'RESULT.json').write_bytes(base_result);(folder/'COLD_REPLAY.json').write_bytes(base_cold)
schema={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'DEFECT_REPRODUCED','id':'FP01-OPS-002','cases':schema_cases,'external_actions':0,'contract':'SCHEMA_AND_USE requires candidate_revision and normalized_fields_ignored; current-freeze reviews accept a missing or contradictory revision and a missing normalization declaration.'}
(W/'SCHEMA_ADVERSARY.json').write_text(json.dumps(schema,indent=2)+'\n');print(json.dumps(schema))

