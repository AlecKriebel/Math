#!/usr/bin/env python3
"""Fresh failure controls on private copies of the extracted distribution."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'tmp/extracted'
PDF = HERE.parent.parent / 'publication/output/pdf/note.pdf'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(root, optimized, extra=('--integrity-only',)):
    command = [sys.executable] + (['-O'] if optimized else []) + [str(root / 'verify_package.py'), *extra]
    child = subprocess.run(command, text=True, capture_output=True, timeout=300,
                           env=dict(os.environ, PYTHONOPTIMIZE='2'))
    return {'returncode': child.returncode, 'stdout': child.stdout, 'stderr': child.stderr}


def main():
    records = []
    with tempfile.TemporaryDirectory(prefix='gate-controls-', dir=HERE / 'tmp') as temp:
        base = Path(temp)
        for optimized in (False, True):
            root = base / ('optimized' if optimized else 'ordinary')
            shutil.copytree(SOURCE, root)
            require(run(root, optimized)['returncode'] == 0, 'pristine fails')

            def rejection(case, modify, extra=('--integrity-only',)):
                work = root.with_name(root.name + '-case')
                shutil.copytree(root, work)
                modify(work)
                result = run(work, optimized, extra)
                require(result['returncode'] != 0, 'accepted corruption: ' + case)
                records.append({'case': case, 'optimized': optimized,
                                'PYTHONOPTIMIZE': '2', **result})
                shutil.rmtree(work)

            rejection('changed manuscript', lambda w: (w / 'note.tex').write_bytes((w / 'note.tex').read_bytes() + b'\nCHANGED\n'))
            rejection('missing audit', lambda w: (w / 'reviews/proof_family/AUDIT.md').unlink())
            rejection('unexpected payload', lambda w: (w / 'unexpected.txt').write_text('extra'))
            rejection('same bytes symlink', lambda w: ((w / 'note.tex').unlink(), (w / 'note.tex').symlink_to(SOURCE / 'note.tex')))
            rejection('malformed manifest', lambda w: (w / 'PACKAGE_MANIFEST.json').write_text('{'))

            def wrong_identity(w):
                p = w / 'PACKAGE_MANIFEST.json'
                manifest = json.loads(p.read_text())
                manifest['problem_id'] = 30000348
                p.write_text(json.dumps(manifest))
            rejection('wrong identity', wrong_identity)

            def rewrite_proof(w):
                p = w / 'original_packet/frozen_packet/PROOF.md'
                p.write_bytes(p.read_bytes() + b'\nCHANGED\n')
                m = w / 'PACKAGE_MANIFEST.json'
                manifest = json.loads(m.read_text())
                manifest['files'][p.relative_to(w).as_posix()] = {'bytes': p.stat().st_size,
                       'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                m.write_text(json.dumps(manifest))
            rejection('proof and outer manifest jointly rewritten', rewrite_proof)

            fake_pdf = base / 'wrong.pdf'
            fake_pdf.write_bytes(PDF.read_bytes() + b'\nCHANGED\n')
            rejection('wrong PDF', lambda w: None, ('--integrity-only', '--pdf', str(fake_pdf)))

            def assertion_sentinel(w):
                p = w / 'original_packet/verify_publication.py'
                p.write_bytes(b"assert False, 'FRESH CHILD ASSERTION SENTINEL'\n" + p.read_bytes())
                m = w / 'PACKAGE_MANIFEST.json'
                manifest = json.loads(m.read_text())
                manifest['files'][p.relative_to(w).as_posix()] = {'bytes': p.stat().st_size,
                       'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                m.write_text(json.dumps(manifest))
            rejection('replay retains child assertions', assertion_sentinel, ())
            require('FRESH CHILD ASSERTION SENTINEL' in records[-1]['stderr'], 'assertion sentinel was not cause of failure')
    result = {'status': 'PASS', 'rejected_controls': len(records), 'records': records,
              'mutations_confined_to_private_copies': True}
    (HERE / 'outer_gate_failure_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'rejected_controls': len(records)}, indent=2))


if __name__ == '__main__':
    main()
