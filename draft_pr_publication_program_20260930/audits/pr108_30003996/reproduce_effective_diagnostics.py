from pathlib import Path
import json,hashlib,datetime,os,subprocess,shutil,ast
A=Path(__file__).resolve().parent;D=A/'repaired_diagnostics_v1';O=A/'original_source_authentication_20261006/original_attempt';W=A/'root_effective_reproductions_20261006';W.mkdir(exist_ok=False)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(c,m):
 if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
records=[]
def run(label,argv,cwd,expected):
 start=now();p=subprocess.Popen(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
 (W/(label+'.stdout.bin')).write_bytes(out);(W/(label+'.stderr.bin')).write_bytes(err)
 row={'label':label,'argv':argv,'cwd':str(cwd),'PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'expected_exit_code':expected,'stdout_bytes':len(out),'stderr_bytes':len(err),'stdout_sha256':sha(out),'stderr_sha256':sha(err)};records.append(row)
 (W/'PROCESS_JOURNAL.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'records':records},indent=2)+'\n')
 require(p.returncode==expected,'unexpected execution: '+label+': '+err.decode()[:1000])
 return row
checks=[]
for mode in ['normal','optimized']:
 case=W/('candidate_'+mode);shutil.copytree(D,case)
 opts=['/opt/homebrew/bin/python3','-E','-B']+(['-O'] if mode=='optimized' else [])
 for family,script,result,original in [
  ('author','verify.py','verification.json','verification.json'),
  ('old_review','independent_review/independent_checks.py','independent_review/independent_results.json','independent_review/independent_results.json')]:
  label=family+'_'+mode
  run(label,opts+[script],case,0)
  x=json.loads((case/result).read_text());old=json.loads((O/original).read_text())
  require(x['all_pass'] is True and x['artifact_sha256']==sha((D/'PROOF.md').read_bytes()),'result proof/pass')
  require(x['verifier_sha256']==sha((D/script).read_bytes()),'result code')
  require(x['guard_mode']=='explicit_require_survives_python_optimization','guard mode')
  for key,value in old.items():
   if key!='artifact_sha256':require(x[key]==value,'original count/result changed: '+key)
  (W/(label+'.receipt.json')).write_text(json.dumps(x,indent=2)+'\n')
  checks.append({'label':label,'counts_equal_original':True,'proof_sha256':x['artifact_sha256'],'verifier_sha256':x['verifier_sha256'],'actual_checks':x['assertions']})
 # Extract the actual guard function from each current body, preserving its exact code.
 for family,script in [('author','verify.py'),('old_review','independent_review/independent_checks.py')]:
  text=(D/script).read_text();nodes=[n for n in ast.walk(ast.parse(text)) if isinstance(n,ast.FunctionDef) and n.name=='require'];require(len(nodes)==1,'guard function')
  body=ast.get_source_segment(text,nodes[0]);control=W/(family+'_'+mode+'_falseguard.py');control.write_text(body+'\nrequire(False, "intentional known-false control")\n')
  run(family+'_'+mode+'_falseguard',opts+[str(control)],W,1)
 corrupt=W/('corrupt_proof_'+mode);shutil.copytree(D,corrupt);q=corrupt/'independent_review/author_replay/PROOF.md';q.write_bytes(q.read_bytes()+b'\nintentional corruption\n')
 run('proof_binding_'+mode,opts+['independent_review/independent_checks.py'],corrupt,1)
 corrupt=W/('corrupt_cost_'+mode);shutil.copytree(D,corrupt);q=corrupt/'verify.py';t=q.read_text();old='val=0 if (u,v)==(0,1) else (B if v>=n+2 else 1)';new='val=0 if (u,v)==(0,1) else (B+1 if v>=n+2 else 1)';require(t.count(old)==1,'cost corruption span');q.write_text(t.replace(old,new))
 run('cost_guard_'+mode,opts+['verify.py'],corrupt,1)
result={'schema':'pr108-root-effective-reproduction/v1','UTC':now(),'actual_operator_PID':os.getpid(),'all_actual_exits_expected':True,'valid_replays':checks,'intentional_false_or_corrupt_controls_rejected':8,'actual_runs':len(records),'original_budget':'2/5','new_central_proof_search_turns':0,'priority_clearance':False,'proof_sha256':sha((D/'PROOF.md').read_bytes())}
(W/'REPRODUCTION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
