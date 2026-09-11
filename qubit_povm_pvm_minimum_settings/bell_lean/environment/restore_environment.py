#!/usr/bin/env python3
"""Restore a split Linux Lean 4.19/Mathlib export without Internet access.

Accepts raw part files or the ZIP artifacts returned by GitHub. Transfer hashes
are integrity checks, not a signature on an untrusted producer. Use exports from
an inspected workflow run. Default mode runs positive AND negative Lean smoke
checks after extraction. --extract-only makes NO compiler-verification claim.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import posixpath
import re
import shutil
import subprocess
import tarfile
import tempfile
import zipfile

LEAN_HASH = '6caaee842e9495688c1567e78c0e68dbb96942aa'
TOOLCHAIN = 'leanprover/lean4:v4.19.0'
BUNDLE_NAME = 'bell-lean419-environment'
PART_PREFIX = 'bell-lean419-linux-x64.tar.gz.part-'
MAX_PART_BYTES = 400*1024*1024


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')


@contextmanager
def open_source(source: tuple[Path, str | None]):
    path, member = source
    if member is None:
        with path.open('rb') as f:
            yield f
    else:
        with zipfile.ZipFile(path) as z, z.open(member) as f:
            yield f


def locate(directory: Path, name: str) -> list[tuple[Path, str | None]]:
    found = [(p, None) for p in directory.rglob(name) if p.is_file()]
    for p in sorted(directory.rglob('*.zip')):
        with zipfile.ZipFile(p) as z:
            for info in z.infolist():
                if not info.is_dir() and PurePosixPath(info.filename).name == name:
                    found.append((p, info.filename))
    return found


def load_manifest(directory: Path, explicit: Path | None) -> dict:
    if explicit is not None and explicit.suffix.lower() != '.zip':
        data = explicit.read_bytes()
    else:
        locations = (locate(directory, 'environment-manifest.json') if explicit is None
                     else [(explicit, i.filename) for i in zipfile.ZipFile(explicit).infolist()
                           if PurePosixPath(i.filename).name == 'environment-manifest.json'])
        if not locations:
            raise ValueError('No environment-manifest.json found in raw files or artifact ZIPs')
        alternatives = []
        for source in locations:
            with open_source(source) as f:
                content = f.read(4*1024*1024+1)
            if len(content) > 4*1024*1024:
                raise ValueError('Oversized manifest')
            alternatives.append(content)
        if len(set(alternatives)) != 1:
            raise ValueError('Conflicting manifests; select the correct one with --manifest')
        data = alternatives[0]
    result = json.loads(data)
    validate_manifest(result)
    return result


def validate_manifest(m: dict) -> None:
    if m.get('schema') != 'bell-lean-offline/v1':
        raise ValueError('Unsupported manifest schema')
    if (m.get('lean_git_hash') != LEAN_HASH or m.get('toolchain') != TOOLCHAIN
            or m.get('platform') != 'linux-x86_64' or m.get('payload_root') != BUNDLE_NAME):
        raise ValueError('Unexpected platform/toolchain/payload pins')
    parts = m.get('parts')
    if not isinstance(parts, list) or not (1 <= len(parts) <= 12):
        raise ValueError('Invalid part count')
    for i, p in enumerate(parts):
        if p.get('index') != i or p.get('name') != f'{PART_PREFIX}{i:02d}':
            raise ValueError('Parts must be contiguous and canonically named')
        if not isinstance(p.get('bytes'), int) or not (0 < p['bytes'] <= MAX_PART_BYTES):
            raise ValueError('Invalid part length')
        if not re.fullmatch(r'[0-9a-f]{64}', p.get('sha256', '')):
            raise ValueError('Invalid part SHA-256')
    if sum(p['bytes'] for p in parts) != m.get('archive_bytes'):
        raise ValueError('Part sizes do not sum to the archive size')
    if not re.fullmatch(r'[0-9a-f]{64}', m.get('archive_sha256', '')):
        raise ValueError('Invalid archive hash')
    if not isinstance(m.get('unpacked_regular_bytes'), int) or m['unpacked_regular_bytes'] < 0:
        raise ValueError('Invalid unpacked size')
    if m.get('paper_kernel_checked') is not False or m.get('full_paper_proved') is not False:
        raise ValueError('An environment export must not claim the paper is proved')


def combine(directory: Path, manifest: dict, destination: Path) -> None:
    whole = hashlib.sha256()
    with destination.open('xb') as target:
        for part in manifest['parts']:
            candidates = locate(directory, part['name'])
            if not candidates:
                raise ValueError(f"Missing part: {part['name']}")
            # Refuse ambiguous duplicate representations rather than guessing.
            if len(candidates) != 1:
                raise ValueError(f"Duplicate part {part['name']}; use a directory with one copy per part")
            digest = hashlib.sha256()
            count = 0
            with open_source(candidates[0]) as f:
                for chunk in iter(lambda: f.read(1024*1024), b''):
                    count += len(chunk)
                    if count > part['bytes']:
                        raise ValueError('Part longer than the manifest declares')
                    digest.update(chunk)
                    whole.update(chunk)
                    target.write(chunk)
            if count != part['bytes'] or digest.hexdigest() != part['sha256']:
                raise ValueError(f"Part integrity failure: {part['name']}")
    if whole.hexdigest() != manifest['archive_sha256']:
        raise ValueError('Combined archive SHA-256 mismatch')


def safe_name(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if '\\' in name or '\x00' in name or path.is_absolute() or '..' in path.parts:
        raise ValueError(f'Unsafe archive path: {name!r}')
    if not path.parts or path.parts[0] != BUNDLE_NAME:
        raise ValueError('All archive entries must be inside the one expected payload directory')
    return path


def extract(archive: Path, directory: Path, expected_bytes: int) -> Path:
    seen = set()
    hardlinks = []
    directory_modes = []
    total = 0
    root = directory/BUNDLE_NAME
    with tarfile.open(archive, 'r|gz') as tf:
        for member in tf:
            relative = safe_name(member.name)
            if relative.as_posix() in seen:
                raise ValueError(f'Duplicate archive entry: {relative}')
            seen.add(relative.as_posix())
            target = directory.joinpath(*relative.parts)
            # Resolve every existing parent, rejecting an archive symlink escape.
            if not target.parent.resolve().is_relative_to(directory.resolve()):
                raise ValueError('Archive parent escapes the extraction directory')
            target.parent.mkdir(parents=True, exist_ok=True)
            if member.isdir():
                target.mkdir(exist_ok=True)
                if target.is_symlink():
                    raise ValueError('Directory collides with symlink')
                directory_modes.append((target, member.mode & 0o777))
            elif member.isfile():
                total += member.size
                if total > expected_bytes:
                    raise ValueError('Archive exceeds the declared unpacked size')
                source = tf.extractfile(member)
                if source is None:
                    raise ValueError('Missing archive file stream')
                with source, target.open('xb') as f:
                    shutil.copyfileobj(source, f, 1024*1024)
                os.chmod(target, member.mode & 0o777)
            elif member.issym():
                link = member.linkname
                if PurePosixPath(link).is_absolute() or '\\' in link or '\x00' in link:
                    raise ValueError('Unsafe symlink')
                normalized = posixpath.normpath(posixpath.join(str(relative.parent), link))
                safe_name(normalized)
                os.symlink(link, target)
            elif member.islnk():
                link = safe_name(member.linkname)
                hardlinks.append((target, directory.joinpath(*link.parts)))
            else:
                raise ValueError('Archive contains a device, FIFO, or other unsupported entry')
    if total != expected_bytes:
        raise ValueError('Unpacked regular-file byte count does not match the manifest')
    while hardlinks:
        pending = []
        made = 0
        for target, source in hardlinks:
            if source.is_file() and not source.is_symlink():
                if not source.resolve().is_relative_to(root.resolve()):
                    raise ValueError('Hardlink escapes payload')
                os.link(source, target)
                made += 1
            else:
                pending.append((target, source))
        if not made:
            raise ValueError('Unresolved or cyclic hardlinks')
        hardlinks = pending
    for path, mode in reversed(directory_modes):
        os.chmod(path, mode)
    return root


def execute(command: list[str], cwd: Path, env: dict[str, str], log: Path) -> tuple[int, str]:
    with log.open('w') as output:
        p = subprocess.run(command, cwd=cwd, env=env, stdout=output,
                           stderr=subprocess.STDOUT, check=False)
    return p.returncode, log.read_text(errors='replace')


def validate_restored(root: Path, manifest: dict) -> dict:
    if platform.system() != 'Linux' or platform.machine() not in ('x86_64', 'AMD64'):
        raise ValueError('Executing this toolchain requires Linux x86_64; use --extract-only for byte checks elsewhere')
    receipts = root/'restore-receipts'
    receipts.mkdir()
    workspace = root/'workspace'
    for name, expected in manifest['config_sha256'].items():
        if name not in ('lakefile.toml', 'lake-manifest.json', 'lean-toolchain'):
            raise ValueError('Unexpected configuration filename')
        if hashlib.sha256((workspace/name).read_bytes()).hexdigest() != expected:
            raise ValueError('Extracted configuration hash mismatch')
    packages = json.loads((workspace/'lake-manifest.json').read_text())['packages']
    for p in packages:
        code, actual = execute(['git', 'rev-parse', 'HEAD'], workspace/'.lake/packages'/p['name'],
                              os.environ.copy(), receipts/f"{p['name']}-head.log")
        if code or actual.strip() != p['rev'] or manifest['dependency_revisions'][p['name']] != p['rev']:
            raise ValueError(f"Dependency revision mismatch: {p['name']}")
    relative_paths = json.loads((root/'lean-paths.json').read_text())
    for relative in relative_paths:
        candidate = (root/relative).resolve()
        if not candidate.is_relative_to(root.resolve()):
            raise ValueError('Library search path escapes the restored environment')
    env = os.environ.copy()
    env['PATH'] = str(root/'runtime/bin') + os.pathsep + env.get('PATH', '')
    env['LEAN_PATH'] = os.pathsep.join(str(root/p) for p in relative_paths)
    env.pop('LEAN_SYSROOT', None)
    lean = str(root/'runtime/bin/lean')
    code, text = execute([lean, '--githash'], workspace, env, receipts/'githash.log')
    if code or text.strip() != LEAN_HASH:
        raise ValueError('Restored Lean revision mismatch or executable failure')
    code, version = execute([lean, '--version'], workspace, env, receipts/'version.log')
    if code:
        raise ValueError('Cannot run restored Lean')
    code, text = execute([lean, 'EnvironmentSmoke.lean'], workspace, env, receipts/'positive.log')
    if code or 'sorryAx' in text:
        raise ValueError('Restored positive Lean test failed; inspect restore-receipts/positive.log')
    negative, text = execute([lean, 'EnvironmentNegative.lean'], workspace, env, receipts/'negative.log')
    if negative == 0 or 'unsolved goals' not in text:
        raise ValueError('Restored negative Lean test did not fail for the expected reason')
    result = {'status': 'environment_smoke_passed', 'lean_git_hash': LEAN_HASH,
              'lean_version': version.strip(), 'positive_exit': code,
              'negative_exit': negative, 'paper_kernel_checked': False,
              'full_paper_proved': False, 'note': 'No Bell theorem was checked by these smoke tests.'}
    write_json(receipts/'result.json', result)
    return result


def attach_project(root: Path, project: Path, build: bool) -> dict:
    project = project.resolve()
    workspace = root/'workspace'
    if (project/'lean-toolchain').read_text().strip() != TOOLCHAIN:
        raise ValueError('Project toolchain pin differs')
    if json.loads((project/'lake-manifest.json').read_text()) != json.loads((workspace/'lake-manifest.json').read_text()):
        raise ValueError('Project dependency manifest differs from the exported environment')
    if (project/'lakefile.toml').read_bytes() != (workspace/'lakefile.toml').read_bytes():
        raise ValueError('Project Lake configuration differs')
    destination = project/'.lake/packages'
    source = workspace/'.lake/packages'
    destination.parent.mkdir(exist_ok=True)
    if os.path.lexists(destination):
        if not destination.is_symlink() or destination.resolve() != source.resolve():
            raise ValueError('Project already has dependencies; refusing to replace them')
    else:
        destination.symlink_to(source, target_is_directory=True)
    result = {'dependencies_attached_to': str(project), 'build_invoked': False,
              'paper_kernel_checked': False, 'full_paper_proved': False}
    if build:
        env = os.environ.copy()
        env['PATH'] = str(root/'runtime/bin')+os.pathsep+env.get('PATH', '')
        env.pop('LEAN_PATH', None)
        env.pop('LEAN_SYSROOT', None)
        report = project/'reports/offline-build.log'
        report.parent.mkdir(exist_ok=True)
        code, text = execute(['bash', 'scripts/check.sh'], project, env, report)
        result.update({'build_invoked': True, 'build_exit': code, 'build_log': str(report),
                       'note': 'Inspect the project kernel report; even a subset build does not prove the full paper.'})
        print(text[-12000:])
    return result


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--parts', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--manifest', type=Path)
    p.add_argument('--extract-only', action='store_true')
    p.add_argument('--project', type=Path)
    p.add_argument('--build-project', action='store_true')
    args = p.parse_args()
    if args.build_project and (args.project is None or args.extract_only):
        p.error('--build-project requires --project and compiler validation')
    if args.extract_only and args.project is not None:
        p.error('--extract-only cannot attach or build a project')
    output = args.output.resolve()
    if os.path.lexists(output):
        raise SystemExit(f'Refusing to overwrite existing output: {output}')
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(args.parts.resolve(), args.manifest)
    needed = manifest['archive_bytes']+manifest['unpacked_regular_bytes']+64*1024*1024
    if shutil.disk_usage(output.parent).free < needed:
        raise SystemExit('Insufficient free disk for assembly and extraction')
    with tempfile.TemporaryDirectory(prefix='.bell-restore-', dir=output.parent) as tmp:
        temporary = Path(tmp)
        archive = temporary/'payload.tar.gz'
        combine(args.parts.resolve(), manifest, archive)
        root = extract(archive, temporary/'extracted', manifest['unpacked_regular_bytes'])
        root.rename(output)
    write_json(output/'transfer-manifest.json', manifest)
    result = {'status': 'bytes_restored_not_compiler_checked', 'output': str(output),
              'paper_kernel_checked': False, 'full_paper_proved': False}
    if not args.extract_only:
        try:
            result.update(validate_restored(output, manifest))
            if args.project is not None:
                result['project'] = attach_project(output, args.project, args.build_project)
        except Exception as exc:
            write_json(output/'restore-status.json', {**result, 'status': 'validation_failed', 'error': str(exc)})
            raise
    write_json(output/'restore-status.json', result)
    print(json.dumps(result, indent=2))
    return result.get('project', {}).get('build_exit', 0)

if __name__ == '__main__':
    raise SystemExit(main())
