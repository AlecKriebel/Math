#!/usr/bin/env python3
"""Dependency-free PR421 delivery checks. Run this file, not frozen history.

Checks remain active under -O. All program execution and mutations occur in
fresh disposable copies; the delivered packet is read-only input to this driver.
"""
import argparse
import ast
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile


PACKET_PINS = {
    'ATTEMPT_1.md': 'c022afdfe003d0692a032cee48855ddf712de22953b358b895c485215875d8a6',
    'INITIAL_WIP_FREEZE.json': '6ffab2644b59aa1767780860039b87150ce6213ac2283255ea8e54b09ceb015f',
    'RESEARCH_LOG.md': '885ebc99c4123ea229e757047d532f92640d6d481838e450629405f1747a1b90',
    'SOURCE_GATE.md': '69e562b8d0b428fbce36a49cdca51a2e921b67258bd4b3887b285d03f7903b72',
    'VERIFICATION_ADDENDUM.md': '51983adea5a4dff15f951ddfdb517a1710d36b50bfbba93158fafb3dd5c5ca06',
    'audit/AUDIT.md': '154858d740a27eaadff20a72b25cefb56bfeb1c458d9aab18dca1c67f67cba3f',
    'audit/AUDIT_RESULT.json': '79bbdd08b29cd631a0e5c0728e384834a2742b5862d8b50fd76fcefebb518651',
    'audit/independent_algebra.py': '3fda0f889aa454390c6f30c54c842a0a49a5f5a3d1bdea0bce5819711e3dbc96',
    'audit/independent_algebra_results.json': 'ebba35993d64973e0d4fc432052314e82eaa72088d1c70dbd65ac7387c15c4bf',
    'audit/independent_audit.py': '281ebf97900d047447a2a3865f233cfba1c41df6dd6c4e8aaae66150250b1903',
    'audit/independent_results.json': '438d623b96bc48e927753bb1c2a7e4d390d3eb5207d5d0ae785b44c5860817cf',
    'checks.json': '23d6f2d3ee4126b1b712a636ed8bc3b19f4298806962ecdb8acb0a5ddf6f675e',
    'verify.py': 'e3357a9af58d68c2f450d2901ab71c58ed955112017fe0ec758d1adc3b36ca42',
}
PROGRAMS = ('verify.py', 'audit/independent_audit.py', 'audit/independent_algebra.py')
OUTPUTS = ('checks.json', 'audit/independent_results.json',
           'audit/independent_algebra_results.json')
GEOMETRY_SUMMARY_KEYS = ('status', 'frozen_proof_hash_matches', 'Z_link_f_vector',
                         'Z_all_cliques_by_size', 'negative_controls', 'cell_f_vector')
MANIFEST_EXCLUDES = {'MANIFEST.json', 'PUBLIC_OUTPUT_WHITELIST.json'}


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + str(key))
        result[key] = value
    return result


def bad_constant(value):
    raise VerificationError('Nonfinite JSON constant: ' + value)


def parse(data):
    return json.loads(data, object_pairs_hook=unique_object, parse_constant=bad_constant)


def load(path):
    return parse(path.read_text(encoding='utf-8'))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('utf-8')


def records(document):
    require(document.get('schema_version') == 1, 'Unknown manifest schema')
    rows = document.get('files')
    require(isinstance(rows, list), 'Missing manifest file records')
    answer = {}
    for row in rows:
        require(isinstance(row, dict), 'Invalid file record')
        name = row.get('path')
        require(isinstance(name, str), 'Non-string manifest path')
        p = pathlib.PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts and str(p) == name,
                'Unsafe or noncanonical manifest path: ' + name)
        require(name not in answer, 'Duplicate manifest path: ' + name)
        require(isinstance(row.get('bytes'), int) and row['bytes'] >= 0,
                'Invalid byte count: ' + name)
        digest = row.get('sha256', '')
        require(isinstance(digest, str) and len(digest) == 64 and
                all(c in '0123456789abcdef' for c in digest),
                'Invalid SHA-256: ' + name)
        answer[name] = {'path': name, 'bytes': row['bytes'], 'sha256': digest}
    return answer


def check_integrity(root):
    require(not root.is_symlink(), 'Bundle root is a symlink')
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink excluded: ' + str(path.relative_to(root)))
        require(path.is_file() or path.is_dir(), 'Nonordinary filesystem entry')
    manifest = records(load(root / 'MANIFEST.json'))
    whitelist = records(load(root / 'PUBLIC_OUTPUT_WHITELIST.json'))
    require(not (set(manifest) & MANIFEST_EXCLUDES), 'Manifest self/cycle hash')
    require(set(whitelist) == set(manifest) | {'MANIFEST.json'},
            'Whitelist/manifest inventory mismatch')
    require(all(whitelist[name] == row for name, row in manifest.items()),
            'Whitelist/manifest record mismatch')
    expected = set(manifest) | MANIFEST_EXCLUDES
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    require(actual == expected, 'Unlisted/missing bundle files: ' +
            repr(sorted(actual ^ expected)))
    dirs = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_dir()}
    expected_dirs = {str(p) for name in expected for p in pathlib.PurePosixPath(name).parents
                     if str(p) != '.'}
    require(dirs == expected_dirs, 'Unlisted/missing bundle directories')
    for name, row in whitelist.items():
        data = (root / name).read_bytes()
        require(sha(data) == row['sha256'], 'SHA-256 mismatch: ' + name)
        require(len(data) == row['bytes'], 'Byte count mismatch: ' + name)
    packet_files = {str(p.relative_to(root / 'packet'))
                    for p in (root / 'packet').rglob('*') if p.is_file()}
    require(packet_files == set(PACKET_PINS), 'Packet is not exact13-file layout')
    for name, digest in PACKET_PINS.items():
        require(sha((root / 'packet' / name).read_bytes()) == digest,
                'Accepted packet SHA-256 mismatch: ' + name)
    for name in PROGRAMS:
        tree = ast.parse((root / 'packet' / name).read_text(encoding='utf-8'))
        require(not any(isinstance(n, ast.Assert) for n in ast.walk(tree)),
                'Optimization-sensitive assert in accepted script: ' + name)
    return {'file_count': len(actual), 'exact_packet_files': 13,
            'manifest_sha256': sha((root / 'MANIFEST.json').read_bytes()),
            'whitelist_sha256': sha((root / 'PUBLIC_OUTPUT_WHITELIST.json').read_bytes()),
            'all_pins_match': True, 'peer_scripts_included': False}


def fresh_fixture(root, target):
    shutil.copytree(root / 'packet', target)
    for name in OUTPUTS:
        (target / name).unlink()
    require(all(not (target / name).exists() for name in OUTPUTS),
            'Saved result survived fixture cleanup')
    return target


def launch(python, fixture, program, optimized, cwd):
    argv = [python, '-I', '-S', '-B'] + (['-O'] if optimized else [])
    argv.append(str(fixture / program))
    result = subprocess.run(argv, cwd=str(cwd), capture_output=True,
                            text=True, encoding='utf-8', timeout=90)
    return result


def baseline(root, work, python):
    checks = load(root / 'packet' / OUTPUTS[0])
    geometry = load(root / 'packet' / OUTPUTS[1])
    algebra = load(root / 'packet' / OUTPUTS[2])
    require(checks['Z_cells_by_dimension'] == [1, 7, 8, 2] and
            checks['Z_link'] == {'edges': 32, 'flag': True, 'four_vertex_cliques': 0,
                                'triangles': 16, 'vertices': 14}, 'Unexpected target data')
    require(geometry['cell_f_vector'] == [1, 7, 8, 2] and
            geometry['Z_link_f_vector'] == [14, 32, 16] and
            geometry['negative_controls'] == 17, 'Unexpected geometry baseline')
    require(algebra['phi'] == {'a': 'a', 'b': 'ab', 'c': 'bcb'} and
            len(algebra['nine_target_relation_checks']) == 9 and
            all(value == ['', 0] for value in algebra['nine_target_relation_checks'].values()),
            'Unexpected exact-group baseline')
    expected = {PROGRAMS[0]: checks,
                PROGRAMS[1]: {key: geometry[key] for key in GEOMETRY_SUMMARY_KEYS},
                PROGRAMS[2]: algebra}
    rows = []
    for optimized in (False, True):
        for index, program in enumerate(PROGRAMS):
            label = ('optimized' if optimized else 'normal') + ' ' + str(index)
            fixture = fresh_fixture(root, work / ('packet with spaces ' + label))
            result = launch(python, fixture, program, optimized, work)
            require(result.returncode == 0 and result.stderr == '',
                    label + ' failed: ' + result.stderr)
            observed = parse(result.stdout)
            require(canonical(observed) == canonical(expected[program]),
                    'Fresh stdout differs: ' + program)
            if program == PROGRAMS[0]:
                require(all(not (fixture / name).exists() for name in OUTPUTS),
                        'Author program unexpectedly wrote output files')
                artifact = None
            else:
                out_name = OUTPUTS[1 if program == PROGRAMS[1] else 2]
                generated = fixture / out_name
                require(generated.is_file(), 'Fresh full result not generated')
                full = load(generated)
                require(canonical(full) == canonical(geometry if program == PROGRAMS[1]
                                                    else algebra), 'Fresh full result differs')
                require(generated.read_bytes() == (root / 'packet' / out_name).read_bytes(),
                        'Fresh result bytes differ')
                require(all(not (fixture / name).exists() for name in OUTPUTS
                            if name != out_name), 'Unexpected extra generated result')
                artifact = {'path': out_name, 'sha256': sha(generated.read_bytes()),
                            'canonical_sha256': sha(canonical(full))}
            require(sha((fixture / 'ATTEMPT_1.md').read_bytes()) == PACKET_PINS['ATTEMPT_1.md'],
                    'Execution modified proof bytes')
            rows.append({'program': program, 'mode': '-O' if optimized else 'normal',
                         'exit_code': result.returncode, 'stderr_empty': True,
                         'stdout_canonical_sha256': sha(canonical(observed)),
                         'fresh_full_artifact': artifact,
                         'saved_outputs_deleted_before_run': True,
                         'fixture_path_contains_spaces': True, 'cwd_outside_packet': True})
    for i in range(3):
        require(rows[i]['stdout_canonical_sha256'] == rows[i + 3]['stdout_canonical_sha256'],
                'Normal/-O canonical output mismatch')
    return rows


def replace_exact(path, old, new):
    text = path.read_text(encoding='utf-8')
    require(text.count(old) == 1, 'Mutation target not unique: ' + old)
    path.write_text(text.replace(old, new), encoding='utf-8')


def controls(root, work, python):
    integrity_rows = []
    for name in ('packet/ATTEMPT_1.md', 'packet/verify.py', 'packet/checks.json'):
        target = work / ('tamper ' + str(len(integrity_rows)))
        shutil.copytree(root, target)
        path = target / name
        path.write_bytes(path.read_bytes() + b'\n')
        try:
            check_integrity(target)
        except VerificationError as exc:
            require('SHA-256 mismatch' in str(exc), 'Tamper rejected for incidental reason')
            integrity_rows.append({'changed_path': name, 'rejected': True,
                                   'diagnostic': str(exc)})
        else:
            raise VerificationError('SHA tampering accepted: ' + name)
    mutations = (
        ('duplicate base square', PROGRAMS[0],
         'K_FACES = [(1, 2, -1, -2), (3, 1, -3, -2)]',
         'K_FACES = [(1, 2, -1, -2), (1, 2, -1, -2)]'),
        ('nonclosed Q square', PROGRAMS[0],
         'Q_FACES = [(1, 2, -3, -4), (5, 1, -6, -2)]',
         'Q_FACES = [(1, 2, 3, -4), (5, 1, -6, -2)]'),
        ('wrong cubical involution b sign', PROGRAMS[1],
         "return {'x': ('y', s), 'y': ('x', s), 'b': ('b', -s)}[e]",
         "return {'x': ('y', s), 'y': ('x', s), 'b': ('b', s)}[e]"),
        ('omitted actual cube corner triangle', PROGRAMS[1],
         'ztri = set(tri_counts)',
         'ztri = set(tri_counts)\nztri.remove(sorted(ztri, key=lambda t: tuple(sorted(t)))[0])'),
        ('wrong cube side vertical sign', PROGRAMS[1],
         'side = [l, vertical(v), inv(lamb(l)), vertical(u, -1)]',
         'side = [l, vertical(v), inv(lamb(l)), vertical(u, 1)]'),
        ('wrong inverse monodromy', PROGRAMS[2],
         "psi = {'a': 'a', 'b': 'Ab', 'c': 'BacBa'}",
         "psi = {'a': 'a', 'b': 'Ab', 'c': 'BacB'}"),
        ('changed proof pin', PROGRAMS[1], None, None),
    )
    math_rows = []
    for index, (description, program, old, new) in enumerate(mutations):
        for optimized in (False, True):
            fixture = fresh_fixture(root, work / ('bad input ' + str(index) +
                                                  (' O' if optimized else ' normal')))
            if old is None:
                p = fixture / 'ATTEMPT_1.md'
                p.write_bytes(p.read_bytes() + b'\nprivate falsification control\n')
            else:
                replace_exact(fixture / program, old, new)
            result = launch(python, fixture, program, optimized, work)
            require(result.returncode != 0 and result.stdout == '',
                    'Corrupted data produced successful output: ' + description)
            last = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else ''
            require(last == 'AssertionError' or last.startswith('AssertionError: '),
                    'Corruption failed for incidental reason: ' + result.stderr)
            require(all(not (fixture / name).exists() for name in OUTPUTS),
                    'Corruption wrote successful result')
            math_rows.append({'control': description, 'program': program,
                              'mode': '-O' if optimized else 'normal',
                              'exit_code': result.returncode, 'exception_tail': last,
                              'stdout_empty': True, 'result_files_absent': True,
                              'input_sha256': sha((fixture / program).read_bytes())})
    return {'sha_tampering': integrity_rows, 'mathematical_data': math_rows}


def relocation(root, work, python):
    relocated = work / 'relocated complete bundle with spaces'
    shutil.copytree(root, relocated)
    result = subprocess.run([python, '-I', '-S', '-B', '-O',
                             str(relocated / 'verify_bundle.py'), '--baseline-only',
                             '--python', python], cwd=str(work), capture_output=True,
                            text=True, encoding='utf-8', timeout=90)
    require(result.returncode == 0 and result.stderr == '',
            'Relocated optimized driver failed: ' + result.stderr)
    report = parse(result.stdout)
    require(report['status'] == 'PASS' and len(report['baseline_runs']) == 6,
            'Relocated driver did not execute all baseline checks')
    require(report['integrity']['manifest_sha256'] == sha((root / 'MANIFEST.json').read_bytes()),
            'Relocated manifest differs')
    return {'complete_bundle_path_contains_spaces': True,
            'driver_mode': '-O', 'cwd_outside_bundle': True,
            'clean_normal_and_O_program_runs': 6, 'exit_code': result.returncode,
            'stdout_canonical_sha256': sha(canonical(report))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python', default=sys.executable,
                        help='Python 3 interpreter for clean direct subprocesses')
    parser.add_argument('--baseline-only', action='store_true',
                        help='Run integrity and six clean baselines; skip controls/relocation')
    args = parser.parse_args()
    require(sys.version_info >= (3, 9), 'Python 3.9 or later is required')
    root = pathlib.Path(__file__).resolve().parent
    python = shutil.which(args.python) if not pathlib.Path(args.python).is_absolute() else args.python
    require(python is not None and pathlib.Path(python).is_file(), 'Python executable unavailable')
    integrity = check_integrity(root)
    with tempfile.TemporaryDirectory(prefix='PR421 verification with spaces ') as name:
        work = pathlib.Path(name)
        rows = baseline(root, work, python)
        negatives = None if args.baseline_only else controls(root, work, python)
        moved = None if args.baseline_only else relocation(root, work, python)
    require(check_integrity(root) == integrity, 'Input bundle changed during verification')
    report = {'status': 'PASS', 'pr': 421, 'problem_id': '20001515',
              'source_head': 'd5bf8b5a25cabb177433338fae60af52ebfecf1c',
              'driver_python_version': sys.version.split()[0],
              'driver_optimized': sys.flags.optimize > 0,
              'subprocess_python': python, 'subprocess_flags': ['-I', '-S', '-B'],
              'integrity': integrity, 'baseline_runs': rows,
              'negative_controls': negatives, 'relocated_bundle': moved,
              'scope': 'Finite certificate reproduction and input integrity only. Written proof is primary; no formal/global proof, external source or priority guarantee.'}
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    try:
        main()
    except (VerificationError, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        print('VERIFICATION FAILED: ' + str(error), file=sys.stderr)
        sys.exit(1)
