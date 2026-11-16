#!/usr/bin/env python3
"""Fixed18 16A2M private production preparation. Default is a literal no-action response.

--install and --publish are distinct, separately root-authorized transactions.
Explicit preflights are offline; install/Git require separate current root authority.
No project import, deploy, Sheet or lock release.
Failures preserve partial state/journals/locks; no automatic rollback/retry.
"""
from pathlib import Path
import base64, ctypes, datetime, hashlib, json, os, re, stat, struct, subprocess, sys
import xml.etree.ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M = P.parent
N = P/'verification/odd-areas-boolean-city-production-sol-20261116'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
PLAN_SHA = '04bedcae80908b0b772c319ef12ef8b35a533f4cc3fd110d04443737f5b453fd'
LOG = None
ENV = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_OPTIONAL_LOCKS='0', GIT_INDEX_VERSION='2', GIT_TERMINAL_PROMPT='0')
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
def event(phase,**fields):
    if LOG is not None:
        LOG.write(packed({'UTC':utc().isoformat(),'phase':phase,**fields})); LOG.flush(); os.fsync(LOG.fileno())
def git(*args,data=None,index=None,identity=None,cwd=W,opaque=False,absent_origin_vcs_ok=False):
    env=dict(ENV)
    if index is not None: env['GIT_INDEX_FILE']=str(index)
    if identity: env.update(identity)
    cmd=['git','--no-optional-locks',*GIT_OPTIONS,*args]; r=subprocess.run(cmd,cwd=cwd,env=env,input=data,capture_output=True)
    event('git',argv=cmd,input_SHA256=None if data is None else sha(data),exit=r.returncode,stdout_SHA256=sha(r.stdout),stderr_SHA256=sha(r.stderr),stdout_base64=None if opaque else base64.b64encode(r.stdout).decode(),stderr_base64=None if opaque else base64.b64encode(r.stderr).decode())
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

def contract():
    need(Path(__file__).absolute()==N/'release_four.py','fixed current helper location')
    raw=read(N/'PLAN.json'); need(sha(raw)==PLAN_SHA,'exact plan'); p=json.loads(raw)
    need(p.get('root_adoption_state')=='ROOT_PROVIDED_AND_ADOPTED' and isinstance(p.get('root_adoption'),dict),'independent stage PASS and actual root adoption required; pending preparation is not authority')
    need(p['root_adoption']['path']==p['root_adoption_expected_path'],'exact root receipt path')
    adoption=json.loads(bound(p['root_adoption']))
    need(adoption['status']==p['root_adoption_required_status'] and adoption['production_install_Git_deploy_or_tracker_authority'] is False,'private stage adoption only')
    need(adoption['independent_stage_audit_PASS'] is True and isinstance(adoption['independent_stage_audit_FINAL'],dict),'root-adopted independent integration PASS required')
    bound(adoption['independent_stage_audit_FINAL'])
    need(adoption['stage_FINAL']==p['stage_FINAL'] and adoption['stage_manifest']==p['stage_manifest'] and adoption['public_payloads']==p['public_payloads'],'exact adopted stage/manifest/public payloads')
    need(sorted(adoption['candidate_exact_paths'])==p['scope_paths'],'exact root-adopted eighteen scope paths')
    reading=json.loads(bound(p['root_stage_reading'])); need(reading['production_execution_authority'] is False,'earlier reading receipt is preparation only')
    S=P/p['stage']; seal=json.loads(bound(p['stage_FINAL'])); manifest=json.loads(bound(p['stage_manifest']))
    need(p['stage_manifest']['path']==p['stage']+'/MANIFEST.json' and all(p['stage_manifest'][k]==seal['manifest'][k] for k in ('bytes','SHA256')),'actual stage manifest schema and pin')
    need(seal['status']=='PASS_PRIVATE_18_PATH_STAGE_PREPARED_NOT_INSTALLED' and seal['production_install_Git_deploy_tracker_or_publication_authority'] is False,'private source stage only')
    terminals={'MANIFEST.json','FINAL.json'}; rows_manifest=manifest['files']; expected_names=terminals|{x['path'] for x in rows_manifest}
    need(set(manifest['exact_existing_root_terminal_controls_excluded'])==terminals and len(rows_manifest)==38 and len(expected_names)==40 and seal['finite_extent']['regular_files']==40 and seal['finite_extent']['child_directories']==7,'exact38payload/40file/7directory source stage')
    for row in rows_manifest:
        name=row['path']; need('..' not in Path(name).parts and not Path(name).is_absolute(),'finite stage source path')
        need(pin(read(S/name))=={k:row[k] for k in ('bytes','SHA256')},'whole frozen stage payload')
    sf,sd=census(S); need(set(sf)==expected_names and len(sf)==40 and len(sd)==8,'immutable source stage40/7')
    need(set(sd)-{'.'}=={x['path'] for x in manifest['directories']} and all(x['mode']==0o644 for x in sf.values()) and set(sd.values())=={0o755},'stage source types/modes')
    need(p['source_guards']==p['baseline'] and p['source_guards']['path']==p['stage']+'/BASELINE.json','bound28-source guard container')
    baseline=json.loads(bound(p['baseline'])); guards=baseline['source_guards']
    need(len(guards)==p['source_guard_count']==28,'complete fixed source guard table in bound container')
    for row in guards:
        bound(row); need(mode(Path(row['path']))==int(row['mode'],8),'source mode unchanged')
    need(p['root_editorial_adoptions']==seal['root_copy_adoptions'],'same four editorial adoptions')
    for row in p['root_editorial_adoptions']: bound(row)
    need(baseline['website_git']['HEAD']['commit']==p['website_HEAD'] and baseline['website_tree_previously_read']==p['website_tree'] and baseline['website_git']['index']['SHA256']==p['website_index']['SHA256'],'same fresh711 baseline authority')
    old_files={r['path']:{**{k:r[k] for k in ('bytes','SHA256')},'mode':int(r['mode'],8)} for r in baseline['public_files']}
    old_dirs={r['path']:int(r['mode'],8) for r in baseline['public_directory_modes_including_root']}
    need(len(old_files)==baseline['current_public_count']==711 and len(old_dirs)==360 and baseline['current_public_child_directory_count']==359,'exact711/360 public baseline/modes')
    payloads=json.loads(bound(p['public_payloads'])); need(payloads==seal['whole_public_payload_bindings'] and len(payloads)==18,'same exact eighteen public buffers')
    rows=payloads; names=[r['website_relative_path'] for r in rows]
    need(len(rows)==len(set(names))==18 and sorted(names)==p['scope_paths'] and p['new_leaves']==16 and p['replacements']==2,'fixed eighteen paths16A2M')
    need(p['replacement_paths']==['public/research/index.html','public/research/sitemap.xml'],'only two aggregate replacements')
    buffers={}
    for row in rows:
        name=row['website_relative_path']; need(name.startswith('public/research/') and '..' not in Path(name).parts and not Path(name).is_absolute(),'finite exact public research path')
        b=read(S/'candidate'/name); need(pin(b)=={k:row[k] for k in ('bytes','SHA256')} and row['mode']=='0644','exact candidate bytes/mode'); buffers[name]=b
        need((name[7:] in old_files)==(name in p['replacement_paths']),'sixteen absent new targets/two existing aggregates')
    index=buffers['public/research/index.html'].decode()
    visible=re.findall(r'<li\b[^>]*>[\s\S]*?</li>',index); rawjson=re.search(r'<script type="application/ld\+json">(.*?)</script>',index,re.S)[1]; entity=json.loads(rawjson)['mainEntity']
    nodes=re.findall(r'<url>[\s\S]*?</url>',buffers['public/research/sitemap.xml'].decode())
    need(len(visible)==len(entity['itemListElement'])==entity['numberOfItems']==118 and len(nodes)==119,'candidate118/119 actual aggregates')
    for units,old_units,count in [(visible,baseline['visible_items_raw'],114),(typed_spans(rawjson),typed_spans(baseline['typed_script_complete_raw']),114),(nodes,baseline['sitemap_nodes_raw'],115)]:
        need(len(old_units)==count and units[:count]==old_units,'whole old114 visible/raw-typed items and115 XML nodes preserved')
    for row in baseline['website_configuration_guards']+baseline['template_guards']: bound(row); need(mode(Path(row['path']))==int(row['mode'],8),'website source/config mode')
    for k in ('old_completed_lock','old_SUCCESS','old_install_authorization','old_Git_lock','old_Git_SUCCESS','old_Git_authorization','old_publication'): bound(p[k])
    oldsuccess=json.loads(bound(p['old_SUCCESS'])); need(oldsuccess['counts']==[711,114,115] and oldsuccess['authorization_SHA256']==p['old_install_authorization']['SHA256'],'completed prior711 installation context')
    oldgit=json.loads(bound(p['old_Git_SUCCESS']))
    need(oldgit['status']=='SCOPED18_COMMIT_AND_PUSH_VERIFIED' and oldgit['delta']=='12A2M' and oldgit['commit']==p['website_HEAD'] and oldgit['tree']==p['website_tree'] and oldgit['index_SHA256']==p['previous_published_native_index']['SHA256'] and oldgit['index_mode']=='0600' and oldgit['successor_index_records']==58651,'completed prior f632/0f58 context, not fresh-index continuity')
    transition=json.loads(bound(p['index_transition']))
    need(transition['status']=='OBSERVED_STAT_CACHE_AND_NATIVE_FILE_MODE_TRANSITION_NO_STAGING_CONTENT_CHANGE' and transition['current_native_index']=={'bytes':p['website_index']['bytes'],'SHA256':p['website_index']['SHA256'],'mode':'0644'} and transition['records']==58651 and transition['path_object_ID_mode_flags_stage_and_padding_semantic_differences']==[] and transition['only_record_stat_fields_changed'] is True,'root adopted fresh8db8/0644 baseline')
    publication=json.loads(bound(p['old_publication']))
    need(publication['website_commit']==p['website_HEAD'] and publication['tree']==p['website_tree'] and publication['hosting_version']==p['old_hosting_version'],'prior exact hosting context')
    new_dirs=set()
    for name in buffers: new_dirs.update(q.as_posix() for q in Path(name[7:]).parents if q.as_posix() not in old_dirs)
    need(new_dirs=={'research/odd-period-pedal-antipedal-area-product','research/outer-focal-inversion-area-product','research/boolean-cube-polynomial-compatibility','research/fixed-city-quantitative-persistence'} and len(new_dirs)==p['new_directories']==4,'only four necessary new directories')
    return p,buffers,old_files,old_dirs,new_dirs

def math_fence(p):
    b=read(M/'.git/index'); need(pin(b)=={k:p['Math_index'][k] for k in ('bytes','SHA256')} and mode(M/'.git/index')==p['Math_index']['mode'],'Math shared index exact')
    need(pin(read(M/'.git/config'))==p['Math_config'] and mode(M/'.git/config')==0o644,'Math config exact')
    need(sha(read(M/'.git/HEAD'))==p['Math_HEAD_file_SHA256'] and git('rev-parse','HEAD',cwd=M).strip().decode()==p['Math_HEAD'],'Math localHEAD unchanged')

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
    need(git('symbolic-ref','HEAD').strip().decode()==p['branch'] and git('rev-parse','HEAD').strip().decode()==p['website_HEAD'] and git('rev-parse','HEAD^{tree}').strip().decode()==p['website_tree'],'existing Wmaster/parent/tree')
    need(git('rev-parse','--show-object-format').strip()==b'sha1','SHA1 repository')
    need(pin(read(W/'.git/config'))==p['website_config'] and mode(W/'.git/config')==0o644,'same local origin/config')
    route=routing(p)
    need(sha(read(W/'firebase.json'))==p['firebase_config_SHA256'] and mode(W/'firebase.json')==0o644,'unchanged hosting config')
    old=read(W/'.git/index'); need(pin(old)=={k:p['website_index'][k] for k in ('bytes','SHA256')} and mode(W/'.git/index')==0o644,'exact fresh Windex0644')
    er,extension=entries(old); need(pin(extension)=={k:p['baseline_extension'][k] for k in ('bytes','SHA256')} and len(old)-20-len(extension)==p['baseline_extension']['offset'],'exact baseline TREE extension')
    targets={n.encode() for n in buffers}; replacements={n.encode() for n in p['replacement_paths']}
    need(len(er)==58651 and set(er)&targets==replacements and len(replacements)==2 and len(targets-set(er))==16 and len(set(er)-targets)==58649,'original index2M/16A scope and58649protected records')
    lock=W/'.git/index.lock'
    need(not os.path.lexists(lock) if owned_index_lock is None else inode(lock.lstat())==owned_index_lock,'exclusive Git index lock state')
    installed=all((W/n).is_file() and pin(read(W/n))==pin(b) for n,b in buffers.items())
    actual,counts=public_fence(p,buffers,old_files,old_dirs,new_dirs,installed)
    if required is not None: need(installed==required,'required installed/preinstall phase')
    identities={n:[*inode((W/n).lstat()),(W/n).lstat().st_mtime_ns,(W/n).lstat().st_ctime_ns] for n in p['replacement_paths']}
    state={'installed':installed,'plan_SHA256':PLAN_SHA,'helper_SHA256':sha(read(N/'release_four.py')),'adoption':p['root_adoption'],'public':actual,'counts':counts,'W_HEAD':p['website_HEAD'],'W_tree':p['website_tree'],'W_index':pin(old),'Math_HEAD':p['Math_HEAD'],'Math_index':p['Math_index'],'routing':route,'aggregate_identities':identities,'scope':[(n,pin(b)) for n,b in sorted(buffers.items())]}
    return p,buffers,old_files,old_dirs,new_dirs,old,sha(packed(state)),state

def authorization(kind,fp,p):
    path=N/p['authorization_paths'][kind]; raw=read(path); a=json.loads(raw)
    fixed={'schema':'odd-areas-boolean-city-root-authorization-v1','action':'INSTALL_EXACT18_FILESYSTEM' if kind=='install' else 'PUBLISH_EXACT18_GIT','plan_SHA256':PLAN_SHA,'helper_SHA256':sha(read(N/'release_four.py')),'root_adoption':p['root_adoption'],'preflight_SHA256':fp,'scope_paths':p['scope_paths'],'concurrency':'ROOT_SERIALIZED_NO_OTHER_W_WRITER','old_lock_disposition':p['lock_disposition'],'deployment_authorized':False,'Sheet_authorized':False,'AA':None,'follow_up':None}
    extras={'expires_UTC'} if kind=='install' else {'expires_UTC','author_name','author_email','commit_date','installation_SUCCESS'}
    need(set(a)==set(fixed)|extras and all(a[k]==v for k,v in fixed.items()),'exact separate root '+kind+' authorization')
    expiry=datetime.datetime.fromisoformat(a['expires_UTC']); need(expiry.utcoffset() is not None and utc()<expiry,'unexpired timezone-qualified authority')
    if kind=='Git':
        for k in ('author_name','author_email','commit_date'): need(isinstance(a[k],str) and a[k] and '\n' not in a[k] and '\0' not in a[k],'literal commit identity/date')
        need(datetime.datetime.fromisoformat(a['commit_date']).utcoffset() is not None,'timezone-qualified commit date')
        success=json.loads(bound(a['installation_SUCCESS'])); success_path=Path(a['installation_SUCCESS']['path'])
        need(success_path.is_relative_to(N/'transactions') and success_path.name=='SUCCESS.json','current effort install receipt')
        need(success['status']=='FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT' and success['counts']==[727,118,119] and success['plan_SHA256']==PLAN_SHA,'completed exact new installation')
    return path,raw,a,expiry

def transaction(kind,auth_raw):
    global LOG
    safe(N); need(W.stat().st_dev==N.stat().st_dev,'same filesystem')
    lock=N/('ACTIVE_INSTALL.lock' if kind=='install' else 'ACTIVE_GIT.lock')
    body=packed({'protocol':'odd-areas-boolean-city-'+kind+'-v1','authorization_SHA256':sha(auth_raw),'PID':os.getpid()}); new_file(lock,body)
    lock_fd=os.open(lock,os.O_RDONLY|os.O_NOFOLLOW); owner=inode(os.fstat(lock_fd))
    parent=N/('transactions' if kind=='install' else 'git-transactions')
    if not os.path.lexists(parent): parent.mkdir(mode=0o700); sync_dir(N)
    safe(parent); need(stat.S_ISDIR(parent.lstat().st_mode) and mode(parent)==0o700,'ordinary private transaction parent')
    t=parent/sha(auth_raw); t.mkdir(mode=0o700); sync_dir(parent)
    fd=os.open(t/'journal.jsonl',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600); os.fchmod(fd,0o600); LOG=os.fdopen(fd,'wb'); sync_dir(t)
    def check(): need(inode(lock.lstat())==owner and held(lock_fd)==body and mode(lock)==0o600,'held exact new transaction lock')
    check(); event('AUTHORIZED',kind=kind,authorization_SHA256=sha(auth_raw)); return t,check,lock_fd

def install(snapshot):
    p,buffers,old_files,old_dirs,new_dirs,old,fp,state=snapshot; path,auth_raw,a,expiry=authorization('install',fp,p)
    need(not state['installed'] and sys.platform=='darwin','preinstall Darwin only')
    t,check,lock_fd=transaction('install',auth_raw); opened=[]; made={}; completed=[]
    libc=ctypes.CDLL('/usr/lib/libSystem.B.dylib',use_errno=True); rename=libc.renameatx_np
    rename.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint]; rename.restype=ctypes.c_int
    def current():
        check(); need(read(path)==auth_raw and utc()<expiry and sha(read(N/'PLAN.json'))==PLAN_SHA and sha(read(N/'release_four.py'))==a['helper_SHA256'],'same current installation authority/code')
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
        absent=sorted(set(buffers)-set(p['replacement_paths'])); need(len(absent)==16 and all(not os.path.lexists(W/n) for n in absent),'sixteen original target absences')
        new_file(t/'new-targets.before.json',packed({n:'ABSENT' for n in absent}))
        new_file(t/'rollback.before.json',packed({'original_replacements':{n:old_files[n[7:]] for n in p['replacement_paths']},'original_new_target_state':{n:'ABSENT' for n in absent},'original_new_directories':{n:'ABSENT' for n in sorted(new_dirs)},'original_index':pin(old),'recovery':'STOP_AND_ROOT_REVIEW_NO_AUTOMATIC_ROLLBACK_OR_RETRY'}))
        sync_dir(staged); sync_dir(backups); sync_dir(t); event('ALL18_BUFFERS_2_RELATIVE_BACKUPS_16_ABSENCES_ROLLBACK_INPUTS_DURABLE_BEFORE_W_WRITE')
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
        need(not list(staged.iterdir()) and {f.relative_to(backups).as_posix() for f in backups.rglob('*') if f.is_file()}==set(p['replacement_paths']),'complete18 staged/two relative-backup extent')
        result={'status':'FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT','counts':[727,118,119],'plan_SHA256':PLAN_SHA,'authorization_SHA256':sha(auth_raw),'helper_SHA256':sha(read(N/'release_four.py')),'targets':sorted(buffers),'W_index_unchanged':True,'Math_HEAD_index_unchanged':True,'Git_deploy_Sheet_actions':False,'transaction':str(t),'new_lock_retained':True,'old_completed_lock_untouched':True}
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
        check(); need(read(path)==auth_raw and utc()<expiry and sha(read(N/'PLAN.json'))==PLAN_SHA and sha(read(N/'release_four.py'))==a['helper_SHA256'],'same current Git authority/code')
    try:
        current(); routing(p,state['routing']); current(); need(git('ls-remote','--exit-code','origin',p['branch'])==(p['website_HEAD']+'\t'+p['branch']+'\n').encode(),'remote parent exact')
        native=t/'native-successor.index'; commit_index=t/'commit.index'; new_file(t/'shared-index.before',old); new_file(native,old)
        oids={n:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() for n,b in buffers.items()}
        for n,b in sorted(buffers.items()): current(); need(git('hash-object','--no-filters','-w','--stdin',data=b).strip().decode()==oids[n],'exact unfiltered blob')
        info=b''.join(('100644 '+oids[n]+'\t'+n).encode()+b'\0' for n in sorted(buffers))
        git('update-index','--add','-z','--index-info',data=info,index=native)
        git('read-tree',p['website_tree'],index=commit_index); git('update-index','--add','-z','--index-info',data=info,index=commit_index)
        tree=git('write-tree',index=commit_index).strip().decode(); staged=read(native); before,before_extension=entries(old); after,after_extension=entries(staged); targets={n.encode() for n in buffers}
        need(len(after)==58667 and set(after)==set(before)|targets and sum(n not in targets for n in before)==58649,'exact58667/58649 raw scope')
        need(all(after[n]==record for n,record in before.items() if n not in targets),'all58649untargeted full raw records exact')
        need(all(after[n.encode()][1:]==(struct.pack('>I',0o100644),bytes.fromhex(oids[n])) for n in buffers),'all18index blob/mode targets')
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
        need(set(at)==set(bt)|targets and all(at[n]==record for n,record in bt.items() if n not in targets),'all untargeted HEAD tree records exact plus sixteen additions')
        delta=git('diff-tree','--raw','-r','--no-commit-id','--no-abbrev','--no-renames','--no-ext-diff','-z',p['website_tree'],tree).split(b'\0'); need(delta.pop()==b'' and len(delta)==36,'exact18tree delta')
        need({delta[i+1] for i in range(0,36,2)}==targets,'only fixed18paths in commit')
        need(all(delta[i].split()[1]==b'100644' and delta[i].split()[3].decode()==oids[delta[i+1].decode()] for i in range(0,36,2)),'all commit bytes/modes')
        need(all(delta[i].split()[4]==(b'M' if delta[i+1].decode() in p['replacement_paths'] else b'A') for i in range(0,36,2)),'exact16A2M; no unrelated additions/deletions')
        current(); lock=W/'.git/index.lock'; fd=os.open(lock,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600); os.fchmod(fd,0o644); native_owner=inode(os.fstat(fd))
        try: write_all(fd,staged); os.fsync(fd); need(held(fd)==staged,'whole durable index successor')
        finally: os.close(fd)
        sync_dir(W/'.git'); event('SHARED_INDEX_LOCKED_DURABLE',owner=native_owner)
        current(); need(preflight(True,native_owner)[6]==fp,'full final source/public/index/HEAD/Math fence under lock')
        identity={f'GIT_{role}_{key}':a[value] for role in ('AUTHOR','COMMITTER') for key,value in [('NAME','author_name'),('EMAIL','author_email'),('DATE','commit_date')]}
        commit=git('commit-tree',tree,'-p',p['website_HEAD'],data=(p['commit_message']+'\n').encode(),identity=identity).strip().decode(); event('COMMIT_OBJECT',commit=commit,tree=tree)
        current(); need(git('rev-parse','HEAD').strip().decode()==p['website_HEAD'] and read(W/'.git/index')==old,'final CAS/index old state'); math_fence(p)
        event('CAS_REF_INTENT',commit=commit); ref_attempted=True; git('update-ref',p['branch'],commit,p['website_HEAD']); event('CAS_REF_COMPLETE',commit=commit)
        need(inode(lock.lstat())==native_owner and read(lock)==staged and mode(lock)==0o644,'own durable index lock before replacement')
        os.replace(lock,W/'.git/index'); sync_dir(W/'.git'); event('INDEX_ATOMIC_REPLACEMENT_COMPLETE',SHA256=sha(staged))
        def final_local():
            need(read(W/'.git/index')==staged and mode(W/'.git/index')==0o644 and git('rev-parse',p['branch']).strip().decode()==commit,'exact final W ref/index')
            need(entries(read(W/'.git/index'))==(after,after_extension) and tree_entries(commit)==at and all(native_after[n]==at[n] for n in targets),'postshared-index raw/staged target semantics equal new commit; foreign staging unchanged')
            need(git('symbolic-ref','HEAD').strip().decode()==p['branch'],'existing master retained'); public_fence(p,buffers,old_files,old_dirs,new_dirs,True); math_fence(p); contract()
        current(); final_local(); current(); routing(p,state['routing']); current(); git('push','--no-follow-tags','--recurse-submodules=no','origin',commit+':'+p['branch'])
        current(); routing(p,state['routing']); current(); need(git('ls-remote','--exit-code','origin',p['branch'])==(commit+'\t'+p['branch']+'\n').encode(),'remote immutable commit verified'); final_local()
        result={'status':'SCOPED18_COMMIT_AND_PUSH_VERIFIED','commit':commit,'tree':tree,'paths':18,'delta':'16A2M','protected_full_raw_records':58649,'successor_index_records':58667,'index_SHA256':sha(staged),'index_mode':'0644','native_successor_semantic_tree':native_tree,'TREE_extension_before':pin(before_extension),'TREE_extension_after':pin(after_extension),'TREE_extension_changed':before_extension!=after_extension,'foreign_staging_semantics_preserved':True,'Math_HEAD_index_unchanged':True,'deployment_or_Sheet_actions':False,'new_Git_lock_retained':True,'old_completed_lock_untouched':True}
        new_file(t/'SUCCESS.json',packed(result)); event('GIT_SUCCESS',**result); return result
    except BaseException as error:
        event('STOPPED_GIT_STATE_PRESERVED',error=repr(error),CAS_attempted=ref_attempted,index_lock_owner=native_owner,automatic_rollback=False); raise
    finally: os.close(lock_fd)

def main():
    args=sys.argv[1:]
    need(args in [[],['--preflight'],['--verify-installed'],['--install'],['--publish']],'literal default or four explicit finite modes only')
    if not args:
        print(json.dumps({'status':'NO_ACTION_EXPLICIT_MODE_REQUIRED','writes':0,'repository_reads':0,'remote_calls':0,'authority_inferred':False}))
        return
    snapshot=preflight(True if args==['--verify-installed'] else None)
    if args==['--install']: result=install(snapshot)
    elif args==['--publish']: result=publish(snapshot)
    else:
        p,buffers,old_files,old_dirs,new_dirs,old,fp,state=snapshot
        result={'status':'READONLY_INSTALLED_PREFLIGHT_PASS' if state['installed'] else 'READONLY_PREINSTALL_PREFLIGHT_PASS','preflight_SHA256':fp,'helper_SHA256':sha(read(N/'release_four.py')),'plan_SHA256':PLAN_SHA,'counts':state['counts'],'fixed_paths':sorted(buffers),'new_leaves':16,'replacements':2,'protected_raw_records':58649,'successor_raw_records':58667,'W_HEAD':p['website_HEAD'],'Math_HEAD':p['Math_HEAD'],'routing':state['routing'],'baseline_TREE_extension':p['baseline_extension'],'TREE_change_policy':p['extension_policy'],'old_completed_lock_retained':True,'remote_checked':False,'writes':0,'publication_authority_inferred':False}
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    try: main()
    except BaseException as error: event('FAILED_HISTORY_RETAINED',error=repr(error)); raise
