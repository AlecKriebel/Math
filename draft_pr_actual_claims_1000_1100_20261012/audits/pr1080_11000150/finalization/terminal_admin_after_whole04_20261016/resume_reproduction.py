#!/usr/bin/env python3
"""Resume the four remaining interfaces after the explicit storage interruption."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0';S=W/'scratch';K=S/'clean_check/verification_kit';receipt=W/'ACTUAL_COMMAND_RECEIPTS.jsonl'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pins(root):return {p.relative_to(root).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink() and (root!=A or not p.is_relative_to(W))}
def need(x,s):
 if not x:raise RuntimeError(s)
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
prior=[json.loads(s) for s in receipt.read_text().splitlines()];need(len(prior)==27 and all((r['returncode']==0)==r['expected_success'] for r in prior[:26]) and prior[-1]['returncode']!=0 and 'Errno 28' in prior[-1]['stderr'],'Exact interrupted final-stage receipts')
baseline=pins(A);initial=pins(K);canonical=pins(D/'verification_kit');need(initial==canonical and len(baseline)==898 and len(initial)==299,'Exact final extraction/canonical identity before resume')
dump(W/'RESUME_FROZEN_INPUTS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'canonical':baseline,'clean_extracted':initial,'source':'Current final package; existing26 completed commands remain exact evidence, output wrapper interruption explicit.'})
env=dict(os.environ,TMPDIR=str(S/'temp'),PYTHONDONTWRITEBYTECODE='1');rows=[]
def run(label,args,cwd=K):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run([str(x) for x in args],cwd=cwd,env=env,capture_output=True,text=True,timeout=300);v={'utc':start,'label':label,'argv':[str(x) for x in args],'cwd':str(cwd),'expected_success':True,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'free_bytes_after':shutil.disk_usage(W).free}
 with receipt.open('a') as f:f.write(json.dumps(v)+'\n')
 rows.append(v);need(r.returncode==0,'Resumed command failed '+label+' '+r.stderr[-1400:])
run('complete output guards normal/optimized internally resumed',[sys.executable,'-B','-I',K/'output_guard_checks.py'])
run('independent complete path/binding interfaces normal/optimized',[sys.executable,'-B','-I',W/'interface_regressions.py'],cwd=W)
run('current status/evidence coherently rehashed closed-repacked faults normal/optimized',[sys.executable,'-B','-I',W/'status_faults.py'],cwd=W)
run('actual repository native uploader LOCAL check',[sys.executable,'-B',A.parents[2]/'zenodo_deposit_tool/zenodo.py','check',D/'deposit_metadata.json'],cwd=A.parents[2])
need(pins(K)==initial and pins(A)==baseline,'Resume changed inputs');need((W/'FULL_MATHEMATICAL_OUTPUT_COMPARISON.json').read_bytes()==(W/'FULL_MATHEMATICAL_OUTPUT_COMPARISON_O.json').read_bytes(),'Full mathematical modes differ')
guard=json.loads(rows[0]['stdout']);interfaces=json.loads((W/'INDEPENDENT_SEMANTIC_RESULTS.json').read_text());semantic=json.loads((W/'STATUS_SEMANTIC_RESULTS.json').read_text())
dump(W/'REPRODUCTION_SUMMARY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_commands':len(prior)+len(rows),'completed_expected_commands':30,'explicit_ENOSPC_interrupted_commands':1,'completed_before_storage_interruption':26,'resumed_commands':4,'canonical_files_unchanged':len(baseline),'extracted_files_unchanged':len(initial),'normal_optimized_full_mathematical_JSON_equal':True,'all_mathematical_fields_equal_adopted_whole04':True,'historical_52_input_tail_replayed':False,'guard_rejections':guard['rejection_count'],'guard_protected_files':guard['protected_file_count'],'physical_case_rejections':sum(r.get('fault','').startswith('physical-case') for r in guard['rejections']),'independent_path_binding_interface_commands':interfaces['actual_commands'],'coherently_rehashed_repacked_status_evidence_fault_commands':semantic['actual_commands'],'native_LOCAL_check_only':True,'new_compile_render_view':False,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032});print((W/'REPRODUCTION_SUMMARY.json').read_text())
