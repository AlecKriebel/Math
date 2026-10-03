#!/usr/bin/env python3
"""Root reproduction of sealed family controls, in disposable private copies."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, shutil, subprocess

A = Path(__file__).resolve().parent
PY = A.parents[0] / 'pr378_30004322/sources_effective_review/private_runtime/bin/python'
WORK = A / 'tmp/root_family_controls'
assert not WORK.exists(), 'Preserve a prior run; do not overwrite it.'
WORK.mkdir(parents=True)

def sha(b): return hashlib.sha256(b).hexdigest()
def bind(p, item):
    b = p.read_bytes()
    assert len(b) == item['bytes'] and sha(b) == item['sha256'], str(p)
    return b

families = [('global_bounds_review', 'PUBLIC_MANIFEST.json'),
            ('thermodynamic_review', 'PUBLIC_MANIFEST.json'),
            ('hessian_holonomy_review/public', 'MANIFEST.json')]
bindings = []
before = {}
for name, mf in families:
    source = A / name
    manifest = json.loads((source / mf).read_text())
    dest = WORK / name
    dest.mkdir(parents=True)
    for item in manifest['files']:
        assert not {'private', 'raw_sources', 'sources', 'tmp'} & set(Path(item['path']).parts)
        p = source / item['path']
        b = bind(p, item)
        before[str(p)] = sha(b)
        out = dest / item['path']
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(b)
    shutil.copyfile(source / mf, dest / mf)
    before[str(source / mf)] = sha((source / mf).read_bytes())
    bindings.append({'family': name, 'files': len(manifest['files']),
                     'manifest_sha256': before[str(source / mf)]})

# Verify all pre-candidate and pre-prior-verdict seals, independently of manifests.
seals = []
g = A / 'global_bounds_review'
for f in ['receipts/baseline_seal.sha256', 'receipts/verdict_seal.sha256']:
    for line in (g / f).read_text().splitlines():
        wanted, name = line.split(None, 1)
        p = Path(name.strip())
        assert p.is_relative_to(g) and sha(p.read_bytes()) == wanted
        seals.append({'seal': str(Path('global_bounds_review') / f), 'path': str(p.relative_to(A)), 'sha256': wanted})
t = A / 'thermodynamic_review'
for f in ['independent_seal.md', 'verdict_seal.md']:
    matches = re.findall(r'SHA-256 ([^:]+): ([0-9a-f]{64})', (t / f).read_text())
    assert len(matches) == 3
    for name, wanted in matches:
        assert sha((t / name).read_bytes()) == wanted
        seals.append({'seal': str(Path('thermodynamic_review') / f), 'path': str(Path('thermodynamic_review') / name), 'sha256': wanted})
h = A / 'hessian_holonomy_review/public'
for f, target in [('pre_candidate_seal.sha256', 'independent_pre_candidate_seal.md'),
                  ('independent_verdict_seal.sha256', 'independent_verdict_seal.md')]:
    wanted = (h / f).read_text().split()[0]
    assert sha((h / target).read_bytes()) == wanted
    seals.append({'seal': str(Path('hessian_holonomy_review/public') / f), 'path': str(Path('hessian_holonomy_review/public') / target), 'sha256': wanted})

# The root already reproduced all ten complete candidate streams. Compare the
# families' full streams to that actual replay, rather than rerunning for counts.
stream_pairs = []
for turn in range(1, 6):
    stream_pairs += [(f'root_turn{turn}.stdout', f'global_bounds_review/private/verify_turn{turn}.py.stdout'),
                     (f'root_turn{turn}.stdout', f'thermodynamic_review/checks/author_streams/verify_turn{turn}.py.stdout.txt'),
                     (f'root_turn{turn}.stdout', f'hessian_holonomy_review/public/author_turn{turn}_stdout.json')]
stream_pairs += [('root_hessian_certificate.stdout', 'global_bounds_review/private/hessian_certificate.py.stdout'),
                 ('root_hessian_certificate.stdout', 'thermodynamic_review/checks/author_streams/hessian_certificate.py.stdout.txt'),
                 ('root_hessian_certificate.stdout', 'hessian_holonomy_review/public/author_full_hessian_certificate_stdout.json'),
                 ('root_public_author_replay.stdout', 'global_bounds_review/private/REPLAY_ALL.py.stdout'),
                 ('root_public_author_replay.stdout', 'thermodynamic_review/checks/author_replay.stdout.txt'),
                 ('root_public_author_replay.stdout', 'hessian_holonomy_review/public/author_replay_stdout.json'),
                 ('root_source_bound_author_replay.stdout', 'thermodynamic_review/checks/author_replay_sources.stdout.txt'),
                 ('root_source_bound_author_replay.stdout', 'hessian_holonomy_review/public/author_replay_with_sources_stdout.json'),
                 ('root_historical_independent.stdout', 'global_bounds_review/private/independent_check.py.post_seal.stdout'),
                 ('root_historical_independent.stdout', 'thermodynamic_review/checks/post_seal_existing_independent.stdout.txt'),
                 ('root_public_review_wrapper.stdout', 'global_bounds_review/private/verify_review.py.post_seal.stdout'),
                 ('root_public_review_wrapper.stdout', 'thermodynamic_review/checks/post_seal_existing_review.stdout.txt'),
                 ('root_public_review_wrapper.stdout', 'hessian_holonomy_review/public/prior_review_replay_stdout.txt')]
stream_checks = []
for root, family in stream_pairs:
    b = (A / root).read_bytes()
    assert b == (A / family).read_bytes(), family
    stream_checks.append({'root': root, 'family': family, 'bytes': len(b), 'sha256': sha(b)})

programs = [
 ('global_baseline', 'global_bounds_review/code/baseline_controls.py', 'global_bounds_review/receipts/baseline_controls.json'),
 ('global_independent', 'global_bounds_review/code/independent_controls.py', 'global_bounds_review/receipts/independent_controls.json'),
 ('thermo_source_first', 'thermodynamic_review/checks/source_first_checks.py', 'thermodynamic_review/checks/source_first_checks.stdout.txt'),
 ('thermo_independent', 'thermodynamic_review/checks/thermodynamic_checks.py', 'thermodynamic_review/checks/thermodynamic_checks.stdout.txt'),
 ('hessian_topology', 'hessian_holonomy_review/public/stdlib_holonomy_controls.py', 'hessian_holonomy_review/public/stdlib_holonomy_stdout.json'),
 ('hessian_symbolic', 'hessian_holonomy_review/public/independent_symbolic_controls.py', 'hessian_holonomy_review/public/independent_symbolic_stdout.json'),
 ('hessian_post_comparison', 'hessian_holonomy_review/public/compare_independent_to_frozen.py', 'hessian_holonomy_review/public/post_seal_comparison_stdout.json'),
 ('hessian_manifest', 'hessian_holonomy_review/public/verify_audit_manifest.py', None),
]
records = []
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
for label, program, expected in programs:
    p = subprocess.run([str(PY), '-B', str(WORK / program)], cwd=(WORK / program).parent, env=env, capture_output=True)
    (A / f'root_family_{label}.stdout').write_bytes(p.stdout)
    (A / f'root_family_{label}.stderr').write_bytes(p.stderr)
    assert p.returncode == 0 and not p.stderr, (label, p.returncode, p.stderr.decode())
    if expected: assert p.stdout == (A / expected).read_bytes(), label
    records.append({'program': program, 'label': label, 'returncode': p.returncode,
                    'stdout_bytes': len(p.stdout), 'stdout_sha256': sha(p.stdout),
                    'stderr_bytes': len(p.stderr), 'byte_exact_family_stream': expected is not None})
    print(label + ': PASS', flush=True)
assert (WORK / 'hessian_holonomy_review/public/independent_full_hessian.txt').read_bytes() == (h / 'independent_full_hessian.txt').read_bytes()
assert all(sha(Path(p).read_bytes()) == digest for p, digest in before.items()), 'Family originals changed'

receipt = {'status': 'PASS', 'created_utc': datetime.now(timezone.utc).isoformat(),
           'completion_percent': 70, 'scope': 'All three initial mathematical families reproduced; final actual-head review pending',
           'families': bindings, 'seals': seals, 'full_candidate_stream_comparisons': stream_checks,
           'programs': records, 'family_originals_unchanged': True,
           'independent_full_hessian_byte_exact': True,
           'python_literal_path': str(PY), 'new_assertions': {'global': 21, 'thermodynamic': 17809, 'hessian_symbolic': 8662, 'hessian_topology': 19},
           'source_replay_counts': {'global_family': 0, 'root': 3, 'thermodynamic_family': 3, 'hessian_family': 3},
           'original_problem_status': 'unsolved', 'original_problem_resolution_percent': 0}
(A / 'root_family_reproduction_receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps({'status': receipt['status'], 'bindings': sum(x['files'] for x in bindings),
                  'seals': len(seals), 'streams': len(stream_checks), 'programs': len(records)}, sort_keys=True))
