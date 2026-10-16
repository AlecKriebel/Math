#!/usr/bin/env python3
"""PR952 closed source-free finite verification. Use Python -I -S -B.

Authenticate this verifier externally BEFORE executing it. Supply a separately
obtained manifest SHA256; a colocated mutable sidecar is not authority.
Installed Python/stdlib/host and nonconcurrent inputs remain trust roots.
"""
import sys
if not (sys.flags.isolated == 1 and sys.flags.no_site == 1 and sys.dont_write_bytecode):
    raise SystemExit('PROFILE_STARTUP: Python -I -S -B is required')
import argparse,hashlib,io,json,os,re,stat,subprocess,tempfile,threading,time,zipfile
from pathlib import Path,PurePosixPath
HEAD='989a532ae1d50894190d010a0a02ba8c3d71ee05'
PREFIX='original/unsolved_math_prioritization/attempts/10400145/'
MATH='checks/independent_math.py'
MATH_SHA='ff44cdce74d36b40995843f7bc450e31fcac532163f3a411da51f3244ea82601'
MANIFEST='PACKAGE_MANIFEST.json'
SCHEMA='pr952-sourcefree-package-v1'
MAX_FILES,MAX_DIRS,MAX_DEPTH=1024,256,16
MAX_FILE_BYTES,MAX_TOTAL_BYTES,MAX_MANIFEST_BYTES=16*1024**2,64*1024**2,512*1024
MAX_ZIP_MEMBERS,MAX_ZIP_BYTES,MAX_ZIP_RATIO=1280,32*1024**2,200
HEX64=re.compile(r'[0-9a-f]{64}\Z')
# ORIGINAL_PINS is generated solely from authenticated ORIGINAL_FILE_RECORDS.json.
ORIGINAL_PINS={'BIBLIOGRAPHIC_CORRECTION.patch': {'bytes': 1960, 'sha256': 'dd133cee1c11de3a452bd2aae8f89f415550d37473f8caf624c723c4546aab72', 'git_blob': '07e4713ba957abcc2cf3ea29a4001b9670914b4d'}, 'BOOTSTRAP.py': {'bytes': 1493, 'sha256': '72378da263ab077353da81c68c3d890ad1eafdeba170c3e450d3b1ccd4b72ad3', 'git_blob': 'd917e4a60059458c40685bdf91c98eeb1c11e3c6'}, 'CORPUS_VERIFICATION.json': {'bytes': 827, 'sha256': '097f3a2cd2559a5d1d33e43c471a603348201704952ac31c0f25af4c4294c21c', 'git_blob': '524b179d947377268553a715124cfb069ecad09e'}, 'EXTERNAL_PINS.json': {'bytes': 406, 'sha256': 'bc4624415f0ce8a57cd734c164cbf1f7fe044654080142cc5f326351d35a467c', 'git_blob': '3edd054100500de322d0814a665600c7f3897fd7'}, 'FINAL_AUDIT_MANIFEST.json': {'bytes': 810, 'sha256': '2ba36792f0aabd6afc082e3b70e0327d2018c3640715834e3dc32c2276a14aa9', 'git_blob': 'a3e21a1680ad56e985e92fefda0ae9b81d80284a'}, 'METADATA_TIMESTAMP_CORRECTION.patch': {'bytes': 506, 'sha256': 'e0814ab9afd06211c39093f3b32f9fd9dac88a4485ed8c87108c8f7c76028bcb', 'git_blob': '043e73519dde41e5d013105c0c8c7822d3ed0375'}, 'PUBLICATION_MANIFEST.json': {'bytes': 5162, 'sha256': 'e5748a840564410c91e0c4268415a802401a642f7b484494d9e0daa8831160cb', 'git_blob': '2f9a3953311eaa73d3f1b0c0b2a54cff90c4dae3'}, 'README.md': {'bytes': 4697, 'sha256': 'bf898e1473e17fa2fe173756ec7bdae6541e75e5db7404b31d332cde1ee0c4a2', 'git_blob': '1decc6efcc39200e7b688654736c9c946fd9e629'}, 'REPLAY_CONTROLS.json': {'bytes': 24848, 'sha256': 'd8dfa72218d7ee2729c2819860f3ec14121ac12e1d5bce7db3440eefe14c20b2', 'git_blob': '4ed4d2f56822de40df73d662300ce87b48176018'}, 'SOURCE_BRIDGE_AUDIT_MANIFEST.json': {'bytes': 1283, 'sha256': '2c99bfa0fef6a10bdd723c8908af998dde0a6bae452f1542c303d1a13c9263cb', 'git_blob': 'b63f18162d44bdf8e4a7c4c7c3d8b53af3ae689e'}, 'TEST_MUTATIONS.py': {'bytes': 6556, 'sha256': '405733c6b0914e8645b088954315b4e4a826bdf2198826e7c399fd272a07eb9b', 'git_blob': '41d3390aa5c73835a65465753c2f42d5e6a3a1a8'}, 'VERIFY_PUBLICATION.py': {'bytes': 10858, 'sha256': '26af53e20751505dcb2b310fb10d66c79042daf220c85b96395d8fed03066d6e', 'git_blob': '91ddd1fb92762d83d878e06f73c7624dffb25dd6'}, 'audit_algebra/ACCEPTANCE.json': {'bytes': 1338, 'sha256': '04ef6e96e81db64ef482a8d8e85034ba82cfd93f4bdc02e91482578bb37329c6', 'git_blob': '4a34f2af342d49493104e8e8415f2e93a85a3b88'}, 'audit_algebra/AUDIT_RECEIPT.json': {'bytes': 4886, 'sha256': '8c02e10d9534cfdd76a60b973c90f2d5e003ea5e877cb7842400df791685493c', 'git_blob': 'a12eb137ac91a8f9a3568d6c188700ce15dd0c4c'}, 'audit_algebra/INDEPENDENT_AUDIT.md': {'bytes': 12701, 'sha256': 'c9bdf6c5097bdf4c65625433d87232b1b21d7c1ea293790ccc084d2de606c2a1', 'git_blob': '7e79d53fd2434887ba4f23b257cec070454ba8df'}, 'audit_algebra/audit_controls.py': {'bytes': 8718, 'sha256': '18baf9448829a8049332e6dfa11cb3f0585dcc18a26c4d1a134ec3baa01d160e', 'git_blob': '0b081087abeea0751e2f582d6059438787f162e0'}, 'audit_source_bridge/ACCEPTANCE.json': {'bytes': 1729, 'sha256': '51390a363ff1ad499b0b7400adffd080178ebf87bebf5dbd3a10cd1b95cb3093', 'git_blob': '0bdd339251c870d50389bfd44b3170cb7f69450b'}, 'audit_source_bridge/FULL_AUDIT.md': {'bytes': 16804, 'sha256': '97a73549e4dbfdf4716cbc8039565c84b74cd02f08fccfd60ae36be280ee71d3', 'git_blob': '4f9bcd16d9b0c8b7c5a2b39d979b4aa8d7f0732e'}, 'audit_source_bridge/REPLAY_RECEIPT.json': {'bytes': 12416, 'sha256': '010fdd177c490767440a220cf1e98492e9cdbdb4a7850858a3034fb1c6c5d189', 'git_blob': '58e31f25f772891ab1db7e29c13721bdd9dbb240'}, 'audit_source_bridge/SOURCE_INSPECTION.json': {'bytes': 6158, 'sha256': '945af554f32fdb205a9eba143b2dba5237c79a84d4ff80e418e5aada65b7742b', 'git_blob': '9eb0a0837e5bdf42084379c3e01f248d8aa140dc'}, 'audit_source_bridge/independent_algebra.py': {'bytes': 3056, 'sha256': 'cca45522c8ca635caffd92589e7aa52372f16371e97e7f6eb0c2b7ecc1732020', 'git_blob': '14a20dfd9c9fc00b41132ed9b345deb36db6db2a'}, 'audit_source_bridge/run_audit.py': {'bytes': 10147, 'sha256': 'c35afade977c17eb0afa73953b37467dd19e273fa5763b54b4d6b8db311f2c43', 'git_blob': 'e5cb630a90699a4e2ff788ce556f8eeb8fe62180'}, 'author_v3/AUTHOR_MANIFEST.json': {'bytes': 1513, 'sha256': 'abc975e091ff72d9b020f238ef4ff7884a4ce9c0ed755b34f45626c1ef74158c', 'git_blob': '4314f85900629c6a938bd1f7d3ed7443b6fad29b'}, 'author_v3/bootstrap.py': {'bytes': 3273, 'sha256': '301e0c33f5eafccb1701687ae9cfbd574496b0ef1fd357bb4c4efe728c2379fa', 'git_blob': '62eb92e71744fb8ed55eafaa0727457d012008e5'}, 'author_v3/packet/APPROACH_LEDGER.json': {'bytes': 803, 'sha256': '03ec94080e3a4916120fc90dd259006445deedc2b79b35357c8054d90a0a3650', 'git_blob': 'd4bd1085e8e23c4d7b797ed53f183e1613e27064'}, 'author_v3/packet/CERTIFICATE.json': {'bytes': 580, 'sha256': 'c8e7bdc0790a4a51184699ffb436b6ce52e8e243b7c628bb666f9cd9f38dccd0', 'git_blob': 'ebbd7c8378d30f41c508488a8e6f6ce3155eb0c6'}, 'author_v3/packet/CLAIMS.json': {'bytes': 845, 'sha256': '9e4d7c542c659c5c1de2bb0534981965a98f0106eecbd36775fac8872b9fa051', 'git_blob': 'f844c9a623cf80927bca24d1ff59116f90d4c97f'}, 'author_v3/packet/DIAGNOSTICS.json': {'bytes': 343, 'sha256': '26dabf3b19d2806922d317a38c07333440c4d9471576deab408bf977b576d1a0', 'git_blob': 'f5090d820f31da5ef0e8d2c73da506d254ea3748'}, 'author_v3/packet/GATE_METADATA.json': {'bytes': 951, 'sha256': '1307a1619f841c6ad67128dc0ca58d7d88b87f5fc979fd0de4a8ccbd364deb16', 'git_blob': '077292f806c39e576a4f47fb142fc7bb523db9a4'}, 'author_v3/packet/PROOF_AND_STATUS.md': {'bytes': 11062, 'sha256': 'ef2895590a3f7a32fe87e391fce50860df2f61c55c46e1732d6f934928017762', 'git_blob': '3b011ceaa7473491e3f1a0fee3c1ad47ba4771fa'}, 'author_v3/packet/REPRODUCIBILITY.md': {'bytes': 2233, 'sha256': 'b389d6b12626ed7e1bd2450bcc6adae5b03249d10cea1b73be2dd27f4565d34d', 'git_blob': 'f82a9a1fbab7fbb8a3d10cde13f4acda69298a32'}, 'author_v3/packet/SOURCE_METADATA.json': {'bytes': 5719, 'sha256': 'a0326e63762d4da5cf03d016015e894ad53f16f6d46dfc62ffd389735c44768c', 'git_blob': 'fee2050b636dbdc86f032d8013d7e4441643124c'}, 'author_v3/packet/verify.py': {'bytes': 5752, 'sha256': 'f131676e31272e2a0a55ad242b0302e6a356ecb6c3cfbe56f71c3fd4dac0ab53', 'git_blob': '22ff9a0cf9df645b95a5d72eb664531c4d84fe88'}}
class Reject(ValueError):pass

def need(ok,message):
    if not ok:raise Reject(message)

def sha(data):return hashlib.sha256(data).hexdigest()
def integer(x,low=0,high=MAX_TOTAL_BYTES):return type(x) is int and low<=x<=high

def keys(x,want,label):need(type(x) is dict and set(x)==set(want),'schema keys: '+label)

def parse(raw,label='JSON'):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'duplicate JSON key: '+label);out[k]=v
        return out
    try:return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(Reject('nonfinite JSON')))
    except (UnicodeError,json.JSONDecodeError,RecursionError) as e:raise Reject('invalid JSON: '+label) from e

def canonical(name):
    need(type(name) is str and name not in ('.','..') and 0<len(name)<=512 and re.fullmatch(r'[A-Za-z0-9_./-]+',name) is not None,'path scalar/characters')
    p=PurePosixPath(name)
    need(not p.is_absolute() and p.as_posix()==name and len(p.parts)<=MAX_DEPTH,'path canonical/depth')
    reserved={'CON','PRN','AUX','NUL'}|{s+str(i) for s in ('COM','LPT') for i in range(1,10)}
    need(all(x not in ('.','..','') and len(x)<=255 and not x.endswith('.') and x.split('.')[0].upper() not in reserved for x in p.parts),'path component/reserved')
    return name

def namespace(files,directories=()):
    fs=list(files);ds=list(directories)
    need(len(fs)==len(set(fs)) and len(ds)==len(set(ds)),'duplicate namespace')
    f=set(fs);d=set(ds)
    for n in f|d:
        canonical(n);d.update(q.as_posix() for q in PurePosixPath(n).parents if q.as_posix()!='.')
    need(not f&d,'file used as directory/ancestor')
    combined=f|d
    need(len(combined)==len({n.casefold() for n in combined}),'case-alias file/directory namespace')
    return d

def root_without_links(value):
    need(type(value) is str and value and '..' not in Path(value).parts,'root canonical path')
    p=Path(os.path.abspath(value))
    for q in [*reversed(p.parents),p]:
        s=q.lstat();need(stat.S_ISDIR(s.st_mode),'root/ancestor must be real directory')
    return p

def regular_path(value,cap):
    p=Path(value)
    root_without_links(str(p.absolute().parent))
    s=p.lstat()
    need(stat.S_ISREG(s.st_mode) and s.st_nlink==1 and stat.S_IMODE(s.st_mode)==0o644,'external input regular single-link0644')
    need(integer(s.st_size,high=cap),'external input size cap')
    return read_file(p.parent,p.name,s,cap)

def scan(value):
    root=root_without_links(value);files={};dirs=set();todo=[(root,'')];total=0
    while todo:
        folder,prefix=todo.pop()
        with os.scandir(folder) as entries:
            for e in entries:
                n=canonical(prefix+e.name);s=e.stat(follow_symlinks=False)
                if stat.S_ISDIR(s.st_mode):
                    need(len(dirs)<MAX_DIRS,'directory count cap');dirs.add(n);todo.append((root/n,n+'/'))
                else:
                    need(stat.S_ISREG(s.st_mode),'nonregular payload: '+n)
                    need(s.st_nlink==1,'hard-linked payload: '+n)
                    need(stat.S_IMODE(s.st_mode)==0o644,'disk mode0644: '+n)
                    need(integer(s.st_size,high=MAX_FILE_BYTES),'per-file size cap')
                    need(len(files)<MAX_FILES,'file count cap');total+=s.st_size
                    need(total<=MAX_TOTAL_BYTES,'total size cap');files[n]=s
    namespace(files,dirs)
    return root,files,dirs

def read_file(root,name,before,cap=MAX_FILE_BYTES):
    fd=os.open(root/name,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)|getattr(os,'O_NONBLOCK',0))
    try:
        s=os.fstat(fd)
        need(stat.S_ISREG(s.st_mode) and s.st_nlink==1 and stat.S_IMODE(s.st_mode)==0o644,'file type/mode/link changed')
        need((s.st_dev,s.st_ino,s.st_size)==(before.st_dev,before.st_ino,before.st_size) and s.st_size<=cap,'file identity/size cap')
        chunks=[];size=0
        while True:
            b=os.read(fd,min(65536,cap+1-size))
            if not b:break
            size+=len(b);need(size<=cap and size<=s.st_size,'file grew');chunks.append(b)
        need(size==s.st_size,'file shortened');return b''.join(chunks)
    finally:os.close(fd)

def entry(e,label):
    keys(e,('bytes','sha256','mode'),label)
    need(integer(e['bytes'],high=MAX_FILE_BYTES),'integer byte size: '+label)
    need(type(e['sha256']) is str and HEX64.fullmatch(e['sha256']),'lowercase SHA256: '+label)
    need(e['mode']=='100644' and type(e['mode']) is str,'mode100644: '+label)

def file_map(m,label):
    need(type(m) is dict and 0<len(m)<MAX_FILES,'file map count: '+label)
    for n,e in m.items():canonical(n);entry(e,n)
    namespace(m)
    need(sum(e['bytes'] for e in m.values())<=MAX_TOTAL_BYTES,'declared total size cap')

def manifest(raw,anchor):
    need(type(anchor) is str and HEX64.fullmatch(anchor),'external manifest SHA256 required')
    need(len(raw)<=MAX_MANIFEST_BYTES and sha(raw)==anchor,'external manifest anchor mismatch')
    d=parse(raw,MANIFEST)
    keys(d,('schema','version','problem_id','original_head','files','archives'),'manifest')
    need(d['schema']==SCHEMA and type(d['version']) is int and d['version']==1,'manifest identity/version')
    need(type(d['problem_id']) is int and d['problem_id']==10400145 and d['original_head']==HEAD,'manifest target')
    file_map(d['files'],'package');need(MANIFEST not in d['files'],'manifest cannot inventory itself')
    need(type(d['archives']) is dict and set(d['archives'])=={n for n in d['files'] if n.lower().endswith('.zip')},'complete ZIP inventory')
    for n,m in d['archives'].items():file_map(m,'archive '+n)
    return d

def zip_metadata(z):
    infos=z.infolist();need(0<len(infos)<=MAX_ZIP_MEMBERS,'archive member count')
    files={};dirs=[];total=0;all_names=[]
    for i in infos:
        need(i.orig_filename==i.filename,'ZIP raw-name truncation')
        directory=i.is_dir();name=i.filename[:-1] if directory else i.filename
        canonical(name);all_names.append(name)
        need(i.create_system==3 and (i.external_attr>>16)==(0o40755 if directory else 0o100644),'ZIP exact Unix type/mode')
        need(i.external_attr&0xFFFF==(0x10 if directory else 0),'ZIP DOS attributes')
        need(not(i.flag_bits&~(0x800|0x08)) and i.compress_type in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED),'ZIP encryption/flags/compression')
        need(integer(i.file_size,high=MAX_FILE_BYTES) and integer(i.compress_size,high=MAX_ZIP_BYTES),'ZIP member size cap')
        need(i.file_size<=MAX_ZIP_RATIO*max(1,i.compress_size),'ZIP ratio cap')
        total+=i.file_size;need(total<=MAX_TOTAL_BYTES,'ZIP cumulative size cap')
        if directory:
            need(i.file_size==0 and i.CRC==0,'ZIP directory data');dirs.append(name)
        else:files[name]=i
    need(len(all_names)==len(set(all_names)),'ZIP duplicate member')
    implied=namespace(files,dirs)
    need(set(dirs)<=namespace(files),'ZIP empty directory')
    need(len(implied)<=MAX_DIRS,'ZIP implied-directory count cap')
    return files

def zip_bytes(z,item):
    with z.open(item,'r') as stream:
        data=stream.read(item.file_size+1)
        need(len(data)==item.file_size and not stream.read(1),'ZIP expanded size mismatch')
    return data

def inspect_archive(data,expected):
    need(type(data) is bytes and len(data)<=MAX_ZIP_BYTES,'ZIP byte cap')
    file_map(expected,'expected ZIP')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        items=zip_metadata(z)
        need(set(items)==set(expected),'ZIP complete member map')
        for n,i in items.items():need(i.file_size==expected[n]['bytes'],'ZIP declared size')
        result={n:zip_bytes(z,i) for n,i in items.items()}
    for n,b in result.items():need(sha(b)==expected[n]['sha256'],'ZIP expanded hash: '+n)
    return result

def authenticate(payload,doc):
    need(set(payload)==set(doc['files']),'closed payload inventory')
    for n,b in payload.items():need(len(b)==doc['files'][n]['bytes'] and sha(b)==doc['files'][n]['sha256'],'payload fingerprint: '+n)
    originals={n[len(PREFIX):]:b for n,b in payload.items() if n.startswith(PREFIX)}
    need(set(originals)==set(ORIGINAL_PINS) and len(originals)==33,'exact original33 inventory')
    for n,b in originals.items():
        p=ORIGINAL_PINS[n];blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        need(len(b)==p['bytes'] and sha(b)==p['sha256'] and blob==p['git_blob'],'immutable original: '+n)
    need(MATH in payload and sha(payload[MATH])==MATH_SHA,'independent math fixed pin')
    for n,m in doc['archives'].items():inspect_archive(payload[n],m)
    return {'schema':SCHEMA,'status':'PASS_CLOSED_FINITE_PACKAGE','original_head':HEAD,'original_files':33,'files':len(payload)+1,'archive_count':len(doc['archives'])}

def verify(root_value,anchor):
    root,files,dirs=scan(root_value);need(MANIFEST in files,'manifest missing')
    raw=read_file(root,MANIFEST,files[MANIFEST],MAX_MANIFEST_BYTES);doc=manifest(raw,anchor)
    need(set(files)==set(doc['files'])|{MANIFEST},'closed file inventory')
    need(dirs==namespace(files),'closed directory inventory')
    payload={n:read_file(root,n,files[n]) for n in doc['files']}
    result=authenticate(payload,doc);result['manifest_sha256']=anchor
    return result,payload,raw

def verify_zip(data,anchor):
    need(type(data) is bytes and len(data)<=MAX_ZIP_BYTES,'outer ZIP byte cap')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        items=zip_metadata(z);need(MANIFEST in items,'ZIP manifest missing')
        need(items[MANIFEST].file_size<=MAX_MANIFEST_BYTES,'ZIP manifest cap')
        raw=zip_bytes(z,items[MANIFEST]);doc=manifest(raw,anchor)
        need(set(items)==set(doc['files'])|{MANIFEST},'outer ZIP exact file inventory')
        # All member metadata and the externally sealed manifest precede payload reads.
        for n,e in doc['files'].items():need(items[n].file_size==e['bytes'],'outer ZIP declared size')
        payload={n:zip_bytes(z,items[n]) for n in doc['files']}
    result=authenticate(payload,doc);result['manifest_sha256']=anchor
    return result,payload,raw

def run_bounded(argv,cwd,env,seconds=60,stdout_cap=128*1024,stderr_cap=16*1024):
    need(seconds>0 and stdout_cap>0 and stderr_cap>0,'child bounds')
    p=subprocess.Popen(argv,cwd=cwd,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    buffers=[bytearray(),bytearray()];overflow=threading.Event()
    def consume(s,index,cap):
        try:
            while True:
                chunk=s.read(4096)
                if not chunk:break
                room=cap-len(buffers[index]);buffers[index].extend(chunk[:max(room,0)])
                if len(chunk)>room:overflow.set();break
        finally:s.close()
    ts=[threading.Thread(target=consume,args=(s,i,c),daemon=True) for i,(s,c) in enumerate(((p.stdout,stdout_cap),(p.stderr,stderr_cap)))]
    for t in ts:t.start()
    deadline=time.monotonic()+seconds;failure=None
    while p.poll() is None:
        if overflow.is_set():failure='child output cap';break
        if time.monotonic()>=deadline:failure='child wall-time cap';break
        overflow.wait(0.02)
    if failure:p.kill()
    p.wait(timeout=5)
    for t in ts:t.join(timeout=1)
    need(not any(t.is_alive() for t in ts),'child stream cleanup')
    need(not overflow.is_set(),'child output cap');need(failure is None,failure or 'child failure')
    return p.returncode,bytes(buffers[0]),bytes(buffers[1])

def replay(payload,work_value):
    work=root_without_links(work_value);rows=[];outputs={}
    with tempfile.TemporaryDirectory(prefix='pr952-cold-',dir=work) as td:
        temp=Path(td);packet=temp/'packet';packet.mkdir();scratch=temp/'scratch';scratch.mkdir()
        for n,b in payload.items():
            p=packet/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o644)
        original=packet/PREFIX
        stages=[('independent-math',packet/MATH,[]),('original-author',original/'author_v3/bootstrap.py',[original/'author_v3/packet']),('original-algebra-audit',original/'audit_algebra/audit_controls.py',[original/'author_v3']),('original-bridge-finite-algebra',original/'audit_source_bridge/independent_algebra.py',[])]
        env={'TMPDIR':str(scratch),'TMP':str(scratch),'TEMP':str(scratch)}
        for k in ('SYSTEMROOT','WINDIR'):
            if k in os.environ:env[k]=os.environ[k]
        for mode,flag in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
            for label,script,args in stages:
                code,out,err=run_bounded([sys.executable,'-I','-S','-B',*flag,str(script),*map(str,args)],scratch,env)
                need(code==0 and not err,'supported checker failed: '+label+': '+err.decode('utf-8','replace')[:1000])
                obj=parse(out,label);need(type(obj) is dict,'checker JSON object')
                need(label not in outputs or outputs[label]==out,'optimization changed checker output: '+label);outputs[label]=out
                rows.append({'stage':label,'mode':mode,'returncode':code,'stdout_sha256':sha(out),'result':obj})
        # Explicit false-check exception survives every optimization mode.
        for flag in ([],['-O'],['-OO']):
            code,out,err=run_bounded([sys.executable,'-I','-S','-B',*flag,'-c',"raise RuntimeError('PR952_ACTIVE_GUARD')"],scratch,env)
            need(code!=0 and b'PR952_ACTIVE_GUARD' in err,'active guard failed')
        need(not any(scratch.iterdir()),'checker left scratch data')
        _,files,dirs=scan(str(packet))
        need(set(files)==set(payload) and dirs==namespace(payload),'checker modified namespace')
        need(all(read_file(packet,n,files[n])==b for n,b in payload.items()),'checker modified payload')
    return rows

def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--root');g.add_argument('--archive');p.add_argument('--archive-sha256')
    p.add_argument('--manifest-sha256',required=True);p.add_argument('--run-checkers',action='store_true');p.add_argument('--work-dir')
    a=p.parse_args()
    if a.archive:
        need(type(a.archive_sha256) is str and HEX64.fullmatch(a.archive_sha256),'external archive SHA256 required')
        b=regular_path(a.archive,MAX_ZIP_BYTES);need(sha(b)==a.archive_sha256,'external archive SHA256 mismatch')
        result,payload,raw=verify_zip(b,a.manifest_sha256)
    else:
        need(a.archive_sha256 is None,'archive SHA supplied without archive');result,payload,raw=verify(a.root,a.manifest_sha256)
    if a.run_checkers:
        need(a.work_dir is not None,'explicit owned work directory required')
        work=root_without_links(a.work_dir)
        if a.root:
            root=root_without_links(a.root);need(work!=root and not work.is_relative_to(root),'work must be outside package')
        result['replays']=replay(payload,str(work))
        if a.root:
            _,after,after_raw=verify(a.root,a.manifest_sha256);need(after==payload and after_raw==raw,'source package changed during replay')
    result['outer_runtime']={'optimize':sys.flags.optimize,'isolated':sys.flags.isolated,'no_site':sys.flags.no_site,'dont_write_bytecode':sys.dont_write_bytecode}
    result['scope']={'linux_legacy_full_bwrap_EROFS':'NOT_RUN','whole_filesystem_readonly':'NOT_TESTED','quantum_topology_reproof':'NOT_RUN','primary_source_inspection':'NOT_RUN','priority_certification':False,'human_certification':False,'formal_certification':False,'full_paper_acceptance':False,'historical_receipts_relabelled':False}
    result['trust_roots']=['Externally authenticated verifier and manifest SHA256','Pinned original33 and independent checker','Installed Python executable, standard library and host OS/account','Nonconcurrent source replacement; no race-resistant OS sandbox']
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
    try:main()
    except (Reject,OSError,RuntimeError,zipfile.BadZipFile,subprocess.SubprocessError) as e:
        print('PROFILE_REJECT: '+str(e),file=sys.stderr);raise SystemExit(1)
