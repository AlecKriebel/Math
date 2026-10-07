#!/usr/bin/env python3
"""Execute a frozen script with assertions effective in normal and optimized mode.
Only AST Assert nodes are rewritten; original source bytes are never modified.
Nested Python children inherit the actual optimization mode explicitly.
"""
import ast,json,subprocess,sys
from pathlib import Path
p=Path(sys.argv[1]).resolve(); sys.argv=sys.argv[1:]
class Harden(ast.NodeTransformer):
    count=0
    def visit_Assert(self,node):
        self.count+=1
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[] if node.msg is None else [node.msg],keywords=[]),cause=None)],orelse=[]),node)
h=Harden(); tree=ast.fix_missing_locations(h.visit(ast.parse(p.read_text(),filename=str(p))))
real_run=subprocess.run; modes=[]
def run(args,*a,**kw):
    args=list(args)
    if args and args[0]==sys.executable:
        flags=['-I','-B']+(['-O'] if sys.flags.optimize else [])
        args=[args[0],*flags,*args[1:]]
        if '-c' in args:
            index=args.index('-c')+1
            args[index]='import sys as _mode_sys; import json as _mode_json; print("CHILD_MODE="+_mode_json.dumps({"optimize":_mode_sys.flags.optimize}),file=_mode_sys.stderr)\n'+args[index]
        result=real_run(args,*a,**kw)
        stderr=result.stderr.decode() if isinstance(result.stderr,bytes) else result.stderr
        markers=[json.loads(x.split('=',1)[1])['optimize'] for x in (stderr or '').splitlines() if x.startswith('CHILD_MODE=')]
        if markers!=[sys.flags.optimize]:raise RuntimeError('Nested child optimization mode mismatch')
        modes.extend(markers)
        return result
    return real_run(args,*a,**kw)
subprocess.run=run
exec(compile(tree,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
print('REPLAY_MODE='+json.dumps({'optimize':sys.flags.optimize,'assertions_hardened':h.count,'nested_child_modes':modes}),file=sys.stderr)
