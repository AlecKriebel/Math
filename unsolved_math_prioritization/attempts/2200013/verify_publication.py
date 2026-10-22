#!/usr/bin/env python3
"""Read-only, externally pinned, source-free publication replay.

Independently verify this script's SHA-256 before executing it. Obtain the
manifest digest independently too. Hashes establish byte identity, not a proof
kernel, and assume a trusted interpreter/stdlib and stable filesystem.
"""
import argparse
import difflib
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile

SHA = re.compile(r'[0-9a-f]{64}')
PUBLIC = {'PROOF.md', 'README.md', 'RESULT.json', 'certificate.json',
          'replay.py', 'sources.json', 'verify_math.py'}
AUDIT = {'ACCEPTANCE.json', 'AUDIT.md', 'AUDIT_MANIFEST.json',
         'CONTROL_REPORT.json', 'EXTERNAL_PINS.json', 'INDEPENDENT_MATH.json',
         'PARSER_HARDENING.patch', 'RELEASE_ALLOWLIST.json', 'SOURCE_METADATA.json',
         'independent_math.py', 'run_audit.py', 'seal_audit.py'}
AUDIT |= {'corrected/public/' + name for name in PUBLIC}
AUDIT |= {'corrected/verification/MANIFEST.json', 'corrected/verification/bootstrap.py'}
FILES = {'README.md', 'ACCEPTANCE.md', 'RESEARCH_LOG.md', 'verify_publication.py',
         'historical/ORIGINAL_CONTROL_REPORT.json',
         'audit_scope/AUDIT.md', 'audit_scope/MANIFEST.json'}
FILES |= {'original/public/' + name for name in PUBLIC}
FILES |= {'original/verification/MANIFEST.json', 'original/verification/bootstrap.py'}
FILES |= {'audit_reproducibility/' + name for name in AUDIT}
PINS = {
 'audit_scope/AUDIT.md': 'd8fe55d6605aeeb03ea4dce05123e81888d038be1a140654706ad2f2c643ffc5',
 'audit_scope/MANIFEST.json': '85eaf029db7e3c9d59cee7e5ddc2bc72fc7f3e09492de5724507d50f42b69a18',
 'audit_reproducibility/AUDIT_MANIFEST.json': 'd2d1af43345732393f56c7911fa56ab0d2d4d7d58b2fb9f3e993f380f1bb3f80',
 'audit_reproducibility/corrected/verification/MANIFEST.json': 'cf8ddfc1ea755b8a9c136d6bdf420ea274b6add35be7fba66a02090efe087ed0',
 'audit_reproducibility/corrected/verification/bootstrap.py': 'f6e973e17500ae4c690cf4d9be4ba03f1b3ff29d1a0e54c8e7ada20a86391521',
 'audit_reproducibility/corrected/public/verify_math.py': '58f8eec4d54eb1de9855f880623fe1ad2380f0e4e1005a148f681b019dfc97c6',
 'audit_reproducibility/CONTROL_REPORT.json': '21747d6dd4ca8d1e1f4cfe2ad97feff6760bb80cf292d87c5c027ecde3f75cf9',
}


def need(value, reason):
    if not value:
        raise ValueError(reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def no_constant(value):
    raise ValueError('nonfinite JSON constant')


def finite_float(value):
    result = float(value)
    need(math.isfinite(result), 'nonfinite or overflow JSON float')
    return result


def read_json(raw):
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=no_constant, parse_float=finite_float)


def safe_path(value):
    need(type(value) is str and value != '' and '\\' not in value,
         'invalid relative path type')
    p = PurePosixPath(value)
    need(not p.is_absolute() and p.as_posix() == value and
         all(part not in {'', '.', '..'} for part in p.parts), 'unsafe relative path')
    return value


def nonsymlink(path):
    for p in [path, *path.parents]:
        need(not p.is_symlink(), 'symlink path component')


def file_bytes(path):
    nonsymlink(path)
    need(stat.S_ISREG(path.stat().st_mode), 'nonregular file')
    need(path.stat().st_size < 2000000, 'file size bound')
    return path.read_bytes()


def inventory(root):
    nonsymlink(root)
    need(root.is_dir(), 'packet root must be a directory')
    files, dirs = set(), set()
    for parent, ds, fs in os.walk(root, followlinks=False):
        for name in ds:
            path = Path(parent) / name
            nonsymlink(path)
            need(stat.S_ISDIR(path.stat().st_mode), 'non-directory entry')
            dirs.add(path.relative_to(root).as_posix())
        for name in fs:
            path = Path(parent) / name
            file_bytes(path)
            files.add(path.relative_to(root).as_posix())
    return files, dirs


def check_entries(root, entries, expected):
    need(type(entries) is list and len(entries) == len(expected), 'manifest count')
    seen = set()
    for e in entries:
        need(type(e) is dict and set(e) == {'path', 'bytes', 'sha256'}, 'entry schema')
        name = safe_path(e['path'])
        need(name in expected and name not in seen, 'unexpected or duplicate path')
        seen.add(name)
        need(type(e['bytes']) is int and 0 <= e['bytes'] < 2000000, 'exact bounded integer byte count')
        need(type(e['sha256']) is str and SHA.fullmatch(e['sha256']), 'digest schema')
        raw = file_bytes(root / name)
        need(len(raw) == e['bytes'] and digest(raw) == e['sha256'], 'entry identity: ' + name)
    need(seen == expected, 'manifest coverage')


def exact_integer(obj, key, value):
    need(type(obj.get(key)) is int and obj[key] == value, 'integer field: ' + key)


def check_report(report):
    need(type(report) is dict and report.get('schema') == 'independent-tropical-reproducibility-audit-v1', 'control report schema')
    for key, value in [('control_count', 687), ('passed_count', 687), ('uid', 1000), ('euid', 1000)]:
        exact_integer(report, key, value)
    for key in ['all_passed', 'original_preserved', 'proof_bytes_unchanged']:
        need(report.get(key) is True, 'report truth field: ' + key)
    rows = report.get('controls')
    need(type(rows) is list and len(rows) == 687, 'control list')
    need(all(type(r) is dict and r.get('passed') is True for r in rows), 'failed control')
    for mode in ['normal', 'O', 'OO']:
        need(sum(r.get('mode') == mode for r in rows) == 229, 'per-mode count')
    need(sum('overflow literal' in r.get('name', '') for r in rows) == 78, 'overflow count')


def validate(root, pin):
    need(type(pin) is str and SHA.fullmatch(pin), 'external digest schema')
    raw = file_bytes(root / 'PUBLIC_MANIFEST.json')
    need(digest(raw) == pin, 'external manifest mismatch')
    manifest = read_json(raw)
    need(type(manifest) is dict and set(manifest) == {'schema', 'file_count', 'files'}, 'manifest schema')
    need(manifest['schema'] == 'tropical-publication-v1', 'manifest version')
    exact_integer(manifest, 'file_count', len(FILES))
    files, dirs = inventory(root)
    need(files == FILES | {'PUBLIC_MANIFEST.json'}, 'exact file inventory')
    expected_dirs = {p.as_posix() for name in FILES for p in PurePosixPath(name).parents if str(p) != '.'}
    need(dirs == expected_dirs, 'exact directory inventory')
    check_entries(root, manifest['files'], FILES)
    for name in sorted(files):
        if name.endswith('.json'):
            read_json(file_bytes(root / name))
    for name, expected in PINS.items():
        need(digest(file_bytes(root / name)) == expected, 'independent audit pin: ' + name)
    scope = read_json(file_bytes(root / 'audit_scope/MANIFEST.json'))
    check_entries(root / 'audit_scope', scope['files'], {'AUDIT.md'})
    ar = root / 'audit_reproducibility'
    am = read_json(file_bytes(ar / 'AUDIT_MANIFEST.json'))
    need(type(am) is dict and set(am) == {'schema', 'self_excluded_for_external_pinning', 'file_count', 'files'}, 'audit manifest schema')
    need(am['schema'] == 'independent-source-free-audit-manifest-v1' and am['self_excluded_for_external_pinning'] is True, 'audit manifest version')
    exact_integer(am, 'file_count', 20)
    check_entries(ar, am['files'], AUDIT - {'AUDIT_MANIFEST.json'})
    allow = read_json(file_bytes(ar / 'RELEASE_ALLOWLIST.json'))
    need(type(allow) is dict and set(allow) == {'schema', 'paths'} and allow['schema'] == 'source-free-audit-allowlist-v1', 'audit allowlist schema')
    need(type(allow['paths']) is list and allow['paths'] == sorted(AUDIT), 'audit allowlist')
    check_report(read_json(file_bytes(ar / 'CONTROL_REPORT.json')))
    accept = read_json(file_bytes(ar / 'ACCEPTANCE.json'))
    for key, value in [('problem_id', 2200013), ('rank', 1031), ('control_count', 687), ('passed_count', 687), ('controls_per_mode', 229), ('overflow_literal_rejection_controls', 78)]:
        exact_integer(accept, key, value)
    need(accept.get('mathematical_verdict') == accept.get('corrected_verifier_verdict') == 'ACCEPTED', 'accepted release verdict')
    need(accept.get('classification') == 'LITERATURE_DERIVED_NEGATIVE_RESOLUTION_WITH_EXPLICIT_RECONSTRUCTION', 'classification')
    need(accept.get('actual_degree') == '200000000000000000100', 'degree')
    exact_integer(accept, 'distinct_binomial_weighted_corners', 3)
    exact_integer(accept, 'distinct_negative_roots_at_least', 4)
    for key in ['novelty_claim', 'minimal_degree_claim', 'exact_total_root_claim', 'conventional_slope_multiplicity_target']:
        need(accept.get(key) is False, 'scope bound: ' + key)
    pins = read_json(file_bytes(ar / 'EXTERNAL_PINS.json'))
    for label, sub in [('original', root / 'original'), ('corrected', ar / 'corrected')]:
        for name, e in pins[label].items():
            check_entries(sub, [dict(path=name, **e)], {name})
        m = read_json(file_bytes(sub / 'verification/MANIFEST.json'))
        need(type(m) is dict and set(m) == {'schema', 'files'} and m['schema'] == 'authored-slice-manifest-v1', 'slice manifest schema')
        check_entries(sub / 'public', m['files'], PUBLIC)
    for name in PUBLIC - {'verify_math.py'}:
        need(file_bytes(root / 'original/public' / name) == file_bytes(ar / 'corrected/public' / name), 'unchanged original bytes: ' + name)
    old = file_bytes(root / 'original/public/verify_math.py').decode()
    new = file_bytes(ar / 'corrected/public/verify_math.py').decode()
    patch = ''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile='a/verify_math.py', tofile='b/verify_math.py'))
    need(patch.encode() == file_bytes(ar / 'PARSER_HARDENING.patch'), 'actual parser code patch')
    return manifest


def command(script, *args):
    mode = ['-' + 'O' * sys.flags.optimize] if sys.flags.optimize else []
    return [sys.executable, '-I', '-B', *mode, str(script), *map(str, args)]


def run(script, *args, timeout=240):
    cp = subprocess.run(command(script, *args), capture_output=True, timeout=timeout)
    need(cp.returncode == 0 and not cp.stderr, 'subprocess failed: ' + script.name)
    return read_json(cp.stdout)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--manifest-sha256', required=True)
    a = p.parse_args()
    try:
        need(sys.flags.isolated == 1 and sys.dont_write_bytecode, 'invoke with -I -B')
        need(os.getuid() == os.geteuid() == 1000, 'genuine UID/EUID 1000 required')
        nonsymlink(a.root.absolute())
        root = a.root.resolve()
        validate(root, a.manifest_sha256)
        ar = root / 'audit_reproducibility'
        fresh = run(ar / 'independent_math.py')
        need(fresh == read_json(file_bytes(ar / 'INDEPENDENT_MATH.json')), 'independent integer reconstruction output')
        for sub in [root / 'original', ar / 'corrected']:
            result = run(sub / 'verification/bootstrap.py', '--root', sub / 'public', '--manifest', sub / 'verification/MANIFEST.json')
            need(result.get('status') == 'PASS', 'frozen slice replay')
        # Only disposable copies are writable. All original publication bytes stay frozen.
        with tempfile.TemporaryDirectory(prefix='tropical-publication-replay-') as td:
            temp = Path(td)
            shutil.copytree(root / 'original', temp / 'original', copy_function=shutil.copyfile)
            shutil.copytree(ar, temp / 'audit', copy_function=shutil.copyfile)
            # copytree preserves source directory modes. Make only disposable
            # copy directories writable for the auditor's deliberate mutations.
            for copied in [temp / 'original', temp / 'audit']:
                for directory in [copied, *(q for q in copied.rglob('*') if q.is_dir())]:
                    directory.chmod(0o755)
            result = run(temp / 'audit/run_audit.py', '--original', temp / 'original')
            need(result.get('all_passed') is True, 'fresh independent audit')
            report = read_json(file_bytes(temp / 'audit/CONTROL_REPORT.json'))
            check_report(report)
            sealed = run(temp / 'audit/seal_audit.py')
            need(sealed.get('status') == 'PASS', 'fresh audit seal')
            # Runtime receipts may differ with interpreter versions. Mathematical
            # and acceptance data must agree; frozen historical receipts stay intact.
            need(read_json(file_bytes(temp / 'audit/ACCEPTANCE.json')) == read_json(file_bytes(ar / 'ACCEPTANCE.json')), 'fresh acceptance mismatch')
            for name in ['corrected/verification/MANIFEST.json', 'corrected/verification/bootstrap.py', 'PARSER_HARDENING.patch']:
                need(file_bytes(temp / 'audit' / name) == file_bytes(ar / name), 'reproduction changed release bytes')
        validate(root, a.manifest_sha256)
        print(json.dumps({'status': 'PASS', 'packet_files': len(FILES) + 1,
            'manifest_sha256': a.manifest_sha256, 'optimization': sys.flags.optimize,
            'uid': os.getuid(), 'euid': os.geteuid(), 'fresh_audit_controls': 687,
            'controls_per_mode': 229, 'overflow_rejections': 78,
            'source_retrieval': 'NOT_RUN', 'corpus_retrieval': 'NOT_RUN',
            'proof_assistant': 'NOT_RUN', 'ci': 'NOT_RUN'}, sort_keys=True))
        return 0
    except (ValueError, KeyError, TypeError, OSError, RecursionError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'REJECT', 'reason': str(exc)}, sort_keys=True))
        return 2


if __name__ == '__main__':
    sys.exit(main())
