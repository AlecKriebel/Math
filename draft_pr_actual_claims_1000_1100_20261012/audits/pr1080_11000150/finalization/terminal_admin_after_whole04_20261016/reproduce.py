#!/usr/bin/env python3
"""Actual canonical and clean current checks; all subprocess outcomes retained."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,zipfile
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0';S=W/'scratch';K=S/'clean_check/verification_kit';C=D/'verification_kit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pins(root):return {p.relative_to(root).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink() and not p.is_relative_to(W)}
def need(x,s):
 if not x:raise RuntimeError(s)
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
receipt=W/'ACTUAL_COMMAND_RECEIPTS.jsonl';need(not receipt.exists(),'Never erase attempt receipts');S.mkdir();(S/'temp').mkdir();env=dict(os.environ,TMPDIR=str(S/'temp'),PYTHONDONTWRITEBYTECODE='1');baseline=pins(A)
with zipfile.ZipFile(D/'verification_kit.zip') as z:z.extractall(S/'clean_check')
initial={p.relative_to(K).as_posix():sha(p) for p in K.rglob('*') if p.is_file()};rows=[]
def run(label,args,cwd=K,success=True,needle=None):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run([str(x) for x in args],cwd=cwd,env=env,capture_output=True,text=True,timeout=300);v={'utc':start,'label':label,'argv':[str(x) for x in args],'cwd':str(cwd),'expected_success':success,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'free_bytes_after':shutil.disk_usage(W).free}
 with receipt.open('a') as f:f.write(json.dumps(v)+'\n')
 rows.append(v);need((r.returncode==0)==success,'Actual unexpected result '+label+' '+r.stderr[-1400:])
 if needle:need(needle in r.stderr,'Wrong fault cause '+label)
 return r
for opt in [False,True]:
 prefix=[sys.executable,'-B','-I']+(['-O'] if opt else [])
 for loc,kit in [('canonical',C),('clean',K)]:
  run(loc+' verifier',prefix+[kit/'verify.py']);run(loc+' complete portable adapters',prefix+[kit/'run_checks.py']);run(loc+' complete mathematical/custody fault wrapper',prefix+[kit/'fault_checks.py'])
 run('strict required external binding',prefix+[K/'verify.py','--require-binding','--binding',D/'EXTERNAL_BINDING.json','--pdf',D/'preprint.pdf','--archive',D/'verification_kit.zip'])
 run('full mathematical JSON against adopted whole04',prefix+[W/'fullmath.py'])
 run('independent whole04 finite controls',prefix+[A/'newreviews/package_04/independent_controls.py'])
 for fault,needle in [('insertion','whole04 independent guard'),('parity','whole04 independent guard'),('crossing','whole04 independent guard')]:run('independent '+fault+' fault',prefix+[A/'newreviews/package_04/independent_controls.py','--fault',fault],success=False,needle=needle)
 target=S/('rebuilt-O.zip' if opt else 'rebuilt.zip');run('fresh deterministic external rebuild',prefix+[K/'build_archive.py','--output',target]);need(sha(target)==sha(D/'verification_kit.zip'),'Closed rebuilt archive differs')
 with (W/'OWNED_EARLY_CLEANUP.jsonl').open('a') as f:f.write(json.dumps({'path':str(target),'bytes':target.stat().st_size,'sha256':sha(target),'reason':'Own fresh rebuild after exact current-ZIP comparison'})+'\n')
 target.unlink()
run('complete output guards normal/optimized internally',[sys.executable,'-B','-I',K/'output_guard_checks.py'])
run('independent complete path/binding interfaces normal/optimized',[sys.executable,'-B','-I',W/'interface_regressions.py'],cwd=W)
run('current status/evidence coherently rehashed closed-repacked faults normal/optimized',[sys.executable,'-B','-I',W/'status_faults.py'],cwd=W)
run('actual repository native uploader LOCAL check',[sys.executable,'-B',A.parents[2]/'zenodo_deposit_tool/zenodo.py','check',D/'deposit_metadata.json'],cwd=A.parents[2])
need({p.relative_to(K).as_posix():sha(p) for p in K.rglob('*') if p.is_file()}==initial,'Clean extracted inputs changed');need(pins(A)==baseline,'Canonical inputs changed')
need((W/'FULL_MATHEMATICAL_OUTPUT_COMPARISON.json').read_bytes()==(W/'FULL_MATHEMATICAL_OUTPUT_COMPARISON_O.json').read_bytes(),'Normal/-O mathematical JSON differs')
guard=json.loads(next(r['stdout'] for r in rows if r['label'].startswith('complete output guards')));interfaces=json.loads((W/'INDEPENDENT_SEMANTIC_RESULTS.json').read_text());semantic=json.loads((W/'STATUS_SEMANTIC_RESULTS.json').read_text())
dump(W/'REPRODUCTION_SUMMARY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_commands':len(rows),'canonical_files_unchanged':len(baseline),'extracted_files_unchanged':len(initial),'normal_optimized_full_mathematical_JSON_equal':True,'all_mathematical_fields_equal_adopted_whole04':True,'historical_52_input_tail_replayed':False,'guard_rejections':guard['rejection_count'],'guard_protected_files':guard['protected_file_count'],'physical_case_rejections':sum(r.get('fault','').startswith('physical-case') for r in guard['rejections']),'independent_path_binding_interface_commands':interfaces['actual_commands'],'coherently_rehashed_repacked_status_evidence_fault_commands':semantic['actual_commands'],'native_LOCAL_check_only':True,'new_compile_render_view':False,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032});print((W/'REPRODUCTION_SUMMARY.json').read_text())
