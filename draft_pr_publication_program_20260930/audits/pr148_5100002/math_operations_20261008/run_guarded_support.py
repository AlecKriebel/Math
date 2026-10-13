"""Run immutable guarded sources in fresh output folders with complete closure."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
from fractions import Fraction
import argparse, json, os, shutil, signal, subprocess, sys, time
A=Path(__file__).resolve().parent.parent
D=A/'guarded_support_v1'
def require(v,msg):
    if not v: raise RuntimeError(msg)
def utc():return datetime.now(timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
parser=argparse.ArgumentParser();parser.add_argument('--sympy-python',required=True);parser.add_argument('--run-name',required=True);args=parser.parse_args()
require(args.run_name.isalnum() or all(c.isalnum() or c=='_' for c in args.run_name),'run name')
manifest=json.loads((D/'SOURCE_MANIFEST.json').read_bytes())
for member in manifest['members']:
    p=D/member['path'];require(not p.is_symlink() and pin(p)=={k:member[k] for k in ('bytes','sha256')},'reviewed source changed')
run=A/'math_operations_20261008/private'/args.run_name;run.mkdir(parents=True,exist_ok=False)
records=[]
for mode in ('normal','optimized'):
    for name,script,output in [('author','verify.py','verification.json'),('inherited','independent_checks.py','independent_results.json'),('analytic','check_analytic_family.py',None),('geometry','independent_geometry.py','independent_geometry_results.json')]:
        label=name+'_'+mode;dest=run/label;dest.mkdir();work=dest/'work';shutil.copytree(D/name,work)
        if output:require(not (work/output).exists(),'fresh output must be absent')
        executable=args.sympy_python if name=='author' else sys.executable
        argv=[executable,'-E']+([] if name=='author' else ['-S'])+['-B','-P']+(['-O'] if mode=='optimized' else [])+[str(work/script)]
        started=utc();reason=None;begin=time.monotonic()
        with (dest/'stdout.txt').open('xb') as out,(dest/'stderr.txt').open('xb') as err:
            p=subprocess.Popen(argv,cwd=work,stdout=out,stderr=err,start_new_session=True);pid=p.pid;pgid=os.getpgid(pid)
            while p.poll() is None:
                if time.monotonic()-begin>60:reason='timeout';break
                if out.tell()+err.tell()>524288:reason='output cap';break
                time.sleep(.025)
            if reason:
                os.killpg(pgid,signal.SIGTERM)
                try:p.wait(timeout=2)
                except subprocess.TimeoutExpired:os.killpg(pgid,signal.SIGKILL)
            rc=p.wait()
        try:os.killpg(pgid,0);absent=False
        except ProcessLookupError:absent=True
        r={'label':label,'argv':argv,'actual_PID':pid,'PGID':pgid,'start_UTC':started,'end_UTC':utc(),'exit_code':rc,'child_reaped':p.returncode is not None,'process_group_absent':absent,'termination_reason':reason,'stdout':pin(dest/'stdout.txt'),'stderr':pin(dest/'stderr.txt')}
        (dest/'PROCESS_RECEIPT.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
        require(reason is None and absent and rc==0,'failed or unclosed current verification')
        raw=(dest/'stdout.txt').read_bytes();obj=json.loads(raw)
        if name in ('author','inherited'):
            fresh=(work/output).read_bytes();require(raw==fresh,'current stdout and fresh result differ')
            expected=json.loads((work/('expected_verification.json' if name=='author' else 'expected_independent_results.json')).read_bytes())
            comparison=dict(obj)
            if name=='author':
                require(obj['verifier_sha256']==pin(work/script)['sha256'],'actual guarded verifier source binding')
                comparison['verifier_sha256']=expected['verifier_sha256']
            require(comparison==expected,'fresh result differs from pinned expected mathematics')
            require(obj['status']==('PASS_EXACT_SIX_PERIOD_COUNTEREXAMPLE' if name=='author' else 'PASS'),'scientific status')
        elif name=='analytic':
            require(obj['status']=='PASS' and obj['return_map_polynomial_identity'] is True,'analytic certificate')
            require(obj['H']['k108']=='11664/3125' and obj['V']['k108']=='3645/1024' and obj['exact_k108_difference']=='553311/3200000','analytic values')
        else:
            fresh=json.loads((work/output).read_bytes())
            require(fresh['PH']['k108']==obj['PH_k108']=='11664/3125' and fresh['PV']['k108']==obj['PV_k108']=='3645/1024','geometry values')
            require(fresh['exact_k108_difference']==obj['difference']=='553311/3200000','geometry difference')
        r['fresh_output_and_scientific_data_verified']=True;records.append(r)
        (dest/'PROCESS_RECEIPT.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
for member in manifest['members']:
    require(pin(D/member['path'])=={k:member[k] for k in ('bytes','sha256')},'source changed during verification')
receipt={'schema':'pr148-root-guarded-support-reproduction/v1','UTC':utc(),'actual_ROOT_PID':os.getpid(),'status':'PASS_GUARDED_SUPPORT_FRESH_CLOSED_REPRODUCTION','source_manifest':pin(D/'SOURCE_MANIFEST.json'),'children':records,'all_obtained_children_complete':True,'original_effort':'1/5','new_central_proof_search_turns':0,'mathematical_acceptance':None,'priority_acceptance':None,'publication_acceptance':None}
(run/'RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':receipt['status'],'closed_children':len(records),'receipt_path':str(run/'RECEIPT.json'), 'receipt':pin(run/'RECEIPT.json')}))
