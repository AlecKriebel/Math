"""Fail-closed local frozen-package verification; receipt must be outside package."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

def inventory(root):
    # Inspect every entry before reading any package payload. Do not follow links.
    found = []
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise RuntimeError('root is not a real directory')
    def walk(directory):
        with os.scandir(directory) as entries:
            for entry in entries:
                mode = entry.stat(follow_symlinks=False).st_mode
                p = Path(entry.path)
                if stat.S_ISDIR(mode):
                    raise RuntimeError('unexpected directory: ' + str(p))
                if not stat.S_ISREG(mode):
                    raise RuntimeError('nonregular entry rejected before payload reads: ' + str(p))
                found.append(p.name)
    walk(root)
    return set(found)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def verify(root, receipt_path):
    names = inventory(root)
    if receipt_path.parent.resolve() == root.resolve():
        raise RuntimeError('receipt must be external')
    if not stat.S_ISREG(receipt_path.lstat().st_mode):
        raise RuntimeError('receipt is not regular')
    receipt = json.loads(receipt_path.read_bytes())
    manifest_bytes = (root/'MANIFEST.json').read_bytes()
    if digest(manifest_bytes) != receipt['manifest_sha256']:
        raise RuntimeError('external manifest pin mismatch')
    manifest = json.loads(manifest_bytes)
    if names != set(manifest) | {'MANIFEST.json'}:
        raise RuntimeError('inventory mismatch')
    for name, meta in manifest.items():
        if Path(name).name != name or name in ('.','..'):
            raise RuntimeError('unsafe manifest path')
        data = (root/name).read_bytes()
        if len(data) != meta['bytes'] or digest(data) != meta['sha256']:
            raise RuntimeError('payload mismatch: ' + name)
    expected_ast = json.loads((root/'AST_PROVENANCE.json').read_bytes())
    scripts = sorted(n for n in manifest if n.endswith('.py'))
    if set(expected_ast) != set(scripts):
        raise RuntimeError('AST coverage mismatch')
    for name in scripts:
        parsed = ast.dump(ast.parse((root/name).read_text()), include_attributes=True)
        if parsed != expected_ast[name]:
            raise RuntimeError('AST mismatch: ' + name)
    outputs = []
    for flags, saved in [([], 'LATTICE_CHECK.json'), (['-O'], 'LATTICE_CHECK_OPTIMIZED.json')]:
        run = subprocess.run([sys.executable, *flags, '-B', str(root/'check_lattice.py')], capture_output=True, text=True, timeout=30)
        if run.returncode or run.stderr:
            raise RuntimeError('checker replay failed: ' + run.stderr)
        value = json.loads(run.stdout)
        if value != json.loads((root/saved).read_bytes()):
            raise RuntimeError('saved replay mismatch')
        outputs.append(value)
    if outputs[0] != outputs[1]:
        raise RuntimeError('optimization mismatch')
    return {'status':'PASS','files':len(manifest)+1,'normal_and_optimized_replay':True,'full_ast_coverage':scripts,'receipt_pin':'external SHA-256; integrity, not mathematical proof'}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python -B verify.py EXTERNAL_RECEIPT.json')
    print(json.dumps(verify(Path(__file__).absolute().parent, Path(sys.argv[1]).absolute()), indent=2))
