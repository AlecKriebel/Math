"""Capture actual subprocess PIDs, exits and complete output hashes.

All mutations and copied original runs stay inside this audit's ignored private
directory. The authenticated original is read-only.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT.parent / 'original_head_authentication_20261006' / 'original_attempt'
PRIVATE = ROOT / 'private' / 'replays'
PRIVATE.mkdir(parents=True, exist_ok=True)

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

INPUT_FILES = ['source_record.json', 'prior_imported_report.json', 'COUNTEREXAMPLE.md', 'verify.py', 'verification.json', 'README.md', 'RESEARCH_LOG.md', 'source_manifest.json']
before = {name: {'bytes': (ORIGINAL/name).stat().st_size, 'sha256': digest(ORIGINAL/name)} for name in INPUT_FILES}
records = []

def run(name, argv, cwd, expected_exit):
    started = datetime.now(timezone.utc).isoformat()
    timer = time.monotonic()
    process = subprocess.Popen(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    record = {'name': name, 'argv': argv, 'working_directory': str(cwd.relative_to(ROOT)), 'PID': process.pid, 'started_UTC': started, 'finished_UTC': datetime.now(timezone.utc).isoformat(), 'elapsed_seconds': time.monotonic()-timer, 'exit': process.returncode, 'expected_exit': expected_exit, 'stdout_sha256': sha256(stdout).hexdigest(), 'stderr_sha256': sha256(stderr).hexdigest(), 'stdout': stdout.decode(errors='replace'), 'stderr': stderr.decode(errors='replace')}
    records.append(record)
    if process.returncode != expected_exit:
        raise RuntimeError(f'{name}: exit {process.returncode}, expected {expected_exit}; {record["stdout"]}; {record["stderr"]}')
    return record

for optimize in [False, True]:
    prefix = [sys.executable] + (['-O'] if optimize else [])
    tag = 'optimized' if optimize else 'normal'
    run('independent_' + tag, prefix + [str(ROOT/'audit_exact.py')], ROOT, 0)
    for mutant in ['order_one', 'zero_order_zero', 'empty_det_zero', 'primitive_content', 'drop_torsion', 'remove_tminus1', 'valuation_as_nullity', 'rectangular_as_square']:
        run('independent_' + tag + '_' + mutant, prefix + [str(ROOT/'audit_exact.py'), '--mutant', mutant], ROOT, 1)
    for negative in [False, True]:
        kind = 'false_assertion' if negative else 'original'
        directory = PRIVATE / (tag + '_' + kind)
        directory.mkdir(exist_ok=True)
        shutil.copyfile(ORIGINAL/'COUNTEREXAMPLE.md', directory/'COUNTEREXAMPLE.md')
        code = (ORIGINAL/'verify.py').read_text()
        if negative:
            needle = 'assert x;checks+=1'
            if code.count(needle) != 1:
                raise RuntimeError('original assertion mutation needle missing or ambiguous')
            code = code.replace(needle, 'assert False;checks+=1')
        (directory/'verify.py').write_text(code)
        run('author_' + tag + '_' + kind, prefix + ['verify.py'], directory, 1 if negative and not optimize else 0)

after = {name: {'bytes': (ORIGINAL/name).stat().st_size, 'sha256': digest(ORIGINAL/name)} for name in INPUT_FILES}
if after != before:
    raise RuntimeError('authenticated original changed during copied replay')
normal = next(x for x in records if x['name']=='independent_normal')
optimized = next(x for x in records if x['name']=='independent_optimized')
if normal['stdout_sha256'] != optimized['stdout_sha256']:
    raise RuntimeError('independent normal and optimized semantic outputs differ')
result = {'schema': 'pr124-integral-algebra-actual-runs/v1', 'UTC': datetime.now(timezone.utc).isoformat(), 'operator_PID': os.getpid(), 'python_executable': sys.executable, 'python_version': sys.version, 'original_inputs': before, 'authenticated_original_unchanged': True, 'independent_script_sha256': digest(ROOT/'audit_exact.py'), 'runner_sha256': digest(Path(__file__)), 'normal_optimized_independent_outputs_identical': True, 'runs': records, 'scope': 'Checks certify only exact algebraic fixtures, not topology, completeness, novelty, priority, or literature status.'}
(ROOT/'RUNS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'operator_PID': os.getpid(), 'run_count': len(records), 'normal_and_optimized_explicit_checks': json.loads(normal['stdout'])['explicit_checks'], 'normal_and_optimized_matrix_cases': json.loads(normal['stdout'])['matrix_cases'], 'independent_mutant_rejections': 16, 'author_assertion_mutant_detected_only_without_optimization': True, 'RUNS_sha256': digest(ROOT/'RUNS.json')}, sort_keys=True))
