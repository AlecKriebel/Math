#!/usr/bin/env python3
"""Inventory, replay and mutation controls; not a mathematical theorem prover."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

def require(ok, label):
    if not ok:
        raise ValueError(label)

def inventory(root):
    entries = {}
    def scan(d):
        for x in sorted(d.iterdir()):
            rel = x.relative_to(root).as_posix()
            require(not x.is_symlink(), 'symlink: '+rel)
            require(all(part not in ('.', '..') and part and not any(c in part for c in '\\:\n\r') for part in PurePosixPath(rel).parts), 'unsafe path')
            if x.is_dir():
                require(x.name != '__pycache__', 'unexpected cache directory')
                entries[rel] = {'type': 'directory'}
                scan(x)
            else:
                require(x.is_file(), 'nonregular entry')
                if rel == 'MANIFEST.json':
                    continue
                require(x.name != 'MANIFEST.json', 'nested manifest')
                b = x.read_bytes()
                entries[rel] = {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
    scan(root)
    return entries

def check_inventory(root):
    manifest = json.loads((root/'MANIFEST.json').read_text())
    require(manifest['schema'] == 1, 'schema')
    require(inventory(root) == manifest['files'], 'recursive inventory mismatch')

def execute(script, optimized=False):
    return subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(script)], capture_output=True, text=True)

def main():
    root = Path(__file__).resolve().parent
    check_inventory(root)
    replay = []
    for opt in (False, True):
        for script, output in [('checks.py', 'EXACT_CHECKS.json'), ('identity_checks.py', 'IDENTITY_CHECKS.json')]:
            with tempfile.TemporaryDirectory() as td:
                target = Path(td)/script
                shutil.copyfile(root/script, target)
                result = execute(target, opt)
                expected = (root/output).read_text()
                require(result.returncode == 0 and result.stderr == '', 'replay execution')
                require(result.stdout == expected, 'full stdout replay')
                require((Path(td)/output).read_bytes() == (root/output).read_bytes(), 'full JSON replay')
                replay.append({'script': script, 'optimized': opt, 'stdout_and_json_exact': True})
    mutations = [
        ('local second coefficient', 'checks.py', 'K * (K + 3) // 2', 'K * (K + 1) // 2'),
        ('local p2 denominator', 'checks.py', '(1 + sign_sum) / 3', '(1 + sign_sum) / 2'),
        ('ordinary Gauss sign', 'checks.py', 'g + 1j * 3 ** 0.5', 'g - 1j * 3 ** 0.5'),
        ('shifted pole sign', 'identity_checks.py', 'Tminus = {-1: -C/2', 'Tminus = {-1: C/2'),
        ('Mellin derivative sign', 'identity_checks.py', '{0: f0, 1: -f1}', '{0: f0, 1: f1}'),
        ('missing smoothing coefficient', 'identity_checks.py', 'C/2*(f0*logX+f1-f0*g1)', 'C/2*(f0*logX-f0*g1)'),
        ('normalized Gauss sign', 'identity_checks.py', 'normalized = -1j*g', 'normalized = 1j*g'),
        ('conductor normalization', 'identity_checks.py', 'conductor = ((L-h)**2+3*(L-h)+5)/8', 'conductor = ((L-h)**2+3*(L-h)+5)'),
    ]
    mutation_results = []
    for label, script, old, new in mutations:
        source = (root/script).read_text()
        require(source.count(old) == 1, 'mutation match '+label)
        for opt in (False, True):
            with tempfile.TemporaryDirectory() as td:
                target = Path(td)/script
                target.write_text(source.replace(old, new))
                result = execute(target, opt)
                require(result.returncode != 0 and ('AssertionError' in result.stderr or 'ValueError' in result.stderr), 'mutation not detected '+label)
                mutation_results.append({'mutation': label, 'optimized': opt, 'rejected': True})
    controls = []
    for kind in ('extra_file', 'empty_directory', 'nested_manifest', 'symlink', 'unsafe_path', 'changed_file'):
        with tempfile.TemporaryDirectory() as td:
            clone = Path(td)/'package'
            shutil.copytree(root, clone)
            if kind == 'extra_file': (clone/'extra.txt').write_text('unexpected')
            elif kind == 'empty_directory': (clone/'empty').mkdir()
            elif kind == 'nested_manifest':
                (clone/'nested').mkdir(); (clone/'nested/MANIFEST.json').write_text('{}')
            elif kind == 'symlink': (clone/'alias').symlink_to('RESEARCH.md')
            elif kind == 'unsafe_path': (clone/'bad\\name').write_text('bad')
            else: (clone/'RESEARCH.md').write_text('changed')
            rejected = False
            try: check_inventory(clone)
            except ValueError: rejected = True
            require(rejected, 'inventory control '+kind)
            controls.append({'control': kind, 'rejected': True})
    print(json.dumps({'verdict': 'PASS_PORTABLE_CHECKS_ONLY', 'replays': replay, 'mathematical_mutations': mutation_results, 'inventory_controls': controls, 'analytic_theorem_certified': False}, indent=2))

if __name__ == '__main__':
    main()
