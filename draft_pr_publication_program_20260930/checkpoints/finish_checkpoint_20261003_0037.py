"""Finish only the already enumerated owned checkpoint after ignored-path rejection.

Git partially staged allowed paths, then refused explicitly listed audit-local
tmp capture directories. Retain the failed source/capture. Force-add only the
exact enumerated own files, never any native cache or foreign project file.
"""
from pathlib import Path
import json
import hashlib
import subprocess
import datetime as dt
import os

P=Path(__file__).resolve().parents[1];R=P.parent;A=P/'audits/pr44_2912'


def main():
    assert __debug__
    ck=P/'checkpoints/CHECKPOINT_20261003_0037.json'
    manifest=json.loads(ck.read_bytes())
    assert manifest['main_before']=='c61dc0cb572de281b871264819c8b80d647d0373'
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==manifest['main_before']
    allowed={row['path']for row in manifest['owned_files']}
    for row in manifest['owned_files']:
        p=R/row['path'];assert p.is_file() and not p.is_symlink()
        raw=p.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    allowed.add(ck.relative_to(R).as_posix())
    allowed.add(Path(__file__).relative_to(R).as_posix())
    # Completed actual failed stage capture; preserve all four full members.
    old=A/'root_checkpoint_0037_actual_capture'
    assert {p.name for p in old.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
    failure=json.loads((old/'CAPTURE.json').read_bytes());assert failure['actual_execution'] is True and failure['exit_code']==1
    for p in old.iterdir():allowed.add(p.relative_to(R).as_posix())
    currently=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0')
    assert {n for n in currently if n}.issubset(allowed)
    for name in allowed:
        assert name.startswith('draft_pr_publication_program_20260930/')
        p=R/name;assert p.is_file() and not p.is_symlink() and p.stat().st_size<=100*1024*1024
        if '/tmp/'in name:
            assert '/audits/pr42_2233/tmp/root_pr42_current_build_'in name or '/audits/pr43_30004386/tmp/root_pr43_current_'in name
    subprocess.run(['git','add','-f','--',*sorted(allowed)],cwd=R,check=True)
    staged=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0')
    assert {n for n in staged if n}.issubset(allowed)
    for name in filter(None,staged):
        assert subprocess.check_output(['git','show',':'+name],cwd=R)==(R/name).read_bytes()
    result={'status':'PASS_EXACT_OWNED_CHECKPOINT_REPAIRED_AND_STAGED','utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'actual_pid':os.getpid(),'prior_actual_failed_stage_pid':failure['pid'],
        'reason':'Explicit ignored audit-local own capture paths required force-add; no scientific or publication defect.',
        'staged_changed_paths':len([n for n in staged if n]),'foreign_staged_paths':0,
        'completed_count':31,'total':180,'program_completion_estimate_percent':31/180*100}
    out=P/'checkpoints/CHECKPOINT_20261003_0037_STAGE_REPAIR.json'
    with out.open('x')as f:json.dump(result,f,indent=2);f.write('\n')
    subprocess.run(['git','add','--',out.relative_to(R).as_posix()],cwd=R,check=True)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
