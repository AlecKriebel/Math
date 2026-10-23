import ast,hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
class Guards(ast.NodeTransformer):
 def visit_Assert(self,node):
  return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[node.msg] if node.msg else [],keywords=[]),cause=None)],orelse=[]),node)
a=(p/'verify_exact_original.py').read_bytes();b=(p/'verify_exact.py').read_bytes();prov=json.loads((p/'CONVERSION_PROVENANCE.json').read_text())
if hashlib.sha256(a).hexdigest()!=prov['original_sha256'] or hashlib.sha256(b).hexdigest()!=prov['converted_sha256']:raise RuntimeError('hash mismatch')
if ast.dump(Guards().visit(ast.parse(a)),include_attributes=False)!=ast.dump(ast.parse(b),include_attributes=False):raise RuntimeError('full AST mismatch')
if any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(b))):raise RuntimeError('assert remains')
print(json.dumps({'full_ast_equal':True,'hashes_match':True,'assert_nodes_converted':prov['assert_nodes_converted']},indent=2))
