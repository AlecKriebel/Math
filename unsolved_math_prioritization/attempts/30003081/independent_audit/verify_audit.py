#!/usr/bin/env python3
"""Verify this source-free audit against a separately supplied manifest pin and replay its mathematics."""
import argparse,ast,hashlib,json,re,stat,subprocess,sys,tempfile
from pathlib import Path

class InvalidAudit(Exception):
    pass

def require(value,message):
    if not value: raise InvalidAudit(message)

def pairs(entries):
    result={}
    for key,value in entries:
        require(key not in result,'duplicate JSON key')
        result[key]=value
    return result

def check(root,pin):
    require(root.is_dir() and not root.is_symlink(),'nonregular root')
    require(re.fullmatch('[0-9a-f]{64}',pin) is not None,'bad external pin')
    manifest=root/'MANIFEST.json'
    require(stat.S_ISREG(manifest.lstat().st_mode),'nonregular manifest')
    raw=manifest.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==pin,'manifest does not match external pin')
    obj=json.loads(raw,object_pairs_hook=pairs)
    require(type(obj) is dict and set(obj)=={'schema','files'},'manifest shape')
    require(obj['schema']=='source-free-independent-audit-v1' and type(obj['files']) is list,'schema or inventory type')
    inventory={'MANIFEST.json'}
    for entry in obj['files']:
        require(type(entry) is dict and set(entry)=={'path','bytes','sha256'},'entry shape')
        name=entry['path']
        require(type(name) is str and re.fullmatch('[A-Za-z0-9_.-]+',name) is not None and name not in {'.','..'},'unsafe path')
        require(name not in inventory,'duplicate path')
        inventory.add(name)
        require(type(entry['bytes']) is int and entry['bytes']>=0,'bad size')
        require(type(entry['sha256']) is str and re.fullmatch('[0-9a-f]{64}',entry['sha256']) is not None,'bad digest')
        path=root/name
        require(stat.S_ISREG(path.lstat().st_mode),'nonregular payload')
        raw=path.read_bytes()
        require(len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256'],'payload mismatch: '+name)
        if name.endswith('.py'):
            require(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse(raw))),'assert in executable')
    require({p.name for p in root.iterdir()}==inventory,'unexpected or missing member')
    mode=sys.flags.optimize
    require(mode in (0,1,2),'unsupported optimization')
    flags=[] if mode==0 else ['-O' if mode==1 else '-OO']
    with tempfile.TemporaryDirectory(prefix='audit-replay-') as cwd:
        program='import runpy,sys\nif sys.flags.optimize!='+str(mode)+': raise RuntimeError("wrong child optimization")\npath=sys.argv[1];sys.argv=[path];runpy.run_path(path,run_name="__main__")'
        result=subprocess.run([sys.executable,*flags,'-I','-B','-c',program,str((root/'independent_math.py').resolve())],cwd=cwd,capture_output=True,timeout=60)
    require(result.returncode==0,'independent mathematics failed')
    require(result.stdout==(root/'INDEPENDENT_MATH_RESULTS.json').read_bytes(),'independent output mismatch')
    return {'status':'PASS','optimization':mode,'payload_files':len(obj['files']),'manifest_sha256':pin,
            'source_bytes':'NOT_RUN: intentionally absent','scope':'Integrity and finite mathematical replay only; written review remains separate.'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--manifest-sha256',required=True)
    args=parser.parse_args()
    try: result=check(args.root,args.manifest_sha256)
    except (InvalidAudit,ValueError,TypeError,KeyError,OSError,SyntaxError,subprocess.SubprocessError) as error:
        print('REJECT: '+str(error),file=sys.stderr);return 1
    print(json.dumps(result,sort_keys=True));return 0

if __name__=='__main__':
    sys.exit(main())
