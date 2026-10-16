#!/usr/bin/env python3
"""Root replay of three sealed audit controls in separate owned directories."""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
OUT = HERE / 'root_reproduction'
SOURCE = HERE / 'submitted/unsolved_math_prioritization/attempts/9700040'
EXPECTED_MANIFESTS = {
    'poisson_dynamics_adversary_01': 'ff02ad3c05a85f8a9fb736311915da59db143cb5042deafa03166408f9a76366',
    'rsk_joint_law_adversary_01': 'd1d3de9cea00ce1b5351d38acbefd350ef847f8aa1da7db97f8ac0d61956fc6c',
    'source_certificate_adversary_01': '340f674b5dc27c0148b1ecd020854e4b2799b51f14f060f37ea5dbcf857d0c24',
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def verify_seals():
    receipts = []
    for family, expected in EXPECTED_MANIFESTS.items():
        folder = HERE / family
        raw = (folder / 'FINAL_AUDIT_MANIFEST.json').read_bytes()
        assert sha(raw) == expected, family
        manifest = json.loads(raw)
        artifacts = manifest.get('public_authored_artifacts', manifest.get('authored_and_reproduction_artifact_files'))
        for item in artifacts:
            p = folder / item['path']
            assert p.resolve().is_relative_to(folder.resolve())
            b = p.read_bytes()
            assert len(b) == item['bytes'] and sha(b) == item['sha256'], p
        originals = manifest.get('original_native_inputs', manifest.get('original_inputs'))
        assert len(originals) == 20
        for item in originals:
            rel = item['native_path'].split('unsolved_math_prioritization/attempts/9700040/', 1)[1]
            b = (SOURCE / rel).read_bytes()
            assert len(b) == item['bytes'] and sha(b) == item['sha256'], rel
            blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
            assert blob == item.get('native_blob', item.get('git_blob_sha1')), rel
        receipts.append({'family': family, 'manifest_sha256': expected,
                         'authored_artifacts_verified': len(artifacts), 'original_inputs_verified': 20})
    return receipts

def run_one(kind):
    configs = {
        'dynamics': ('poisson_dynamics_adversary_01', 'independent_dynamics_checks.py', 'INDEPENDENT_CHECKS.json'),
        'rsk': ('rsk_joint_law_adversary_01', 'controls/growth_inverse_rsk_controls.py', 'controls/growth_inverse_rsk_stdout.json'),
        'certificate': ('source_certificate_adversary_01', 'certificate_controls.py', 'CONTROL_RECEIPTS.json'),
    }
    family, script_rel, expected_rel = configs[kind]
    work = OUT / ('fresh_' + kind)
    work.mkdir(parents=True, exist_ok=False)
    script = HERE / family / script_rel
    target = work / script.name
    shutil.copyfile(script, target)
    assert script.read_bytes() == target.read_bytes()
    if kind == 'certificate':
        code_dir = OUT / 'submitted/unsolved_math_prioritization/attempts/9700040'
        code_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / 'stationary_law.py', code_dir / 'stationary_law.py')
    args = [sys.executable, str(target)]
    if kind == 'dynamics':
        args += ['--output', str(work / 'INDEPENDENT_CHECKS.json')]
    started = now()
    p = subprocess.run(args, cwd=work, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, capture_output=True, timeout=360)
    ended = now()
    (work / 'stdout.json').write_bytes(p.stdout)
    (work / 'stderr.txt').write_bytes(p.stderr)
    assert p.returncode == 0 and not p.stderr, (kind, p.returncode, p.stderr)
    expected = json.loads((HERE / family / expected_rel).read_bytes())
    actual = json.loads((work / 'CONTROL_RECEIPTS.json').read_bytes() if kind == 'certificate' else p.stdout)
    removals = []
    if kind == 'dynamics':
        removals = ['created_utc']
    if kind == 'certificate':
        removals = ['utc']
        # Full runtime errors differ only by script/source filesystem location.
        replacements = [(str(work), str(HERE / family)),
                        (str(OUT / 'submitted'), str(HERE / 'submitted'))]
        for item in actual['resource_limit_controls']:
            for old, new in replacements:
                item['stderr'] = item['stderr'].replace(old, new)
    for key in removals:
        assert key in actual and key in expected
        del actual[key]
        del expected[key]
    assert actual == expected, (kind, [k for k in actual if actual[k] != expected.get(k)])
    result = {'kind': kind, 'started_utc': started, 'ended_utc': ended, 'returncode': p.returncode,
              'script_sha256': sha(target.read_bytes()), 'stdout_sha256': sha(p.stdout),
              'complete_scientific_receipt_matches': True, 'excluded_informational_fields': removals,
              'path_normalization': 'certificate runtime traceback paths only' if kind == 'certificate' else None,
              'exact_assertions': actual.get('exact_assertions', actual.get('assertions'))}
    (work / 'ROOT_REPLAY_ACCEPTANCE.json').write_text(json.dumps(result, indent=2) + '\n')
    return result

if __name__ == '__main__':
    seals = verify_seals()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run_one, ['dynamics', 'rsk', 'certificate']))
    result = {'utc': now(), 'status': 'PASS', 'seal_checks': seals, 'root_actual_replays': results,
              'scope': 'Complete control-output comparisons and original/artifact byte verification; not a historical priority verdict.'}
    (HERE / 'ROOT_FRESH_FAMILY_VALIDATION.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
