"""Actual parsed07 lifecycle with fully intercepted provider adapters; no real I/O."""
from pathlib import Path
import contextlib,copy,datetime,hashlib,io,json,os,sys,types

REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW.parent/'operations07';SOURCE=ROOT/'source';OLD=ROOT.parent/'operations'
MODE='OO' if sys.flags.optimize==2 else 'O' if sys.flags.optimize else 'normal'
DEST=REVIEW/'private'/('parsed_final_'+MODE);DEST.mkdir(exist_ok=False)
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
CONTROL_SHA=sha(Path(__file__).read_bytes())
MS=sha((SOURCE/'SOURCE_MANIFEST.json').read_bytes());BS=sha((SOURCE/'bootstrap07.py').read_bytes())
base=(OLD/'bootstrap.py').read_bytes();need(sha(base)=='960b33e83135968ab40ef069b1b8876df47b70d1c4ef528bf0d8c836213ac58b','Original bootstrap pin')
ns={'__file__':str(OLD/'bootstrap.py'),'__name__':'checked_old_bootstrap'}
exec(compile(base,str(OLD/'bootstrap.py'),'exec'),ns)
load,_=ns['load_verified'](OLD,'eab69e53e9d32510bbf00d74c1b94b70542a8b29cf326c42f5d974e510f09d00',sha(base))
model=load('full_controls')  # blocks every real network/process escape before loading07
boot={'__file__':str(SOURCE/'bootstrap07.py'),'__name__':'checked07_bootstrap'}
exec(compile((SOURCE/'bootstrap07.py').read_bytes(),str(SOURCE/'bootstrap07.py'),'exec'),boot)
m=boot['load_verified'](SOURCE,MS,BS);c=m.c;pub=m.pl;live=m.live;ir=m.ir
modules={n:m.LOAD05(n) for n in ['ops_common','publish_and_ledger','collect_live','integrate_remote','native_policy']}
c.zenodo.token_for=lambda *a,**k:'OFFLINE_SENTINEL_NO_CREDENTIAL'
c.zenodo.doi_status=lambda doi:{'status':'offline_mock','url':'https://doi.org/'+doi}
results=[];bodies={};actual_durable=c.durable
CAS=REVIEW/'private'/('owned_capture_CAS_'+MODE);CAS.mkdir(exist_ok=True)
archive_ns={'__file__':str(ROOT/'archive_owned.py'),'__name__':'owned_archive_helper'}
exec(compile((ROOT/'archive_owned.py').read_bytes(),str(ROOT/'archive_owned.py'),'exec'),archive_ns)
archive_ns['ARCHIVES']=REVIEW/'private'/('chunk_custody_'+MODE)
archive_ns['ARCHIVES'].mkdir(exist_ok=True)
archive_ns['STORE']=archive_ns['ARCHIVES']/'chunks.zip'
def archive_completed():
    for case in list(DEST.iterdir()):
        if case.is_dir() and (DEST/(case.name+'.json')).exists():
            archive_ns['archive'](case)
            for capture in CAS.iterdir():
                if capture.stat().st_nlink==1:capture.unlink()
def compact(path,value):
    actual_durable(path,value)
    if path.parent.name=='runtime':return
    body=path.read_bytes();key=sha(body);prior=CAS/key
    if prior.exists():need(prior.read_bytes()==body,'Capture dedup mismatch')
    else:os.link(path,prior)
    if path.stat().st_ino!=prior.stat().st_ino:
        tmp=path.with_name(path.name+'.own_dedup')
        try:os.link(prior,tmp);os.replace(tmp,path)
        finally:
            if tmp.exists():tmp.unlink()
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
    ad=json.loads((SOURCE/'ROOT_CLEARANCE07.example.json').read_bytes())
    ad.update(operations07_sources_sha256=MS,bootstrap07_sha256=BS,publication_ready=True,
              whole07_review_adopted=True,unresolved_findings=[],
              root_confirmed_failure_before_delegate_create=True,initial_create_attempt_was_sent=False,
              allowed_actions=['resume-stage','publish','ledger'],instructions='OFFLINE MODEL ONLY; NO PRODUCTION AUTHORITY')
    w.ad_path=rt/'ROOT_OPERATIONAL_CLEARANCE07.json';w.ad_path.write_text(json.dumps(ad,indent=2)+'\n')
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
    need(allocated()<=20*1024*1024,'New allocation budget exceeded')
    (DEST/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n');results.append(r)
    print(json.dumps({'case':label,'status':'PASS','native_writes':len(w.native.calls),'appends':w.appends}),flush=True)


# The scenarios/adjudications below are independently authored for this review.
# Every case invokes checked_lifecycle07.main (actual parsed command surface).
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
    need(allocated()<20*1024*1024,'Review allocated bytes exceed75MiB')
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


# Fresh reviewer-authored scenarios. The adapter setup is a separately pinned
# derivation of the preparer's fake World; decision logic below is independent.
INDEPENDENT_CASES=[]
def check(label,w,action,expected_native,expected_append,expected_success,hook=None,required=None):
    before=(len(w.native.calls),w.appends)
    with (hook or contextlib.nullcontext()),w.installed(): answer,error=run(w,action)
    delta=(len(w.native.calls)-before[0],w.appends-before[1])
    need(delta==(expected_native,expected_append),label+": actual edge delta "+str(delta))
    need((error is None)==expected_success,label+": unexpected success/failure "+str(error))
    if required:required(w,answer,error)
    record(label,w,expected_success,answer,error,before,{'native':expected_native,'append':expected_append})
    INDEPENDENT_CASES.append(label)
    return answer,error

def no_final(phase):
    name={'stage':'ZENODO_STAGE_VERIFIED.json','publish':'ZENODO_PUBLISH_VERIFIED.json','ledger':'LEDGER_VERIFIED.json'}[phase]
    return lambda w,a,e:need(not (m.RUNTIME/name).exists(),"False final certificate: "+name)

w=setup('independent_positive_entire_chain')
with w.installed():
    for action in ['resume-stage','publish','verify-public','ledger']:
        a,e=run(w,action);need(e is None,"Positive full chain "+action+": "+str(e))
need(len(w.native.calls)==5 and w.appends==1 and a['verified'] is True,"positive actual edges")
record('independent_positive_entire_chain',w,True,a,e,(0,0),{'native':5,'append':1})
INDEPENDENT_CASES.append('independent_positive_entire_chain')

w=setup('independent_lost_create_no_reallocation')
original=w.native.create
def lost(md):
    original(md)
    raise c.zenodo.DepositError("Independent simulated connection loss after successful create")
w.native.create=lost
check('independent_lost_create_no_reallocation',w,'resume-stage',1,0,False,required=no_final('stage'))
count=len(w.native.calls)
with w.installed():a,e=run(w,'resume-stage')
need(e is not None and len(w.native.calls)==count and w.native.allocated,"Ambiguous create was retried")
(DEST/'lost_create_reentry.json').write_text(json.dumps({'error':e,'create_count':w.native.calls.count('create'),'new_service_calls':len(w.native.calls)-count,'state_exists':c.zenodo.local_state(pub.MANIFEST.resolve(),'production')[1] is not None},indent=2)+'\n')

w=setup('independent_lost_publish_preserved_exact_family','publish');w.native.lost=True
check('independent_lost_publish_preserved_exact_family',w,'publish',1,0,True,
      required=lambda w,a,e:need((m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists() and w.native.published,"Known successful POST not reconciled"))
before=len(w.native.calls)
with w.installed():a,e=run(w,'publish')
need(e is not None and len(w.native.calls)==before,"Second publish POST after known success")
(DEST/'lost_publish_reentry.json').write_text(json.dumps({'error':e,'new_service_calls':len(w.native.calls)-before},indent=2)+'\n')

w=setup('independent_perwrite_fsync_OSerror_before_POST','publish')
writer=c.durable
def own_error(path,value):
    writer(path,value)
    if path.name=='WRITE_publish_publish_INTENT.json':raise OSError("Independent post-fsync exception")
check('independent_perwrite_fsync_OSerror_before_POST',w,'publish',0,0,False,
      model.patch((c,'durable',own_error)),no_final('publish'))

w=setup('independent_swallowed_summary_OSerror_plus_intent_drift','publish')
save=c.zenodo.save_state;hits=[0]
def altered_save(path,value):
    save(path,value)
    if 'publication' in value and hits[0]==0:
        hits[0]+=1;p=m.RUNTIME/'ZENODO_PUBLISH_INTENT.json';v=json.loads(p.read_bytes());v['id']=999;p.write_text(json.dumps(v)+'\n')
        raise OSError("Independent swallowed summary receipt exception after changed own intent")
check('independent_swallowed_summary_OSerror_plus_intent_drift',w,'publish',1,0,False,
      model.patch((c.zenodo,'save_state',altered_save)),no_final('publish'))
need(hits[0]==1,"Summary save hook not exercised")

w=setup('independent_swallowed_summary_OSerror_plus_revocation','publish')
save=c.zenodo.save_state;hits=[0]
def revoked_save(path,value):
    save(path,value)
    if 'publication' in value and hits[0]==0:
        hits[0]+=1;w.ad_path.rename(w.ad_path.with_suffix('.revoked'))
        raise OSError("Independent swallowed summary exception after authority revocation")
check('independent_swallowed_summary_OSerror_plus_revocation',w,'publish',1,0,False,
      model.patch((c.zenodo,'save_state',revoked_save)),no_final('publish'))
need(hits[0]==1,"Summary revocation hook not exercised")

# Full raw unknown fields have type-sensitive identity across both native Sheets views.
for kind in ['unknown_int_to_bool','unknown_float_to_int']:
    label='independent_raw_sheet_'+kind;w=setup(label);original=w.command
    def command(argv,body=None):
        v=original(argv,body)
        if argv[0]=='gws' and argv[3:5]==['values','batchGetByDataFilter']:
            mode=json.loads(argv[argv.index('--json')+1])['valueRenderOption']
            v['unknownReviewerField']=0 if mode=='UNFORMATTED_VALUE' else False if kind=='unknown_int_to_bool' else 0.0
        return v
    w.command=command
    check(label,w,'resume-stage',0,0,False,required=no_final('stage'))

for kind in ['approval','own_intent','native_family','metadata']:
    label='independent_final_direct_append_edge_'+kind;w=setup(label,'ledger');writer=c.durable;hit=[False]
    def inject(path,value):
        writer(path,value)
        if path.name=='LEDGER_APPEND_INTENT.json' and not hit[0]:
            hit[0]=True
            if kind=='approval':w.ad_path.rename(w.ad_path.with_suffix('.revoked'))
            elif kind=='own_intent':
                v=json.loads(path.read_bytes());v['record']=999;path.write_text(json.dumps(v)+'\n')
            elif kind=='native_family':
                def drift(l,n,f):
                    l['conceptrecid']='999';l['conceptdoi']='10.5281/zenodo.999'
                    n['parent']['id']='999';n['parent']['pids']['doi']['identifier']='10.5281/zenodo.999'
                w.native.fault=drift
            else:
                orig=w.book
                def driftbook():
                    value=orig();value['reviewerUnknown']={'flag':False};return value
                w.book=driftbook
    check(label,w,'ledger',0,0,False,model.patch((c,'durable',inject)),no_final('ledger'))
    need(hit[0],"Actual append intent hook not hit")

w=setup('independent_latest_native_31second_refresh','ledger');real=c.dt.datetime;offset=[0];gatecount=[0]
class Late(real):
    @classmethod
    def now(cls,tz=None):return real.now(tz)+datetime.timedelta(seconds=offset[0])
def late(*a,**k):offset[0]=31;gatecount[0]+=1
w.gate_hook=late
check('independent_latest_native_31second_refresh',w,'ledger',0,1,True,
      model.patch((c.dt,'datetime',Late)),lambda w,a,e:need(gatecount[0]>0 and a['verified'],"Refresh positive control"))

w=setup('independent_postappend_unknown_full_metadata_drift','ledger');original=w.command;hit=[False]
def after_append(argv,body=None):
    v=original(argv,body)
    if w.appends and argv[0]=='gws' and argv[3]=='get':
        hit[0]=True;v['newUnknownField']={'nested':[1,False]}
    return v
w.command=after_append
check('independent_postappend_unknown_full_metadata_drift',w,'ledger',0,1,False,required=no_final('ledger'))
need(hit[0],"Postappend metadata hook not hit")

w=setup('independent_lost_append_strict_GET_reconciliation','ledger');w.append_mode='lost'
check('independent_lost_append_strict_GET_reconciliation',w,'ledger',0,1,False,required=no_final('ledger'))
count=w.appends
with w.installed():a,e=run(w,'ledger')
need(e is None and a['new_row'] is False and w.appends==count==1 and a['verified'] is True,"Lost append not one exact GET-only reentry")
(DEST/'lost_append_reentry.json').write_text(json.dumps({'answer':a,'new_appends':w.appends-count,'total_appends':w.appends},indent=2)+'\n')

# Before mutation the exact owner/concept, source, original trusted failure context
# and accepted merged scientific subtree must survive every long gate.
for kind in ['source','old_reconciliation','current_main']:
    label='independent_stage_long_gate_'+kind;w=setup(label);hit=[False]
    def change(*a,**k):
        if not hit[0]:
            hit[0]=True
            if kind=='source':
                p=m.CONTEXT['source_root']/'sheet07.py';p.write_bytes(p.read_bytes()+b'\n# independent controlled drift\n')
            elif kind=='old_reconciliation':
                p=m.PRIOR_RUNTIME/'ROOT_STAGE_FAILURE_READONLY_RECONCILIATION.json';v=json.loads(p.read_bytes());v['no_service_mutation']=False;p.write_text(json.dumps(v)+'\n')
            else:
                orig=w.git.get
                def bad(endpoint):
                    if endpoint=='compare/'+m.MERGE+'...main':return {'status':'diverged','merge_base_commit':{'sha':'e'*40}}
                    return orig(endpoint)
                w.git.get=bad
    w.gate_hook=change
    check(label,w,'resume-stage',0,0,False,required=no_final('stage'))
    need(hit[0],"Long gate hook not reached")

archive_completed()
need(not model.ATTEMPTS,"External escape attempted")
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':MS,'bootstrap_sha256':BS,
        'case_engine_derivation':'Fresh copy of final_controls07 definitions before scenario execution with only destination/source locations and20MiB budget changed; independent scenario logic in this file.',
        'independent_scenarios':INDEPENDENT_CASES,'scenario_count':len(checks),'parser_invocations_including_setups':len(CLI_INVOCATIONS),
        'counterexamples':[x['case'] for x in checks if x['status']!='PASS'],'results':checks,
        'external_attempts':model.ATTEMPTS,'real_service_or_Git_mutations':0,'allocated_bytes':allocated(),'publication_ready':False}
(DEST/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in {'results','independent_scenarios'}},indent=2))
