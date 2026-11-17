#!/usr/bin/env python3
"""Fixed15/13A2M controlled preparation. Default has no repository reads or writes.
All active modes remain UNEXECUTED until later explicit root GO.
Install and publish need separate fresh root authorizations. Runtime is separate
from this immutable preparation. Failures retain partial state/locks; no retry.
"""
from pathlib import Path
import base64, ctypes, datetime, hashlib, json, os, re, stat, struct, subprocess, sys
import xml.etree.ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M = P.parent
N = P/'verification/low-exponent-su5-production-sol-20261116'
RUN = P/'verification/low-exponent-su5-runtime-root-20261116'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
PLAN_SHA = '9f2874242ce96320a219c7819b5579c620f4344ad8ee08f7c296e4363129a580'
TARGETS = frozenset(["public/research/index.html","public/research/low-exponent-supersolvability/citation.bib","public/research/low-exponent-supersolvability/index.html","public/research/low-exponent-supersolvability/low_exponent_supersolvability.pdf","public/research/low-exponent-supersolvability/low_exponent_verification.zip","public/research/sitemap.xml","public/research/su5-lens-space-counterexample/LICENSE.txt","public/research/su5-lens-space-counterexample/PR95_PRIORITY_QUALIFICATION.md","public/research/su5-lens-space-counterexample/README.md","public/research/su5-lens-space-counterexample/SHA256SUMS.txt","public/research/su5-lens-space-counterexample/citation.bib","public/research/su5-lens-space-counterexample/index.html","public/research/su5-lens-space-counterexample/pr95_note.pdf","public/research/su5-lens-space-counterexample/pr95_note.tex","public/research/su5-lens-space-counterexample/pr95_support.zip"])
REPLACEMENTS = ['public/research/index.html', 'public/research/sitemap.xml']
LOG = None
TRACE = []
ENV = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_OPTIONAL_LOCKS='0', GIT_INDEX_VERSION='2', GIT_TERMINAL_PROMPT='0', GIT_NO_LAZY_FETCH='1')
GIT_OPTIONS = ['-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','core.untrackedCache=false','-c','gc.auto=0','-c','maintenance.auto=false','-c','commit.gpgsign=false','-c','core.splitIndex=false','-c','index.version=2','-c','remote.origin.mirror=false']

def need(ok, why):
    if not ok: raise ValueError(why)
def utc(): return datetime.datetime.now(datetime.timezone.utc)
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(b): return {'bytes':len(b),'SHA256':sha(b)}
def packed(x): return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def inode(s): return (s.st_dev,s.st_ino)
def mode(p): return stat.S_IMODE(p.lstat().st_mode)
def safe(p):
    need(p.is_absolute() and '..' not in p.parts,'absolute canonical path')
    need(all(not q.is_symlink() for q in [p,*p.parents]),'no symlink path')
def held(fd):
    a=os.fstat(fd); need(stat.S_ISREG(a.st_mode),'regular held file'); os.lseek(fd,0,0); parts=[]
    while block:=os.read(fd,1048576): parts.append(block)
    z=os.fstat(fd); need((a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_size,z.st_mtime_ns,z.st_ctime_ns),'stable held read')
    b=b''.join(parts); need(len(b)==a.st_size,'whole held buffer'); return b
def read(p):
    safe(p); first=p.lstat(); need(stat.S_ISREG(first.st_mode),'ordinary file: '+str(p)); fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        need(inode(first)==inode(os.fstat(fd)),'opened identity'); b=held(fd)
        need(inode(p.lstat())==inode(os.fstat(fd)),'live held identity'); return b
    finally: os.close(fd)
def bound(row):
    p=Path(row['path']); p=p if p.is_absolute() else P/p
    b=read(p); need(pin(b)=={k:row[k] for k in ('bytes','SHA256')},'bound input: '+str(p)); return b
def write_all(fd,b):
    i=0
    while i<len(b):
        n=os.write(fd,b[i:]); need(n>0,'complete write'); i+=n
def sync_dir(p):
    fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try: os.fsync(fd)
    finally: os.close(fd)
def new_file(p,b,permissions=0o600):
    safe(p); fd=os.open(p,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,permissions)
    try: write_all(fd,b); os.fchmod(fd,permissions); os.fsync(fd); need(held(fd)==b,'durable complete private buffer')
    finally: os.close(fd)
    sync_dir(p.parent)
def event(phase, **fields):
    row = {'UTC':utc().isoformat(), 'phase':phase, **fields}
    if LOG is None:
        TRACE.append(row)
    else:
        LOG.write(packed(row)); LOG.flush(); os.fsync(LOG.fileno())

def git(*args,data=None,index=None,identity=None,cwd=W,opaque=False,absent_origin_vcs_ok=False):
    env=dict(ENV)
    if index is not None: env['GIT_INDEX_FILE']=str(index)
    if identity: env.update(identity)
    cmd=['git','--no-optional-locks',*GIT_OPTIONS,*args]; r=subprocess.run(cmd,cwd=cwd,env=env,input=data,capture_output=True)
    event('git',argv=cmd,input_SHA256=None if data is None else sha(data),exit=r.returncode,stdout_SHA256=sha(r.stdout),stderr_SHA256=sha(r.stderr),stdout_base64=None if opaque else base64.b64encode(r.stdout).decode(),stderr_base64=base64.b64encode(r.stderr).decode())
    absent = absent_origin_vcs_ok and args==('config','--null','--get-all','remote.origin.vcs') and r.returncode==1 and r.stdout==b'' and r.stderr==b''
    need(r.returncode==0 or absent,'Git failed: '+args[0]); return r.stdout

def routing(p,expected=None):
    args=('config','--null','--show-origin','--show-scope','--get-regexp',p['routing_config_key_regex'])
    before=git(*args,opaque=True)
    selector=git('config','--null','--get-all','remote.origin.vcs',opaque=True,absent_origin_vcs_ok=True)
    need(selector==b'','remote.origin.vcs transport selector must be absent')
    fetch=git('remote','get-url','--all','origin',opaque=True)
    push=git('remote','get-url','--push','--all','origin',opaque=True)
    after=git(*args,opaque=True)
    need(before==after,'stable effective routing configuration')
    intended=(p['origin']+'\n').encode()
    need(fetch==intended and push==intended,'exact singleton effective origin fetch/push URLs')
    state={'configuration':pin(before),'effective_fetch_URL_SHA256':sha(fetch),'effective_push_URL_SHA256':sha(push),'singletons_match_intended_origin':True,'origin_vcs_selector_absent':True}
    need(expected is None or state==expected,'authorization-bound routing configuration unchanged')
    return state

def census(root):
    files,dirs={},{}
    def visit(d):
        safe(d); before=d.lstat(); need(stat.S_ISDIR(before.st_mode),'ordinary directory'); dirs[d.relative_to(root).as_posix()]=mode(d)
        for p in sorted(d.iterdir()):
            s=p.lstat()
            if stat.S_ISDIR(s.st_mode): visit(p)
            elif stat.S_ISREG(s.st_mode): files[p.relative_to(root).as_posix()]={**pin(read(p)),'mode':mode(p)}
            else: raise ValueError('special namespace entry')
        z=d.lstat(); need((before.st_ino,before.st_mtime_ns,before.st_ctime_ns)==(z.st_ino,z.st_mtime_ns,z.st_ctime_ns),'stable namespace enumeration')
    visit(root); return files,dirs

def typed_spans(raw):
    start=raw.index('[',raw.index('"itemListElement"')); decoder=json.JSONDecoder(); items,end=decoder.raw_decode(raw,start); pos=start+1; spans=[]
    for unused in items:
        while raw[pos].isspace() or raw[pos]==',': pos+=1
        unused,end=decoder.raw_decode(raw,pos); spans.append(raw[pos:end]); pos=end
    return spans

def snapshot_tables(snapshot):
    files = {x['path']:{'bytes':x['bytes'],'SHA256':x['sha256'],'mode':int(x['mode'],8)} for x in snapshot['files']}
    dirs = {x['path']:int(x['mode'],8) for x in snapshot['directories']}
    need(len(files)==len(snapshot['files']) and len(dirs)==len(snapshot['directories']),'unique finite rows')
    return files,dirs

def contract():
    need(Path(__file__).absolute()==N/'release_two.py','fixed helper location')
    raw=read(N/'PLAN.json'); need(sha(raw)==PLAN_SHA,'immutable current plan')
    p=json.loads(raw)
    need(p['preparation_root']==str(N) and p['runtime_root']==str(RUN) and p['website']==str(W),'fixed distinct prep/runtime/W')
    need(p['scope_paths']==sorted(TARGETS) and p['replacement_paths']==REPLACEMENTS and (p['paths'],p['new_leaves'],p['replacements'])==(15,13,2),'exact fixed15/13A2M')
    need(p['record_ids']==[23331709,23174156] and p['branch']=='refs/heads/master','only admitted records/master')
    adoption=json.loads(bound(p['root_stage_adoption']))
    need(adoption['status']=='ROOT_PRIVATE_STAGE_ADOPTED_PRODUCTION_PREPARATION_ONLY' and adoption['install_commit_push_deploy_Sheet_AA_authority'] is False,'actual private-stage adoption is not action GO')
    need(adoption['records']==p['record_ids'] and adoption['all15targetpayloads_adopted'] is True,'actual two-page15-payload adoption')
    need(adoption['checks']['stage']['FINAL_SHA256']==p['stage_FINAL']['SHA256'] and adoption['checks']['stage']['manifest_SHA256']==p['stage_manifest']['SHA256'],'adopted frozen stage controls')
    need(adoption['checks']['stage']['whole_payloads_modes_topology_authenticated'] is True and adoption['checks']['independent_audit']['whole_payloads_modes_topology_authenticated'] is True,'root adopted whole stage and independent stage audit')
    S=Path(p['stage_root']); need(S==P/'verification/low-exponent-su5-stage-sol-20261116','fixed fresh stage')
    final=json.loads(bound(p['stage_FINAL'])); manifest=json.loads(bound(p['stage_manifest']))
    stage_files,stage_dirs=census(S)
    need(len(stage_files)==34 and len(stage_dirs)==5 and manifest['regular_file_count']==34 and manifest['child_directory_count']==4,'whole34/4 frozen stage extent')
    need(set(stage_files)=={x['path'] for x in manifest['files']},'stage exact finite file membership')
    for row in manifest['files']:
        if row['path'] in ('FINAL.json','OWNED_MANIFEST.json'): continue
        need(stage_files[row['path']]=={'bytes':row['bytes'],'SHA256':row['sha256'],'mode':int(row['mode'],8)},'whole stage row')
    need(stage_dirs=={x['path']:int(x['mode'],8) for x in manifest['directories']},'all frozen stage directory modes')
    need(stage_files['FINAL.json']=={**pin(bound(p['stage_FINAL'])),'mode':0o644} and stage_files['OWNED_MANIFEST.json']=={**pin(bound(p['stage_manifest'])),'mode':0o644},'terminal controls whole-byte/mode bound')
    target_plan=json.loads(bound(p['stage_target_plan']))
    need(len(target_plan['targets'])==15 and {'public/'+x['target'] for x in target_plan['targets']}==TARGETS,'only exact15 candidate targets')
    buffers={}
    for row in target_plan['targets']:
        name='public/'+row['target']; rel=name
        need(rel in stage_files and row['after']['path']==row['target'] and row['after']['mode']=='0644','typed exact candidate path/mode')
        b=read(S/rel); need(pin(b)=={'bytes':row['after']['bytes'],'SHA256':row['after']['sha256']} and stage_files[rel]=={**pin(b),'mode':0o644},'whole adopted candidate')
        need(row['operation']==('MODIFY' if name in REPLACEMENTS else 'ADD'),'literal13A2M plan'); buffers[name]=b
    need({x for x in stage_files if x.startswith('public/')}==TARGETS,'candidate has no extra public path')
    baseline=json.loads(bound(p['baseline'])); old_files,old_dirs=snapshot_tables(baseline['public'])
    need(len(old_files)==747 and len(old_dirs)==367 and old_dirs['.']==0o750,'exact independent747-filesystem baseline')
    need(len(baseline['DS_Store_rows_included_in_complete_public_guard'])==17,'all17DSStore separately whole-guarded')
    for name in TARGETS: need((name[7:] in old_files)==(name in REPLACEMENTS),'13filesystem absences/two old aggregates')
    new_dirs=set()
    for name in buffers: new_dirs.update(q.as_posix() for q in Path(name[7:]).parents if q.as_posix() not in old_dirs)
    need(new_dirs==set(p['new_directories']) and len(new_dirs)==2,'two necessary new directories only')
    custody=json.loads(bound(p['source_custody']))
    before=custody['before']; namespaces=before['writer_packets']+[before['original167_packet']]+before['source_packets']
    need([len(x['files']) for x in before['writer_packets']]==[21,26] and len(before['original167_packet']['files'])==22 and sum(len(x['files']) for x in before['source_packets'])==306,'exact47+22+306 source contract')
    for namespace in namespaces: need(census(Path(namespace['root']))==snapshot_tables(namespace),'whole source/editorial namespace unchanged')
    row=before['authority']; need(pin(read(Path(row['path'])))=={'bytes':row['bytes'],'SHA256':row['sha256']} and mode(Path(row['path']))==int(row['mode'],8),'original root copy adoption unchanged')
    for row in p['configuration_guards']: need(pin(read(Path(row['path'])))=={k:row[k] for k in ('bytes','SHA256')} and mode(Path(row['path']))==row['mode'],'hosting configuration bytes/modes unchanged')
    for row in baseline['raw_HEAD_ref_config_guards']:
        if row['path']==str(W/'.git/config'):
            need(pin(read(Path(row['path'])))=={'bytes':row['bytes'],'SHA256':row['sha256']} and mode(Path(row['path']))==int(row['mode'],8),'W config unchanged')
    index=buffers['public/research/index.html'].decode('utf-8')
    entity=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',index,re.S)[1])['mainEntity']
    need(entity['numberOfItems']==len(entity['itemListElement'])==123 and len(ET.fromstring(buffers['public/research/sitemap.xml']))==124,'actual123/124 candidate aggregate counts')
    p['_baseline']=baseline
    return p,buffers,old_files,old_dirs,new_dirs

def math_fence(p):
    baseline=p['_baseline']
    rows=[x for x in baseline['native_indices']+baseline['raw_HEAD_ref_config_guards'] if Path(x['path']).is_relative_to(M/'.git')]
    need(len(rows)==4,'exact Math index/HEAD/packed-ref/config guards')
    for row in rows:
        need(pin(read(Path(row['path'])))=={'bytes':row['bytes'],'SHA256':row['sha256']} and mode(Path(row['path']))==int(row['mode'],8),'Math raw shared metadata unchanged')
    for name in baseline['explicit_absent_paths']: need(not os.path.lexists(name),'Math explicit absence unchanged')

def public_fence(p,buffers,old_files,old_dirs,new_dirs,installed):
    expected={k:dict(v) for k,v in old_files.items()}; dirs=dict(old_dirs)
    if installed:
        expected.update({k[7:]:{**pin(v),'mode':0o644} for k,v in buffers.items()}); dirs.update({q:0o755 for q in new_dirs})
    actual=census(W/'public'); need(actual==(expected,dirs),'whole phase-appropriate public bytes/types/modes/topology')
    index=read(W/'public/research/index.html'); obj=json.loads(re.search(rb'<script type="application/ld\+json">(.*?)</script>',index,re.S)[1])
    counts=[len(expected),obj['mainEntity']['numberOfItems'],len(ET.fromstring(read(W/'public/research/sitemap.xml')))]
    need(counts==(p['after_counts'] if installed else p['before_counts']),'exact phase counts')
    need(len(obj['mainEntity']['itemListElement'])==counts[1],'actual index list count')
    return actual,counts

def entries(b):
    need(b[:4]==b'DIRC' and struct.unpack('>I',b[4:8])[0]==2 and hashlib.sha1(b[:-20]).digest()==b[-20:],'v2 index/checksum')
    result={}; pos=12; previous=None
    for unused in range(struct.unpack('>I',b[8:12])[0]):
        start=pos; flags=struct.unpack('>H',b[pos+60:pos+62])[0]; need(not flags&0x7000,'ordinary stage-zero index record')
        end=b.index(b'\0',pos+62); name=b[pos+62:end]; pos=start+((end+1-start+7)//8)*8
        need(name and (previous is None or previous<name) and not any(b[end+1:pos]) and flags&0xfff==min(len(name),0xfff),'sorted unique whole raw record')
        result[name]=(b[start:pos],b[start+24:start+28],b[start+40:start+60]); previous=name
    extension_start=pos
    while pos<len(b)-20:
        kind,size=b[pos:pos+4],struct.unpack('>I',b[pos+4:pos+8])[0]; need(kind==b'TREE' and pos+8+size<=len(b)-20,'only cache-tree extension'); pos+=8+size
    need(pos==len(b)-20,'whole index extent'); return result,b[extension_start:-20]

def preflight(required=None,owned_index_lock=None):
    p,buffers,old_files,old_dirs,new_dirs=contract(); math_fence(p)
    need(git('rev-parse','--show-toplevel').strip().decode()==str(W),'exact W repository root')
    need(git('symbolic-ref','HEAD').strip().decode()==p['branch'] and git('rev-parse','HEAD').strip().decode()==p['website_HEAD'],'existing master and immutable parent')
    need(git('rev-parse','--show-object-format').strip()==b'sha1','SHA1 repository')
    p['website_tree']=git('rev-parse','HEAD^{tree}').strip().decode()
    route=routing(p)
    old=read(W/'.git/index'); need(pin(old)=={k:p['website_index'][k] for k in ('bytes','SHA256')} and mode(W/'.git/index')==0o644,'exact9054454B/71ea native index0644')
    er,extension=entries(old); targets={n.encode() for n in TARGETS}
    need(len(er)==58687 and set(er)&targets=={n.encode() for n in REPLACEMENTS} and len(targets-set(er))==13 and len(set(er)-targets)==58685,'exact58687 original records,58685 protected,13A2M')
    protected=b''.join(er[n][0] for n in sorted(set(er)-targets))
    lock=W/'.git/index.lock'
    need(not os.path.lexists(lock) if owned_index_lock is None else os.path.lexists(lock) and inode(lock.lstat())==owned_index_lock,'exclusive native index lock state')
    tracked=git('ls-tree','-r','-z','--full-tree',p['website_HEAD'],'--',*sorted(TARGETS)).split(b'\0')
    need(tracked.pop()==b'' and {x.split(b'\t',1)[1] for x in tracked}=={x.encode() for x in REPLACEMENTS},'HEAD has only the two replacement leaves in fixed scope')
    installed=all((W/n).is_file() and pin(read(W/n))==pin(b) and mode(W/n)==0o644 for n,b in buffers.items())
    actual,counts=public_fence(p,buffers,old_files,old_dirs,new_dirs,installed)
    if required is not None: need(installed==required,'required whole preinstall/installed phase; partial state never resumed')
    identities={n:[*inode((W/n).lstat()),(W/n).lstat().st_mtime_ns,(W/n).lstat().st_ctime_ns] for n in REPLACEMENTS}
    state={'installed':installed,'plan_SHA256':PLAN_SHA,'helper_SHA256':sha(read(N/'release_two.py')),'root_stage_adoption':p['root_stage_adoption'],'stage_FINAL':p['stage_FINAL'],'public':actual,'counts':counts,'W_HEAD':p['website_HEAD'],'W_tree':p['website_tree'],'W_index':pin(old),'routing':route,'aggregate_identities':identities,'scope':[(n,pin(b)) for n,b in sorted(buffers.items())],'protected_raw_records':pin(protected),'protected_count':58685,'baseline_TREE_extension':pin(extension)}
    return p,buffers,old_files,old_dirs,new_dirs,old,sha(packed(state)),state

def authorization(kind,fp,p):
    path=Path(p['authorization_paths'][kind]); raw=read(path); a=json.loads(raw)
    fixed={'schema':p['authorization_schema'],'action':'INSTALL_EXACT15_FILESYSTEM' if kind=='install' else 'PUBLISH_EXACT15_GIT','plan_SHA256':PLAN_SHA,'helper_SHA256':sha(read(N/'release_two.py')),'root_stage_adoption':p['root_stage_adoption'],'stage_FINAL':p['stage_FINAL'],'preflight_SHA256':fp,'scope_paths':p['scope_paths'],'concurrency':p['concurrency'],'production_helper_static_audit_PASS':True,'deployment_authorized':False,'Sheet_authorized':False,'AA':None,'follow_up':None}
    extras={'issued_UTC','expires_UTC','nonce','production_helper_static_audit_FINAL'} if kind=='install' else {'issued_UTC','expires_UTC','nonce','production_helper_static_audit_FINAL','author_name','author_email','commit_date','installation_SUCCESS'}
    need(set(a)==set(fixed)|extras and all(a[k]==v for k,v in fixed.items()),'exact separate current root action authorization')
    audit=a['production_helper_static_audit_FINAL']; need(set(audit)=={'path','bytes','SHA256'} and type(audit['bytes']) is int and audit['bytes']>0 and Path(audit['path']).is_relative_to(P/'verification') and Path(audit['path']).name=='FINAL.json','concrete independently audited helper FINAL pin')
    audit_doc=json.loads(bound(audit)); need(isinstance(audit_doc,dict) and bool(audit_doc),'nonempty pinned audit FINAL; semantic PASS is explicitly adopted by root action authority')
    issued=datetime.datetime.fromisoformat(a['issued_UTC']); expiry=datetime.datetime.fromisoformat(a['expires_UTC'])
    need(issued.utcoffset() is not None and expiry.utcoffset() is not None and issued<=utc()<expiry,'current root issue/expiry')
    need(isinstance(a['nonce'],str) and re.fullmatch('[0-9a-f]{32}',a['nonce']),'fresh root action nonce')
    if kind=='Git':
        for key in ('author_name','author_email','commit_date'): need(isinstance(a[key],str) and a[key] and '\n' not in a[key] and '\0' not in a[key],'literal root commit identity/date')
        need(datetime.datetime.fromisoformat(a['commit_date']).utcoffset() is not None,'timezone-qualified commit date')
        success=json.loads(bound(a['installation_SUCCESS'])); q=Path(a['installation_SUCCESS']['path'])
        need(q.parent.parent==RUN/'install' and q.name=='SUCCESS.json' and re.fullmatch('[0-9a-f]{64}',q.parent.name),'fresh current runtime install receipt only')
        need(success['status']=='FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT' and success['counts']==[760,123,124] and success['plan_SHA256']==PLAN_SHA and success['helper_SHA256']==a['helper_SHA256'] and success['targets']==sorted(TARGETS) and success['authorization_SHA256']==q.parent.name and success['nonce']!=a['nonce'],'completed exact15 install and separate publish nonce')
    return path,raw,a,expiry

def transaction(kind,auth_raw):
    global LOG
    safe(N); safe(RUN); need(W.stat().st_dev==N.stat().st_dev,'same filesystem for atomic install')
    if not os.path.lexists(RUN): RUN.mkdir(mode=0o700); sync_dir(RUN.parent)
    need(stat.S_ISDIR(RUN.lstat().st_mode) and mode(RUN)==0o700,'fresh separate runtime root0700')
    need(RUN.stat().st_dev==W.stat().st_dev,'actual runtime staging filesystem matches W before W mutation')
    lock=RUN/('ACTIVE_INSTALL.lock' if kind=='install' else 'ACTIVE_GIT.lock')
    body=packed({'protocol':'low-exponent-su5-'+kind+'-v1','authorization_SHA256':sha(auth_raw),'PID':os.getpid()}); new_file(lock,body)
    lock_fd=os.open(lock,os.O_RDONLY|os.O_NOFOLLOW); owner=inode(os.fstat(lock_fd))
    parent=RUN/('install' if kind=='install' else 'publish')
    if not os.path.lexists(parent): parent.mkdir(mode=0o700); sync_dir(RUN)
    safe(parent); need(stat.S_ISDIR(parent.lstat().st_mode) and mode(parent)==0o700,'new private runtime phase')
    t=parent/sha(auth_raw); t.mkdir(mode=0o700); sync_dir(parent)
    fd=os.open(t/'journal.jsonl',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600); os.fchmod(fd,0o600); LOG=os.fdopen(fd,'wb'); sync_dir(t)
    def check(): need(inode(lock.lstat())==owner and held(lock_fd)==body and mode(lock)==0o600,'held exact current runtime lock')
    check(); event('PRETRANSACTION_READ_EVENTS',events=list(TRACE)); event('AUTHORIZED',kind=kind,authorization_SHA256=sha(auth_raw))
    return t,check,lock_fd

def install(snapshot):
    p,buffers,old_files,old_dirs,new_dirs,old,fp,state=snapshot; path,auth_raw,a,expiry=authorization('install',fp,p)
    need(not state['installed'] and sys.platform=='darwin','preinstall Darwin only')
    t,check,lock_fd=transaction('install',auth_raw); opened=[]; made={}; completed=[]
    libc=ctypes.CDLL('/usr/lib/libSystem.B.dylib',use_errno=True); rename=libc.renameatx_np
    rename.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint]; rename.restype=ctypes.c_int
    def current():
        check(); need(read(path)==auth_raw and datetime.datetime.fromisoformat(a['issued_UTC'])<=utc()<expiry and sha(read(N/'PLAN.json'))==PLAN_SHA and sha(read(N/'release_two.py'))==a['helper_SHA256'],'same current installation authority/code')
    try:
        staged=t/'staged'; backups=t/'backups'; staged.mkdir(mode=0o700); backups.mkdir(mode=0o700); sync_dir(t)
        order=sorted(set(buffers)-set(p['replacement_paths']))+p['replacement_paths']; originals={}; prepared={}
        for i,n in enumerate(order):
            new_file(staged/str(i),buffers[n],0o644)
            fd=os.open(staged/str(i),os.O_RDONLY|os.O_NOFOLLOW); opened.append(fd); prepared[n]=fd
        for n in p['replacement_paths']:
            fd=os.open(W/n,os.O_RDONLY|os.O_NOFOLLOW); opened.append(fd); originals[n]=fd
            need(inode(os.fstat(fd))==inode((W/n).lstat()),'held original identity'); b=held(fd)
            need(pin(b)=={k:old_files[n[7:]][k] for k in ('bytes','SHA256')},'original aggregate before backup')
            parent=backups
            for part in Path(n).parts[:-1]:
                parent=parent/part
                if not os.path.lexists(parent): parent.mkdir(mode=0o700); sync_dir(parent.parent)
                safe(parent); need(stat.S_ISDIR(parent.lstat().st_mode) and mode(parent)==0o700,'ordinary private relative backup directory')
            new_file(backups/n,b,0o644)
        absent=sorted(set(buffers)-set(p['replacement_paths'])); need(len(absent)==13 and all(not os.path.lexists(W/n) for n in absent),'thirteen original target absences')
        new_file(t/'new-targets.before.json',packed({n:'ABSENT' for n in absent}))
        new_file(t/'rollback.before.json',packed({'original_replacements':{n:old_files[n[7:]] for n in p['replacement_paths']},'original_new_target_state':{n:'ABSENT' for n in absent},'original_new_directories':{n:'ABSENT' for n in sorted(new_dirs)},'original_index':pin(old),'recovery':'STOP_AND_ROOT_REVIEW_NO_AUTOMATIC_ROLLBACK_OR_RETRY'}))
        sync_dir(staged); sync_dir(backups); sync_dir(t); event('ALL15_BUFFERS_2_RELATIVE_BACKUPS_13_ABSENCES_ROLLBACK_INPUTS_DURABLE_BEFORE_W_WRITE')
        current(); need(preflight(False)[6]==fp,'full authorization fence after durable staging before W writes')
        root_fd=os.open(W,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW); opened.append(root_fd)
        stage_fd=os.open(staged,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW); opened.append(stage_fd)
        def chain(n):
            fds=[os.dup(root_fd)]; parents=[]
            try:
                for part in Path(n).parts[:-1]:
                    parents.append(part); rel='/'.join(parents); created=False; current(); need(inode(W.lstat())==inode(os.fstat(root_fd)),'W root identity')
                    if rel.startswith('public/') and rel[7:] in new_dirs and rel not in made:
                        need(not os.path.lexists(W/rel),'exclusive new directory'); event('MKDIR_INTENT',path=rel)
                        os.mkdir(part,0o755,dir_fd=fds[-1]); os.fsync(fds[-1]); made[rel]=inode(os.stat(part,dir_fd=fds[-1],follow_symlinks=False)); created=True
                    child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fds[-1]); need(inode(os.fstat(child))==inode(os.stat(part,dir_fd=fds[-1],follow_symlinks=False)),'live ancestor')
                    if rel in made: need(inode(os.fstat(child))==made[rel],'same created directory')
                    if created: os.fchmod(child,0o755); os.fsync(child); event('MKDIR_COMPLETE',path=rel)
                    fds.append(child)
                return fds
            except BaseException:
                for fd in reversed(fds): os.close(fd)
                raise
        for i,n in enumerate(order):
            fds=chain(n)
            try:
                current(); need(inode(W.lstat())==inode(os.fstat(root_fd)),'live W immediately before mutation')
                for j,part in enumerate(Path(n).parts[:-1]): need(inode(os.stat(part,dir_fd=fds[j],follow_symlinks=False))==inode(os.fstat(fds[j+1])),'live parent chain immediately before mutation')
                need(inode(os.stat(str(i),dir_fd=stage_fd,follow_symlinks=False))==inode(os.fstat(prepared[n])) and held(prepared[n])==buffers[n],'same prepared whole held buffer'); event('PUBLISH_INTENT',path=n,atomic_replacement=n in originals)
                if n in originals:
                    fd=originals[n]; need(inode(os.stat(Path(n).name,dir_fd=fds[-1],follow_symlinks=False))==inode(os.fstat(fd)),'same held original before atomic replacement')
                    need(held(fd)==read(backups/n),'durable whole original backup'); os.replace(str(i),Path(n).name,src_dir_fd=stage_fd,dst_dir_fd=fds[-1])
                else:
                    if rename(stage_fd,os.fsencode(str(i)),fds[-1],os.fsencode(Path(n).name),4):
                        error=ctypes.get_errno(); raise OSError(error,os.strerror(error))
                os.fsync(stage_fd); os.fsync(fds[-1]); need(inode((W/n).lstat())==inode(os.fstat(prepared[n])) and read(W/n)==buffers[n] and mode(W/n)==0o644,'published exact held identity/bytes/mode'); completed.append(n); event('PUBLISH_COMPLETE',path=n)
            finally:
                for fd in reversed(fds): os.close(fd)
        current(); verified=preflight(True); need(verified[5]==old,'Git index unchanged after filesystem install')
        need(not list(staged.iterdir()) and {f.relative_to(backups).as_posix() for f in backups.rglob('*') if f.is_file()}==set(p['replacement_paths']),'complete15 staged/two relative-backup extent')
        result={'status':'FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT','counts':[760,123,124],'plan_SHA256':PLAN_SHA,'authorization_SHA256':sha(auth_raw),'nonce':a['nonce'],'helper_SHA256':sha(read(N/'release_two.py')),'targets':sorted(buffers),'W_index_unchanged':True,'Math_HEAD_index_unchanged':True,'Git_deploy_Sheet_actions':False,'transaction':str(t),'new_lock_retained':True,'old_runtime_never_reused':True}
        new_file(t/'SUCCESS.json',packed(result)); event('FILESYSTEM_SUCCESS',**result); return result
    except BaseException as error:
        event('STOPPED_PARTIAL_STATE_PRESERVED',error=repr(error),completed_targets=completed,created_directories=made,automatic_rollback=False); raise
    finally:
        for fd in reversed(opened): os.close(fd)
        os.close(lock_fd)

def tree_entries(tree):
    records=git('ls-tree','-r','-z','--full-tree',tree).split(b'\0'); need(records.pop()==b'','whole tree list'); result={}
    for record in records:
        header,name=record.split(b'\t',1); need(name not in result,'unique tree leaf'); result[name]=header
    return result

def publish(snapshot):
    p,buffers,old_files,old_dirs,new_dirs,old,fp,state=snapshot; need(state['installed'],'publish requires installed phase')
    path,auth_raw,a,expiry=authorization('Git',fp,p); t,check,lock_fd=transaction('Git',auth_raw); native_owner=None; ref_attempted=False
    def current():
        check(); need(read(path)==auth_raw and datetime.datetime.fromisoformat(a['issued_UTC'])<=utc()<expiry and sha(read(N/'PLAN.json'))==PLAN_SHA and sha(read(N/'release_two.py'))==a['helper_SHA256'],'same current Git authority/code')
    try:
        current(); routing(p,state['routing']); current(); need(git('ls-remote','--exit-code','origin',p['branch'])==(p['website_HEAD']+'\t'+p['branch']+'\n').encode(),'remote parent exact')
        native=t/'native-successor.index'; commit_index=t/'commit.index'; new_file(t/'shared-index.before',old); new_file(native,old)
        oids={n:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() for n,b in buffers.items()}
        for n,b in sorted(buffers.items()): current(); need(git('hash-object','--no-filters','-w','--stdin',data=b).strip().decode()==oids[n],'exact unfiltered blob')
        info=b''.join(('100644 '+oids[n]+'\t'+n).encode()+b'\0' for n in sorted(buffers))
        git('update-index','--add','-z','--index-info',data=info,index=native)
        git('read-tree',p['website_tree'],index=commit_index); git('update-index','--add','-z','--index-info',data=info,index=commit_index)
        tree=git('write-tree',index=commit_index).strip().decode(); staged=read(native); before,before_extension=entries(old); after,after_extension=entries(staged); targets={n.encode() for n in buffers}
        need(len(after)==58700 and set(after)==set(before)|targets and sum(n not in targets for n in before)==58685,'exact58700/58685 raw scope')
        need(all(after[n]==record for n,record in before.items() if n not in targets),'all58685untargeted full raw records exact')
        need(all(after[n.encode()][1:]==(struct.pack('>I',0o100644),bytes.fromhex(oids[n])) for n in buffers),'all15index blob/mode targets')
        def record_tree(records):
            result={}
            for name,record in records.items():
                bits=struct.unpack('>I',record[1])[0]; need(bits in (0o100644,0o100755,0o120000,0o160000),'ordinary index tree mode')
                result[name]=(format(bits,'06o')+' '+('commit' if bits==0o160000 else 'blob')+' '+record[2].hex()).encode()
            return result
        before_check=t/'before-semantic.index'; after_check=t/'after-semantic.index'
        new_file(before_check,old); new_file(after_check,staged)
        native_before=tree_entries(git('write-tree',index=before_check).strip().decode())
        native_tree=git('write-tree',index=after_check).strip().decode(); native_after=tree_entries(native_tree)
        need(native_before==record_tree(before) and native_after==record_tree(after),'isolated Git trees equal all raw index path/OID/mode semantics; derived TREE may invalidate/rebuild/drop')
        need(read(native)==staged and read(W/'.git/index')==old,'semantic cache rebuilds confined to separate private checking indices')
        event('NATIVE_SEMANTICS_VERIFIED',native_successor_tree=native_tree,TREE_extension_before=pin(before_extension),TREE_extension_after=pin(after_extension),TREE_extension_changed=before_extension!=after_extension)
        bt,at=tree_entries(p['website_tree']),tree_entries(tree)
        foreign=lambda native,head:{n:(native.get(n),head.get(n)) for n in (set(native)|set(head))-targets if native.get(n)!=head.get(n)}
        need(foreign(native_before,bt)==foreign(native_after,at),'all foreign staging differences preserved against successor commit')
        need(set(at)==set(bt)|targets and all(at[n]==record for n,record in bt.items() if n not in targets),'all untargeted HEAD tree records exact plus thirteen additions')
        delta=git('diff-tree','--raw','-r','--no-commit-id','--no-abbrev','--no-renames','--no-ext-diff','-z',p['website_tree'],tree).split(b'\0'); need(delta.pop()==b'' and len(delta)==30,'exact15tree delta')
        need({delta[i+1] for i in range(0,30,2)}==targets,'only fixed15paths in commit')
        need(all(delta[i].split()[1]==b'100644' and delta[i].split()[3].decode()==oids[delta[i+1].decode()] for i in range(0,30,2)),'all commit bytes/modes')
        need(all(delta[i].split()[4]==(b'M' if delta[i+1].decode() in p['replacement_paths'] else b'A') for i in range(0,30,2)),'exact13A2M; no unrelated additions/deletions')
        current(); lock=W/'.git/index.lock'; fd=os.open(lock,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600); os.fchmod(fd,0o644); native_owner=inode(os.fstat(fd))
        try: write_all(fd,staged); os.fsync(fd); need(held(fd)==staged,'whole durable index successor')
        finally: os.close(fd)
        sync_dir(W/'.git'); event('SHARED_INDEX_LOCKED_DURABLE',owner=native_owner)
        current(); need(preflight(True,native_owner)[6]==fp,'full final source/public/index/HEAD/Math fence under lock'); current()
        identity={f'GIT_{role}_{key}':a[value] for role in ('AUTHOR','COMMITTER') for key,value in [('NAME','author_name'),('EMAIL','author_email'),('DATE','commit_date')]}
        commit=git('commit-tree',tree,'-p',p['website_HEAD'],data=(p['commit_message']+'\n').encode(),identity=identity).strip().decode(); event('COMMIT_OBJECT',commit=commit,tree=tree)
        current(); need(git('rev-parse','HEAD').strip().decode()==p['website_HEAD'] and read(W/'.git/index')==old,'final CAS/index old state'); math_fence(p)
        current(); event('CAS_REF_INTENT',commit=commit); ref_attempted=True; git('update-ref',p['branch'],commit,p['website_HEAD']); event('CAS_REF_COMPLETE',commit=commit)
        current(); need(inode(lock.lstat())==native_owner and read(lock)==staged and mode(lock)==0o644,'own durable index lock before replacement')
        os.replace(lock,W/'.git/index'); sync_dir(W/'.git'); event('INDEX_ATOMIC_REPLACEMENT_COMPLETE',SHA256=sha(staged))
        def final_local():
            need(read(W/'.git/index')==staged and mode(W/'.git/index')==0o644 and git('rev-parse',p['branch']).strip().decode()==commit,'exact final W ref/index')
            need(entries(read(W/'.git/index'))==(after,after_extension) and tree_entries(commit)==at and all(native_after[n]==at[n] for n in targets),'postshared-index raw/staged target semantics equal new commit; foreign staging unchanged')
            need(git('symbolic-ref','HEAD').strip().decode()==p['branch'],'existing master retained'); public_fence(p,buffers,old_files,old_dirs,new_dirs,True); math_fence(p); contract()
        current(); final_local(); current(); routing(p,state['routing']); current(); git('push','--no-follow-tags','--recurse-submodules=no','origin',commit+':'+p['branch'])
        current(); routing(p,state['routing']); current(); need(git('ls-remote','--exit-code','origin',p['branch'])==(commit+'\t'+p['branch']+'\n').encode(),'remote immutable commit verified'); final_local()
        result={'status':'SCOPED15_COMMIT_AND_PUSH_VERIFIED','authorization_SHA256':sha(auth_raw),'nonce':a['nonce'],'plan_SHA256':PLAN_SHA,'helper_SHA256':sha(read(N/'release_two.py')),'commit':commit,'tree':tree,'paths':15,'delta':'13A2M','protected_full_raw_records':58685,'successor_index_records':58700,'index_SHA256':sha(staged),'index_mode':'0644','native_successor_semantic_tree':native_tree,'TREE_extension_before':pin(before_extension),'TREE_extension_after':pin(after_extension),'TREE_extension_changed':before_extension!=after_extension,'foreign_staging_semantics_preserved':True,'Math_HEAD_index_unchanged':True,'deployment_or_Sheet_actions':False,'new_Git_lock_retained':True,'old_runtime_never_reused':True}
        new_file(t/'SUCCESS.json',packed(result)); event('GIT_SUCCESS',**result); return result
    except BaseException as error:
        event('STOPPED_GIT_STATE_PRESERVED',error=repr(error),CAS_attempted=ref_attempted,index_lock_owner=native_owner,automatic_rollback=False); raise
    finally: os.close(lock_fd)

def main():
    args=sys.argv[1:]
    need(args in [[],['--preflight'],['--verify-installed'],['--install'],['--publish']],'literal default or four explicit modes')
    if not args:
        print(json.dumps({'status':'NO_ACTION_EXPLICIT_ROOT_MODE_REQUIRED','writes':0,'repository_reads':0,'Git_commands':0,'remote_calls':0,'authority_inferred':False}))
        return
    snapshot=preflight(True if args==['--verify-installed'] else None)
    if args==['--install']: result=install(snapshot)
    elif args==['--publish']: result=publish(snapshot)
    else:
        p,buffers,old_files,old_dirs,new_dirs,old,fp,state=snapshot
        result={'status':'READONLY_INSTALLED_PREFLIGHT' if state['installed'] else 'READONLY_PREINSTALL_PREFLIGHT','preflight_SHA256':fp,'helper_SHA256':sha(read(N/'release_two.py')),'plan_SHA256':PLAN_SHA,'counts':state['counts'],'fixed_paths':sorted(TARGETS),'new_leaves':13,'replacements':2,'protected_raw_records':58685,'successor_records_if_published':58700,'routing':state['routing'],'baseline_TREE_extension':state['baseline_TREE_extension'],'protected_raw_buffer':state['protected_raw_records'],'writes':0,'remote_checked':False,'authority_inferred':False,'read_events':list(TRACE)}
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    try: main()
    except BaseException as error:
        event('FAILED_HISTORY_RETAINED',error=repr(error))
        print(json.dumps({'status':'STOPPED_STATE_RETAINED','error':repr(error),'pretransaction_read_events':TRACE,'automatic_rollback':False}),file=sys.stderr)
        raise
