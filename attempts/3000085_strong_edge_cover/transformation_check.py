"""Exact whole-module provenance check, independent of assert optimization."""
import ast
import hashlib
import json
from pathlib import Path

def verify(root):
    original = (root / 'regression.original.txt').read_bytes()
    hardened = (root / 'regression.py').read_bytes()
    receipt = json.loads((root / 'CHECKER_TRANSFORMATION.json').read_text())
    tree = ast.parse(original)
    assertions = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    guard = tree.body[4]
    expected_guard = ast.parse('if not __debug__:\n    raise RuntimeError("Run without -O: assertions are required for this regression.")').body[0]
    if ast.dump(guard, include_attributes=False) != ast.dump(expected_guard, include_attributes=False):
        raise RuntimeError('Original guard mismatch')
    if len(assertions) != 7:
        raise RuntimeError('Unexpected assertion count')
    lines = [n.lineno for n in assertions]
    class Transform(ast.NodeTransformer):
        def visit_Assert(self, node):
            number = assertions.index(node) + 1
            return ast.If(test=ast.UnaryOp(op=ast.Not(), operand=node.test), body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError', ctx=ast.Load()), args=[ast.Constant(value=f'regression check {number} failed')], keywords=[]), cause=None)], orelse=[])
        def visit_If(self, node):
            return None if node is guard else self.generic_visit(node)
    expected = ast.dump(Transform().visit(tree), include_attributes=False)
    parsed = ast.parse(hardened)
    actual = ast.dump(parsed, include_attributes=False)
    if expected != actual or any(isinstance(n, ast.Assert) for n in ast.walk(parsed)):
        raise RuntimeError('Whole-module transformation mismatch')
    calculated = dict(original_sha256=hashlib.sha256(original).hexdigest(), hardened_sha256=hashlib.sha256(hardened).hexdigest(), assertions_replaced=7, assertion_original_lines=lines, optimized_guard_removed=True, whole_module_expected_ast_equals_hardened_ast=True, expected_ast_sha256=hashlib.sha256(expected.encode()).hexdigest(), hardened_ast_sha256=hashlib.sha256(actual.encode()).hexdigest(), policy='Only replace each Assert(test) by if not test: raise AssertionError with numbered diagnostic; remove exact original not __debug__ guard. No other AST changes.')
    if receipt != calculated:
        raise RuntimeError('Transformation receipt mismatch')
    return calculated

if __name__ == '__main__':
    verify(Path(__file__).resolve().parent)
    print('Whole-module AST transformation verified; seven explicit checks; no residual asserts.')
