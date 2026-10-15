#!/usr/bin/env python3
"""Root replay of inspected fresh-review supplements in an isolated write tree.

No candidate/reviewer receipt is overwritten. These finite controls supplement,
and do not replace, the separately read analytic reports.
"""
from pathlib import Path
from datetime import datetime, timezone
import concurrent.futures
import hashlib
import json
import shutil
import subprocess
import sys

D = Path(__file__).resolve().parent
W = D / 'root_reproduction' / 'fresh_review_checks'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_manifest(family, name):
    root = D / family
    data = json.loads((root / name).read_text())
    if 'artifacts' in data:
        rows = [(Path(x['path']) if Path(x['path']).is_absolute() else root / x['path'],
                 x['sha256']) for x in data['artifacts']]
    elif 'authored_files_sha256' in data:
        rows = [(root / p, h) for p, h in data['authored_files_sha256'].items()]
    elif 'authored_files' in data:
        rows = [(root / x['path'], x['sha256']) for x in data['authored_files']]
    else:
        raise ValueError('Unrecognized manifest schema: ' + name)
    for p, h in rows:
        assert p.is_file() and sha(p) == h, str(p)
    return {'family': family, 'manifest_sha256': sha(root / name),
            'verified_entries': len(rows)}

def run_one(family, script):
    original = D / family / script
    copied = W / family / script
    copied.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(original, copied)
    assert sha(copied) == sha(original)
    if family == 'source_scope_adversary_01':
        for name in ['.gitignore', 'SOURCE_MANIFEST.json']:
            shutil.copyfile(D / family / name, W / family / name)
        (W / family / 'private_reading').symlink_to(D / family / 'private_reading', target_is_directory=True)
    proc = subprocess.run([sys.executable, '-I', '-B', str(copied)],
                          cwd=W / family, capture_output=True, timeout=180)
    (W / family / 'root_stdout.txt').write_bytes(proc.stdout)
    (W / family / 'root_stderr.txt').write_bytes(proc.stderr)
    assert proc.returncode == 0 and not proc.stderr, family
    return {'family': family, 'source_sha256': sha(original), 'exit_code': proc.returncode,
            'stdout_sha256': hashlib.sha256(proc.stdout).hexdigest(),
            'stderr_empty': True, 'copied_source_byte_identical': True}

def main():
    W.mkdir(exist_ok=False)
    # Read-only references preserve the unchanged scripts' relative input paths.
    (W / 'submitted').symlink_to(D / 'submitted', target_is_directory=True)
    (W / '.gitignore').write_text('/submitted\n/source_scope_adversary_01/private_reading\n')
    families = [
        ('kernel_adversary_01', 'authored_manifest.json', 'exact_controls.py'),
        ('stochastic_truncation_adversary_01', 'AUTHORED_MANIFEST.json', 'verify_prehistory_weight.py'),
        ('source_scope_adversary_01', 'ARTIFACT_MANIFEST.json', 'checks/source_scope_checks.py'),
        ('phase_mixing_adversary_01', 'MANIFEST.json', 'exact_phase_controls.py'),
    ]
    pins_before = [verify_manifest(f, m) for f, m, _ in families]
    proof = D / 'submitted/unsolved_math_prioritization/attempts/30002291/PROOF.md'
    assert sha(proof) == '508f71b81ee669d4934ef1cc9e061c129e47d36359896ad7b3e20574dbfbc539'
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda x: run_one(x[0], x[2]), families))
    pins_after = [verify_manifest(f, m) for f, m, _ in families]
    assert pins_before == pins_after
    kernel = json.loads((W / 'kernel_adversary_01/replay_receipt.json').read_text())
    stochastic = json.loads((W / 'stochastic_truncation_adversary_01/INDEPENDENT_CHECK_RECEIPT.json').read_text())
    source = json.loads((W / 'source_scope_adversary_01/checks/PROVENANCE_CHECKS.json').read_text())
    phase = json.loads((W / 'phase_mixing_adversary_01/exact_phase_controls_receipt.json').read_text())
    assert kernel['status'] == stochastic['status'] == phase['status'] == 'PASS'
    assert source['all_passed'] and all(x['passed'] for x in source['checks'])
    assert len(kernel['checks']) == 5 and stochastic['exact_rational_rectangle_cases'] == 2448
    assert len(phase['controls']) == 11 and len(phase['ordered_diagonal_control']['checks']) == 6
    out = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
           'root_read_all_reports_and_scripts_before_execution': True,
           'unchanged_authored_manifest_entries_verified': sum(x['verified_entries'] for x in pins_after),
           'manifest_checks': pins_after, 'actual_replays': results,
           'supplements': {'kernel_named_controls': 5, 'stochastic_exact_cases': 2448,
                          'source_provenance_checks': len(source['checks']),
                          'phase_weighted_mesh_controls': 11, 'phase_diagonal_controls': 6},
           'original_reviewer_files_unchanged': True,
           'private_reading_symlinks_excluded_from_publication': True,
           'analytic_not_numerical_theorem_basis': True,
           'novelty_or_publication_clearance': False}
    (D / 'ROOT_FRESH_REVIEW_REPLAY_ACCEPTANCE.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
