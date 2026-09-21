#!/usr/bin/env python3
"""Stage an explicit public version-2 shipment; never publish it.

Requires a Git checkout for selection. Verification uses the staged standalone
reproduce.py and does not require a checkout of this repository.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import zipfile

EFFORT = Path(__file__).resolve().parent
PROJECT = EFFORT.parent
REPO = PROJECT.parent
NAME = 'qubit-povm-pvm-v2.0.0'
OMIT = {'.git', '.lake', '.venv', '__pycache__', 'work'}


def public_files() -> list[Path]:
    tracked = subprocess.check_output(['git', 'ls-files', '-z', '--', PROJECT.name],
                                      cwd=REPO).decode().split('\0')
    roots = {'paper', 'artifacts', 'bell_lean', 'referee_2026-09-11', 'referee_response_20260911'}
    top = {'README.md', 'CITATION.cff', 'LICENSE', '.python-version', 'requirements.txt',
           'run_all.sh', 'reproduce.py', 'VERSION_2.md'}
    paths = {REPO / name for name in tracked if name and
             (Path(name).parts[1] in roots or Path(name).relative_to(PROJECT.name).as_posix() in top)}
    paths |= {PROJECT / name for name in top}
    paths.add(PROJECT / 'bell_lean/CERTIFICATION_20260911.md')
    for directory, pattern in [('bell_lean/Bell', '*.lean'), ('bell_lean/validation', '*.lean'),
                                ('bell_lean/scripts', '*.py'), ('bell_lean/docs', '*.md')]:
        paths.update((PROJECT / directory).rglob(pattern))
    # Public current-run receipts and evidence are selected only after they exist.
    for directory in ('bell_lean/reports', 'version2_completion_20260921/archive_current',
                      'version2_completion_20260921/reviews'):
        paths.update(p for p in (PROJECT / directory).rglob('*') if p.is_file())
    paths.update((PROJECT / 'bell_lean/docs/history').glob('*.md'))
    for path in (EFFORT / 'evidence').glob('*'):
        if path.is_file() and path.name != 'start_state.txt':
            paths.add(path)
    for pattern in ('hilbert*.log', 'finite*.log', '*isometric*.log', '*IsometryAudit.lean',
                    'HilbertAxiomCheck.lean', 'FiniteLabelAxioms.lean'):
        paths.update((PROJECT / 'bell_lean/local_verification').glob(pattern))
    for name in ('stochastic.md', 'finite_labels.md', 'dimension.md', 'manuscript_notes.md',
                 'ARCHIVE_COMPARISON.md'):
        if (EFFORT / name).exists():
            paths.add(EFFORT / name)
    result = []
    for path in sorted(paths):
        rel = path.relative_to(PROJECT)
        if any(part in OMIT for part in rel.parts) or rel.as_posix() in {'SHA256SUMS.txt', 'bell_lean/SHA256SUMS.txt'}:
            continue
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'Missing or symlinked selected input: {rel}')
        if path.suffix in {'.pyc', '.olean', '.ilean', '.o', '.log.tmp'}:
            continue
        if rel.parts[0] == 'paper' and path.suffix not in {'.tex', '.bib', '.sty', '.sh', '.pdf'}:
            continue
        result.append(path)
    # Historical nested manifests are preserved as historical evidence; active
    # artifact and Lean manifests are regenerated for exact selected membership.
    for directory in ('artifacts', 'referee_2026-09-11', 'referee_response_20260911'):
        path = PROJECT / directory / 'SHA256SUMS.txt'
        if path.exists():
            result.append(path)
    return sorted(set(result))


def manifest(root: Path, target: Path) -> None:
    rows = []
    for path in sorted(root.rglob('*')):
        if path.is_file() and path != target:
            rows.append(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' +
                        path.relative_to(root).as_posix() + '\n')
    target.write_text(''.join(rows))


def archive(stage: Path, output: Path) -> dict:
    for path in stage.rglob('*'):
        if path.is_symlink() or any(part in OMIT for part in path.relative_to(stage).parts):
            raise ValueError(f'Runtime directory or symlink in stage: {path}')
    manifest(stage / 'bell_lean', stage / 'bell_lean/SHA256SUMS.txt')
    manifest(stage, stage / 'SHA256SUMS.txt')
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(stage.rglob('*')):
            if not path.is_file():
                continue
            if path.is_symlink():
                raise ValueError(f'Symlink not permitted: {path}')
            entry = zipfile.ZipInfo(NAME + '/' + path.relative_to(stage).as_posix(),
                                    date_time=(2026, 9, 21, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | (path.stat().st_mode & 0o777)) << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(entry, path.read_bytes())
    with zipfile.ZipFile(output) as z:
        if z.testzip() is not None or len(z.namelist()) != len(set(z.namelist())):
            raise ValueError('Invalid ZIP CRC or duplicate entry')
        for path in stage.rglob('*'):
            if path.is_file() and z.read(NAME + '/' + path.relative_to(stage).as_posix()) != path.read_bytes():
                raise ValueError('Source changed while packaging')
    receipt = {'archive': output.name, 'bytes': output.stat().st_size,
               'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
               'shipment_manifest_sha256': hashlib.sha256((stage/'SHA256SUMS.txt').read_bytes()).hexdigest(),
               'integrity_checked': True, 'lean_verified_by_packaging': False,
               'note': 'Proof verification is recorded separately by reproduce.py.'}
    output.with_suffix('.integrity.json').write_text(json.dumps(receipt, indent=2) + '\n')
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', type=Path, default=EFFORT / 'staging' / NAME)
    parser.add_argument('--output', type=Path, default=EFFORT / 'output' / (NAME + '.zip'))
    parser.add_argument('--archive-existing', action='store_true',
                       help='archive a previously selected stage after copying authoritative receipts')
    args = parser.parse_args()
    stage = args.stage.resolve()
    if not args.archive_existing:
        stage.mkdir(parents=True, exist_ok=False)
        for path in public_files():
            dest = stage / path.relative_to(PROJECT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    print(json.dumps(archive(stage, args.output), indent=2))


if __name__ == '__main__':
    main()
