#!/usr/bin/env python3
"""Standalone audit authentication and meaningful negative controls. No assertions."""
import argparse
import datetime
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import stat
import tempfile

class AuditFailure(RuntimeError):
    pass

def require(condition, message):
    if not condition:
        raise AuditFailure(message)

def digest(path):
    data = path.read_bytes()
    return {'path': None, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def inventory(root, exclude):
    result = []
    for path in sorted(root.rglob('*')):
        require(not path.is_symlink(), 'symlink retained')
        if path.is_file() and path != exclude:
            row = digest(path)
            row['path'] = str(path.relative_to(root))
            row['mode'] = '0444'
            result.append(row)
    return result

def verify(root, manifest):
    root, manifest = root.resolve(), manifest.resolve()
    require(manifest.parent == root / 'public', 'manifest outside own public folder')
    data = json.loads(manifest.read_text())
    require(data.get('schema') == 'priority-source-lineage-final-seal-v1', 'wrong schema')
    listed = data.get('inventory')
    require(isinstance(listed, list), 'inventory missing')
    names = [row.get('path') for row in listed]
    require(len(set(names)) == len(names), 'duplicate manifest path')
    for name in names:
        require(isinstance(name, str) and not Path(name).is_absolute() and '..' not in Path(name).parts,
                'unsafe manifest path')
    actual = inventory(root, manifest)
    require(set(names) == {row['path'] for row in actual}, 'incomplete retained-file inventory')
    for row in listed:
        path = root / row['path']
        got = digest(path)
        require(got['size'] == row.get('size'), 'size mismatch: ' + row['path'])
        require(got['sha256'] == row.get('sha256'), 'hash mismatch: ' + row['path'])
        require(stat.S_IMODE(path.stat().st_mode) == 0o444, 'not sealed0444: ' + row['path'])
    require(stat.S_IMODE(manifest.stat().st_mode) == 0o444, 'manifest not sealed0444')
    public = data.get('public_allowlist', [])
    require(len(set(public)) == len(public), 'duplicate public path')
    for name in public:
        require(isinstance(name, str) and name.startswith('public/') and '..' not in Path(name).parts,
                'private source or unsafe path in public allowlist')
        require(name in names or name == str(manifest.relative_to(root)), 'allowlisted file absent')
    return {'verified_retained_files': len(listed) + 1,
            'manifest_size': manifest.stat().st_size,
            'manifest_sha256': digest(manifest)['sha256'],
            'all_retained_regular_files_mode': '0444'}

def seal(root, manifest, allowlist):
    root = root.resolve()
    manifest = manifest.resolve()
    require(not manifest.exists(), 'refusing to overwrite seal')
    require(manifest.parent == root / 'public', 'seal outside own public folder')
    public = json.loads(allowlist.read_text())['public_files']
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'symlink retained')
        if path.is_file():
            path.chmod(0o444)
    data = {'schema': 'priority-source-lineage-final-seal-v1',
            'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'inventory': inventory(root, manifest),
            'public_allowlist': public,
            'self_entry': {'path': str(manifest.relative_to(root)),
                           'hash': 'reported externally after write to avoid a hash cycle'},
            'classification_rule': 'Only explicit public_allowlist may be released. All other retained files are PRIVATE.'}
    manifest.write_text(json.dumps(data, indent=2) + '\n')
    manifest.chmod(0o444)
    return verify(root, manifest)

def self_test(root):
    receipt = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'tests': []}
    folder = Path(tempfile.mkdtemp(prefix='lineage_controls_', dir=root / 'private'))
    try:
        (folder / 'public').mkdir()
        (folder / 'private').mkdir()
        own = folder / 'public' / 'own.md'
        source = folder / 'private' / 'synthetic_source.bin'
        own.write_text('own safe test text\n')
        source.write_bytes(b'synthetic private source fixture')
        allow = folder / 'public' / 'allow.json'
        allow.write_text(json.dumps({'public_files': ['public/own.md', 'public/allow.json', 'public/seal.json']}))
        manifest = folder / 'public' / 'seal.json'
        positive = seal(folder, manifest, allow)
        require(positive['verified_retained_files'] == 4, 'positive inventory count wrong')
        receipt['tests'].append({'test': 'complete exact inventory, hashes, sizes and0444', 'result': 'PASS'})
        original = manifest.read_bytes()
        def negative(label, mutate, cleanup, reason):
            mutate()
            caught = None
            try:
                verify(folder, manifest)
            except AuditFailure as error:
                caught = str(error)
            cleanup()
            require(caught is not None and reason in caught, 'negative control not rejected: ' + label)
            receipt['tests'].append({'test': label, 'result': 'REJECTED_AS_REQUIRED', 'reason': caught})
        extra = folder / 'private' / 'omitted.bin'
        negative('unlisted retained source must fail', lambda: extra.write_bytes(b'omitted'), lambda: extra.unlink(), 'incomplete')
        before = source.read_bytes()
        def change():
            source.chmod(0o644)
            source.write_bytes(b'x' * len(before))
            source.chmod(0o444)
        def restore():
            source.chmod(0o644)
            source.write_bytes(before)
            source.chmod(0o444)
        negative('same-size source corruption must fail', change, restore, 'hash mismatch')
        negative('writeable retained artifact must fail', lambda: own.chmod(0o644), lambda: own.chmod(0o444), 'not sealed0444')
        def manifest_change(kind):
            data = json.loads(original)
            if kind == 'private':
                data['public_allowlist'].append('private/synthetic_source.bin')
            else:
                data['inventory'][0]['path'] = '../outside'
            manifest.chmod(0o644)
            manifest.write_text(json.dumps(data))
            manifest.chmod(0o444)
        def manifest_restore():
            manifest.chmod(0o644)
            manifest.write_bytes(original)
            manifest.chmod(0o444)
        negative('semantic source leak must fail', lambda: manifest_change('private'), manifest_restore, 'private source')
        negative('outside path must fail', lambda: manifest_change('outside'), manifest_restore, 'unsafe manifest path')
        # Exact algebra catches a misleading reversal of fast/slow seed roles.
        for ratio in [Fraction(1, 10), Fraction(1, 3), Fraction(3, 4), Fraction(99, 100)]:
            threshold = 1 - ratio
            for alpha in [threshold / 2, threshold, (1 + threshold) / 2]:
                fast_final_exponent = (1 - alpha) / ratio
                require((fast_final_exponent < 1) == (alpha > threshold), 'ADMP winning-regime algebra wrong')
                slow_losing_exponent = alpha + ratio
                require((slow_losing_exponent < 1) == (alpha < threshold), 'ADMP losing-regime algebra wrong')
            wrong = (1 + threshold) / 2 < threshold
            require(not wrong, 'reversed winning inequality accepted')
        receipt['tests'].append({'test': 'ADMP fast-root/slow-many role reversal, exact rational exponents', 'result': 'PASS; reversed regime rejected'})
        receipt['scope'] = 'Authenticates artifacts and checks elementary regime algebra; does not validate a stochastic limit by computation.'
        return receipt
    finally:
        for path in folder.rglob('*'):
            if path.is_file():
                path.chmod(0o644)
        shutil.rmtree(folder)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--receipt', type=Path)
    parser.add_argument('--verify', type=Path)
    parser.add_argument('--seal', type=Path)
    parser.add_argument('--allowlist', type=Path)
    args = parser.parse_args()
    require(sum([args.self_test, args.verify is not None, args.seal is not None]) == 1, 'select exactly one operation')
    if args.self_test:
        result = self_test(args.root)
        if args.receipt:
            require(not args.receipt.exists(), 'refusing to overwrite receipt')
            args.receipt.write_text(json.dumps(result, indent=2) + '\n')
    elif args.verify:
        result = verify(args.root, args.verify)
    else:
        require(args.allowlist is not None, 'allowlist required')
        result = seal(args.root, args.seal, args.allowlist)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
