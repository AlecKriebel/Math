#!/usr/bin/env python3
"""Run unchanged audit B without its two source-PDF identity checks.

The original script is hash-pinned and never rewritten. Only its single top-level
source_expected loop is omitted in an in-memory AST. Every other node executes.
This adapter does not claim source retrieval, source inspection, or 675 checks.
"""
import argparse, ast, hashlib, json, sys
from pathlib import Path

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--manuscript', required=True, type=Path)
parser.add_argument('--output', required=True, type=Path)
args = parser.parse_args()
source = Path(__file__).resolve().parent / 'audit_b' / 'independent_checks.py'
data = source.read_bytes()
require(hashlib.sha256(data).hexdigest() == '77cd7b1d12bae0c6d31d59c63876b88149328c8d5300523ec0f72c14a068ce28', 'Audit B script is not the accepted freeze')
tree = ast.parse(data, filename=str(source))
omitted = []
for node in tree.body:
    if isinstance(node, ast.For) and isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Attribute) and isinstance(node.iter.func.value, ast.Name) and node.iter.func.value.id == 'source_expected' and node.iter.func.attr == 'items':
        omitted.append(node)
require(len(omitted) == 1, 'Expected exactly one source identity loop')
tree.body.remove(omitted[0])
namespace = {'__file__': str(source), '__name__': '__main__'}
sys.argv = [str(source), '--manuscript', str(args.manuscript.resolve()), '--output', str(args.output.resolve())]
exec(compile(tree, str(source), 'exec'), namespace)
result = json.loads(args.output.read_bytes())
require(result['status'] == 'PASS' and result['checks'] == 673 and result['failed'] == 0, 'Unexpected source-free control outcome')
require(not any(x['name'].startswith('independently_retrieved_') for x in result['results']), 'Source check was unexpectedly reported')
result['source_free_replay'] = {'original_full_check_count': 675, 'executed_check_count': 673, 'omitted_source_identity_checks': ['meier_vikman_wenger_v1.pdf', 'owr_2025_30.pdf'], 'source_retrieval_performed': False, 'source_inspection_performed': False, 'original_script_unchanged': True}
args.output.write_text(json.dumps(result, indent=2) + '\n')
