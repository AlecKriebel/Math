"""Mutate copies only; replay under both optimization modes from unrelated directories."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def need(ok, label):
    if not ok:
        raise RuntimeError(label)


def rebind(root, name):
    manifest_path = root / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_bytes())
    raw = (root / name).read_bytes()
    for row in manifest['files']:
        if row['path'] == name:
            row.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')


def run(root, optimized, cwd):
    return subprocess.run([sys.executable] + (['-O'] if optimized else []) + [str(root / 'audit/verify.py')],
                          cwd=cwd, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                          capture_output=True, text=True, timeout=45)


def main():
    source = Path(__file__).resolve().parents[1]
    mutations = ['tamper_report', 'missing_author', 'unexpected_file', 'empty_directory',
                 'bytecode_directory', 'symlink', 'fifo', 'manifest_duplicate',
                 'rebound_bad_results', 'rebound_bad_source', 'rebound_scope_drift',
                 'rebound_author_manifest', 'rebound_author_proof']
    rows = []
    with tempfile.TemporaryDirectory(prefix='wreath-independent-integrity-') as tmp:
        tmp = Path(tmp)
        clean = tmp / 'clean'
        shutil.copytree(source, clean)
        normal, optimized = [run(clean, o, tmp) for o in [False, True]]
        need(normal.returncode == optimized.returncode == 0, 'relocated clean replay')
        need(normal.stdout == optimized.stdout, 'normal optimized mismatch')
        need(not list(clean.rglob('__pycache__')), 'cache created')
        for mutation in mutations:
            root = tmp / mutation
            shutil.copytree(source, root)
            if mutation == 'tamper_report':
                with (root / 'audit/REPORT.md').open('a') as f: f.write('\naltered\n')
            elif mutation == 'missing_author':
                (root / 'author/README.md').unlink()
            elif mutation == 'unexpected_file':
                (root / 'audit/unexpected.txt').write_text('unlisted')
            elif mutation == 'empty_directory':
                (root / 'audit/empty').mkdir()
            elif mutation == 'bytecode_directory':
                (root / 'audit/__pycache__').mkdir()
                (root / 'audit/__pycache__/independent_checks.pyc').write_bytes(b'bad cache')
            elif mutation in ['symlink', 'fifo']:
                f = root / 'audit/README.md'
                f.unlink()
                if mutation == 'symlink': f.symlink_to(source / 'audit/README.md')
                else: os.mkfifo(f)
            elif mutation == 'manifest_duplicate':
                f = root / 'MANIFEST.json'
                d = json.loads(f.read_bytes()); d['files'].append(d['files'][0])
                f.write_text(json.dumps(d))
            elif mutation == 'rebound_bad_results':
                f = root / 'audit/INDEPENDENT_RESULTS.json'
                d = json.loads(f.read_bytes()); d['counts']['coarse_distance_checks'] += 1
                f.write_text(json.dumps(d, indent=2, sort_keys=True) + '\n')
                rebind(root, 'audit/INDEPENDENT_RESULTS.json')
            elif mutation == 'rebound_bad_source':
                f = root / 'audit/independent_checks.py'
                s = f.read_text(); need("'all_diagnostics_passed': True" in s, 'source target')
                f.write_text(s.replace("'all_diagnostics_passed': True", "'all_diagnostics_passed': False"))
                rebind(root, 'audit/independent_checks.py')
            elif mutation == 'rebound_scope_drift':
                f = root / 'audit/ACCEPTANCE.json'
                d = json.loads(f.read_bytes()); d['human_peer_review'] = True
                f.write_text(json.dumps(d, indent=2, sort_keys=True) + '\n')
                rebind(root, 'audit/ACCEPTANCE.json')
            elif mutation == 'rebound_author_manifest':
                f = root / 'author/MANIFEST.json'
                f.write_bytes(f.read_bytes() + b'\n')
                rebind(root, 'author/MANIFEST.json')
            elif mutation == 'rebound_author_proof':
                f = root / 'author/PROOF.md'
                f.write_bytes(f.read_bytes() + b'\n')
                rebind(root, 'author/PROOF.md')
            results = [run(root, o, tmp) for o in [False, True]]
            need(all(x.returncode != 0 for x in results), 'mutation accepted: ' + mutation)
            rows.append({'mutation': mutation, 'normal_rejected': True, 'optimized_rejected': True})
    return {'schema': 1, 'relocated_normal_passed': True, 'relocated_optimized_passed': True,
            'normal_optimized_identical': True, 'cache_created': False, 'mutation_rejections': 2*len(rows),
            'mutation_cases': rows, 'scope': 'software integrity controls; not verification of the infinite theorem'}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
