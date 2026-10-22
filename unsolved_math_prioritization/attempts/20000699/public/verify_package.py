#!/usr/bin/env python3
"""Offline fail-closed integrity, complete frozen-checker replay, and corruption controls."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
ACCEPTANCE = '17b1ea3cc46ee519f5c5353f172dffadbc9cd61bfcf0c0927aed846b2ee6eccc'
FROZEN_MANIFEST = '169e8b6860671a2d85cd4fd4492f181830fc4b09f06514c5bcf15aca7207b172'
EXACT_RECEIPT = '93236933f11375fa14c0a73349b538ac8d4355a90d7d7f8be974ba1a9750a206'
SCOPE = {
    'disposition': 'resolved 1/5 only in explicitly amended conditional V1',
    'arithmetic_H_CK_proved': False,
    'individual_fixed_gap_Hardy_Littlewood_proved': False,
    'unrestricted_full_zeta_ratios_proved': False,
    'novelty_claim': False,
    'original_gate_accepted_unchanged': False,
    'mandatory_parameter_range': '0<psi<=phi<1',
    'corrected_swap': 'B_(-beta,-alpha-s,gamma+s,delta)(1)',
    'whole_line_w0_endpoint_retained': True,
}
SPEC = [
    ('witness/exact/verify_exact.py', 'witness/exact/EXACT_RESULTS.json', True),
    ('witness/reverse/check_reverse_identities.py', 'witness/reverse/CHECK_RESULTS.json', False),
    ('witness/euler/verify_local_algebra.py', 'witness/euler/LOCAL_ALGEBRA_CHECKS.json', True),
    ('witness/audit/independent_controls.py', 'witness/audit/independent_controls.json', True),
]
GUARD = {'optimize': 0, 'debug': True, 'false_assertion_rejected': True, 'compile_optimize': 0}
BOOTSTRAP = r'''
import json,pathlib,sys
if sys.flags.optimize != 0 or not __debug__:
    raise RuntimeError('ASSERTIONS_DISABLED_IN_CHILD')
try:
    exec(compile('assert False, "ASSERTION_PROBE"', '<assertion-probe>', 'exec', optimize=0), {})
except AssertionError:
    pass
else:
    raise RuntimeError('ASSERTION_PROBE_NOT_REJECTED')
print('ASSERTION_GUARD=' + json.dumps({'optimize':sys.flags.optimize,'debug':__debug__,'false_assertion_rejected':True,'compile_optimize':0},sort_keys=True),file=sys.stderr,flush=True)
p=pathlib.Path(sys.argv[1])
sys.argv=sys.argv[1:]
exec(compile(p.read_bytes(),str(p),'exec',optimize=0), {'__name__':'__main__','__file__':str(p),'__builtins__':__builtins__})
'''


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(name):
    require(isinstance(name, str) and bool(name), 'Unsafe path: nonstring or empty')
    p = PurePosixPath(name)
    require(not p.is_absolute() and p.as_posix() == name and '..' not in p.parts
            and '\\' not in name and '\0' not in name, 'Unsafe path: ' + name)
    return name


def inventory(root):
    require(root.is_dir() and not root.is_symlink(), 'Package root must be a real directory')
    out = {}
    for p in sorted(root.rglob('*')):
        name = p.relative_to(root).as_posix()
        require(not p.is_symlink(), 'Symlink forbidden: ' + name)
        if p.is_file():
            out[canonical(name)] = p.read_bytes()
        else:
            require(p.is_dir(), 'Nonregular entry: ' + name)
    return out


def json_object(raw):
    def unique(pairs):
        value = {}
        for k, v in pairs:
            require(k not in value, 'Duplicate JSON key: ' + k)
            value[k] = v
        return value
    return json.loads(raw, object_pairs_hook=unique)


def integrity(root=ROOT, anchor=None):
    files = inventory(root)
    require('MANIFEST.json' in files, 'Missing manifest')
    raw = files['MANIFEST.json']
    if anchor is not None:
        require(len(anchor) == 64 and digest(raw) == anchor, 'External manifest trust anchor mismatch')
    m = json_object(raw)
    require(m['schema'] == 'ratios_public_checkpoint_v1', 'Wrong manifest schema')
    require(m['row'] == 1795 and m['id'] == 20000699, 'Wrong target')
    require(m['scope'] == SCOPE, 'Wrong scope')
    require(m['accepted_original_theorem_sha256'] == ACCEPTANCE, 'Wrong original acceptance anchor')
    names = set()
    for e in m['files']:
        n = canonical(e['path'])
        require(n != 'MANIFEST.json' and n not in names, 'Duplicate/self-referential manifest entry')
        names.add(n)
        require(n in files, 'Missing file: ' + n)
        require(type(e['bytes']) is int and e['bytes'] >= 0 and len(files[n]) == e['bytes']
                and digest(files[n]) == e['sha256'], 'File binding mismatch: ' + n)
    require(names == set(files) - {'MANIFEST.json'}, 'Unexpected or unlisted file')
    require(digest(files['witness/audit/FROZEN_REVIEW_MANIFEST.json']) == FROZEN_MANIFEST,
            'Frozen review manifest changed')
    require(digest(files['witness/exact/AUDIT_RECEIPT.json']) == EXACT_RECEIPT, 'Exact audit receipt changed')
    frozen = json_object(files['witness/audit/FROZEN_REVIEW_MANIFEST.json'])
    receipt = json_object(files['witness/exact/AUDIT_RECEIPT.json'])
    require(frozen['disposition'] == 'ACCEPTED_AMENDED_V1_CONDITIONAL_TWO_ARROW_WITNESS'
            and frozen['original_gate_accepted_unchanged'] is False, 'Historical scope changed')
    require(frozen['component_count'] == len(frozen['files']) == 18, 'Historical component count changed')
    editions = json_object(files['EDITION_MAP.json'])
    require(editions['schema'] == 'ratios_public_editions_v1', 'Wrong edition schema')
    ed = {}
    for e in editions['artifact_bindings']:
        n = canonical(e['path'])
        require(n not in ed and n in files, 'Duplicate/missing edition path')
        require(n == 'witness/' + canonical(e['accepted_relative_path']), 'Edition source mapping mismatch')
        require(e['edition'] in ('byte-identical', 'presentation-only'), 'Unknown edition class')
        require(e['public_bytes'] == len(files[n]) and e['public_sha256'] == digest(files[n]),
                'Public edition binding mismatch: ' + n)
        if e['edition'] == 'byte-identical':
            require(e['accepted_bytes'] == len(files[n]) and e['accepted_sha256'] == digest(files[n]),
                    'Accepted byte identity mismatch: ' + n)
        ed[n] = e
    expected_originals = {e['path'] for e in frozen['files'] + receipt['audited_files']} | {
        'audit/FROZEN_REVIEW_MANIFEST.json', 'exact/AUDIT_RECEIPT.json'}
    require(set(ed) == {'witness/' + n for n in expected_originals}
            == {n for n in files if n.startswith('witness/')}, 'Edition coverage incomplete')
    require(len(ed) == 22, 'Wrong edition artifact count')
    require(ed['witness/audit/INDEPENDENT_ACCEPTANCE_AND_COMBINED_THEOREM.md']['accepted_sha256']
            == ACCEPTANCE, 'Accepted theorem edition anchor changed')
    expected_bindings = []
    for origin, entries in [
        ('witness/audit/FROZEN_REVIEW_MANIFEST.json', frozen['files']),
        ('witness/exact/AUDIT_RECEIPT.json', receipt['audited_files']),
        ('witness/source/PUBLIC_SOURCE_METADATA.json', json_object(files['witness/source/PUBLIC_SOURCE_METADATA.json'])['authored_outputs']),
    ]:
        for e in entries:
            n = 'witness/' + canonical(e['path'])
            require(n in ed and ed[n]['accepted_sha256'] == e['sha256']
                    and ed[n]['accepted_bytes'] == e['bytes'], 'Historical edition binding mismatch: ' + n)
            expected_bindings.append({'origin': origin, 'path': n, 'bytes': e['bytes'], 'sha256': e['sha256'],
                                      'status': 'BYTE_IDENTICAL' if ed[n]['edition'] == 'byte-identical' else 'PRESENTATION_EDITION'})
    graph = json_object(files['HISTORICAL_BINDING_ACCOUNTING.json'])
    require(graph['schema'] == 'ratios_historical_bindings_v1' and graph['bindings'] == expected_bindings,
            'Historical binding accounting incomplete')
    scope = json_object(files['REPLAY_SCOPE.json'])
    scripts = {n for n, _, _ in SPEC}
    require(set(scope['mathematical_scripts']) == scripts and scope['mathematical_scripts_omitted'] == [],
            'Incomplete mathematical replay coverage')
    require({n for n in files if n.endswith('.py')} == scripts | {'verify_package.py'},
            'Unclassified executable')
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(files['verify_package.py']))),
            'Wrapper guards may not use optimization-removable assert statements')
    for n in scripts:
        require(ed[n]['edition'] == 'byte-identical', 'Frozen checker has changed: ' + n)
        # The four audited scripts have no child launchers or dynamic loaders.
        # Their imports and entire bodies execute in the same optimization-zero child.
        tree = ast.parse(files[n])
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                require(all(x.name.split('.')[0] in {'fractions','pathlib','json','math','sympy','hashlib'}
                            for x in node.names), 'Unexpected checker import: ' + n)
            if isinstance(node, ast.ImportFrom):
                require(node.module in {'fractions','pathlib','math'}, 'Unexpected checker import: ' + n)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                require(node.func.id not in {'eval','exec','compile','__import__'}, 'Dynamic checker loader: ' + n)
    return files, digest(raw), ed


def materialize(root, files):
    for n, b in files.items():
        p = root / canonical(n)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)


def launch(script, cwd):
    env = dict(os.environ)
    for key in ('PYTHONOPTIMIZE', 'PYTHONPATH', 'PYTHONHOME', 'PYTHONSTARTUP'):
        env.pop(key, None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    proc = subprocess.run([sys.executable, '-I', '-B', '-c', BOOTSTRAP, str(script)],
                          cwd=cwd, env=env, capture_output=True, text=True, timeout=180)
    marks = [s.split('=', 1)[1] for s in proc.stderr.splitlines() if s.startswith('ASSERTION_GUARD=')]
    require(len(marks) == 1 and json_object(marks[0]) == GUARD, 'Missing/invalid child assertion guard')
    return proc


def compare_output(script, actual, expected):
    if script != 'witness/reverse/check_reverse_identities.py':
        require(actual == expected, 'Replay byte mismatch: ' + script)
        return {'output_byte_identical': True}
    a, b = json_object(actual), json_object(expected)
    key = 'maximum_floating_derivative_discrepancy'
    value = a.pop(key)
    b.pop(key)
    require(type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1e-12,
            'Floating derivative regression failed')
    require(a == b, 'Reverse exact fields mismatch')
    return {'output_byte_identical': actual == expected, 'all_nonfloating_fields_identical': True,
            'maximum_floating_derivative_discrepancy': value, 'floating_tolerance': 1e-12}


def replay(files):
    results = []
    with tempfile.TemporaryDirectory(prefix='ratios-clean-replay-') as directory:
        tmp = Path(directory)
        materialize(tmp, files)
        for script, result, writes in SPEC:
            # Always delete every frozen output before execution. A stale PASS cannot be read back.
            (tmp/result).unlink()
            proc = launch(tmp/script, tmp)
            require(proc.returncode == 0, 'CHECKER_FAILED ' + script + '\n' + proc.stdout + proc.stderr)
            comparison = compare_output(script, proc.stdout.encode(), files[result])
            if writes:
                require((tmp/result).is_file() and (tmp/result).read_bytes() == proc.stdout.encode(),
                        'Generated result/stdout mismatch: ' + script)
            else:
                require(not (tmp/result).exists(), 'Unexpected output generation by stdout-only checker')
            results.append({'script': script, 'status': 'PASS', 'child_assertion_guard': GUARD,
                            'frozen_result_deleted_before_execution': True, **comparison})
    return results


MUTATIONS = {
    'witness/exact/verify_exact.py':
        ('assert sum(mu(e) for e in ds) == (1 if n == 1 else 0)',
         'assert sum(mu(e) for e in ds) == (2 if n == 1 else 0), "MATHEMATICAL_MUTANT_EXACT"'),
    'witness/reverse/check_reverse_identities.py':
        ('assert inverse == (1 if n == 1 else 0)',
         'assert inverse == (2 if n == 1 else 0), "MATHEMATICAL_MUTANT_REVERSE"'),
    'witness/euler/verify_local_algebra.py':
        ('expected=1-X*U-X*V+X*K*U*V', 'expected=2-X*U-X*V+X*K*U*V'),
    'witness/audit/independent_controls.py':
        ('assert S.factor(density_local-correct)==0',
         'assert S.factor(density_local-correct+1)==0, "MATHEMATICAL_MUTANT_AUDIT"'),
}


def negative_controls(files):
    results = []
    with tempfile.TemporaryDirectory(prefix='ratios-negative-controls-') as directory:
        tmp = Path(directory)
        for script, _, _ in SPEC:
            for mode in ('assertion-tripwire', 'mathematical-mutant'):
                work = tmp / (Path(script).parent.name + '-' + mode)
                materialize(work, files)
                p = work/script
                if mode == 'assertion-tripwire':
                    changed = b'assert False, "FROZEN_SCRIPT_ASSERTION_TRIPWIRE"\n' + files[script]
                    token = 'FROZEN_SCRIPT_ASSERTION_TRIPWIRE'
                else:
                    old, new = MUTATIONS[script]
                    text = files[script].decode()
                    require(text.count(old) == 1, 'Nonunique mathematical mutation anchor')
                    changed = text.replace(old, new).encode()
                    token = 'AssertionError'
                p.write_bytes(changed)
                proc = launch(p, work)
                require(proc.returncode != 0 and 'AssertionError' in proc.stderr and token in proc.stderr,
                        'MUTANT_NOT_REJECTED ' + mode + ' ' + script + '\n' + proc.stdout + proc.stderr)
                # These tests intentionally bypass integrity to exercise the checker itself.
                results.append({'control': mode, 'script': script, 'rejected_by_assertion': True,
                                'child_assertion_guard': GUARD})
        corruptions = [
            ('changed-proof', 'File binding mismatch: witness/forward/FORWARD_TRANSFER.md'),
            ('changed-checker', 'File binding mismatch: witness/exact/verify_exact.py'),
            ('changed-frozen-output', 'File binding mismatch: witness/exact/EXACT_RESULTS.json'),
            ('missing-checker', 'Missing file: witness/exact/verify_exact.py'),
            ('unexpected-file', 'Unexpected or unlisted file'),
            ('duplicate-entry', 'Duplicate/self-referential manifest entry'),
            ('unsafe-manifest-path', 'Unsafe path:'),
            ('wrong-scope', 'Wrong scope'),
            ('external-anchor-mismatch', 'External manifest trust anchor mismatch'),
            ('symlink', 'Symlink forbidden:'),
        ]
        for mode, reason in corruptions:
            work = tmp/mode
            materialize(work, files)
            m = json_object(files['MANIFEST.json'])
            anchor = None
            if mode.startswith('changed-'):
                target = {'changed-proof':'witness/forward/FORWARD_TRANSFER.md',
                          'changed-checker':'witness/exact/verify_exact.py',
                          'changed-frozen-output':'witness/exact/EXACT_RESULTS.json'}[mode]
                (work/target).write_bytes(files[target]+b'\nCORRUPTED\n')
            elif mode == 'missing-checker':
                (work/'witness/exact/verify_exact.py').unlink()
            elif mode == 'unexpected-file':
                (work/'unexpected.txt').write_text('unexpected')
            elif mode == 'duplicate-entry':
                m['files'].append(m['files'][0])
            elif mode == 'unsafe-manifest-path':
                m['files'][0]['path'] = '../outside.txt'
            elif mode == 'wrong-scope':
                m['scope']['arithmetic_H_CK_proved'] = True
            elif mode == 'external-anchor-mismatch':
                anchor = '0'*64
            elif mode == 'symlink':
                (work/'linked.txt').symlink_to(work/'README.md')
            if mode in ('duplicate-entry','unsafe-manifest-path','wrong-scope'):
                (work/'MANIFEST.json').write_text(json.dumps(m))
            try:
                integrity(work, anchor)
            except (RuntimeError, KeyError, ValueError) as error:
                require(reason in str(error), 'Wrong rejection for '+mode+': '+str(error))
            else:
                raise RuntimeError('CORRUPTION_NOT_REJECTED '+mode)
            results.append({'control':mode,'rejected':True,'expected_reason':reason})
    require(len(results) == 18, 'Incomplete negative controls')
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256')
    parser.add_argument('--integrity-only', action='store_true')
    parser.add_argument('--negative-controls', action='store_true')
    args = parser.parse_args()
    require(not (args.integrity_only and args.negative_controls), 'Negative controls require full replay')
    files, anchor, editions = integrity(ROOT, args.manifest_sha256)
    result = {'status':'PASS','target_row':1795,'target_id':20000699,'scope':SCOPE,
              'manifest_sha256':anchor,'package_file_count':len(files),
              'caller_optimize':sys.flags.optimize,'caller_PYTHONOPTIMIZE':os.environ.get('PYTHONOPTIMIZE'),
              'accepted_original_theorem_sha256':ACCEPTANCE,'historical_authored_bindings_accounted':27,
              'edition_counts':{kind:sum(e['edition']==kind for e in editions.values())
                                for kind in ('byte-identical','presentation-only')},
              'external_source_and_dataset_bytes':'EXCLUDED; historical metadata only, not live checks'}
    if not args.integrity_only:
        result['replay'] = replay(files)
    if args.negative_controls:
        result['negative_controls'] = negative_controls(files)
        result['negative_control_rejections'] = 18
    require(inventory(ROOT) == files, 'Original public package mutated during verification')
    result['package_unchanged'] = True
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('FAIL: '+str(error), file=sys.stderr)
        sys.exit(1)
