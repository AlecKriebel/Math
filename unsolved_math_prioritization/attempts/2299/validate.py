"""Offline verification of frozen authored audit package. Python 3 standard library."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

def require(value, message):
    if not value:
        raise RuntimeError(message)

def inventory(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'root must be a real directory')
    files = {}
    directories = []
    def walk(directory):
        for entry in sorted(directory.iterdir()):
            mode = entry.lstat().st_mode
            rel = entry.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                directories.append(rel)
                walk(entry)
            elif stat.S_ISREG(mode):
                data = entry.read_bytes()
                files[rel] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
            else:
                raise RuntimeError('Rejected symlink or special file: ' + rel)
    walk(root)
    return {'directories': sorted(directories), 'files': files}

def validate(root):
    actual = inventory(root)  # Reject unsafe types before reading any manifest or executing code.
    require('FROZEN_RECEIPT.json' in actual['files'], 'missing frozen receipt')
    receipt = json.loads((root/'FROZEN_RECEIPT.json').read_text())
    del actual['files']['FROZEN_RECEIPT.json']
    require(receipt['inventory'] == actual, 'Frozen inventory mismatch')
    print('PASS recursive exact inventory, byte counts and SHA-256; no symlinks or special files', flush=True)
    expected = json.loads((root/'audit/INDEPENDENT_ARITHMETIC.json').read_text())
    for flags in ([], ['-O']):
        command = [sys.executable, '-B'] + flags + [str(root/'audit/independent_arithmetic.py')]
        result = subprocess.run(command, capture_output=True, text=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'}, check=False)
        print('COMMAND:', 'python3 -B ' + ('-O ' if flags else '') + 'audit/independent_arithmetic.py')
        print('STDOUT:\n' + result.stdout, end='')
        print('STDERR:\n' + result.stderr, end='')
        print('EXIT:', result.returncode)
        require(result.returncode == 0, 'arithmetic failed')
        require(json.loads(result.stdout) == expected, 'Arithmetic output differs from accepted reference')
    require(len(expected['small']) == 7 and len(expected['uniform_finite']) == 18, 'finite range mismatch')
    require(expected['lower_window'] == {'range':[11,377], 'count':367, 'failures':0, 'minimum_slack':3, 'first_minimum_r':20}, 'lower window mismatch')
    print('PASS normal and optimized exact arithmetic, reference output and range checks')
    print('SCOPE: existing prior result; corrected mathematical audit only. No local Lean build or inspected axiom output.')

if __name__ == '__main__':
    try:
        require(len(sys.argv) <= 2, 'usage: python3 -B validate.py [package-directory]')
        root = Path(sys.argv[1]).absolute() if len(sys.argv) == 2 else Path(__file__).absolute().parent
        validate(root)
    except Exception as error:
        print('FAIL:', error, file=sys.stderr)
        sys.exit(1)
