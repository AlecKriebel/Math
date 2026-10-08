#!/usr/bin/env python3
"""Capture complete, byte-equal runs from pre-frozen read-only input directories.
Usage: python run_validation.py FROZEN_AUTHOR_PUBLIC OUTPUT_DIRECTORY
The audit directory containing this file and the author's public directory must
already be mode 0555, with ordinary input files mode 0444. Outputs go elsewhere.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time


def check(ok,message):
    if not ok: raise RuntimeError(message)


def digest(data): return hashlib.sha256(data).hexdigest()

def stamp(): return datetime.now(timezone.utc).isoformat()

def snapshot(directory):
    return [{'path':p.name,'bytes':p.stat().st_size,'sha256':digest(p.read_bytes()),
             'mode':oct(stat.S_IMODE(p.stat().st_mode))}
            for p in sorted(directory.iterdir()) if p.is_file()]


def probe(directory,existing):
    observations=[]
    for label,target,mode in [('create',directory/'denied_write_probe.tmp','xb'),
                              ('append',directory/existing,'ab')]:
        try:
            with target.open(mode): pass
        except PermissionError as error:
            observations.append({'operation':label,'denied':True,'exception':type(error).__name__,
                                 'errno':error.errno})
        else:
            raise RuntimeError('write probe unexpectedly succeeded: '+label)
    return observations


def main():
    check(os.getuid()==1000 and os.geteuid()==1000,'actual real/effective UID must be 1000')
    check(len(sys.argv)==3,'usage: run_validation.py FROZEN_AUTHOR_PUBLIC OUTPUT_DIRECTORY')
    author=Path(sys.argv[1]).resolve()
    audit=Path(__file__).resolve().parent
    output=Path(sys.argv[2]).resolve()
    check(output!=author and output!=audit,'capture output must be external to read-only inputs')
    output.mkdir(parents=True,exist_ok=True)
    before={'author':snapshot(author),'audit':snapshot(audit)}
    for directory in (author,audit):
        check(stat.S_IMODE(directory.stat().st_mode)==0o555,'input directory must be 0555')
        check(all(stat.S_IMODE(p.stat().st_mode)==0o444 for p in directory.iterdir() if p.is_file()),'input files must be 0444')
    receipt={'started_utc':stamp(),'real_uid':os.getuid(),'effective_uid':os.geteuid(),
             'python':sys.version,'input_directory_modes':'0555','input_file_modes':'0444',
             'isolation_scope':'Observed POSIX permission bits and real denied-write probes; no mount/container isolation claim.',
             'write_probes':{'author':probe(author,'check_counting.py'),'audit':probe(audit,'audit_counting.py')},
             'inputs_before':before,'runs':[]}
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    for name,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        for kind,script,args,expected in [('author',author/'check_counting.py',[],author/'EXPECTED_RESULTS.json'),
                                         ('audit',audit/'audit_counting.py',[str(author)],audit/'EXPECTED_AUDIT_RESULTS.json')]:
            start=stamp();clock=time.monotonic()
            completed=subprocess.run([sys.executable]+flags+[str(script)]+args,cwd=audit,env=env,capture_output=True,timeout=300)
            stdout_file=f'{kind}.{name}.stdout.json';stderr_file=f'{kind}.{name}.stderr.txt'
            (output/stdout_file).write_bytes(completed.stdout);(output/stderr_file).write_bytes(completed.stderr)
            equal=completed.stdout==expected.read_bytes()
            record={'kind':kind,'mode':name,'started_utc':start,'elapsed_seconds':round(time.monotonic()-clock,6),
                    'exit_code':completed.returncode,'stdout_bytes':len(completed.stdout),'stdout_sha256':digest(completed.stdout),
                    'stderr_bytes':len(completed.stderr),'stderr_sha256':digest(completed.stderr),
                    'full_stdout_matches_expected':equal,'expected_file':expected.name,
                    'stdout_capture':stdout_file,'stderr_capture':stderr_file}
            receipt['runs'].append(record)
            check(completed.returncode==0 and not completed.stderr and equal,f'{kind} {name} failed')
    after={'author':snapshot(author),'audit':snapshot(audit)}
    receipt.update(completed_utc=stamp(),input_snapshots_unchanged=before==after,inputs_after=after)
    check(before==after,'input snapshots changed')
    (output/'EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'runs':len(receipt['runs']),'unchanged':True},sort_keys=True))

if __name__=='__main__': main()
