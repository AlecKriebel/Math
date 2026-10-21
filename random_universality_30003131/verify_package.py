"""Read-only package integrity and finite-check verifier; not a proof checker."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    root = Path(__file__).resolve().parent
    manifest_path = root / 'MANIFEST.json'
    require(manifest_path.is_file() and not manifest_path.is_symlink(), 'Non-regular manifest')
    manifest = json.loads(manifest_path.read_text())
    records = manifest['files']
    names = [record['name'] for record in records]
    require(len(names) == len(set(names)), 'Duplicate manifest names')
    require(all(Path(n).name == n and n not in ('.', '..', 'MANIFEST.json') for n in names), 'Unsafe manifest name')
    actual = {p.name for p in root.iterdir()}
    require(actual == set(names) | {'MANIFEST.json'}, 'Extra or missing package entries')
    for record in records:
        path = root / record['name']
        require(path.is_file() and not path.is_symlink(), 'Non-regular package entry')
        data = path.read_bytes()
        require(len(data) == record['bytes'], 'Size mismatch: ' + path.name)
        require(hashlib.sha256(data).hexdigest() == record['sha256'], 'Hash mismatch: ' + path.name)
    expected = (root / 'CHECK_RESULTS.json').read_bytes()
    for flags in ([], ['-O']):
        result = subprocess.run([sys.executable, *flags, str(root / 'check_audit.py')], capture_output=True, check=True)
        require(not result.stderr, 'Unexpected checker stderr')
        require(result.stdout == expected, 'Finite-check output mismatch')
    print('PASS: package inventory/hashes and normal/-O finite-check outputs; not an analytic proof certificate.')


if __name__ == '__main__':
    main()
