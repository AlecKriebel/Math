#!/usr/bin/env python3
"""Capture one real owned review computation with complete streams and source."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
base = Path(__file__).absolute().parent
name, *argv = sys.argv[1:]
assert name and '/' not in name and argv
folder = base / name
folder.mkdir()
operator = Path(__file__).read_bytes()
(folder / 'prelaunch_operator.py').write_bytes(operator)
pins = []
for arg in argv:
    p = Path(arg)
    if p.is_file() and not p.is_symlink() and p.suffix == '.py':
        body = p.read_bytes()
        copy = 'prelaunch_source_%d.py' % len(pins)
        (folder / copy).write_bytes(body)
        pins.append({'path': str(p.absolute()), 'copy': copy, 'bytes':len(body),
                     'sha256': hashlib.sha256(body).hexdigest()})
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
child = subprocess.Popen(argv, cwd=base, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = child.communicate()
finished = datetime.datetime.now(datetime.timezone.utc).isoformat()
(folder / 'stdout.bin').write_bytes(out)
(folder / 'stderr.bin').write_bytes(err)
for pin in pins:
    assert Path(pin['path']).read_bytes() == (folder / pin['copy']).read_bytes()
record = {'schema':'pr50-final-review-real-command/v1', 'operator_pid':os.getpid(),
          'child_pid':child.pid,'argv':argv,'cwd':str(base),'started_utc':started,
          'finished_utc':finished,'interval_kind':'enclosing operator interval; child times not separately instrumented',
          'exit_code':child.returncode,'source_pins':pins,
          'stdout':{'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},
          'stderr':{'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
(folder / 'CAPTURE.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record, indent=2))
if child.returncode: raise SystemExit(child.returncode)
