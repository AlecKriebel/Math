"""Fail-closed publication inventory, AST provenance and complete symbolic replay."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
EXPECTED = {'RESEARCH.md', 'AUDIT.md', 'SOURCE_GATE.md', 'SOURCE_METADATA.json', 'DATASET_MAPPING.json', 'ACCEPTANCE_RECEIPT.json', 'PUBLICATION_PROVENANCE.json', 'check_obstruction.py', 'checks.py', 'symbolic_checks.json', 'CHECK_RESULTS.json', 'verify.py', 'README.md', 'PACKAGE_AUDIT.md', 'MANIFEST.json'}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def inventory(root):
    entries = list(root.rglob('*'))
    require(not any(p.is_symlink() or not p.is_file() for p in entries), 'Non-file or symlink in package')
    require({p.relative_to(root).as_posix() for p in entries} == EXPECTED, 'Strict inventory mismatch')
    m = json.loads((root / 'MANIFEST.json').read_text())
    require(set(m['files']) == EXPECTED - {'MANIFEST.json'}, 'Manifest key mismatch')
    for name, spec in m['files'].items():
        data = (root / name).read_bytes()
        require(spec == {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}, 'Hash/size mismatch: ' + name)

class Harden(ast.NodeTransformer):
    def __init__(self, name, source):
        self.name, self.source = name, source
    def visit_Assert(self, node):
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(), operand=node.test), body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError', ctx=ast.Load()), args=[ast.Constant(value=f'{self.name}:{node.lineno}: ' + ast.get_source_segment(self.source, node.test))], keywords=[]), cause=None)], orelse=[]), node)

def provenance():
    data = json.loads((ROOT / 'PUBLICATION_PROVENANCE.json').read_text())
    for item in data['assert_hardening']:
        source = item['original_source']
        raw = source.encode()
        require(item['original'] == {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}, 'Original source provenance hash mismatch')
        records = []
        def walk(node, ancestors):
            if isinstance(node, ast.Assert):
                records.append({'line': node.lineno, 'column': node.col_offset, 'condition': ast.get_source_segment(source, node.test), 'condition_ast': ast.dump(node.test, include_attributes=False), 'control_flow': [{'kind': type(a).__name__, 'line': a.lineno, 'header': ast.unparse(a.test) if isinstance(a, ast.If) else ast.unparse(a.target) + ' in ' + ast.unparse(a.iter)} for a in ancestors]})
            for child in ast.iter_child_nodes(node):
                walk(child, ancestors + ([node] if isinstance(node, (ast.For, ast.If)) else []))
        original = ast.parse(source)
        walk(original, [])
        require(records == item['assertions'], 'Exact assertion/control-flow provenance mismatch')
        expected = ast.fix_missing_locations(Harden(item['file'], source).visit(original))
        actual = ast.parse((ROOT / item['file']).read_text())
        require(ast.dump(expected, include_attributes=False) == ast.dump(actual, include_attributes=False), 'Hardened AST differs beyond assertion replacement')
        require(not any(isinstance(n, ast.Assert) for n in ast.walk(actual)), 'Residual assert')

def run(path, optimized):
    return subprocess.run([sys.executable, '-B'] + (['-O'] if optimized else []) + [str(path)], text=True, capture_output=True, timeout=120, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})

def main():
    inventory(ROOT)
    if '--inventory-only' in sys.argv:
        print('inventory PASS')
        return
    provenance()
    replay = []
    for script, result in [('check_obstruction.py', 'symbolic_checks.json'), ('checks.py', 'CHECK_RESULTS.json')]:
        reference = json.loads((ROOT / result).read_text())
        for optimized in (False, True):
            process = run(ROOT / script, optimized)
            require(process.returncode == 0, process.stderr)
            require(json.loads(process.stdout) == reference, 'Complete result replay mismatch')
            replay.append({'script': script, 'optimized': optimized, 'full_json_match': True})
    source = (ROOT / 'checks.py').read_text()
    mutations = [('polynomial_derivation', 'L = s.cancel(pi * s.diff(d, x) / d)', 'L = s.cancel(pi * s.diff(d, x) / d) + 1'), ('bracket', 'q = s.cancel(L * g - pi * s.diff(g, x))', 'q = s.cancel(L * g - pi * s.diff(g, x)) + 1'), ('cup', 's.rem(s.expand(g * pi), d, x)', 's.rem(s.expand(g * pi + 1), d, x)')]
    controls = []
    with tempfile.TemporaryDirectory() as temporary:
        tmp = Path(temporary)
        for name, before, after in mutations:
            require(source.count(before) == 1, 'Mutation target is not unique: ' + name)
            f = tmp / (name + '.py')
            f.write_text(source.replace(before, after))
            for optimized in (False, True):
                process = run(f, optimized)
                require(process.returncode != 0 and 'RuntimeError: checks.py:' in process.stderr, 'Mutation not rejected by mathematical check: ' + name)
                controls.append({'mutation': name, 'optimized': optimized, 'rejected': True, 'failure': process.stderr.strip().splitlines()[-1]})
        # Exercise inventory rejection before hashing, including a nested MANIFEST.
        import shutil
        copied = tmp / 'copy'
        shutil.copytree(ROOT, copied)
        nested = copied / 'nested'
        nested.mkdir()
        (nested / 'MANIFEST.json').write_text('{}')
        try:
            inventory(copied)
        except RuntimeError:
            pass
        else:
            raise RuntimeError('Nested MANIFEST was not rejected')
    print(json.dumps({'replay': replay, 'corruption_controls': controls, 'nested_manifest_rejected': True, 'ast_provenance': 'PASS', 'inventory': 'PASS'}, indent=2))

if __name__ == '__main__':
    main()
