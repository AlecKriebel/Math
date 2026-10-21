"""Standard-library exact inventory, hashes, and frozen acceptance validation."""
import hashlib
import json
import pathlib


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def main():
    root = pathlib.Path(__file__).resolve().parent
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    expected = {}
    for entry in manifest['files']:
        name = entry['path']
        rel = pathlib.PurePosixPath(name)
        require(not rel.is_absolute() and '..' not in rel.parts and name not in expected and name != 'MANIFEST.json',
                'Invalid manifest path: ' + name)
        expected[name] = entry
    actual = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'Symlink forbidden: ' + p.name)
        if p.is_file() and p.relative_to(root).as_posix() != 'MANIFEST.json':
            actual.add(p.relative_to(root).as_posix())
    require(actual == set(expected), 'Inventory mismatch')
    total = 0
    for name, entry in expected.items():
        data = (root / name).read_bytes()
        require(len(data) == entry['bytes'], 'Byte-count mismatch: ' + name)
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'SHA-256 mismatch: ' + name)
        total += len(data)
    require(len(expected) == manifest['file_count_excluding_manifest'], 'Manifest count mismatch')
    require(total == manifest['total_bytes_excluding_manifest'], 'Manifest total mismatch')
    acceptance = json.loads((root / 'AUDIT_ACCEPTANCE.json').read_text())
    require(acceptance['overall_problem_status'] == 'UNSOLVED' and acceptance['avenues_completed'] == 5,
            'Incorrect problem scope')
    for entry in acceptance['frozen_authored_reports']:
        require(entry['file'] in expected, 'Frozen report absent')
        require(all(entry[k] == expected[entry['file']][k] for k in ('sha256', 'bytes')), 'Frozen version mismatch')
    provenance = json.loads((root / 'PROVENANCE.json').read_text())
    for entry in provenance['copies']:
        require(entry['file'] in expected, 'Provenance file absent')
        require(expected[entry['file']]['sha256'] == entry['source_sha256'] and
                expected[entry['file']]['bytes'] == entry['source_bytes'], 'Unchanged source provenance mismatch')
    print(json.dumps({'status': 'PASS', 'verified_files': len(expected), 'verified_bytes': total,
                      'overall_problem_status': 'UNSOLVED', 'frozen_reports_match': True}, indent=2))


if __name__ == '__main__':
    main()
