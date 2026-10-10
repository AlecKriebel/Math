#!/usr/bin/env python3
"""Actual-copy delivery mutations plus relocated full replays; no source edits."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-manifest', required=True)
    args = parser.parse_args()
    anchor = args.expected_manifest
    need(hashlib.sha256((ROOT / 'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest() == anchor,
         'initial external manifest mismatch')
    positives, negatives = [], []
    with tempfile.TemporaryDirectory(prefix='ricci-publication-test-') as tmp:
        temp = Path(tmp)
        relocated = temp / 'relocated'
        shutil.copytree(ROOT, relocated)
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE', None)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        def run(root, opt=False, given=anchor, full=False):
            cmd = [sys.executable] + (['-O'] if opt else []) + ['-B', str(root / 'verify_publication.py'),
                '--expected-manifest', given] + ([] if full else ['--integrity-only'])
            return subprocess.run(cmd, cwd=temp, capture_output=True, env=env)
        for opt in (False, True):
            for root, label in ((ROOT, 'original'), (relocated, 'relocated')):
                p = run(root, opt, full=True)
                need(p.returncode == 0, label + p.stderr.decode())
                positives.append(label + ('_optimized' if opt else '_normal'))
            for kind in ('proof_edit', 'first_audit_edit', 'second_audit_edit', 'result_edit',
                         'missing_member', 'extra_file', 'extra_directory', 'member_symlink',
                         'directory_symlink', 'archive_truncated', 'archive_changed',
                         'manifest_symlink', 'wrong_anchor', 'self_rehashed_outer_manifest',
                         'duplicate_manifest_key', 'unsafe_manifest_path'):
                dst = temp / (kind + str(opt))
                shutil.copytree(ROOT, dst)
                proof = dst / 'author' / 'APPROACH_1_PDE_REALIZATION.md'
                mp = dst / 'PUBLICATION_MANIFEST.json'
                if kind == 'proof_edit':
                    proof.write_bytes(proof.read_bytes() + b'\nchanged\n')
                if kind == 'first_audit_edit':
                    (dst / 'audit' / 'AUDIT_REPORT.md').write_text('changed\n')
                if kind == 'second_audit_edit':
                    (dst / 'second_audit' / 'SECOND_ANALYTIC_AUDIT.md').write_text('changed\n')
                if kind == 'result_edit':
                    (dst / 'second_audit' / 'stress_results.json').write_text('{}\n')
                if kind == 'missing_member':
                    proof.unlink()
                if kind == 'extra_file':
                    (dst / 'UNEXPECTED.txt').write_text('extra\n')
                if kind == 'extra_directory':
                    (dst / 'UNEXPECTED').mkdir()
                if kind == 'member_symlink':
                    proof.unlink()
                    proof.symlink_to(ROOT / 'author' / 'APPROACH_1_PDE_REALIZATION.md')
                if kind == 'directory_symlink':
                    shutil.rmtree(dst / 'audit')
                    (dst / 'audit').symlink_to(ROOT / 'audit', target_is_directory=True)
                if kind in ('archive_truncated', 'archive_changed'):
                    zp = next((dst / 'archives').glob('*AUTHOR*'))
                    b = zp.read_bytes()
                    zp.write_bytes(b[:-1] if kind == 'archive_truncated' else b + b'changed')
                if kind == 'manifest_symlink':
                    mp.unlink()
                    mp.symlink_to(ROOT / 'PUBLICATION_MANIFEST.json')
                if kind == 'self_rehashed_outer_manifest':
                    proof.write_text('changed\n')
                    m = json.loads(mp.read_bytes())
                    b = proof.read_bytes()
                    m['files']['author/APPROACH_1_PDE_REALIZATION.md'] = {
                        'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
                    mp.write_text(json.dumps(m, sort_keys=True, indent=2) + '\n')
                if kind == 'duplicate_manifest_key':
                    mp.write_text(mp.read_text().replace('{', '{"schema":"injected",', 1))
                if kind == 'unsafe_manifest_path':
                    m = json.loads(mp.read_bytes())
                    m['files']['../escape'] = m['files']['README.md']
                    mp.write_text(json.dumps(m, sort_keys=True, indent=2) + '\n')
                given = '0' * 64 if kind == 'wrong_anchor' else anchor
                p = run(dst, opt, given)
                need(p.returncode != 0, 'mutation accepted: ' + kind)
                negatives.append(kind + ('_optimized' if opt else '_normal'))
    print(json.dumps({'status': 'PASS', 'full_replays': positives,
        'actual_corruption_rejections': negatives,
        'scope': 'External-anchor delivery and selected corruption controls; not formal mathematical certification.'},
        sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
