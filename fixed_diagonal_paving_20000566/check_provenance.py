"""Reconstruct full AST guard transformation and verify publication derivatives."""
import ast,hashlib,json
from pathlib import Path
class Guard(ast.NodeTransformer):
    def visit_Assert(self,node):
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError',ctx=ast.Load()),args=[ast.Constant(value='Exact check failed at original line '+str(node.lineno))],keywords=[]),cause=None)],orelse=[]),node)
def check(root):
    root=Path(root); data=json.loads((root/'CHECK_PROVENANCE.json').read_text())
    for row in data:
        original=(root/row['original']).read_bytes(); derived=(root/row['derived']).read_bytes()
        if hashlib.sha256(original).hexdigest()!=row['original_sha256'] or hashlib.sha256(derived).hexdigest()!=row['derived_sha256']:raise RuntimeError('provenance digest mismatch')
        tree=ast.parse(original); count=sum(isinstance(n,ast.Assert) for n in ast.walk(tree))
        expected=ast.dump(ast.fix_missing_locations(Guard().visit(tree)),include_attributes=False)
        actual=ast.dump(ast.parse(derived),include_attributes=False)
        if not (expected==actual==row['full_transformed_ast']==row['full_derived_ast'] and count==row['assertions_replaced'] and row['exact_full_ast_equal'] is True):raise RuntimeError('full AST provenance mismatch')
        if any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(derived))):raise RuntimeError('removable assertion')
    return {'status':'PASS','scripts':len(data),'full_AST_equivalence':True}
if __name__=='__main__':print(json.dumps(check(Path(__file__).parent),sort_keys=True))
