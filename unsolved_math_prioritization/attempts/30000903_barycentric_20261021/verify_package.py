"""Offline integrity and optimization-safe replay of entire authored modules."""
import ast
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
SCRIPTS={'INDEPENDENT_CHECKS.py':'INDEPENDENT_CHECK_RESULTS.json','INDEPENDENT_RESIDUAL_CHECKS.py':'INDEPENDENT_RESIDUAL_RESULTS.json','verify_residual.py':'RESIDUAL_CHECK_RESULTS.txt'}
def digest(data): return hashlib.sha256(data).hexdigest()
def require(condition,message):
    if not condition: raise RuntimeError(message)
class ExplicitAssertions(ast.NodeTransformer):
    def visit_Assert(self,node):
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[node.msg] if node.msg is not None else [],keywords=[]),cause=None)],orelse=[]),node)
def transformed(source):
    return ast.fix_missing_locations(ExplicitAssertions().visit(ast.parse(source)))
def provenance(source):
    tree=ast.parse(source)
    return {'source_sha256':digest(source.encode()),'whole_module_ast_sha256':digest(ast.dump(tree,include_attributes=False).encode()),'assert_count':sum(isinstance(n,ast.Assert) for n in ast.walk(tree)),'transformed_whole_module_ast_sha256':digest(ast.dump(transformed(source),include_attributes=False).encode())}
def integrity():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    entries=manifest['files']; names=[e['file'] for e in entries]
    require(len(names)==len(set(names)),'duplicate inventory')
    require(all(Path(n).name==n and n not in ('.','..','MANIFEST.json') for n in names),'unsafe inventory name')
    actual=set()
    for p in ROOT.iterdir():
        require(p.is_file() and not p.is_symlink(),'nonregular inventory entry: '+p.name)
        actual.add(p.name)
    require(actual==set(names)|{'MANIFEST.json'},'inventory mismatch')
    for e in entries:
        data=(ROOT/e['file']).read_bytes()
        require(len(data)==e['bytes'] and digest(data)==e['sha256'],'hash mismatch: '+e['file'])
    expected=json.loads((ROOT/'AST_PROVENANCE.json').read_text())
    for name in SCRIPTS:
        require(provenance((ROOT/name).read_text())==expected[name],'AST provenance mismatch: '+name)
    print('PASS: exact regular-file inventory, byte hashes, and whole-module AST provenance.')
def no_network(event,args):
    if event.startswith('socket.'):
        raise RuntimeError('Network operation denied: '+event)
def execute(name,source):
    stream=io.StringIO()
    scope={'__name__':'__main__','__file__':str(ROOT/name)}
    with contextlib.redirect_stdout(stream):
        exec(compile(transformed(source),str(ROOT/name),'exec',optimize=0),scope)
    return stream.getvalue()
def replay():
    for name,result in SCRIPTS.items():
        actual=execute(name,(ROOT/name).read_text())
        expected=(ROOT/result).read_text()
        require(actual==expected,'full output mismatch: '+name)
        print('=== '+name+' full output ===')
        print(actual,end='')
        print('PASS: byte-for-byte saved output match.')
def mutations():
    cases=[('INDEPENDENT_CHECKS.py','ans += comb(n + 1, j + 1)','ans += comb(n, j)'),('INDEPENDENT_RESIDUAL_CHECKS.py','(1+lam*k)','(2+lam*k)'),('verify_residual.py','(2*x)**i','(3*x)**i'),('verify_residual.py','(d+1)*x','(d+2)*x'),('verify_residual.py','2*x*(1-x)*s.diff(h,x)','3*x*(1-x)*s.diff(h,x)')]
    for name,old,new in cases:
        original=(ROOT/name).read_text()
        require(original.count(old)==1,'mutation target ambiguity')
        try: execute(name,original.replace(old,new))
        except AssertionError: print('PASS: mathematical mutation rejected: '+name+': '+old+' -> '+new)
        else: raise RuntimeError('mutation survived: '+name+': '+old)
    import socket
    try: socket.socket()
    except RuntimeError as exc: require('Network operation denied' in str(exc),'unexpected socket failure')
    else: raise RuntimeError('socket guard failed')
    print('PASS: socket construction blocked.')
def main():
    sys.dont_write_bytecode=True
    sys.addaudithook(no_network)
    require(len(sys.argv)==2 and sys.argv[1] in ('--integrity','--replay','--mutations'),'choose --integrity, --replay or --mutations')
    integrity()
    if sys.argv[1]=='--replay': replay()
    if sys.argv[1]=='--mutations': mutations()
if __name__=='__main__': main()
