#!/usr/bin/env python3
"""Authenticate frozen finite-subgroup realization partial results; replay source-free finite checks."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile

ACCEPTED = {'original/ATTEMPT_LEDGER.json': {'bytes': 2384, 'sha256': 'd2b2faf5f8625a360cfc36478bda90b2444a34350ed78adb9de3aa16e8cdb5af'}, 'original/EXACT_CHECKS.json': {'bytes': 1415, 'sha256': '02b9d16335a3a70d4316b7cc04a0f868aac910ebb8587759d967513743436c7b'}, 'original/MANIFEST.sha256.json': {'bytes': 1271, 'sha256': '3308459e594672876a4953fac77a08719bb4cd52f13e3992a54600fff5904a5b'}, 'original/README.md': {'bytes': 1310, 'sha256': '8b453620e157fec6005f29c72afec90b4bec6b6e48886a8fa90ae6963df431e6'}, 'original/REPORT.md': {'bytes': 31687, 'sha256': '209da640c766e9fc6c0b6dababa77569b2d8799a4202ad7377c0beae6ae0087c'}, 'original/SOURCE_METADATA.json': {'bytes': 5404, 'sha256': '7ec536a64db74e011b0f60f1621a809b7b0f1bff2c9e44122876793bbc36ad87'}, 'original/exact_checks.py': {'bytes': 5629, 'sha256': '0a3984b5310b4705e6fac71f426f527e0d05adc71e3c3008eb3677127dfeb390'}, 'audit/AUDIT.md': {'bytes': 18283, 'sha256': 'b642635174b10f8f8bf4a028e91762951e21bd45ff9f7cc425173f662a687a98'}, 'audit/INDEPENDENT_CHECKS.json': {'bytes': 1572, 'sha256': '851448d96edc9ec9ce14d5c4ee698a6dc93468a8484011d2a748f58e9f27a8bc'}, 'audit/INPUT_AND_SOURCE_PINS.json': {'bytes': 5926, 'sha256': '9624729c1c8ccf14033ac75d1267ae19eb811c603f4a3a80f085bac52ac75ff1'}, 'audit/MANIFEST.sha256.json': {'bytes': 1859, 'sha256': 'f8d0e3cc0aa8af5f403146a75f5d551fd655b598cd9e74b79341563019cb75e2'}, 'audit/README.md': {'bytes': 2572, 'sha256': '6811c237a8f0441e68dd720abcdfae53f70bbaba5752b0866962577ed40d4dd7'}, 'audit/REPRODUCTION.json': {'bytes': 15970, 'sha256': '24812803b600d2630982e66767ae4001dd79b72bb74be8d99c892d74d77e97b5'}, 'audit/exact_checks_hardened.py': {'bytes': 6787, 'sha256': 'ce602ada6ca79fcb2059e98055b4befa4e0bd108a78d3d7bccf22dd26224c6c3'}, 'audit/exact_checks_hardening.patch': {'bytes': 6243, 'sha256': '694b17455f4255c4ba8722407809354d2f9017e4de1c3b89dab016d291151ce0'}, 'audit/independent_checks.py': {'bytes': 7643, 'sha256': '83a1ca63bedbef8c4110388efe7cf26e64f2cdde3f186ce96288f62c2b7483fd'}, 'audit/reproduce_checks.py': {'bytes': 6158, 'sha256': 'b0362ca7b08b778c866c3947c32f6d84a79a08fd98096ba344dc4c753d7c6ac1'}, 'corrected/EXACT_CHECKS.json': {'bytes': 1415, 'sha256': '02b9d16335a3a70d4316b7cc04a0f868aac910ebb8587759d967513743436c7b'}, 'corrected/MANIFEST.sha256.json': {'bytes': 704, 'sha256': 'ac9c427603225e55ff28e27481f90fd626fc5c482301a630d75a2329752ba543'}, 'corrected/PATCH_APPLICATION.json': {'bytes': 653, 'sha256': 'e4aa678bd593cb00f4abc3b2a95e3733d8ab4e08f6c27a818d225e4567551be7'}, 'corrected/README.md': {'bytes': 746, 'sha256': '36c7d28e15cfc78cab029a73a653ee48b526d41a479385df7b4c8cd6fbb035ed'}, 'corrected/exact_checks.py': {'bytes': 6787, 'sha256': 'ce602ada6ca79fcb2059e98055b4befa4e0bd108a78d3d7bccf22dd26224c6c3'}}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'original', 'audit', 'corrected'}
ORIGINAL_PIN = '3308459e594672876a4953fac77a08719bb4cd52f13e3992a54600fff5904a5b'
AUDIT_PIN = 'f8d0e3cc0aa8af5f403146a75f5d551fd655b598cd9e74b79341563019cb75e2'
CORRECTED_PIN = 'ac9c427603225e55ff28e27481f90fd626fc5c482301a630d75a2329752ba543'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(b) is dict:
        return set(a) == set(b) and all(same(a[k], v) for k, v in b.items())
    if type(b) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def nonfinite(value):
    raise ValueError('nonfinite JSON number')


def finite(value):
    result = float(value)
    need(math.isfinite(result), 'overflowed JSON number')
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite, parse_float=finite)


def keys(obj, names):
    need(type(obj) is dict and set(obj) == set(names), 'exact object schema')


def exact_int(value, expected=None):
    need(type(value) is int and value >= 0 and (expected is None or value == expected), 'exact nonnegative integer')


def digest(value):
    need(type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None, 'lowercase SHA-256')


def inventory(root):
    for path in (root, *root.parents):
        need(stat.S_ISDIR(path.lstat().st_mode), 'linked/non-directory root or ancestor')
    files, dirs = set(), set()
    def visit(directory):
        for entry in os.scandir(directory):
            path = Path(entry.path)
            name = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                need(name in DIRS, 'extra directory')
                dirs.add(name)
                visit(path)
            else:
                need(stat.S_ISREG(mode), 'symlink or special member')
                files.add(name)
    visit(root)
    need(files == FILES and dirs == DIRS, 'exact recursive inventory')


def ordinary(path):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_size <= 1000000, 'regular bounded member')
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        need((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino), 'member replaced at open')
        raw = stream.read(1000001)
    need(len(raw) == before.st_size, 'member size changed')
    return raw


def manifest(value, snapshot, payload, role=None):
    keys(value, ['schema', 'problem_id', 'files'] + (['role'] if role is not None else []))
    if role is not None:
        need(same(value['role'], role), 'manifest role')
    exact_int(value['schema'], 1)
    exact_int(value['problem_id'], 2960)
    rows = value['files']
    need(type(rows) is list and len(rows) == len(payload), 'manifest list length/type')
    seen = set()
    for row in rows:
        keys(row, ['path', 'bytes', 'sha256'])
        name = row['path']
        need(type(name) is str and name in payload and name not in seen, 'unknown/duplicate manifest path')
        seen.add(name)
        exact_int(row['bytes']); digest(row['sha256'])
        need(same(row, dict(path=name, bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'manifest byte binding')
    need(seen == payload, 'manifest inventory')


def integrity(root, manifest_pin, bootstrap_pin):
    digest(manifest_pin); digest(bootstrap_pin)
    inventory(root)
    snapshot = {name: ordinary(root/name) for name in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json']) == manifest_pin, 'external manifest pin')
    need(sha(snapshot['BOOTSTRAP.py']) == bootstrap_pin, 'external bootstrap pin')
    parsed = {name: parse(raw) for name, raw in snapshot.items() if name.endswith('.json')}
    manifest(parsed['PUBLICATION_MANIFEST.json'], snapshot, PAYLOAD)
    for name, row in ACCEPTED.items():
        need(same(row, dict(bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'accepted evidence bytes changed')
    for prefix, pin in [('original/', ORIGINAL_PIN), ('audit/', AUDIT_PIN), ('corrected/', CORRECTED_PIN)]:
        name = prefix + 'MANIFEST.sha256.json'
        need(sha(snapshot[name]) == pin, 'externally frozen slice manifest')
        value = parsed[name]
        names = {n[len(prefix):] for n in ACCEPTED if n.startswith(prefix)} - {'MANIFEST.sha256.json'}
        rows = value['files']
        need(type(rows) is list and len(rows) == len(names), 'slice exact row count')
        seen = set()
        for row in rows:
            keys(row, ['path', 'bytes', 'sha256'])
            n = row['path']; need(type(n) is str and n in names and n not in seen, 'slice exact path')
            seen.add(n); exact_int(row['bytes']); digest(row['sha256'])
            need(same(row, dict(path=n, bytes=len(snapshot[prefix+n]), sha256=sha(snapshot[prefix+n]))), 'slice row binding')
        need(seen == names, 'slice inventory')
    original = parsed['original/MANIFEST.sha256.json']
    need(original['problem_number'] == 'KP-4.84' and original['classification'] == 'partial_unresolved', 'original scope')
    exact_int(original['schema_version'], 1); exact_int(original['problem_id'], 2960); exact_int(original['approaches'], 5)
    need(original['full_resolution_claimed'] is False, 'unresolved target')
    audit = parsed['audit/MANIFEST.sha256.json']
    need(audit['mathematical_verdict'] == 'accepted' and audit['checker_verdict'] == 'separate_hardening_required_and_verified', 'audit disposition')
    exact_int(audit['mathematical_approaches'], 5); exact_int(audit['audit_attempt_increment'], 0)
    need(audit['original_manifest_sha256'] == ORIGINAL_PIN, 'audit original binding')
    need(snapshot['corrected/exact_checks.py'] == snapshot['audit/exact_checks_hardened.py'], 'corrected audited code')
    need(snapshot['corrected/EXACT_CHECKS.json'] == snapshot['original/EXACT_CHECKS.json'], 'unchanged exact output')
    pins = parsed['audit/INPUT_AND_SOURCE_PINS.json']
    need(pins['classification'] == 'partial_unresolved' and pins['mathematical_correction_required'] is False, 'unchanged mathematical disposition')
    need(pins['original_checker_requires_hardening'] is True and pins['original_files_preserved'] is True, 'historical defects retained')
    exact_int(pins['approaches_completed'], 5); exact_int(pins['audit_attempt_increment'], 0)
    inventory(root)
    return snapshot, parsed


def normalized_native(value):
    import copy
    value = copy.deepcopy(value)
    need(type(value['python']) is str and re.fullmatch(r'3\.[0-9]+\.[0-9]+', value['python']) is not None, 'Python version schema')
    value['python'] = '<runtime-version>'
    return value


def replay(snapshot, parsed):
    import ast
    need(hasattr(os, 'geteuid') and os.getuid() == os.geteuid() == 1000, 'actual UID/EUID 1000 required')
    need(sum(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(snapshot['original/exact_checks.py']))) == 17, 'original 17 asserts')
    for name in ['corrected/exact_checks.py', 'audit/independent_checks.py', 'audit/reproduce_checks.py']:
        need(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(snapshot[name]))), 'optimization-safe executable')
    with tempfile.TemporaryDirectory(prefix='finite-realization-publication-') as directory:
        work = Path(directory)
        for name in ['original', 'audit', 'corrected', 'cwd']: (work/name).mkdir()
        for name in ACCEPTED: (work/name).write_bytes(snapshot[name])
        for name in ACCEPTED: (work/name).chmod(0o444)
        readonly = [work/name for name in ['original', 'audit', 'corrected', 'cwd']]
        for directory in readonly: directory.chmod(0o555)
        denied = []
        env = dict(PATH=os.defpath, HOME=str(work), TMPDIR=str(work), LC_ALL='C', PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1', PYTHONSAFEPATH='1')
        flags = [] if sys.flags.optimize == 0 else ['-' + 'O'*sys.flags.optimize]
        def execute(script, args=(), cwd=None):
            return subprocess.run([sys.executable, '-I', '-S', '-B', *flags, str(script), *args], cwd=cwd or work/'cwd', env=env, capture_output=True, timeout=300)
        def successful(script, expected, args=()):
            result = execute(script, args)
            need(result.returncode == 0 and result.stderr == b'', 'fresh executable failed')
            need(result.stdout == expected, 'complete exact stdout mismatch')
            need(same(parse(result.stdout), parse(expected)), 'exact typed result mismatch')
            return result
        try:
            for name in ['original/NEW_FILE', 'original/exact_checks.py', 'audit/NEW_FILE', 'audit/reproduce_checks.py', 'corrected/NEW_FILE', 'corrected/exact_checks.py', 'cwd/NEW_FILE']:
                try:
                    with (work/name).open('ab') as stream: stream.write(b'forbidden')
                except PermissionError: denied.append(name)
                else: raise ValueError('read-only write unexpectedly succeeded')
            # Reapply the actual pinned patch in an isolated writable scratch directory.
            patched = work/'patch_application'; patched.mkdir()
            (patched/'exact_checks.py').write_bytes(snapshot['original/exact_checks.py'])
            patch = subprocess.run(['/usr/bin/patch', '--batch', '--fuzz=0', '-p1', '-i', str(work/'audit/exact_checks_hardening.patch')], cwd=patched, env=env, capture_output=True, timeout=30)
            need(patch.returncode == 0 and patch.stdout == b'patching file exact_checks.py\n' and patch.stderr == b'', 'exact patch application')
            need({x.name for x in patched.iterdir()} == {'exact_checks.py'}, 'patch extra output')
            need((patched/'exact_checks.py').read_bytes() == snapshot['corrected/exact_checks.py'], 'actual patch output differs')
            corrected = successful(work/'corrected/exact_checks.py', snapshot['corrected/EXACT_CHECKS.json'])
            independent = successful(work/'audit/independent_checks.py', snapshot['audit/INDEPENDENT_CHECKS.json'])
            external = work/'external_output.json'
            successful(work/'corrected/exact_checks.py', snapshot['corrected/EXACT_CHECKS.json'], ['--output', str(external)])
            need(external.read_bytes() == snapshot['corrected/EXACT_CHECKS.json'], 'explicit external output bytes')
            original_failure = execute(work/'original/exact_checks.py')
            need(original_failure.returncode == 1 and original_failure.stdout == b'' and b'PermissionError: ' in original_failure.stderr, 'original read-only failure must remain disclosed')
            # The original frozen harness recreates 36 runs, including all modes.
            native = execute(work/'audit/reproduce_checks.py', [str(work/'original'), str(work/'native_runs')])
            need(native.returncode == 0 and native.stderr == b'', 'native historical harness failed')
            native_value = parse(native.stdout)
            need(native_value['python'] == sys.version.split()[0], 'native actual Python version')
            need(same(normalized_native(native_value), normalized_native(parsed['audit/REPRODUCTION.json'])), 'complete native receipt mismatch')
            need(sum(row['kind'] == 'original' and row['mutation'] not in ['pristine','readonly'] and row['optimization'] != 'normal' and row['emitted_PASS'] is True for row in native_value['runs']) == 8, 'eight optimized false passes reproduced')
            # Fresh independent runtime controls are frozen read-only before execution.
            mutations = [
                ('wrong_torus_generator','corrected/exact_checks.py','(0,0,1,-1)); powers=','(0,0,1,0)); powers=', 'AssertionError: exact check at original line 18'),
                ('remove_countermodel_twist','corrected/exact_checks.py','(z+w+e*m)%2','(z+w)%2','AssertionError: exact check at original line 42'),
                ('wrong_wreath_conjugator','corrected/exact_checks.py','c=wi[(e,a,0)]','c=wi[(a,e,0)]','AssertionError: exact check at original line 81'),
                ('orientation_reversing_coset','corrected/exact_checks.py','if sum(v)%2==0','if sum(v)%2==1','AssertionError: exact check at original line 90'),
                ('wrong_gram_determinant','corrected/exact_checks.py','det(Q)==2000','det(Q)==2001','AssertionError: displayed Gram matrix and determinant'),
                ('wrong_subgroup_count','corrected/exact_checks.py','len(seen)==112','len(seen)==111','AssertionError: complete subgroup enumeration counts'),
                ('independent_wrong_conjugator','audit/independent_checks.py','c = tuple(range(3)) + tuple(3 + a[i] for i in range(3))','c = a + tuple(range(3, 6))','RuntimeError: Wreath conjugator'),
                ('independent_wrong_count','audit/independent_checks.py','len(all_groups) == 112','len(all_groups) == 111','RuntimeError: Subgroup counts'),
            ]
            mutation_results = []
            for label, name, before, after, expected_error in mutations:
                source = snapshot[name].decode(); need(source.count(before) == 1, 'unique mutation anchor')
                folder = work/label; folder.mkdir(); script = folder/'check.py'; script.write_text(source.replace(before, after)); script.chmod(0o444); folder.chmod(0o555)
                readonly.append(folder)
                try:
                    with script.open('ab') as stream: stream.write(b'forbidden')
                except PermissionError: pass
                else: raise ValueError('mutation read-only proof failed')
                result = execute(script)
                error = result.stderr.decode().strip().splitlines()[-1:]
                need(result.returncode == 1 and result.stdout == b'' and error == [expected_error], 'semantic mutation not rejected at intended guard: '+label)
                mutation_results.append(dict(case=label, returncode=1, stdout_bytes=0, stderr_final_line=expected_error, file_mode='0444', directory_mode='0555', denied_write=True))
            need(not list((work/'cwd').iterdir()), 'read-only cwd changed')
            for name in ACCEPTED: need((work/name).read_bytes() == snapshot[name], 'accepted evidence changed')
            result = dict(corrected_output_sha256=sha(corrected.stdout), independent_output_sha256=sha(independent.stdout),
                          complete_corrected_result=parse(corrected.stdout), complete_independent_result=parse(independent.stdout),
                          patch_application='REAPPLIED_ZERO_FUZZ_MATCHES_AUDITED_AND_CORRECTED_BYTES',
                          readonly_write_probes_denied=denied, semantic_mutation_results=mutation_results,
                          native_harness_runs=36, native_harness_modes=['normal','-O','-OO'], native_optimized_original_false_passes=8,
                          original_readonly_failure='REPRODUCED_PERMISSION_ERROR', original_assertions=17, corrected_assertions=0,
                          explicit_external_output='BYTE_IDENTICAL', original_files_preserved=7, audit_files_preserved=10,
                          corrected_slice_files=5, python_version=sys.version.split()[0],
                          fresh_source_bindings='NOT_RUN', fresh_corpus_bindings='NOT_RUN',
                          historical_source_bindings='SEVEN_PDF_PINS_MATCHED_IN_FROZEN_AUDIT',
                          historical_corpus_bindings='TWO_PUBLIC_DATASET_PINS_AND_UNIQUE_RECORD_MATCHED_IN_FROZEN_AUDIT',
                          Illman_full_text='NOT_INSPECTED', imported_theorems='EXTERNAL_INPUTS_NOT_MACHINE_CERTIFIED',
                          mathematical_report='ACCEPTED_UNCHANGED', standard_product_and_swap_subgroup='REALIZATION_PROVED',
                          full_smooth_mapping_class_kernel='UNRESOLVED', novelty='NOT_ESTABLISHED', general_problem='UNSOLVED')
        finally:
            for directory in readonly: directory.chmod(0o755)
            for name in ACCEPTED: (work/name).chmod(0o644)
        return result


def main():
    need(len(sys.argv) == 4, 'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin, bootstrap_pin, path = sys.argv[1:]
    root = Path(os.path.abspath(path))
    snapshot, parsed = integrity(root, manifest_pin, bootstrap_pin)
    result = replay(snapshot, parsed)
    after, after_parsed = integrity(root, manifest_pin, bootstrap_pin)
    need(after == snapshot and same(after_parsed, parsed), 'publication changed during replay')
    result.update(schema=1, problem_id=2960, status='PASS', publication_files=len(FILES),
                  optimization=sys.flags.optimize, uid=os.getuid(), euid=os.geteuid(),
                  queue_status='unsolved', substantive_turns='5/5',
                  manifest_sha256=manifest_pin, bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError, subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed', file=sys.stderr)
        sys.exit(1)
