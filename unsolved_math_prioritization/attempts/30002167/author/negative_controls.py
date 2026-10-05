#!/usr/bin/env python3
"""Verify exact rejection of intentionally false claims and altered packets."""
import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path
sys.dont_write_bytecode = True
from exact_checks import verify_certificate
from verify_manifest import verify

ROOT = Path(__file__).resolve().parent


def reject(action, label):
    try:
        action()
    except ValueError:
        return label
    raise RuntimeError('False claim was accepted: ' + label)


def main():
    certificate = json.loads((ROOT / 'CERTIFICATE.json').read_text())
    controls = []
    for key, value in [('minimum_squared_tour_cost', '8'),
                       ('analytic_tour_lower_bound', '9'),
                       ('undirected_tour_count', 59),
                       ('minimum_squared_matching_cost', '5')]:
        bad = copy.deepcopy(certificate)
        bad[key] = value
        controls.append(reject(lambda: verify_certificate(bad), 'reject ' + key))
    for kind in ('edited proof', 'extra file', 'missing file', 'same-content symlink'):
        with tempfile.TemporaryDirectory(prefix='hamiltonian-negative-') as temp:
            target = Path(temp) / 'packet'
            shutil.copytree(ROOT, target)
            proof = target / 'PROOF.md'
            if kind == 'edited proof':
                proof.write_bytes(proof.read_bytes() + b'\nchanged\n')
            elif kind == 'extra file':
                (target / 'unexpected.txt').write_text('unexpected')
            elif kind == 'missing file':
                proof.unlink()
            else:
                saved = Path(temp) / 'same-content.md'
                saved.write_bytes(proof.read_bytes())
                proof.unlink()
                proof.symlink_to(saved)
            controls.append(reject(lambda: verify(target), 'reject ' + kind))
    print(json.dumps({'negative_controls_passed': len(controls), 'controls': controls}, sort_keys=True))


if __name__ == '__main__':
    main()
