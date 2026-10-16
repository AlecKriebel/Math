#!/usr/bin/env python3
"""Trusted entry point; authenticate this script and the manifest externally first.

This is a finite replay/integrity tool, not a proof assistant or OS sandbox.
The outer process supports optimization, but every diagnostic child uses level 0.
"""
import sys
if not getattr(sys.flags, 'safe_path', False):
    raise SystemExit('REJECTED: safe-path startup required; use Python >=3.11 with -P or -I before any package imports')
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone

MANIFEST = 'PACKAGE_MANIFEST.json'
CAP = 64 * 1024 * 1024
ORIGINAL = 'original/unsolved_math_prioritization/attempts/6000001'
TOOLS = {
    'launch_portable_gate.py': '0199b8c7c481527121813c6d3c57a5acd2e598e8a5223acba69eb2161235d3b8',
    'portable_gate.py': '65f2d6b7f96f9994d073d7bf3741af5dcfc92ac6fe9f9aaadf224d25016e5b57',
    'portable_worker.py': 'fe5a88a4e5c5a8a6e95ad4b729a0427366f33eabbb512017a06ce362e2739fa2',
    'compare_results.py': '85c7a936c3333a6dc283bb46525589f21ab11584f0cde88c745286fb364bbd4b',
}
CHECKS = [
    'reviews/jet_calculus/independent_checks.py',
    'reviews/global_hessian/independent_controls.py',
    'reviews/global_adversary/global_controls.py',
    'reviews/reproducibility/independent_exact_controls.py',
]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def safe_name(name):
    require(type(name) is str and bool(name) and '\\' not in name and
            all(ord(c) >= 32 and ord(c) != 127 for c in name), 'Malformed path')
    path = PurePosixPath(name)
    require(not path.is_absolute() and str(path) == name and
            all(p not in ('', '.', '..') for p in path.parts), 'Noncanonical path')
    return name


def pin(value):
    require(type(value) is str and len(value) == 64 and
            all(c in '0123456789abcdef' for c in value), 'Malformed external pin')
    return value


def pairs(items):
    out = {}
    for key, value in items:
        require(key not in out, 'Duplicate JSON key')
        out[key] = value
    return out


def parse(raw):
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))


def directory(path):
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NONBLOCK)
    try:
        for part in Path(os.path.abspath(path)).parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY |
                            os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def read_fd(fd, limit, size=None):
    info = os.fstat(fd)
    require(stat.S_ISREG(info.st_mode), 'Special file rejected')
    require(stat.S_IMODE(info.st_mode) == 0o644, 'File mode must be 0644')
    require(0 <= info.st_size <= limit, 'Byte limit exceeded')
    require(size is None or info.st_size == size, 'Byte size differs')
    result = []
    remaining = limit + 1
    while remaining:
        chunk = os.read(fd, min(65536, remaining))
        if not chunk:
            break
        result.append(chunk)
        remaining -= len(chunk)
    raw = b''.join(result)
    require(len(raw) == info.st_size and len(raw) <= limit, 'File changed during bounded read')
    return raw


def read_path(path, limit):
    parent = directory(path.parent)
    try:
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    finally:
        os.close(parent)
    try:
        return read_fd(fd, limit)
    finally:
        os.close(fd)


def manifest(raw, anchor):
    require(digest(raw) == pin(anchor), 'External manifest pin differs')
    m = parse(raw)
    require(m['schema'] == 'pr946-closed-verification-package-v1', 'Manifest schema')
    rows = m['files']
    require(type(rows) is dict and bool(rows) and MANIFEST not in rows, 'Bad file map')
    for name, row in rows.items():
        safe_name(name)
        require(type(row) is dict and set(row) == {'bytes', 'sha256', 'mode'}, 'Bad file row')
        require(type(row['bytes']) is int and 0 <= row['bytes'] <= CAP and
                row['mode'] == '0644', 'Bad file size/mode')
        pin(row['sha256'])
    require(sum(row['bytes'] for row in rows.values()) <= CAP, 'Package exceeds cap')
    require(m['explicit_public_allowlist'] == sorted(rows), 'Allowlist differs')
    directories = {str(parent) for name in rows for parent in PurePosixPath(name).parents
                   if str(parent) != '.'}
    require(m['directories'] == sorted(directories), 'Directory allowlist differs')
    require(len(m['original_inventory']) == 33, 'Original inventory must have 33 files')
    for name, row in m['original_inventory'].items():
        require(rows[ORIGINAL + '/' + safe_name(name)] == row, 'Original pin differs')
    for name, anchor in TOOLS.items():
        require(rows['tools/' + name]['sha256'] == anchor, 'Current v2 tool differs')
    return m


def checked(raw, row, name):
    require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'Payload differs: ' + name)
    return raw


def from_directory(root, anchor):
    raw = read_path(root / MANIFEST, 8 * 1024 * 1024)
    m = manifest(raw, anchor)
    rows = dict(m['files'])
    rows[MANIFEST] = dict(bytes=len(raw), sha256=digest(raw), mode='0644')
    result, found_dirs = {}, set()
    def walk(fd, prefix=''):
        with os.scandir(fd) as entries:
            for entry in entries:
                name = safe_name(prefix + entry.name)
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    require(name in m['directories'], 'Unexpected directory: ' + name)
                    found_dirs.add(name)
                    child = os.open(entry.name, os.O_RDONLY | os.O_DIRECTORY |
                                    os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
                    try:
                        walk(child, name + '/')
                    finally:
                        os.close(child)
                else:
                    require(stat.S_ISREG(mode) and name in rows, 'Extra/special/linked file: ' + name)
                    child = os.open(entry.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
                    try:
                        data = read_fd(child, rows[name]['bytes'], rows[name]['bytes'])
                    finally:
                        os.close(child)
                    result[name] = checked(data, rows[name], name)
    fd = directory(root)
    try:
        walk(fd)
    finally:
        os.close(fd)
    require(set(result) == set(rows) and found_dirs == set(m['directories']), 'Closed inventory differs')
    return m, result


def from_archive(path, anchor, archive_anchor):
    archive = read_path(path, CAP)
    require(digest(archive) == pin(archive_anchor), 'External archive pin differs')
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        infos = z.infolist()
        names = [safe_name(i.filename) for i in infos]
        require(len(names) == len(set(names)), 'Duplicate archive member')
        require(MANIFEST in names, 'Missing archive manifest')
        require(all(i.create_system == 3 and (i.external_attr >> 16) == 0o100644 and
                    not i.is_dir() and not i.flag_bits & 1 and 0 <= i.file_size <= CAP
                    for i in infos), 'Archive nonregular/mode/encryption rejected')
        require(sum(i.file_size for i in infos) <= CAP, 'Expanded archive exceeds cap')
        raw = z.read(MANIFEST)
        require(len(raw) <= 8 * 1024 * 1024, 'Manifest cap exceeded')
        m = manifest(raw, anchor)
        require(set(names) == set(m['files']) | {MANIFEST}, 'Closed archive members differ')
        result = {MANIFEST: raw}
        for name, row in m['files'].items():
            require(z.getinfo(name).file_size == row['bytes'], 'Archive member size differs')
            result[name] = checked(z.read(name), row, name)
    return m, result


BOOT = '''import sys,base64,json
flags=dict(optimize=sys.flags.optimize,debug=__debug__,isolated=sys.flags.isolated,bytecode_disabled=sys.dont_write_bytecode)
print(json.dumps(flags),file=sys.stderr)
if sys.flags.optimize!=0 or not __debug__ or not sys.flags.isolated or not sys.dont_write_bytecode:
 raise SystemExit('REJECTED: diagnostic child is not isolated nonoptimized Python')
raw=base64.b64decode(sys.argv[1],validate=True);filename=sys.argv[2];sys.argv=sys.argv[2:]
exec(compile(raw,filename,'exec'),dict(__name__='__main__',__file__=filename))
'''


def child(raw, path, args, cwd, no_site=False):
    cmd = [sys.executable, '-I', '-B'] + (['-S'] if no_site else [])
    cmd += ['-c', BOOT, base64.b64encode(raw).decode(), str(path), *map(str, args)]
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith('PYTHON')}
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=1200)
    require(r.returncode == 0, 'Diagnostic failed: ' + str(path) + '\n' + r.stderr + '\n' + r.stdout)
    flags = parse(r.stderr.splitlines()[0])
    require(flags == dict(optimize=0, debug=True, isolated=1, bytecode_disabled=True), 'Child flags differ')
    result = parse(r.stdout)
    require(result.get('status') == 'PASS' or result.get('pass') is True or
            result.get('all_pass') is True, 'Diagnostic result did not PASS')
    return dict(actual_child_flags=flags, stdout_sha256=digest(r.stdout.encode()), result=result)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    source = p.add_mutually_exclusive_group()
    source.add_argument('--package', type=Path, default=Path(__file__).absolute().parent)
    source.add_argument('--archive', type=Path, help='Standalone package-only ZIP, with no prefix/directories')
    p.add_argument('--manifest-sha256', required=True)
    p.add_argument('--archive-sha256')
    p.add_argument('--integrity-only', action='store_true')
    p.add_argument('--runtime-receipt', type=Path,
                   help='Optional detailed receipt outside the package; stdout remains deterministic')
    a = p.parse_args()
    require(not a.archive or a.archive_sha256, 'Archive requires external archive pin')
    m, payload = (from_archive(a.archive, a.manifest_sha256, a.archive_sha256) if a.archive
                  else from_directory(a.package, a.manifest_sha256))
    result = dict(status='PASS', pr=946, problem_id='6000001',
                  package_manifest_sha256=a.manifest_sha256, original_files_unchanged=33,
                  observed_outer_optimization=sys.flags.optimize, worker_optimization=None,
                  entry_safe_path=True,
                  payload_files=len(m['files']),
                  inventory='closed; every payload captured and authenticated before diagnostic execution',
                  proof_search_turns_added=0)
    runtime = dict(utc=datetime.now(timezone.utc).isoformat(), python=sys.version,
                   actual_outer_flags=dict(optimize=sys.flags.optimize, debug=__debug__,
                   isolated=sys.flags.isolated, safe_path=sys.flags.safe_path,
                   bytecode_disabled=sys.dont_write_bytecode))
    if not a.integrity_only:
        # Resolve only the trusted OS temporary root; package/archive inputs never
        # use resolve(). macOS commonly exposes /var as a link to /private/var.
        scratch_root = Path(tempfile.gettempdir()).resolve(strict=True)
        fd = directory(scratch_root)
        os.close(fd)
        with tempfile.TemporaryDirectory(prefix='pr946-package-', dir=scratch_root) as td:
            top = Path(td)
            # Materialize captured authenticated bytes; no original dependency is reloaded.
            for name, raw in payload.items():
                q = top / name
                q.parent.mkdir(parents=True, exist_ok=True)
                q.write_bytes(raw)
                q.chmod(0o644)
            tool = top / 'tools'
            args = [top / ORIGINAL, '--gate', tool / 'portable_gate.py', '--gate-sha256', TOOLS['portable_gate.py'],
                    '--worker', tool / 'portable_worker.py', '--worker-sha256', TOOLS['portable_worker.py'],
                    '--comparator', tool / 'compare_results.py', '--comparator-sha256', TOOLS['compare_results.py'],
                    '--scratch', top]
            runtime['portable_replay'] = child(payload['tools/launch_portable_gate.py'],
                                               tool / 'launch_portable_gate.py', args, top, no_site=True)
            gate = runtime['portable_replay']['result']
            worker = gate['worker']
            result['worker_optimization'] = worker['actual_worker_flags']['optimize']
            require(result['worker_optimization'] == 0, 'Worker optimization differs')
            result['portable_replay'] = dict(status=gate['status'], original_files=gate['original_files'],
                 original_manifest_sha256=gate['original_manifest_sha256'], proof_sha256=gate['proof_sha256'],
                 actual_worker_flags=worker['actual_worker_flags'], replays=[
                 {k: row[k] for k in ('script', 'status', 'actual_child_flags', 'comparison')}
                 for row in worker['replays']])
            result['independent_finite_checks'] = {}
            runtime['independent_finite_checks'] = {}
            for name in CHECKS:
                # The global-adversary program writes an output beside its scratch copy only.
                record = child(payload[name], top / name, [], top)
                runtime['independent_finite_checks'][name] = record
                stable = dict(record['result'])
                # These precisely identified fields are provenance, never mathematics.
                ignored = {'reviews/jet_calculus/independent_checks.py': (),
                           'reviews/global_hessian/independent_controls.py': ('utc',),
                           'reviews/global_adversary/global_controls.py': ('utc', 'python'),
                           'reviews/reproducibility/independent_exact_controls.py': ('python', 'sympy')}[name]
                for key in ignored:
                    require(key in stable, 'Missing declared provenance field')
                    del stable[key]
                result['independent_finite_checks'][name] = dict(actual_child_flags=record['actual_child_flags'],
                                                               mathematical_result=stable)
            # Authenticate the caller's source tree again; scratch outputs never enter the release.
            if not a.archive:
                require(from_directory(a.package, a.manifest_sha256)[1] == payload, 'Source changed during replay')
    result['limitation'] = ('Finite exact identities and bounded numerical consistency supplement the written proof; '
                           'they establish neither arbitrary-manifold existence nor priority. Trusted entry script, '
                           'interpreter, startup environment, installed packages, process and filesystem are assumed; no OS sandbox. '
                           'Manifest and entry-script pins must come from a trusted separate record.')
    if a.runtime_receipt:
        require(a.runtime_receipt.is_absolute(), 'Runtime receipt path must be absolute')
        require(not a.runtime_receipt.is_relative_to(a.package.absolute()),
                'Runtime receipt must be outside the closed package')
        a.runtime_receipt.write_text(json.dumps(runtime, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        raise SystemExit('REJECTED: ' + str(exc))
