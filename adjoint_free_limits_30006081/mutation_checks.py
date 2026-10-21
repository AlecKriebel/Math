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


source = (ROOT / 'sanity_checks.py').read_text()
# Each mutation changes a mathematical quantity and must reach an explicit guard.
mutations = {
    'EP_reconstruction_sign': ('recovered = Y @', 'recovered = -Y @'),
    'row_tail_Frobenius_sign': ('np.linalg.norm(delta) ** 2 +', '-1000000.0 +'),
    'rank_one_diameter_scale': ('- 2 * radius', '- 3 * radius'),
    'convection_skew_symmetry': ('D[i - 1, j - 1] = 4 *', 'D[i - 1, j - 1] = 4 *'),
    'PDE_zero_bound': ('bound = min(', 'bound = 0.0 * min('),
}
with tempfile.TemporaryDirectory(prefix='adjoint_free_controls_') as tmp:
    tmp = Path(tmp)
    for optimized in (False, True):
        baseline = run(ROOT / 'sanity_checks.py', optimized)
        check(baseline.returncode == 0, 'baseline failed: ' + baseline.stderr)
        expected = json.loads((ROOT / 'sanity_results.json').read_text())
        check(json.loads(baseline.stdout) == expected, 'complete numerical output mismatch')
        results.append({'control': 'complete_output_replay', 'optimized': optimized, 'passed': True, 'byte_identical': baseline.stdout == (ROOT / 'sanity_results.json').read_text()})
        for label, (old, new) in mutations.items():
            check(old in source, 'mutation anchor missing: ' + label)
            changed = source.replace(old, new, 1)
            if label == 'convection_skew_symmetry':
                changed = changed.replace('if not np.linalg.norm(D + D.T) == 0:', 'D[0, 0] = 1.0\nif not np.linalg.norm(D + D.T) == 0:', 1)
            path = tmp / (label + '.py')
            path.write_text(changed)
            result = run(path, optimized)
            check(result.returncode != 0 and 'AssertionError' in result.stderr, 'mathematical mutation escaped: ' + label)
            results.append({'control': label, 'optimized': optimized, 'passed': True, 'rejected_by': 'AssertionError'})
        # Exercise every guard independently, including under -O.
        tree = ast.parse(source)
        guards = [n for n in ast.walk(tree) if isinstance(n, ast.If) and len(n.body) == 1 and isinstance(n.body[0], ast.Raise)]
        check(len(guards) == 4, 'expected four explicit guards')
        for index in range(4):
            tree = ast.parse(source)
            guards = [n for n in ast.walk(tree) if isinstance(n, ast.If) and len(n.body) == 1 and isinstance(n.body[0], ast.Raise)]
            guards[index].test = ast.Constant(value=True)
            path = tmp / ('guard_' + str(index) + '.py')
            path.write_text(ast.unparse(ast.fix_missing_locations(tree)))
            result = run(path, optimized)
            check(result.returncode != 0 and 'AssertionError' in result.stderr, 'guard inactive')
            results.append({'control': 'force_guard_' + str(index), 'optimized': optimized, 'passed': True})
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
