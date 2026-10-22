"""Disclosed assertion-preserving AST adapter; execute only authenticated code."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('Use -I -S -B')
import ast,contextlib,io,json
from pathlib import Path
class Guards(ast.NodeTransformer):
    def __init__(self):self.count=0
    def visit_Assert(self,node):
        self.count+=1
        error=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[] if node.msg is None else [node.msg],keywords=[])
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=error,cause=None)],orelse=[]),node)
def compiled(source,name):
    tree=ast.parse(source,filename=name);adapter=Guards();tree=adapter.visit(tree);ast.fix_missing_locations(tree)
    return compile(tree,name,'exec',optimize=sys.flags.optimize),adapter.count
# A negative assertion must raise even in the actual optimized child interpreter.
code,n=compiled('assert False, "guard-negative-control"','<guard-self-test>')
try:exec(code,{})
except AssertionError as exc:
    if str(exc)!='guard-negative-control':raise RuntimeError('wrong guard failure')
else:raise RuntimeError('disabled guard')
if len(sys.argv)<2:raise SystemExit('Expected authenticated script path and optional arguments')
path=Path(sys.argv[1]);code,count=compiled(path.read_bytes(),str(path));sys.argv=sys.argv[1:]
buffer=io.StringIO()
with contextlib.redirect_stdout(buffer):exec(code,{'__name__':'__main__','__file__':str(path),'__package__':None})
print(json.dumps({'optimization':sys.flags.optimize,'assertions_rewritten':count,'negative_assertion_rejected':True,'stdout':buffer.getvalue()},sort_keys=True))
