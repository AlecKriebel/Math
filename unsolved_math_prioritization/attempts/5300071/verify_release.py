#!/usr/bin/env python3
"""Verify the publication allowlist, hashes and frozen ZIP bindings, offline."""
import hashlib
import json
import pathlib
import zipfile


def main():
    root = pathlib.Path(__file__).resolve().parent
    manifest = json.loads((root / 'SHA256SUMS.json').read_text())
    expected = set(manifest) | {'SHA256SUMS.json'}
    entries = list(root.rglob('*'))
    assert not any(p.is_symlink() for p in entries), 'symlinks are not allowed'
    actual = {p.relative_to(root).as_posix() for p in entries if p.is_file()}
    assert actual == expected, ('unexpected or missing files', actual ^ expected)
    expected_dirs = set()
    for name in expected:
        expected_dirs.update(str(p) for p in pathlib.PurePosixPath(name).parents if str(p) != '.')
    actual_dirs = {p.relative_to(root).as_posix() for p in entries if p.is_dir()}
    assert actual_dirs == expected_dirs, ('unexpected directories', actual_dirs ^ expected_dirs)
    for name, info in manifest.items():
        data = (root / name).read_bytes()
        assert len(data) == info['bytes'], name
        assert hashlib.sha256(data).hexdigest() == info['sha256'], name
    archives = [
        ('rank650-5300071-author-freeze.zip', 'submission',
         '291263a5a2454913eb161b8361acfdb56cf6840908eb0cdc995716061b122fb2'),
        ('rank650-5300071-independent-audit.zip', 'audit-independent',
         '22295eda6631ac061069c6fd593fcbd11b026ba75e0a9ce48a5ccb7bac7f5f8f'),
    ]
    for archive, directory, expected_sha in archives:
        data = (root / archive).read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected_sha, archive
        names = {p.name for p in (root / directory).iterdir()}
        with zipfile.ZipFile(root / archive) as z:
            assert len(z.namelist()) == len(names), archive
            assert set(z.namelist()) == names, archive
            for name in names:
                assert z.read(name) == (root / directory / name).read_bytes(), name
    print(json.dumps({'verified': True, 'publication_files': len(expected),
                      'frozen_archives_bound': 2, 'status': 'unsolved',
                      'substantive_approaches_used': 5}, sort_keys=True))


if __name__ == '__main__':
    main()
