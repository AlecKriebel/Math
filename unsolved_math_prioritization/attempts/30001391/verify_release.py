#!/usr/bin/env python3
"""Strict final-layout integrity and finite replay checks; not a theorem prover."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
AUTHOR='63df37afcb5592e0bde27cf8e66383025710e5fcc685d38afb954a37275d48b8'
AUDIT='7a79ca94f1d54e59e13c67720fb1f4a3749e529d3d334395b46fb0e7cc320ebe'

def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def run(cmd):
    r=subprocess.run([sys.executable,'-B',*cmd],cwd=ROOT,capture_output=True,text=True)
    need(r.returncode==0,'failed: '+str(cmd)+' '+r.stdout+' '+r.stderr)
    return json.loads(r.stdout)
def verify():
    need(not (ROOT/'RELEASE_MANIFEST.json').is_symlink(),'manifest symlink')
    m=json.loads((ROOT/'RELEASE_MANIFEST.json').read_text())
    need(m['problem_id']==30001391,'wrong problem')
    actual=set();dirs=set()
    for p in ROOT.rglob('*'):
        need(not p.is_symlink(),'symlink: '+str(p))
        n=p.relative_to(ROOT).as_posix()
        if p.is_dir():dirs.add(n)
        elif p.is_file():actual.add(n)
        else:raise ValueError('nonregular entry: '+n)
    need(dirs=={'audit','submission'},'unexpected directory set')
    expected=set(m['files'])|{'RELEASE_MANIFEST.json'}
    need(actual==expected,'exact file-set mismatch')
    for n,r in m['files'].items():
        need(n==Path(n).as_posix() and not Path(n).is_absolute() and '..' not in Path(n).parts,'unsafe manifest path')
        b=(ROOT/n).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'mismatch: '+n)
    need(sha((ROOT/'submission/SHA256SUMS.json').read_bytes())==AUTHOR,'author binding mismatch')
    need(sha((ROOT/'audit/AUDIT_MANIFEST.json').read_bytes())==AUDIT,'audit binding mismatch')
    am=run(['submission/verify_manifest.py']);ar=run(['submission/verify.py'])
    need(ar==json.loads((ROOT/'submission/CONTROL_RESULTS.json').read_text()),'author replay differs')
    im=run(['audit/verify_audit.py','submission']);ir=run(['audit/independent_checks.py','submission'])
    need(ir==json.loads((ROOT/'audit/INDEPENDENT_CONTROL_RESULTS.json').read_text()),'audit replay differs')
    return {'result':'PASS','release_payload_files':len(m['files']),'author_payload_files':am['file_count'],'audit_payload_files':im['audit_file_count'],'author_replay_exact':True,'independent_replay_exact':True,'author_manifest_sha256':AUTHOR,'audit_manifest_sha256':AUDIT,'limits':'Integrity and finite checks only; no formal theorem, novelty, or unrestricted-period certification.'}
if __name__=='__main__':
    try:print(json.dumps(verify(),indent=2,sort_keys=True))
    except Exception as e:print(json.dumps({'result':'FAIL','error':str(e)},indent=2));sys.exit(1)
