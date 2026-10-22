"""Actual parsed06 lifecycle with fully intercepted provider adapters; no real I/O."""
from pathlib import Path
import contextlib,copy,datetime,hashlib,io,json,os,sys,types

ROOT=Path(__file__).resolve().parent;SOURCE=ROOT/'source';OLD=ROOT.parent/'operations'
MODE='OO' if sys.flags.optimize==2 else 'O' if sys.flags.optimize else 'normal'
DEST=ROOT/'private'/('controls_v3_'+MODE);DEST.mkdir(exist_ok=False)
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
    for p in [ROOT,*ROOT.rglob('*')]:
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
    need(allocated()<=120*1024*1024,'New allocation budget exceeded')
    (DEST/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n');results.append(r)
    print(json.dumps({'case':label,'status':'PASS','native_writes':len(w.native.calls),'appends':w.appends}),flush=True)

# Grammar coverage is deliberately bounded; do not reintroduce a substring
# fallback that truncates longer integers or treats other-repository URLs as ours.
positive=['PR1131','PR #1131','PR: # 001131','pull request1131','pull request 1131',
          'pull request #1131','PULL\u2003REQUEST : #001131',
          'https://github.com/AlecKriebel/Math/pull/1131',
          'HTTPS://WWW.GITHUB.COM/ALECKRIEBEL/MATH/PULL/001131/?a=2#x',
          'pull%20request%20%231131','p\u200br1131','ＰＲ１１３１']
negative=['1131','PR11310','PR1131.0','prePR1131','PR1131x','PR_1131',
          'pullrequest1131','pull request11310','pull request1131.7','pull requests1131',
          'https://github.com/Other/Math/pull/1131','https://github.com/AlecKriebel/Math/pull/11310',
          'https://github.com/AlecKriebel/Math/pull/1131.5','https://github.com/AlecKriebel/Math/pull/1131evil']
for s in positive:need(m.PR_POLICY.known_pr(s,live.decoded),'Missing bounded known reference '+repr(s))
for s in negative:need(not m.PR_POLICY.known_pr(s,live.decoded),'False known reference '+repr(s))

w=world('complete_original_manifest_lifecycle')
with w.installed():
    staged=cli(w);pubresult=cli(w,'publish');ledger=cli(w,'ledger')
    before=list(w.native.calls);again=failure(lambda:cli(w))
need(staged['id']==777 and ledger['verified'] and w.appends==1
     and w.native.calls==before and w.native.calls.count('create')==w.native.calls.count('publish')==1,
     'Complete actual06 parsed lifecycle/reentry')
finish('complete_original_manifest_lifecycle',w,again,{'staged':staged,'publication':pubresult,'ledger':ledger})

w=world('guard_expires_during_edge_intent_fsync');holder={};actual_guard=pub.GuardedClient;writer=c.durable
def guard(*a,**k):
    instance=actual_guard(*a,**k);holder['guard']=instance;return instance
def expires(path,value):
    writer(path,value)
    if path.name=='WRITE_stage_create_INTENT.json':
        holder['guard'].edge_gate['at_start']='2000-01-01T00:00:00+00:00'
with model.patch((pub,'GuardedClient',guard),(c,'durable',expires)),w.installed():error=failure(lambda:cli(w))
need(not w.native.calls and 'Expired/future observation' in error['message'],'Expired gate reached delegate after intent fsync')
finish('guard_expires_during_edge_intent_fsync',w,error)

for kind in ['adoption','old_intent']:
    for boundary in [1,2,3,4]:
        label=kind+'_after_long_guard_'+str(boundary);w=world(label);seen=[0]
        def late(*a,**k):
            seen[0]+=1
            if seen[0]==boundary:
                if kind=='adoption':w.ad_path.rename(w.ad_path.with_suffix('.revoked'))
                else:
                    path=m.PRIOR_RUNTIME/'ZENODO_STAGE_INTENT.json';v=json.loads(path.read_bytes());v['id']=999
                    path.write_text(json.dumps(v)+'\n')
        w.gate_hook=late
        with w.installed():error=failure(lambda:cli(w))
        need(seen[0]==boundary and len(w.native.calls)==boundary-1
             and not (m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Postguard context drift reached a delegated write')
        finish(label,w,error,{'guard_boundary':boundary,'delegated_writes_before_boundary':boundary-1})

for kind in ['source','reconciliation']:
    w=world('late_'+kind)
    def late(*a,**k):
        if kind=='source':
            path=m.CONTEXT['source_root']/'lifecycle06.py';path.write_bytes(path.read_bytes()+b'\n')
        else:
            path=m.PRIOR_RUNTIME/'ROOT_STAGE_FAILURE_READONLY_RECONCILIATION.json'
            v=json.loads(path.read_bytes());v['state_absent']=False;path.write_text(json.dumps(v)+'\n')
    w.gate_hook=late
    with w.installed():error=failure(lambda:cli(w))
    need(not w.native.calls and not (m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Late source/recon drift accepted')
    finish('late_'+kind,w,error)

for label,channel,text in [('compact_ledger','ledger','pull request1131'),
                           ('spaced_ledger','ledger','pull request 1131'),
                           ('hash_ledger','ledger','pull request #1131'),
                           ('account','account','pull request1131'),
                           ('source_nested','source','pull request #001131'),
                           ('result_nested','result','pull request 1131'),
                           ('local_state','local','pull request #1131')]:
    w=world('reference_'+label)
    if channel=='ledger':w.rows.append(['Incomplete target','','',text])
    elif channel in {'account','source','result'}:
        if channel=='account':w.accounts[0]['metadata']['description']=text
        else:w.accounts[0].setdefault('extra',{})[channel]={'nested_evidence':[{'note':text}]}
    else:
        (live.REPO/'.zenodo-state/unrelated.json').write_text(json.dumps({'id':42,'note':text})+'\n')
    with w.installed():error=failure(lambda:cli(w))
    need(not w.native.calls and not (m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Explicit known source lead reached creation')
    finish('reference_'+label,w,error,{'channel':channel,'lead_requires_semantic_reconciliation':True})

for kind in ['root_not_ready','prior_attempt_not_false','saved_state']:
    w=world(kind)
    if kind=='saved_state':
        path=c.zenodo.state_path(pub.MANIFEST.resolve(),'production')
        path.parent.mkdir();path.write_text(json.dumps({'id':777,'manifest':str(pub.MANIFEST.resolve()),'environment':'production'})+'\n')
    else:
        ad=json.loads(w.ad_path.read_bytes());ad['publication_ready' if kind=='root_not_ready' else 'initial_create_attempt_was_sent']=False if kind=='root_not_ready' else True
        w.ad_path.write_text(json.dumps(ad)+'\n');w.clearance_sha=sha(w.ad_path.read_bytes())
    with w.installed():error=failure(lambda:cli(w))
    need(not w.native.calls,'Invalid initial resumption premise reached creation')
    finish(kind,w,error)

for phase in ['create','upload','known_id_native_invalid','update_context_drift']:
    w=world('unknown_'+phase)
    if phase in {'create','upload'}:
        original=getattr(w.native,phase)
        def lost(*a,**k):original(*a,**k);raise c.zenodo.DepositError('Independent loss after model success')
        setattr(w.native,phase,lost)
    elif phase=='known_id_native_invalid':
        w.native.fault=lambda l,n,f:n['access'].__setitem__('files','restricted')
    else:
        original=w.native.update
        def changed(*a,**k):
            result=original(*a,**k);path=m.PRIOR_RUNTIME/'ZENODO_STAGE_INTENT.json'
            v=json.loads(path.read_bytes());v['id']=999;path.write_text(json.dumps(v)+'\n');return result
        w.native.update=changed
    with w.installed():
        error=failure(lambda:cli(w));before=list(w.native.calls);again=failure(lambda:cli(w))
    receipt=json.loads((m.RUNTIME/'RESUME_STAGE_FAILURE.json').read_bytes())
    need(w.native.calls==before and w.native.calls.count('create')==1
         and not (m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Unknown outcome restaged or falsely verified')
    if phase!='create':need(receipt['delegate_known_id']==777,'Known service ID lost')
    finish('unknown_'+phase,w,error,{'failure_receipt':receipt,'reentry_error':again})

for phase in ['first_upload','second_upload','metadata_update','publication','ledger']:
    w=world('family_'+phase);active=[False]
    other=next(r['id'] for r in w.accounts if r['id']!=23408971 and not any(live.semantic(t) for t in live.strings(r)))
    def account(records,page):
        if active[0] and any(r['id']==777 for r in records):
            for r in records:
                if r['id'] in {777,other}:
                    concept=999 if r['id']==777 else 778
                    r['conceptrecid']=str(concept);r['conceptdoi']='10.5281/zenodo.'+str(concept)
                    r['metadata'].setdefault('relations',{})['version']=[{'index':0,'is_last':True,'parent':{'pid_type':'recid','pid_value':str(concept)}}]
        return records
    w.account_fault=account
    if phase=='first_upload':active[0]=True
    if phase in {'second_upload','metadata_update'}:
        original=w.native.upload
        def uploaded(*a,**k):
            result=original(*a,**k)
            if len(w.native.present)==(1 if phase=='second_upload' else 2):active[0]=True
            return result
        w.native.upload=uploaded
    action='resume-stage'
    with w.installed():
        if phase in {'publication','ledger'}:
            cli(w);action='publish'
            if phase=='ledger':cli(w,'publish');action='ledger'
            active[0]=True
        before=w.native.calls.count('publish');error=failure(lambda:cli(w,action))
    need('Account/native target families disagree' in error['message']
         and w.native.calls.count('publish')==before and w.appends==0,'Inherited05 native-family binding lost')
    finish('family_'+phase,w,error)

w=world('nearby_PR11310_is_not1131');w.rows.append(['Unrelated source','','','pull request #11310'])
with w.installed():answer=cli(w)
need(answer['id']==777 and w.native.calls.count('create')==1,'Longer PR number truncated to1131')
finish('nearby_PR11310_is_not1131',w,None,{'near_number_is_not_target':True})

w=world('postappend_equivalent_old_formula')
with w.installed():
    cli(w);cli(w,'publish');w.formula_after=True
    error=failure(lambda:cli(w,'ledger'));before=w.appends;again=failure(lambda:cli(w,'ledger'))
need(w.appends==before==1 and 'Formula/unformatted' in error['message']
     and not (m.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Postappend formula falsely certified')
finish('postappend_equivalent_old_formula',w,error,{'reentry_error':again})
for name,value in [('numeric',1),('boolean',True)]:
    w=world('old_'+name);w.rows.append([value,'','',''])
    with w.installed():error=failure(lambda:cli(w))
    need(not w.native.calls and 'four-cell schema' in error['message'],'Typed old-cell schema bypass')
    finish('old_'+name,w,error)

need(not model.ATTEMPTS,'A real external interface was attempted')
for n,p in m.F['prior_runtime_files'].items():need({'bytes':len((OLD/'runtime'/n).read_bytes()),'sha256':sha((OLD/'runtime'/n).read_bytes())}==p,'Actual old runtime changed')
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':MODE,'status':'PASS',
        'sources_sha256':MS,'bootstrap_sha256':BS,'controls_source_sha256':CONTROL_SHA,'full_parsed_CLI_cases':len(results),
        'grammar_positive':len(positive),'grammar_negative':len(negative),'results':results,
        'actual_old_runtime_all13_pins_unchanged':True,'real_external_attempts':model.ATTEMPTS,
        'real_external_mutations':0,'allocated_new_bytes':allocated(),'publication_ready':False}
(DEST/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
