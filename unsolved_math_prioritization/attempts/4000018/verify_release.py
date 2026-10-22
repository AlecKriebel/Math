#!/usr/bin/env python3
"""Verify this frozen partial-results packet with Python's standard library."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def safe(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and str(p) == name and not p.is_absolute()
            and name not in ('', '.') and '..' not in p.parts, 'Unsafe path')
    return name

def read_manifest(base, name):
    doc = json.loads((base / name).read_text())
    names = set()
    for item in doc['files']:
        rel = safe(item['path'])
        require(rel not in names, 'Duplicate manifest path')
        names.add(rel)
        path = base / rel
        require(path.is_file() and not path.is_symlink(), 'Missing or linked file: '+rel)
        data = path.read_bytes()
        require(len(data) == item['bytes'] and digest(data) == item['sha256'], 'Manifest mismatch: '+rel)
    return names

def verify_sums(base):
    seen = set()
    for line in (base / 'SHA256SUMS').read_text().splitlines():
        expected, rel = line.split(None, 1)
        rel = safe(rel.lstrip('*'))
        require(rel not in seen, 'Duplicate checksum path')
        seen.add(rel)
        require(digest((base / rel).read_bytes()) == expected, 'Checksum mismatch: '+rel)
    return len(seen)

def verify():
    require(not (ROOT / 'PUBLICATION_MANIFEST.json').is_symlink(), 'Linked manifest')
    names = read_manifest(ROOT, 'PUBLICATION_MANIFEST.json')
    actual = set()
    for path in ROOT.rglob('*'):
        require(not path.is_symlink(), 'Symlink present')
        if path.is_file():
            actual.add(path.relative_to(ROOT).as_posix())
        else:
            require(path.is_dir(), 'Nonregular object')
    require(actual == names | {'PUBLICATION_MANIFEST.json'}, 'Unexpected or missing file')
    for archive, prefix, expected, size in (
        ('rank663-4000018-authored-packet.zip', 'author_packet', '82f9acc92840eaef8ad85c7473817ed3eca5107ba4c851aaabd23c874eb2714e', 26133),
        ('rank663-4000018-independent-audit.zip', '', 'd3507a9a8767eda60109f851f442445b1ee2baac4bcd0435b35d0912da8a8690', 14956),
    ):
        data = (ROOT / archive).read_bytes()
        require(digest(data) == expected and len(data) == size, 'Archive mismatch')
        with zipfile.ZipFile(ROOT / archive) as z:
            members = z.namelist()
            require(len(members) == len(set(members)), 'Duplicate archive member')
            expected_names = set()
            for member in members:
                safe(member)
                target = '/'.join(filter(None, (prefix, member)))
                expected_names.add(target)
                require(z.read(member) == (ROOT / target).read_bytes(), 'Archive extraction mismatch')
            scope = prefix + '/' if prefix else 'independent_audit/'
            require(expected_names == {n for n in names if n.startswith(scope)}, 'Archive file-set mismatch')
    author = ROOT / 'author_packet'
    audit = ROOT / 'independent_audit'
    require(len(read_manifest(author, 'AUTHOR_MANIFEST.json')) == 11, 'Author manifest size')
    require(len(read_manifest(audit, 'AUDIT_MANIFEST.json')) == 8, 'Audit manifest size')
    require(verify_sums(author) == 12, 'Author checksum count')
    verify_sums(audit)
    result = json.loads((audit / 'AUDIT_RESULT.json').read_text())
    require(result['original_problem_status'] == 'UNSOLVED' and result['approaches_completed'] == 5
            and result['claims_audited'] == 7 and not result['mandatory_corrections']
            and not result['blocking_findings'], 'Audit gate mismatch')
    outputs = []
    for script, expected_file, expected_count in (
        (author / 'authored/verify_exact.py', author / 'authored/CONTROL_RESULT.json', 28156),
        (audit / 'independent_checks.py', audit / 'INDEPENDENT_CONTROLS.json', 52820),
    ):
        proc = subprocess.run([sys.executable, '-B', str(script)], cwd=script.parent,
                              check=True, text=True, capture_output=True)
        got = json.loads(proc.stdout)
        require(got == json.loads(expected_file.read_text()), 'Replay output mismatch')
        require(got['status'] == 'PASS' and got['total_assertions'] == expected_count, 'Replay count mismatch')
        outputs.append(expected_count)
    return {'status':'PASS', 'target':'4000018 / AMR-039-0018',
            'publication_files':len(actual), 'frozen_author_files':13,
            'frozen_audit_files':10, 'author_assertions':outputs[0],
            'independent_assertions':outputs[1], 'replays_match_frozen_records':True,
            'original_problem_status':'UNSOLVED', 'approaches_completed':5}

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2, sort_keys=True))
