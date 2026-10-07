#!/usr/bin/env python3
"""Fail-closed inventory and isolated exact replay; Python standard library only."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parent
FROZEN = {
    'public_candidate/MANIFEST.json': '70a4f39602d298d2fbcc7284259660e92ab6fff65bd81e38b1e619c66fc17a99',
    'independent_audit/AUDIT_MANIFEST.json': '2a7d429f2fc3df24af048893b512867a232734bd4ff7d10075c5e268cdf8e043',
    'independent_audit/ACCEPTANCE_REPORT.txt': '3918b45b34c3c9c45467101841e60846f39b2adeca5b9d7f8811ecbbe3b84a37',
    'authored_candidate.tar.gz': '39569a25dc07224ee3494a9ba7e44cced3063653127e315c2764fe392e02fed7',
}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def manifest_records(path):
    data = json.loads(path.read_bytes())
    records = {}
    for row in data['files']:
        name = row['path']
        p = PurePosixPath(name)
        require(isinstance(name, str) and p.as_posix() == name and not p.is_absolute()
                and name not in ('', '.') and '..' not in p.parts and '\\' not in name,
                'unsafe manifest path')
        require(name not in records, 'duplicate manifest path')
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'invalid size')
        require(len(row['sha256']) == 64 and all(c in '0123456789abcdef' for c in row['sha256']),
                'invalid digest')
        records[name] = row
    return records

def check_records(base, rows):
    for name, row in rows.items():
        data = (base / name).read_bytes()
        require(len(data) == row['bytes'] and sha(data) == row['sha256'],
                'integrity mismatch: ' + name)

def inventory(root):
    names = set()
    for p in root.rglob('*'):
        mode = p.lstat().st_mode
        require(stat.S_ISDIR(mode) or stat.S_ISREG(mode), 'nonregular object: ' + str(p))
        if stat.S_ISREG(mode):
            names.add(p.relative_to(root).as_posix())
    return names

def main():
    names = inventory(ROOT)
    rows = manifest_records(ROOT / 'PUBLICATION_MANIFEST.json')
    require(names == set(rows) | {'PUBLICATION_MANIFEST.json'}, 'publication inventory mismatch')
    check_records(ROOT, rows)
    for name, expected in FROZEN.items():
        require(sha((ROOT / name).read_bytes()) == expected, 'frozen anchor mismatch: ' + name)
    original = manifest_records(ROOT / 'public_candidate/MANIFEST.json')
    audit = manifest_records(ROOT / 'independent_audit/AUDIT_MANIFEST.json')
    require(inventory(ROOT / 'public_candidate') == set(original) | {'MANIFEST.json'},
            'author inventory mismatch')
    require(inventory(ROOT / 'independent_audit') == set(audit) | {'AUDIT_MANIFEST.json'},
            'audit inventory mismatch')
    check_records(ROOT / 'public_candidate', original)
    check_records(ROOT / 'independent_audit', audit)
    archive_names = set()
    with tarfile.open(ROOT / 'authored_candidate.tar.gz', 'r:gz') as archive:
        for member in archive.getmembers():
            require(member.isfile() and member.name in set(original) | {'MANIFEST.json'},
                    'unsafe or unexpected archive member')
            require(member.name not in archive_names, 'duplicate archive member')
            archive_names.add(member.name)
            require(archive.extractfile(member).read() == (ROOT / 'public_candidate' / member.name).read_bytes(),
                    'archive mismatch: ' + member.name)
    require(archive_names == set(original) | {'MANIFEST.json'}, 'archive inventory mismatch')
    runs = []
    with tempfile.TemporaryDirectory(prefix='plane-partials-replay-') as temporary:
        dest = Path(temporary) / 'packet'
        shutil.copytree(ROOT, dest)
        for flags in ([], ['-O']):
            for script, expected in [
                ('public_candidate/verify_math.py', 'checks/author.stdout.json'),
                ('public_candidate/verify_integrity.py', 'checks/integrity.stdout.json'),
                ('independent_audit/independent_checks.py', 'independent_audit/independent_checks.json'),
            ]:
                run = subprocess.run([sys.executable, '-B'] + flags + [str(dest / script)],
                                     cwd=temporary, capture_output=True, check=True, timeout=120)
                require(not run.stderr, 'unexpected replay stderr')
                require(run.stdout == (dest / expected).read_bytes(), 'stdout mismatch: ' + script)
                if script.endswith('/verify_math.py'):
                    require(json.loads(run.stdout) == json.loads((dest / 'public_candidate/checks_result.json').read_bytes()),
                            'author JSON mismatch')
                runs.append({'script': script, 'optimized': bool(flags), 'stdout_sha256': sha(run.stdout)})
        require(inventory(dest) == names, 'replay changed inventory')
        check_records(dest, rows)
    check_records(ROOT, rows)
    print(json.dumps({'status': 'PASS', 'publication_files': len(names), 'frozen_author_files': 10,
                      'frozen_audit_files': 4, 'archive_members': len(archive_names), 'replays': runs,
                      'full_conjecture_status': 'unsolved, 5/5',
                      'scope': 'integrity and exact arithmetic; not a full-conjecture certificate'}, indent=2))

if __name__ == '__main__':
    main()
