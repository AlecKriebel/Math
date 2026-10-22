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

