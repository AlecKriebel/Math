"""Reproduce valid/negative package-wrapper controls in isolated fixture copies."""
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    source = root / 'extracted/dfc_stability_verification'
    fixtures = root / 'wrapper_mutation_fixtures'
    fixtures.mkdir(exist_ok=True)
    rows = []
    for kind in ('valid', 'source_tamper', 'extra_file', 'missing_file', 'symlink', 'optimized'):
        target = fixtures / kind
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        if kind == 'source_tamper':
            path = target / 'main.tex'
            path.write_text(path.read_text().replace('For every fixed real', 'For no fixed real', 1))
        elif kind == 'extra_file':
            (target / 'unlisted.txt').write_text('unlisted')
        elif kind == 'missing_file':
            (target / 'main.tex').unlink()
        elif kind == 'symlink':
            (target / 'unlisted-link').symlink_to('main.tex')
        command = [sys.executable] + (['-O'] if kind == 'optimized' else [])
        command += [str(target / 'reproduce.py'), '--integrity-only']
        proc = subprocess.run(command, cwd=target, text=True, capture_output=True,
                              env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        row = {'kind': kind, 'exit_code': proc.returncode, 'stdout': proc.stdout,
               'stderr': proc.stderr, 'expected': 'pass' if kind == 'valid' else 'reject'}
        rows.append(row)
        if (proc.returncode == 0) != (kind == 'valid'):
            raise RuntimeError(row)
    result = {'utc': datetime.now(timezone.utc).isoformat(), 'results': rows}
    (root / 'WRAPPER_MUTATION_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'PASS_WRAPPER_VALIDITY_AND_MUTATION_CONTROLS',
                      'cases': len(rows), 'negative_rejections': len(rows) - 1}))


if __name__ == '__main__':
    main()
