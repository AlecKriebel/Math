#!/usr/bin/env python3
"""Read-only controls for finite diagnostics and immutable-source authentication.

Successful replay emits JSON only. Negative controls execute mutated source in
memory; neither original source blobs nor curated receipts are modified.
"""
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

OWN = Path(__file__).resolve().parent
FINITE = OWN / 'check_topology_applicability.py'
AUTH = OWN / 'authenticate_sources.py'
OLD_MANIFEST_PIN = 'dca3fb07891b932f1ac1c493f9e919adef6b890b6e310047a56f9649784aca07'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def snapshot():
    names = json.loads((OWN / 'PUBLIC_ALLOWLIST.json').read_text())['files']
    return {name: {'sha256': hashlib.sha256((OWN / name).read_bytes()).hexdigest(),
                   'mtime_ns': (OWN / name).stat().st_mtime_ns,
                   'bytes': (OWN / name).stat().st_size}
            for name in names if (OWN / name).is_file()}

def execute(flags, env, path=None, source=None):
    command = [sys.executable, *flags]
    if source is None:
        command.append(str(path))
    else:
        command.extend(['-c', source])
    return subprocess.run(command, env=env, capture_output=True, text=True,
                          timeout=30, cwd=OWN)

def main():
    before = snapshot()
    finite_source = FINITE.read_text()
    auth_source = AUTH.read_text()
    for name, source in [('finite', finite_source), ('authentication', auth_source)]:
        tree = ast.parse(source)
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
                name + ' helper contains an optimization-removable assertion')
        forbidden = {'write_text', 'write_bytes', 'unlink', 'rename', 'remove', 'mkdir', 'touch'}
        require(not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and node.func.attr in forbidden for node in ast.walk(tree)),
                name + ' helper contains a file mutation call')

    length_needle = 'EXPECTED_WORD_LENGTH = 104'
    rank_needle = 'require(rank(twist) >= rank(ordinary, 2),'
    pin_needle = '0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b'
    require(finite_source.count(length_needle) == 1, 'length mutation anchor is ambiguous')
    require(finite_source.count(rank_needle) == 1, 'rank mutation anchor is ambiguous')
    require(auth_source.count(pin_needle) == 1, 'authentication mutation anchor is ambiguous')
    negative_sources = {
        'incorrect_word_length_105': finite_source.replace(length_needle, 'EXPECTED_WORD_LENGTH = 105'),
        'incorrect_rank_inequality': finite_source.replace(rank_needle, 'require(rank(twist) < rank(ordinary, 2),'),
        'incorrect_proof_sha256': '__file__ = ' + repr(str(AUTH)) + '\n' + auth_source.replace(pin_needle, '0' * 64)
    }
    expected_failure = {
        'incorrect_word_length_105': 'nested commutator Artin length differs from the expected 104',
        'incorrect_rank_inequality': 'signed rational rank is smaller than mod-2 rank',
        'incorrect_proof_sha256': 'immutable source authentication failed'
    }
    frozen = json.loads((OWN / 'FINITE_CHECKS.json').read_text())
    modes = [('normal', [], None, 0), ('-O', ['-O'], None, 1),
             ('-OO', ['-OO'], None, 2), ('actual_inherited_2', [], '2', 2)]
    rows = []
    for name, flags, inherited, expected_optimize in modes:
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        if inherited is not None:
            env['PYTHONOPTIMIZE'] = inherited
        # This probe and both helpers receive the identical real process environment.
        # In the inherited case there is no optimization command-line flag.
        probe = execute(flags, env, source="import json,os,sys; print(json.dumps({'optimize':sys.flags.optimize,'PYTHONOPTIMIZE':os.environ.get('PYTHONOPTIMIZE')}))")
        require(probe.returncode == 0, name + ': interpreter probe failed')
        observed = json.loads(probe.stdout)
        require(observed['optimize'] == expected_optimize,
                name + ': actual optimization level differs from requested control')
        if name == 'actual_inherited_2':
            require(flags == [] and observed['PYTHONOPTIMIZE'] == '2',
                    'inherited control was not genuinely environment-driven')
        good = execute(flags, env, path=FINITE)
        require(good.returncode == 0 and good.stderr == '', name + ': finite replay failed')
        actual = json.loads(good.stdout)
        require(actual == frozen, name + ': finite result differs from frozen receipt')
        require(actual['rank_diagnostics']['signed_group_ring_2_by_2_matrices_tested'] == 6561,
                name + ': finite replay omitted rank cases')
        authenticated = execute(flags, env, path=AUTH)
        require(authenticated.returncode == 0 and authenticated.stderr == '',
                name + ': immutable authentication replay failed')
        auth = json.loads(authenticated.stdout)
        require(auth['all_pass'] and auth['closed_inventory_matches'] and
                auth['pinned_digests_pass'] and auth['selected_count'] == 44,
                name + ': immutable source receipt is incomplete')
        negatives = []
        for control, source in negative_sources.items():
            bad = execute(flags, env, source=source)
            require(bad.returncode != 0, name + ': incorrect check succeeded: ' + control)
            require(bad.stdout == '', name + ': incorrect check emitted success JSON: ' + control)
            require(expected_failure[control] in bad.stderr,
                    name + ': incorrect check failed for an unrelated reason: ' + control)
            negatives.append({'control': control, 'returncode': bad.returncode,
                              'success_stdout_empty': True,
                              'expected_failure_seen': expected_failure[control]})
        rows.append({'mode': name, 'command_optimization_flags': flags,
                     'observed_interpreter': observed, 'finite_replay_matches_frozen': True,
                     'rank_cases_executed': 6561, 'authentication_count': 44,
                     'authentication_all_pass': True, 'negative_controls': negatives})
    after = snapshot()
    require(after == before, 'diagnostic replay mutated a curated file or its timestamp')
    return {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'scope': 'Diagnostic-code hardening only; mathematical proof and verdict unchanged.',
            'superseded_manifest_sha256': OLD_MANIFEST_PIN,
            'runtime': {'executable': sys.executable, 'version': sys.version,
                        'harness_optimize': sys.flags.optimize,
                        'harness_PYTHONOPTIMIZE': os.environ.get('PYTHONOPTIMIZE')},
            'controls': rows,
            'assert_nodes_in_both_helpers': 0,
            'curated_files_checked_read_only': len(before),
            'all_curated_content_sizes_and_mtimes_unchanged': True,
            'negative_control_execution': 'Mutated source executed in memory; original44 and curated source/receipts unchanged.',
            'all_pass': True}

if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
