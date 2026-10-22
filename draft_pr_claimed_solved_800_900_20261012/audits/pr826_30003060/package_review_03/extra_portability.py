#!/usr/bin/env python3
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, os, shutil, subprocess, sys
R=Path(__file__).resolve().parent;A=R.parent;S=json.loads((A/'PACKAGE_SEAL_R2.json').read_text());I=Path(S['assembly_tree'])/'publication_20261014/verification_package'
D=R/'replays/additional portability with spaces';D.mkdir();rows=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def test(opt):
    root=D/('relocated package '+str(opt));shutil.copytree(I,root);cwd=D/('hostile cwd '+str(opt));cwd.mkdir();marker=cwd/'imported'
    for mod in ['sitecustomize','usercustomize','json','pathlib','hashlib','zipfile','subprocess']:(cwd/(mod+'.py')).write_text('raise RuntimeError("hostile module loaded")\n')
    env=dict(os.environ,PYTHONPATH=str(cwd),PYTHONHOME=str(cwd),PYTHONOPTIMIZE='2')
    flags=[sys.executable,'-I','-S','-B']+(['-O'] if opt else [])
    p=subprocess.run(flags+[str(root/'verify_package.py'),S['index_sha256'],'--full'],cwd=cwd,env=env,capture_output=True,text=True,timeout=180)
    if p.returncode or p.stderr:raise RuntimeError(p.stderr)
    (D/('relocated full '+str(opt)+'.json')).write_text(p.stdout)
    out=D/('rebuilt outside input '+str(opt))
    b=subprocess.run(flags+[str(root/'build_verification.py'),'--from-package',str(root),'--trusted-index-sha256',S['index_sha256'],'--output-root',str(out)],cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
    if b.returncode or b.stderr or sha(out/'package_index.json')!=S['index_sha256'] or sha(out/'verification.zip')!=S['core_files'][8]['sha256']:raise RuntimeError(b.stderr or 'not exact')
    return {'optimized':opt,'relocation_full_passed':True,'relocated_root_has_spaces':True,'hostile_cwd_and_pythonhome_pythonpath_ignored':True,'builder_byte_exact':True,'full_result':json.loads(p.stdout),'builder_result':json.loads(b.stdout)}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(test,[False,True]))
out={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_passed':True,'runs':rows}
(R/'EXTRA_PORTABILITY_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_passed':True,'additional_full_runs':2,'additional_byte_exact_rebuilds':2}))
