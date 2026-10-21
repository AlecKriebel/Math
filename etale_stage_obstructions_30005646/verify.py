"""Fail-closed package integrity checks, not an arithmetic theorem verifier."""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
EXPECTED = {'README.md', 'SOURCE_GATE.md', 'SOURCE_METADATA.json',
            'FIVE_APPROACHES.md', 'FINITE_STAGE_LEMMA.md',
            'INDEPENDENT_OBSTRUCTION_AUDIT.md', 'FINAL_CLAIMS_ACCEPTANCE.md',
            'verify.py', 'MANIFEST.json'}

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def inventory(root):
    entries = list(root.rglob('*'))
    require(not any(p.is_symlink() for p in entries), 'Symlink in package')
    require(all(p.is_file() for p in entries), 'Unexpected directory or special entry')
    names = {p.relative_to(root).as_posix() for p in entries}
    require(names == EXPECTED, 'Strict recursive inventory mismatch')
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    require(set(manifest) == {'format', 'files'}, 'Manifest schema mismatch')
    require(manifest['format'] == 'sha256-bytes-v1', 'Manifest format mismatch')
    require(set(manifest['files']) == EXPECTED - {'MANIFEST.json'}, 'Manifest key mismatch')
    for name, spec in manifest['files'].items():
        data = (root / name).read_bytes()
        require(spec == {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()},
                'Hash/size mismatch: ' + name)

def main():
    require(sys.argv[1:] in ([], ['--inventory-only']), 'Unexpected arguments')
    inventory(ROOT)
    if sys.argv[1:]:
        print('inventory PASS')
        return
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(
        ast.parse((ROOT / 'verify.py').read_text()))), 'Optimizable assertion guard')
    controls = []
    with tempfile.TemporaryDirectory() as directory:
        for case in ('missing', 'altered', 'extra', 'nested_manifest', 'symlink',
                     'manifest_omission', 'manifest_extra', 'manifest_self_hash', 'wrong_size'):
            target = Path(directory) / case
            shutil.copytree(ROOT, target)
            if case == 'missing':
                (target / 'README.md').unlink()
            elif case == 'altered':
                with (target / 'README.md').open('ab') as stream:
                    stream.write(b'altered')
            elif case == 'extra':
                (target / 'extra.txt').write_text('extra')
            elif case == 'nested_manifest':
                (target / 'nested').mkdir()
                (target / 'nested' / 'MANIFEST.json').write_text('{}')
            elif case == 'symlink':
                (target / 'extra').symlink_to('README.md')
            else:
                path = target / 'MANIFEST.json'
                manifest = json.loads(path.read_text())
                if case == 'manifest_omission':
                    del manifest['files']['README.md']
                elif case == 'manifest_extra':
                    manifest['files']['phantom.txt'] = {'bytes': 0, 'sha256': ''}
                elif case == 'manifest_self_hash':
                    manifest['files']['MANIFEST.json'] = {'bytes': 0, 'sha256': ''}
                else:
                    manifest['files']['README.md']['bytes'] += 1
                path.write_text(json.dumps(manifest))
            for optimized in (False, True):
                result = subprocess.run(
                    [sys.executable, '-B'] + (['-O'] if optimized else []) +
                    [str(target / 'verify.py'), '--inventory-only'],
                    capture_output=True, text=True, timeout=30,
                    env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
                require(result.returncode != 0 and 'RuntimeError:' in result.stderr,
                        'Integrity mutant survived: ' + case)
                controls.append({'case': case, 'optimized': optimized, 'rejected': True})
    print(json.dumps({'inventory': 'PASS', 'explicit_guards': 'PASS',
                      'scope': 'Integrity only; no computational mathematical claims',
                      'integrity_controls': controls}, indent=2))

if __name__ == '__main__':
    main()
