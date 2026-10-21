"""Guard/inventory negative controls. Numerical mutations are diagnostics, not proof."""
import ast
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
ENV = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
results = []


def run(path, optimized=False, argument=None):
    args = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(path)]
    if argument is not None:
        args.append(str(argument))
    return subprocess.run(args, capture_output=True, text=True, env=ENV, timeout=120)


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


sources = {name:(ROOT / name).read_text() for name in ('exact_checks.py','independent_exact_audit.py','residual_checks.py')}
mutations = {
    'PF_factors': ('exact_checks.py', 'k - j, 5', 'k - j, 6'),
    'inverse_series': ('exact_checks.py', 'K += S.solve(expr, c)[0] * w ** n', 'K -= S.solve(expr, c)[0] * w ** n'),
    'Yukawa_normalization': ('exact_checks.py', 'tr(5 / A[1]', 'tr(6 / A[1]'),
    'genus_one_normalization': ('exact_checks.py', 'S.Rational(31, 3)', 'S.Rational(30, 3)'),
    'residual_degree': ('residual_checks.py', 'degree_bound=g-m-2', 'degree_bound=g-m-1'),
    'leading_functional': ('residual_checks.py', 'leading=5**(2*g-2)*derivative', 'leading=5**(2*g-2)*(derivative+1)'),
}
with tempfile.TemporaryDirectory(prefix='quintic_controls_') as tmp:
    tmp = Path(tmp)
    for optimized in (False, True):
        integrity = run(ROOT / "verify_package.py", optimized)
        check(integrity.returncode == 0, "inventory baseline failed: " + integrity.stderr)
        results.append({"control":"inventory_baseline","optimized":optimized,"passed":True})
        for name, output in [('exact_checks.py','exact_checks.log'),('independent_exact_audit.py','independent_exact_audit.txt'),('residual_checks.py','residual_results.json')]:
            replay=tmp/name
            replay.write_text(sources[name])
            baseline = run(replay, optimized)
            check(baseline.returncode == 0, 'baseline failed: ' + baseline.stderr)
            check(baseline.stdout == (ROOT/output).read_text(), 'complete stdout mismatch: '+name)
            if name=='exact_checks.py':
                check((tmp/'exact_checks.json').read_bytes()==(ROOT/'exact_checks.json').read_bytes(),'complete JSON mismatch')
            results.append({'control':'complete_output_replay_'+name,'optimized':optimized,'passed':True})
        for label, (name, old, new) in mutations.items():
            source=sources[name]
            check(old in source, 'mutation anchor missing: '+label)
            path=tmp/(label+'.py')
            path.write_text(source.replace(old,new,1))
            result=run(path,optimized)
            check(result.returncode!=0 and 'AssertionError' in result.stderr,'mathematical mutation escaped: '+label+' '+result.stderr)
            results.append({'control':label,'optimized':optimized,'passed':True,'rejected_by':'AssertionError'})
        for name,source in sources.items():
            tree=ast.parse(source)
            check(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)), 'optimization-sensitive assert')
            check(any(isinstance(n,ast.Raise) for n in ast.walk(tree)), 'no explicit guards')
            results.append({'control':'explicit_guard_AST_'+name,'optimized':optimized,'passed':True})
        controls = ['alter_file', 'missing_file', 'extra_root', 'extra_nested', 'nested_manifest', 'symlink_file', 'symlink_directory', 'symlink_manifest', 'unsafe_parent', 'unsafe_absolute', 'unsafe_backslash', 'unsafe_dot', 'duplicate_path', 'self_entry']
        for label in controls:
            target = tmp / 'inventory_case'
            shutil.copytree(ROOT, target)
            mf = target / 'package_manifest.json'
            data = json.loads(mf.read_text())
            if label == 'alter_file': (target / 'README.md').write_text('changed')
            elif label == 'missing_file': (target / 'README.md').unlink()
            elif label == 'extra_root': (target / 'extra.txt').write_text('extra')
            elif label in ('extra_nested', 'nested_manifest'):
                (target / 'nested').mkdir()
                (target / 'nested' / ('package_manifest.json' if label == 'nested_manifest' else 'extra.txt')).write_text('{}')
            elif label == 'symlink_file': (target / 'link').symlink_to('README.md')
            elif label == 'symlink_directory': (target / 'nested').symlink_to(ROOT, target_is_directory=True)
            elif label == 'symlink_manifest':
                mf.unlink(); mf.symlink_to(ROOT / 'package_manifest.json')
            else:
                if label == 'duplicate_path': data['files'].append(data['files'][0].copy())
                else:
                    names = {'unsafe_parent': '../outside', 'unsafe_absolute': '/outside', 'unsafe_backslash': 'a\\b', 'unsafe_dot': './README.md', 'self_entry': 'package_manifest.json'}
                    data['files'][0]['path'] = names[label]
                mf.write_text(json.dumps(data))
            result = run(ROOT / 'verify_package.py', optimized, target)
            check(result.returncode != 0 and 'FAIL:' in result.stderr, 'inventory mutation escaped: ' + label)
            results.append({'control': label, 'optimized': optimized, 'passed': True})
            shutil.rmtree(target)
print(json.dumps({'status': 'PASS', 'controls': results, 'total': len(results)}, indent=2))
