#!/usr/bin/env python3
"""Inventory integrity, exact guarded-AST equivalence, and full result replay."""
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SUITES = {'check_partials.py': 'CHECK_RESULTS.json', 'independent_checks.py': 'independent_checks.json'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

class GuardAssertions(ast.NodeTransformer):
    def visit_Assert(self, node):
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(), operand=node.test), body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError', ctx=ast.Load()), args=[] if node.msg is None else [node.msg], keywords=[]), cause=None)], orelse=[]), node)

class RestoreAssertions(ast.NodeTransformer):
    def visit_If(self, node):
        # Only the canonical generated structure is reversed.
        if isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not) and not node.orelse and len(node.body)==1:
            r=node.body[0]
            if isinstance(r, ast.Raise) and r.cause is None and isinstance(r.exc, ast.Call) and isinstance(r.exc.func, ast.Name) and r.exc.func.id=='AssertionError' and not r.exc.keywords and len(r.exc.args)<=1:
                return ast.copy_location(ast.Assert(test=node.test.operand, msg=r.exc.args[0] if r.exc.args else None),node)
        return self.generic_visit(node)

def dump(tree):
    return ast.dump(tree, include_attributes=False)

def inventory():
    raw=(ROOT/'MANIFEST.json').read_text()
    m=json.loads(raw)
    require(set(m)=={'schema','files'}, 'unexpected manifest schema')
    require(m['schema']==1 and isinstance(m['files'],dict),'invalid manifest')
    expected=m['files']; allowed_dirs=set()
    for name, entry in expected.items():
        p=PurePosixPath(name)
        require(isinstance(name,str) and name and '\\' not in name and not p.is_absolute() and str(p)==name and all(x not in ('','.','..') for x in name.split('/')), 'unsafe manifest path')
        require(name!='MANIFEST.json','root manifest must not hash itself')
        require(isinstance(entry,dict) and set(entry)=={'sha256','bytes'},'bad entry')
        require(type(entry['bytes']) is int and entry['bytes']>=0 and isinstance(entry['sha256'],str) and len(entry['sha256'])==64 and all(x in '0123456789abcdef' for x in entry['sha256']), 'bad hash metadata')
        allowed_dirs.update(str(x) for x in p.parents if str(x)!='.')
    actual=set()
    for base,dirs,files in os.walk(ROOT,followlinks=False):
        for name in dirs+files:
            p=Path(base)/name; rel=p.relative_to(ROOT).as_posix()
            require(not p.is_symlink(),'symlink forbidden: '+rel)
            if p.is_dir():
                require(rel in allowed_dirs,'unexpected directory: '+rel)
            else:
                require(p.is_file(),'nonregular file: '+rel)
                if rel!='MANIFEST.json': actual.add(rel)
    require(actual==set(expected),'inventory mismatch')
    for name,entry in expected.items():
        b=(ROOT/name).read_bytes()
        require(len(b)==entry['bytes'] and hashlib.sha256(b).hexdigest()==entry['sha256'],'hash mismatch: '+name)

def equivalence():
    counts={}
    for name in SUITES:
        original=ast.parse((ROOT/'accepted_originals'/(name+'.txt')).read_text())
        guarded=ast.parse((ROOT/name).read_text())
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(guarded)), 'unguarded assertion')
        transformed=ast.fix_missing_locations(GuardAssertions().visit(ast.parse((ROOT/'accepted_originals'/(name+'.txt')).read_text())))
        require(dump(transformed)==dump(guarded),'forward AST mismatch: '+name)
        restored=RestoreAssertions().visit(guarded)
        require(dump(original)==dump(restored),'reverse AST mismatch: '+name)
        counts[name]=sum(isinstance(n,ast.Assert) for n in ast.walk(original))
    return counts

def replay():
    runs=[]
    for name,out in SUITES.items():
        expected=(ROOT/out).read_text()
        expected_stdout=expected if name=='check_partials.py' else json.dumps(json.loads(expected))+'\n'
        for flags in ([],['-O']):
            with tempfile.TemporaryDirectory(prefix='growth-four-') as td:
                script=Path(td)/name; script.write_bytes((ROOT/name).read_bytes())
                command=[sys.executable,*flags,'-B',str(script)]
                r=subprocess.run(command,cwd=td,text=True,capture_output=True,timeout=180)
                require(r.returncode==0, name+' failed: '+r.stderr)
                require(r.stderr=='','unexpected stderr')
                require(r.stdout==expected_stdout,'full stdout mismatch: '+name)
                require(json.loads(r.stdout)==json.loads(expected),'JSON mismatch')
                if name=='independent_checks.py':
                    require(script.with_name(out).read_text()==expected,'result file mismatch')
                runs.append({'suite':name,'optimized':bool(flags),'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'result':'PASS'})
    return runs

def main():
    inventory()
    guards=equivalence()
    if len(sys.argv)>1:
        require(sys.argv[1:]==['--inventory-only'],'unknown arguments')
        print(json.dumps({'inventory':'PASS','ast_guards':guards},sort_keys=True))
        return
    results=replay()
    print(json.dumps({'status':'PASS','inventory':'PASS','ast_guards':guards,'runs':results},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
