#!/usr/bin/env python3
"""Replay the frozen family's assertions on an authenticated scratch copy only."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'source_question_family'
EXPECTED = '072a33c18f04d5b21dd651e81bf0116000a24442457cec453e1958d01ba802b3'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if sys.flags.optimize:
        raise RuntimeError('This replay requires the normal interpreter, without optimization.')
    source = SOURCE / 'exact_checks.py'
    if digest(source) != EXPECTED:
        raise RuntimeError('Frozen source authentication failed.')
    scratch = ROOT / '_local' / 'source_check_replay'
    scratch.mkdir(parents=True, exist_ok=True)
    copied = scratch / 'exact_checks.py'
    shutil.copyfile(source, copied)
    if digest(copied) != EXPECTED:
        raise RuntimeError('Scratch copy authentication failed.')
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    run = subprocess.run([sys.executable, str(copied)], cwd=scratch, env=env,
                         text=True, capture_output=True, check=False)
    (ROOT / 'replay_stdout.txt').write_text(run.stdout + run.stderr)
    if run.returncode:
        raise RuntimeError('Frozen normal-interpreter replay failed; inspect replay_stdout.txt.')
    generated = scratch / 'exact_results.json'
    shutil.move(str(generated), str(ROOT / 'replay_results.json'))
    result = ROOT / 'replay_results.json'
    source_after = digest(source)
    same = result.read_bytes() == (SOURCE / 'exact_results.json').read_bytes()
    if source_after != EXPECTED or not same:
        raise RuntimeError('Source changed or replay differs from frozen result.')
    meta = dict(started_at_utc=started,
                completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                interpreter=sys.executable, interpreter_optimize=sys.flags.optimize,
                pythonoptimize_removed_from_child_environment=True,
                command=[sys.executable, str(copied)], returncode=run.returncode,
                source_before_sha256=EXPECTED, source_after_sha256=source_after,
                scratch_copy_sha256=digest(copied), source_mutated=False,
                result_sha256=digest(result),
                result_byte_identical_to_frozen=True,
                limitations='Normal interpreter assertion replay of finite tests, not a proof or formal verification.')
    (ROOT / 'replay_metadata.json').write_text(json.dumps(meta, indent=2) + '\n')
    print(json.dumps(meta, indent=2))


if __name__ == '__main__':
    main()
