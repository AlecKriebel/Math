#!/usr/bin/env python3
"""Externally authenticate this bootstrap before execution; it pins the manifest."""
import hashlib,json,os,re,stat,subprocess,sys,tempfile
from pathlib import Path
PIN='45f641b37f6e58df37729e194076c2512cdc77ce12faa7c7c937dd6fc09195fa'
class Reject(Exception):pass
def need(ok,msg):
    if not ok:raise Reject(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(items):
    d={}
    for k,v in items:need(k not in d,'duplicate JSON key');d[k]=v
    return d
def constant(x):raise Reject('nonfinite JSON')
def read_regular(p,max_size):
    st=p.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'nonregular, symbolic or hard link: '+p.name)
    need(st.st_size<=max_size,'file too large')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        fst=os.fstat(fd);need((fst.st_dev,fst.st_ino)==(st.st_dev,st.st_ino),'changed file before read')
        with os.fdopen(fd,'rb',closefd=False) as f:b=f.read(max_size+1)
        aft=os.fstat(fd);need((fst.st_size,fst.st_mtime_ns,fst.st_ctime_ns)==(aft.st_size,aft.st_mtime_ns,aft.st_ctime_ns),'file changed during read')
    finally:os.close(fd)
    need(len(b)<=max_size and len(b)==st.st_size,'size mismatch during read');return b
def run():
    need(len(sys.argv)==1,'no arguments accepted')
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'run with -I -S -B')
    here=Path(__file__).absolute().parent;need(not here.is_symlink() and here.is_dir(),'invalid root')
    need(set(p.name for p in here.iterdir())=={'bootstrap.py','AUTHOR_MANIFEST.json','packet'},'outer inventory mismatch')
    root=here/'packet';need(root.is_dir() and not root.is_symlink(),'invalid packet directory')
    raw=read_regular(here/'AUTHOR_MANIFEST.json',1000000);need(sha(raw)==PIN,'manifest trust anchor mismatch')
    m=json.loads(raw,object_pairs_hook=pairs,parse_constant=constant)
    need(type(m) is dict and set(m)=={'schema','problem_id','status','approaches','files'},'manifest keys')
    need(m['schema']=='positive-twist-manifest-v1' and type(m['problem_id']) is int and m['problem_id']==11000112,'manifest identity')
    need(m['status']=='prior-negative' and type(m['approaches']) is int and m['approaches']==0,'manifest disposition')
    need(type(m['files']) is list and 1<=len(m['files'])<=100,'manifest files')
    snapshot={};total=0
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry keys');name=e['path']
        need(type(name) is str and re.fullmatch('[A-Za-z0-9_.-]+',name) and name not in ('.','..'),'unsafe path')
        need(name not in snapshot,'duplicate path');need(type(e['bytes']) is int and 0<=e['bytes']<=2000000,'bad size')
        need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']),'bad digest')
        b=read_regular(root/name,2000000);need(len(b)==e['bytes'] and sha(b)==e['sha256'],'payload mismatch: '+name)
        snapshot[name]=b;total+=len(b);need(total<=16000000,'oversized payload')
    need(set(p.name for p in root.iterdir())==set(snapshot),'payload inventory mismatch')
    # No payload imports or code execution occurs before every byte is authenticated.
    flags=[] if sys.flags.optimize==0 else (['-O'] if sys.flags.optimize==1 else ['-OO'])
    with tempfile.TemporaryDirectory(prefix='positive-twist-verified-') as td:
        target=Path(td)
        for name,b in snapshot.items():(target/name).write_bytes(b)
        for name in snapshot:(target/name).chmod(0o444)
        r=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(target/'verify.py')],cwd=target,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
        need(r.returncode==0,'diagnostic failure: '+r.stderr.decode('utf-8','replace'))
        need(r.stdout==snapshot['DIAGNOSTICS.json'],'diagnostic output mismatch')
    return {'schema':'positive-twist-bootstrap-v1','status':'PASS','manifest_sha256':PIN,'payload_files':len(snapshot),'payload_bytes':total,'diagnostics_sha256':sha(snapshot['DIAGNOSTICS.json']),'source_rehash':'NOT_RUN','corpus_rehash':'NOT_RUN'}
if __name__=='__main__':
    try:print(json.dumps(run(),sort_keys=True,separators=(',',':')))
    except (Reject,OSError,ValueError,TypeError,KeyError,RecursionError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
