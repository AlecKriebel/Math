#!/usr/bin/env python3
"""Source-free supplementary verification; replays only disposable copies."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
ORIGINAL_PROOF_SHA256 = 'f31b19b8e4286e0104ed1e272f5cbc4a39e20aea78aa30334466f5b44e5830f7'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def integrity(pdf):
    manifest = json.loads((ROOT / 'PACKAGE_MANIFEST.json').read_text())
    require(manifest['problem_id'] == 30000347 and manifest['version'] == '1.0', 'Wrong identity')
    expected = manifest['files']
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() or p.is_symlink()}
    require(actual == set(expected) | {'PACKAGE_MANIFEST.json'}, 'Package file-set mismatch')
    for name, item in expected.items():
        relative = PurePosixPath(name)
        require(not relative.is_absolute() and '..' not in relative.parts
                and relative.as_posix() == name, 'Unsafe package path')
        p = ROOT.joinpath(*relative.parts)
        require(p.is_file() and not p.is_symlink(), 'Nonregular file: ' + name)
        require(type(item['bytes']) is int and p.stat().st_size == item['bytes'], 'Size mismatch: ' + name)
        require(sha256(p) == item['sha256'], 'Digest mismatch: ' + name)
    require(sha256(ROOT/'original_packet/frozen_packet/PROOF.md') == ORIGINAL_PROOF_SHA256,
            'Original proof anchor mismatch')
    if pdf is not None:
        require(pdf.is_file() and not pdf.is_symlink(), 'Missing/nonregular PDF')
        require(sha256(pdf) == manifest['separate_pdf']['sha256'], 'Separate PDF digest mismatch')
        require(pdf.stat().st_size == manifest['separate_pdf']['bytes'], 'Separate PDF size mismatch')
    return len(expected)

def execute(script, extra=()):
    result = subprocess.run([sys.executable, '-I', str(script), *extra], cwd=script.parent,
                            text=True, capture_output=True, timeout=300)
    require(result.returncode == 0, 'Replay failed: '+str(script)+'\n'+result.stderr)
    return result.stdout

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--integrity-only', action='store_true')
    ap.add_argument('--pdf', type=Path)
    args = ap.parse_args()
    count = integrity(args.pdf)
    records = []
    if not args.integrity_only:
        with tempfile.TemporaryDirectory(prefix='three-terminal-package-') as directory:
            work = Path(directory)/'package'
            shutil.copytree(ROOT, work)
            jobs = [
                ('original_packet/verify_publication.py', ()),
                ('original_packet/mutation_tests.py', ()),
                ('reviews/proof_family/independent_checks.py', ()),
                ('reviews/computation_family/independent_structural_checks.py', ()),
            ]
            for name, extra in jobs:
                out = execute(work/name, extra)
                result = json.loads(out)
                require(result.get('result', result.get('status')) == 'PASS', 'No PASS: '+name)
                records.append({'script': name, 'status': 'PASS'})
            controls = work/'reviews/computation_family'
            shutil.copytree(work/'original_packet', controls/'submitted_working_copy')
            name = 'reviews/computation_family/optimization_and_integrity_controls.py'
            out = execute(work/name)
            result = json.loads(out)
            require(result.get('result', result.get('status')) == 'PASS', 'No PASS from controls')
            records.append({'script': name, 'status': 'PASS'})
    integrity(args.pdf)
    print(json.dumps({'status': 'PASS', 'problem_id': 30000347,
                      'payload_files': count, 'source_free': True,
                      'pdf_verified': args.pdf is not None,
                      'replayed_suites': records, 'distributed_files_unchanged': True}, indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('FAIL: '+str(error), file=sys.stderr)
        sys.exit(1)
