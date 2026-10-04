"""Actual capture of independent authored review programs, never proposed code."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

H = Path(__file__).resolve().parent
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(x): return hashlib.sha256(x).hexdigest()
def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0')
    name, script = sys.argv[1:3]
    assert name and '/' not in name and name not in ('.', '..')
    p = Path(script)
    assert p.parent == H and p.is_file() and not p.is_symlink()
    source = p.read_bytes()
    d = H / name
    d.mkdir(mode=0o700)
    (d/'PRELAUNCH_SOURCE.py').write_bytes(source)
    (d/'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
    argv = ['/usr/bin/python3', '-B', str(p), *sys.argv[3:]]
    record = {'schema':'PR43_NEW_ACCEPTANCE_SOURCE_ADVERSARY_ACTUAL_CAPTURE_v1',
              'argv':argv,'cwd':str(H),'started_utc':now(),'actual_execution':False,
              'completed':False,'pid':None,'prelaunch_source_sha256':sha(source),
              'stdin_supplied':False,'proposed_code_executed':False}
    proc = subprocess.Popen(argv, cwd=H, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            env=dict(os.environ, PYTHONOPTIMIZE='0', PYTHONDONTWRITEBYTECODE='1'))
    record.update(actual_execution=True, pid=proc.pid)
    out, err = proc.communicate()
    record.update(completed=True,exit_code=proc.returncode,finished_utc=now(),
                  source_unchanged=p.read_bytes()==source)
    for channel, raw in [('stdout',out),('stderr',err)]:
        with (d/(channel+'.bin')).open('xb') as f:
            f.write(raw);f.flush();os.fsync(f.fileno())
        record[channel]={'path':channel+'.bin','bytes':len(raw),'sha256':sha(raw)}
    with (d/'CAPTURE.json').open('x') as f:
        json.dump(record,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    if p.name=='close_review.py' and proc.returncode==0:
        # The actual child is finished and all five capture members now exist.
        # Freeze this exact family only; no inputs outside H are copied or changed.
        rows=[];dirs=[]
        for file in sorted(H.rglob('*')):
            assert not file.is_symlink() and (file.is_file() or file.is_dir())
            if file.is_dir():dirs.append(file.relative_to(H).as_posix())
            else:
                assert file.name!='SELF_MANIFEST.json' or file.parent!=H
                file.chmod(0o444);raw=file.read_bytes()
                rows.append({'path':file.relative_to(H).as_posix(),'bytes':len(raw),'sha256':sha(raw),'mode':'0444','classification':'own review source/report/private fixture or attributed actual project-evidence capture','novelty_claim':False})
        result={'schema':'PR43_NEW_ACCEPTANCE_SOURCE_ADVERSARY_SELF_ONLY_CLOSURE_v1','created_utc':now(),'actual_closure_parent_pid':os.getpid(),'actual_closure_child_pid':proc.pid,'files_count':len(rows),'files':rows,'self_excluded':['SELF_MANIFEST.json'],'mode':'0444','directories':dirs,'preparation_manifest_sha256':'4161032794d175f8e0cfc3b62b3d1567f172ca93abe590f43ef81576d6cd20f9','external_inputs_individually_excluded_manifest':{'path':'EXTERNAL_INPUTS_INDIVIDUALLY_EXCLUDED.json','bytes':len((H/'EXTERNAL_INPUTS_INDIVIDUALLY_EXCLUDED.json').read_bytes()),'sha256':sha((H/'EXTERNAL_INPUTS_INDIVIDUALLY_EXCLUDED.json').read_bytes())},'external_full_bodies_copied':False,'proposed_sources_imported_compiled_executed':False,'future_ROOT_or_repaired_source_approval_certified':False,'mandatory_defects':['M1','M2'],'review_completion_percent':100,'new_discovery_percent':0}
        mf=H/'SELF_MANIFEST.json'
        with mf.open('x')as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        mf.chmod(0o444)
        print(json.dumps({'status':'CLOSED_SOURCE_REVIEW_REQUIRES_TWO_REPAIRS','files_count':len(rows),'manifest_sha256':sha(mf.read_bytes()),'actual_parent_pid':os.getpid(),'actual_child_pid':proc.pid,'future_execution_approved':False},indent=2))
    print(json.dumps(record,indent=2))
    return proc.returncode
if __name__=='__main__':sys.exit(main())
