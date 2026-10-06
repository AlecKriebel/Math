from pathlib import Path
import subprocess,json,hashlib,datetime,os
A=Path(__file__).resolve().parent;V=A/'credited_verification_candidate_v2';D=A/'root_credited_candidate_reproduction_20261006';D.mkdir(exist_ok=False);records=[]
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
proof=(V/'CANDIDATE.md').read_bytes();outputs={}
for kind,script,count in [('author','verify.py',87),('independent','review/independent_checks.py',89)]:
    for optimized in [False,True]:
        label=kind+('_O' if optimized else '_normal');case=D/label;case.mkdir();code=case/Path(script).name;code.write_bytes((V/script).read_bytes())
        target=case/'CANDIDATE.md' if kind=='author' else case/'author_replay/CANDIDATE.md';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(proof)
        args=['/usr/bin/python3','-E','-B']+(['-O'] if optimized else [])+[str(code)];start=now();p=subprocess.Popen(args,cwd=case,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
        (case/'stdout.bin').write_bytes(out);(case/'stderr.bin').write_bytes(err)
        r={'label':label,'argv':args,'PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'source_sha256':sha(code),'candidate_sha256':sha(target),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()};dump(case/'execution.json',r);records.append(r);dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records})
        require(p.returncode==0,'current reproduction failed '+label);result=json.loads(out);require(result['status']=='PASS' and result['assertions']==count and result['candidate_sha256']==sha(V/'CANDIDATE.md'),'current receipt binding')
        if kind=='author':require(result['verifier_sha256']==sha(code),'current author source binding')
        outputs[label]=out
for kind in ['author','independent']:require(outputs[kind+'_normal']==outputs[kind+'_O'],'ordinary optimized byte equality')
x={'schema':'pr97-current-repaired-candidate-root-reproduction/v1','UTC':now(),'actual_operator_PID':os.getpid(),'passed':True,'runs':records,'author_diagnostics':87,'independent_diagnostics':89,'current_candidate_sha256':sha(V/'CANDIDATE.md'),'normal_optimized_JSON_byte_identical':True,'false_controls':'Fresh pencil adversary authenticated exact adopted guard bytes and already rejected false controls in both modes; not rerun without a new source change.','global_theorem_inputs_not_reproved_by_diagnostics':True,'priority_clearance':False,'publication_clearance':False,'new_central_proof_search_turns':0}
dump(D/'RESULT.json',x);(V/'current_author_verification.json').write_bytes(outputs['author_normal']);(V/'review/current_independent_results.json').write_bytes(outputs['independent_normal']);print(json.dumps({k:v for k,v in x.items() if k!='runs'}))
