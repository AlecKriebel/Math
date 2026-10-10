#!/usr/bin/env python3
"""Authenticate this wrapper externally before use. Finite replay is not a proof."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECTED: use python -I -S -B [-O|-OO] verify_publication.py PIN PACKET')
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import tempfile

FILES = set(['ACCEPTANCE.md', 'README.md', 'RESEARCH_LOG.md', 'independent_audit_b/public/ACCEPTANCE.json', 'independent_audit_b/public/AUTHOR_FREEZE_VERIFICATION.json', 'independent_audit_b/public/CITATION_SCOPE_NOTE.md', 'independent_audit_b/public/FULL_REPORT.md', 'independent_audit_b/public/INDEPENDENT_CHECKS.json', 'independent_audit_b/public/MANIFEST.json', 'independent_audit_b/public/README.md', 'independent_audit_b/public/SOURCE_METADATA.json', 'independent_audit_b/public/independent_checks.py', 'independent_audit_b/public/verify_audit.py', 'independent_global_audit/public/ACCEPTANCE.json', 'independent_global_audit/public/GLOBAL_AUDIT.md', 'independent_global_audit/public/INDEPENDENT_CONTROLS.json', 'independent_global_audit/public/MANIFEST.json', 'independent_global_audit/public/README.md', 'independent_global_audit/public/SOURCE_METADATA.json', 'independent_global_audit/public/independent_controls.py', 'independent_global_audit/public/verify_audit_packet.py', 'mutation_tests.py', 'public/APPROACH_LEDGER.md', 'public/INHERITED_CHECK_SUMMARY.json', 'public/MANIFEST.json', 'public/PROOF.md', 'public/README.md', 'public/SOURCE_METADATA.json', 'public/VERIFICATION.json', 'public/verify_math.py', 'public/verify_packet.py', 'verify_publication.py'])
DIRS = {'public', 'independent_global_audit', 'independent_global_audit/public',
        'independent_audit_b', 'independent_audit_b/public'}
FROZEN = {
    'public': '7df56d745e4c57a30d0303388b1adda3e52d1c99190d2f96fe50b6d616b1cf3f',
    'independent_global_audit/public': '22d1bab327e70db3d594c2580f592256bb342bd33c1081fa07beb1c197f0edff',
    'independent_audit_b/public': '8bbb5b62a4610881e7b1f78a52f7c208723529304dd0e8ab341a1be9f1283459',
}
PROOF = {'bytes': 17635, 'sha256': 'a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2'}
AUTHOR_MANIFEST = {'bytes': 1433, 'sha256': FROZEN['public']}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result

def parse(raw):
    return json.loads(raw, object_pairs_hook=unique)

def valid_path(name):
    return (isinstance(name, str) and bool(name) and '\\' not in name
            and not name.startswith('/') and all(p not in ('', '.', '..') for p in name.split('/'))
            and PurePosixPath(name).as_posix() == name)

def check_record(raw, row, label):
    require(type(row.get('bytes')) is int and len(raw) == row['bytes']
            and sha(raw) == row.get('sha256'), 'Payload mismatch: ' + label)

def integrity(root, pin):
    require(len(pin) == 64 and all(c in '0123456789abcdef' for c in pin), 'Malformed external pin')
    require(not root.is_symlink() and root.is_dir(), 'Invalid or linked packet root')
    files, directories = set(), set()
    def walk(parent):
        for entry in os.scandir(parent):
            path = Path(entry.path)
            name = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                require(name in DIRS, 'Unexpected directory: ' + name)
                directories.add(name)
                walk(path)
            else:
                require(stat.S_ISREG(mode), 'Linked or special entry: ' + name)
                files.add(name)
    walk(root)
    require(files == FILES | {'PUBLIC_MANIFEST.json'} and directories == DIRS, 'Closed inventory mismatch')
    raw = (root / 'PUBLIC_MANIFEST.json').read_bytes()
    require(sha(raw) == pin, 'External manifest anchor mismatch')
    manifest = parse(raw)
    require(set(manifest) == {'schema', 'problem_id', 'files'}
            and manifest['schema'] == 'statistical-embedding-publication-v1'
            and manifest['problem_id'] == 6000001, 'Wrong publication schema or target')
    rows = manifest['files']
    require(isinstance(rows, list) and len(rows) == len(FILES), 'Invalid inventory size')
    snapshot = {}
    for row in rows:
        require(isinstance(row, dict) and set(row) == {'path', 'bytes', 'sha256'}, 'Malformed entry')
        name = row['path']
        require(valid_path(name) and name in FILES and name not in snapshot, 'Unsafe or duplicate path')
        data = (root / name).read_bytes()
        check_record(data, row, name)
        snapshot[name] = data
    require(set(snapshot) == FILES, 'Allowlist mismatch')
    for folder, frozen_pin in FROZEN.items():
        name = folder + '/MANIFEST.json'
        require(sha(snapshot[name]) == frozen_pin, 'Frozen manifest anchor mismatch: ' + folder)
        frozen = parse(snapshot[name])
        require(frozen['problem_id'] == 6000001 and isinstance(frozen['files'], dict), 'Frozen target mismatch')
        expected = {name}
        for relative, row in frozen['files'].items():
            require(valid_path(relative) and '/' not in relative, 'Unsafe frozen path')
            full = folder + '/' + relative
            expected.add(full)
            require(full in snapshot, 'Missing frozen payload')
            check_record(snapshot[full], row, full)
        actual = {name for name in snapshot if name.startswith(folder + '/')}
        require(actual == expected, 'Frozen closed inventory mismatch: ' + folder)
    check_record(snapshot['public/PROOF.md'], PROOF, 'proof binding')
    check_record(snapshot['public/MANIFEST.json'], AUTHOR_MANIFEST, 'author manifest binding')
    a = parse(snapshot['independent_global_audit/public/ACCEPTANCE.json'])
    b = parse(snapshot['independent_audit_b/public/ACCEPTANCE.json'])
    require(a['verdict'] == b['verdict'] == 'PASS' and not a['blocking_defects']
            and not a['required_proof_changes'] and not b['required_mathematical_patches'], 'Acceptance is not unconditional PASS')
    require(a['frozen_author_proof'] == b['accepted_author_packet']['proof'] == PROOF
            and a['frozen_author_manifest'] == b['accepted_author_packet']['manifest'] == AUTHOR_MANIFEST,
            'Acceptance bindings differ')
    check_record(snapshot['independent_global_audit/public/GLOBAL_AUDIT.md'], a['full_audit'], 'audit A report')
    check_record(snapshot['independent_audit_b/public/FULL_REPORT.md'], b['report'], 'audit B report')
    return snapshot

BOOTSTRAP = '''import sys, json
print(json.dumps({'optimize': sys.flags.optimize, 'debug': __debug__, 'isolated': sys.flags.isolated, 'bytecode_disabled': sys.dont_write_bytecode}), file=sys.stderr)
if sys.flags.optimize != 0 or not __debug__:
    raise SystemExit('REJECTED: optimized child would remove frozen assertions')
import runpy
script = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(script, run_name='__main__')
'''

def clean_versions(value, path):
    value = dict(value)
    if path == 'public/VERIFICATION.json':
        for key in ('python', 'sympy', 'numpy'):
            value.pop(key, None)
    elif path.endswith('INDEPENDENT_CONTROLS.json'):
        value.pop('sympy_version', None)
    else:
        value.pop('versions', None)
    return value

def replay(snapshot, child_optimize):
    results = []
    with tempfile.TemporaryDirectory(prefix='statistical-embedding-replay-') as td:
        root = Path(td) / 'packet'
        for name, data in snapshot.items():
            p = root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        checks = [
            ('public/verify_packet.py', ['--expected-manifest', FROZEN['public']], None),
            ('independent_global_audit/public/verify_audit_packet.py', ['--author-public', str(root/'public')], None),
            ('independent_audit_b/public/verify_audit.py', ['--expected-manifest', FROZEN['independent_audit_b/public'], '--author-dir', str(root/'public')], None),
            ('public/verify_math.py', [], 'public/VERIFICATION.json'),
            ('independent_global_audit/public/independent_controls.py', [], 'independent_global_audit/public/INDEPENDENT_CONTROLS.json'),
            ('independent_audit_b/public/independent_checks.py', [], 'independent_audit_b/public/INDEPENDENT_CHECKS.json'),
        ]
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith('PYTHON')}
        for name, extra, recorded in checks:
            command = [sys.executable, '-I', '-B'] + (['-' + 'O'*child_optimize] if child_optimize else [])
            command += ['-c', BOOTSTRAP, str(root/name)] + extra
            run = subprocess.run(command, cwd=td, env=env, capture_output=True, text=True, timeout=300)
            lines = run.stderr.splitlines()
            require(bool(lines), 'Missing actual child mode record')
            flags = parse(lines[0])
            require(run.returncode == 0, 'Child failed: ' + name + '\n' + run.stderr + '\n' + run.stdout)
            require(flags == {'optimize': 0, 'debug': True, 'isolated': 1, 'bytecode_disabled': True}, 'Unsafe actual child flags')
            output = parse(run.stdout)
            require(output.get('status', output.get('verdict')) == 'PASS', 'Child did not report PASS: ' + name)
            if recorded:
                require(clean_versions(output, recorded) == clean_versions(parse(snapshot[recorded]), recorded),
                        'Fresh replay differs from frozen result: ' + name)
            results.append({'script': name, 'status': 'PASS', 'child_flags': flags,
                            'recorded_results_match': bool(recorded), 'stdout_sha256': sha(run.stdout.encode())})
        # Audit A rewrites its recorded output. Require that every frozen byte survives.
        for name, raw in snapshot.items():
            require((root/name).read_bytes() == raw, 'Replay changed frozen bytes: ' + name)
        actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
        require(actual == set(snapshot), 'Replay added a file')
    return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('expected_manifest')
    parser.add_argument('packet', type=Path)
    parser.add_argument('--integrity-only', action='store_true')
    parser.add_argument('--child-optimize', type=int, choices=(0, 1, 2), default=0)
    args = parser.parse_args()
    root = args.packet.absolute()
    before = integrity(root, args.expected_manifest)
    require(Path(__file__).read_bytes() == before['verify_publication.py'], 'Executing wrapper differs from authenticated packet')
    results = [] if args.integrity_only else replay(before, args.child_optimize)
    require(before == integrity(root, args.expected_manifest), 'Packet changed during validation')
    print(json.dumps({'status': 'PASS', 'problem_id': 6000001, 'manifest_sha256': args.expected_manifest,
                      'files': len(before) + 1, 'outer_optimize': sys.flags.optimize,
                      'integrity_only': args.integrity_only, 'replays': results,
                      'limitation': 'Byte integrity and finite consistency checks, not formal proof or journal acceptance.'}, indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        raise SystemExit('REJECTED: ' + str(exc))
