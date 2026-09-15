#!/usr/bin/env python3
"""Fail-closed clean candidate build and axiom audit; no automatic paper certification.

Run from the companion root:
  python3 scripts/check.py --bootstrap --manuscript ../main.tex

Requires Python >=3.10, Git, and Lean/Lake (normally through elan). --bootstrap
fetches exact locked dependency commits and their Mathlib cache. It never updates
the manuscript, changes branches, commits, pushes, or resets existing work.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import traceback

from static_audit import audit, ROOT, strip_comments_strings

ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
COMPILER = '6caaee842e9495688c1567e78c0e68dbb96942aa'
SOURCE_BLOB = 'bbd0667c934d5a34dd9c8ced50df91515cb1308c'
SOURCE_SHA256 = '82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71'

# Exhausting resources is not evidence that a false theorem was mathematically
# rejected. These diagnostics invalidate both ordinary and negative-control runs.
RESOURCE_DIAGNOSTIC = re.compile(
    r'(?i)(maximum (?:number of )?(?:heartbeats|recursion depth)|'
    r'(?:deterministic[) ]*)?timeout|time limit (?:exceeded|reached)|'
    r'out of memory|memory exhausted|std::bad_alloc|bad allocation|'
    r'stack overflow|resource (?:exhausted|limit)|killed by signal|'
    r'interrupted by signal|process (?:was )?killed)')


def protected_fingerprints():
    paths = [ROOT/'lean-toolchain', ROOT/'lakefile.toml', ROOT/'lake-manifest.json',
             ROOT/'STATEMENT_CONTRACT.md', ROOT/'CyclicBell.lean']
    paths.extend(ROOT.glob('*.md'))
    paths.extend(ROOT.glob('*REPORT.json'))
    if (ROOT/'SOURCE_HASHES.sha256').exists(): paths.append(ROOT/'SOURCE_HASHES.sha256')
    for sub in ['CyclicBell','validation','scripts','reference']:
        paths.extend(p for p in (ROOT/sub).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}


def parse_axioms(text, expected):
    result = {}
    pat = re.compile(r"'([^\n]+?)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", re.S)
    for m in pat.finditer(text):
        name = m.group(1)
        axioms = [] if m.group(2) is None else [a.strip() for a in m.group(2).split(',') if a.strip()]
        if name in result:
            raise ValueError(f'Duplicate dependency report: {name}')
        if set(axioms) - ALLOWED_AXIOMS:
            raise ValueError(f'Unapproved axioms for {name}: {axioms}')
        result[name] = axioms
    if set(result) != set(expected):
        raise ValueError(f'Missing/extra dependency reports. Missing: {set(expected)-set(result)}; extra: {set(result)-set(expected)}')
    return result


def validate_negative_diagnostics(text: str, control: Path):
    """Require proof diagnostics in this control's sole example proof.

    This is a mutation smoke test, not a proof that the target is false. In
    particular, a type mismatch in an attempted proof can reject a true target.
    Semantic rejection must also be justified by checked mathematical results.
    """
    source = strip_comments_strings(control.read_text())
    examples = list(re.finditer(r'^\s*example\b', source, re.M))
    if len(examples) != 1:
        raise RuntimeError('Negative control must contain exactly one example')
    proof = re.search(r':=\s*(by)\b', source[examples[0].end():])
    if proof is None:
        raise RuntimeError('Negative control must use an explicit tactic proof')
    offset = examples[0].end() + proof.start(1)
    proof_line = source.count('\n', 0, offset) + 1
    proof_column = offset - source.rfind('\n', 0, offset) - 1  # Lean columns are zero based.
    headers = list(re.finditer(r'^(.+?):(\d+):(\d+): error:([^\n]*)', text, re.M))
    if not headers:
        raise RuntimeError('Negative control has no source-located Lean proof diagnostic')
    if len(re.findall(r'\berror:', text)) != len(headers):
        raise RuntimeError('Negative control contains an unlocated error')
    recognized = re.compile(r'(?i)(unsolved goals|tactic\b.*\bfailed|type mismatch)')
    for header in headers:
        filename, line, column, message = header.groups()
        diagnostic_path = Path(filename)
        if not diagnostic_path.is_absolute():
            # Lean is invoked at the companion root and receives the relative
            # path to the validation file. Do not accept another file's error.
            diagnostic_path = control.parent.parent / diagnostic_path
        if diagnostic_path.resolve() != control.resolve():
            raise RuntimeError('Negative control failed in a different source file')
        if (int(line), int(column)) < (proof_line, proof_column):
            raise RuntimeError('Negative control failed in its statement or imports')
        if not recognized.search(message):
            raise RuntimeError('Negative control contains an unrelated compiler error: '+message.strip())


class Runner:
    def __init__(self, directory):
        self.directory = directory
        self.commands = []

    def run(self, args, *, cwd=ROOT, expect_failure=False):
        i = len(self.commands) + 1
        logfile = self.directory / f'{i:03d}.log'
        started = datetime.now(timezone.utc).isoformat()
        p = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        text = p.stdout
        logfile.write_text(text)
        self.commands.append({'command': list(map(str,args)), 'cwd': str(cwd), 'started_utc': started,
                              'exit_code': p.returncode, 'expected_failure': expect_failure,
                              'log': logfile.name, 'log_sha256': hashlib.sha256(logfile.read_bytes()).hexdigest()})
        if p.returncode < 0:
            raise RuntimeError(f'Process terminated by signal {-p.returncode}; see {logfile.name}')
        resource = RESOURCE_DIAGNOSTIC.search(text)
        if resource:
            raise RuntimeError(f'Resource failure is not a proof rejection: {resource.group()} ({logfile.name})')
        bad = re.search(r'(?i)(panic|segmentation fault|sorryAx|declaration uses .?sorry|unknown module|unknown package|unknown identifier|unknown constant|unknown namespace|invalid field|failed to synthesize|unexpected token|object file .* does not exist|failed to load)', text)
        if bad:
            raise RuntimeError(f'Invalid run diagnostic: {bad.group()} ({logfile.name})')
        if expect_failure:
            if p.returncode == 0:
                raise RuntimeError(f'False control accepted: {args}')
            # Lean's ordinary command-line proof-error exit is 1. Shell failures,
            # process kills (for example 137), and loader failures are not controls.
            if p.returncode != 1:
                raise RuntimeError(f'Abnormal negative-control exit {p.returncode}; see {logfile.name}')
            control = Path(args[-1])
            if not control.is_absolute(): control = Path(cwd)/control
            validate_negative_diagnostics(text, control)
        elif p.returncode:
            raise RuntimeError(f'Command failed with exit {p.returncode}; see {logfile.name}')
        elif re.search(r'(^|\n).*\berror:', text):
            raise RuntimeError('Compiler reported an error despite zero exit status')
        return text.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bootstrap', action='store_true')
    ap.add_argument('--manuscript', type=Path, default=ROOT.parent/'main.tex')
    args = ap.parse_args()
    start = datetime.now(timezone.utc)
    run_id = start.strftime('%Y%m%dT%H%M%S%fZ')
    directory = ROOT/'logs'/'runs'/run_id
    directory.mkdir(parents=True, exist_ok=False)
    runner = Runner(directory)
    report = {'status': 'started', 'kernel_checked': False, 'formal_endpoint_certified': False,
              'started_utc': start.isoformat(), 'run_id':run_id, 'commands':runner.commands,
              'remaining_scope_gaps': ['offline elaboration/proof repair until this command succeeds',
                  'independent statement and manuscript-correspondence review',
                  'general Qqa subset Qqc/closedness theorem not supplied and not required for these values',
                  'full canonical source-Z/polar strategy identification not supplied']}
    exit_code = 2
    try:
        before = protected_fingerprints()
        report['protected_source_hashes'] = before
        report['static_audit'] = audit()
        if shutil.which('lake') is None or shutil.which('lean') is None:
            raise RuntimeError('BLOCKED: Lake/Lean is not installed or not on PATH; no Lean command was executed')
        if shutil.which('git') is None:
            raise RuntimeError('BLOCKED: Git is unavailable')
        source = args.manuscript.expanduser().resolve()
        if not source.is_file():
            raise RuntimeError(f'BLOCKED: canonical manuscript not present at {source}; place the companion next to the matching main.tex')
        data = source.read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        digest = hashlib.sha256(data).hexdigest()
        report['manuscript'] = {'path': str(source), 'git_blob_sha1':blob, 'sha256':digest, 'bytes':len(data)}
        if blob != SOURCE_BLOB or digest != SOURCE_SHA256:
            raise RuntimeError('BLOCKED: manuscript differs from statement-contract baseline; review/reconcile rather than silently certify another source')
        version = runner.run(['lean','--version'])
        report['lean_version'] = version
        if not re.search(r'\b4\.19\.0\b', version):
            raise RuntimeError('Lean version mismatch')
        compiler = runner.run(['lean','--githash'])
        if compiler != COMPILER:
            raise RuntimeError(f'Compiler commit mismatch: {compiler}')
        report['compiler_commit'] = compiler
        lock = json.loads((ROOT/'lake-manifest.json').read_text())
        lake_dir = ROOT/'.lake'
        if lake_dir.is_symlink():
            raise RuntimeError('Refusing to clean or populate a symlinked .lake directory')
        package_root = lake_dir/'packages'
        if package_root.is_symlink():
            raise RuntimeError('Refusing to populate a symlinked package directory')
        package_root.mkdir(parents=True,exist_ok=True)
        for package in lock['packages']:
            path = package_root/package['name']
            if path.is_symlink():
                raise RuntimeError(f'Symlinked dependency is not accepted: {path}')
            if not path.exists():
                if not args.bootstrap:
                    raise RuntimeError(f'Missing dependency {package["name"]}; rerun with --bootstrap')
                path.mkdir()
                runner.run(['git','init'],cwd=path)
                runner.run(['git','remote','add','origin',package['url']],cwd=path)
                runner.run(['git','fetch','--depth=1','origin',package['rev']],cwd=path)
                runner.run(['git','checkout','--detach',package['rev']],cwd=path)
            head = runner.run(['git','rev-parse','HEAD'],cwd=path)
            dirty = runner.run(['git','status','--porcelain','--untracked-files=no'],cwd=path)
            if head != package['rev'] or dirty:
                raise RuntimeError(f'Dependency {package["name"]} has wrong revision or tracked modifications; it was not reset')
        if runner.run(['lake','env','lean','--githash']) != COMPILER:
            raise RuntimeError('Lake selected a different compiler')
        if args.bootstrap:
            runner.run(['lake','exe','cache','get'])
        build = lake_dir/'build'
        if build.is_symlink():
            raise RuntimeError('Refusing to remove symlinked build directory')
        if build.exists():
            shutil.rmtree(build)
        report['clean_project_build_directory'] = str(build)
        runner.run(['lake','build'])
        runner.run(['lake','env','lean','validation/AcceptPhysical.lean'])
        runner.run(['lake','env','lean','validation/AcceptGeneral.lean'])
        runner.run(['lake','env','lean','validation/AcceptModels.lean'])
        runner.run(['lake','env','lean','validation/AcceptAdversarial.lean'])
        runner.run(['lake','env','lean','validation/AcceptSettings.lean'])
        runner.run(['lake','env','lean','validation/RejectUniform.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectNormalization.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectFirstNormalization.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectConjugation.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectAlteredWitness.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectGeneralNormalization.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectGeneralCoefficients.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectGeneralSwap.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectModelValue.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectClosureValue.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectPurificationNorm.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectCycleCharpoly.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectAdversarialUniformBound.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectEveProjectivity.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectEveNormalization.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectClosureSliceOrder.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectSourceQutritSign.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectSettingsUniform.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectSettingsNormalization.lean'],expect_failure=True)
        runner.run(['lake','env','lean','validation/RejectAnchorQubitGap.lean'],expect_failure=True)
        axtext = runner.run(['lake','env','lean','CyclicBell/AxiomAudit.lean'])
        expected = json.loads((ROOT/'reference/expected_theorems.json').read_text())
        report['axioms'] = parse_axioms(axtext, expected)
        runner.run(['lake','env','lean','CyclicBell/Statements.lean'])
        if before != protected_fingerprints():
            raise RuntimeError('Protected sources changed during audit')
        if data != source.read_bytes():
            raise RuntimeError('Manuscript changed during audit')
        for package in lock['packages']:
            path = package_root/package['name']
            if runner.run(['git','rev-parse','HEAD'],cwd=path) != package['rev']:
                raise RuntimeError('Dependency commit changed during audit')
            if runner.run(['git','status','--porcelain','--untracked-files=no'],cwd=path):
                raise RuntimeError('Dependency sources changed during audit')
        report['status'] = 'candidate_kernel_checks_passed_statement_review_required'
        report['kernel_checked'] = True
        report['remaining_scope_gaps'] = ['independent statement and manuscript-correspondence review',
            'general Qqa subset Qqc/closedness theorem not supplied and not required for these values',
            'full canonical source-Z/polar strategy identification not supplied']
        # Kernel acceptance alone does not certify source correspondence or the entire paper.
        report['formal_endpoint_certified'] = False
        exit_code = 0
    except Exception as exc:
        report['status'] = 'blocked_or_failed_NOT_CERTIFIED'
        report['error'] = str(exc)
        (directory/'failure.txt').write_text(traceback.format_exc())
    finally:
        finish = datetime.now(timezone.utc)
        report['finished_utc'] = finish.isoformat()
        report['elapsed_seconds'] = (finish-start).total_seconds()
        text = json.dumps(report,indent=2)+'\n'
        (directory/'run.json').write_text(text)
        (ROOT/'logs'/'latest_run.json').write_text(text)
        print(report['status'])
        print(report.get('error','Candidate checks passed; scope and correspondence still require review.'))
        print(f'Receipt: {directory / "run.json"}')
        print('Whole-paper certification: false; independent manuscript statement-review status: pending')
    return exit_code

if __name__ == '__main__':
    sys.exit(main())
