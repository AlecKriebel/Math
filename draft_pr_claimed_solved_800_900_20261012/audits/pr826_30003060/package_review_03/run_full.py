#!/usr/bin/env python3
"""Fresh read-only-input replays, with disposable copies and persistent receipts."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, os, shutil, subprocess, sys, time
R=Path(__file__).resolve().parent
A=R.parent
S=json.loads((A/'PACKAGE_SEAL_R2.json').read_text())
T=Path(S['assembly_tree'])
BASE=R/'replays'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def execute(kind,opt):
    d=BASE/(kind+('_optimized' if opt else '_normal'))
    shutil.copytree(T,d)
    script=d/'verify_publication.py' if kind=='outer' else d/'publication_20261014/verification_package/verify_package.py'
    pin=S['outer_manifest_sha256'] if kind=='outer' else S['index_sha256']
    cmd=[sys.executable,'-I','-S','-B']+(['-O'] if opt else [])+[str(script),pin,'--full']
    start=time.monotonic()
    p=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=600)
    (BASE/(kind+str(opt)+'.stdout.json')).write_text(p.stdout)
    (BASE/(kind+str(opt)+'.stderr.txt')).write_text(p.stderr)
    out=json.loads(p.stdout) if p.returncode==0 else None
    if p.returncode!=0 or p.stderr or out['status']!='PASS': raise RuntimeError(p.stderr)
    return {'kind':kind,'optimized':opt,'command':cmd,'seconds':time.monotonic()-start,'returncode':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'result':out}
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        full=list(pool.map(lambda a:execute(*a),[(k,o) for k in ['portable','outer'] for o in [False,True]]))
    rebuild=[]
    for opt in [False,True]:
        out=BASE/('rebuilt with spaces '+str(opt))
        pre=T/'publication_20261014/preprint'
        cmd=[sys.executable,'-I','-S','-B']+(['-O'] if opt else [])+['build_verification.py','--from-package','../verification_package','--trusted-index-sha256',S['index_sha256'],'--output-root',str(out)]
        p=subprocess.run(cmd,cwd=pre,capture_output=True,text=True,timeout=90)
        if p.returncode or p.stderr or sha(out/'package_index.json')!=S['index_sha256'] or sha(out/'verification.zip')!=S['core_files'][8]['sha256']:raise RuntimeError(p.stderr or 'nonidentical rebuild')
        rebuild.append({'optimized':opt,'command':cmd,'returncode':p.returncode,'result':json.loads(p.stdout),'byte_exact':True})
    receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'full_runs':full,'assembled_preprint_rebuilds':rebuild,'all_passed':True}
    (R/'FULL_EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'all_passed':True,'full_runs':len(full),'byte_exact_rebuilds':len(rebuild)}))
