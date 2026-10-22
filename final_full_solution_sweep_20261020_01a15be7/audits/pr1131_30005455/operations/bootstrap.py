#!/usr/bin/env python3
"""Reviewed source-only loader. External launcher must hash this file before exec.
Trust boundary: isolated Python standard library; all project code is checked in
memory before any project module executes. Never imports project .py/.pyc normally.
"""
import argparse
import builtins
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import types

MODULE_FILES={'ops_common':'ops_common.py','collect_live':'collect_live.py',
              'integrate_remote':'integrate_remote.py','publish_and_ledger':'publish_and_ledger.py',
              'native_policy':'native_policy.py','check_package':'check_package.py',
              'offline_controls':'offline_controls.py','full_controls':'full_controls.py','prepare_offline':'prepare_offline.py'}
ENTRIES={'check_package','collect_live','integrate_remote','publish_and_ledger','offline_controls','full_controls','prepare_offline'}
EXCLUDED=['OPERATIONS_MANIFEST.json','private/','runtime/','__pycache__/']

def need(ok,message):
    if not ok:raise RuntimeError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def strict(data):
    def pairs(items):
        result={}
        for k,v in items:
            need(k not in result,'Duplicate bootstrap JSON key');result[k]=v
        return result
    return json.loads(data,object_pairs_hook=pairs)
def safe(root,name):
    need(isinstance(name,str) and name and not any(c in name for c in ['\\',':','\0']),'Unsafe bootstrap path')
    p=PurePosixPath(name)
    need(not p.is_absolute() and p.as_posix()==name and all(c not in {'','.','..'} for c in name.split('/')),'Unsafe bootstrap path')
    need(not root.is_symlink() and not any(root.joinpath(*p.parts[:i]).is_symlink() for i in range(1,len(p.parts)+1)),'Bootstrap symlink rejected')
    return root/name

def public_files(root):
    result=set()
    for parent,dirs,names in os.walk(root,followlinks=False):
        selected=[]
        for name in dirs:
            if name in {'private','runtime','__pycache__'}:continue
            need(not (Path(parent)/name).is_symlink(),'Public closure directory symlink')
            selected.append(name)
        dirs[:]=selected
        for name in names:
            path=Path(parent)/name;relative=path.relative_to(root).as_posix()
            if relative=='OPERATIONS_MANIFEST.json':continue
            need(not path.is_symlink() and path.is_file(),'Public closure entry is not a regular file')
            result.add(relative)
    return result

def load_verified(operations,operations_sha,bootstrap_sha):
    """No project code executes until the entire source/data closure verifies."""
    need(sys.flags.isolated and sys.flags.no_site,'Use an isolated -I -S interpreter')
    operations=Path(operations).resolve()
    for value in [operations_sha,bootstrap_sha]:need(isinstance(value,str) and len(value)==64 and all(c in '0123456789abcdef' for c in value),'External SHA anchors required')
    boot=operations/'bootstrap.py';bootbytes=boot.read_bytes();need(sha(bootbytes)==bootstrap_sha,'Externally pinned bootstrap changed')
    manifestbytes=(operations/'OPERATIONS_MANIFEST.json').read_bytes();need(sha(manifestbytes)==operations_sha,'External operations anchor changed')
    manifest=strict(manifestbytes);need(manifest['excluded']==EXCLUDED,'Bootstrap exclusion policy changed')
    files=manifest['files'];need(isinstance(files,dict) and files,'Empty operation closure')
    actual=public_files(operations)
    need(actual==set(files),'Operations closure changed before code load')
    checked={}
    for name,pin in files.items():
        data=safe(operations,name).read_bytes()
        need(pin=={'bytes':len(data),'sha256':sha(data)},'Operation payload changed before code load: '+name);checked[name]=data
    need(checked['bootstrap.py']==bootbytes,'Bootstrap differs from closed source bundle')
    dependencies=strict(checked['DEPENDENCY_PINS.json']);need(set(dependencies)=={'zenodo_deposit_tool/zenodo.py'},'Unexpected shared code dependency')
    repo=operations.parents[3];sources={name:(operations/filename,checked[filename]) for name,filename in MODULE_FILES.items()}
    for path,pin in dependencies.items():
        data=safe(repo,path).read_bytes();need(pin=={'bytes':len(data),'sha256':sha(data)},'Shared dependency changed before any code load')
        sources['zenodo']=(repo/path,data)
    # sys.modules and filesystem import caches never select project code here.
    modules={};loading=set();original_import=builtins.__import__
    context={'operations_sha256':operations_sha,'bootstrap_sha256':bootstrap_sha,'operations_dir':str(operations)}
    def guarded_import(name,globals=None,locals=None,fromlist=(),level=0):
        need(level==0,'Relative project imports forbidden')
        if name in sources:return load(name)
        root=name.split('.',1)[0]
        need(root in sys.stdlib_module_names or root in sys.builtin_module_names,'Unsealed/nonstdlib import forbidden: '+name)
        return original_import(name,globals,locals,fromlist,level)
    def load(name):
        need(name in sources,'Unknown sealed module')
        if name in modules:return modules[name]
        need(name not in loading,'Circular project module import')
        loading.add(name);path,data=sources[name]
        module=types.ModuleType(name);module.__file__=str(path);module.__package__=''
        module.__dict__.update(_PR1131_SOURCE_VERIFIED=True,_PR1131_EXECUTION=dict(context),_PR1131_BOOTSTRAP=load_verified)
        module.__dict__['__builtins__']={**vars(builtins),'__import__':guarded_import}
        # compile exactly the already checked bytes; never a .pyc, loader-selected
        # source, or a second filesystem read. Only trusted stdlib uses normal imports.
        exec(compile(data,str(path),'exec',dont_inherit=True),module.__dict__)
        loading.remove(name);modules[name]=module;return module
    return load,context

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operations-dir',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--bootstrap-sha256',required=True);parser.add_argument('--operations-sha256',required=True)
    parser.add_argument('entry',choices=sorted(ENTRIES));parser.add_argument('entry_args',nargs=argparse.REMAINDER)
    args=parser.parse_args();load,_=load_verified(args.operations_dir,args.operations_sha256,args.bootstrap_sha256)
    module=load(args.entry);sys.argv=[module.__file__,*args.entry_args]
    result=module.main()
    if isinstance(result,int):raise SystemExit(result)
if __name__=='__main__':main()
