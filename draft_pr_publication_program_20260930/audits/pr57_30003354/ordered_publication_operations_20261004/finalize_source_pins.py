"""Final SOURCE-only integrity readback; no integration helper import or execution."""
import ast,datetime as dt,hashlib,json,os,stat,sys
from pathlib import Path
own=Path(__file__).resolve().parent;repo=own.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(repo).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
for p in [own/'NATIVE_MERGE_RESULT.json',own/'NATIVE_ACCEPTANCE_RESULT.json',own/'private/integration-merge',own/'private/integration-mirror']:
 if p.exists():raise RuntimeError('SOURCE-only handoff must have no helper execution receipt/directory')
inputs=json.loads((own/'SOURCE_BINDINGS.json').read_bytes());helper=own/'integrate_published_result.py';h=pin(helper)
if h['sha256']!=inputs['integration_helper']['sha256']:raise RuntimeError('Operative helper hash differs')
source=helper.read_bytes();parsed=ast.parse(source,str(helper));compile(parsed,str(helper),'exec')
commands=json.loads((own/'private/actual_readonly_inspection/COMMANDS.json').read_bytes())
for i,x in enumerate(commands,1):
 p=own/'private/actual_readonly_inspection'
 if sha((p/(str(i)+'.stdout')).read_bytes())!=x['stdout_sha256'] or sha((p/(str(i)+'.stderr')).read_bytes())!=x['stderr_sha256']:raise RuntimeError('Actual inspection command stream drift')
 if not isinstance(x['actual_pid'],int) or x['exit_code'] not in [0,128]:raise RuntimeError('Actual provenance differs')
for n in ['source_build_capture','source_build_capture_v2']:
 x=json.loads((own/'private'/n/'CAPTURE.json').read_bytes())
 if x['exit_code']!=0 or x['integration_helper_executed'] is not False:raise RuntimeError('SOURCE builder actual execution differs')
 p=own/'private'/n
 if sha((p/'stdout.bin').read_bytes())!=x['stdout_sha256'] or sha((p/'stderr.bin').read_bytes())!=x['stderr_sha256']:raise RuntimeError('Builder exact output differs')
now=dt.datetime.now(dt.timezone.utc).isoformat()
with (own/'RESEARCH_LOG.md').open('a') as f:
 f.write('- '+now+' — Final SOURCE-v2 checkpoint: status-first helper guards strengthened before any scientific inputs; draft v1 and its capture retained. ROOT reports actual record23131374, DOI10.5281/zenodo.23131374 publication, with service verification/tracker/final gate in progress. Child performs no service or Git/native action and does not infer those pending receipts. Operations SOURCE preparation100%; helper execution remains0%.\n')
x=json.loads((own/'READINESS.json').read_bytes());x['SOURCE_version']='v2';x['final_SOURCE_checkpoint_UTC']=now;x['root_actual_publication_report_received']={'DOI':'10.5281/zenodo.23131374','record_id':23131374,'status':'Reported by ROOT; child has not performed publication/service verification'}
(own/'READINESS.json').write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
paths=sorted(p for p in own.rglob('*') if p.is_file() and p.name!='FINAL_SOURCE_PINS.json')
result={'schema':'pr57-ordered-publication-operations-final-SOURCE-pins/v1','UTC':now,'actual_finalizer_pid':os.getpid(),'actual_argv':sys.argv,'SOURCE_version':'v2','pins':[pin(p) for p in paths],'integration_helper':h,'SOURCE_BINDINGS':pin(own/'SOURCE_BINDINGS.json'),'helper_AST_parse_and_compile':True,'helper_imported_or_executed':False,'actual_inspection_commands_and_streams_verified':len(commands),'actual_source_builder_exit_codes':[0,0],'original_remote_science_body_mode_blob_checks':17,'frozen_custody_members_checked':273,'ROOT_authority_asserted_by_child':False,'actual_exclusive_PR57_writer_window_claimed':False,'native_Git_index_ref_PR_service_or_human_contact_action':False,'operations_SOURCE_preparation_percent':100,'new_central_proof_attempts':0,'original_budget':'1/5','old_frozen_packet_mutation':False}
p=own/'FINAL_SOURCE_PINS.json'
if p.exists():raise RuntimeError('Final SOURCE pins already exist')
p.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps({'final_SOURCE_pins':pin(p),'integration_helper':h,'SOURCE_BINDINGS':pin(own/'SOURCE_BINDINGS.json'),'SOURCE_member_count':len(paths),'actual_inspection_command_count':len(commands)},indent=2))
