"""Reproduce bounded controls and falsify repaired guards in both Python modes."""
from pathlib import Path
import subprocess,json,hashlib,datetime,os
A=Path(__file__).resolve().parent;D=A/'repaired_diagnostics_v1';O=A/'original_source_authentication_20261006/original_attempt'
E=A/'repaired_diagnostics_validation_20261006';E.mkdir(exist_ok=False)
records=[]
def require(ok,message):
    if not ok:raise RuntimeError(message)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(label,argv):
    start=now();p=subprocess.Popen(argv,cwd=D,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate()
    (E/(label+'.stdout.bin')).write_bytes(out);(E/(label+'.stderr.bin')).write_bytes(err)
    records.append({'label':label,'argv':argv,'PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest()})
    (E/'PROCESS_JOURNAL.json').write_text(json.dumps({'operator_PID':os.getpid(),'records':records},indent=2)+'\n')
    return p.returncode,out,err
probe="import ast,sys; from pathlib import Path; from collections import Counter; source=Path(sys.argv[1]); tree=ast.parse(source.read_text()); node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='ck'); scope={'C':Counter(),'checks':{}}; exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),scope); scope['ck']('injected_false_control',False); print('ACCEPTED_FALSE')"
for filename,original_receipt,count in [('verify.py','verification.json',2087),('independent_checks.py','review/independent_results.json',752)]:
    baseline=json.loads((O/original_receipt).read_text())
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal';prefix=['/usr/bin/python3','-E','-B']+(['-O'] if optimized else [])
        label=filename.replace('.py','')+'_'+mode
        rc,out,err=run(label,prefix+[str(D/filename)])
        require(rc==0,label+' failed')
        result=json.loads(out)
        require(result['status']=='PASS' and result['exact_assertions']==count and result['checks']==baseline['checks'],label+' count/check mismatch')
        require(result['artifact_sha256']==baseline['artifact_sha256'],label+' proof identity mismatch')
        rc,out,err=run(label+'_false_guard',prefix+['-c',probe,str(D/filename)])
        require(rc!=0 and not out and b'RuntimeError: injected_false_control' in err,label+' failed to reject false control')
original=json.loads((A/'original_source_authentication_20261006/ORIGINAL_BLOB_MANIFEST.json').read_text())
for pin in original['files']:
    body=Path(pin['preserved_path']).read_bytes();require(len(body)==pin['bytes'] and hashlib.sha256(body).hexdigest()==pin['sha256'],'preserved source changed')
result={'UTC':now(),'actual_operator_PID':os.getpid(),'status':'PASS_REPAIRED_BOUNDED_DIAGNOSTICS',
 'normal_and_optimized_counts':{'author':2087,'independent':752},'checks_match_original_receipts':True,
 'four_false_controls_rejected_normally_and_optimized':True,'all_original_bodies_unchanged':True,
 'mathematical_proof_changed':False,'original_budget':'1/5','new_central_proof_search_turns':0,
 'scope':'Diagnostic guard repair and finite computation reproduction; global proof requires the separate mathematical audit.'}
(E/'VERDICT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result))
