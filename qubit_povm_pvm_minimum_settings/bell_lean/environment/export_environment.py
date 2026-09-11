#!/usr/bin/env python3
"""Export the project's exact Linux Lean/Mathlib environment on an ONLINE host.

This script is not a proof of the paper. It validates toolchain smoke tests only.
The companion workflow runs this on GitHub Actions without repository writes.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tarfile
import time
import urllib.request

LEAN_HASH = '6caaee842e9495688c1567e78c0e68dbb96942aa'
TOOLCHAIN = 'leanprover/lean4:v4.19.0'
ASSET = 'https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst'
ASSET_BYTES = 343842845
PART_BYTES = 400 * 1024 * 1024
MAX_PARTS = 12
BUNDLE_NAME = 'bell-lean419-environment'
PART_PREFIX = 'bell-lean419-linux-x64.tar.gz.part-'
FONT_SUFFIXES = {'.ttf', '.otf', '.woff', '.woff2', '.eot'}

POSITIVE = '''import Mathlib\nnamespace EnvironmentSmoke\ntheorem square_identity (a b : ℝ) : (a+b)^2 = a^2 + 2*a*b + b^2 := by\n  ring\n#print axioms square_identity\nend EnvironmentSmoke\n'''
NEGATIVE = '''import Mathlib\nexample : (1 : ℝ) = 0 := by\n  norm_num\n'''


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def run(command: list[str], cwd: Path, log: Path, env: dict[str, str] | None = None,
        allow_failure: bool = False) -> tuple[int, str]:
    print('+', ' '.join(command), flush=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open('w') as stream:
        result = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                                stderr=subprocess.STDOUT, check=False)
    text = log.read_text(errors='replace')
    if result.returncode and not allow_failure:
        print(text[-12000:], flush=True)
        raise RuntimeError(f'Command failed ({result.returncode}); see {log}')
    return result.returncode, text


def fetch_dependency(package: dict, directory: Path, logs: Path) -> None:
    name, rev = package['name'], package['rev']
    target = directory / name
    target.mkdir()
    run(['git', 'init', '-q'], target, logs/f'{name}-init.log')
    run(['git', 'remote', 'add', 'origin', package['url']], target, logs/f'{name}-remote.log')
    for attempt in range(3):
        status, text = run(['git', '-c', 'core.autocrlf=false', 'fetch', '--depth=1',
                            'origin', rev], target, logs/f'{name}-fetch.log', allow_failure=True)
        if status == 0:
            break
        if attempt == 2:
            raise RuntimeError(f'Cannot fetch exact dependency {name}@{rev}: {text[-3000:]}')
        time.sleep(5 * (attempt+1))
    run(['git', '-c', 'core.autocrlf=false', 'checkout', '--detach', 'FETCH_HEAD'],
        target, logs/f'{name}-checkout.log')
    actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=target, text=True).strip()
    if actual != rev:
        raise RuntimeError(f'Dependency pin mismatch: {name}: {actual} != {rev}')


def smoke(root: Path, relative_paths: list[str], phase: str) -> dict:
    workspace = root/'workspace'
    receipts = root/'receipts'
    env = os.environ.copy()
    env['PATH'] = str(root/'runtime/bin') + os.pathsep + env.get('PATH', '')
    env['LEAN_PATH'] = os.pathsep.join(str(root/p) for p in relative_paths)
    env.pop('LEAN_SYSROOT', None)
    lean = str(root/'runtime/bin/lean')
    _, version = run([lean, '--version'], workspace, receipts/f'{phase}-version.log', env)
    _, git_hash = run([lean, '--githash'], workspace, receipts/f'{phase}-githash.log', env)
    if git_hash.strip() != LEAN_HASH:
        raise RuntimeError('Unexpected Lean executable revision')
    (workspace/'EnvironmentSmoke.lean').write_text(POSITIVE)
    (workspace/'EnvironmentNegative.lean').write_text(NEGATIVE)
    positive_status, positive_text = run(
        [lean, '-o', 'EnvironmentSmoke.olean', 'EnvironmentSmoke.lean'],
        workspace, receipts/f'{phase}-positive.log', env)
    negative_status, negative_text = run([lean, 'EnvironmentNegative.lean'],
        workspace, receipts/f'{phase}-negative.log', env, allow_failure=True)
    if positive_status != 0 or 'sorryAx' in positive_text:
        raise RuntimeError('The positive smoke theorem did not pass cleanly')
    if negative_status == 0 or 'unsolved goals' not in negative_text:
        raise RuntimeError('The negative smoke test was not rejected as expected')
    return {'phase': phase, 'version': version.strip(), 'lean_git_hash': git_hash.strip(),
            'positive_exit': positive_status, 'negative_exit': negative_status,
            'smoke_only': True, 'paper_kernel_checked': False}


def export(work: Path, output: Path, pins_path: Path, restore_path: Path) -> None:
    if platform.system() != 'Linux' or platform.machine() not in ('x86_64', 'AMD64'):
        raise RuntimeError('This exporter targets Linux x86_64, not the host Mac toolchain')
    for cmd in ('git', 'tar', 'unzstd'):
        if not shutil.which(cmd):
            raise RuntimeError(f'Missing command: {cmd}')
    if work.exists():
        raise RuntimeError(f'Refusing to reuse a preexisting build directory: {work}')
    work.mkdir(parents=True)
    output.mkdir(parents=True, exist_ok=True)
    logs = output/'logs'
    logs.mkdir(exist_ok=True)
    pins = json.loads(pins_path.read_text())
    if pins['toolchain'] != TOOLCHAIN or pins['lean_git_hash'] != LEAN_HASH:
        raise RuntimeError('Pin file does not match this exporter')
    original = work/'before-relocation'/BUNDLE_NAME
    workspace, runtime = original/'workspace', original/'runtime'
    workspace.mkdir(parents=True)
    runtime.mkdir()
    (original/'receipts').mkdir()
    for name in ('lakefile.toml', 'lake-manifest.json', 'lean-toolchain'):
        (workspace/name).write_text(pins['files'][name])
    (workspace/'Bell.lean').write_text('import Mathlib\n')
    archive = work/'lean-4.19.0-linux.tar.zst'
    print('Downloading the official pinned Lean release asset', flush=True)
    request = urllib.request.Request(ASSET, headers={'User-Agent': 'Bell-Lean-Offline-Exporter'})
    with urllib.request.urlopen(request, timeout=120) as response, archive.open('wb') as target:
        shutil.copyfileobj(response, target, 1024*1024)
    if archive.stat().st_size != ASSET_BYTES:
        raise RuntimeError('Official release asset size differs from the inspected metadata')
    release_sha = sha(archive)
    run(['tar', '--use-compress-program=unzstd', '-xf', str(archive),
         '--strip-components=1', '-C', str(runtime)], work, logs/'release-extract.log')
    env = os.environ.copy()
    env['PATH'] = str(runtime/'bin') + os.pathsep + env.get('PATH', '')
    env.pop('LEAN_SYSROOT', None)
    env.pop('LEAN_PATH', None)
    _, git_hash = run([str(runtime/'bin/lean'), '--githash'], workspace,
                       logs/'official-lean-githash.log', env)
    if git_hash.strip() != LEAN_HASH:
        raise RuntimeError('Release binary revision does not match the official v4.19.0 tag')
    packages = workspace/'.lake/packages'
    packages.mkdir(parents=True)
    manifest = json.loads(pins['files']['lake-manifest.json'])
    print('Cloning all nine dependencies at their exact recorded commits', flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(lambda p: fetch_dependency(p, packages, logs), manifest['packages']))
    run([str(runtime/'bin/lake'), 'exe', 'cache', 'get'], workspace, logs/'mathlib-cache.log', env)
    if json.loads((workspace/'lake-manifest.json').read_text()) != manifest:
        raise RuntimeError('Lake altered the pinned manifest; refusing to export a different environment')
    # Retain exact original formatting after verifying semantic identity.
    (workspace/'lake-manifest.json').write_text(pins['files']['lake-manifest.json'])
    revisions = {}
    for pkg in manifest['packages']:
        actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'],
                    cwd=packages/pkg['name'], text=True).strip()
        if actual != pkg['rev']:
            raise RuntimeError('A dependency revision changed during cache acquisition')
        revisions[pkg['name']] = actual
    _, lean_path_text = run([str(runtime/'bin/lake'), 'env', 'printenv', 'LEAN_PATH'],
                            workspace, logs/'lean-path.log', env)
    relative_paths = []
    for item in lean_path_text.strip().split(os.pathsep):
        if not item:
            continue
        absolute = Path(item)
        if not absolute.is_absolute():
            absolute = workspace/absolute
        relative_paths.append(absolute.resolve().relative_to(original.resolve()).as_posix())
    core = 'runtime/lib/lean'
    if core not in relative_paths:
        relative_paths.append(core)
    write_json(original/'lean-paths.json', relative_paths)
    write_json(original/'pins.json', pins)
    first = smoke(original, relative_paths, 'before-relocation')
    relocated_parent = work/'after-relocation'
    relocated_parent.mkdir()
    root = relocated_parent/BUNDLE_NAME
    original.rename(root)
    if original.exists():
        raise RuntimeError('Relocation did not remove the original path')
    second = smoke(root, relative_paths, 'after-relocation')
    moved_env = os.environ.copy()
    moved_env['PATH'] = str(root/'runtime/bin') + os.pathsep + moved_env.get('PATH', '')
    moved_env.pop('LEAN_PATH', None)
    moved_env.pop('LEAN_SYSROOT', None)
    run([str(root/'runtime/bin/lake'), 'env', 'lean', 'EnvironmentSmoke.lean'],
        root/'workspace', root/'receipts/relocated-lake-positive.log', moved_env)
    shutil.copy2(restore_path, root/'restore_environment.py')
    receipt = {'status': 'smoke_tests_passed', 'toolchain': TOOLCHAIN,
        'lean_git_hash': LEAN_HASH, 'dependency_revisions': revisions,
        'positive_and_negative_tests': [first, second], 'paper_kernel_checked': False,
        'scope': 'Toolchain and Mathlib smoke tests, NOT the Bell project or the paper.',
        'workflow_provenance': {k: os.environ.get(k) for k in
             ('BELL_EXPORT_REPOSITORY', 'BELL_EXPORT_COMMIT', 'BELL_EXPORT_RUN_ID')},
        'release_asset': {'url': ASSET, 'bytes': ASSET_BYTES, 'sha256': release_sha,
            'upstream_digest_available': False,
            'note': 'SHA-256 is computed here; upstream metadata supplied no digest.'}}
    write_json(root/'receipts/environment.json', receipt)
    excluded = []
    raw_bytes = 0
    def filter_member(member: tarfile.TarInfo) -> tarfile.TarInfo | None:
        nonlocal raw_bytes
        path = Path(member.name)
        if path.suffix.lower() in FONT_SUFFIXES or '__pycache__' in path.parts:
            excluded.append(member.name)
            return None
        if member.isfile():
            raw_bytes += member.size
        return member
    bundled = output/'bell-lean419-linux-x64.tar.gz'
    print('Packaging the relocated environment and recording transfer checksums', flush=True)
    with tarfile.open(bundled, 'w:gz', compresslevel=1, dereference=False) as tf:
        tf.add(root, arcname=BUNDLE_NAME, filter=filter_member)
    parts = []
    with bundled.open('rb') as f:
        for index in range(MAX_PARTS+1):
            data = f.read(PART_BYTES)
            if not data:
                break
            if index == MAX_PARTS:
                raise RuntimeError('Bundle exceeds the workflow artifact slots; no completion manifest emitted')
            part = output/f'{PART_PREFIX}{index:02d}'
            part.write_bytes(data)
            parts.append({'index': index, 'name': part.name, 'bytes': len(data),
                          'sha256': hashlib.sha256(data).hexdigest()})
    complete = {'schema': 'bell-lean-offline/v1',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'platform': 'linux-x86_64', 'toolchain': TOOLCHAIN, 'lean_git_hash': LEAN_HASH,
        'payload_root': BUNDLE_NAME, 'archive_bytes': bundled.stat().st_size,
        'archive_sha256': sha(bundled), 'unpacked_regular_bytes': raw_bytes,
        'parts': parts, 'max_part_bytes': PART_BYTES, 'dependency_revisions': revisions,
        'config_sha256': {name: hashlib.sha256(text.encode()).hexdigest()
                          for name, text in pins['files'].items()},
        'smoke_receipt': receipt, 'excluded_nonessential_paths': excluded,
        'paper_kernel_checked': False, 'full_paper_proved': False}
    write_json(output/'environment-manifest.json', complete)
    shutil.copy2(restore_path, output/'restore_environment.py')
    shutil.copytree(root/'receipts', output/'receipts', dirs_exist_ok=True)
    (output/'PARTS.sha256').write_text(''.join(f"{p['sha256']}  {p['name']}\n" for p in parts))
    bundled.unlink()  # separately uploaded parts are the retained transfer representation
    print(json.dumps({'parts': len(parts), 'manifest': str(output/'environment-manifest.json'),
                      'paper_kernel_checked': False}, indent=2), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--pins', type=Path, required=True)
    parser.add_argument('--restore', type=Path, required=True)
    args = parser.parse_args()
    try:
        export(args.work.resolve(), args.output.resolve(), args.pins.resolve(), args.restore.resolve())
    except Exception as exc:
        args.output.mkdir(parents=True, exist_ok=True)
        write_json(args.output/'export-failure.json', {
            'status': 'failed', 'error': str(exc), 'paper_kernel_checked': False})
        raise
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
