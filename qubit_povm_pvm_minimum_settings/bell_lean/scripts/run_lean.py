#!/usr/bin/env python3
"""Run the pinned Lean build and audits, failing closed with per-run provenance.

Prepare the pinned compiler first. This runner has no compiler installer; a
Lake/elan shim retains its normal behavior. --bootstrap permits dependency-cache
acquisition. Without it, missing checkouts fail before Lake is invoked. This
script is not a network sandbox.
A completed subprocess is not equated with a completed paper proof: the build,
statement checks, dependency audit and final source hash must all succeed.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
PINNED_TOOLCHAIN = 'leanprover/lean4:v4.19.0'
PINNED_LEAN_COMMIT = '6caaee842e9495688c1567e78c0e68dbb96942aa'
PINNED_MATHLIB_COMMIT = 'c44e0c8ee63ca166450922a373c7409c5d26b00b'

class RunFailure(RuntimeError):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code


def write_json(path: Path, value: dict) -> None:
    """Atomic file replacement prevents a truncated status from looking complete."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name+'.tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
    tmp.replace(path)


def source_snapshot(root: Path) -> dict[str, str]:
    files = [root/'Bell.lean', root/'lakefile.toml', root/'lake-manifest.json', root/'lean-toolchain']
    files.append(root/'environment/pins.json')
    # Freeze the generated declaration inventory and serial-build order too.
    files.extend(root/p for p in ('reports/declarations.json',
                                  'reports/source_completion/source_inventory.json'))
    for directory in ('Bell', 'validation', 'scripts'):
        files.extend(p for p in (root/directory).rglob('*')
                     if p.is_file() and p.suffix in {'.lean', '.py', '.sh'}
                     and '__pycache__' not in p.parts)
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(set(files))}


def validate_pins(root: Path) -> list[dict]:
    tc = (root/'lean-toolchain').read_text().strip()
    if tc != PINNED_TOOLCHAIN:
        raise RunFailure(f'Unexpected lean-toolchain: {tc!r}')
    pin = json.loads((root/'environment/pins.json').read_text())
    if pin['toolchain'] != PINNED_TOOLCHAIN or pin['lean_git_hash'] != PINNED_LEAN_COMMIT:
        raise RunFailure('Environment toolchain pins do not match the reviewed release.')
    for name, content in pin['files'].items():
        if (root/name).read_text() != content:
            raise RunFailure(f'{name} differs from the reviewed environment pins. Do not run lake update.')
    manifest = json.loads((root/'lake-manifest.json').read_text())
    packages = manifest['packages']
    if len({p['name'] for p in packages}) != len(packages):
        raise RunFailure('Duplicate dependency name in manifest.')
    mathlib = [p for p in packages if p['name'] == 'mathlib']
    if len(mathlib) != 1 or mathlib[0]['rev'] != PINNED_MATHLIB_COMMIT:
        raise RunFailure('Wrong Mathlib revision.')
    for p in packages:
        if not re.fullmatch(r'[A-Za-z0-9_-]+', p['name']) or not re.fullmatch(r'[0-9a-f]{40}', p['rev']):
            raise RunFailure('Unsafe or unpinned package descriptor.')
    return packages


def inspect_compiler(version: str, commit: str) -> None:
    if re.search(r'\bversion 4\.19\.0(?=[,\s)]|$)', version) is None:
        raise RunFailure(f'Wrong Lean version: {version.strip()}')
    if commit.strip() != PINNED_LEAN_COMMIT:
        raise RunFailure(f'Wrong Lean Git revision: {commit.strip()}')


def require_negative_control_rejection(code: int, log: str) -> None:
    if code == 0:
        raise RunFailure('Compiler accepted the intentionally invalid proof. Stop verification.')
    if 'error:' not in log or not re.search(r'type mismatch|has type', log, flags=re.I):
        raise RunFailure('Invalid-proof smoke test failed for an unrelated reason; not counted as rejection.')


def check_no_errors(log: str, stage: str) -> None:
    if re.search(r'(?m)\berror:', log) or 'declaration uses \'sorry\'' in log or 'sorryAx' in log or 'PANIC' in log:
        raise RunFailure(f'{stage}: proof error or incomplete-proof diagnostic in log.')


def initial_reports(root: Path, run_dir: Path, run_id: str) -> None:
    for name in ('kernel_report.json', 'axiom_audit.json', 'statement_audit.json'):
        old = root/'reports'/name
        if old.is_file():
            (run_dir/'previous').mkdir(exist_ok=True)
            shutil.copyfile(old, run_dir/'previous'/name)
        write_json(old, {'status': 'not_run', 'run_id': run_id,
                        'dependency_audit_passed': False,
                        'main_declarations_kernel_checked': False,
                        'all_imported_source_kernel_checked': False})


def run(args: argparse.Namespace, root: Path = ROOT) -> int:
    reports = root/'reports'
    reports.mkdir(exist_ok=True)
    lock = reports/'.lean-run.lock'
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        print('Another run owns reports/.lean-run.lock. After a crashed run, confirm no process remains before removing it.', file=sys.stderr)
        return 2
    run_id = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    os.write(fd, json.dumps({'pid': os.getpid(), 'run_id': run_id}).encode())
    os.close(fd)
    run_dir = reports/'runs'/run_id
    run_dir.mkdir(parents=True)
    stage = 'initialization'
    commands: list[dict] = []
    lean_invoked = False
    snapshot: dict = {}
    error = None
    status_code = 1
    audit = None
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    (run_dir/'command.json').write_text(json.dumps(vars(args), indent=2)+'\n')

    def command(argv: list[str], name: str, allow_failure: bool = False) -> tuple[int, str]:
        logfile = run_dir/(f'{len(commands):03d}-'+name+'.log')
        print('$ '+' '.join(argv), flush=True)
        # Real executable only; tests mock this subprocess API in temporary roots.
        with logfile.open('w') as stream:
            proc = subprocess.Popen(argv, cwd=root, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            try:
                assert proc.stdout is not None
                for line in proc.stdout:
                    stream.write(line)
                    stream.flush()
                    print(line, end='', flush=True)
                code = proc.wait()
            except BaseException:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill(); proc.wait()
                raise
        text = logfile.read_text()
        commands.append({'argv': argv, 'exit_code': code, 'log': str(logfile.relative_to(root)),
                         'log_sha256': hashlib.sha256(logfile.read_bytes()).hexdigest()})
        write_json(run_dir/'commands.json', {'commands': commands})
        if code != 0 and not allow_failure:
            raise RunFailure(f'{stage} failed with exit code {code}; see {logfile}', code if 0 < code < 126 else 1)
        return code, text

    def verify_dependencies(packages: list[dict]) -> None:
        for pkg in packages:
            path = root/'.lake/packages'/pkg['name']
            if not (path/'.git').exists():
                raise RunFailure(f'Missing checkout: {path}. Prepare with --bootstrap while online, or restore the pinned environment.')
            _, rev = command(['git', '-C', str(path), 'rev-parse', 'HEAD'], 'pin-'+pkg['name'])
            if rev.strip() != pkg['rev']:
                raise RunFailure(f"Dependency {pkg['name']} is at {rev.strip()}, expected {pkg['rev']}.")
            code, _ = command(['git', '-C', str(path), 'diff', '--quiet', 'HEAD', '--'], 'clean-'+pkg['name'], True)
            if code != 0:
                raise RunFailure(f"Dependency {pkg['name']} has modified tracked files; review rather than silently trusting them.")

    try:
        initial_reports(root, run_dir, run_id)
        stage = 'configuration_pins'
        packages = validate_pins(root)
        stage = 'static_source_audit'
        command([sys.executable, 'scripts/source_audit.py'], 'source-audit')
        command([sys.executable, 'scripts/source_completion_inventory.py'], 'import-inventory')
        command([sys.executable, 'scripts/preflight_checks.py'], 'preflight-static')
        snapshot = source_snapshot(root)
        write_json(run_dir/'source_snapshot.json', snapshot)
        stage = 'toolchain_discovery'
        if shutil.which('lake') is None:
            raise RunFailure('Lean build NOT RUN: lake is not installed or is not on PATH.', 127)
        if not args.bootstrap:
            stage = 'dependency_precheck'
            verify_dependencies(packages)
        stage = 'compiler_identity'
        _, version = command(['lake', 'env', 'lean', '--version'], 'lean-version')
        _, commit = command(['lake', 'env', 'lean', '--githash'], 'lean-githash')
        inspect_compiler(version, commit)
        if args.bootstrap:
            stage = 'dependency_cache'
            # Interpret the pinned cache tool: older Lean native linkers can produce
            # executables rejected by current macOS dyld. This runs identical
            # pinned Mathlib source without modifying compiler/dependencies.
            command(['lake', 'env', 'lean', '--run',
                     '.lake/packages/mathlib/Cache/Main.lean', 'get'], 'dependency-cache')
        stage = 'dependency_identity'
        verify_dependencies(packages)
        stage = 'compiler_controls'
        good = run_dir/'SmokeValid.lean'
        bad = run_dir/'SmokeInvalid.lean'
        good.write_text('import Mathlib\nexample (x y : ℝ) : (x+y)^2 = x^2+2*x*y+y^2 := by ring\n')
        bad.write_text('import Mathlib\nexample : False := True.intro\n')
        _, smoke = command(['lake', 'env', 'lean', str(good.relative_to(root))], 'smoke-valid')
        check_no_errors(smoke, stage)
        code, smoke = command(['lake', 'env', 'lean', str(bad.relative_to(root))], 'smoke-invalid', True)
        require_negative_control_rejection(code, smoke)
        stage = 'fresh_project_build'
        # Dependencies retain their pinned cache; local proof outputs never
        # stand in for checking this source. Preserve old build products locally.
        local_build = root/'.lake/build'
        if (root/'.lake').is_symlink() or local_build.is_symlink():
            raise RunFailure('Refusing to move symlinked local build directories.')
        if local_build.exists():
            backup = root/'.lake/preflight-builds'/run_id
            backup.parent.mkdir(parents=True, exist_ok=True)
            local_build.rename(backup)
            write_json(run_dir/'previous_project_build.json', {'moved_to': str(backup.relative_to(root))})
        stage = 'lean_build'
        lean_invoked = True
        if args.serial:
            order = json.loads((reports/'source_completion/source_inventory.json').read_text())['topological_module_order']
            for module in order:
                _, text = command(['lake', 'build', module], 'build-'+module)
                check_no_errors(text, stage)
        _, text = command(['lake', 'build', 'Bell'], 'build-Bell')
        check_no_errors(text, stage)
        stage = 'statement_contracts'
        _, text = command(['lake', 'env', 'lean', 'validation/Statements.lean'], 'statement-contracts')
        check_no_errors(text, stage)
        _, text = command(['lake', 'env', 'lean', 'validation/PhysicalContracts.lean'], 'physical-contracts')
        check_no_errors(text, stage)
        write_json(run_dir/'statement_audit.json', {'status': 'passed', 'run_id': run_id,
                       'source': 'validation/Statements.lean',
                       'supplementary_source': 'validation/PhysicalContracts.lean',
                       'formal_statement_contracts_passed': True,
                       'independent_mathematical_referee_review': False})
        stage = 'dependency_audit'
        _, log = command(['lake', 'env', 'lean', 'Bell/Audit.lean'], 'axioms')
        check_no_errors(log, stage)
        sys.path.insert(0, str(root/'scripts'))
        from check_axioms import inspect_reports, REQUIRED_MAIN
        declarations = json.loads((reports/'declarations.json').read_text())
        names = {d['name'] for d in declarations if d.get('visibility') != 'private'}
        if REQUIRED_MAIN-names:
            raise RunFailure('Main declarations missing from dependency inventory.')
        results = inspect_reports(log, declarations)
        stage = 'source_and_dependencies_unchanged'
        if source_snapshot(root) != snapshot:
            raise RunFailure('Source/configuration changed during verification; results discarded.')
        verify_dependencies(packages)
        audit = {'status': 'passed', 'run_id': run_id, 'dependency_audit_passed': True,
                 'main_declarations_dependency_audited': True,
                 'source_snapshot_sha256': hashlib.sha256((run_dir/'source_snapshot.json').read_bytes()).hexdigest(),
                 'declarations': results,
                 'allowed_standard_axioms': ['Classical.choice', 'Quot.sound', 'propext']}
        stage = 'complete'
        status_code = 0
    except KeyboardInterrupt:
        status_code = 130; error = 'Interrupted; no full verification success claimed.'
    except (RunFailure, OSError, ValueError, AssertionError, KeyError) as exc:
        status_code = exc.code if isinstance(exc, RunFailure) else 1
        error = str(exc)
        print(error, file=sys.stderr)
    finally:
        passed = status_code == 0 and stage == 'complete'
        receipt = {'status': 'passed' if passed else 'failed_or_not_run', 'run_id': run_id,
                   'started_utc': start, 'ended_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                   'exit_code': status_code, 'last_stage': stage, 'error': error,
                   'lean_build_invoked': lean_invoked, 'all_imported_source_kernel_checked': passed,
                   'main_declarations_kernel_checked': passed,
                   'formal_statement_contracts_passed': passed,
                   'statement_to_manuscript_review_required': True,
                   'logs_directory': run_dir.relative_to(root).as_posix(),
                   'source_snapshot': snapshot, 'commands': commands,
                   'note': 'Static/smoke/subset success is not full success. Compiler/cache producer remains a trust assumption.'}
        write_json(run_dir/'kernel_report.json', receipt)
        write_json(reports/'kernel_report.json', receipt)
        if passed:
            write_json(run_dir/'axiom_audit.json', audit)
            write_json(reports/'axiom_audit.json', audit)
            shutil.copyfile(run_dir/'statement_audit.json', reports/'statement_audit.json')
        else:
            not_run = {'status': 'not_completed', 'run_id': run_id,
                       'dependency_audit_passed': False,
                       'main_declarations_dependency_audited': False,
                       'formal_statement_contracts_passed': False, 'error': error}
            write_json(reports/'axiom_audit.json', not_run)
            write_json(reports/'statement_audit.json', not_run)
        write_json(reports/'latest_run.json', {'run_id': run_id, 'directory': run_dir.relative_to(root).as_posix()})
        lock.unlink(missing_ok=True)
    if status_code == 0:
        print('PASS: full imported build, statement contracts, exact dependency audit, and unchanged-source check.')
    else:
        print('NOT VERIFIED: inspect reports/kernel_report.json and its per-run logs.')
    return status_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bootstrap', action='store_true', help='Permit dependency acquisition while online.')
    parser.add_argument('--serial', action='store_true', help='Build project modules in dependency order, preserving Lake caches.')
    return run(parser.parse_args())

if __name__ == '__main__':
    raise SystemExit(main())
