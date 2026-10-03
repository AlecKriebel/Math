#!/usr/bin/env python3
"""Capture actual local child execution after source/operator review.
Only the explicitly named own source is launched; no historical helper is used.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys, time

def sha(data): return hashlib.sha256(data).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
source = Path(sys.argv[1]).resolve(strict=True)
out = Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=False)
source_bytes = source.read_bytes()
operator_bytes = Path(__file__).resolve().read_bytes()
(out / 'prelaunch_source.py').write_bytes(source_bytes)
(out / 'prelaunch_operator.py').write_bytes(operator_bytes)
argv = [sys.executable, str(source), *sys.argv[3:]]
pre = {'utc':utc(),'operator_pid':os.getpid(),'operator_argv':sys.argv,
       'cwd':str(Path.cwd()),'source':str(source),'source_sha256':sha(source_bytes),
       'source_bytes':len(source_bytes),'operator_sha256':sha(operator_bytes),
       'operator_bytes':len(operator_bytes),'child_argv':argv,
       'source_and_operator_full_read_before_launch':True}
(out / 'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
started = utc(); mono = time.monotonic_ns()
with (out/'stdout.bin').open('wb') as stdout, (out/'stderr.bin').open('wb') as stderr:
    child = subprocess.Popen(argv, cwd=str(Path.cwd()), stdin=subprocess.DEVNULL,
                             stdout=stdout, stderr=stderr)
    pid = child.pid
    code = child.wait()
ended = utc(); elapsed = time.monotonic_ns()-mono
outputs = {}
for name in ('stdout.bin','stderr.bin'):
    data=(out/name).read_bytes()
    outputs[name]={'bytes':len(data),'sha256':sha(data)}
record = {**pre,'launch_utc':started,'end_utc':ended,'elapsed_monotonic_ns':elapsed,
          'actual_child_pid':pid,'actual_child_exit_code':code,'stdio':outputs,
          'source_sha256_after':sha(source.read_bytes()),
          'operator_sha256_after':sha(Path(__file__).resolve().read_bytes())}
(out/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'capture':str(out),'actual_child_pid':pid,'exit_code':code,
                  'launch_utc':started,'end_utc':ended,'stdout':outputs['stdout.bin'],
                  'stderr':outputs['stderr.bin']},indent=2))
sys.exit(code)
