#!/usr/bin/env python3
"""Regression for the second review's blocking nonregular-index counterexample."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time

AUDIT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    require(args.label.isalnum(), 'Alphanumeric review label required')
    assembly = json.loads((AUDIT / ('LOCAL_PR_ASSEMBLY_' + args.label.upper() + '.json')).read_text())
    tree = Path(assembly['tree'])
    pre = tree / 'publication_20261014/preprint'
    inner = tree / 'publication_20261014/verification_package'
    pin = hashlib.sha256((inner / 'package_index.json').read_bytes()).hexdigest()
    before = {p.relative_to(tree).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in tree.rglob('*') if p.is_file()}
    cases = []
    for optimized in [False, True]:
        for kind in ['fifo', 'socket', 'directory', 'symlink', 'broken_symlink', 'checker_fifo']:
            with tempfile.TemporaryDirectory(prefix='k826-', dir=Path('/tmp').resolve()) as temporary:
                temporary = Path(temporary).resolve()
                root = temporary / 'input kit'
                shutil.copytree(inner, root)
                target = root / ('verify_package.py' if kind == 'checker_fifo' else 'package_index.json')
                original = target.read_bytes()
                target.unlink()
                endpoint = None
                if kind in {'fifo', 'checker_fifo'}:
                    os.mkfifo(target)
                elif kind == 'socket':
                    endpoint = socket.socket(socket.AF_UNIX)
                    endpoint.bind(str(target))
                elif kind == 'directory':
                    target.mkdir()
                else:
                    destination = temporary / 'external regular index'
                    if kind == 'symlink':
                        destination.write_bytes(original)
                    target.symlink_to(destination)
                output = temporary / 'fresh output'
                started = time.monotonic()
                try:
                    result = subprocess.run(
                        [sys.executable, '-I', '-S', '-B', *(['-O'] if optimized else []),
                         str(pre / 'build_verification.py'), '--from-package', str(root),
                         '--trusted-index-sha256', pin, '--output-root', str(output)],
                        cwd='/', capture_output=True, text=True, timeout=5)
                finally:
                    if endpoint is not None:
                        endpoint.close()
                expected = 'trusted input verifier binding failed' if kind == 'checker_fifo' else 'input index must be a regular file'
                require(result.returncode != 0 and not result.stdout and expected in result.stderr,
                        'Nonregular input did not reject safely: ' + kind)
                require(not output.exists(), 'Rejected input created output')
                cases.append({'optimized': optimized, 'kind': kind, 'returncode': result.returncode,
                              'elapsed_seconds': time.monotonic() - started,
                              'diagnostic': result.stderr.splitlines()[-1], 'output_absent': True})
    after = {p.relative_to(tree).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in tree.rglob('*') if p.is_file()}
    require(before == after, 'Sealed assembly changed')
    receipt = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'status': 'PASS', 'label': args.label, 'cases': cases,
               'expected_prompt_rejections': len(cases), 'sealed_assembly_unchanged': True,
               'builder_sha256': hashlib.sha256((pre / 'build_verification.py').read_bytes()).hexdigest(),
               'index_sha256': pin, 'operating_system_sandbox_claimed': False}
    (AUDIT / ('BUILDER_NONREGULAR_REGRESSION_' + args.label.upper() + '.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: value for key, value in receipt.items() if key != 'cases'}))


if __name__ == '__main__':
    main()
