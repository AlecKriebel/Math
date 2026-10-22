"""Portable authored audit-gate controls; preserves the 43 reviewed cases."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('isolated execution required')
import hashlib
import copy
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import warnings
import zipfile

# Run only after the complete publication inventory is authenticated.
if len(sys.argv) != 2: raise SystemExit('canonical package root required')
base = Path(sys.argv[1])
if not base.is_absolute() or str(base.resolve()) != str(base): raise SystemExit('canonical package root required')
original = base / 'audit'
archive = base / 'LEAF_SPACE_10300026_INDEPENDENT_AUDIT_SAFE.zip'
manifest = base / 'LEAF_SPACE_10300026_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'
bootstrap = base / 'LEAF_SPACE_10300026_INDEPENDENT_AUDIT_BOOTSTRAP.py'
records = []
with tempfile.TemporaryDirectory(prefix='leaf_audit_gate_') as td:
    t = Path(td)
    cwd = t / 'cwd'
    cwd.mkdir()
    hostile = t / 'hostile'
    hostile.mkdir()
    marker = t / 'MARKER'
    poison = 'from pathlib import Path\nPath(' + repr(str(marker)) + ").write_text('executed')\nraise SystemExit('SHADOW EXECUTED')\n"
    for name in ['json.py', 'pathlib.py', 'hashlib.py', 'zipfile.py', 'sitecustomize.py']:
        (hostile / name).write_text(poison)
    def run(label, expect, flags, root=original, arc=archive, mf=manifest, wd=cwd, env=None):
        p = subprocess.run([sys.executable, *flags, str(bootstrap), str(arc), str(root), str(mf)], cwd=wd, env=env, capture_output=True, text=True, timeout=20)
        output = (p.stdout+p.stderr).strip()
        good = p.returncode == 0 and json.loads(output).get('audit_metadata') == 'PASS' if expect == 'ACCEPT' else p.returncode != 0 and output.startswith('REJECT:')
        records.append({'case':label,'expected':expect,'returncode':p.returncode,'output':output,'shadow_marker_absent':not marker.exists(),'pass':good and not marker.exists()})
    for opt in [False, True]:
        flags = ['-I','-S','-B'] + (['-O'] if opt else [])
        suffix = '_optimized' if opt else '_normal'
        run('clean'+suffix,'ACCEPT',flags)
        relocated = t / ('relocated space'+suffix)
        shutil.copytree(original,relocated)
        run('relocated'+suffix,'ACCEPT',flags,root=relocated)
        env=os.environ.copy();env.update({'PYTHONPATH':str(hostile),'PYTHONHOME':str(hostile),'PYTHONSTARTUP':str(hostile/'sitecustomize.py')})
        run('hostile_environment'+suffix,'ACCEPT',flags,wd=hostile,env=env)
        mutations=['extra','missing','entrypoint','cache','shadow','member_symlink','root_symlink','wrong_root','manifest_entrypoint','archive_tamper','archive_duplicate','archive_extra','archive_symlink_member','archive_byte_mismatch','archive_missing','manifest_symlink','archive_symlink']
        for mutation in mutations:
            trial=t/(mutation+suffix);shutil.copytree(original,trial)
            root,arc,mf=trial,archive,manifest
            if mutation=='extra':(trial/'extra.txt').write_text('extra')
            elif mutation=='missing':(trial/'AUDIT_REPORT.md').unlink()
            elif mutation=='entrypoint':(trial/'verify_audit.py').write_text(poison)
            elif mutation=='cache':(trial/'__pycache__').mkdir()
            elif mutation=='shadow':(trial/'json.py').write_text(poison)
            elif mutation=='member_symlink':
                (trial/'AUDIT_REPORT.md').unlink();(trial/'AUDIT_REPORT.md').symlink_to(original/'AUDIT_REPORT.md')
            elif mutation=='root_symlink':
                root=t/('linked'+suffix);root.symlink_to(trial,target_is_directory=True)
            elif mutation=='wrong_root':root=cwd
            elif mutation=='manifest_entrypoint':
                m=json.loads(manifest.read_bytes());m['entrypoint']='replay_author.py';mf=t/(mutation+suffix+'.json');mf.write_text(json.dumps(m))
            elif mutation=='manifest_symlink':
                mf=t/(mutation+suffix+'.json');mf.symlink_to(manifest)
            elif mutation=='archive_symlink':
                arc=t/(mutation+suffix+'.zip');arc.symlink_to(archive)
            elif mutation=='archive_tamper':
                arc=t/(mutation+suffix+'.zip');arc.write_bytes(archive.read_bytes()+b'changed')
            elif mutation.startswith('archive_'):
                arc=t/(mutation+suffix+'.zip')
                with zipfile.ZipFile(archive) as zin, zipfile.ZipFile(arc,'w') as zout:
                    for i in zin.infolist():
                        if mutation=='archive_missing' and i.filename=='AUDIT_REPORT.md':continue
                        b=zin.read(i.filename)
                        i=copy.copy(i)
                        if i.filename=='AUDIT_REPORT.md':
                            if mutation=='archive_symlink_member':i.external_attr=(stat.S_IFLNK|0o777)<<16
                            elif mutation=='archive_byte_mismatch':b=b+'changed'.encode()
                        zout.writestr(i,b)
                    if mutation=='archive_extra':zout.writestr('../extra.txt','extra')
                    elif mutation=='archive_duplicate':
                        with warnings.catch_warnings():
                            warnings.simplefilter('ignore',UserWarning);zout.writestr('AUDIT_REPORT.md',zin.read('AUDIT_REPORT.md'))
                m=json.loads(manifest.read_bytes());b=arc.read_bytes();m['archive']['bytes']=len(b);m['archive']['sha256']=hashlib.sha256(b).hexdigest();mf=t/(mutation+suffix+'.json');mf.write_text(json.dumps(m))
            run(mutation+suffix,'REJECT',flags,root=root,arc=arc,mf=mf)
    run('without_isolation','REJECT',['-S','-B'])
    run('without_no_site','REJECT',['-I','-B'])
    run('without_no_bytecode','REJECT',['-I','-S'])
result={'test_count':len(records),'all_tests_pass':all(x['pass'] for x in records),'tests':records}
print(json.dumps(result,indent=2,sort_keys=True))
if not result['all_tests_pass']:raise SystemExit(1)
