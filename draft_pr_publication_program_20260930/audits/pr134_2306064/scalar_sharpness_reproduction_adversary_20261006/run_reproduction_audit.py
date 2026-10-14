#!/usr/bin/env python3
"""Run original bytes only in isolated copies; preserve complete receipts and seals."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import datetime, json, os, subprocess, sys

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT.parent / 'original_head_authentication_20261006' / 'original_attempt'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')

def digest(path):
    return {'bytes': path.stat().st_size, 'sha256': sha256(path.read_bytes()).hexdigest()}

author = (ORIGINAL / 'verify.py').read_bytes()
independent = (ORIGINAL / 'review/independent_checks.py').read_bytes()
proof = (ORIGINAL / 'CANDIDATE.md').read_bytes()
author_bad = author.replace(b"2*k*k-d*k-b==0", b"2*k*k-d*k-b==1")
independent_bad = independent.replace(b"2*k*k-(a+2*b-1)*k-b==0", b"2*k*k-(a+2*b-1)*k-b==1")
assert author_bad != author and independent_bad != independent
assert author.count(b"2*k*k-d*k-b==0") == 1
assert independent.count(b"2*k*k-(a+2*b-1)*k-b==0") == 1
fixed = independent.replace(b" assert t;count+=1", b" if not t:raise AssertionError('independent control failed')\n count+=1")
assert fixed != independent and independent.count(b" assert t;count+=1") == 1
fixed_bad = fixed.replace(b"2*k*k-(a+2*b-1)*k-b==0", b"2*k*k-(a+2*b-1)*k-b==1")

specs = []
for mode in ('normal', 'optimized'):
    for suite, code, expected_failure in (
        ('author_baseline', author, False),
        ('independent_baseline', independent, False),
        ('author_false_parameter', author_bad, True),
        ('independent_false_parameter', independent_bad, mode == 'normal'),
        ('independent_hardened_baseline', fixed, False),
        ('independent_hardened_false_parameter', fixed_bad, True),
    ):
        name = f'{suite}_{mode}'
        folder = ROOT / 'isolated_runs' / name
        folder.mkdir(parents=True, exist_ok=True)
        script = folder / ('verify.py' if suite.startswith('author') else 'independent_checks.py')
        script.write_bytes(code)
        if suite.startswith('author'):
            (folder / 'CANDIDATE.md').write_bytes(proof)
        specs.append((name, folder, script, mode, expected_failure))

def run(spec):
    name, folder, script, mode, expected_failure = spec
    command = [sys.executable] + (['-O'] if mode == 'optimized' else []) + [str(script)]
    start = utc()
    stdout_path, stderr_path = folder / 'stdout.json', folder / 'stderr.txt'
    with stdout_path.open('wb') as out, stderr_path.open('wb') as err:
        process = subprocess.Popen(command, cwd=folder, stdout=out, stderr=err)
        launch = {'event': 'launch', 'utc': start, 'runner_pid': os.getpid(), 'child_pid': process.pid,
                  'mode': mode, 'command': command, 'script': digest(script)}
        (folder / 'PROCESS_JOURNAL.jsonl').write_text(json.dumps(launch, sort_keys=True) + '\n')
        rc = process.wait()
    end = utc()
    receipt = None
    if rc == 0:
        receipt = json.loads(stdout_path.read_text())
    reference_path = ORIGINAL / ('verification.json' if name.startswith('author') else 'review/independent_results.json')
    reference = json.loads(reference_path.read_text())
    output_file = folder / 'independent_results.json'
    result = {'name': name, 'started_utc': start, 'finished_utc': end, 'runner_pid': os.getpid(),
              'child_pid': process.pid, 'exit_code': rc, 'expected_failure': expected_failure,
              'expected_failure_observed': (rc != 0) == expected_failure,
              'script': digest(script), 'stdout': digest(stdout_path), 'stderr': digest(stderr_path),
              'reference_path': str(reference_path), 'reference': digest(reference_path),
              'complete_receipt': receipt, 'complete_receipt_matches_reference': receipt == reference,
              'stdout_byte_identical_reference': stdout_path.read_bytes() == reference_path.read_bytes(),
              'written_receipt': digest(output_file) if output_file.exists() else None,
              'written_receipt_byte_identical_reference': output_file.read_bytes() == reference_path.read_bytes() if output_file.exists() else None}
    with (folder / 'PROCESS_JOURNAL.jsonl').open('a') as journal:
        journal.write(json.dumps({'event': 'finish', 'utc': end, 'child_pid': process.pid, 'exit_code': rc,
                                  'stdout': result['stdout'], 'stderr': result['stderr']}, sort_keys=True) + '\n')
    (folder / 'RUN_RECEIPT.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    seal_files = [p for p in sorted(folder.iterdir()) if p.is_file()]
    (folder / 'RUN_SEAL.json').write_text(json.dumps({'sealed_utc': utc(), 'pid': os.getpid(),
        'files': [{'path': p.name, **digest(p)} for p in seal_files]}, indent=2, sort_keys=True) + '\n')
    return result

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, specs))
assert all(r['expected_failure_observed'] for r in results)
assert all(r['complete_receipt_matches_reference'] for r in results if 'baseline' in r['name'])
assert next(r for r in results if r['name'] == 'independent_false_parameter_optimized')['complete_receipt_matches_reference']
before = json.loads((ROOT / 'ORIGINAL_BEFORE_MANIFEST.json').read_text())
after = [{'path': str(p.relative_to(ORIGINAL)), **digest(p)} for p in sorted(ORIGINAL.rglob('*')) if p.is_file()]
unchanged = before['files'] == after
assert unchanged and len(after) == 17
summary = {'utc': utc(), 'runner_pid': os.getpid(), 'python_executable': sys.executable,
           'python_version': sys.version, 'original_file_count': len(after), 'original_unchanged': unchanged,
           'initial_math_freeze_sha256': sha256((ROOT / 'INITIAL_MATH_VERDICT.md').read_bytes()).hexdigest(),
           'runs': results,
           'finding': 'Author guards survive -O. Independent assert-only guard is erased by -O; a false parameter control returns the entire original success receipt. Explicit conditional guard repairs this in isolated copies.'}
(ROOT / 'REPRODUCTION_RESULTS.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
(ROOT / 'ORIGINAL_AFTER_MANIFEST.json').write_text(json.dumps({'utc': utc(), 'pid': os.getpid(),
    'original_root': str(ORIGINAL), 'file_count': len(after), 'files': after, 'unchanged': unchanged}, indent=2) + '\n')
print(json.dumps({'original_unchanged': unchanged, 'runs': [
    {k: r[k] for k in ('name', 'child_pid', 'exit_code', 'complete_receipt_matches_reference',
                      'stdout_byte_identical_reference', 'written_receipt_byte_identical_reference')} for r in results]}, indent=2))
