#!/usr/bin/env python3
"""Fresh fail-closed replay controls. Run from a trusted directory with -I -S."""
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit('Use python -I -S')
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import zipfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def suite(archive, manifest, bootstrap, pins, expected_checks=914):
    paths=list(map(lambda p:Path(p).absolute(),(archive,manifest,bootstrap)))
    archive,manifest,bootstrap=paths
    for p,pin in zip(paths,pins):
        if not stat.S_ISREG(p.lstat().st_mode) or sha(p.read_bytes())!=pin:
            raise RuntimeError('Input pin mismatch: '+p.name)
    expected=json.loads(manifest.read_text())['files']
    with zipfile.ZipFile(archive) as z:
        infos=z.infolist()
        if len(infos)!=len(expected) or {p.filename for p in infos}!=set(expected):
            raise RuntimeError('Archive inventory mismatch')
        payloads={}
        for info in infos:
            name=info.filename
            if Path(name).name!=name or not stat.S_ISREG(info.external_attr>>16):
                raise RuntimeError('Unsafe archive member')
            data=z.read(info)
            if len(data)!=expected[name]['bytes'] or sha(data)!=expected[name]['sha256']:
                raise RuntimeError('Archive member mismatch')
            payloads[name]=data
    results=[]
    with tempfile.TemporaryDirectory(prefix='connected-sum-audit-') as tmp:
        home=Path(tmp)
        counter=0
        def fresh():
            nonlocal counter
            counter+=1
            p=home/('case-'+str(counter));p.mkdir()
            for name,data in payloads.items():(p/name).write_bytes(data)
            return p
        def run(name,root,good,optimized=False,flags=None,cwd=None,man=None,env=None):
            command=[sys.executable,*(flags if flags is not None else ['-I','-S']),str(bootstrap),str(root),str(man or manifest)]
            if optimized:command.append('--optimized')
            r=subprocess.run(command,cwd=cwd or home,capture_output=True,text=True,timeout=30,env=env)
            if good:
                try:d=json.loads(r.stdout)
                except Exception as e:raise RuntimeError(name+': invalid output') from e
                passed=r.returncode==0 and d.get('result')=='PASS' and d.get('checks')==expected_checks
            else:
                passed=r.returncode!=0 and 'UNTRUSTED_ENTRYPOINT_EXECUTED' not in r.stdout and '"result": "PASS"' not in r.stdout
            record={'test':name,'expected_acceptance':good,'returncode':r.returncode,'result':'PASS' if passed else 'FAIL','stdout_sha256':sha(r.stdout.encode()),'stderr_sha256':sha(r.stderr.encode())}
            if good:record['diagnostic_checks']=d['checks']
            else:record['rejection']=(r.stderr or r.stdout).strip().splitlines()[-1][:200]
            results.append(record)
            if not passed:raise RuntimeError(json.dumps(record))
        root=fresh();run('normal isolated replay',root,True)
        run('optimized checker replay',root,True,optimized=True)
        relocated=home/'relocated'/'different';relocated.parent.mkdir();shutil.copytree(root,relocated)
        run('relocated package',relocated,True)
        run('relocated optimized package',relocated,True,optimized=True)
        for name in ['json.py','hashlib.py','subprocess.py','pathlib.py','itertools.py','math.py','sitecustomize.py','usercustomize.py','verify_math.pyc']:
            p=fresh();(p/name).write_text('raise RuntimeError("UNTRUSTED_ENTRYPOINT_EXECUTED")\n');run('reject extra '+name,p,False)
        for name in ['__pycache__','empty_directory']:
            p=fresh();(p/name).mkdir();run('reject extra directory '+name,p,False)
        p=fresh();(p/'PROOF.md').unlink();run('reject missing member',p,False)
        p=fresh();(p/'PROOF.md').write_bytes(payloads['PROOF.md']+b'\n');run('reject changed proof',p,False)
        p=fresh();(p/'verify_math.py').write_text('print("UNTRUSTED_ENTRYPOINT_EXECUTED")\n');run('reject replaced entrypoint before execution',p,False)
        p=fresh();(p/'verify_math.py').unlink();(p/'verify_math.py').symlink_to(root/'verify_math.py');run('reject authentic entrypoint symlink',p,False)
        p=fresh();(p/'PROOF.md').unlink();(p/'PROOF.md').mkdir();run('reject member directory',p,False)
        p=fresh();(p/'PROOF.md').unlink();os.mkfifo(p/'PROOF.md');run('reject member FIFO',p,False)
        symlink=home/'root-symlink';symlink.symlink_to(root,target_is_directory=True);run('reject root symlink',symlink,False)
        run('reject root regular file',root/'PROOF.md',False)
        run('reject missing root',home/'missing-root',False)
        changed=home/'changed-manifest.json';changed.write_bytes(manifest.read_bytes()+b'\n');run('reject modified external manifest',root,False,man=changed)
        symbolic=home/'manifest-symlink.json';symbolic.symlink_to(manifest);run('reject manifest symlink',root,False,man=symbolic)
        run('reject nonisolated bootstrap',root,False,flags=['-S'])
        run('reject site-enabled bootstrap',root,False,flags=['-I'])
        hostile=home/'hostile';hostile.mkdir()
        for name in ['json.py','hashlib.py','subprocess.py','pathlib.py','itertools.py','math.py','sitecustomize.py','usercustomize.py']:
            (hostile/name).write_text('raise RuntimeError("UNTRUSTED_ENTRYPOINT_EXECUTED")\n')
        env=dict(os.environ);env['PYTHONPATH']=str(hostile)
        run('hostile cwd and PYTHONPATH ignored',root,True,cwd=hostile,env=env)
        run('hostile cwd optimized replay',root,True,optimized=True,cwd=hostile,env=env)
    return {'archive_sha256':pins[0],'manifest_sha256':pins[1],'bootstrap_sha256':pins[2],'member_count':len(expected),'tests':results,'result':'PASS'}


if __name__=='__main__':
    if len(sys.argv) not in (7,8):raise SystemExit('usage: archive manifest bootstrap archive_sha manifest_sha bootstrap_sha [expected_checks]')
    expected_checks=int(sys.argv[7]) if len(sys.argv)==8 else 914
    print(json.dumps(suite(*sys.argv[1:4],sys.argv[4:7],expected_checks),indent=2,sort_keys=True))
