"""Preparation-only rejections against the three actual successful output directories."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
sys.dont_write_bytecode = True
base = Path(__file__).resolve().parent.parent
root = base/'publicfiles'
sys.path.insert(0,str(root/'support'))
from safe_output import fresh_output, write_new, json_bytes, Journal
outdir = fresh_output(str(base/'private/actual_reuse_controls'), root)
custody = Journal(outdir/'PROCESS_RECEIPTS.json')

def sha(data): return hashlib.sha256(data).hexdigest()
def inventory(folder):
    return {str(p.relative_to(folder)): (dict(link=os.readlink(p)) if p.is_symlink()
            else dict(sha256=sha(p.read_bytes()),bytes=p.stat().st_size))
            for p in folder.rglob('*') if p.is_symlink() or p.is_file()}

records = []
root_before = inventory(root)
for script, prior in [('run_diagnostics.py','diagnostics_current'),
                      ('test_integrity.py','integrity_current'),
                      ('test_runner_custody.py','custody_current')]:
    target = base/'private'/prior
    prior_before = inventory(target)
    if not target.is_dir() or not (target/'PROCESS_RECEIPTS.json').is_file():
        raise ValueError('Actual successful prior run required')
    for optimized in (False,True):
        label = script[:-3]+('_O' if optimized else '_normal')
        marker = outdir/(label+'.child_marker')
        bootstrap = ('import pathlib,runpy,sys\n'
                     'm=pathlib.Path(sys.argv[1]); p=sys.argv[2]\n'
                     'def audit(e,a):\n'
                     ' if e=="subprocess.Popen" and not m.exists():\n'
                     '  with m.open("xb") as f: f.write(b"CHILD")\n'
                     'sys.addaudithook(audit)\n'
                     'sys.path.insert(0,str(pathlib.Path(p).parent))\n'
                     'sys.argv=[p]+sys.argv[3:]; runpy.run_path(p,run_name="__main__")\n')
        argv=[sys.executable,'-E','-B']+(['-O'] if optimized else [])
        argv+=['-c',bootstrap,str(marker),str(root/'support'/script)]
        if script!='run_diagnostics.py': argv+=['--archive',str(base/'pr97_support.zip')]
        argv+=['--output-dir',str(target)]
        started=dt.datetime.now(dt.timezone.utc).isoformat(); tick=time.monotonic()
        p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr=p.communicate()
        write_new(outdir/(label+'.stdout.txt'),stdout)
        write_new(outdir/(label+'.stderr.txt'),stderr)
        r=dict(label=label,command=argv,cwd=os.getcwd(),pid=p.pid,started_utc=started,
               finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
               wall_seconds=time.monotonic()-tick,exit_code=p.returncode,
               stdout_sha256=sha(stdout),stderr_sha256=sha(stderr),
               input_script_sha256=sha((root/'support'/script).read_bytes()),
               prior_actual_run=prior,prior_inventory_before=prior_before,
               prior_inventory_after=inventory(target),child_launched=marker.exists(),
               expected_reason='Output directory must be fresh and non-existing')
        r['accepted']=(p.returncode!=0 and r['expected_reason'].encode() in stderr
                       and not marker.exists() and prior_before==r['prior_inventory_after'])
        records.append(r); custody.save(records)
        if not r['accepted']: raise RuntimeError('Actual reuse rejection failed')
if root_before!=inventory(root): raise RuntimeError('Closed payload changed')
result=dict(status='PASS',actual_successful_output_reuse_rejections=6,
            no_child_launch_attempts=True,all_prior_output_bytes_and_links_unchanged=True,
            closed_payload_unchanged=True,scope='Output custody only, no new mathematical runs')
write_new(outdir/'RESULT.json',json_bytes(result))
print(json.dumps(result,indent=2))
