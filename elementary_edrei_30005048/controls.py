#!/usr/bin/env python3
"""Negative controls run only in automatically removed temporary package copies."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(value, message):
    if not value:
        raise RuntimeError(message)


def refresh(root):
    entries = [{'file': x.name, 'bytes': x.stat().st_size,
                'sha256': hashlib.sha256(x.read_bytes()).hexdigest()}
               for x in sorted(root.iterdir()) if x.name != 'MANIFEST.json']
    (root / 'MANIFEST.json').write_text(json.dumps({'schema': 1, 'files': entries}, indent=2)+'\n')


def main():
    require(len(sys.argv) == 1, 'path: no alternate roots or arguments accepted')
    original = Path(__file__).resolve().parent
    cases = ['exact_corruption', 'full_output_corruption', 'missing', 'extra',
             'changed', 'duplicate', 'traversal', 'symlink', 'main_guard', 'alternate_root']
    results = []
    for mode in ([], ['-O']):
        good = subprocess.run([sys.executable, '-B', *mode, str(original/'verify_package.py')],
                              capture_output=True, text=True, timeout=60)
        require(good.returncode == 0, 'baseline failed: ' + good.stderr)
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='edrei-control-') as temp:
                root = Path(temp)/'package'
                shutil.copytree(original, root)
                args = []
                if case == 'exact_corruption':
                    path = root/'check_examples.py'
                    text = path.read_text()
                    old = 'truncated = [Fraction(1), Fraction(1), Fraction(1)]'
                    require(text.count(old) == 1, 'mutation target absent')
                    path.write_text(text.replace(old, 'truncated = [Fraction(1), Fraction(1), Fraction(2)]'))
                    refresh(root)
                    expected = 'examples: exact validator rejected'
                elif case == 'full_output_corruption':
                    path = root/'EXACT_CHECKS.json'
                    data = json.loads(path.read_text()); data['exp_z2_minor'] = -2
                    path.write_text(json.dumps(data)); refresh(root)
                    expected = 'examples: full result mismatch'
                elif case == 'missing':
                    (root/'README.md').unlink(); expected = 'integrity: inventory mismatch'
                elif case == 'extra':
                    (root/'unexpected.txt').write_text('extra'); expected = 'integrity: inventory mismatch'
                elif case == 'changed':
                    with (root/'README.md').open('a') as f: f.write('changed')
                    expected = 'integrity: content mismatch'
                elif case in ('duplicate', 'traversal'):
                    path = root/'MANIFEST.json'; data=json.loads(path.read_text())
                    if case == 'duplicate':
                        data['files'].append(data['files'][0]); expected = 'integrity: duplicate path'
                    else:
                        data['files'][0]['file'] = '../outside'; expected = 'integrity: unsafe path'
                    path.write_text(json.dumps(data))
                elif case == 'symlink':
                    path=root/'README.md'; path.unlink(); path.symlink_to(root/'REPORT.md')
                    expected = 'integrity: nonregular file'
                elif case == 'main_guard':
                    path=root/'check_examples.py'
                    path.write_text(path.read_text().replace("if __name__ == '__main__':", 'if True:'))
                    refresh(root); expected = 'guard: missing main guard'
                else:
                    args = [str(original)]; expected = 'path: no alternate roots'
                run = subprocess.run([sys.executable, '-B', *mode, str(root/'verify_package.py'), *args],
                                     cwd=temp, capture_output=True, text=True, timeout=60)
                require(run.returncode != 0 and expected in run.stderr,
                        'wrong rejection stage for ' + case + ': ' + run.stdout + run.stderr)
                if case == 'exact_corruption':
                    require('Truncated geometric determinant changed' in run.stderr,
                            'corruption did not reach exact validator')
                results.append({'case':case, 'mode':'optimized' if mode else 'normal',
                                'rejection_stage':expected, 'passed':True})
    print(json.dumps({'baseline_replay':'PASS','controls':results},indent=2))


if __name__ == '__main__':
    main()
