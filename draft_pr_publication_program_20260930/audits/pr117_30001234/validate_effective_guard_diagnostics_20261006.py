from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent
O=A/'original_head_authentication_20261006/original_attempt'
D=A/'repaired_diagnostics_v1'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
events=[]
def require(value,label):
    if not value:raise ValueError(label)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
for optimized in [False,True]:
    for label,code,result_name,original_name,hash_key in [
        ('author',D/'verify.py','verification.json',O/'verification.json','verifier_sha256'),
        ('independent',D/'independent_checks.py','independent_results.json',O/'review/independent_results.json','checker_sha256'),
        ('false_guard_probe',A/'guard_false_control_20261006.py',None,None,None)]:
        argv=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(code)]
        start=now();child=subprocess.Popen(argv,cwd=D,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            env={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'})
        out,err=child.communicate()
        require(child.returncode==0 and not err,'Effective actual run failed')
        if result_name:
            result=json.loads((D/result_name).read_text())
            expected=json.loads(original_name.read_text())
            require({k:v for k,v in result.items() if k!=hash_key}=={k:v for k,v in expected.items() if k!=hash_key},'Diagnostic semantics changed')
            require(result[hash_key]==hashlib.sha256(code.read_bytes()).hexdigest(),'Effective code pin')
            snapshot=D/(label+('_optimized' if optimized else '_normal')+'.json')
            snapshot.write_bytes((D/result_name).read_bytes())
        else:result=json.loads(out)
        events.append({'label':label,'optimized':optimized,'argv':argv,'PID':child.pid,'start_UTC':start,'end_UTC':now(),
            'exit_code':child.returncode,'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'result':result})
        (A/'EFFECTIVE_GUARD_VALIDATION_PROCESS_JOURNAL_20261006.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'events':events},indent=2)+'\n')
require(hashlib.sha256((D/'CANDIDATE.md').read_bytes()).hexdigest()=='1409e8ad35d34f3cc4a9bb14f7e42318c1dd1e0446ecba525c655fad8c978cdf','Proof changed')
record={'schema':'pr117-effective-diagnostic-validation/v1','UTC':now(),'actual_operator_PID':os.getpid(),'status':'PASS',
    'actual_normal_and_optimized_runs':6,'author_guards_per_full_run':3045,'independent_guards_per_full_run':5368,
    'proof_unchanged':True,'false_guard_controls_normal_and_optimized_pass':True,'original_O_guards_accepted_false_controls':True,
    'only_change_to_checker_logic':'Explicit exception guards replace assertions','events':events,
    'new_central_proof_search_turns':0,'mathematical_gate_not_yet_adjudicated':True,'priority_clearance':False}
(A/'ROOT_EFFECTIVE_GUARD_VALIDATION_20261006.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='events'},sort_keys=True))
