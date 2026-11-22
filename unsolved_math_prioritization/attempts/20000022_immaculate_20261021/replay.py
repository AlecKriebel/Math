"""Fail-closed replay. Trust anchor: externally pinned manifest hash."""
import ast
import hashlib
import io
import contextlib
import json
import os
from pathlib import Path
import stat
import sys

BASE=Path(__file__).resolve().parent
NAMES={'REPORT.md','check.py','results.json','ORIGINAL_MANIFEST.json','audit/REVIEW.md','audit/independent_check.py','audit/independent_check.txt','audit/rerun_repaired.json','SOURCE_GATE.md','PUBLIC_SOURCE_METADATA.json','RESULT.md','check_regressions.py','replay.py','AST_PROVENANCE.json','MANIFEST.json','regressions.json'}
def need(ok,message):
    if not ok: raise ValueError(message)
def no_sockets(event,args):
    if event.startswith('socket.'): raise PermissionError('socket use denied')
sys.addaudithook(no_sockets)
sys.dont_write_bytecode=True

def inventory():
    found=set()
    # Never descend into a link, device, FIFO, or unexpected directory.
    for root,dirs,files in os.walk(BASE,followlinks=False):
        for name in dirs+files:
            p=Path(root)/name; rel=p.relative_to(BASE).as_posix(); mode=p.lstat().st_mode
            if stat.S_ISDIR(mode): need(rel=='audit','inventory unexpected directory before content read')
            else:
                need(stat.S_ISREG(mode),'inventory nonregular before content read')
                found.add(rel)
    need(found==NAMES,'inventory mismatch before content read')
inventory()
manifest=json.loads((BASE/'MANIFEST.json').read_text())
need(set(manifest['files'])==NAMES-{'MANIFEST.json'},'manifest inventory')
for name,record in manifest['files'].items():
    data=(BASE/name).read_bytes()
    need(len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256'],'payload mismatch: '+name)
provenance=json.loads((BASE/'AST_PROVENANCE.json').read_text())
need(set(provenance)=={n for n in NAMES if n.endswith('.py')},'AST inventory')
for name,digest in provenance.items():
    whole=ast.dump(ast.parse((BASE/name).read_text()),include_attributes=False)
    need(hashlib.sha256(whole.encode()).hexdigest()==digest,'whole-module AST mismatch: '+name)
if '--inventory-only' in sys.argv:
    print(json.dumps({'verdict':'PASS','inventory_files':len(NAMES)},sort_keys=True));sys.exit(0)

class ExplicitAssertions(ast.NodeTransformer):
    def visit_Assert(self,node):
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[node.msg or ast.Constant(value='explicit assertion failed')],keywords=[]),cause=None)],orelse=[]),node)

def run(name):
    tree=ast.parse((BASE/name).read_text(),filename=name)
    tree=ast.fix_missing_locations(ExplicitAssertions().visit(tree))
    out=io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(tree,str(BASE/name),'exec',optimize=sys.flags.optimize),{'__name__':'__main__','__file__':str(BASE/name)})
    return out.getvalue().encode()
reports={}
for script,expected in [('check.py','results.json'),('audit/independent_check.py','audit/independent_check.txt'),('check_regressions.py','regressions.json')]:
    actual=run(script);need(actual==(BASE/expected).read_bytes(),'exact output mismatch: '+script)
    reports[script]={'bytes':len(actual),'sha256':hashlib.sha256(actual).hexdigest()}
need((BASE/'results.json').read_bytes()==(BASE/'audit/rerun_repaired.json').read_bytes(),'repaired fixture mismatch')
for event in ['socket.__new__','socket.connect','socket.getaddrinfo']:
    blocked=False
    try: no_sockets(event,())
    except PermissionError: blocked=True
    need(blocked,'synthetic socket event not rejected')
print(json.dumps({'verdict':'PASS','optimized':sys.flags.optimize,'whole_modules':len(provenance),'inventory_files':len(NAMES),'reports':reports,'synthetic_socket_events_blocked':3,'actual_socket_calls':0},indent=2,sort_keys=True))
