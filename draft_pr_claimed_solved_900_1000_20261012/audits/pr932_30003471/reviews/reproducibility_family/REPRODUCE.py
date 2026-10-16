#!/usr/bin/env python3
"""Run authenticated frozen diagnostics plus independent controls in own scratch.

Authenticate this program through VERIFY.py and the independent public-map digest
before running it. Requires the documented NumPy/SciPy/SymPy runtime; no downloads.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).absolute().parent
SNAPSHOT_PIN = 'f05112fa43eb99a0c9cd4687b14beeef5eb4d190dcebae9b15c1d84c9acc656f'


def module(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = module('PACKET_GUARD')


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (90, 95))
    resource.setrlimit(resource.RLIMIT_FSIZE, (64_000_000, 64_000_000))
    resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))


def environment(inherited=False):
    result = {key: value for key, value in os.environ.items()
              if not key.startswith('PYTHON') and key not in ('LD_PRELOAD', 'DYLD_INSERT_LIBRARIES', 'DYLD_LIBRARY_PATH')}
    result['PYTHONDONTWRITEBYTECODE'] = '1'
    result['OPENBLAS_NUM_THREADS'] = '1'
    result['OMP_NUM_THREADS'] = '1'
    if inherited:
        result['PYTHONOPTIMIZE'] = '2'
    return result


def execute(command, cwd, inherited=False, timeout=240):
    return subprocess.run(command, cwd=cwd, env=environment(inherited), capture_output=True,
                          timeout=timeout, preexec_fn=limits)


def serialized(value, indent=None):
    return (json.dumps(value, sort_keys=True, indent=indent) + '\n').encode()


def modes():
    return [('normal', ['-I', '-B'], False), ('-O', ['-I', '-B', '-O'], False),
            ('-OO', ['-I', '-B', '-OO'], False), ('inherited_PYTHONOPTIMIZE_2', ['-B'], True)]


def replay(packet, scratch, snapshot, python):
    start = g.authenticate(str(packet), snapshot)
    expected_author = g.strict_json(g.regular(packet/'audit_a/CONTROL_REPLAY.json'))['runs'][0]['result']
    expected_independent = g.strict_json(g.regular(packet/'audit_b/INDEPENDENT_CONTROL_RESULTS.json'))
    need(expected_independent['counts'].pop('source_pin') == 9, 'saved source count')
    expected_independent['total_checks'] -= 9
    expected_independent['source_verification'] = 'NOT_RUN_NO_SEPARATELY_SUPPLIED_SOURCES'
    rows = []
    for label, flags, inherited in modes():
        for suite in ['controls', 'author_self_test', 'portable', 'historical_direct', 'publication', 'mutations']:
            with tempfile.TemporaryDirectory(prefix='replay-', dir=scratch) as temporary:
                work = Path(temporary)
                copy = work/'packet'
                shutil.copytree(packet, copy)
                pre = g.authenticate(str(copy), snapshot)
                script, arguments = {
                    'controls': ('public/controls.py', []),
                    'author_self_test': ('public/verify_packet.py', ['--manifest-sha256', '1cd8291f2025524b351c5cc3cb5780b35ba5fa4c4afde78c6e288daddd350e9f', '--self-test']),
                    'portable': ('PORTABLE_INDEPENDENT.py', ['--packet-root', str(copy)]),
                    'historical_direct': ('audit_b/independent_controls.py', []),
                    'publication': ('VERIFY_PUBLICATION.py', ['--packet', str(copy), '--expected-manifest', g.OUTER_PIN]),
                    'mutations': ('TEST_MUTATIONS.py', ['--packet', str(copy), '--expected-manifest', g.OUTER_PIN, '--expected-wrapper', snapshot['files']['VERIFY_PUBLICATION.py']['sha256']]),
                }[suite]
                # Every copied Python byte (not just the entry point) was checked above.
                cp = execute([python, *flags, str(copy/script), *arguments], work, inherited)
                post = g.authenticate(str(copy), snapshot)
                need(g.typed_equal(pre, post), suite + ' changed input')
                row = {'mode': label, 'suite': suite, 'returncode': cp.returncode,
                       'entrypoint_sha256': g.sha(g.regular(copy/script)), 'all_29_pre_authenticated': True,
                       'unchanged_after': True, 'stdout_bytes': len(cp.stdout), 'stdout_sha256': g.sha(cp.stdout),
                       'stderr_bytes': len(cp.stderr), 'stderr_sha256': g.sha(cp.stderr)}
                if suite == 'historical_direct':
                    need(cp.returncode != 0 and b'FileNotFoundError' in cp.stderr and b'polytope_dihedral_30003471/packet/MANIFEST.json' in cp.stderr,
                         'historical layout failure differed')
                    row['expected_failure'] = 'historical sibling packet/source-PDF layout absent'
                elif suite == 'publication' and cp.returncode != 0:
                    need(cp.returncode == 1 and cp.stdout == b'' and
                         cp.stderr == b'REJECT: Independent replay differs beyond disclosed source selection\n',
                         label+'/publication failed for an unexpected reason: '+cp.stderr.decode(errors='replace'))
                    row['exact_legacy_reproduction'] = False
                    row['expected_failure'] = 'legacy publication gate rejects the observed historical numerical-receipt drift'
                else:
                    need(cp.returncode == 0 and cp.stderr == b'', label+'/'+suite+' failed: '+cp.stderr.decode(errors='replace')[-2000:])
                    obj = g.strict_json(cp.stdout)
                    if suite == 'controls':
                        expected = g.strict_json(g.regular(copy/'public/CONTROL_RESULTS.json'))
                        need(g.typed_equal(obj, expected) and cp.stdout == g.regular(copy/'public/CONTROL_RESULTS.json'), 'saved control stdout mismatch')
                        row.update(total_checks=obj['total'], saved_stdout_byte_identity=True, saved_semantic_exact_types=True)
                    elif suite == 'author_self_test':
                        need(g.typed_equal(obj, expected_author), 'saved author semantic result mismatch')
                        need(cp.stdout == serialized(expected_author), 'author canonical output byte mismatch')
                        row.update(total_checks=5066, negative_controls_rejected=19, saved_semantic_exact_types=True,
                                   saved_result_reserialized_stdout_byte_identity=True,
                                   historical_raw_stdout_stored=False)
                    elif suite == 'portable':
                        differences = {key:{'saved':expected_independent[key], 'actual':obj.get(key)}
                                       for key in expected_independent if not g.typed_equal(obj.get(key), expected_independent[key])}
                        need(obj.keys() == expected_independent.keys(), 'portable schema differs')
                        need(not differences or set(differences) == {'numeric_max_jacobi_error'},
                             'portable differs beyond identified platform-dependent numeric diagnostic')
                        need(type(obj['numeric_max_jacobi_error']) is float and 0 <= obj['numeric_max_jacobi_error'] < 3e-7,
                             'portable numerical diagnostic exceeds its actual original check tolerance')
                        need(cp.stdout == serialized(obj, 2), 'portable output is not the disclosed canonical JSON')
                        row.update(total_checks=obj['total_checks'], skipped_external_source_checks=9,
                                   saved_semantic_exact_types=not differences,
                                   disclosed_transformation_stdout_byte_identity=cp.stdout == serialized(expected_independent, 2),
                                   expected_transformed_stdout_sha256=g.sha(serialized(expected_independent, 2)),
                                   exact_legacy_reproduction=not differences, receipt_differences=differences,
                                   result=obj)
                    elif suite == 'publication':
                        need(obj['bound_files'] == 28 and len(obj['replays']) == 9, 'publication replay count')
                        row['result'] = obj
                    elif suite == 'mutations':
                        need(cp.stdout == g.regular(copy/'MUTATION_RESULTS.json') and
                             g.typed_equal(obj, g.strict_json(g.regular(copy/'MUTATION_RESULTS.json'))), 'saved mutation stdout differs')
                        row.update(cases=obj['cases'], rejections=obj['rejections'], clean_acceptances=obj['clean_acceptances'],
                                   saved_stdout_byte_identity=True, saved_semantic_exact_types=True)
                rows.append(row)
                print('Completed '+label+'/'+suite, file=sys.stderr, flush=True)
    need(g.typed_equal(g.authenticate(str(packet), snapshot), start), 'source packet changed')
    return rows


def current_gate_replays(packet, snapshot, scratch, python):
    rows = []
    for label, flags, inherited in modes():
        before = g.authenticate(str(packet), snapshot)
        cp = execute([python, *flags, str(HERE/'RELEASE_GATE.py'), '--packet', str(packet), '--scratch', str(scratch),
                      '--python', python], scratch, inherited)
        need(cp.returncode == 0 and cp.stderr == b'', 'current gate replay failed: '+cp.stderr.decode(errors='replace'))
        obj = g.strict_json(cp.stdout)
        need(obj['current_gate'] == 'PASS_WITH_DISCLOSED_BOUNDED_NONPROOF_DIAGNOSTIC' and
             obj['legacy_exact_receipt_gate_superseded'] is False and obj['mathematical_acceptance'] is False and
             len(obj['replays']) == 3, 'current gate scope changed')
        need(g.typed_equal(before,g.authenticate(str(packet),snapshot)), 'current gate changed original packet')
        rows.append({'parent_mode':label, 'returncode':0, 'stdout_sha256':g.sha(cp.stdout),
                     'all_29_pre_authenticated':True, 'result':obj})
        print('Completed current gate/'+label,file=sys.stderr,flush=True)
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', required=True)
    p.add_argument('--python', default=sys.executable)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--scratch', required=True, type=Path)
    p.add_argument('--repository', type=Path)
    p.add_argument('--independent-only', action='store_true')
    args = p.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    snapshot = g.load_snapshot(HERE/'PINNED_SNAPSHOT.json', SNAPSHOT_PIN)
    packet = g.canonical_root(args.packet)
    start = g.authenticate(str(packet), snapshot)
    git = g.authenticate_git(args.repository, snapshot) if args.repository else None
    metadata = execute([args.python, '-I', '-B', '-c', 'import json,sys,numpy,scipy,sympy; print(json.dumps({"python":sys.version,"numpy":numpy.__version__,"scipy":scipy.__version__,"sympy":sympy.__version__},sort_keys=True))'], args.scratch)
    need(metadata.returncode == 0, 'scientific runtime unavailable')
    rows = [] if args.independent_only else replay(packet, args.scratch, snapshot, args.python)
    independent = module('INDEPENDENT_CONTROLS').run(packet, snapshot, args.scratch, args.python)
    current = current_gate_replays(packet,snapshot,args.scratch,args.python)
    final = g.authenticate(str(packet), snapshot)
    need(g.typed_equal(start, final), 'final source identity changed')
    exact = None if args.independent_only else all(row.get('exact_legacy_reproduction', True) for row in rows)
    result = {'schema': 'pr932-reproduction-v1', 'status': 'INDEPENDENT_CONTROLS_ONLY' if args.independent_only else 'PASS' if exact else 'EXACT_LEGACY_RECEIPT_MISMATCH',
              'integrity_and_independent_controls_passed': True, 'exact_legacy_receipts_reproduced': exact,
              'snapshot_sha256': SNAPSHOT_PIN,
              'head': g.HEAD, 'uid': os.geteuid(), 'platform': platform.platform(),
              'runtime': g.strict_json(metadata.stdout), 'git': git, 'legacy_runs': rows,
              'independent_controls': independent, 'current_gate_runs':current, 'original_inventory_unchanged': True,
              'analytic_theorem_certified': False, 'external_source_hashes_reproduced': False,
              'limits': 'Serial local byte authentication and finite controls; no concurrent-attacker or OS sandbox guarantee.'}
    args.output.write_bytes(serialized(result, 2))
    print(json.dumps({'status': result['status'], 'legacy_runs': len(rows), 'independent_controls': independent['summary'],
                      'output_sha256': g.sha(args.output.read_bytes())}, sort_keys=True))


if __name__ == '__main__':
    main()
