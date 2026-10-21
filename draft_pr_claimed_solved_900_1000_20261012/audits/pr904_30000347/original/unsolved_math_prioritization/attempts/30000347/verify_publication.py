#!/usr/bin/env python3
"""Source-free publication checks. Explicit guards remain active under python -O."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parent
ANCHORS = {
    'frozen_packet/FROZEN_MANIFEST.json': 'b13c9cee3e806a263ba0e24b2838599692727ea48d26977d4fca714e1e30d273',
    'frozen_packet/PROOF.md': 'f31b19b8e4286e0104ed1e272f5cbc4a39e20aea78aa30334466f5b44e5830f7',
    'AUTHOR_FREEZE.tar.gz': 'f05e41d5a419c2faffc584e495da799bc43b306850ccd50c4f1f8824ab224996',
    'independent_reduction_audit/AUDIT_MANIFEST.json': '94f1d30ec5a49b9cac7403f19c6021af79dd81379ec13948c879a38c34dd1fad',
    'independent_audit_2/AUDIT_MANIFEST.json': '2993c18ccdb759aeb134c527fe5d47ece9b0717de0f2333a432086374fcdace3',
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def safe_path(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and not p.is_absolute() and '..' not in p.parts
            and p.as_posix() == name and bool(p.parts), 'Unsafe manifest path')
    return ROOT.joinpath(*p.parts)

def check_files(parent, files):
    require(isinstance(files, dict) and files, 'Missing file map')
    for name, expected in files.items():
        p = safe_path((PurePosixPath(parent) / name).as_posix()) if parent else safe_path(name)
        require(p.is_file() and not p.is_symlink(), 'Missing or nonregular file: ' + str(p))
        data = p.read_bytes()
        require(type(expected['bytes']) is int and len(data) == expected['bytes'], 'Byte count mismatch: ' + name)
        require(digest(data) == expected['sha256'], 'SHA-256 mismatch: ' + name)

def integrity():
    manifest = json.loads((ROOT / 'PUBLIC_MANIFEST.json').read_text())
    require(manifest.get('problem_id') == 30000347 and manifest.get('status') == 'claimed_solved'
            and manifest.get('turns') == '1/5', 'Wrong publication identity')
    files = manifest['files']
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    require(actual == set(files) | {'PUBLIC_MANIFEST.json'}, 'Publication file-set mismatch')
    check_files('', files)
    for name, expected in ANCHORS.items():
        require(digest(safe_path(name).read_bytes()) == expected, 'Frozen anchor mismatch: ' + name)
    for parent, name in [('frozen_packet', 'FROZEN_MANIFEST.json'),
                         ('independent_reduction_audit', 'AUDIT_MANIFEST.json'),
                         ('independent_audit_2', 'AUDIT_MANIFEST.json')]:
        original = json.loads((ROOT / parent / name).read_text())
        check_files(parent, original['files'])
    # Inspect archive directly, without extracting untrusted member paths.
    frozen = {p.relative_to(ROOT / 'frozen_packet').as_posix(): p.read_bytes()
              for p in (ROOT / 'frozen_packet').rglob('*') if p.is_file()}
    archived = {}
    with tarfile.open(ROOT / 'AUTHOR_FREEZE.tar.gz', 'r:gz') as tf:
        for member in tf.getmembers():
            if member.isdir():
                continue
            require(member.isfile(), 'Nonregular archive member')
            path = PurePosixPath(member.name)
            require(path.parts[0] == 'three_terminal_30000347' and '..' not in path.parts,
                    'Unexpected archive path')
            name = PurePosixPath(*path.parts[1:]).as_posix()
            require(name not in archived, 'Duplicate archive member')
            archived[name] = tf.extractfile(member).read()
    require(archived == frozen, 'Archive/frozen-directory mismatch')
    return len(files)

def normalized(value):
    # Only explicitly nondeterministic timing/platform fields are ignored.
    return {key: entry for key, entry in value.items()
            if key not in {'runtime_seconds', 'seconds', 'elapsed_seconds', 'python'}}

def replay():
    jobs = [
        ('frozen_packet/checks/check_reduction.py', 'frozen_packet/checks/check_results.json', 'result'),
        ('independent_reduction_audit/independent_check.py', 'independent_reduction_audit/independent_check_results.json', 'result'),
        ('independent_audit_2/fresh_controls.py', 'independent_audit_2/fresh_control_results.json', 'status'),
    ]
    records = []
    with tempfile.TemporaryDirectory(prefix='three-terminal-publication-') as directory:
        for index, (script, result, status) in enumerate(jobs):
            work = Path(directory) / str(index) / 'packet'
            shutil.copytree(ROOT, work)
            expected = json.loads((ROOT / result).read_text())
            # -I ignores PYTHONOPTIMIZE and other PYTHON* environment settings.
            # No -O is passed: original mathematical assertions always run.
            run = subprocess.run([sys.executable, '-I', str(work / script)], cwd=work,
                                 text=True, capture_output=True, timeout=180)
            require(run.returncode == 0, 'Replay failed: ' + script + '\n' + run.stderr)
            current = json.loads((work / result).read_text())
            require(current.get(status) == 'PASS', 'Replay did not pass: ' + script)
            require(normalized(current) == normalized(expected), 'Deterministic result mismatch: ' + script)
            records.append({'script': script, 'result': 'PASS', 'deterministic_results_match': True,
                            'counts': current.get('checks', current.get('counts'))})
    return records

def main():
    require(sys.argv[1:] in ([], ['--integrity-only']), 'Usage: verify_publication.py [--integrity-only]')
    count = integrity()
    records = [] if sys.argv[1:] else replay()
    integrity()  # Original published files must remain byte-identical.
    print(json.dumps({'result': 'PASS', 'problem_id': 30000347,
                      'verified_payload_files': count, 'source_free': True,
                      'replayed_suites': records, 'originals_unchanged': True}, indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
