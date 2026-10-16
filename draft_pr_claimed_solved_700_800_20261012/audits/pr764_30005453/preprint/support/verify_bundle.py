"""Verify closed source bytes and replay finite/integrity diagnostics offline.

These checks neither prove the infinite stochastic theorem nor certify priority.
All wrapper guards are explicit exceptions, including under outer Python -O.
"""
from pathlib import Path
import argparse
import json
import os
import stat
import subprocess
import sys
import tempfile
from build_package import (METADATA, PREFIX, PIN, REVIEW_PINS, identity, safe_name,
                           require, review_entries)

ROOT = Path(__file__).resolve().parent


def read_closed(root):
    manifest = json.loads((root / 'MANIFEST.json').read_bytes())
    listed = {}
    for entry in manifest['files']:
        name = safe_name(entry['path'])
        require(name not in listed and name != 'MANIFEST.json', 'Duplicate/self path')
        listed[name] = {k: entry[k] for k in ('bytes', 'sha256')}
    actual = {}
    directories = set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink in closed archive')
        name = path.relative_to(root).as_posix()
        if path.is_dir():
            directories.add(name)
            continue
        require(stat.S_ISREG(path.stat().st_mode), 'Nonregular archive entry')
        actual[name] = path.read_bytes()
    require(set(actual) == set(listed) | {'MANIFEST.json'}, 'File inventory mismatch')
    expected_dirs = {p.as_posix() for name in actual for p in Path(name).parents
                     if p.as_posix() != '.'}
    require(directories == expected_dirs, 'Directory inventory mismatch')
    for name, entry in listed.items():
        require(identity(actual[name]) == entry, 'Content mismatch: ' + name)
    return actual


def run(command, env, cwd):
    result = subprocess.run(command, env=env, cwd=cwd, capture_output=True,
                            text=True, timeout=300)
    require(result.returncode == 0, 'Child failed: ' + result.stderr)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--integrity-only', action='store_true')
    args = ap.parse_args()
    actual = read_closed(ROOT)
    require(json.loads(actual['zenodo-metadata.json']) == {'metadata': METADATA},
            'Publication metadata mismatch')
    gate = json.loads(actual['audit/PRIORITY_GATE.json'])
    require(gate['result'] == 'PASS_FOR_CREDITED_ALTERNATIVE_PROOF_PREPARATION' and
            gate['known_equivalent_results'][0]['covers_candidate'] and
            not gate['first_sole_new_theorem_claim_allowed'] and
            not gate['historical_first_priority_certified'], 'Priority scope mismatch')
    candidate = ROOT / 'historical_candidate'
    require(identity(actual['historical_candidate/PUBLICATION_MANIFEST.json'])['sha256']
            == PIN, 'Historical candidate pin mismatch')
    snapshot = json.loads(actual['audit/SNAPSHOT.json'])
    require(len(snapshot['files']) == 63, 'Wrong candidate inventory size')
    candidate_names = set()
    for entry in snapshot['files']:
        require(entry['path'].startswith(PREFIX), 'Wrong source problem')
        rel = safe_name(entry['path'][len(PREFIX):])
        require(rel not in candidate_names, 'Repeated original path')
        candidate_names.add(rel)
        require(identity(actual['historical_candidate/' + rel]) ==
                {k: entry[k] for k in ('bytes', 'sha256')}, 'Frozen original changed')
    require({name[len('historical_candidate/'):] for name in actual
             if name.startswith('historical_candidate/')} == candidate_names,
            'Candidate closure mismatch')
    for family, pin in REVIEW_PINS.items():
        prefix = 'audit/' + family + '/'
        raw = actual[prefix + 'MANIFEST.json']
        require(identity(raw)['sha256'] == pin, 'Review manifest pin mismatch')
        entries = review_entries(json.loads(raw))
        names = set()
        for entry in entries:
            name = safe_name(entry['path'])
            require(name not in names and name != 'MANIFEST.json', 'Review duplicate/self path')
            names.add(name)
            require(identity(actual[prefix + name]) ==
                    {k: entry[k] for k in ('bytes', 'sha256')}, 'Review content mismatch')
        require({name[len(prefix):] for name in actual if name.startswith(prefix)} ==
                names | {'MANIFEST.json'}, 'Review closure mismatch')
    output = {'result': 'PASS', 'inventory_files': len(actual),
              'outer_optimized': not __debug__,
              'scope': 'Closed bytes and finite diagnostics, not formal infinite proof or priority certification.'}
    if not args.integrity_only:
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        with tempfile.TemporaryDirectory(prefix='vertex-reinforcement-replay-') as temp:
            env['TMPDIR'] = temp
            probe = run([sys.executable, '-B', '-c', 'print(__debug__)'], env, temp)
            require(probe.stdout.strip() == 'True', 'Child assertion mode inactive')
            historical = run([sys.executable, '-B', str(candidate / 'verify_publication.py'),
                              '--replay'], env, temp)
            historical_json = json.loads(historical.stdout)
            require(historical_json['status'] == 'PASS', 'Historical replay failed')
            output['historical_replay'] = historical_json
            output['historical_assertion_scope'] = (
                'The historical wrapper runs normal and optimized children. The '
                'normal author assertions are required evidence; optimized author '
                'assertions are inactive and contribute only integrity replay.')
            det_out = Path(temp) / 'deterministic.json'
            run([sys.executable, '-B', str(ROOT / 'audit/review_deterministic_family/'
                 'independent_controls.py'), '--output', str(det_out)], env, temp)
            det = json.loads(det_out.read_bytes())
            expected = json.loads(actual['audit/review_deterministic_family/INDEPENDENT_CONTROLS.json'])
            det.pop('checked_utc', None)
            expected.pop('checked_utc', None)
            require(det == expected, 'Deterministic finite controls changed')
            output['deterministic_controls'] = det
            stoch = run([sys.executable, '-B', str(ROOT / 'audit/review_stochastic_family/'
                        'independent_controls.py')], env, temp)
            stoch_json = json.loads(stoch.stdout)
            expected = json.loads(actual['audit/review_stochastic_family/NORMAL_CONTROL_RECEIPT.json'])['observed_result']
            require(stoch_json == expected, 'Stochastic finite controls changed')
            output['stochastic_controls'] = stoch_json
            # Run the unmodified historical negative tests, keeping at most one
            # fixture copy resident. The monkeypatch changes storage lifetime only.
            mutation_code = """
import pathlib, runpy, shutil, sys
original_copytree = shutil.copytree
previous = [None]
depth = [0]
def bounded_copytree(source, destination, *args, **kwargs):
    top = depth[0] == 0
    if top and previous[0] is not None:
        shutil.rmtree(previous[0])
    depth[0] += 1
    try:
        answer = original_copytree(source, destination, *args, **kwargs)
    finally:
        depth[0] -= 1
    if top:
        previous[0] = pathlib.Path(destination)
    return answer
shutil.copytree = bounded_copytree
runpy.run_path(sys.argv[1], run_name='__main__')
"""
            mutations = run([sys.executable, '-B', '-c', mutation_code,
                             str(candidate / 'test_publication_integrity.py')], env, temp)
            mutation_json = json.loads(mutations.stdout)
            require(mutation_json == {'status': 'PASS', 'negative_controls': 8,
                    'payload_mutations_rejected': 6, 'unauthorized_queue_edits_rejected': 2},
                    'Historical negative-control mismatch')
            output['historical_mutation_controls'] = mutation_json
        require(read_closed(ROOT) == actual, 'Replay changed the closed archive')
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
