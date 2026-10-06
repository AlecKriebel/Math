#!/usr/bin/env python3
from pathlib import Path
import datetime,hashlib,json,subprocess,sys,time
A=Path(__file__).resolve().parent
B=A.parent
runs=[]
def require(c,m):
 if not c: raise RuntimeError(m)
def execute(label,command,expected=0):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 r=subprocess.run(command,capture_output=True,text=True,cwd=A)
 (A/(label+'.stdout.json')).write_text(r.stdout)
 (A/(label+'.stderr.txt')).write_text(r.stderr)
 require(r.returncode==expected,label+' exit code')
 runs.append({'label':label,'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':command,'returncode':r.returncode,'stdout_file':label+'.stdout.json','stderr_file':label+'.stderr.txt','stdout_bytes':len(r.stdout.encode()),'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stderr_bytes':len(r.stderr.encode()),'stderr_sha256':hashlib.sha256(r.stderr.encode()).hexdigest()})
 return r
for opt in (False,True):
 options=['-O'] if opt else []
 suffix='optimized' if opt else 'normal'
 for checker,receipt,guard in [('verify.py','verification.json',"ck('deliberate false guard',False)"),('independent_checks.py','independent_results.json',"ck(False,'deliberate false guard')")]:
  path=B/'repaired_diagnostics_v2'/checker
  label=checker.replace('.py','')+'_'+suffix
  r=execute(label,[sys.executable]+options+[str(path)])
  require(json.loads(r.stdout)==json.loads((path.parent/receipt).read_text()),label+' actual receipt equality')
  code="exec(compile(open("+repr(str(path))+").read(),"+repr(str(path))+",'exec'),dict(__file__="+repr(str(path))+",__name__='__main__'))"
  # Preserve globals after execution, then invoke the actual checker guard.
  code="g=dict(__file__="+repr(str(path))+",__name__='__main__');exec(compile(open("+repr(str(path))+").read(),"+repr(str(path))+",'exec'),g);exec("+repr(guard)+",g)"
  r=execute(label+'_false_guard',[sys.executable]+options+['-c',code],expected=1)
  require('deliberate false guard' in r.stderr and 'AssertionError' in r.stderr,label+' guard stayed active')
 r=execute('fresh_'+suffix,[sys.executable]+options+[str(A/'fresh_checks.py')])
 require(json.loads(r.stdout)['status']=='PASS','fresh status')
 r=execute('fresh_'+suffix+'_false_guard',[sys.executable]+options+[str(A/'fresh_checks.py'),'--negative-guard'],expected=1)
 require('RuntimeError: deliberate negative guard' in r.stderr,'fresh explicit guard stayed active')
a=json.loads((A/'fresh_normal.stdout.json').read_text());b=json.loads((A/'fresh_optimized.stdout.json').read_text())
for x in (a,b):
 x.pop('UTC');x.pop('optimized_python')
require(a==b,'normal and optimized fresh semantic results identical')
out={'status':'PASS','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'current_package':'repaired_diagnostics_v2','actual_run_count':len(runs),'normal_optimized_receipt_matches':4,'candidate_false_guards_nonzero':4,'fresh_false_guards_nonzero':2,'fresh_normal_optimized_semantic_match':True,'runs':runs}
(A/'REPLAY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='runs'},indent=2))
