#!/usr/bin/env python3
"""Run strict rejection and real nonroot read-only replay controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

MODES = [[], ['-O'], ['-OO']]


def need(test, message):
    if not test:
        raise RuntimeError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(verifier, root, pin, mode):
    return subprocess.run([sys.executable, '-B', *mode, str(verifier),
                           '--root', str(root), '--manifest-sha256', pin],
                          capture_output=True, text=True,
                          env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})


def change(root, name, fn):
    p = root / name
    x = json.loads(p.read_text())
    fn(x)
    p.write_text(json.dumps(x, indent=2, allow_nan=True) + '\n')


def repin(root):
    p = root / 'MANIFEST.json'
    m = json.loads(p.read_text())
    for e in m['files']:
        q = root / e['path']
        if q.is_file() and not q.is_symlink():
            b = q.read_bytes()
            e['bytes'] = len(b)
            e['sha256'] = sha(b)
    p.write_text(json.dumps(m, indent=2) + '\n')
    return sha(p.read_bytes())


def mutate(label, root, pin):
    if label == 'payload_change':
        with (root / 'REPORT.md').open('ab') as f:
            f.write(b'change')
    elif label == 'untrusted_manifest_change':
        with (root / 'MANIFEST.json').open('ab') as f:
            f.write(b' ')
    elif label == 'missing_file':
        (root / 'REPORT.md').unlink()
    elif label == 'extra_file':
        (root / 'EXTRA').write_text('extra')
    elif label == 'symlink_payload':
        (root / 'REPORT.md').unlink()
        (root / 'REPORT.md').symlink_to(root / 'README.md')
    elif label == 'replaced_verifier':
        (root / 'verify.py').write_text('raise SystemExit(0)\n')
    elif label in ['boolean_bytes', 'float_bytes', 'negative_bytes', 'wrong_hash',
                   'traversal_member', 'absolute_member', 'duplicate_member']:
        def f(m):
            e = m['files'][0]
            if label == 'boolean_bytes': e['bytes'] = True
            elif label == 'float_bytes': e['bytes'] = 1.0
            elif label == 'negative_bytes': e['bytes'] = -1
            elif label == 'wrong_hash': e['sha256'] = '0' * 64
            elif label == 'traversal_member': e['path'] = '../REPORT.md'
            elif label == 'absolute_member': e['path'] = '/REPORT.md'
            elif label == 'duplicate_member': m['files'].append(dict(e))
        change(root, 'MANIFEST.json', f)
        pin = sha((root / 'MANIFEST.json').read_bytes())
    elif label == 'duplicate_json_key':
        p = root / 'MANIFEST.json'
        p.write_bytes(p.read_bytes().replace(b'"schema": 1', b'"schema": 1, "schema": 1', 1))
        pin = sha(p.read_bytes())
    elif label in ['new_discovery_overclaim', 'community_overclaim', 'formalization_overclaim',
                   'computational_proof_overclaim', 'missing_claim']:
        def f(c):
            if label == 'new_discovery_overclaim': c['new_discovery_claimed'] = True
            elif label == 'community_overclaim': c['community_acceptance_verified'] = True
            elif label == 'formalization_overclaim': c['proof_assistant_verified'] = True
            elif label == 'computational_proof_overclaim': c['finite_checks_prove_theorem'] = True
            else: del c['new_approaches']
        change(root, 'CLAIMS.json', f)
        pin = repin(root)
    elif label == 'source_acceptance_overclaim':
        change(root, 'SOURCES.json', lambda s: s['scholarly_sources'][0].__setitem__('publication_status', 'peer_reviewed'))
        pin = repin(root)
    elif label in ['false_n0', 'false_epsilon', 'boolean_L', 'nan_fixture',
                   'infinity_fixture', 'zero_denominator', 'noncanonical_fraction',
                   'missing_fixture']:
        def f(x):
            e = x['parameters'][0]
            if label == 'false_n0': e['n0'] += 1
            elif label == 'false_epsilon': e['epsilon'] = [1, 1]
            elif label == 'boolean_L': e['L'] = True
            elif label == 'nan_fixture': e['n0'] = float('nan')
            elif label == 'infinity_fixture': e['n0'] = float('inf')
            elif label == 'zero_denominator': e['eta'] = [1, 0]
            elif label == 'noncanonical_fraction': e['eta'] = [2, 200]
            else: x['parameters'].pop()
        change(root, 'FIXTURES.json', f)
        pin = repin(root)
    else:
        raise RuntimeError('unknown mutation')
    return pin


def unlock(root):
    root.chmod(0o755)
    for p in root.iterdir():
        if not p.is_symlink(): p.chmod(0o644)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--manifest-sha256', required=True)
    ap.add_argument('--verifier-sha256', required=True)
    a = ap.parse_args()
    root = a.root.absolute()
    verifier = root / 'verify.py'
    need(sha(verifier.read_bytes()) == a.verifier_sha256, 'external verifier pin mismatch')
    baseline = [run(verifier, root, a.manifest_sha256, mode) for mode in MODES]
    need(all(r.returncode == 0 for r in baseline), 'baseline rejection')
    need(len({r.stdout for r in baseline}) == 1, 'optimization output mismatch')
    labels = ['payload_change', 'untrusted_manifest_change', 'missing_file', 'extra_file',
              'symlink_payload', 'replaced_verifier', 'boolean_bytes', 'float_bytes',
              'negative_bytes', 'wrong_hash', 'traversal_member', 'absolute_member',
              'duplicate_member', 'duplicate_json_key', 'new_discovery_overclaim',
              'community_overclaim', 'formalization_overclaim', 'computational_proof_overclaim',
              'missing_claim', 'source_acceptance_overclaim', 'false_n0', 'false_epsilon',
              'boolean_L', 'nan_fixture', 'infinity_fixture', 'zero_denominator',
              'noncanonical_fraction', 'missing_fixture']
    with tempfile.TemporaryDirectory(prefix='robust-interpolation-controls-') as td:
        td = Path(td)
        for i, label in enumerate(labels):
            cp = td / str(i)
            shutil.copytree(root, cp)
            pin = mutate(label, cp, a.manifest_sha256)
            # The verifier is the externally pinned original, never mutant code.
            for mode in MODES:
                r = run(verifier, cp, pin, mode)
                need(r.returncode != 0 and r.stderr.startswith('REJECT:'), 'accepted mutation ' + label)
        ro = td / 'readonly'
        shutil.copytree(root, ro)
        before = {p.name: sha(p.read_bytes()) for p in ro.iterdir()}
        for p in ro.iterdir(): p.chmod(0o444)
        ro.chmod(0o555)
        need(hasattr(os, 'geteuid') and os.geteuid() != 0, 'not genuinely nonroot')
        denied = []
        try:
            for p in [ro / 'WRITE_PROBE', ro / 'REPORT.md']:
                try:
                    with p.open('ab') as f: f.write(b'x')
                except PermissionError:
                    denied.append(p.name)
                else:
                    raise RuntimeError('read-only write probe succeeded')
            for mode in MODES:
                # Also execute the authenticated relocated verifier in situ.
                r = run(ro / 'verify.py', ro, a.manifest_sha256, mode)
                need(r.returncode == 0 and r.stdout == baseline[0].stdout,
                     'read-only relocation mismatch')
            after = {p.name: sha(p.read_bytes()) for p in ro.iterdir()}
            need(before == after, 'read-only inventory changed')
        finally:
            unlock(ro)
    out = {'status': 'PASS', 'baseline_modes': ['normal', '-O', '-OO'],
           'identical_optimization_output': True, 'negative_cases': len(labels),
           'negative_rejections': len(labels) * 3, 'negative_labels': labels,
           'nonroot_euid': os.geteuid(), 'read_only_write_probes_denied': denied,
           'read_only_modes': ['normal', '-O', '-OO'], 'relocation_identical': True,
           'read_only_inventory_unchanged': True, 'trusted_external_verifier_used': True}
    print(json.dumps(out, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, TypeError, KeyError, OSError) as exc:
        print('CONTROL FAILURE: ' + str(exc), file=sys.stderr)
        sys.exit(1)
