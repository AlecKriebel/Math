"""Actual parsed07 lifecycle with fully intercepted provider adapters; no real I/O."""
from pathlib import Path
import contextlib,copy,datetime,hashlib,io,json,os,sys,types

REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW;SOURCE=ROOT/'source';OLD=ROOT.parent/'operations'
MODE='OO' if sys.flags.optimize==2 else 'O' if sys.flags.optimize else 'normal'
DEST=REVIEW/'private'/('parsed_persistence_failures01_'+MODE);DEST.mkdir(exist_ok=False)
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
CONTROL_SHA=sha(Path(__file__).read_bytes())
MS=sha((SOURCE/'SOURCE_MANIFEST.json').read_bytes());BS=sha((SOURCE/'bootstrap08.py').read_bytes())
base=(OLD/'bootstrap.py').read_bytes();need(sha(base)=='960b33e83135968ab40ef069b1b8876df47b70d1c4ef528bf0d8c836213ac58b','Original bootstrap pin')
ns={'__file__':str(OLD/'bootstrap.py'),'__name__':'checked_old_bootstrap'}
exec(compile(base,str(OLD/'bootstrap.py'),'exec'),ns)
load,_=ns['load_verified'](OLD,'eab69e53e9d32510bbf00d74c1b94b70542a8b29cf326c42f5d974e510f09d00',sha(base))
model=load('full_controls')  # blocks every real network/process escape before loading07
boot={'__file__':str(SOURCE/'bootstrap08.py'),'__name__':'checked07_bootstrap'}
exec(compile((SOURCE/'bootstrap08.py').read_bytes(),str(SOURCE/'bootstrap08.py'),'exec'),boot)
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
    w=World(OLD,modules);w.formula_after=False;w.place=place
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
    ad=json.loads((SOURCE/'ROOT_CLEARANCE08.example.json').read_bytes())
    ad.update(operations08_sources_sha256=MS,bootstrap08_sha256=BS,publication_ready=True,
              whole08_review_adopted=True,unresolved_findings=[],
              root_confirmed_failure_before_delegate_create=True,initial_create_attempt_was_sent=False,
              allowed_actions=['resume-stage','publish','ledger'],instructions='OFFLINE MODEL ONLY; NO PRODUCTION AUTHORITY')
    w.ad_path=rt/'ROOT_OPERATIONAL_CLEARANCE08.json';w.ad_path.write_text(json.dumps(ad,indent=2)+'\n')
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
    need(not w.git.writes,'07 attempted Git mutation')
    need(allocated()<=12*1024*1024,'New allocation budget exceeded')
    (DEST/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n');results.append(r)
    print(json.dumps({'case':label,'status':'PASS','native_writes':len(w.native.calls),'appends':w.appends}),flush=True)


# The scenarios/adjudications below are independently authored for this review.
# Every case invokes checked_lifecycle08.main (actual parsed command surface).
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
    need(allocated()<12*1024*1024,'Review allocated bytes exceed75MiB')
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
    return m.PRIVATE!=ROOT/'private' and m.PRIVATE in path.parents and not path.name.startswith(('certificate_','state_initial_'))
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


import zipfile,stat
ARCHIVES=ROOT/'private'/'case_archives_persistence_failures01';ARCHIVES.mkdir(exist_ok=True)
def archive_completed():
    for case in list(DEST.iterdir()):
        result=DEST/(case.name+'.json')
        if not case.is_dir() or not result.exists():continue
        paths=sorted(case.rglob('*'));files={};dirs={}
        for path in paths:
            st=path.lstat();rel=path.relative_to(case).as_posix()
            if path.is_dir():dirs[rel]={'mode':stat.S_IMODE(st.st_mode),'mtime_ns':st.st_mtime_ns}
            else:
                body=ORIGINAL_PATH_READ(path);files[rel]={'bytes':len(body),'sha256':sha(body),'mode':stat.S_IMODE(st.st_mode),'mtime_ns':st.st_mtime_ns}
        virtual={k:v for k,v in MEMORY_PATHS.items() if k.startswith(str(case)+'/')}
        content={v:MEMORY_BODIES[v] for v in set(virtual.values())}
        index={'case':case.name,'files':files,'directories':dirs,'virtual_paths':virtual,'virtual_bytes':{k:len(v) for k,v in content.items()},'virtual_directory_paths':[k for k in VIRTUAL_DIRECTORIES if k.startswith(str(case)+'/')],'virtual_api_boundary':'Only large private readonly capture durable/read/mkdir. Actual runtime/state/source/private statecandidate/certificate unchanged.'}
        destination=ARCHIVES/(case.name+'.zip')
        with zipfile.ZipFile(destination,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            z.writestr('INDEX.json',json.dumps(index,sort_keys=True,indent=2)+'\n')
            for rel in files:z.writestr('physical/'+rel,ORIGINAL_PATH_READ(case/rel))
            for key,body in content.items():z.writestr('virtual/'+key,body)
        with zipfile.ZipFile(destination) as z:
            for rel,pin in files.items():
                data=z.read('physical/'+rel);need(len(data)==pin['bytes'] and sha(data)==pin['sha256'],'Physical exact custody failure')
            for key,body in content.items():need(z.read('virtual/'+key)==body,'Virtual exact custody failure')
        # Recheck exact physical tree before retiring only this completed owned case.
        need({x.relative_to(case).as_posix() for x in case.rglob('*')}==set(files)|set(dirs),'Custody closure changed')
        for rel,pin in files.items():
            path=case/rel;st=path.stat();need(sha(ORIGINAL_PATH_READ(path))==pin['sha256'] and st.st_mtime_ns==pin['mtime_ns'] and stat.S_IMODE(st.st_mode)==pin['mode'],'Custody metadata changed');path.unlink()
        for rel in sorted(dirs,key=lambda s:s.count('/'),reverse=True):(case/rel).rmdir()
        case.rmdir()
        for key in virtual:del MEMORY_PATHS[key]
        for key in list(MEMORY_BODIES):
            if key not in MEMORY_PATHS.values():del MEMORY_BODIES[key]
        VIRTUAL_DIRECTORIES.difference_update(index['virtual_directory_paths'])
        compact_ns={'__file__':str(ROOT/'compact_archives08.py'),'__name__':'owned_bounded_compactor'}
        exec(compile((ROOT/'compact_archives08.py').read_bytes(),str(ROOT/'compact_archives08.py'),'exec'),compact_ns)
        compact_ns['compact']()
for point in ['before_link','directory_fsync_after_link']:
    label='initial_state_IO_error_'+point;w=setup(label);original_link=os.link;original_fsync=os.fsync;hit=[False]
    def link(src,dst,*args,**kwargs):
        if point=='before_link' and dst==c.zenodo.state_path(pub.MANIFEST.resolve(),'production').name:
            hit[0]=True;raise OSError('Controlled initial state install failure')
        return original_link(src,dst,*args,**kwargs)
    def fsync(fd):
        place=c.zenodo.state_path(pub.MANIFEST.resolve(),'production')
        if point=='directory_fsync_after_link' and not hit[0] and place.exists() and os.fstat(fd).st_ino==place.parent.stat().st_ino:
            hit[0]=True;raise OSError('Controlled state directory fsync failure after exclusive installation')
        return original_fsync(fd)
    with model.patch((os,'link',link),(os,'fsync',fsync)),w.installed():a,e=run(w,'resume-stage')
    need(hit[0],'Initial save fault not reached')
    place=c.zenodo.state_path(pub.MANIFEST.resolve(),'production')
    need(place.exists()==(point=='directory_fsync_after_link'),'Unexpected canonical installation outcome')
    known=json.loads((m.RUNTIME/'CREATE_RETURNED_KNOWN_ID.json').read_bytes());failure=json.loads((m.RUNTIME/'RESUME_STAGE_FAILURE.json').read_bytes())
    need(known['id']==failure['delegate_known_id']==777,'Known service fact lost')
    need(not(m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'State persistence failure certified')
    record(label,w,False,a,e,(0,0),{'native':1,'append':0},{'known_created_id':777,'canonical_installed':place.exists()})
    with w.installed():
        before=(len(w.native.calls),w.appends);a,e=run(w,'resume-stage')
    record(label+'_no_retry',w,False,a,e,before,{'native':0,'append':0})
archive_completed();need(not model.ATTEMPTS,'Real escape attempted')
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':MS,'bootstrap_sha256':BS,'mode':MODE,'case_count':len(checks),'parsed_invocations_including_setups':len(CLI_INVOCATIONS),'results':checks,'real_escape_attempts':model.ATTEMPTS,'real_service_or_Git_mutations':0,'allocated_bytes':allocated(),'publication_ready':False}
(DEST/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');need(all(q['status']=='PASS' for q in checks),'Persistence error counterexample');print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
