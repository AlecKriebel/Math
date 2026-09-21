#!/usr/bin/env python3
"""Verify a version-2 shipment, exact artifacts, Lean proofs, and both PDFs.

The dependency cache is provisioned separately; this is not an independent
rebuild of Mathlib or the compiler. No network isolation is claimed.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(root: Path) -> int:
    seen = set()
    for line in (root / 'SHA256SUMS.txt').read_text().splitlines():
        expected, name = line.split('  ', 1)
        path = root / name
        if name in seen or Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError(f'Unsafe or duplicate manifest path: {name}')
        if any(p.is_symlink() for p in (path, *path.parents) if p != root.parent):
            raise ValueError(f'Symlink in shipment path: {name}')
        if root.resolve() not in path.resolve().parents or digest(path) != expected:
            raise ValueError(f'Shipment checksum mismatch: {name}')
        seen.add(name)
    if not seen:
        raise ValueError('Empty shipment manifest')
    actual = set()
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if any(part in {'.lake', '__pycache__', '.venv', 'reproduction_runs'} for part in rel.parts):
            continue
        if path.is_symlink():
            raise ValueError(f'Symlink in shipment: {rel}')
        if path.is_file() and path != root / 'SHA256SUMS.txt':
            actual.add(rel.as_posix())
    if actual != seen:
        raise ValueError(f'Shipment membership differs: {sorted(actual ^ seen)}')
    return len(seen)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dependency-cache', type=Path,
                       help='prepared .lake/packages directory; only dependencies are reused')
    group.add_argument('--bootstrap', action='store_true',
                       help='allow the Lean runner to acquire pinned dependencies online')
    args = parser.parse_args()
    checked = verify_manifest(ROOT)
    lean = ROOT / 'bell_lean'
    if args.dependency_cache:
        cache = args.dependency_cache.expanduser().resolve(strict=True)
        target = lean / '.lake/packages'
        target.parent.mkdir(exist_ok=True)
        if target.exists() or target.is_symlink():
            if not target.is_symlink() or target.resolve() != cache:
                raise ValueError('Existing dependency directory differs; use a fresh extraction')
        else:
            target.symlink_to(cache, target_is_directory=True)
    now = dt.datetime.now(dt.timezone.utc)
    out = ROOT / 'reproduction_runs' / now.strftime('%Y%m%dT%H%M%SZ')
    out.mkdir(parents=True, exist_ok=False)
    report = {'status': 'in_progress', 'started_utc': now.isoformat(),
              'shipment_manifest_sha256': digest(ROOT / 'SHA256SUMS.txt'),
              'shipment_files_checked': checked, 'commands': [],
              'trust_boundary': 'Pinned compiler/runtime and separately provisioned compiled '
                               'dependency cache are trusted; all project proofs are rebuilt.'}
    path = out / 'receipt.json'
    def save():
        path.write_text(json.dumps(report, indent=2) + '\n')
    save()
    commands = [
        ('exact-artifacts', ['bash', 'run_all.sh'], ROOT),
        ('preflight', [sys.executable, 'scripts/preflight_all.py'], lean),
        ('lean', [sys.executable, 'scripts/run_lean.py', '--serial'] +
                 (['--bootstrap'] if args.bootstrap else []), lean),
        ('pdfs', ['bash', 'paper/build.sh'], ROOT),
    ]
    env = dict(os.environ, PYTHON=sys.executable, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    try:
        for name, command, cwd in commands:
            print(f'Checking {name}...', flush=True)
            log = out / (name + '.log')
            with log.open('w') as stream:
                result = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                                        stderr=subprocess.STDOUT)
            report['commands'].append({'name': name, 'command': command,
                                       'exit_code': result.returncode,
                                       'log': log.relative_to(ROOT).as_posix(),
                                       'log_sha256': digest(log)})
            save()
            if result.returncode:
                raise RuntimeError(f'{name} failed; inspect {log}')
        latest = json.loads((lean / 'reports/latest_run.json').read_text())
        receipt_path = lean / latest['directory'] / 'kernel_report.json'
        receipt = json.loads(receipt_path.read_text())
        axiom_path = receipt_path.parent / 'axiom_audit.json'
        axiom_receipt = json.loads(axiom_path.read_text())
        if (receipt.get('status') != 'passed' or receipt.get('last_stage') != 'complete'
                or receipt.get('run_id') != latest['run_id']
                or not receipt.get('formal_statement_contracts_passed')
                or not receipt.get('all_project_source_kernel_checked')
                or axiom_receipt.get('run_id') != latest['run_id']
                or not axiom_receipt.get('dependency_audit_passed')):
            raise RuntimeError('Lean runner did not produce a successful current receipt')
        report['lean_receipt'] = {'pointer': latest, 'sha256': digest(receipt_path),
                                  'kernel_report': receipt}
        report['pdf_sha256'] = {name: digest(ROOT / 'paper' / name)
                                for name in ('main.pdf', 'review.pdf')}
        report['status'] = 'passed'
    except BaseException as exc:
        report['status'] = 'failed'
        report['error'] = str(exc)
        raise
    finally:
        report['ended_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        save()
    print(f'Complete reproduction passed: {path}', flush=True)


if __name__ == '__main__':
    main()
