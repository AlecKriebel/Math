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


source = (ROOT / 'check_exact.py').read_text()
# Each mutation changes a mathematical quantity and must reach an explicit guard.
mutations = {
    'product_Hilbert_sign': ('h = lambda r, s: (r + 1)', 'h = lambda r, s: -(r + 1)'),
    'quadric_Hilbert_sign': ('hq = lambda d: (d + 1)', 'hq = lambda d: -(d + 1)'),
    'mixed_square_rounding': ('s = math.isqrt(m * a)', 's = math.isqrt(m * a) + 1'),
    'mixed_capacity_negative': ('B = h(r, s) - 2 +', 'B = -1000000000 + h(r, s) - 2 +'),
    'square_subsequence_coefficient': ('m = 4 * a * d * d', 'm = 5 * a * d * d'),
    'quadric_square_rounding': ('d = math.isqrt(m * min(u, v))', 'd = math.isqrt(m * min(u, v)) + 1'),
    'component_budget_capacity': ('+ min(f(d) - 1, f(e) - 1)', '+ min(f(d) - 1, f(e) - 1) + 1'),
}
expected_bytes = (ROOT / 'CHECK_RESULTS.json').read_text()
expected = json.loads(expected_bytes)
with tempfile.TemporaryDirectory(prefix='boundary_mobility_controls_') as tmp:
    tmp = Path(tmp)
    for optimized in (False, True):
        baseline = run(ROOT / 'check_exact.py', optimized)
        check(baseline.returncode == 0, 'baseline failed: ' + baseline.stderr)
        check(json.loads(baseline.stdout) == expected, 'complete numerical output mismatch')
        check(baseline.stdout == expected_bytes, 'complete stdout bytes mismatch')
        check((ROOT / 'CHECK_RESULTS.json').read_text() == expected_bytes, 'complete result file bytes mismatch')
        results.append({'control': 'complete_output_replay', 'optimized': optimized, 'passed': True, 'byte_identical': baseline.stdout == (ROOT / 'CHECK_RESULTS.json').read_text()})
        for label, (old, new) in mutations.items():
            check(old in source, 'mutation anchor missing: ' + label)
            changed = source.replace(old, new, 1)
            path = tmp / (label + '.py')
            path.write_text(changed)
            result = run(path, optimized)
            check(result.returncode != 0 and 'AssertionError' in result.stderr, 'mathematical mutation escaped: ' + label)
            results.append({'control': label, 'optimized': optimized, 'passed': True, 'rejected_by': 'AssertionError'})
        # Exercise every guard independently, including under -O.
        tree = ast.parse(source)
        guards = [n for n in ast.walk(tree) if isinstance(n, ast.If) and len(n.body) == 1 and isinstance(n.body[0], ast.Raise)]
        check(len(guards) == 8, 'expected eight explicit guards')
        for index in range(8):
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
