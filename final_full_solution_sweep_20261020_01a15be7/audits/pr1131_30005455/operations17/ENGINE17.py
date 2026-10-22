"""Actual parsed07 lifecycle with fully intercepted provider adapters; no real I/O."""
from pathlib import Path
import contextlib,copy,datetime,hashlib,io,json,os,sys,types

REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW;SOURCE=ROOT/'source';OLD=ROOT.parent/'operations'
MODE='OO' if sys.flags.optimize==2 else 'O' if sys.flags.optimize else 'normal'
DEST=REVIEW/'private'/('final_phase17_'+MODE);DEST.mkdir(exist_ok=False)
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
CONTROL_SHA=sha(Path(__file__).read_bytes())
MS=sha((SOURCE/'SOURCE_MANIFEST.json').read_bytes());BS=sha((SOURCE/'bootstrap17.py').read_bytes())
base=(OLD/'bootstrap.py').read_bytes();need(sha(base)=='960b33e83135968ab40ef069b1b8876df47b70d1c4ef528bf0d8c836213ac58b','Original bootstrap pin')
ns={'__file__':str(OLD/'bootstrap.py'),'__name__':'checked_old_bootstrap'}
exec(compile(base,str(OLD/'bootstrap.py'),'exec',dont_inherit=True,optimize=0),ns)
load,_=ns['load_verified'](OLD,'eab69e53e9d32510bbf00d74c1b94b70542a8b29cf326c42f5d974e510f09d00',sha(base))
model=load('full_controls')  # blocks every real network/process escape before loading07
boot={'__file__':str(SOURCE/'bootstrap17.py'),'__name__':'checked07_bootstrap'}
exec(compile((SOURCE/'bootstrap17.py').read_bytes(),str(SOURCE/'bootstrap17.py'),'exec',dont_inherit=True,optimize=0),boot)
m=boot['load_verified'](SOURCE,MS,BS);c=m.c;pub=m.pl;live=m.live;ir=m.ir
modules={n:m.LOAD05(n) for n in ['ops_common','publish_and_ledger','collect_live','integrate_remote','native_policy']}
c.zenodo.token_for=lambda *a,**k:'OFFLINE_SENTINEL_NO_CREDENTIAL'
c.zenodo.doi_status=lambda doi:{'status':'offline_mock','url':'https://doi.org/'+doi}
results=[];bodies={};actual_durable=c.durable
def archive_completed():
    pass
class World(model.World):
    def command(self,argv,body=None):
        result=super().command(argv,body)
        if self.formula_after and self.appends and argv[:5]==['gws','sheets','spreadsheets','values','batchGetByDataFilter']:
            payload=json.loads(argv[argv.index('--json')+1])
            if payload['valueRenderOption']=='FORMULA':
                value=result['valueRanges'][0]['valueRange']['values'][1][0]
                result['valueRanges'][0]['valueRange']['values'][1][0]='='+json.dumps(value)
        if argv[:4]==['gws','sheets','spreadsheets','batchUpdate']:
            if self.append_reply_style=='actual':result.pop('updatedSpreadsheet',None)
            if self.append_reply_style in {'actual','combined'}:result['commentUpdateState']='NO_UPDATES_REQUESTED'
            if self.final_response_fault:self.final_response_fault(result)
        return result

def world(label):
    archive_completed()
    place=DEST/label;place.mkdir();rt=place/'runtime';pr=place/'private';rt.mkdir();pr.mkdir()
    old=place/'preserved05_runtime';old.mkdir()
    for n in m.F['prior_runtime_files']:(old/n).write_bytes((OLD/'runtime'/n).read_bytes())
    src=place/'checked_source';src.mkdir()
    for p in SOURCE.iterdir():(src/p.name).write_bytes(p.read_bytes())
    m.PRIOR_RUNTIME=old;m.RUNTIME=rt;m.PRIVATE=pr
    m.CONTEXT['source_root']=src
    m.CONTEXT['check_sources']=lambda:boot['source_bytes'](src,MS,BS)
    for module in modules.values():
        module.RUNTIME=rt;module.PRIVATE=pr
    c.zenodo.STATE_DIR=place/'.zenodo-state'
    state_repo=place/'mock_repo';state_repo.mkdir();(state_repo/'.zenodo-state').mkdir()
    live.REPO=state_repo
    w=World(OLD,modules);w.formula_after=False;w.place=place;w.append_reply_style='actual';w.final_response_fault=None
    prior_public=w.native.public
    def observed_public():
        p=prior_public()
        # Only these two authenticated aliases were introduced by the old fake union.
        # Production validates raw provider envelopes and never filters them.
        del p['owner'];del p['record_id'];p['owners']=[{'id':str(w.native.owner)}]
        return p
    w.native.public=observed_public
    helper={'__file__':str(ROOT/'fixture_phase17.py'),'__name__':'inert_phase11_shapes'}
    exec(compile((ROOT/'fixture_phase17.py').read_bytes(),str(ROOT/'fixture_phase17.py'),'exec',dont_inherit=True,optimize=0),helper)
    helper['install_phase_world'](w,m.NATIVE_POLICY.PHASE)
    # Reuse the complete provider models while representing the already accepted
    # merge identity; no integrate/ready/merge operation is executed in07.
    pkg=c.package();flat={c.PROBLEM+'/'+n:pkg['source']['original/'+n] for n in c.ORIGINALS}
    flat.update(c.proposal()[1]);tree=w.git.tree(flat)
    w.git.trees[m.F['merge_tree']]=copy.deepcopy(w.git.trees[tree])
    receipt=json.loads((old/'MERGE_VERIFIED.json').read_bytes())
    w.git.commits[m.MERGE]={'sha':m.MERGE,'tree':{'sha':m.F['merge_tree']},'parents':[{'sha':s} for s in receipt['parents']]}
    w.git.head=m.HEAD;w.git.main=m.MERGE
    w.git.pr.update(state='closed',merged=True,draft=False,merge_commit_sha=m.MERGE,
                    body=c.reviewed_description(m.HEAD)[1])
    original_get=w.git.get
    def get(endpoint):
        if endpoint=='compare/'+m.MERGE+'...main':return {'status':'identical','merge_base_commit':{'sha':m.MERGE}}
        return original_get(endpoint)
    w.git.get=get
    ad=json.loads((SOURCE/'ROOT_CLEARANCE17.example.json').read_bytes())
    ad.update(operations17_sources_sha256=MS,bootstrap17_sha256=BS,publication_ready=True,
              whole17_review_adopted=True,unresolved_findings=[],
              root_confirmed_failure_before_delegate_create=True,initial_create_attempt_was_sent=False,
              allowed_actions=['resume-stage','publish','ledger'],instructions='OFFLINE MODEL ONLY; NO PRODUCTION AUTHORITY')
    w.ad_path=rt/'ROOT_OPERATIONAL_CLEARANCE17.json';w.ad_path.write_text(json.dumps(ad,indent=2)+'\n')
    w.clearance_sha=sha(w.ad_path.read_bytes())
    return w

CLI_INVOCATIONS=[]
def cli(w,action='resume-stage'):
    CLI_INVOCATIONS.append(action)
    args=[action,'--expected-pr-head',m.HEAD,'--clearance-sha256',w.clearance_sha]
    if action!='resume-stage':args+=['--deposit-id','777']
    out=io.StringIO()
    with contextlib.redirect_stdout(out):answer=m.main(args)
    need(json.loads(out.getvalue())==answer,'Parsed CLI output mismatch')
    return answer
def failure(fn):
    try:fn()
    except Exception as e:return {'type':type(e).__name__,'message':str(e)}
    raise RuntimeError('Adverse case accepted')
def allocated():
    seen=set();size=0
    for p in [REVIEW,*REVIEW.rglob('*')]:
        # Other owned mode runs intentionally rename fake approvals atomically.
        # Storage measurement is not a lifecycle/source validation predicate.
        try:s=p.lstat()
        except FileNotFoundError:continue
        key=s.st_dev,s.st_ino
        if key not in seen:size+=s.st_blocks*512;seen.add(key)
    return size
def finish(label,w,error=None,extra=None):
    r={'case':label,'error':error,'native_mutations':list(w.native.calls),'Git_mutations':w.git.writes,
       'appends':w.appends,'stage_verified':(m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),
       'stage_failure':(m.RUNTIME/'RESUME_STAGE_FAILURE.json').exists(),
       'publication_verified':(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists(),
       'ledger_verified':(m.RUNTIME/'LEDGER_VERIFIED.json').exists(),'real_external_mutations':0,**(extra or {})}
    need(not w.git.writes,'10 attempted Git mutation')
    need(allocated()<=10*1024*1024,'New allocation budget exceeded')
    (DEST/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n');results.append(r)
    print(json.dumps({'case':label,'status':'PASS','native_writes':len(w.native.calls),'appends':w.appends}),flush=True)


# The scenarios/adjudications below are independently authored for this review.
# Every case invokes checked_lifecycle17.main (actual parsed command surface).
checks=[]
def record(label,w,expected_ok,answer,error,before,expected_delta,details=None):
    delta={'native':len(w.native.calls)-before[0],'append':w.appends-before[1]}
    ok=(error is None)==expected_ok and delta==expected_delta
    v={'case':label,'status':'PASS' if ok else 'COUNTEREXAMPLE','expected_success':expected_ok,
       'expected_write_delta':expected_delta,'actual_write_delta':delta,'answer':answer,'error':error,
       'native_calls':list(w.native.calls),'appends':w.appends,'Git_writes':list(w.git.writes),
       'stage_verified':(m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),
       'publication_verified':(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists(),
       'ledger_verified':(m.RUNTIME/'LEDGER_VERIFIED.json').exists(),**(details or {})}
    (DEST/(label+'.json')).write_text(json.dumps(v,indent=2)+'\n');checks.append(v)
    need(not w.git.writes,'Unexpected model Git write')
    need(allocated()<10*1024*1024,'Review allocated bytes exceed75MiB')
    print(json.dumps({'case':label,'status':v['status'],'delta':delta,'error':error}),flush=True)
def run(w,action):
    try:return cli(w,action),None
    except Exception as exc:return None,{'type':type(exc).__name__,'message':str(exc)}
def setup(label,phase='stage'):
    w=world(label);c.zenodo.STATE_DIR=live.REPO/'.zenodo-state'
    if phase!='stage':
        with w.installed():
            out,err=run(w,'resume-stage');need(err is None,'Setup stage failure: '+str(err))
            if phase=='ledger':
                out,err=run(w,'publish');need(err is None,'Setup publication failure: '+str(err))
    return w


# VFS scope: large PRIVATE read-only provider captures only. Real runtime
# intents, state, source, approval and private certificate files retain real I/O.
# Changed APIs: c/pl/live/native/ir.durable for eligible capture paths;
# Path.read_bytes for exact captured keys; Path.mkdir for virtual capture dirs.
# No capture stat/hash predicate is bypassed: original actor checks byte hashes
# via read_bytes (served exact original canonical bytes); paths need no stat.
ORIGINAL_PATH_READ=Path.read_bytes
ORIGINAL_PATH_MKDIR=Path.mkdir
MEMORY_PATHS={}
MEMORY_BODIES={}
VIRTUAL_DIRECTORIES=set()
def eligible(path):
    return m.PRIVATE!=ROOT/'private' and m.PRIVATE in path.parents and not path.name.startswith(('certificate_','state_initial_','service_original_'))
def memory_durable(path,value):
    if not eligible(path):return actual_durable(path,value)
    need(not path.is_symlink() and (path.parent==m.PRIVATE or m.PRIVATE in path.parents),'Capture adapter path boundary')
    key=str(path)
    need(key not in MEMORY_PATHS and not path.exists(),'Exclusive virtual capture already exists')
    body=(json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    digest=sha(body)
    if digest in MEMORY_BODIES:need(MEMORY_BODIES[digest]==body,'Virtual content hash collision')
    MEMORY_BODIES[digest]=body;MEMORY_PATHS[key]=digest
    VIRTUAL_DIRECTORIES.add(str(path.parent))
def captured_read(self):
    key=str(self)
    if key in MEMORY_PATHS:return MEMORY_BODIES[MEMORY_PATHS[key]]
    return ORIGINAL_PATH_READ(self)
def captured_mkdir(self,mode=0o777,parents=False,exist_ok=False):
    if m.PRIVATE!=ROOT/'private' and m.PRIVATE in self.parents:
        key=str(self)
        need(exist_ok or key not in VIRTUAL_DIRECTORIES,'Exclusive virtual directory already exists')
        VIRTUAL_DIRECTORIES.add(key);return
    return ORIGINAL_PATH_MKDIR(self,mode=mode,parents=parents,exist_ok=exist_ok)
Path.read_bytes=captured_read
Path.mkdir=captured_mkdir
for module in modules.values():
    if hasattr(module,'durable'):module.durable=memory_durable


import zipfile,stat,gzip,zlib,io,lzma,uuid
ARCHIVES=ROOT/'private'/'case_archives_phase17';ARCHIVES.mkdir(exist_ok=True)
STORE=ROOT/'private/chunks17.zip'
def archive_completed():
    reader_ns={'__file__':str(ROOT/'chunk_reader17.py'),'__name__':'bounded_chunk_reader'}
    exec(compile((ROOT/'chunk_reader17.py').read_bytes(),str(ROOT/'chunk_reader17.py'),'exec',dont_inherit=True,optimize=0),reader_ns)
    initial_reader=reader_ns['Reader']();existing=set(initial_reader.keys);initial_reader.close()
    for case in list(DEST.iterdir()):
        if not case.is_dir()or not(DEST/(case.name+'.json')).exists():continue
        files={};dirs={};new={};parts={}
        for path in [case,*sorted(case.rglob('*'))]:
            st=path.lstat();rel=path.relative_to(case).as_posix()
            need(not path.is_symlink(),'Unexpected case symlink')
            meta={'mode':stat.S_IMODE(st.st_mode),'mtime_ns':st.st_mtime_ns}
            if path.is_dir():dirs[rel]=meta
            else:
                data=ORIGINAL_PATH_READ(path);keys=[]
                for start in range(0,len(data),16384):
                    chunk=data[start:start+16384];key=sha(chunk);keys.append(key)
                    if key not in existing:new[key]=chunk
                files[rel]={**meta,'bytes':len(data),'sha256':sha(data),'chunks':keys}
        virtual={k:v for k,v in MEMORY_PATHS.items()if k.startswith(str(case)+'/')}
        virtual_bodies={}
        for digest in set(virtual.values()):
            data=MEMORY_BODIES[digest];keys=[]
            for start in range(0,len(data),16384):
                chunk=data[start:start+16384];key=sha(chunk);keys.append(key)
                if key not in existing:new[key]=chunk
            virtual_bodies[digest]={'bytes':len(data),'chunks':keys}
        index={'case':case.name,'files':files,'directories':dirs,'virtual_paths':virtual,'virtual_bodies':virtual_bodies,
               'virtual_directories':[k for k in VIRTUAL_DIRECTORIES if k.startswith(str(case)+'/')],
               'direct_custody_no_original_ZIP_created':True,
               'cohort':DEST.name,
               'historical_virtual_scope_complete':case.name not in globals().get('VIRTUAL_LOSS_CASES',set()),
               'boundary':'Actual physical runtime/state/source/authority/intent/certificate/consumed-original-response files; only large readonly fresh provider captures use exact-byte VFS.'}
        raw=(json.dumps(index,sort_keys=True,indent=2)+'\n').encode();packed=gzip.compress(raw,mtime=0)
        # Future chunks are compressed together, directly, with known exact
        # lengths before disk allocation. The initial ZIP is never rewritten.
        epoch=None;packed_epoch=b'';epoch_index=b''
        if new:
            offset=0;offsets={};payload=[]
            for key in sorted(new):
                data=new[key];offsets[key]={'offset':offset,'bytes':len(data)};payload.append(data);offset+=len(data)
            payload=b''.join(payload);need(len(payload)<=128*1024*1024,'Segment raw bound')
            packed_epoch=lzma.compress(payload,filters=[{'id':lzma.FILTER_LZMA2,'preset':6,'dict_size':16*1024*1024}])
            name='epoch_'+uuid.uuid4().hex
            epoch={'data_file':name+'.xz','raw_bytes':len(payload),'raw_sha256':sha(payload),'chunks':offsets,'compressed_pin':{'bytes':len(packed_epoch),'sha256':sha(packed_epoch)}}
            epoch_index=gzip.compress((json.dumps(epoch,sort_keys=False,indent=2)+'\n').encode(),mtime=0)
        bound=len(packed_epoch)+len(epoch_index)+len(packed)+65536
        need(allocated()+bound<10*1024*1024,'Preflight direct-segment cap')
        need(os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize>=150*1024*1024+bound,'Direct-segment free reserve')
        if epoch:
            segment_root=ROOT/'private/chunks17_segments'
            for path,data in [(segment_root/epoch['data_file'],packed_epoch),(segment_root/(name+'.index.json.gz'),epoch_index)]:
                with path.open('xb')as h:h.write(data);h.flush();os.fsync(h.fileno())
        recipe=ARCHIVES/(DEST.name+'__'+case.name+'.case.json.gz')
        with recipe.open('xb')as h:h.write(packed);h.flush();os.fsync(h.fileno())
        for directory in [ROOT/'private/chunks17_segments',ARCHIVES]:
            fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY)
            try:os.fsync(fd)
            finally:os.close(fd)
        need(json.loads(gzip.decompress(ORIGINAL_PATH_READ(recipe)))==index,'Case recipe readback')
        reader=reader_ns['Reader']()
        try:
            for rel,pin in files.items():
                body=b''.join(reader.get(k)for k in pin['chunks'])
                need(len(body)==pin['bytes']and sha(body)==pin['sha256']and body==ORIGINAL_PATH_READ(case/rel),'Complete physical custody bytes')
            for digest,pin in virtual_bodies.items():
                body=b''.join(reader.get(k)for k in pin['chunks'])
                need(len(body)==pin['bytes']and sha(body)==digest and body==MEMORY_BODIES[digest],'Complete virtual custody bytes')
        finally:reader.close()
        need({q.relative_to(case).as_posix()for q in case.rglob('*')}==set(files)|(set(dirs)-{'.'}),'Case namespace changed')
        for rel,pin in files.items():
            path=case/rel;st=path.stat()
            need(stat.S_IMODE(st.st_mode)==pin['mode']and st.st_mtime_ns==pin['mtime_ns']and sha(ORIGINAL_PATH_READ(path))==pin['sha256'],'Case metadata changed')
        for rel,pin in dirs.items():
            path=case if rel=='.'else case/rel;st=path.stat()
            need(stat.S_IMODE(st.st_mode)==pin['mode']and st.st_mtime_ns==pin['mtime_ns'],'Case directory metadata changed')
        for rel in files:(case/rel).unlink()
        for rel in sorted(set(dirs)-{'.'},key=lambda n:n.count('/'),reverse=True):(case/rel).rmdir()
        case.rmdir();existing.update(new)
        for key in virtual:del MEMORY_PATHS[key]
        for key in list(MEMORY_BODIES):
            if key not in MEMORY_PATHS.values():del MEMORY_BODIES[key]
        VIRTUAL_DIRECTORIES.difference_update(index['virtual_directories'])
        need(allocated()<10*1024*1024,'Direct-custody allocated cap')
        need(os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize>=150*1024*1024,'Direct-custody free reserve')
        print('Direct exact custody',case.name,flush=True)
