from pathlib import Path
import subprocess,shutil,json,datetime,hashlib,os,sys
root=Path(__file__).resolve().parent
paper=root.parent.parent
source=paper/'sources/published-source'
scratch=root/'replay-copy'
if scratch.exists():raise RuntimeError('refuse to overwrite prior replay')
shutil.copytree(source,scratch)
out=root/'replays';out.mkdir(exist_ok=True)
python=Path('/Users/alec/Documents/Math/.venv/bin/python')
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
jobs=[('verify-normal',['python3','-B','verification/verify_all.py']),('verify-optimized',['python3','-B','-O','verification/verify_all.py']),('self-test-normal',['python3','-B','verification/self_test.py']),('self-test-optimized',['python3','-B','-O','verification/self_test.py']),('optional-matrix',[str(python),'-B','verification/optional_matrix_diagnostics.py']),('optional-optimized-rejection',[str(python),'-B','-O','verification/optional_matrix_diagnostics.py'])]
receipts=[]
for name,cmd in jobs:
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.run(cmd,cwd=scratch,env=env,capture_output=True,timeout=240)
    (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
    r={'name':name,'command':cmd,'cwd':str(scratch),'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()}
    if name=='optional-optimized-rejection':
        r['expected_rejection']=p.returncode!=0 and b'optional matrix diagnostics require normal Python' in p.stderr
        if not r['expected_rejection']:raise RuntimeError(r)
    else:
        if p.returncode!=0 or p.stderr:raise RuntimeError(r)
        data=json.loads(p.stdout)
        r['status']=data.get('status','completed')
        if 'check_count' in data:r['check_count']=data['check_count']
    receipts.append(r)
    print(json.dumps(r),flush=True)
if (out/'verify-normal.stdout').read_bytes()!=(out/'verify-optimized.stdout').read_bytes():raise RuntimeError('mode mismatch')
if (out/'self-test-normal.stdout').read_bytes()!=(out/'self-test-optimized.stdout').read_bytes():raise RuntimeError('self-test mode mismatch')
(root/'replay-receipts.json').write_text(json.dumps({'status':'PASS','source_code_unmodified':True,'isolated_copy':str(scratch),'receipts':receipts},indent=2)+'\n')
