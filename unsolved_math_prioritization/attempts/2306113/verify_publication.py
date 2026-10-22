#!/usr/bin/env python3
"""Externally pinned, source-free replay. Verify this script before executing it.

This is a computer-assisted certificate replay, not a formal proof kernel.
"""
import argparse
import difflib
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile

SHA = re.compile(r'[0-9a-f]{64}')
CANDIDATE = {
    'ALTERNATIVE_REPAIR.md', 'ALTERNATIVE_RESULT.json', 'APPROACHES.md',
    'CERTIFICATE_RESULT.json', 'COUNTEREXAMPLE.json', 'PROOF.md', 'README.md',
    'SOURCE_METADATA.json', 'replay_controls.py', 'search_loewner.py',
    'verify_alternative.py', 'verify_counterexample.py', 'MANIFEST.json',
}
SCOPE = {'SCOPE_AUDIT.md', 'verify_independent_algebra.py',
         'INDEPENDENT_ALGEBRA_RESULT.json', 'AUDIT_MANIFEST.json'}
AUDIT = {
    'AUDIT.md', 'independent_exact_audit.py', 'INDEPENDENT_RESULT.json',
    'INDEPENDENT_DISK_LEAVES.json', 'verify_independent_partition.py',
    'INDEPENDENT_PARTITION_CONTROLS.json', 'expanded_controls.py',
    'EXPANDED_CONTROLS.json', 'ORIGINAL_READONLY_REPLAY.json',
    'PATCHED_READONLY_REPLAY.json', 'REJECT_LARGE_INTEGER.patch',
    'PATCHED_PINS.json', 'SOURCE_FREE_ALLOWLIST.json',
}
FILES = {'README.md', 'ACCEPTANCE.md', 'RESEARCH_LOG.md',
         'verify_publication.py', 'wrapper_controls.py'}
FILES |= {'candidate/' + n for n in CANDIDATE}
FILES |= {'scope_audit/' + n for n in SCOPE}
FILES |= {'exact_audit/' + n for n in AUDIT}
FILES |= {'original_v2/MANIFEST.json', 'original_v2/verify_counterexample.py'}
PINS = {
    'candidate/MANIFEST.json': 'd889cab7f0337d983b9bd352f61b6bdd5e330cd6d011927cb97949dd716471fb',
    'candidate/verify_counterexample.py': '1e76693b2c5b1181b55fcd28e3e894e4828600e1471091ace06fbb6bbba09b25',
    'original_v2/MANIFEST.json': '2f315877db00b3776fe55ab0e576012874078fd8e2df0fc61fec94ff7ac98c28',
    'original_v2/verify_counterexample.py': 'aff03b041039d7cbcddab95d2af02d64df361d4d7911e2f87aa0986b682fa675',
    'scope_audit/AUDIT_MANIFEST.json': '53c6b14481b5b337f592e027c10df8de23ef2dc625953835fe1249aa773785fe',
    'scope_audit/SCOPE_AUDIT.md': '69344269085aff84ab97a777d915936ac6da0e856718d12e65a79552b287fce6',
    'exact_audit/AUDIT.md': '142de082f851dba9c993fd84c42c538a064cd17cdf2da09c85233615ced5dbac',
    'exact_audit/SOURCE_FREE_ALLOWLIST.json': '011bb4af35965b0746609e13282377ff22ea19e836aff91a437df1372f5fbb03',
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def finite_float(value):
    value = float(value)
    need(math.isfinite(value), 'nonfinite JSON float')
    return value


def nonfinite(value):
    raise ValueError('nonfinite JSON constant')


def load(raw):
    return json.loads(raw, object_pairs_hook=unique, parse_float=finite_float,
                      parse_constant=nonfinite)


def nonsymlink(path):
    for entry in [path, *path.parents]:
        need(not entry.is_symlink(), 'symlink path component')


def file_bytes(path):
    nonsymlink(path)
    st = path.stat()
    need(stat.S_ISREG(st.st_mode), 'nonregular file')
    need(st.st_size <= 2000000, 'file size bound')
    return path.read_bytes()


def safe_path(name):
    need(type(name) is str and name and '\\' not in name, 'path type')
    p = PurePosixPath(name)
    need(not p.is_absolute() and p.as_posix() == name and
         all(q not in {'', '.', '..'} for q in p.parts), 'unsafe path')
    return name


def check_entries(entries, expected, reader, key='name'):
    need(type(entries) is list and len(entries) == len(expected), 'entry count')
    seen = set()
    for entry in entries:
        need(type(entry) is dict and set(entry) == {key, 'bytes', 'sha256'}, 'entry schema')
        name = safe_path(entry[key])
        need(name in expected and name not in seen, 'unexpected or duplicate path')
        seen.add(name)
        need(type(entry['bytes']) is int and 0 <= entry['bytes'] <= 2000000,
             'exact bounded integer bytes')
        need(type(entry['sha256']) is str and SHA.fullmatch(entry['sha256']), 'digest schema')
        raw = reader(name)
        need(len(raw) == entry['bytes'] and sha(raw) == entry['sha256'], 'entry identity: ' + name)
    need(seen == expected, 'entry coverage')


def validate(root, pin):
    need(type(pin) is str and SHA.fullmatch(pin), 'external digest schema')
    nonsymlink(root)
    need(root.is_dir(), 'packet root must be directory')
    raw = file_bytes(root / 'PUBLIC_MANIFEST.json')
    need(sha(raw) == pin, 'external manifest pin mismatch')
    mf = load(raw)
    need(type(mf) is dict and set(mf) == {'schema', 'file_count', 'files'}, 'manifest schema')
    need(mf['schema'] == 'sigma-conditional-publication-v1', 'manifest version')
    need(type(mf['file_count']) is int and mf['file_count'] == len(FILES), 'exact integer file count')
    files, dirs = set(), set()
    need(stat.S_IMODE(root.stat().st_mode) & 0o222 == 0, 'root is not read-only')
    for parent, ds, fs in os.walk(root, followlinks=False):
        for name in ds + fs:
            path = Path(parent) / name
            nonsymlink(path)
            st = path.stat()
            need(stat.S_IMODE(st.st_mode) & 0o222 == 0, 'entry is not read-only')
            rel = path.relative_to(root).as_posix()
            if name in ds:
                need(stat.S_ISDIR(st.st_mode), 'non-directory entry')
                dirs.add(rel)
            else:
                file_bytes(path)
                files.add(rel)
    expected_dirs = {p.as_posix() for n in FILES for p in PurePosixPath(n).parents if str(p) != '.'}
    need(files == FILES | {'PUBLIC_MANIFEST.json'}, 'exact file inventory')
    need(dirs == expected_dirs, 'exact directory inventory')
    check_entries(mf['files'], FILES, lambda n: file_bytes(root / n), key='path')
    for name in files:
        if name.endswith('.json'):
            load(file_bytes(root / name))
    for name, expected in PINS.items():
        need(sha(file_bytes(root / name)) == expected, 'fixed accepted pin: ' + name)
    candidate = root / 'candidate'
    for original in [False, True]:
        source = root / 'original_v2' if original else candidate
        manifest = load(file_bytes(source / 'MANIFEST.json'))
        need(type(manifest) is dict and set(manifest) == {'schema', 'files'}, 'slice manifest schema')
        need(type(manifest['schema']) is int and manifest['schema'] == 1, 'slice version')
        # Original v2 is represented losslessly: eleven shared immutable files,
        # plus its own preserved verifier and manifest. Never rewrite originals.
        def read_slice(name):
            origin = source if name == 'verify_counterexample.py' else candidate
            return file_bytes(origin / name)
        check_entries(manifest['files'], CANDIDATE - {'MANIFEST.json'}, read_slice)
    scope = root / 'scope_audit'
    sm = load(file_bytes(scope / 'AUDIT_MANIFEST.json'))
    need(type(sm) is dict and set(sm) == {'date', 'files', 'verdict'}, 'scope manifest schema')
    check_entries(sm['files'], SCOPE - {'AUDIT_MANIFEST.json'}, lambda n: file_bytes(scope / n))
    audit = root / 'exact_audit'
    am = load(file_bytes(audit / 'SOURCE_FREE_ALLOWLIST.json'))
    need(type(am) is dict and set(am) == {'schema', 'scope', 'files'}, 'audit allowlist schema')
    need(type(am['schema']) is int and am['schema'] == 1, 'audit allowlist version')
    check_entries(am['files'], AUDIT - {'SOURCE_FREE_ALLOWLIST.json'}, lambda n: file_bytes(audit / n))
    pins = load(file_bytes(audit / 'PATCHED_PINS.json'))
    need(type(pins) is dict and set(pins) == CANDIDATE, 'corrected pins inventory')
    for name, expected in pins.items():
        need(type(expected) is str and SHA.fullmatch(expected), 'corrected digest schema')
        need(sha(file_bytes(candidate / name)) == expected, 'corrected file pin')
    old = file_bytes(root / 'original_v2/verify_counterexample.py').decode()
    new = file_bytes(candidate / 'verify_counterexample.py').decode()
    patch = ''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                    fromfile='a/verify_counterexample.py', tofile='b/verify_counterexample.py'))
    need(patch.encode() == file_bytes(audit / 'REJECT_LARGE_INTEGER.patch'), 'actual one-line correction')
    return mf


def run(script, args, cwd, env, json_output=True):
    flags = ['-' + 'O' * sys.flags.optimize] if sys.flags.optimize else []
    proc = subprocess.run([sys.executable, '-I', '-B', *flags, str(script), *map(str, args)],
                          cwd=cwd, env=env, capture_output=True, timeout=600)
    need(proc.returncode == 0 and not proc.stderr, 'child failed: ' + script.name)
    return load(proc.stdout) if json_output else proc.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    try:
        need(sys.flags.isolated == 1 and sys.dont_write_bytecode, 'invoke with -I -B')
        need(os.getuid() == os.geteuid() == 1000, 'genuine UID/EUID 1000 required')
        nonsymlink(args.root.absolute())
        root = args.root.resolve()
        validate(root, args.manifest_sha256)
        probes = [root / 'candidate/COUNTEREXAMPLE.json', root / 'unauthorized_probe']
        for target in probes:
            try:
                with target.open('ab') as stream:
                    stream.write(b'forbidden')
            except PermissionError:
                pass
            else:
                raise ValueError('actual read-only write probe succeeded')
        if args.integrity_only:
            print(json.dumps({'status': 'PASS', 'stage': 'integrity-only', 'write_probes_rejected': 2}))
            return 0
        candidate, audit, scope = root / 'candidate', root / 'exact_audit', root / 'scope_audit'
        with tempfile.TemporaryDirectory(prefix='sigma-publication-') as td:
            temp = Path(td)
            (temp / 'fractions.py').write_text('raise RuntimeError("HOSTILE fractions")\n')
            (temp / 'sitecustomize.py').write_text('raise RuntimeError("HOSTILE sitecustomize")\n')
            env = dict(os.environ, PYTHONPATH=td, PYTHONHOME='/nonexistent/hostile-home',
                       PYTHONOPTIMIZE='99', PYTHONDONTWRITEBYTECODE='0')
            baseline = run(candidate / 'replay_controls.py',
                           [candidate, '--manifest-sha256', PINS['candidate/MANIFEST.json']], temp, env)
            need(baseline == load(file_bytes(audit / 'PATCHED_READONLY_REPLAY.json')), 'baseline replay receipt mismatch')
            expanded_path = temp / 'EXPANDED_CONTROLS.json'
            expanded = run(audit / 'expanded_controls.py',
                           [candidate, expanded_path, audit / 'PATCHED_PINS.json'], temp, env)
            fresh_expanded = load(file_bytes(expanded_path))
            historical_expanded = load(file_bytes(audit / 'EXPANDED_CONTROLS.json'))
            need(fresh_expanded == historical_expanded, 'expanded rejection receipt mismatch')
            need(expanded == {k: v for k, v in fresh_expanded.items() if k != 'results'}, 'expanded stdout mismatch')
            algebra = run(scope / 'verify_independent_algebra.py',
                          [candidate / 'COUNTEREXAMPLE.json'], temp, env)
            need(algebra == load(file_bytes(scope / 'INDEPENDENT_ALGEBRA_RESULT.json')), 'independent algebra mismatch')
            result_path = temp / 'INDEPENDENT_RESULT.json'
            run(audit / 'independent_exact_audit.py', [candidate, result_path], temp, env, json_output=False)
            need(load(file_bytes(result_path)) == load(file_bytes(audit / 'INDEPENDENT_RESULT.json')), 'fresh complete arithmetic mismatch')
            leaves = temp / 'INDEPENDENT_DISK_LEAVES.json'
            need(file_bytes(leaves) == file_bytes(audit / leaves.name), 'fresh exact disk leaves mismatch')
            partition = run(audit / 'verify_independent_partition.py', [leaves], temp, env)
            need(partition == load(file_bytes(audit / 'INDEPENDENT_PARTITION_CONTROLS.json')), 'fresh partition controls mismatch')
        validate(root, args.manifest_sha256)
        print(json.dumps({
            'status': 'PASS', 'schema': 'sigma-conditional-replay-v1',
            'packet_files': len(FILES) + 1, 'manifest_sha256': args.manifest_sha256,
            'uid': os.getuid(), 'euid': os.geteuid(), 'optimization': sys.flags.optimize,
            'write_probes_rejected': 2, 'baseline_write_probes_rejected': 2,
            'fresh_baseline_positive_executions': 6, 'fresh_baseline_rejections': 168,
            'fresh_expanded_rejections': 228, 'fresh_trust_boundary_rejections': 7,
            'fresh_partition_rejections': 4, 'independent_circle_points': 32770,
            'independent_disk_nodes': 4050, 'independent_disk_leaves': 2026,
            'independent_disk_depth': 21, 'post_run_hashes_unchanged': True,
            'status_of_historical_problem': 'UNRESOLVED_SOURCE_IDENTITY',
            'queue_status': 'unsolved', 'turns': '5/5',
            'original_v2_reconstruction': 'ALL_THIRTEEN_FILE_IDENTITIES_VERIFIED',
            'original_v2_execution': 'NOT_RUN_HISTORICAL_RECEIPT_ONLY',
            'source_retrieval': 'NOT_RUN', 'floating_point_discovery': 'NOT_RUN',
            'proof_assistant': 'NOT_RUN', 'ci': 'NOT_RUN',
        }, sort_keys=True))
        return 0
    except (ValueError, KeyError, TypeError, OSError, RecursionError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'REJECT', 'reason': str(exc)}, sort_keys=True))
        return 2


if __name__ == '__main__':
    sys.exit(main())
