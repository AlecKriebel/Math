#!/usr/bin/env python3
"""Verify this portable audit and optionally its exact frozen author input.
Uses only Python's standard library; never performs network requests or writes.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile


def digest(b):
    return hashlib.sha256(b).hexdigest()


def check_file(path, entry):
    assert path.is_file() and not path.is_symlink(), str(path)
    b = path.read_bytes()
    assert len(b) == entry['bytes'] and digest(b) == entry['sha256'], str(path)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--author-root', type=Path)
    args = p.parse_args()
    root = Path(__file__).resolve().parent.parent
    audit = root/'audit'
    m = json.loads((root/'AUDIT_MANIFEST.json').read_text())
    expected = {e['path']:e for e in m['audit_files']}
    actual = {x.relative_to(root).as_posix() for x in audit.iterdir() if x.is_file()}
    assert actual == set(expected), (actual-set(expected), set(expected)-actual)
    for path,e in expected.items():
        check_file(root/path,e)
    out = subprocess.check_output([sys.executable,'-B',str(audit/'independent_controls.py')])
    assert out == (audit/'INDEPENDENT_RESULTS.json').read_bytes()
    result = {'audit_files_verified':len(expected), 'independent_output_byte_identical':True}
    if args.author_root:
        r = args.author_root
        for e in m['author_binding']['files']:
            check_file(r/e['path'],e)
        am = json.loads((r/'AUTHOR_FREEZE.json').read_text())
        author_files = {e['path']:e for e in am['files']}
        assert {x.name for x in (r/'packet').iterdir() if x.is_file()} == set(author_files)
        for name,e in author_files.items():
            check_file(r/'packet'/name,e)
        with zipfile.ZipFile(r/'author-packet.zip') as z:
            members = {'AUTHOR_FREEZE.json'}|{'packet/'+name for name in author_files}
            assert len(z.infolist()) == len(members) and set(z.namelist()) == members
            for info in z.infolist():
                assert not info.is_dir()
                assert ((info.external_attr >> 16) & 0o170000) != 0o120000
                assert z.read(info.filename) == (r/info.filename).read_bytes()
        author_out = subprocess.check_output([sys.executable,'-B',str(r/'packet/verify.py')])
        assert author_out == (r/'packet/CONTROL_RESULTS.json').read_bytes()
        result.update({'author_files_verified':len(author_files),'author_archive_exact_match':True,
                       'author_output_byte_identical':True})
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
