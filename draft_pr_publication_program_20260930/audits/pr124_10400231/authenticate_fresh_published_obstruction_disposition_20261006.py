"""Root authentication of the fresh scientific disposition; no shared mutation."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;F=A/'fresh_published_obstruction_disposition_adversary_20261006'
D=A/'root_fresh_disposition_authentication_20261006'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def req(v,s):
 if not v:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def check(x):
 p=Path(x['path']);p=p if p.is_absolute() else A/p;b=p.read_bytes()
 req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Input/member changed '+str(p))
req(not D.exists(),'Prior actual fresh disposition authentication exists')
seal=load(F/'SEAL.json');result=load(F/'RESULT.json')
req(sha((F/'SEAL.json').read_bytes())=='32d7cbbb06934b10b9b5b0b2014f2e7d5b92aec4f404d87c784bf8068801220c','Fresh final seal')
req(result['verdict']=='PASS' and result['global_corrections_required']==[] and result['closing_without_novel_solution_paper_supported_under_precise_human_scope'] and result['already_solved_scoped_only_to_mathematical_content'],'Scientific scope')
req(not result['express_prior_named_refutation_established'] and result['possible_new_bibliographic_application_preserved'],'Historical limits')
for x in seal['public_members']:check(x)
check(seal['public_manifest']);inputs=load(F/'INPUT_HASHES.json')
for x in inputs['inputs']:check(x)
for name,digest in seal['exact_disposition_binding'].items():req(sha((A/name).read_bytes())==digest,'Reviewed final text changed')
D.mkdir();events=[]
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
for optimized in [False,True]:
 label='optimized' if optimized else 'normal';argv=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(F/'validate_algebra.py')]
 start=now();ch=subprocess.Popen(argv,cwd=D,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate()
 (D/(label+'.stdout.json')).write_bytes(out);(D/(label+'.stderr.txt')).write_bytes(err)
 events.append({'PID':ch.pid,'UTC_start':start,'UTC_end':now(),'argv':argv,'exit_code':ch.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)})
 req(ch.returncode==0,'Actual fresh algebra replay')
 actual=json.loads(out);expected=load(F/('ALGEBRA_OPTIMIZED.json' if optimized else 'ALGEBRA_NORMAL.json'))
 req({k:v for k,v in actual.items() if k!='UTC'}=={k:v for k,v in expected.items() if k!='UTC'},'Fresh exact replay mismatch')
 req(actual['optimization']==int(optimized),'Physical optimization mismatch')
for x in seal['public_members']:check(x)
for x in inputs['inputs']:check(x)
r={'schema':'pr124-root-actual-fresh-disposition-authentication/v1','UTC':now(),'actual_operator_PID':os.getpid(),'fresh_seal_sha256':sha((F/'SEAL.json').read_bytes()),'public_member_count_including_manifest_and_seal':len(seal['public_members'])+2,'public_members':seal['public_members']+[seal['public_manifest'],{'path':str((F/'SEAL.json').relative_to(A)),'bytes':(F/'SEAL.json').stat().st_size,'sha256':sha((F/'SEAL.json').read_bytes())}],'full_input_count':len(inputs['inputs']),'all_full_input_hashes_verified':True,'exact_disposition_and_comment_binding':seal['exact_disposition_binding'],'actual_child_events':events,'normal_and_physical_optimized_replays_match':True,'fresh_scientific_disposition_PASS':True,'global_corrections_required':[],'native_PR_services_mutations':False,'original_budget':'2/5','new_central_proof_search_turns':0}
dump(A/'ROOT_FRESH_DISPOSITION_AUTHENTICATION_20261006.json',r)
ready={'schema':'pr124-published-obstruction-scoped-disposition-ready/v1','UTC':now(),'actual_root_authenticator_PID':os.getpid(),'PR':124,'problem_id':10400231,'original_head':'d110ad761291aa6ac1d66d2a49e8b8212c18bed6','original_literal_status':'claimed_solved','original_budget':'2/5','new_central_proof_search_turns':0,'mathematical_clearance':True,'old_published_full_family_and_general_obstruction_verified':True,'fresh_disposition_review_PASS':True,'fresh_disposition_review':str((F/'REPORT.md').relative_to(A)),'fresh_disposition_review_sha256':sha((F/'REPORT.md').read_bytes()),'fresh_disposition_authentication':'ROOT_FRESH_DISPOSITION_AUTHENTICATION_20261006.json','closing_comment_file':'CLOSING_COMMENT_OLD_PUBLISHED_OBSTRUCTION_20261006.md','closing_comment_sha256':seal['exact_disposition_binding']['CLOSING_COMMENT_OLD_PUBLISHED_OBSTRUCTION_20261006.md'],'root_disposition_sha256':seal['exact_disposition_binding']['ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_20261006.md'],'native_status_correction_supported':True,'native_status':'already_solved','classification_scope':'Old published mathematical content/direct corollary; express prior named conjecture refutation unestablished','express_historical_refutation_established':False,'first_explicit_application_priority_established':False,'substantive_novel_resolution_established':False,'publication_authorization':False,'paper_DOI_tracker_allowed':False,'closure_without_merge_authorized_by_human_scope':True,'closure_action_performed':False,'native_correction_performed':False,'fresh_writer_grant_required_before_shared_native_export_and_commit':True,'workflow_percent':80,'program_completed':20,'published':11,'persistent_goal_status':'active'}
dump(A/'ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_READY_20261006.json',ready)
print(json.dumps({k:v for k,v in r.items() if k not in ['public_members','actual_child_events']}))

