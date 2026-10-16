#!/usr/bin/env python3
"""Disposable corruption/optimization controls; never edits the frozen packet."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
MODES = {'normal': ([], None), 'O': (['-O'], None), 'OO': (['-OO'], None), 'env_2': ([], '2')}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def fingerprint(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def encode(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def run(python, mode, command, work, timeout=120):
    flags, optimize = MODES[mode]
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    if optimize is not None:
        env['PYTHONOPTIMIZE'] = optimize
    try:
        process = subprocess.run([str(python)] + flags + command, cwd=work, env=env, capture_output=True, text=True, timeout=timeout)
        return {'exit_code': process.returncode, 'timed_out': False,
                'stdout_sha256': hashlib.sha256(process.stdout.encode()).hexdigest(),
                'stderr_sha256': hashlib.sha256(process.stderr.encode()).hexdigest(),
                'stdout_summary': process.stdout[-300:] if process.returncode != 0 else '',
                'stderr_summary': process.stderr[-300:] if process.returncode != 0 else ''}
    except subprocess.TimeoutExpired:
        return {'exit_code': None, 'timed_out': True,
                'timeout_seconds': timeout, 'process_terminated_by_subprocess_timeout': True}


def mutate(work, kind, temporary):
    root = work
    extra_args = []
    sockets = []
    if kind == 'missing_file':
        (work / 'README.md').unlink()
    elif kind == 'extra_file':
        (work / 'UNDECLARED.txt').write_text('test payload\n')
    elif kind == 'extra_source_pdf':
        (work / 'source.pdf').write_bytes(b'%PDF-test-fixture\n')
    elif kind == 'extra_source_csv':
        (work / 'data.csv').write_text('private,test\n')
    elif kind == 'extra_empty_directory':
        (work / 'empty').mkdir()
    elif kind == 'extra_fifo':
        os.mkfifo(work / 'unexpected_pipe')
    elif kind == 'extra_socket':
        sock = socket.socket(socket.AF_UNIX)
        # AF_UNIX paths have a short platform limit; relative bind creates the
        # actual socket entry inside the assigned disposable copy.
        previous = Path.cwd()
        try:
            os.chdir(work)
            sock.bind('unexpected_socket')
        finally:
            os.chdir(previous)
        sockets.append(sock)
    elif kind == 'expected_file_fifo':
        (work / 'README.md').unlink()
        os.mkfifo(work / 'README.md')
    elif kind == 'manifest_fifo':
        (work / 'PACKAGE_MANIFEST.json').unlink()
        os.mkfifo(work / 'PACKAGE_MANIFEST.json')
    elif kind == 'internal_file_symlink':
        target = temporary / (work.name + '_external_README.md')
        shutil.copy2(work / 'README.md', target)
        (work / 'README.md').unlink()
        (work / 'README.md').symlink_to(target)
    elif kind == 'internal_directory_symlink':
        target = temporary / (work.name + '_external_author')
        shutil.copytree(work / 'author', target)
        shutil.rmtree(work / 'author')
        (work / 'author').symlink_to(target, target_is_directory=True)
    elif kind == 'root_symlink':
        root = temporary / (work.name + '_root_alias')
        root.symlink_to(work, target_is_directory=True)
    elif kind == 'wrong_root':
        root = temporary / (work.name + '_wrong_root')
        root.mkdir()
    elif kind == 'proof_semantic_change_and_resign':
        proof = work / 'author/BOUNDED_REGION_PROOF.md'
        original_proof = proof.read_bytes()
        changed_proof = original_proof.replace(b'\\lim_{N\\to\\infty}\\|D_N^{(\\sigma)}\\Xi_N\\|=2', b'\\lim_{N\\to\\infty}\\|D_N^{(\\sigma)}\\Xi_N\\|=1', 1)
        require(changed_proof != original_proof, 'semantic proof fixture did not change the claimed limit')
        proof.write_bytes(changed_proof)
        author_path = work / 'author/AUTHOR_MANIFEST.json'
        author = json.loads(author_path.read_text())
        author['files']['BOUNDED_REGION_PROOF.md'] = fingerprint(proof)
        encode(author_path, author)
        package_path = work / 'PACKAGE_MANIFEST.json'
        package = json.loads(package_path.read_text())
        for name in ('author/BOUNDED_REGION_PROOF.md', 'author/AUTHOR_MANIFEST.json'):
            package['files'][name] = fingerprint(work / name)
        encode(package_path, package)
    elif kind in {'manifest_wrong_problem_type', 'manifest_wrong_revision', 'manifest_extra_key', 'manifest_bad_record_type', 'manifest_unsafe_path', 'manifest_absolute_path'}:
        path = work / 'PACKAGE_MANIFEST.json'
        value = json.loads(path.read_text())
        if kind == 'manifest_wrong_problem_type': value['problem_id'] = True
        elif kind == 'manifest_wrong_revision': value['revision'] = 999
        elif kind == 'manifest_extra_key': value['unauthenticated_metadata'] = 'altered'
        elif kind == 'manifest_bad_record_type': value['files']['README.md']['bytes'] = str(value['files']['README.md']['bytes'])
        elif kind == 'manifest_unsafe_path': value['files']['../README.md'] = value['files'].pop('README.md')
        elif kind == 'manifest_absolute_path': value['files'][str(work / 'README.md')] = value['files'].pop('README.md')
        encode(path, value)
    elif kind == 'manifest_duplicate_key':
        path = work / 'PACKAGE_MANIFEST.json'
        data = path.read_text()
        path.write_text(data.replace('{', '{\n"problem_id": 7,', 1))
    elif kind == 'manifest_malformed_json':
        (work / 'PACKAGE_MANIFEST.json').write_text('{ not JSON }')
    elif kind == 'changed_nested_manifest':
        path = work / 'audit_a/AUDIT_MANIFEST.json'
        data = json.loads(path.read_text()); data['verdict'] = 'REJECT'; encode(path, data)
    elif kind in {'external_head_anchor', 'external_package_anchor', 'external_proof_anchor'}:
        option = {'external_head_anchor': '--expected-head', 'external_package_anchor': '--expected-package', 'external_proof_anchor': '--expected-proof'}[kind]
        extra_args = [option, '0' * (40 if kind == 'external_head_anchor' else 64)]
    else:
        raise ValueError('unknown fixture ' + kind)
    return root, extra_args, sockets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    (HERE / 'tmp').mkdir(exist_ok=True)
    require((HERE / 'tmp').is_dir() and not (HERE / 'tmp').is_symlink(), 'unsafe disposable work directory')
    import verify_frozen_packet
    before = verify_frozen_packet.verify(str(args.packet))
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse((HERE / 'verify_frozen_packet.py').read_text()))), 'new verifier must have no asserts')
    fixtures = ['missing_file', 'extra_file', 'extra_source_pdf', 'extra_source_csv',
                'extra_empty_directory', 'extra_fifo', 'extra_socket', 'expected_file_fifo',
                'manifest_fifo', 'internal_file_symlink', 'internal_directory_symlink', 'root_symlink',
                'wrong_root', 'proof_semantic_change_and_resign', 'manifest_wrong_problem_type',
                'manifest_wrong_revision', 'manifest_extra_key', 'manifest_bad_record_type',
                'manifest_unsafe_path', 'manifest_absolute_path', 'manifest_duplicate_key',
                'manifest_malformed_json', 'changed_nested_manifest', 'external_head_anchor',
                'external_package_anchor', 'external_proof_anchor']
    results, legacy, optimization, positive = [], [], [], []
    with tempfile.TemporaryDirectory(dir=HERE / 'tmp', prefix='hostile_') as temporary:
        temporary = Path(temporary)
        for kind in fixtures:
            work = temporary / kind
            shutil.copytree(args.packet, work)
            root, extra_args, sockets = mutate(work, kind, temporary)
            try:
                for mode in MODES:
                    result = run(args.python, mode, [str(HERE / 'verify_frozen_packet.py'), '--root', str(root)] + extra_args, temporary, timeout=5)
                    require(result['exit_code'] == 1 and not result['timed_out'], 'new verifier failed to safely reject ' + kind + ' in ' + mode)
                    results.append(dict(result, fixture=kind, mode=mode, expected='safe reject'))
                if not kind.startswith('external_') and kind != 'wrong_root':
                    script_path = root / 'verify_package.py'
                    result = run(args.python, 'normal', [str(script_path), '--integrity-only'], temporary, timeout=2)
                    legacy.append(dict(result, fixture=kind, expected='characterization, not presupposed rejection'))
            finally:
                for sock in sockets: sock.close()
        for layout in ('direct', 'standalone', 'full_prefix'):
            base = temporary / ('positive_' + layout)
            if layout == 'direct':
                packet = base
            elif layout == 'standalone':
                packet = base / 'original_packet'
            else:
                packet = base.joinpath(*verify_frozen_packet.PREFIX)
            shutil.copytree(args.packet, packet)
            for mode in MODES:
                result = run(args.python, mode, [str(HERE / 'verify_frozen_packet.py'), '--root', str(base)], temporary, timeout=5)
                require(result['exit_code'] == 0 and not result['timed_out'], 'positive portable layout rejected')
                positive.append(dict(result, layout=layout, mode=mode))

        # Genuine failures in unchanged original code: corrupt proof bytes while
        # retaining manifests. Direct checks should reject; optimized asserts may not.
        for label, command in {'author': ['author/verify.py'],
                               'audit_a': ['audit_a/independent_checks.py', '--proof', 'author/BOUNDED_REGION_PROOF.md'],
                               'audit_b': ['audit_b/independent_checks.py', '--author-dir', 'author']}.items():
            for mode in MODES:
                work = temporary / ('proof_failure_' + label + '_' + mode)
                shutil.copytree(args.packet, work)
                proof = work / 'author/BOUNDED_REGION_PROOF.md'
                proof.write_bytes(proof.read_bytes().replace(b'counterexample', b'counterexamp1e', 1))
                result = run(args.python, mode, command, work, timeout=120)
                optimization.append(dict(result, fixture='unchanged_checker_changed_proof', checker=label, mode=mode,
                                         expected='failure is genuine in normal Python; optimized result characterized'))

        # Mathematical assertion failure separated from corruption: deliberately
        # change a program's expectation, then update its own author manifest.
        for mode in MODES:
            work = temporary / ('author_math_failure_' + mode)
            shutil.copytree(args.packet, work)
            program = work / 'author/verify.py'
            data = program.read_text().replace('assert kinetic == Fraction(5, 3)', 'assert kinetic == Fraction(7, 3)', 1)
            require(data != program.read_text(), 'math failure fixture did not mutate intended predicate')
            program.write_text(data)
            manifest_path = work / 'author/AUTHOR_MANIFEST.json'
            manifest = json.loads(manifest_path.read_text()); manifest['files']['verify.py'] = fingerprint(program); encode(manifest_path, manifest)
            result = run(args.python, mode, ['author/verify.py'], work)
            optimization.append(dict(result, fixture='author_deliberate_false_math_assert', checker='author', mode=mode))
        # audit A's check() is explicit and must still reject a false predicate.
        for mode in MODES:
            work = temporary / ('auditA_math_failure_' + mode)
            shutil.copytree(args.packet, work)
            program = work / 'audit_a/independent_checks.py'
            data = program.read_text().replace("check('three_dimensional_decay',", "check('three_dimensional_decay',False and ", 1)
            require(data != program.read_text(), 'audit A failure fixture did not mutate')
            program.write_text(data)
            result = run(args.python, mode, ['audit_a/independent_checks.py', '--proof', 'author/BOUNDED_REGION_PROOF.md'], work)
            require(result['exit_code'] != 0 and not result['timed_out'], 'audit A explicit false check incorrectly accepted')
            optimization.append(dict(result, fixture='audit_A_deliberate_false_explicit_check', checker='audit_a', mode=mode))
        # audit B all mathematical guards are asserts; force a false exact CAR guard.
        for mode in MODES:
            work = temporary / ('auditB_math_failure_' + mode)
            shutil.copytree(args.packet, work)
            program = work / 'audit_b/independent_checks.py'
            data = program.read_text().replace('assert car_error == 0', 'assert car_error == 1', 1)
            require(data != program.read_text(), 'audit B failure fixture did not mutate')
            program.write_text(data)
            result = run(args.python, mode, ['audit_b/independent_checks.py', '--author-dir', 'author'], work)
            optimization.append(dict(result, fixture='audit_B_deliberate_false_math_assert', checker='audit_b', mode=mode))
    after = verify_frozen_packet.verify(str(args.packet))
    require(before['files'] == after['files'], 'original packet changed')
    output = {'status': 'PASS independent controls; historical weaknesses characterized',
              'utc': datetime.now(timezone.utc).isoformat(),
              'independent_negative_runs': results, 'independent_positive_runs': positive,
              'historical_wrapper_boundary_runs': legacy, 'historical_optimization_runs': optimization,
              'counts': {'independent_negative': len(results), 'independent_positive': len(positive),
                         'legacy_boundary': len(legacy), 'legacy_optimization': len(optimization)},
              'original_26_unchanged': True,
              'warning': 'Disposable mutated programs demonstrate validation behavior, not a mathematical counterexample. The fixed external trust anchor is not a cryptographic signature.'}
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + '\n')
    print(json.dumps(output['counts']))


if __name__ == '__main__':
    main()
