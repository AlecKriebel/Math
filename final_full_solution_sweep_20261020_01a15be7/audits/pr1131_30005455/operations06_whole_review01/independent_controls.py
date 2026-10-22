"""Actual parsed06 lifecycle with fully intercepted provider adapters; no real I/O."""
from pathlib import Path
import contextlib,copy,datetime,hashlib,io,json,os,sys,types

REVIEW=Path(__file__).resolve().parent
ROOT=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455/operations06');SOURCE=ROOT/'source';OLD=ROOT.parent/'operations'
MODE='OO' if sys.flags.optimize==2 else 'O' if sys.flags.optimize else 'normal'
DEST=REVIEW/'private'/('fresh_'+MODE);DEST.mkdir(exist_ok=False)
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
CONTROL_SHA=sha(Path(__file__).read_bytes())
MS=sha((SOURCE/'SOURCE_MANIFEST.json').read_bytes());BS=sha((SOURCE/'bootstrap06.py').read_bytes())
base=(OLD/'bootstrap.py').read_bytes();need(sha(base)=='960b33e83135968ab40ef069b1b8876df47b70d1c4ef528bf0d8c836213ac58b','Original bootstrap pin')
ns={'__file__':str(OLD/'bootstrap.py'),'__name__':'checked_old_bootstrap'}
exec(compile(base,str(OLD/'bootstrap.py'),'exec'),ns)
load,_=ns['load_verified'](OLD,'eab69e53e9d32510bbf00d74c1b94b70542a8b29cf326c42f5d974e510f09d00',sha(base))
model=load('full_controls')  # blocks every real network/process escape before loading06
boot={'__file__':str(SOURCE/'bootstrap06.py'),'__name__':'checked06_bootstrap'}
exec(compile((SOURCE/'bootstrap06.py').read_bytes(),str(SOURCE/'bootstrap06.py'),'exec'),boot)
m=boot['load_verified'](SOURCE,MS,BS);c=m.c;pub=m.pl;live=m.live;ir=m.ir
modules={n:m.LOAD05(n) for n in ['ops_common','publish_and_ledger','collect_live','integrate_remote','native_policy']}
c.zenodo.token_for=lambda *a,**k:'OFFLINE_SENTINEL_NO_CREDENTIAL'
c.zenodo.doi_status=lambda doi:{'status':'offline_mock','url':'https://doi.org/'+doi}
results=[];bodies={};actual_durable=c.durable
def compact(path,value):
    actual_durable(path,value)
    body=path.read_bytes();key=sha(body);prior=bodies.get(key)
    if prior is not None and prior.exists() and prior!=path:
        need(prior.read_bytes()==body,'Capture dedup mismatch')
        tmp=path.with_name(path.name+'.own_dedup')
        try:os.link(prior,tmp);os.replace(tmp,path)
        finally:
            if tmp.exists():tmp.unlink()
    else:bodies[key]=path
for module in modules.values():
    if hasattr(module,'durable'):module.durable=compact

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
    # merge identity; no integrate/ready/merge operation is executed in06.
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
    ad=json.loads((SOURCE/'ROOT_CLEARANCE06.example.json').read_bytes())
    ad.update(operations06_sources_sha256=MS,bootstrap06_sha256=BS,publication_ready=True,
              whole06_review_adopted=True,unresolved_findings=[],
              root_confirmed_failure_before_delegate_create=True,initial_create_attempt_was_sent=False,
              allowed_actions=['resume-stage','publish','ledger'],instructions='OFFLINE MODEL ONLY; NO PRODUCTION AUTHORITY')
    w.ad_path=rt/'ROOT_OPERATIONAL_CLEARANCE06.json';w.ad_path.write_text(json.dumps(ad,indent=2)+'\n')
    w.clearance_sha=sha(w.ad_path.read_bytes())
    return w

def cli(w,action='resume-stage'):
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
    need(not w.git.writes,'06 attempted Git mutation')
    need(allocated()<=75*1024*1024,'New allocation budget exceeded')
    (DEST/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n');results.append(r)
    print(json.dumps({'case':label,'status':'PASS','native_writes':len(w.native.calls),'appends':w.appends}),flush=True)


# The scenarios/adjudications below are independently authored for this review.
# Every case invokes checked_lifecycle06.main (actual parsed command surface).
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
    need(allocated()<75*1024*1024,'Review allocated bytes exceed75MiB')
    print(json.dumps({'case':label,'status':v['status'],'delta':delta,'error':error}),flush=True)
def run(w,action):
    try:return cli(w,action),None
    except Exception as exc:return None,{'type':type(exc).__name__,'message':str(exc)}
def setup(label,phase='stage'):
    w=world(label);c.zenodo.STATE_DIR=live.REPO/'.zenodo-state'
    if phase!='stage':
        with w.installed():
            need(run(w,'resume-stage')[1] is None,'Setup stage failure')
            if phase=='ledger':need(run(w,'publish')[1] is None,'Setup publication failure')
    return w

w=setup('valid_actual_full_lifecycle')
with w.installed():
    a,e=run(w,'resume-stage');need(e is None,'Positive stage failed')
    p,e=run(w,'publish');need(e is None,'Positive publication failed')
    a,e=run(w,'verify-public');need(e is None,'Positive public readback failed')
    a,e=run(w,'ledger')
record('valid_actual_full_lifecycle',w,True,a,e,(0,0),{'native':5,'append':1})
with w.installed():
    b=(len(w.native.calls),w.appends);a,e=run(w,'resume-stage')
record('no_second_allocation',w,False,a,e,b,{'native':0,'append':0})

# Native edge controls: changes happen only AFTER the real exclusive durable
# per-write intent finishes, immediately before the delegate edge.
for boundary in ['create','first_upload','second_upload','update','publish']:
    label='native_edge_revocation_'+boundary;w=setup(label,'publish' if boundary=='publish' else 'stage')
    writer=c.durable;count=[0];hit=[False]
    def revoke(path,value):
        writer(path,value)
        match=False
        if boundary in {'create','update','publish'}:match=path.name=='WRITE_'+('publish' if boundary=='publish' else 'stage')+'_'+boundary+'_INTENT.json'
        elif path.name.startswith('WRITE_stage_upload_'):
            count[0]+=1;match=count[0]==(1 if boundary=='first_upload' else 2)
        if match:hit[0]=True;w.ad_path.rename(w.ad_path.with_suffix('.revoked'))
    before=(len(w.native.calls),w.appends)
    with model.patch((c,'durable',revoke)),w.installed():a,e=run(w,'publish' if boundary=='publish' else 'resume-stage')
    expected={'create':0,'first_upload':1,'second_upload':2,'update':3,'publish':0}[boundary]
    record(label,w,False,a,e,before,{'native':expected,'append':0},{'fsynced_edge_hook_fired':hit[0]})

# The same final-write-intent condition is attacked at the ledger edge.
for kind in ['approval_revoked','old_intent_changed','source_changed','clock_expired']:
    label='ledger_after_fsync_'+kind;w=setup(label,'ledger');writer=pub.durable;hit=[False]
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
                q=m.CONTEXT['source_root']/'lifecycle06.py';q.write_bytes(q.read_bytes()+b'\n# independent drift\n')
            else:offset[0]=181
    before=(len(w.native.calls),w.appends)
    with model.patch((pub,'durable',changed),(c.dt,'datetime',ReviewClock)),w.installed():a,e=run(w,'ledger')
    record(label,w,False,a,e,before,{'native':0,'append':0},{'fsynced_edge_hook_fired':hit[0],'clock_advance_seconds':offset[0]})

w=setup('ledger_revoked_after_complete_gate','ledger')
def aftergate(*a,**k):w.ad_path.rename(w.ad_path.with_suffix('.revoked'))
w.gate_hook=aftergate;before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'ledger')
record('ledger_revoked_after_complete_gate',w,False,a,e,before,{'native':0,'append':0})

# Exercise actual collector routes, not only PR grammar helpers.
for channel,text,permit in [('ledger','pull request #0001131',False),('account_key','pull request1131',False),
                           ('source','PULL\u2003REQUEST : #001131',False),('result','pull%20request%20%231131',False),
                           ('local_key','https://github.com/AlecKriebel/Math/pull/1131',False),
                           ('ledger','pull request #11310',True),('ledger','prePR1131x',True)]:
    label='explicit_route_'+channel+'_'+str(len(checks));w=setup(label)
    if channel=='ledger':w.rows.append(['Prior result','','',text])
    elif channel=='account_key':w.accounts[0].setdefault('extra',{})[text]='Prior result'
    elif channel in {'source','result'}:w.accounts[0].setdefault('extra',{})[channel]={'deep':[{'evidence':text}]}
    else:(c.zenodo.STATE_DIR/'other.json').write_text(json.dumps({'id':42000,text:'Prior result'})+'\n')
    with w.installed():a,e=run(w,'resume-stage')
    record(label,w,permit,a,e,(0,0),{'native':4 if permit else 0,'append':0},{'channel':channel,'text':text})

# Family disagreements are internally coherent in the complete account view
# but distinct from the immediately observed native family.
for phase in ['first_upload','second_upload','update','publish','ledger']:
    label='family_split_'+phase;w=setup(label,'ledger' if phase=='ledger' else 'publish' if phase=='publish' else 'stage');active=[phase in {'first_upload','publish','ledger'}]
    def split(records,page):
        if active[0]:
            for rec in records:
                if rec['id']==777:
                    rec['conceptrecid']='999';rec['conceptdoi']='10.5281/zenodo.999'
                    if 'relations' in rec['metadata']:
                        for ver in rec['metadata']['relations'].get('version',[]):ver['parent']['pid_value']='999'
        return records
    w.account_fault=split
    if phase in {'second_upload','update'}:
        upload=w.native.upload
        def uploaded(*a,**k):
            r=upload(*a,**k)
            if len(w.native.present)==(1 if phase=='second_upload' else 2):active[0]=True
            return r
        w.native.upload=uploaded
    before=(len(w.native.calls),w.appends)
    with w.installed():a,e=run(w,'ledger' if phase=='ledger' else 'publish' if phase=='publish' else 'resume-stage')
    record(label,w,False,a,e,before,{'native':{'first_upload':1,'second_upload':2,'update':3,'publish':0,'ledger':0}[phase],'append':0})

# Unknown create outcome and known-ID post-create native refusal retain custody;
# reentry must never delegate another write.
for kind in ['lost_create','native_restricted_after_create']:
    label=kind;w=setup(label)
    if kind=='lost_create':
        orig=w.native.create
        def lost(*a,**k):orig(*a,**k);raise c.zenodo.DepositError('Independent lost create response after server success')
        w.native.create=lost
    else:w.native.fault=lambda l,n,f:n['access'].__setitem__('files','restricted')
    with w.installed():
        a,e=run(w,'resume-stage');before=(len(w.native.calls),w.appends);again,err=run(w,'resume-stage')
    failure_receipt=json.loads((m.RUNTIME/'RESUME_STAGE_FAILURE.json').read_bytes())
    record(label,w,False,a,e,(0,0),{'native':1,'append':0},{'failure_receipt':failure_receipt,'reentry_error':err,'no_reentry_writes':before==(len(w.native.calls),w.appends)})

# Literal old-row preservation must observe FORMULA as well as value responses.
w=setup('postappend_old_cell_formula','ledger');w.formula_after=True;before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'ledger')
# One append is necessary before the injected provider corruption is observable.
record('postappend_old_cell_formula',w,False,a,e,before,{'native':0,'append':1})
for value in [1,True]:
    label='old_cell_'+type(value).__name__;w=setup(label);w.rows.append([value,'','',''])
    with w.installed():a,e=run(w,'resume-stage')
    record(label,w,False,a,e,(0,0),{'native':0,'append':0})

# Strict recursive response types: Python's dict equality can equate zero and
# false in echoed numeric range/metadata structures even when cells are strings.
for kind in ['boolean_grid_echo','formula_only_boolean_echo','metadata_bool_drift']:
    label=kind;w=setup(label);original=w.command;meta=[0]
    def command(argv,body=None):
        result=original(argv,body)
        if argv[0]=='gws' and argv[3:5]==['values','batchGetByDataFilter']:
            payload=json.loads(argv[argv.index('--json')+1])
            if kind=='boolean_grid_echo' or kind=='formula_only_boolean_echo' and payload['valueRenderOption']=='FORMULA':result['valueRanges'][0]['dataFilters'][0]['gridRange']['startColumnIndex']=False
        if kind=='metadata_bool_drift' and argv[0]=='gws' and argv[3]=='get':
            meta[0]+=1;result['sheets'][0]['properties']['hidden']=False if meta[0]%2 else 0
        return result
    w.command=command
    with w.installed():a,e=run(w,'resume-stage')
    record(label,w,False,a,e,(0,0),{'native':0,'append':0},{'malformed_provider_structure':kind})

# Guard-age check at a native edge, and fresh unused guard consumption.
w=setup('upload_native_ages_during_fsync');writer=c.durable;offset=[0];real_datetime=c.dt.datetime
class NativeClock(real_datetime):
    @classmethod
    def now(cls,tz=None):return real_datetime.now(tz)+datetime.timedelta(seconds=offset[0])
def age(path,value):
    writer(path,value)
    if path.name.startswith('WRITE_stage_upload_'):offset[0]=31
with model.patch((c,'durable',age),(c.dt,'datetime',NativeClock)),w.installed():a,e=run(w,'resume-stage')
record('upload_native_ages_during_fsync',w,False,a,e,(0,0),{'native':1,'append':0})
w=setup('direct_edge_no_guard');args=types.SimpleNamespace(deposit_id=None,clearance_sha256=w.clearance_sha,operations_sha256=MS,expected_pr_head=m.HEAD)
with w.installed():
    guard=pub.GuardedClient(args,'stage',None)
    try:guard.delegate.create(guard.metadata);a={};e=None
    except Exception as exc:a=None;e={'type':type(exc).__name__,'message':str(exc)}
record('direct_edge_no_guard',w,False,a,e,(0,0),{'native':0,'append':0},{'component_case':True})

poison=types.ModuleType('ops_common');poison.POISON=True
with model.patch((sys,'modules',{**sys.modules,'ops_common':poison,'zenodo':poison,'checked_lifecycle06':poison})):
    freshmodule=boot['load_verified'](SOURCE,MS,BS)
need(freshmodule.c is not poison and hasattr(freshmodule.pl,'GuardedClient'),'Module substitution entered verified loader')
loader_checks={'sys_modules_project_poison_ignored':True}
for filename in ['pr_policy06.py','lifecycle06.py']:
    try:exec(compile((SOURCE/filename).read_bytes(),str(SOURCE/filename),'exec'),{'__name__':'direct'})
    except RuntimeError:loader_checks['direct_'+filename+'_refused']=True
    else:raise RuntimeError('Direct unverified source accepted')
need(not model.ATTEMPTS,'Real network/process interface attempted')
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':MODE,
        'source_sha256':MS,'bootstrap_sha256':BS,'case_count':len(checks),
        'actual_parsed_CLI_cases':sum(not q.get('component_case',False) for q in checks),
        'counterexamples':[q['case'] for q in checks if q['status']=='COUNTEREXAMPLE'],
        'results':checks,'loader_checks':loader_checks,'real_escape_attempts':model.ATTEMPTS,
        'real_service_or_Git_mutations':0,'allocated_bytes':allocated(),'publication_ready':False}
(DEST/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
