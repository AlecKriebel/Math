"""Isolated replay and adversarial inventory/output controls; never edits the original."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def update_binding(root, name):
    p = root / 'MANIFEST.json'
    manifest = json.loads(p.read_bytes())
    raw = (root / name).read_bytes()
    for row in manifest['files']:
        if row['path'] == name:
            row['bytes'] = len(raw)
            row['sha256'] = hashlib.sha256(raw).hexdigest()
    p.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')


def run(root, optimized, cwd):
    command = [sys.executable] + (['-O'] if optimized else []) + [str(root / 'verify.py')]
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=30)


def main():
    source = Path(__file__).resolve().parent
    rows = []
    mutations = ['payload_tamper', 'missing_file', 'unexpected_file', 'cache_directory',
                 'empty_directory', 'symlink', 'fifo', 'manifest_duplicate',
                 'rebound_wrong_output', 'rebound_expected_result', 'rebound_scope_drift']
    with tempfile.TemporaryDirectory(prefix='wreath-integrity-') as temp:
        temp = Path(temp)
        clean = temp / 'relocated'
        shutil.copytree(source, clean)
        normal = run(clean, False, temp)
        opt = run(clean, True, temp)
        require(normal.returncode == 0 and opt.returncode == 0, 'clean relocated replay')
        require(normal.stdout == opt.stdout, 'optimization output changed')
        require(not list(clean.glob('__pycache__')), 'unexpected source cache')
        for name in mutations:
            root = temp / name
            shutil.copytree(source, root)
            if name == 'payload_tamper':
                with (root / 'checks.py').open('a') as f:
                    f.write('\n# altered\n')
            elif name == 'missing_file':
                (root / 'README.md').unlink()
            elif name == 'unexpected_file':
                (root / 'extra.txt').write_text('extra')
            elif name == 'cache_directory':
                (root / '__pycache__').mkdir()
                (root / '__pycache__' / 'checks.pyc').write_bytes(b'not executable cache')
            elif name == 'empty_directory':
                (root / 'extra_dir').mkdir()
            elif name == 'symlink':
                (root / 'README.md').unlink()
                (root / 'README.md').symlink_to(source / 'README.md')
            elif name == 'fifo':
                (root / 'README.md').unlink()
                os.mkfifo(root / 'README.md')
            elif name == 'manifest_duplicate':
                p = root / 'MANIFEST.json'
                d = json.loads(p.read_bytes())
                d['files'].append(d['files'][0])
                p.write_text(json.dumps(d))
            elif name == 'rebound_wrong_output':
                p = root / 'checks.py'
                s = p.read_text()
                require("'all_checks_passed': True" in s, 'mutation target missing')
                p.write_text(s.replace("'all_checks_passed': True", "'all_checks_passed': False"))
                update_binding(root, 'checks.py')
            elif name == 'rebound_expected_result':
                p = root / 'EXPECTED_RESULTS.json'
                d = json.loads(p.read_bytes())
                d['counts']['coordinate_identities'] += 1
                p.write_text(json.dumps(d, indent=2, sort_keys=True) + '\n')
                update_binding(root, 'EXPECTED_RESULTS.json')
            elif name == 'rebound_scope_drift':
                p = root / 'STATUS.json'
                d = json.loads(p.read_bytes())
                d['disposition'] = 'verified_solution'
                p.write_text(json.dumps(d, indent=2, sort_keys=True) + '\n')
                update_binding(root, 'STATUS.json')
            results = [run(root, optimized, temp) for optimized in [False, True]]
            require(all(r.returncode != 0 for r in results), 'mutation escaped: ' + name)
            rows.append({'mutation': name, 'normal_rejected': True, 'optimized_rejected': True})
    return {'schema': 1, 'relocated_normal_passed': True, 'relocated_optimized_passed': True,
            'normal_optimized_outputs_identical': True, 'source_cache_created': False,
            'mutation_cases': rows, 'mutation_rejections': 2 * len(rows),
            'purpose': 'software integrity controls, not mathematical verification'}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
