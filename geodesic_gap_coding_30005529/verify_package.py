from pathlib import Path
import ast, hashlib, json, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parent

def require(ok, message):
    if not ok: raise RuntimeError(message)

def inventory(root=ROOT):
    files={}
    for f in root.rglob('*'):
        require(not f.is_symlink(), 'symlink rejected')
        if f.is_file():
            rel=f.relative_to(root).as_posix()
            if rel=='MANIFEST.json': continue
            require(f.name!='MANIFEST.json', 'nested manifest rejected')
            files[rel]={'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
    return files

class Harden(ast.NodeTransformer):
    def visit_Assert(self,n):
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=n.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[n.msg or ast.Constant(value='exact check failed')],keywords=[]),cause=None)],orelse=[]),n)

def provenance():
    # Parse AST dump via a restricted constructor namespace, never eval arbitrary names.
    import builtins
    constructors={name:getattr(ast,name) for name in dir(ast) if isinstance(getattr(ast,name),type) and issubclass(getattr(ast,name),ast.AST)}
    for e in json.loads((ROOT/'AST_PROVENANCE.json').read_text()):
        dump=e['relocated_original_ast']
        expression=ast.parse(dump,mode='eval')
        def decode(n):
            if isinstance(n,ast.Constant): return n.value
            if isinstance(n,ast.List): return [decode(x) for x in n.elts]
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in constructors:
                return constructors[n.func.id](**{k.arg:decode(k.value) for k in n.keywords})
            raise RuntimeError('invalid AST provenance encoding')
        old=decode(expression.body)
        require(sum(isinstance(n,ast.Assert) for n in ast.walk(old))==e['assertions_replaced'],'assertion count mismatch')
        new=Harden().visit(old); ast.fix_missing_locations(new)
        normalized=ast.unparse(new).replace("Path(__file__).with_name('exact_audit_results.json')", "Path('exact_audit_results.json')")
        actual=ast.parse((ROOT/e['script']).read_text())
        require(ast.dump(ast.parse(normalized),include_attributes=False)==ast.dump(actual,include_attributes=False)==e['hardened_ast'],'AST transformation mismatch')
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(actual)), 'unsafe assert remains')

def replay():
    for e in json.loads((ROOT/'AST_PROVENANCE.json').read_text()):
        for flags in [[],['-O']]:
            with tempfile.TemporaryDirectory() as d:
                run=subprocess.run([sys.executable,*flags,str(ROOT/e['script'])],cwd=d,capture_output=True,text=True)
                require(run.returncode==0 and run.stderr=='','script failed: '+e['script'])
                expected=ROOT/e['expected']
                require((Path(d)/expected.name).read_bytes()==expected.read_bytes(),'complete result mismatch')
                require(run.stdout==(ROOT/e['expected'].replace('.json','.stdout.txt')).read_text(),'complete stdout mismatch')

def main():
    expected=json.loads((ROOT/'MANIFEST.json').read_text())['files']
    require(inventory()==expected,'inventory or hash mismatch')
    provenance(); replay()
    print('PASS: exact inventory, AST provenance, complete normal/-O results and stdout')
if __name__=='__main__':main()
