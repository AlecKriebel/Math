#!/usr/bin/env python3
"""Replay frozen author work, independent geometry, and actual correction tests.

Requires Python 3.10+, its standard library, and the patch command. Writes audit_results.json only
with --write-results; otherwise prints results. Never changes either fixture.
The malicious-cache probe is a local harmless marker, not a network action.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import importlib.util
import importlib._bootstrap_external
from independent_geometry import verify_cases

ROOT = Path(__file__).resolve().parent


def need(ok, label):
    if not ok:
        raise RuntimeError(label)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def update_entry(root, name):
    manifest = json.loads((root/'MANIFEST.json').read_text())
    p = root/name
    manifest['files'][name] = {'bytes': p.stat().st_size, 'sha256': sha(p)}
    (root/'MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')


def run(path, optimized=False, args=(), cwd=None):
    command = [sys.executable]+(['-O'] if optimized else [])+[str(path)]+list(args)
    process = subprocess.run(command, cwd=cwd or ROOT.parent,
                             capture_output=True, text=True, timeout=120)
    return {'returncode': process.returncode, 'stdout': process.stdout,
            'stderr': process.stderr}


def malicious_cache(root, optimized, marker):
    source = root/'exact_geometry.py'
    code = compile('from pathlib import Path\nimport json\n'
                   'Path('+repr(str(marker))+').write_text("unverified cache executed")\n'
                   'def expected_results():\n'
                   ' return json.loads(Path('+repr(str(root/'results.json'))+').read_text())\n',
                   str(source), 'exec')
    cache = Path(importlib.util.cache_from_source(str(source), optimization='1' if optimized else ''))
    cache.parent.mkdir()
    cache.write_bytes(importlib._bootstrap_external._code_to_timestamp_pyc(
        code, int(source.stat().st_mtime), source.stat().st_size))


def probe_mutations():
    rows = []
    labels = ['cache', 'empty_cache', 'source_full_resolution', 'source_independent_audit',
              'source_novelty', 'source_remote_mutation', 'source_documents',
              'source_bool_type', 'source_missing_claim', 'source_extra_claim',
              'rehashed_result_overclaim', 'rehashed_wrong_interior', 'bypass_argument']
    claim_keys = {'source_full_resolution':'full_resolution',
                  'source_independent_audit':'independent_audit_claimed',
                  'source_novelty':'novelty_asserted',
                  'source_remote_mutation':'remote_mutation_performed',
                  'source_documents':'source_documents_in_package'}
    with tempfile.TemporaryDirectory(prefix='independent symmetric audit ') as temp:
        base = Path(temp)
        for fixture in ('author_freeze', 'corrected'):
            for optimized in (False, True):
                for label in labels:
                    root = base/(fixture+str(optimized)+label)
                    shutil.copytree(ROOT/fixture, root)
                    marker = base/(root.name+'_MARKER')
                    args = ()
                    if label == 'cache':
                        malicious_cache(root, optimized, marker)
                    elif label == 'empty_cache':
                        (root/'__pycache__').mkdir()
                    elif label.startswith('source_'):
                        s = json.loads((root/'SOURCES.json').read_text())
                        if label in claim_keys:
                            s['claims'][claim_keys[label]] = True
                        elif label == 'source_bool_type':
                            s['claims']['full_resolution'] = 0
                        elif label == 'source_missing_claim':
                            del s['claims']['full_resolution']
                        elif label == 'source_extra_claim':
                            s['claims']['universal_conjecture_proved'] = True
                        (root/'SOURCES.json').write_text(json.dumps(s))
                        update_entry(root, 'SOURCES.json')
                    elif label.startswith('rehashed_'):
                        r = json.loads((root/'results.json').read_text())
                        if label == 'rehashed_result_overclaim':
                            r['status'] = 'SOLVED'
                        else:
                            r['cases']['cube_scale_2']['interior_count'] = 25
                        (root/'results.json').write_text(json.dumps(r))
                        update_entry(root, 'results.json')
                    else:
                        args = ('--skip-checks',)
                    outcome = run(root/'verify.py', optimized, args, base)
                    is_known_frozen_gap = label in ['cache', 'empty_cache'] or label.startswith('source_')
                    expected_success = fixture == 'author_freeze' and is_known_frozen_gap
                    need((outcome['returncode'] == 0) == expected_success,
                         fixture+' unexpected mutation outcome: '+label+str(outcome))
                    need(marker.exists() == (fixture == 'author_freeze' and label == 'cache'),
                         'unexpected cache execution: '+fixture+label)
                    rows.append({'fixture':fixture, 'optimized':optimized, 'mutation':label,
                                 'expected_success':expected_success, 'cache_executed':marker.exists(),
                                 **outcome})
    return rows


def check_patch():
    # Apply the delivered exact unified diff to a fresh original, then compare
    # all bytes with the derivative that the tests actually execute.
    with tempfile.TemporaryDirectory(prefix='symmetric patch application ') as temp:
        root = Path(temp)/'apply'
        shutil.copytree(ROOT/'author_freeze', root)
        p = subprocess.run(['patch', '--batch', '-p1', '-i', str(ROOT/'correction.patch')],
                           cwd=root, capture_output=True, text=True, timeout=30)
        need(p.returncode == 0, 'patch failed: '+p.stdout+p.stderr)
        need(sorted(p.name for p in root.iterdir()) == sorted(p.name for p in (ROOT/'corrected').iterdir()),
             'patch file set')
        need(all(p.read_bytes() == (ROOT/'corrected'/p.name).read_bytes() for p in root.iterdir()),
             'patch differs from tested derivative')
        tests = []
        for optimized in (False, True):
            r = run(root/'verify.py', optimized, cwd=Path(temp))
            need(r['returncode'] == 0, 'applied patch baseline')
            tests.append({'optimized':optimized, **r})
        return {'applies_exactly':True, 'actual_applied_patch_baselines':tests}


def main():
    need(sys.argv[1:] in ([], ['--write-results']), 'arguments')
    replay = []
    for fixture in ('author_freeze', 'corrected'):
        for optimized in (False, True):
            r = run(ROOT/fixture/'verify.py', optimized)
            need(r['returncode'] == 0, fixture+' baseline')
            replay.append({'fixture':fixture, 'optimized':optimized, 'script':'verify.py', **r})
        r = run(ROOT/fixture/'test_fail_closed.py')
        need(r['returncode'] == 0 and json.loads(r['stdout'])['checks'] == 36,
             fixture+' original regression suite')
        replay.append({'fixture':fixture, 'script':'test_fail_closed.py', **r})
    results = json.loads((ROOT/'author_freeze/results.json').read_text())
    independent = verify_cases(results)
    patch = check_patch()
    mutations = probe_mutations()
    output = {'audit_status':'ACCEPT_CORRECTED_PARTIAL', 'original_question':'UNSOLVED',
              'mathematical_proof_audit':'PASS_PARTIAL',
              'frozen_verifier_status':'TWO_REPRODUCED_GAPS',
              'corrected_verifier_status':'PASS_TESTED_SCOPE',
              'replay':replay, 'patch_application':patch,
              'independent_geometry':independent, 'mutation_probes':mutations,
              'counts':{'independent_geometry':len(independent),
                        'mutation_probes':len(mutations),
                        'author_regression_checks':72}}
    if '--write-results' in sys.argv:
        (ROOT/'audit_results.json').write_text(json.dumps(output, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status':output['audit_status'], 'counts':output['counts'],
                      'actual_patch_applies_and_runs':True}, sort_keys=True))


if __name__ == '__main__':
    main()
