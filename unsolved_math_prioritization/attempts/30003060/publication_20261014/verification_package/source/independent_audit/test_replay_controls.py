#!/usr/bin/env python3
"""Pinned corrected replay and fail-closed controls. No source or dataset text is emitted."""
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

PINS = {
 'HIGHER_KOSZUL_30003060_CORRECTED_SAFE.zip':(18999,'98cff6efc620ab156ceb1876a3252d002db1dad1bc3a6c9650268d0350bfc8e3'),
 'HIGHER_KOSZUL_30003060_CORRECTED_EXTERNAL_MANIFEST.json':(2185,'d1516daeb5bd8b21c987b55a15ba1755fc3af0a4491a80669eeb50b7a20cb7df'),
 'HIGHER_KOSZUL_30003060_CORRECTED_BOOTSTRAP.py':(4442,'3aacca33222d1342bfedbd30a0348c75a45cac6414c77adfe892e8c70b1f2b28')}

def need(c,m):
    if not c:raise RuntimeError(m)

def pin(path,expected):
    b=path.read_bytes()
    need(len(b)==expected[0] and hashlib.sha256(b).hexdigest()==expected[1],'external artifact pin rejected before execution')
    return b

def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode,'use -I -S -B')
    need(len(sys.argv)==2,'pass directory of corrected external artifacts')
    root=Path(sys.argv[1]);contents={n:pin(root/n,p) for n,p in PINS.items()}
    zn,mn,bn=PINS
    controls=[]; replay=None
    with tempfile.TemporaryDirectory(prefix='koszul-review-control-') as td:
        t=Path(td); hostile=t/'hostile';hostile.mkdir(); marker=t/'marker'
        for name in ['hashlib','json','subprocess','fractions','zipfile','sitecustomize','usercustomize']:
            (hostile/(name+'.py')).write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("UNEXPECTED_IMPORT")\nraise RuntimeError("hostile import")\n')
        # Hostile direct-entrypoint and package names must not be loaded by the verified absolute command.
        (hostile/'verify_free_algebra.py').write_text('raise RuntimeError("wrong entrypoint")\n')
        (hostile/'__main__.py').write_text('raise RuntimeError("wrong directory entrypoint")\n')
        for n,b in contents.items():(t/n).write_bytes(b)
        env=dict(os.environ);env['PYTHONPATH']=str(hostile);env['PYTHONHOME']=str(hostile)
        def run(name, archive=None, manifest=None, bootstrap=None, flags=None, ok=False, diagnostic=None):
            b=bootstrap or t/bn
            # Even symlink-entrypoint tests must reference the exact approved script bytes.
            pin(b,PINS[bn])
            cmd=[sys.executable,*(flags or ['-I','-S','-B']),str(b),str(archive or t/zn),str(manifest or t/mn)]
            q=subprocess.run(cmd,cwd=hostile,env=env,capture_output=True,timeout=120)
            need((q.returncode==0)==ok,name+' unexpected result')
            if diagnostic:need(diagnostic.encode() in q.stderr,name+' diagnostic mismatch')
            need(not marker.exists(),name+' loaded hostile module')
            controls.append({'control':name,'passed':True,'expected_success':ok,'returncode':q.returncode,'diagnostic':diagnostic})
            return json.loads(q.stdout) if ok else None
        replay=run('relocated strict normal replay with hostile cwd and startup environment',ok=True)
        run('optimized corrected bootstrap fails closed',flags=['-I','-S','-B','-O'],diagnostic='optimized execution rejected')
        run('missing no-bytecode flag rejected',flags=['-I','-S'],diagnostic='run bootstrap with python -I -S -B')
        (t/'archive-link.zip').symlink_to(t/zn);run('archive symlink rejected',archive=t/'archive-link.zip',diagnostic='input paths must not use symlinks')
        (t/'manifest-link.json').symlink_to(t/mn);run('manifest symlink rejected',manifest=t/'manifest-link.json',diagnostic='input paths must not use symlinks')
        (t/'bootstrap-link.py').symlink_to(t/bn);run('bootstrap entrypoint symlink rejected',bootstrap=t/'bootstrap-link.py',diagnostic='bootstrap entrypoint must not use symlinks')
        (t/'directory-link').symlink_to(t,target_is_directory=True);run('symlinked archive ancestor rejected',archive=t/'directory-link'/zn,diagnostic='input paths must not use symlinks')
        run('symlinked entrypoint ancestor rejected',bootstrap=t/'directory-link'/bn,diagnostic='bootstrap entrypoint must not use symlinks')
        trunc=t/'truncated.zip';trunc.write_bytes(contents[zn][:-1]);run('truncated archive rejected',archive=trunc,diagnostic='archive byte count mismatch')
        changed=t/'changed.zip';b=bytearray(contents[zn]);b[len(b)//2]^=1;changed.write_bytes(b);run('same-size archive mutation rejected',archive=changed,diagnostic='archive SHA-256 mismatch')
        mm=t/'changed_manifest.json';mm.write_bytes(contents[mn]+b' ');run('external manifest mutation rejected',manifest=mm,diagnostic='external manifest pin mismatch')
        # Whole-archive pins are expected to reject these before member parsing or archive-code execution.
        for kind in ['changed checker','added entrypoint','traversal entry','symlink member','duplicate member']:
            zp=t/(kind.replace(' ','_')+'.zip')
            with zipfile.ZipFile(io.BytesIO(contents[zn])) as source,zipfile.ZipFile(zp,'w') as dest:
                for info in source.infolist():
                    data=source.read(info)
                    if kind=='changed checker' and info.filename=='verify_free_algebra.py':data+=b'\nraise RuntimeError("mutated checker")\n'
                    dest.writestr(info,data)
                if kind=='added entrypoint':dest.writestr('__main__.py',b'raise RuntimeError("wrong entrypoint")')
                if kind=='traversal entry':dest.writestr('../escape.py',b'raise RuntimeError("escape")')
                if kind=='symlink member':
                    info=zipfile.ZipInfo('link');info.create_system=3;info.external_attr=(stat.S_IFLNK|0o777)<<16;dest.writestr(info,b'verify_free_algebra.py')
                if kind=='duplicate member':
                    import warnings
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore');dest.writestr('verify_free_algebra.py',b'raise RuntimeError("duplicate")')
            run(kind+' rejected by whole-archive pin',archive=zp,diagnostic='archive byte count mismatch')
        # Updating all declared hashes cannot repair the separately pinned external manifest.
        coherent=json.loads(contents[mn]);data=(t/'changed_checker.zip').read_bytes();coherent['archive']['bytes']=len(data);coherent['archive']['sha256']=hashlib.sha256(data).hexdigest();mm.write_text(json.dumps(coherent))
        run('coherent archive and manifest substitution rejected',archive=t/'changed_checker.zip',manifest=mm,diagnostic='external manifest pin mismatch')
        # Changed bootstrap must be rejected by this outer independently pinned gate, never launched.
        wrong=t/'changed_bootstrap.py';wrong.write_bytes(contents[bn]+b'\nraise RuntimeError("wrong bootstrap")\n')
        try:pin(wrong,PINS[bn])
        except RuntimeError:controls.append({'control':'changed bootstrap rejected by outer pin before execution','passed':True,'expected_success':False,'author_or_mutated_code_executed':False})
        else:raise RuntimeError('changed bootstrap accepted')
        need(not marker.exists(),'hostile import marker')
        need(not list(t.rglob('*.pyc')),'bytecode created')
    print(json.dumps({'status':'PASS','corrected_replay':replay,'controls':controls,'control_count':len(controls),'hostile_marker_absent':True,'no_bytecode_artifacts':True,'optimized_independent_harness_supported':True,'threat_model':'Pinned reproducible execution under tested path, archive and startup mutations; not an OS sandbox or proof against hostile root/system Python.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
