"""Local integrity/provenance only: this is NOT a mathematical certificate."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

FILES = frozenset({'README.md', 'RESONANT_NODAL_ANALYSIS.md', 'INDEPENDENT_AUDIT.md',
    'SOURCE_GATE.md', 'PUBLIC_METADATA.json', 'PROVENANCE.json', 'verify.py',
    'test_integrity.py', 'AST_PROVENANCE.json', 'MANIFEST.json'})
ANCHORS = {
    'RESONANT_NODAL_ANALYSIS.md': 'b6cb50858de1136ed41a78bc1666c51ca2e15210e1da472f2bde1927bd4649ec',
    'INDEPENDENT_AUDIT.md': '93c861d807448d5ad9b2d85e9f645755430262f88a8ee2f496c67d6d74fdc4da'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def strict_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('nonfinite JSON value: ' + value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=invalid)

def inventory(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'root is not a real directory')
    names = set()
    with os.scandir(root) as entries:
        for entry in entries:
            require(stat.S_ISREG(entry.stat(follow_symlinks=False).st_mode),
                    'nonregular entry: ' + entry.name)
            names.add(entry.name)
    require(names == FILES, 'inventory mismatch')

def verify(root, receipt_path):
    inventory(root)
    require(root.resolve() not in receipt_path.resolve().parents, 'receipt must be external')
    require(stat.S_ISREG(receipt_path.lstat().st_mode), 'receipt must be regular')
    receipt = strict_json(receipt_path.read_bytes())
    require(receipt['schema'] == 1 and receipt['ordered_row'] == 1877 and
            receipt['problem_id'] == 30001258, 'wrong receipt identity')
    manifest_bytes = (root / 'MANIFEST.json').read_bytes()
    require(digest(manifest_bytes) == receipt['manifest_sha256'], 'external manifest pin mismatch')
    manifest = strict_json(manifest_bytes)
    require(set(manifest) == FILES - {'MANIFEST.json'}, 'manifest inventory mismatch')
    payload = {}
    for name, meta in manifest.items():
        require(set(meta) == {'bytes', 'sha256'}, 'manifest schema mismatch')
        require(type(meta['bytes']) is int and meta['bytes'] >= 0, 'invalid byte count')
        data = (root / name).read_bytes()
        require(len(data) == meta['bytes'] and digest(data) == meta['sha256'], 'payload mismatch: ' + name)
        payload[name] = data
    for name, expected in ANCHORS.items():
        require(digest(payload[name]) == expected, 'fixed original anchor mismatch')
    provenance = strict_json(payload['PROVENANCE.json'])
    require(provenance['schema'] == 1 and provenance['ordered_row'] == 1877 and
            provenance['problem_id'] == 30001258 and provenance['status'] == 'SCOPED PARTIAL', 'provenance identity/scope mismatch')
    require(provenance['mathematical_certificate'] is False and provenance['publication'] == 'none'
            and provenance['queue_edits'] is False, 'provenance scope mismatch')
    require(set(provenance['anchors']) == {'RESONANT_NODAL_ANALYSIS.md', 'INDEPENDENT_AUDIT.md',
            'SOURCE_GATE.md', 'PUBLIC_METADATA.json'}, 'provenance anchor coverage mismatch')
    for name, expected in provenance['anchors'].items():
        require(digest(payload[name]) == expected, 'provenance anchor mismatch')
    public = strict_json(payload['PUBLIC_METADATA.json'])
    require(public['problem_id'] == 30001258 and public['ordered_row'] == 1877,
            'public metadata identity mismatch')
    for entry in public['sources']:
        require(entry['url'].startswith('https://') and type(entry['bytes']) is int and entry['bytes'] > 0,
                'invalid public source metadata')
        require(len(entry['sha256']) == 64 and all(c in '0123456789abcdef' for c in entry['sha256']),
                'invalid public source hash')
    scripts = {name for name in payload if name.endswith('.py')}
    asts = strict_json(payload['AST_PROVENANCE.json'])
    require(set(asts) == scripts, 'AST coverage mismatch')
    for name in sorted(scripts):
        tree = ast.parse(payload[name].decode('utf-8'))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), 'assert-dependent check prohibited')
        require(ast.dump(tree, include_attributes=True) == asts[name], 'AST mismatch: ' + name)
    return {'status': 'PASS', 'ordered_row': 1877, 'problem_id': 30001258,
            'files': len(FILES), 'mathematical_certificate': False,
            'scope': 'byte integrity, inventory and recorded provenance only',
            'manifest_sha256': digest(manifest_bytes), 'python_optimized': bool(sys.flags.optimize)}

if __name__ == '__main__':
    try:
        require(len(sys.argv) == 3, 'usage: verify.py PACKAGE EXTERNAL_RECEIPT')
        print(json.dumps(verify(Path(sys.argv[1]), Path(sys.argv[2])), sort_keys=True))
    except Exception as error:
        print(json.dumps({'status': 'FAIL', 'error': str(error)}, sort_keys=True))
        sys.exit(1)
