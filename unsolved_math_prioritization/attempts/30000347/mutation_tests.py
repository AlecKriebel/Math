#!/usr/bin/env python3
"""Reject publication mutations in ordinary and optimized Python modes."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def run(root, optimized):
    command = [sys.executable, '-I'] + (['-O'] if optimized else [])
    return subprocess.run(command + [str(root / 'verify_publication.py'), '--integrity-only'],
                          text=True, capture_output=True, timeout=30)

def main():
    files = json.loads((ROOT / 'PUBLIC_MANIFEST.json').read_text())['files']
    cases = []
    with tempfile.TemporaryDirectory(prefix='three-terminal-mutations-') as directory:
        work = Path(directory) / 'packet'
        shutil.copytree(ROOT, work)
        for optimized in (False, True):
            require(run(work, optimized).returncode == 0, 'Pristine integrity check failed')
            for name in sorted(files):
                # Self-modifying a verifier could change execution semantics;
                # this test uses payload mutations, not adversarial code execution.
                if name == 'verify_publication.py':
                    continue
                p = work / name
                saved = p.read_bytes()
                p.write_bytes(saved + b'\nMUTATION\n')
                result = run(work, optimized)
                p.write_bytes(saved)
                require(result.returncode != 0, 'Undetected content mutation: ' + name)
                cases.append({'mode': 'optimized' if optimized else 'normal', 'case': 'changed ' + name})
                p.unlink()
                result = run(work, optimized)
                p.write_bytes(saved)
                require(result.returncode != 0, 'Undetected missing payload: ' + name)
                cases.append({'mode': 'optimized' if optimized else 'normal', 'case': 'missing ' + name})
            p = work / 'PUBLIC_MANIFEST.json'
            saved = p.read_bytes()
            p.write_text('{')
            require(run(work, optimized).returncode != 0, 'Undetected malformed manifest')
            p.write_bytes(saved)
            cases.append({'mode': 'optimized' if optimized else 'normal', 'case': 'malformed public manifest'})
            m = json.loads(saved)
            m['files'].pop('frozen_packet/PROOF.md')
            p.write_text(json.dumps(m))
            require(run(work, optimized).returncode != 0, 'Undetected omitted manifest entry')
            p.write_bytes(saved)
            cases.append({'mode': 'optimized' if optimized else 'normal', 'case': 'omitted manifest entry'})
            target = work / 'frozen_packet/PROOF.md'
            original = target.read_bytes()
            modified = original + b'\nAltered proof.\n'
            target.write_bytes(modified)
            m = json.loads(saved)
            m['files']['frozen_packet/PROOF.md'] = {'bytes': len(modified), 'sha256': hashlib.sha256(modified).hexdigest()}
            p.write_text(json.dumps(m))
            require(run(work, optimized).returncode != 0, 'Coordinated manifest rewrite defeated frozen anchor')
            target.write_bytes(original)
            p.write_bytes(saved)
            cases.append({'mode': 'optimized' if optimized else 'normal', 'case': 'proof and public manifest jointly rewritten'})
            (work / 'unexpected.txt').write_text('Unexpected payload')
            require(run(work, optimized).returncode != 0, 'Undetected extra file')
            (work / 'unexpected.txt').unlink()
            cases.append({'mode': 'optimized' if optimized else 'normal', 'case': 'unexpected file'})
            require(run(work, optimized).returncode == 0, 'Pristine restoration failed')
    print(json.dumps({'result': 'PASS', 'rejected_mutations': len(cases), 'cases': cases,
                     'limitation': 'These guards test integrity and fail-closed behavior, not authenticity against coordinated replacement of verifier and all trust anchors.'}, indent=2))

if __name__ == '__main__':
    main()
