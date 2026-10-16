#!/usr/bin/env python3
"""Reproduce the frozen candidate and audit checks under genuine UID 1000.

Usage: python reproduce_audit.py CANDIDATE_DIRECTORY OUTPUT_JSON
Only temporary audit copies are made read-only or mutated. No supplied candidate
or source file is modified. Results are written only to the selected output file.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile

FREEZE_SHA256 = '5ca5ea8c8f68876e60dbc5d576ff1cd4415adf22761ea2fcf1969cbdc428c901'
TREE_SHA256 = '9373856af6e529c088f6df98cc42e147f3b8730e00494a90af7781e62d90cf83'
MODES = [('normal', []), ('-O', ['-O']), ('-OO', ['-OO'])]
WRAPPER = '''import json,os,sys,runpy
print(json.dumps({'runtime':{'uid':os.getuid(),'euid':os.geteuid(),'gid':os.getgid(),'optimize':sys.flags.optimize}}),flush=True)
runpy.run_path(sys.argv[1],run_name='__main__')
'''


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(folder):
    return {str(p.relative_to(folder)): {'bytes': p.stat().st_size,
                'sha256': sha(p.read_bytes()), 'mode': stat.S_IMODE(p.stat().st_mode)}
            for p in sorted(folder.rglob('*')) if p.is_file()}


def validate_freeze(candidate):
    raw = (candidate/'CANDIDATE_FREEZE.json').read_bytes()
    require(sha(raw) == FREEZE_SHA256, 'external frozen-manifest hash mismatch')
    freeze = json.loads(raw)
    rows = freeze['files']
    tree = sha(json.dumps(rows, sort_keys=True, separators=(',', ':')).encode())
    require(tree == freeze['candidate_tree_sha256'] == TREE_SHA256, 'tree pin mismatch')
    require({str(p.relative_to(candidate)) for p in (candidate/'public').iterdir()} ==
            {r['path'] for r in rows}, 'unexpected or missing public candidate file')
    for row in rows:
        p = candidate/row['path']
        require(p.is_file() and not p.is_symlink(), 'candidate path is not a regular file')
        data = p.read_bytes()
        require(len(data) == row['bytes'] and sha(data) == row['sha256'],
                'candidate file does not match external freeze')
    return {'manifest_sha256': FREEZE_SHA256, 'tree_sha256': tree, 'files_checked': len(rows)}


def readonly(folder):
    for p in folder.rglob('*'):
        p.chmod(0o555 if p.is_dir() else 0o444)
    folder.chmod(0o555)
    denied = []
    for path in [folder/'verify_exact_checks.py', folder/'new_write_probe']:
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT, 0o600)
        except PermissionError:
            denied.append(True)
        else:
            os.close(fd)
            denied.append(False)
    require(all(denied) and not os.access(folder, os.W_OK), 'read-only write probe failed')
    return {'directory_mode': '0555', 'file_modes': '0444',
            'existing_file_write_denied': denied[0], 'new_file_write_denied': denied[1]}


def run(folder, script, mode):
    label, flags = mode
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    before = snapshot(folder)
    p = subprocess.run([sys.executable, '-B', *flags, '-c', WRAPPER, str(folder/script)],
                       cwd=folder, env=env, text=True, capture_output=True, timeout=120)
    require(snapshot(folder) == before, 'test changed read-only input')
    lines = p.stdout.splitlines()
    require(lines, 'missing child runtime record')
    runtime = json.loads(lines[0])['runtime']
    require(runtime['uid'] == runtime['euid'] == 1000, 'child is not genuine UID 1000')
    require(runtime['optimize'] == len(flags[0])-1 if flags else runtime['optimize'] == 0,
            'wrong optimization mode')
    body = '\n'.join(lines[1:]) + ('\n' if len(lines) > 1 else '')
    return {'mode': label, 'script': script, 'runtime': runtime,
            'returncode': p.returncode, 'body_sha256': sha(body.encode()),
            'stderr_sha256': sha(p.stderr.encode()),
            'error_last_line': p.stderr.strip().splitlines()[-1] if p.stderr.strip() else None,
            'result': json.loads(body) if p.returncode == 0 else None,
            'input_unchanged': True}, body


MUTATIONS = {
    'wrong_x_square': ('3*j*ell', '0*j*ell'),
    'wrong_conjugation': ('(-1 if j else 1)', '(1 if j else 1)'),
    'wrong_derived_expectation': ('derived == {(0, 0), (2, 0), (4, 0)}',
                                'derived == {(0, 0)}'),
    'wrong_smith_expectation': ('(delta1, delta2) == (1, 4)', '(delta1, delta2) == (1, 2)'),
    'omit_one_twist': ('boundary_of_left == all_edges', 'boundary_of_left == (all_edges ^ 1)'),
    'false_single_edge_cancellation': ('gf2_rank(vertex_rows + [1]) == rank+1',
                                     'gf2_rank(vertex_rows + [1]) == rank'),
    'wrong_cover_rank': ('cycle_rank == (m-1)*(n-1)', 'cycle_rank == m*n'),
    'wrong_kunneth_input': ('base_betti = [1, 0, 0, 1]', 'base_betti = [1, 1, 0, 1]'),
    'noncancelling_obstruction_sum': ('(a[0]^a[0], a[1]^a[1]) == (0, 0)',
                                    '(a[0]|a[0], a[1]|a[1]) == (0, 0)'),
    'explicit_false_check': ("group = group_checks()", "check(False, 'audit false predicate'); group = group_checks()"),
}


def main():
    require(len(sys.argv) == 3, 'usage: CANDIDATE_DIRECTORY OUTPUT_JSON')
    candidate, output = (Path(x).resolve() for x in sys.argv[1:])
    require(os.getuid() == os.geteuid() == 1000, 'audit must run as UID 1000')
    public = candidate/'public'
    original = snapshot(public)
    pins = validate_freeze(candidate)
    code = (public/'verify_exact_checks.py').read_text()
    independent = Path(__file__).with_name('independent_checks.py').read_text()
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(code))),
            'candidate checks contain optimization-disabled assertions')
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(independent))),
            'independent checks contain optimization-disabled assertions')
    expected_bytes = (public/'EXACT_CHECKS.json').read_bytes()
    rows = []
    independent_results = []
    with tempfile.TemporaryDirectory(prefix='pseudoisotopy-audit-') as td:
        temp = Path(td)
        baseline = temp/'baseline'
        shutil.copytree(public, baseline)
        (baseline/'independent_checks.py').write_text(independent)
        ro = readonly(baseline)
        for mode in MODES:
            r, body = run(baseline, 'verify_exact_checks.py', mode)
            require(r['returncode'] == 0 and body.encode() == expected_bytes,
                    'candidate exact output mismatch')
            r.update(test='baseline', readonly=ro, saved_output_byte_match=True)
            rows.append(r)
            r, body = run(baseline, 'independent_checks.py', mode)
            require(r['returncode'] == 0 and r['result']['status'] == 'PASS',
                    'independent checks failed')
            r.update(test='independent_baseline', readonly=ro)
            rows.append(r)
            independent_results.append(body)
        require(len(set(independent_results)) == 1, 'optimization changed independent output')
        for name, (old, new) in MUTATIONS.items():
            require(code.count(old) == 1, 'mutation target not unique: '+name)
            folder = temp/name
            shutil.copytree(public, folder)
            (folder/'verify_exact_checks.py').write_text(code.replace(old, new))
            ro = readonly(folder)
            for mode in MODES:
                r, body = run(folder, 'verify_exact_checks.py', mode)
                require(r['returncode'] != 0 and r['result'] is None,
                        'invalid mathematical control was accepted: '+name)
                require(r['error_last_line'].startswith('RuntimeError:'),
                        'control failed for an unintended reason')
                r.update(test=name, readonly=ro, invalid_control_rejected=True)
                rows.append(r)
        # Restore permissions only on temporary directories for their cleanup.
        for p in temp.rglob('*'):
            if p.is_dir():
                p.chmod(0o755)
    require(snapshot(public) == original, 'original candidate was changed')
    require(validate_freeze(candidate) == pins, 'original freeze was changed')
    result = {'status': 'PASS', 'uid': os.getuid(), 'euid': os.geteuid(),
              'python_version': sys.version, 'pins': pins, 'modes': [m[0] for m in MODES],
              'runs': len(rows), 'negative_controls_per_mode': len(MUTATIONS),
              'invalid_control_rejections': len(MUTATIONS)*len(MODES),
              'candidate_assert_statements': 0, 'independent_assert_statements': 0,
              'candidate_unchanged': True, 'rows': rows,
              'limits': ['Checks do not certify smooth or topological pseudo-isotopy.',
                         'Source-theorem hypotheses are audited in prose.',
                         'Original exact checker is arithmetic, not a bundle-integrity verifier.']}
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: result[k] for k in ['status', 'runs', 'invalid_control_rejections',
                                           'candidate_unchanged', 'pins']}, indent=2))


if __name__ == '__main__':
    main()
