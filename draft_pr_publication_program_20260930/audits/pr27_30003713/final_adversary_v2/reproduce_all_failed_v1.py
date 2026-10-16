"""Run unchanged current, original, all families, firstfresh and root computations in isolated topology."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess
P=Path(__file__).resolve().parent;A=P.parent;R=P.parents[3];PY='/usr/bin/python3';sha=lambda b:hashlib.sha256(b).hexdigest()
W=P/'ignoredtmp/legacytopology';WA=W/'draft_pr_publication_program_20260930/audits/pr27_30003713';WA.mkdir(parents=True,exist_ok=True)
D=json.loads((A/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json').read_text())
for x in D['supporting_first_party_files']:
 src=R/x['path'];dst=W/x['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
for n in ['source_snapshot','historical_candidate_v1']:
 shutil.copytree(A/n,WA/n,dirs_exist_ok=True)
shutil.copytree(A/'historical_candidate_v1',WA/'reviewed_candidate',dirs_exist_ok=True)
for n in ['snapshot_manifest.json','pr_input.json']:
 shutil.copyfile(A/n,WA/n)
Q=W/'unsolved_math_prioritization';Q.mkdir(exist_ok=True);shutil.copyfile(R/'unsolved_math_prioritization/manifest.json',Q/'manifest.json')
if not (Q/'cache').exists():(Q/'cache').symlink_to(R/'unsolved_math_prioritization/cache',target_is_directory=True)
ENV=os.environ.copy();ENV.update({'GIT_DIR':str(R/'.git'),'GIT_WORK_TREE':str(W),'PYTHONDONTWRITEBYTECODE':'1'})
records=[]
def run(name,script,receipt=None,old=None,volatile=(),expect=0,expected_stderr=None):
 b=script.read_bytes();r=subprocess.run([PY,str(script)],cwd=script.parent,env=ENV,capture_output=True,text=True,timeout=900)
 log=P/'ignoredtmp'/('run_'+name+'.log');log.write_text(r.stdout+'\n'+r.stderr)
 assert r.returncode==expect if expect==0 else r.returncode!=0,(name,r.returncode,r.stderr[-1500:])
 assert b==script.read_bytes()
 row={'name':name,'exit_code':r.returncode,'script_sha256':sha(b),'log_sha256':sha(log.read_bytes())}
 if expected_stderr:assert expected_stderr in r.stderr,(name,r.stderr)
 if receipt:
  fb=receipt.read_bytes();ob=old.read_bytes();fj=json.loads(fb);oj=json.loads(ob)
  for k in volatile:fj.pop(k,None);oj.pop(k,None)
  assert fj==oj,(name,'mathematical output changed');row.update({'receipt_sha256':sha(fb),'old_receipt_sha256':sha(ob),'byte_exact':fb==ob,'mathematical_fields_equal':True,'excluded_fields':list(volatile)})
 records.append(row);print('verified '+name,flush=True)
# Old hardcoded guard receives exactly its historical22 topology; never current23.
run('firstfresh_historical_guard',WA/'final_adversary/verify_gate_inputs.py')
run('firstfresh_reproduce_complete',WA/'final_adversary/reproduce_complete.py')
# Its nested reproduction reruns original/current22/allthree/rootbase; independently compare receipt.
oldrep=json.loads((A/'final_adversary/REPRODUCTION_RECEIPT.json').read_text());newrep=json.loads((WA/'final_adversary/REPRODUCTION_RECEIPT.json').read_text())
assert newrep['status']==oldrep['status']=='PASS_REPRODUCTION'
assert newrep['all_original_and_current_receipts_byte_exact'] and oldrep['all_original_and_current_receipts_byte_exact']
for row in newrep['runs']:
 oldrow=next(x for x in oldrep['runs'] if x['name']==row['name'])
 for key in ['script_sha256','mathematical_fields_equal','byte_equal','historical_receipt_sha256','excluded_volatile_fields','exit_code']:
  if key in oldrow:assert row[key]==oldrow[key],(row['name'],key)
run('firstfresh_controls',WA/'final_adversary/fresh_controls.py',WA/'final_adversary/FRESH_CONTROLS_RECEIPT.json',A/'final_adversary/FRESH_CONTROLS_RECEIPT.json',('utc',))
run('firstfresh_r2',WA/'final_adversary/r2_comparison_control.py',WA/'final_adversary/R2_COMPARISON_RECEIPT.json',A/'final_adversary/R2_COMPARISON_RECEIPT.json')
run('root_range',WA/'root_auxiliary_range_controls.py',WA/'root_auxiliary_range_results.json',A/'root_auxiliary_range_results.json')
# Every failed executable is still reproduced as failure; no failed run promoted to a receipt.
for name,rel,error in [('root_base_failed','root_powell_base_controls_failed_v1.py','AttributeError'),('firstfresh_v1_failed','final_adversary/fresh_controls_failed_v1.py','AssertionError'),('firstfresh_v2_failed','final_adversary/fresh_controls_failed_v2.py','TypeError'),('firstfresh_r2_failed','final_adversary/r2_comparison_control_failed_v1.py','AssertionError')]:
 run(name,WA/rel,expect=1,expected_stderr=error)
# Restore independent current23 copy and reproduce the unmodified author/reviewer pair.
CW=P/'ignoredtmp/current23';shutil.copytree(A/'reviewed_candidate',CW,dirs_exist_ok=True)
for name,rel,receipt in [('current23_author','verify.py','verification.json'),('current23_reviewer','review/independent_checks.py','review/independent_results.json')]:
 run(name,CW/rel,CW/receipt,A/'reviewed_candidate'/receipt)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ALL_REPRODUCTION','runtime':PY,'firstfresh_historical_topology':'historical_candidate_v1 restored as reviewed_candidate; old code byte unchanged','firstfresh_nested_runs':newrep['runs'],'runs':records,'new_substantive_attempts':0,'future_canonical_bytes_blessed':False}
(P/'REPRODUCTION_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'direct_runs':len(records),'nested_runs':len(newrep['runs'])}))
