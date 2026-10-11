#!/usr/bin/env python3
"""One-shot external root closure; never writes within the reviewed namespace."""
from pathlib import Path
import datetime, hashlib, json, stat, subprocess, sys
A = Path(__file__).resolve().parent
N = A / 'priority_supersingular_mechanism'
OUT = A / 'root_priority_private/mechanism_final_replay001'
AUTH = A / 'ROOT_MECHANISM_CLOSURE_AUTHORIZATION.json'
EXPECTED = '1c32e5dd532eabb573bc2713e064b9b6a624633b5be2a1e4436c6841b6f8d38c'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(path):
    data = path.read_bytes()
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), mode=oct(stat.S_IMODE(path.stat().st_mode)))
def snapshot(base):
    result = {}
    for p in sorted(base.rglob('*')):
        if p.is_symlink(): raise RuntimeError('Unexpected symlink')
        if p.is_file(): result[str(p.relative_to(base))] = pin(p)
    return result
assert not OUT.exists() and not (A / 'ROOT_MECHANISM_CLOSURE.json').exists()
auth = json.loads(AUTH.read_text())
assert auth['namespace'] == str(N) and auth['manifest_sha256'] == EXPECTED
assert auth['one_time_external_closure_authorized'] is True
before = snapshot(N)
old_before = snapshot(A / 'honda_lifting')
assert len(before) == 144 and before['MANIFEST.json']['sha256'] == EXPECTED
manifest = json.loads((N / 'MANIFEST.json').read_text())
assert len(manifest['entries']) == 143
assert {e['relative_path']: {k:v for k,v in e.items() if k != 'relative_path'} for e in manifest['entries']} == {k:v for k,v in before.items() if k != 'MANIFEST.json'}
definitions = json.loads((N / 'MUTANT_DEFINITIONS.json').read_text())
assert len(definitions) == 4
baseline = json.loads((N / 'executions/013_reproduce_integral_flag/metadata.json').read_text())
interpreter = Path(baseline['actual_argv'][0]).resolve()
argv = [str(interpreter), str(N / 'verify_readonly.py')]
env = baseline['actual_env']
OUT.mkdir(parents=True)
start = now()
pre = dict(started_utc=start, argv=argv, cwd=str(N), environment=env,
           authorization=pin(AUTH), program=pin(Path(__file__)), interpreter=pin(interpreter),
           reviewed_namespace_before=before)
(OUT / 'preexecution.json').write_text(json.dumps(pre, indent=2)+'\n')
proc = subprocess.run(argv, cwd=N, env=env, capture_output=True)
(OUT / 'stdout.txt').write_bytes(proc.stdout)
(OUT / 'stderr.txt').write_bytes(proc.stderr)
after = snapshot(N)
rec = dict(pre, completed_utc=now(), actual_exit=proc.returncode,
           stdout=pin(OUT / 'stdout.txt'), stderr=pin(OUT / 'stderr.txt'),
           namespace_unchanged=before == after,
           old_sealed_honda_namespace_unchanged=old_before == snapshot(A / 'honda_lifting'))
(OUT / 'native_receipt.json').write_text(json.dumps(rec, indent=2)+'\n')
assert proc.returncode == 0 and not proc.stderr and rec['namespace_unchanged'] and rec['old_sealed_honda_namespace_unchanged']
output = json.loads(proc.stdout)
assert output['mathematical_control_assertions'] == 71 and len(output['native_negative_controls']) == 4
assert output['manifest_payload_files'] == 143 and output['namespace_files'] == 144
closure = dict(utc=now(), status='ROOT_CLOSED_MATHEMATICAL_MECHANISM_PASS', completion_percent=100,
               historical_first_priority_certified=False, namespace=str(N), manifest_sha256=EXPECTED,
               source_scope='Root operative Yu pages2–4 and Auer–Top1,5–6; Oort1–15, Nicole–Vasiu full9; Lazard supportive source not read by root. No full foundational proof reproduction claimed.',
               exact_result='Integral saturated flag has three elliptic supersingular factors; contravariance and exact p-kernels prove special-fiber qss. Finite Honda input separately realizes the finite group over W(k).',
               reviewed_namespace_closed_unchanged=True, authorization=pin(AUTH),
               actual_native_receipt=pin(OUT / 'native_receipt.json'),
               native_receipt_directory=str(OUT),
               evidence_boundary='This closure records a root decision supported by the separately captured actual verifier process; it is not a process exit receipt for its own creation.')
(A / 'ROOT_MECHANISM_CLOSURE.json').write_text(json.dumps(closure, indent=2)+'\n')
print(proc.stdout.decode(), end='')
print(json.dumps(closure, indent=2))
