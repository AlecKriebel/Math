#!/usr/bin/env python3
"""Fresh structural negative controls; all altered copies remain in own folder."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess

R=Path(__file__).resolve().parents[1]
P=R/'evidence/candidate_full/archive'
G=R/'evidence/guard_controls'
G.mkdir(parents=True,exist_ok=True)
python='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def snapshot():
    return {str(p.relative_to(P)):(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mode) for p in P.rglob('*') if p.is_file()}
before=snapshot()
tests=[]
for name,message in [('body','File body/mode mismatch'),('missing','Complete file inventory mismatch'),('extra','Complete file inventory mismatch'),('file_mode','File body/mode mismatch'),('directory_mode','Directory mode/inventory mismatch'),('symlink','Symlink:')]:
    dest=G/name
    assert not dest.exists(),name+' would overwrite evidence'
    shutil.copytree(P,dest)
    if name=='body':
        with (dest/'README.md').open('ab') as f:f.write(b'\nindependent deliberately incorrect body control\n')
    elif name=='missing':(dest/'README.md').unlink()
    elif name=='extra':(dest/'unexpected.txt').write_text('independent extra-file control\n')
    elif name=='file_mode':(dest/'README.md').chmod(0o600)
    elif name=='directory_mode':(dest/'programs').chmod(0o700)
    elif name=='symlink':
        (dest/'README.md').unlink()
        (dest/'README.md').symlink_to(P/'README.md')
    receipts=G/(name+'_actual_receipt')
    receipts.mkdir()
    argv=[python,'-B',str(dest/'verify.py'),'--suite','arithmetic']
    (receipts/'argv.json').write_text(json.dumps(dict(argv=argv,cwd=str(dest)),indent=2)+'\n')
    start=subprocess.check_output(['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ']).decode().strip()
    (receipts/'native_start.txt').write_text(start+'\n')
    run=subprocess.run(argv,cwd=dest,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    (receipts/'stdout.bin').write_bytes(run.stdout)
    (receipts/'stderr.bin').write_bytes(run.stderr)
    end=subprocess.check_output(['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ']).decode().strip()
    (receipts/'native_end.txt').write_text(end+'\n')
    record=dict(name=name,argv=argv,start_native_utc=start,end_native_utc=end,exit=run.returncode,stdout_bytes=len(run.stdout),stderr_bytes=len(run.stderr),expected_error=message)
    (receipts/'record.json').write_text(json.dumps(record,indent=2)+'\n')
    assert run.returncode==1 and not run.stdout and message.encode() in run.stderr,record
    tests.append(record)
    if name=='symlink':
        # Actual rejection remains captured above. Restore this disposable copy
        # afterward so final namespace inventory contains only regular bodies.
        (dest/'README.md').unlink()
        shutil.copy2(P/'README.md',dest/'README.md')
        (receipts/'post_run_cleanup.txt').write_text('After actual rejection, own disposable symlink was removed and README restored from own untouched archive. This is cleanup, not the tested pre-run state.\n')
assert snapshot()==before,'Original own archive changed'
print(json.dumps(dict(status='PASS',negative_controls=6,actual_results=tests,original_archive_unchanged=True),indent=2))
