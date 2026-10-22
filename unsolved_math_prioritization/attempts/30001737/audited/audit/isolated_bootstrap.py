#!/usr/bin/env python3
"""External reviewed bootstrap: validate all bytes before running package code.
Use python -I -S -B isolated_bootstrap.py ROOT MANIFEST_SHA256 [ENTRY [ARGS...]].
Trust this bootstrap and its externally supplied hash; never take a pin from an
untrusted package. This is an integrity gate, not a general-purpose sandbox.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('Bootstrap requires python -I -S -B before any nonbuiltin import')
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile

FILES = {'MANIFEST.json','PUBLIC_METADATA.json','REPORT.md','SOURCES.json',
         'VERIFICATION.json','audit_checks.py','math_checks.py','verify.py','verify_corpora.py'}
ENTRIES = {'audit_checks.py','math_checks.py','verify.py','verify_corpora.py'}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def unique(pairs):
    value = {}
    for key, item in pairs:
        need(key not in value, 'Duplicate JSON key')
        value[key] = item
    return value

def snapshot(root, pin):
    # Check lexical ancestors before resolving: a symlinked parent is also refused.
    root = Path(os.path.abspath(root))
    for parent in (root, *root.parents):
        st = parent.lstat()
        need(stat.S_ISDIR(st.st_mode), 'Root or ancestor is not a real directory')
    entries = list(root.iterdir())
    need({p.name for p in entries} == FILES, 'Unexpected inventory before execution')
    data = {}
    for path in entries:
        st = path.lstat()
        need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1, 'Nonregular or aliased entry')
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        try:
            actual = os.fstat(fd)
            need(stat.S_ISREG(actual.st_mode) and actual.st_nlink == 1 and
                 (actual.st_dev, actual.st_ino) == (st.st_dev, st.st_ino), 'Entry changed during read')
            with os.fdopen(fd, 'rb', closefd=False) as source:
                data[path.name] = source.read()
        finally:
            os.close(fd)
    need(hashlib.sha256(data['MANIFEST.json']).hexdigest() == pin, 'Manifest pin mismatch')
    manifest = json.loads(data['MANIFEST.json'], object_pairs_hook=unique)
    need(set(manifest) == {'schema','files'} and manifest['schema'] == 'strict-flat-sha256-v1', 'Manifest schema')
    need(set(manifest['files']) == FILES - {'MANIFEST.json'}, 'Manifest inventory')
    for name in FILES - {'MANIFEST.json'}:
        content = data[name]
        need(manifest['files'][name] == {'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest()}, 'Payload mismatch: ' + name)
    return data

def main():
    need(len(sys.argv) >= 3, 'Expected root and external manifest SHA256')
    root, pin = sys.argv[1:3]
    entry = sys.argv[3] if len(sys.argv)>3 else 'verify.py'
    need(entry in ENTRIES, 'Unsupported entry point')
    extra = sys.argv[4:]
    data = snapshot(root, pin)
    # Run a private copy of exactly the validated bytes, avoiding a later reread
    # of mutable input. Trusted interpreter / OS / bootstrap remain assumptions.
    with tempfile.TemporaryDirectory(prefix='unitary isolated validated ') as temp:
        copied = Path(temp)/'payload'; copied.mkdir()
        for name, content in data.items():
            (copied/name).write_bytes(content)
        args = ['--root',str(copied),'--manifest-sha256',pin] if entry == 'verify.py' else (['--manifest-sha256',pin] if entry == 'audit_checks.py' else [])
        cmd = [sys.executable,'-I','-S','-B'] + (['-O'] if sys.flags.optimize else []) + [str(copied/entry)] + args + extra
        result = subprocess.run(cmd, cwd=temp, capture_output=True, text=True, timeout=240)
        sys.stdout.write(result.stdout); sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)

if __name__ == '__main__':
    main()
