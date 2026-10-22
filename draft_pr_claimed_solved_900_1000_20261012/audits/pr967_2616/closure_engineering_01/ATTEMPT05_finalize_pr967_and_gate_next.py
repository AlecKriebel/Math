#!/usr/bin/env python3
"""PROPOSED PR967 local closure finalization; read-only unless --execute.

Authenticate both helpers before loading any repository dependency. This helper
never comments, closes, merges, deposits, appends a sheet, or changes native Git
queue/state/history. External pins/interpreter are trust roots, not a sandbox.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise RuntimeError('Use Python -I -S -B')
import argparse,base64,hashlib,json,os,re,stat,subprocess
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent
ROOT=P.parent
A=P/'audits/pr967_2616'
PR=967
KEY='2616'
HEAD='b356dec5cb01e5f536b9cfeece56ad08844c03cb'
HELPERS=['close_pr967.py','finalize_pr967_and_gate_next.py']
MAX=32*1024*1024
MAX_JSON=8*1024*1024
def need(ok,message):
    if not ok:raise RuntimeError('PR967 closure guard: '+message)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def pin(raw):return {'bytes':len(raw),'sha256':sha(raw)}
def enc(value):return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
def now():return datetime.now(timezone.utc).isoformat()
def utc(value):
    need(type(value) is str,'timestamp string')
    result=datetime.fromisoformat(value.replace('Z','+00:00'))
    need(result.tzinfo is not None and result.utcoffset().total_seconds()==0,'explicit UTC timestamp')
    return result

def exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b

def strict(raw):
    def pairs(items):
        out={}
        for k,v in items:need(k not in out,'duplicate JSON key');out[k]=v
        return out
    def bad(x):raise RuntimeError('Nonfinite JSON: '+x)
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)

def safe(name):
    return (type(name) is str and bool(name) and '\\' not in name and '\0' not in name
        and not PurePosixPath(name).is_absolute() and PurePosixPath(name).as_posix()==name
        and all(x not in ('','.','..') for x in name.split('/')))

def fingerprint(value):
    need(type(value) is dict and set(value)=={'bytes','sha256'} and type(value['bytes']) is int
        and 0<=value['bytes']<=MAX and type(value['sha256']) is str
        and re.fullmatch('[0-9a-f]{64}',value['sha256']),'exact bounded fingerprint')

def digest(value):need(type(value) is str and re.fullmatch('[0-9a-f]{64}',value),'SHA256 string')
def oid(value):need(type(value) is str and re.fullmatch('[0-9a-f]{40}',value),'Git object identity')
def fields(value,types,label):
    need(type(value) is dict and set(types)<=set(value),label+' mandatory fields')
    for k,t in types.items():need(type(value[k]) is t,label+' type '+k)

def directory(path):
    name=Path(path).relative_to(ROOT).as_posix();need(safe(name),'directory scope')
    fd=os.open(ROOT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        for part in name.split('/'):
            child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
            os.close(fd);fd=child
        return os.dup(fd)
    finally:os.close(fd)

def read(path,expected=None,cap=MAX):
    path=Path(path);name=path.relative_to(ROOT).as_posix();need(safe(name),'read path scope')
    if expected is not None:fingerprint(expected);cap=expected['bytes']
    fd=directory(path.parent)
    try:
        handle=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        try:
            info=os.fstat(handle);need(stat.S_ISREG(info.st_mode) and info.st_size<=cap,'regular bounded input: '+name)
            blocks=[];total=0
            while total<=cap:
                block=os.read(handle,min(1024*1024,cap+1-total))
                if not block:break
                blocks.append(block);total+=len(block)
            raw=b''.join(blocks);need(len(raw)<=cap,'input grew: '+name)
            if expected is not None:need(pin(raw)==expected,'input fingerprint changed: '+name)
            return raw
        finally:os.close(handle)
    finally:os.close(fd)

def exists(path):
    try:read(path,cap=MAX_JSON);return True
    except FileNotFoundError:return False

def save(path,value):
    """Exclusive durable receipt; no silent overwrite or following ancestors."""
    raw=enc(value);need(len(raw)<=MAX_JSON,'receipt size cap');fd=directory(Path(path).parent)
    try:
        handle=os.open(Path(path).name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_NONBLOCK,0o600,dir_fd=fd)
        with os.fdopen(handle,'wb') as stream:
            need(stream.write(raw)==len(raw),'receipt short write');stream.flush();os.fsync(stream.fileno())
        os.fsync(fd)
    finally:os.close(fd)

def load(path):return strict(read(path,cap=MAX_JSON))


def inventory(expected):
    digest(expected);raw=read(A/'CLOSURE_OPERATIONS_INVENTORY.json');need(sha(raw)==expected,'external two-helper operations inventory')
    doc=strict(raw);need(type(doc) is dict and set(doc)=={'schema','pr','problem_id','original_pr_head','files'} and doc['schema']=='pr967-closure-operations-v1' and type(doc['pr']) is int and doc['pr']==PR and doc['problem_id']==KEY and doc['original_pr_head']==HEAD,'operations target/schema')
    names={(P/n).relative_to(ROOT).as_posix() for n in HELPERS};need(type(doc['files']) is dict and set(doc['files'])==names,'entire two-helper inventory')
    captured={name:read(ROOT/name,expected=value) for name,value in doc['files'].items()}
    return {'inventory_sha256':expected,'inventory':doc,'captured':captured}


def entry(action):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operations-sha256',required=True);parser.add_argument('--disposition-sha256',required=True);parser.add_argument('--execute',action='store_true');parser.add_argument('--approval-sha256')
    args=parser.parse_args();context=inventory(args.operations_sha256)
    bundle={'action':action,'args':vars(args),'inventory_sha256':context['inventory_sha256'],'inventory':context['inventory'],'captured':{k:base64.b64encode(v).decode() for k,v in context['captured'].items()}}
    bootstrap=('import argparse,base64,json,sys; b=json.loads(sys.stdin.buffer.read()); '
      'c={"inventory_sha256":b["inventory_sha256"],"inventory":b["inventory"],"captured":{k:base64.b64decode(v,validate=True) for k,v in b["captured"].items()}}; '
      'n={"__name__":"_pr967_authenticated_core_","__file__":sys.argv[1]}; '
      'exec(compile(c["captured"][sys.argv[2]],sys.argv[1],"exec",dont_inherit=True,optimize=0),n); '
      'n["operation"](b["action"],argparse.Namespace(**b["args"]),c)')
    result=subprocess.run([sys.executable,'-I','-S','-B','-c',bootstrap,str(P/'close_pr967.py'),(P/'close_pr967.py').relative_to(ROOT).as_posix()],cwd=ROOT,input=json.dumps(bundle).encode())
    raise SystemExit(result.returncode)

if __name__=='__main__':entry('finalize')
