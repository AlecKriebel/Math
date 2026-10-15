#!/usr/bin/env python3
"""Run normal, optimized and deliberately failing diagnostics with custody receipts."""
from pathlib import Path
import ast,datetime,hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
RECEIPTS=HERE/'guard_control_receipts'

def require(condition,message):
    if not condition:raise RuntimeError(message)

def sha(data):return hashlib.sha256(data).hexdigest()

def capture(argv,name):
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc=subprocess.Popen(argv,cwd=HERE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    pid=proc.pid
    stdout,stderr=proc.communicate()
    ended=datetime.datetime.now(datetime.timezone.utc).isoformat()
    stdout_path=RECEIPTS/(name+'.stdout.bin');stdout_path.write_bytes(stdout)
    stderr_path=RECEIPTS/(name+'.stderr.bin');stderr_path.write_bytes(stderr)
    return {'name':name,'argv':argv,'cwd':str(HERE),'actual_pid':pid,'utc_start':started,'utc_end':ended,'exit_code':proc.returncode,'stdout_path':str(stdout_path),'stdout_bytes':len(stdout),'stdout_sha256':sha(stdout),'stderr_path':str(stderr_path),'stderr_bytes':len(stderr),'stderr_sha256':sha(stderr)}

def main():
    RECEIPTS.mkdir(exist_ok=True)
    records=[];parity={}
    for checker,result_name in [('check_boundaries.py','BOUNDARY_RESULTS.json'),('inspect_sourcepair.py','SOURCEPAIR_CHECK.json')]:
        path=HERE/checker
        source=path.read_bytes()
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(source))),checker+' retains executable assert')
        positive_results=[]
        for optimization,label in [([], 'normal'),(['-O'],'optimized')]:
            name=path.stem+'.'+label
            receipt=capture([sys.executable,*optimization,str(path)],name)
            receipt['checker_sha256']=sha(source);receipt['expected_outcome']='success'
            records.append(receipt)
            require(receipt['exit_code']==0,name+' failed')
            result=json.loads((HERE/result_name).read_text())
            if checker=='check_boundaries.py':require(result['all_pass'] is True,'Boundary result not passed')
            else:require(result['source_record_submitted_equals_raw_equals_sql'] is True and result['normalized_report_equals_sql'] is True,'Sourcepair result not passed')
            snapshot=RECEIPTS/(name+'.result.json');snapshot.write_text(json.dumps(result,indent=2)+'\n')
            receipt['result_snapshot_path']=str(snapshot);receipt['result_snapshot_sha256']=sha(snapshot.read_bytes())
            positive_results.append({k:v for k,v in result.items() if k!='checked_at_utc'})
        require(positive_results[0]==positive_results[1],checker+' normal/-O semantic results differ')
        parity[checker]=True
        for optimization,label in [([], 'normal'),(['-O'],'optimized')]:
            name=path.stem+'.'+label+'.known_false_guard'
            receipt=capture([sys.executable,*optimization,str(path),'--known-false-guard'],name)
            receipt['checker_sha256']=sha(source);receipt['expected_outcome']='failure with known-false diagnostic'
            records.append(receipt)
            require(receipt['exit_code']!=0,name+' incorrectly passed')
            require(b'Known-false guard control must fail' in Path(receipt['stderr_path']).read_bytes(),name+' did not reach explicit guard')
    result={'schema':'pr108-explicit-guard-control-receipts/v1','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_pid':__import__('os').getpid(),'executable_assert_nodes_remaining':0,'normal_optimized_semantic_parity':parity,'success_runs':4,'known_false_guard_failure_runs':4,'all_controls_pass':True,'records':records,'new_central_proof_search_turns':0,'scope':'Diagnostic trust repair only; original reduction and source inputs unchanged.'}
    (HERE/'GUARD_CONTROL_RECEIPTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
if __name__=='__main__':main()
