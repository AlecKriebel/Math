#!/usr/bin/env python3
"""Fail-closed recursive inventory, guard equivalence, and complete output replay."""
import ast, hashlib, json, pathlib, shutil, stat, subprocess, sys, tempfile
ROOT=pathlib.Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(root):
    found={}
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'symlink forbidden: '+str(path))
        mode=path.lstat().st_mode
        require(stat.S_ISREG(mode) or stat.S_ISDIR(mode), 'nonregular entry')
        if path.is_dir():
            require(any(path.iterdir()), 'unlisted empty directory')
            continue
        name=path.relative_to(root).as_posix()
        if name=='MANIFEST.json':
            continue
        require(path.name!='MANIFEST.json', 'nested manifest forbidden')
        found[name]={'sha256':digest(path),'bytes':path.stat().st_size}
    return found

def verify_inventory(root):
    mp=root/'MANIFEST.json'
    require(mp.is_file() and not mp.is_symlink(),'missing or linked manifest')
    def pairs(items):
        d={}
        for k,v in items:
            require(k not in d,'duplicate JSON key')
            d[k]=v
        return d
    manifest=json.loads(mp.read_text(), object_pairs_hook=pairs)
    require(set(manifest)=={'schema','files'} and manifest['schema']==1,'manifest schema')
    for name, entry in manifest['files'].items():
        parts=pathlib.PurePosixPath(name).parts
        require(name and not name.startswith('/') and '\\' not in name and all(x not in ('..','.') for x in parts) and pathlib.PurePosixPath(name).as_posix()==name,'unsafe inventory path')
        require(name!='MANIFEST.json' and pathlib.PurePosixPath(name).name!='MANIFEST.json','manifest cannot list manifests')
        require(set(entry)=={'sha256','bytes'},'entry schema')
    require(inventory(root)==manifest['files'],'recursive inventory mismatch')

class Guard(ast.NodeTransformer):
    def visit_Assert(self,node):
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[] if node.msg is None else [node.msg],keywords=[]),cause=None)],orelse=[]),node)

def verify_equivalence(root):
    for name in ('checks.py','independent_audit.py'):
        expected=Guard().visit(ast.parse((root/'original'/name).read_text()))
        if name=='independent_audit.py':
            prefix=ast.parse("from pathlib import Path as _RequiredPath\nfor _required in ('certificate_N144.json', 'checks_results.json'):\n    if not _RequiredPath(__file__).with_name(_required).is_file():\n        raise FileNotFoundError(_required)\n")
            expected.body=prefix.body+expected.body
        actual=ast.parse((root/name).read_text())
        require(ast.dump(expected,include_attributes=False)==ast.dump(actual,include_attributes=False),'AST mismatch: '+name)
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(actual)),'optimization-sensitive assertion')

def replay(root):
    for optimize in (False,True):
        with tempfile.TemporaryDirectory() as td:
            dest=pathlib.Path(td)/'packet';shutil.copytree(root,dest)
            for name in ('checks.py','independent_audit.py'):
                command=[sys.executable]+(['-O'] if optimize else [])+[str(dest/name)]
                run=subprocess.run(command,cwd=td,capture_output=True,timeout=120)
                require(run.returncode==0 and not run.stderr,'replay execution failed: '+name)
                require(run.stdout==(root/'replay'/ (name+'.stdout')).read_bytes(),'full stdout mismatch: '+name)
                for output in ('checks_results.json','certificate_N144.json','independent_audit_results.json'):
                    require((dest/output).read_bytes()==(root/output).read_bytes(),'output file mismatch: '+output)
    print('PASS: complete normal/-O stdout and all JSON outputs match')

if __name__=='__main__':
    verify_inventory(ROOT)
    verify_equivalence(ROOT)
    replay(ROOT)
    print('PASS: recursive inventory and AST guard equivalence')
