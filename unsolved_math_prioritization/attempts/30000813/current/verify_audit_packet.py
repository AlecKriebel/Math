#!/usr/bin/env python3
"""Verify this authored audit packet without reading or running third-party code.

Run from a read-only packet, as a non-root user. Output is a receipt on stdout.
Explicit checks remain active under Python -O and -OO. This verifies finite
calculations and packet integrity, not the seventeen general proof arguments.
"""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile


def need(condition, label):
    if not condition:
        raise RuntimeError('FAILED: ' + label)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    packet = Path(__file__).resolve().parent
    manifest_bytes = (packet / 'AUDIT_MANIFEST.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    before = {}
    for entry in manifest['files']:
        name = entry['name']
        need(Path(name).name == name and name not in before, 'unsafe_or_duplicate_manifest_entry')
        p = packet / name
        need(p.is_file() and not p.is_symlink(), 'regular_payload_file:' + name)
        b = p.read_bytes()
        need(len(b) == entry['bytes'] and digest(b) == entry['sha256'], 'payload_digest:' + name)
        before[name] = digest(b)
    need('independent_exact_checks.py' in before and 'EXACT_CHECK_RESULTS.json' in before,
         'required_payload_files')
    script = packet / 'independent_exact_checks.py'
    source = script.read_text()
    need(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(source))),
         'assert_free_checker')
    expected = (packet / 'EXACT_CHECK_RESULTS.json').read_bytes()
    need(json.loads(expected)['status'] == 'PASS', 'expected_result_status')
    need(os.geteuid() != 0, 'non_root_required_for_read_only_probes')
    probes = []
    try:
        descriptor = os.open(script, os.O_WRONLY | os.O_APPEND)
    except PermissionError:
        probes.append({'probe': 'open_existing_checker_for_append', 'outcome': 'PermissionError'})
    else:
        os.close(descriptor)
        raise RuntimeError('FAILED: existing_file_is_writable')
    try:
        descriptor = os.open(packet / '.write_probe', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except PermissionError:
        probes.append({'probe': 'create_new_file_in_packet', 'outcome': 'PermissionError'})
    else:
        os.close(descriptor)
        raise RuntimeError('FAILED: packet_directory_is_writable')
    runs = []
    for option in ([], ['-O'], ['-OO']):
        command = [sys.executable, '-B', *option, str(script)]
        result = subprocess.run(command, cwd=packet, capture_output=True)
        need(result.returncode == 0 and result.stdout == expected and not result.stderr,
             'exact_replay:' + str(option))
        runs.append({'optimization': option[0] if option else 'none', 'exit_code': result.returncode,
                     'stdout_bytes': len(result.stdout), 'stdout_sha256': digest(result.stdout),
                     'matches_frozen_results': True})
    controls = []
    for option in ([], ['-O'], ['-OO']):
        program = ('import runpy; runpy.run_path(' + repr(str(script)) +
                   ')["check"](False,"deliberate_false_condition")')
        result = subprocess.run([sys.executable, '-B', *option, '-c', program], capture_output=True)
        need(result.returncode != 0 and b'FAILED: deliberate_false_condition' in result.stderr,
             'optimization_false_condition_control')
        controls.append({'control': 'forced_false_condition',
                         'optimization': option[0] if option else 'none',
                         'exit_code': result.returncode, 'expected_failure_observed': True})
    old = 'check(determinant(minor) == 64,'
    need(source.count(old) == 1, 'mutation_anchor_unique')
    mutated = source.replace(old, 'check(determinant(minor) == 65,', 1)
    with tempfile.TemporaryDirectory(prefix='hadamard_authored_control_') as temp:
        mutant = Path(temp) / 'mutated_authored_checker.py'
        mutant.write_text(mutated)
        for option in ([], ['-O'], ['-OO']):
            result = subprocess.run([sys.executable, '-B', *option, str(mutant)], capture_output=True)
            need(result.returncode != 0 and b'FAILED: exact_check_' in result.stderr,
                 'wrong_determinant_control')
            controls.append({'control': 'expected_active_determinant_64_changed_to_65',
                             'optimization': option[0] if option else 'none',
                             'exit_code': result.returncode, 'expected_failure_observed': True})
    after = {name: digest((packet / name).read_bytes()) for name in before}
    need(before == after, 'payload_unchanged_during_replay')
    receipt = {'schema': 1, 'status': 'PASS_FINITE_CHECKS_AND_PACKET_INTEGRITY',
               'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'manifest_sha256': digest(manifest_bytes), 'manifest_bytes': len(manifest_bytes),
               'checked_payload_files': len(before), 'euid': os.geteuid(), 'egid': os.getegid(),
               'packet_mode': oct(stat.S_IMODE(packet.stat().st_mode)),
               'checker_mode': oct(stat.S_IMODE(script.stat().st_mode)),
               'python_version': sys.version.split()[0], 'read_only_probes': probes,
               'replays': runs, 'failure_controls': controls, 'payload_unchanged': True,
               'scope': 'Finite exact diagnostics, optimization safety, read-only execution and authored packet hashes only.',
               'general_proof_audit': 'Separate written mathematical analysis in AUDIT.md; not certified by this script.',
               'formal_companion': 'Static inspection only; no Lean build, axiom audit or downloaded companion execution.'}
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
