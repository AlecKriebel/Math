"""Read-only package replay with lossless retention of complete child outputs."""
from pathlib import Path
import base64,datetime,gzip,json,runpy,subprocess,sys,traceback
D=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
original=subprocess.run
with gzip.open(D/'package_child_outputs.jsonl.gz','wb') as log:
    def retained(*args,**kwargs):
        begin=datetime.datetime.now(datetime.timezone.utc).isoformat()
        result=original(*args,**kwargs)
        row={'utc_started':begin,'utc_finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'args':list(map(str,result.args)),'cwd':str(kwargs.get('cwd')),'returncode':result.returncode,
             'stdout_b64':base64.b64encode(result.stdout or b'').decode(),
             'stderr_b64':base64.b64encode(result.stderr or b'').decode()}
        log.write((json.dumps(row,separators=(',',':'))+'\n').encode());log.flush()
        return result
    subprocess.run=retained
    begin=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        runpy.run_path(str(D/'isolation/verification/verify_package.py'),run_name='__main__')
        status='PASS'
    except BaseException:
        status='FAIL';traceback.print_exc();raise
    finally:
        (D/'PACKAGE_REPLAY.json').write_text(json.dumps({'utc_started':begin,
            'utc_finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,
            'complete_child_outputs':'package_child_outputs.jsonl.gz','standard_python':sys.version,
            'isolation':'own extracted ZIP; all candidate originals read-only'},indent=2)+'\n')
