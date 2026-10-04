"""One-shot native replay of the main priority family's final stable scientific package."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat, subprocess, sys

A = Path(__file__).resolve().parent
N = A / 'priority_audit'
OUT = A / 'root_priority_private' / 'priority_audit_replay002_final'

def utc():
    return datetime.now(timezone.utc).isoformat()

def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
            'mode': stat.S_IMODE(p.stat().st_mode)}

assert len(sys.argv) == 3, 'Supply reviewed whole/public manifest SHA256 values'
assert not OUT.exists(), 'One-shot output already exists'
whole = N / 'DRAFT_AUDIT_MANIFEST.json'
public = N / 'public_report/PUBLIC_MANIFEST.json'
assert pin(whole)['sha256'] == sys.argv[1]
assert pin(public)['sha256'] == sys.argv[2]
w = json.loads(whole.read_bytes())
assert w['sealed'] is False
files = {whole, public, Path(__file__)}
for row in w['payloads']:
    p = N / row['path']
    assert p.resolve().is_relative_to(N.resolve()) and not p.is_symlink()
    files.add(p)
for row in w['external_pins']:
    files.add(Path(row['path']))
before = {str(p): pin(p) for p in sorted(files)}
OUT.mkdir()
(OUT / 'PREEXECUTION_PAYLOAD_PINS.json').write_text(json.dumps(
    {'utc': utc(), 'pins': before, 'python': sys.version,
     'python_executable': sys.executable}, indent=2) + '\n')
results = []
for label, target in [('public', N / 'public_report/verify_public.py'),
                      ('whole', N / 'verify_audit_readonly.py')]:
    argv = [sys.executable, '-B', str(target)]
    start = utc()
    pre = {'utc': start, 'argv': argv, 'cwd': str(A),
           'target': pin(target), 'orchestrator': pin(Path(__file__))}
    (OUT / (label + '.preexecution.json')).write_text(json.dumps(pre, indent=2) + '\n')
    proc = subprocess.run(argv, cwd=A, capture_output=True)
    stdout = OUT / (label + '.stdout')
    stderr = OUT / (label + '.stderr')
    stdout.write_bytes(proc.stdout)
    stderr.write_bytes(proc.stderr)
    rec = dict(pre, started_utc=start, completed_utc=utc(),
               actual_subprocess_exit_status=proc.returncode,
               stdout=pin(stdout), stderr=pin(stderr))
    (OUT / (label + '.receipt.json')).write_text(json.dumps(rec, indent=2) + '\n')
    results.append(rec)
    print(label, 'actual exit', proc.returncode)
    print(proc.stdout.decode())
    assert proc.returncode == 0 and not proc.stderr, 'Native replay failed'
after = {str(p): pin(p) for p in sorted(files)}
assert before == after, 'Reviewed draft/source payload changed during replay'
summary = {'utc': utc(), 'status': 'PASS_ROOT_FINAL_PRIORITY_SCIENTIFIC_REPLAY',
           'checked_payload_and_external_files': len(files),
           'all_reviewed_body_mode_pins_stable': True,
           'whole_manifest_sha256': sys.argv[1], 'public_manifest_sha256': sys.argv[2],
           'actual_subprocess_receipts': [r['completed_utc'] for r in results],
           'sealed': False, 'first_priority_certified': False,
           'summary_is_computed_metadata_not_subprocess_exit_receipt': True}
(OUT / 'SUMMARY.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
