"""Actual parsed07 lifecycle with fully intercepted provider adapters; no real I/O."""
from pathlib import Path
import contextlib,copy,datetime,hashlib,io,json,os,sys,types

REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW;SOURCE=ROOT/'source';OLD=ROOT.parent/'operations'
MODE='OO' if sys.flags.optimize==2 else 'O' if sys.flags.optimize else 'normal'
DEST=REVIEW/'private'/('parsed_regression01_'+MODE);DEST.mkdir(exist_ok=False)
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
ARCHIVES=ROOT/'private'/'case_archives_regression01';ARCHIVES.mkdir(exist_ok=True)
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
for kind in ['approval_revoked','old_intent_changed','source_changed','clock_expired']:
    label='ledger_after_fsync_'+kind;w=setup(label,'ledger');writer=c.durable;hit=[False]
    real_datetime=c.dt.datetime;offset=[0]
    class ReviewClock(real_datetime):
        @classmethod
        def now(cls,tz=None):return real_datetime.now(tz)+datetime.timedelta(seconds=offset[0])
    def changed(path,value):
        writer(path,value)
        if path.name=='LEDGER_APPEND_INTENT.json':
            hit[0]=True
            if kind=='approval_revoked':w.ad_path.rename(w.ad_path.with_suffix('.revoked'))
            elif kind=='old_intent_changed':
                q=m.PRIOR_RUNTIME/'ZENODO_STAGE_INTENT.json';v=json.loads(q.read_bytes());v['id']=999;q.write_text(json.dumps(v)+'\n')
            elif kind=='source_changed':
                q=m.CONTEXT['source_root']/'lifecycle08.py';q.write_bytes(q.read_bytes()+b'\n# controlled drift\n')
            else:offset[0]=181
    before=(len(w.native.calls),w.appends)
    with model.patch((c,'durable',changed),(c.dt,'datetime',ReviewClock)),w.installed():a,e=run(w,'ledger')
    need(hit[0],'Ledger intent hook not hit')
    record(label,w,False,a,e,before,{'native':0,'append':0},{'old06_countercase':True})
w=setup('ledger_native31seconds_after_complete_gate','ledger');offset=[0];real_datetime=c.dt.datetime;hits=[0]
class LateClock(real_datetime):
    @classmethod
    def now(cls,tz=None):return real_datetime.now(tz)+datetime.timedelta(seconds=offset[0])
def late(*a,**k):offset[0]=31;hits[0]+=1
w.gate_hook=late;before=(len(w.native.calls),w.appends)
with model.patch((c.dt,'datetime',LateClock)),w.installed():a,e=run(w,'ledger')
record('ledger_native31seconds_after_complete_gate',w,True,a,e,before,{'native':0,'append':1},{'old06_countercase':True,'safe_refresh_after_collector':True,'gate_hooks':hits[0]})
w=setup('ledger_native_family_changed_after_complete_gate','ledger')
def aftergate(*a,**k):
    def changed(l,n,f):
        l['conceptrecid']='999';l['conceptdoi']='10.5281/zenodo.999';n['parent']['id']='999';n['parent']['pids']['doi']['identifier']='10.5281/zenodo.999'
    w.native.fault=changed
w.gate_hook=aftergate;before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'ledger')
record('ledger_native_family_changed_after_complete_gate',w,False,a,e,before,{'native':0,'append':0},{'old06_countercase':True})
for kind in ['boolean_grid_echo','formula_only_boolean_echo','metadata_bool_drift','fullmetadata_hidden_changes_between_paired_gets']:
    label=kind;w=setup(label);original=w.command;meta=[0]
    def command(argv,body=None):
        result=original(argv,body)
        if argv[0]=='gws' and argv[3:5]==['values','batchGetByDataFilter']:
            payload=json.loads(argv[argv.index('--json')+1])
            if kind=='boolean_grid_echo' or kind=='formula_only_boolean_echo' and payload['valueRenderOption']=='FORMULA':result['valueRanges'][0]['dataFilters'][0]['gridRange']['startColumnIndex']=False
        if argv[0]=='gws' and argv[3]=='get':
            meta[0]+=1
            if kind=='metadata_bool_drift':result['sheets'][0]['properties']['hidden']=False if meta[0]%2 else 0
            if kind=='fullmetadata_hidden_changes_between_paired_gets':result['sheets'][0]['properties']['hidden']=bool(meta[0]%2)
        return result
    w.command=command
    with w.installed():a,e=run(w,'resume-stage')
    record(label,w,False,a,e,(0,0),{'native':0,'append':0},{'old06_countercase':True})
w=setup('publication_revoked_during_postwrite_native_verification','publish');native=modules['native_policy'];writer=native.durable;hit=[False]
def revoke(path,value):
    writer(path,value)
    if path.name=='verified.json' and value.get('published') is True and not hit[0]:hit[0]=True;w.ad_path.rename(w.ad_path.with_suffix('.revoked'))
before=(len(w.native.calls),w.appends)
with model.patch((native,'durable',revoke)),w.installed():a,e=run(w,'publish')
need(hit[0] and not (m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists(),'False final publication certification')
record('publication_revoked_during_postwrite_native_verification',w,False,a,e,before,{'native':1,'append':0},{'old06_countercase':True})
# New expected-byte intent races. Long collector callback alters persisted
# action intent, not the copy passed to the delegate.
for phase in ['resume','publish','ledger']:
    label='own_intent_drift_after_long_gate_'+phase;w=setup(label,'ledger' if phase=='ledger' else 'publish' if phase=='publish' else 'stage');hit=[False]
    target={'resume':'RESUME_STAGE_INTENT.json','publish':'ZENODO_PUBLISH_INTENT.json','ledger':'LEDGER_APPEND_INTENT.json'}[phase]
    def drift(*a,**k):
        q=m.RUNTIME/target
        if q.exists() and not hit[0]:
            hit[0]=True;v=json.loads(q.read_bytes());v['id' if phase!='ledger' else 'record']=999;q.write_text(json.dumps(v)+'\n')
    if phase=='ledger':
        # Actual post-intent strict metadata GET is the long provider boundary.
        original=w.command
        def command(argv,body=None):
            value=original(argv,body)
            if argv[0]=='gws' and argv[3]=='get':drift()
            return value
        w.command=command
    else:w.gate_hook=drift
    before=(len(w.native.calls),w.appends)
    with w.installed():a,e=run(w,{'resume':'resume-stage','publish':'publish','ledger':'ledger'}[phase])
    need(hit[0],'Intent drift hook missed')
    record(label,w,False,a,e,before,{'native':0,'append':0})
# Changes made after fsync itself are caught against the requested bytes.
for phase in ['create','publish','ledger']:
    label='own_perwrite_intent_drift_after_fsync_'+phase;w=setup(label,'ledger' if phase=='ledger' else 'publish' if phase=='publish' else 'stage');writer=c.durable;hit=[False]
    target={'create':'WRITE_stage_create_INTENT.json','publish':'WRITE_publish_publish_INTENT.json','ledger':'LEDGER_APPEND_INTENT.json'}[phase]
    def drift(path,value):
        writer(path,value)
        if path.name==target:
            hit[0]=True;v=json.loads(path.read_bytes());v['known_id' if phase!='ledger' else 'record']=999;path.write_text(json.dumps(v)+'\n')
    before=(len(w.native.calls),w.appends)
    with model.patch((c,'durable',drift)),w.installed():a,e=run(w,'resume-stage' if phase=='create' else phase)
    need(hit[0],'Fsync intent hook missed')
    record(label,w,False,a,e,before,{'native':0,'append':0})
# Authority lost while preparing the final private certificate cannot mint a
# final VERIFIED receipt. Actual successful service outcomes remain in custody.
for phase in ['stage','publish','ledger']:
    label='final_certificate_revocation_'+phase;w=setup(label,'ledger' if phase=='ledger' else 'publish' if phase=='publish' else 'stage');writer=c.durable;hit=[False]
    def revoke(path,value):
        writer(path,value)
        if path.name.startswith('certificate_') and not hit[0]:hit[0]=True;w.ad_path.rename(w.ad_path.with_suffix('.revoked'))
    before=(len(w.native.calls),w.appends)
    with model.patch((c,'durable',revoke)),w.installed():a,e=run(w,'resume-stage' if phase=='stage' else phase)
    need(hit[0],'Final certificate hook missed')
    need(not (m.RUNTIME/{'stage':'ZENODO_STAGE_VERIFIED.json','publish':'ZENODO_PUBLISH_VERIFIED.json','ledger':'LEDGER_VERIFIED.json'}[phase]).exists(),'False final certificate')
    record(label,w,False,a,e,before,{'native':4 if phase=='stage' else 1 if phase=='publish' else 0,'append':1 if phase=='ledger' else 0})
w=setup('public_readback_revocation_after_DOI','ledger');original=w.fetch;hit=[False]
def fetch(url,limit):
    value=original(url,limit)
    if url.startswith('https://doi.org/') and not hit[0]:hit[0]=True;w.ad_path.rename(w.ad_path.with_suffix('.revoked'))
    return value
w.fetch=fetch;before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'verify-public')
need(hit[0],'Public boundary hook missed')
record('public_readback_revocation_after_DOI',w,False,a,e,before,{'native':0,'append':0})
w=setup('lost_append_GET_only_reentry','ledger');w.append_mode='lost';before=(len(w.native.calls),w.appends)
with w.installed():
    a,e=run(w,'ledger');count=w.appends;again,err=run(w,'ledger')
need(count==w.appends==1 and err is None and again['new_row'] is False,'Lost append not reconciled safely: '+str(err))
record('lost_append_GET_only_reentry',w,False,a,e,before,{'native':0,'append':1},{'GET_only_reentry':again})
w=setup('postappend_old_cell_formula','ledger');w.formula_after=True;before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'ledger')
record('postappend_old_cell_formula',w,False,a,e,before,{'native':0,'append':1})
for text,permit in [('pull request1131',False),('pull request #0001131',False),('pull request #11310',True)]:
    label='explicit_PR_lead_'+str(len(checks));w=setup(label);w.rows.append(['Other result','','',text])
    with w.installed():a,e=run(w,'resume-stage')
    record(label,w,permit,a,e,(0,0),{'native':4 if permit else 0,'append':0},{'text':text})

# Fresh adversarial control for the certificate preparation/check/link boundary.
for phase in ['stage','publish','ledger']:
    label='pending_certificate_drift_after_long_context_'+phase;w=setup(label,'ledger' if phase=='ledger' else 'publish' if phase=='publish' else 'stage');original=m.local_context;hit=[False]
    def drift(args,action):
        result=original(args,action)
        if not hit[0]:
            runtime_inodes={(r.stat().st_dev,r.stat().st_ino)for r in m.RUNTIME.iterdir()if r.is_file()}
            for candidate in m.PRIVATE.glob('certificate_*.json'):
                if (candidate.stat().st_dev,candidate.stat().st_ino)not in runtime_inodes:
                    hit[0]=True;v=json.loads(candidate.read_bytes());v['id']=999;candidate.write_text(json.dumps(v)+'\n');break
        return result
    before=(len(w.native.calls),w.appends)
    with model.patch((m,'local_context',drift)),w.installed():a,e=run(w,'resume-stage' if phase=='stage' else phase)
    target={'stage':'RESUME_STAGE_VERIFIED.json','publish':'ZENODO_PUBLISH_VERIFIED.json','ledger':'LEDGER_VERIFIED.json'}[phase]
    need(hit[0] and not(m.RUNTIME/target).exists(),'Changed private certificate was committed')
    record(label,w,False,a,e,before,{'native':4 if phase=='stage' else 1 if phase=='publish' else 0,'append':1 if phase=='ledger' else 0})
w=setup('publish_action_intent_drift_during_first_owned_page','publish');hit=[False]
def drift(records,page):
    q=m.RUNTIME/'ZENODO_PUBLISH_INTENT.json'
    if page==1 and q.exists() and not hit[0]:
        hit[0]=True;value=json.loads(q.read_bytes());value['id']=999;q.write_text(json.dumps(value)+'\n')
    return records
w.account_fault=drift;before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'publish')
need(hit[0] and not(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists(),'Late account intent hook/certification failed')
record('publish_action_intent_drift_during_first_owned_page',w,False,a,e,before,{'native':0,'append':0})
w=setup('publish_perwrite_intent_drift_after_POST','publish');native=modules['native_policy'];writer=native.durable;hit=[False]
def drift(path,value):
    writer(path,value)
    if path.name=='verified.json' and value.get('published') is True and not hit[0]:
        hit[0]=True;q=m.RUNTIME/'WRITE_publish_publish_INTENT.json';v=json.loads(q.read_bytes());v['known_id']=999;q.write_text(json.dumps(v)+'\n')
before=(len(w.native.calls),w.appends)
with model.patch((native,'durable',drift)),w.installed():a,e=run(w,'publish')
need(hit[0] and not(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists(),'Postwrite intent drift falsely certified')
record('publish_perwrite_intent_drift_after_POST',w,False,a,e,before,{'native':1,'append':0})
w=setup('ledger_intent_drift_after_actual_append','ledger');original=w.command;hit=[False]
def command(argv,body=None):
    value=original(argv,body)
    if w.appends and argv[0]=='gws' and argv[3]=='get' and not hit[0]:
        hit[0]=True;q=m.RUNTIME/'LEDGER_APPEND_INTENT.json';v=json.loads(q.read_bytes());v['record']=999;q.write_text(json.dumps(v)+'\n')
    return value
w.command=command;before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'ledger')
need(hit[0] and not(m.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Postappend intent drift falsely certified')
record('ledger_intent_drift_after_actual_append',w,False,a,e,before,{'native':0,'append':1})
for target,field,value in [('ZENODO_STAGE_INTENT.json','id',999),('ROOT_STAGE_FAILURE_READONLY_RECONCILIATION.json','no_service_mutation',False)]:
    label='old_context_drift_after_long_stage_guard_'+field;w=setup(label);hit=[False]
    def drift(*a,**k):
        if not hit[0]:
            hit[0]=True;q=m.PRIOR_RUNTIME/target;v=json.loads(q.read_bytes());v[field]=value;q.write_text(json.dumps(v)+'\n')
    w.gate_hook=drift
    with w.installed():a,e=run(w,'resume-stage')
    need(hit[0],'Old context drift hook missed')
    record(label,w,False,a,e,(0,0),{'native':0,'append':0})
def canonical(w):return c.zenodo.state_path(pub.MANIFEST.resolve(),'production')
def competing(w,identifier=999):
    path=canonical(w);path.parent.mkdir(exist_ok=True)
    data=(json.dumps({'manifest':str(pub.MANIFEST.resolve()),'environment':'production','id':identifier,
        'concurrent_other_process_marker':'PRESERVE_EXACT_BYTES_µ','unknown_fields':{'b':True,'n':1}},indent=1,ensure_ascii=False)+'\n').encode()
    temporary=path.with_suffix('.competing');temporary.write_bytes(data);os.replace(temporary,path)
    return data
# Required typed postappend old-cell controls.
for value in [1,True]:
    label='postappend_numeric_cell_'+type(value).__name__;w=setup(label,'ledger');hit=[False]
    def corrupt(response):hit[0]=True;w.rows[1][0]=value
    w.response_fault=corrupt;before=(len(w.native.calls),w.appends)
    with w.installed():a,e=run(w,'ledger')
    need(hit[0] and not(m.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Typed old cell falsely certified')
    record(label,w,False,a,e,before,{'native':0,'append':1})
# All native durable-intent actual edges, preserving earlier completed effects.
for kind,ordinal,expected in [('create',0,0),('upload',1,1),('upload',2,2),('update',0,3),('publish',0,0)]:
    label='native_intent_fsync_revocation_'+kind+str(ordinal);w=setup(label,'publish' if kind=='publish' else 'stage');writer=c.durable;hit=[False];uploads=[0]
    def revoke(path,value):
        writer(path,value)
        match=path.name=='WRITE_'+('publish' if kind=='publish' else 'stage')+'_'+kind+'_INTENT.json'
        if kind=='upload' and path.name.startswith('WRITE_stage_upload_'):uploads[0]+=1;match=uploads[0]==ordinal
        if match and not hit[0]:hit[0]=True;w.ad_path.rename(w.ad_path.with_suffix('.revoked'))
    before=(len(w.native.calls),w.appends)
    with model.patch((c,'durable',revoke)),w.installed():a,e=run(w,'publish' if kind=='publish' else 'resume-stage')
    need(hit[0],'Native edge hook missed')
    record(label,w,False,a,e,before,{'native':expected,'append':0})
# Stable state before stage prevents any allocation. Ledger drift before its
# actual direct append remains a no-write hold; postappend drift cannot certify.
w=setup('preexisting_original_manifest_state');body=competing(w)
with w.installed():a,e=run(w,'resume-stage')
need(canonical(w).read_bytes()==body,'Preexisting state changed')
record('preexisting_original_manifest_state',w,False,a,e,(0,0),{'native':0,'append':0})
for phase in ['before_append','after_append']:
    label='ledger_state_drift_'+phase;w=setup(label,'ledger');original=w.command;writer=c.durable;sentinel={}
    def drift(path,value):
        writer(path,value)
        if phase=='before_append' and path.name=='LEDGER_APPEND_INTENT.json':sentinel['body']=competing(w)
    def command(argv,body=None):
        value=original(argv,body)
        if phase=='after_append' and w.appends and not sentinel:sentinel['body']=competing(w)
        return value
    w.command=command;before=(len(w.native.calls),w.appends)
    with model.patch((c,'durable',drift)),w.installed():a,e=run(w,'ledger')
    need(sentinel and canonical(w).read_bytes()==sentinel['body'],'Ledger replaced competing bytes')
    need(not(m.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Ledger conflict falsely certified')
    record(label,w,False,a,e,before,{'native':0,'append':int(phase=='after_append')})
w=setup('lost_publish_existing_state_functional','publish');w.native.lost=True;before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'publish')
record('lost_publish_existing_state_functional',w,True,a,e,before,{'native':1,'append':0})
archive_completed()
need(not model.ATTEMPTS,'Real network/process escape attempted')
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':MODE,'source_sha256':MS,'bootstrap_sha256':BS,'case_count':len(checks),'parsed_invocations_including_setups':len(CLI_INVOCATIONS),'results':checks,'real_escape_attempts':model.ATTEMPTS,'real_service_or_Git_mutations':0,'allocated_bytes':allocated(),'publication_ready':False}
(DEST/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
need(all(q['status']=='PASS' for q in checks),'Unresolved regression')
