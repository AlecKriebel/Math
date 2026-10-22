"""Independent finite controls of the actual proposed resume() implementation.

Unchanged sealed production package/merge/account/native decision functions run
against the retained provider model. Only owned paths, exact fixture identities
and external transports are redirected. No actual service call is possible.
"""
from pathlib import Path
import argparse, contextlib, copy, hashlib, io, json, os, sys

ROOT=Path(__file__).resolve().parent
INFO=json.loads((ROOT/'private/MIRROR.json').read_bytes())
MIRROR=Path(INFO['mirror']); OPS=Path(INFO['operations'])
SOURCE=ROOT/'private/resume_known_unattempted_stage.py'
BS='960b33e83135968ab40ef069b1b8876df47b70d1c4ef528bf0d8c836213ac58b'
MS='eab69e53e9d32510bbf00d74c1b94b70542a8b29cf326c42f5d974e510f09d00'
WS='cc3b78b9728f4dbc9b5f3a899e7d5029c872387ab5af989ecddd1feb04d5bf6a'
MODE='OO' if sys.flags.optimize==2 else 'O' if sys.flags.optimize else 'normal'
DEST=ROOT/'private'/('cases_'+MODE); DEST.mkdir(exist_ok=False)
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def allocated():
    seen=set();out=0
    for p in ROOT.rglob('*'):
        st=p.lstat();k=st.st_dev,st.st_ino
        if k not in seen:out+=st.st_blocks*512;seen.add(k)
    return out
boot=(OPS/'bootstrap.py').read_bytes();need(sha(boot)==BS,'bootstrap source')
ns={'__file__':str(OPS/'bootstrap.py'),'__name__':'independent_verified_bootstrap'}
exec(compile(boot,str(OPS/'bootstrap.py'),'exec'),ns)
load,_=ns['load_verified'](OPS,MS,BS)
# The sealed model disables networking, credentials and subprocesses before
# loading actual lifecycle modules. Its definitions are reused, not its cases.
model=load('full_controls')
ops,modules,checked_load,_=model.load_bundle(MIRROR)
c=modules['ops_common'];pub=modules['publish_and_ledger'];ir=modules['integrate_remote']
actual_durable=c.durable;dedup={};results=[]
def compact(path,value):
    actual_durable(path,value)
    b=path.read_bytes();key=sha(b);prior=dedup.get(key)
    if prior is not None and prior.exists() and prior!=path:
        need(prior.read_bytes()==b,'runtime dedup equality')
        t=path.with_name(path.name+'.review-dedup')
        os.link(prior,t);os.replace(t,path)
    else:dedup[key]=path
for module in modules.values():
    if hasattr(module,'durable'):module.durable=compact

def setup_transport_paths(place):
    rt=place/'ops/runtime';pr=place/'captures';rt.mkdir(parents=True);pr.mkdir()
    for module in modules.values():
        if hasattr(module,'RUNTIME'):module.RUNTIME=rt
        if hasattr(module,'PRIVATE'):module.PRIVATE=pr
    c.zenodo.STATE_DIR=place/'.zenodo-state'
    cl=json.loads((ops/'ROOT_OPERATIONAL_CLEARANCE.example.json').read_bytes())
    cl.update(operations_manifest_sha256=MS,bootstrap_sha256=BS,publication_ready=True,
              unresolved_operational_findings=[],root_complete_reports_read_and_all_seals_verified=True,
              allowed_actions=['integrate','pr-description','ready','merge','stage','publish','ledger'],
              instructions='INDEPENDENT OFFLINE FIXTURE ONLY; NO PRODUCTION AUTHORITY')
    write(rt/'ROOT_OPERATIONAL_CLEARANCE.json',cl)
    return rt,sha((rt/'ROOT_OPERATIONAL_CLEARANCE.json').read_bytes())

# Execute actual integration once per mode, then clone the resulting valid
# provider state and exact merge receipt for the focused wrapper cases.
base=DEST/'base';base.mkdir();base_rt,base_clear=setup_transport_paths(base)
base_world=model.World(ops,modules);base_world.clearance_sha=base_clear
with base_world.installed():base_world.through_merge()
merged=json.loads((base_rt/'MERGE_VERIFIED.json').read_bytes())
base_git={k:copy.deepcopy(v) for k,v in base_world.git.__dict__.items() if k not in {'c','ops'}}

def world(label):
    place=DEST/label;place.mkdir();rt,clsha=setup_transport_paths(place)
    w=model.World(ops,modules);w.clearance_sha=clsha
    for k,v in base_git.items():setattr(w.git,k,copy.deepcopy(v))
    write(rt/'MERGE_VERIFIED.json',merged)
    wrapper=place/'wrapper.py';source=SOURCE.read_bytes();need(sha(source)==WS,'actual wrapper source')
    wrapper.write_bytes(source)
    n={'__file__':str(wrapper),'__name__':'independent_actual_resume_source'}
    exec(compile(source,str(wrapper),'exec'),n)
    # Explicit input/path fixtures; function implementation bytes are unchanged.
    n['OPS']=place/'ops';n['CLEAR']=clsha;n['HEAD']=w.git.head
    old={'action':'stage','head':w.git.head,'id':None,'manifest':str(pub.MANIFEST),
         'manifest_sha256':sha(pub.MANIFEST.read_bytes()),'at':'2026-10-22T09:07:05+00:00',
         'rule':'OFFLINE ORIGINAL INTENT: preserve; unknown outcome GET-only'}
    write(rt/'ZENODO_STAGE_INTENT.json',old)
    oldbytes=(rt/'ZENODO_STAGE_INTENT.json').read_bytes()
    recon={'original_intent_sha256':sha(oldbytes),'original_intent_preserved':True,
           'state_absent':True,'no_service_mutation':True,'no_retry_performed':True,
           'scope':'OFFLINE fixture of explicit root no-attempt adjudication, not a new absence inference'}
    write(rt/'ROOT_STAGE_FAILURE_READONLY_RECONCILIATION.json',recon)
    ad={'wrapper_sha256':WS,'original_stage_intent_sha256':sha(oldbytes),
        'operations_manifest_sha256':MS,'whole_operations_review_sha256':n['REVIEW'],
        'pr':1131,'head':w.git.head,'allowed_action':'FIRST_CREATE_FOR_ORIGINAL_STAGE_INTENT_ONLY',
        'root_confirmed_failure_before_delegate_create':True,'initial_create_attempt_was_sent':False,
        'unresolved_findings':[],
        'readonly_reconciliation_sha256':sha((rt/'ROOT_STAGE_FAILURE_READONLY_RECONCILIATION.json').read_bytes())}
    ap=rt/'ROOT_KNOWN_UNATTEMPTED_STAGE_RESUMPTION_ADOPTION.json';write(ap,ad)
    args=argparse.Namespace(source_sha256=WS,adoption_sha256=sha(ap.read_bytes()),execute=True)
    return w,n,args,rt,ap,oldbytes

def invoke(w,n,args):
    with w.installed():return n['resume'](args,checked_load)
def error(fn):
    try:fn()
    except Exception as e:return {'type':type(e).__name__,'message':str(e)}
    raise RuntimeError('Expected failure accepted')
def record(label,w,rt,exception=None,extra=None):
    entry={'case':label,'native_calls':list(w.native.calls),'create_POSTs':w.native.calls.count('create'),
           'upload_attempts':sum(v.startswith('upload:') for v in w.native.calls),
           'update_attempts':w.native.calls.count('update'),'exception':exception,
           'resumption_intent':(rt/'ROOT_STAGE_RESUMPTION_INTENT.json').exists(),
           'stage_verified':(rt/'ZENODO_STAGE_VERIFIED.json').exists(),
           'failure_receipt':(rt/'ROOT_STAGE_RESUMPTION_FAILURE.json').exists(),
           'account_page_observations':len([v for v in w.events if 'account_page' in v]),
           'dual_numeric_reads':w.numeric_calls,'actual_external_mutations':0,**(extra or {})}
    results.append(entry);write(DEST/(label+'.json'),entry)
    need(allocated()<50*1024*1024,'new owned allocation exceeds50MiB')
    print(json.dumps({'case':label,'create':entry['create_POSTs'],'uploads':entry['upload_attempts'],
                      'stage_verified':entry['stage_verified']}),flush=True)

w,n,args,rt,ap,old=world('valid_first_actual_stage')
out=invoke(w,n,args)
need(out['state']=='ready_to_publish' and out['id']==777 and w.native.calls==
     ['create',*[('upload:'+e['name']) for e in w.native.uploads],'update'],'valid complete stage')
need((rt/'ZENODO_STAGE_INTENT.json').read_bytes()==old,'old intent preserved')
record('valid_first_actual_stage',w,rt,extra={'result':out})

for label,mutation in [
 ('initial_adoption_known_attempt_not_false',lambda ad:ad.__setitem__('initial_create_attempt_was_sent',True)),
 ('initial_adoption_unresolved',lambda ad:ad.__setitem__('unresolved_findings',['unknown outcome'])),
 ('initial_adoption_wrong_action',lambda ad:ad.__setitem__('allowed_action','RETRY_UNKNOWN_CREATE'))]:
    w,n,args,rt,ap,old=world(label);ad=json.loads(ap.read_bytes());mutation(ad);write(ap,ad)
    args.adoption_sha256=sha(ap.read_bytes())
    e=error(lambda:invoke(w,n,args));need(not w.native.calls and not (rt/'ROOT_STAGE_RESUMPTION_INTENT.json').exists(),'initial adoption guard')
    record(label,w,rt,e)

w,n,args,rt,ap,old=world('existing_saved_state')
place,_=c.zenodo.local_state(pub.MANIFEST.resolve(),'production')
c.zenodo.save_state(place,{'manifest':str(pub.MANIFEST.resolve()),'environment':'production','id':777})
e=error(lambda:invoke(w,n,args));need(not w.native.calls and 'existing target state' in e['message'],'existing state guard')
record('existing_saved_state',w,rt,e)

w,n,args,rt,ap,old=world('existing_resumption_intent')
write(rt/'ROOT_STAGE_RESUMPTION_INTENT.json',{'old':'preserve'})
e=error(lambda:invoke(w,n,args));need(not w.native.calls and 'already entered' in e['message'],'reentry before creation')
record('existing_resumption_intent',w,rt,e)

for label,kind in [('gate_fails_before_create','read'),('create_succeeds_response_lost','lost'),
                   ('known_ID_native_policy_rejects','native'),('upload_succeeds_response_lost','upload')]:
    w,n,args,rt,ap,old=world(label)
    if kind=='read':
        def bad_account(*a):raise RuntimeError('independent pre-create GET failure')
        w.account_fault=bad_account
    elif kind=='lost':
        delegate=w.native.create
        def lost_create(md):
            delegate(md);raise c.zenodo.DepositError('independent POST success response lost')
        w.native.create=lost_create
    elif kind=='native':
        w.native.fault=lambda l,native,f:native['access'].__setitem__('files','restricted')
    else:
        delegate=w.native.upload
        def lost_upload(bucket,entry):
            delegate(bucket,entry);raise c.zenodo.DepositError('independent upload success response lost')
        w.native.upload=lost_upload
    e=error(lambda:invoke(w,n,args));before=list(w.native.calls)
    again=error(lambda:invoke(w,n,args))
    need(w.native.calls==before and not (rt/'ZENODO_STAGE_VERIFIED.json').exists(),'failure must not repeat')
    fr=json.loads((rt/'ROOT_STAGE_RESUMPTION_FAILURE.json').read_bytes())
    need(fr['unknown_outcome_requires_GET_only_reconciliation'] is True,'unknown must retain hold')
    if kind=='read':need(w.native.calls==[] and fr['client_target_id'] is None,'pre-create read has no mutation')
    if kind=='lost':need(w.native.calls==['create'] and fr['client_target_id'] is None,'unknown create must not infer no POST')
    if kind=='native':need(w.native.calls==['create'] and fr['client_target_id']==777,'known allocated ID preserved')
    if kind=='upload':need(w.native.calls.count('create')==1 and len(w.native.calls)==2 and fr['client_target_id']==777,'upload unknown retains ID')
    record(label,w,rt,e,{'reentry_error':again,'failure_capture':fr})

for label,kind in [('late_original_clearance_change','clearance'),('late_merge_head_change','head'),
                   ('late_resumption_adoption_revoked','adoption'),('late_old_stage_intent_changed','old_intent')]:
    w,n,args,rt,ap,old=world(label);gates=[0]
    def drift(*a,**k):
        if a[0]!='before_stage':return
        gates[0]+=1
        if gates[0]!=1:return
        if kind=='clearance':
            q=rt/'ROOT_OPERATIONAL_CLEARANCE.json';v=json.loads(q.read_bytes());v['publication_ready']=False;write(q,v)
        elif kind=='head':w.git.head='d'*40
        elif kind=='adoption':
            v=json.loads(ap.read_bytes());v['root_confirmed_failure_before_delegate_create']=False;v['unresolved_findings']=['revoked before first actual create'];write(ap,v)
        else:
            q=rt/'ZENODO_STAGE_INTENT.json';v=json.loads(q.read_bytes());v['id']=999;v['rule']='Concurrent root reconciliation now identifies an existing possible target';write(q,v)
    w.gate_hook=drift
    if kind in {'clearance','head','old_intent'}:e=error(lambda:invoke(w,n,args));out=None
    else:out=invoke(w,n,args);e=None
    if kind in {'clearance','head'}:
        need(w.native.calls==[] and not (rt/'ZENODO_STAGE_VERIFIED.json').exists(),'old production guard must reject drift')
    else:
        need(w.native.calls.count('create')==1 and len(w.native.calls)==4,'new authority/old premise drift actual writes reproduced')
        need((rt/'ZENODO_STAGE_VERIFIED.json').exists(),'stage verification survives new-authority/premise drift')
    record(label,w,rt,e,{'full_stage_gates':gates[0],'result':out,
                        'counterexample':kind in {'adoption','old_intent'},
                        'adoption_original_sha':args.adoption_sha256,'adoption_final_sha':sha(ap.read_bytes()),
                        'old_intent_original_sha':sha(old),'old_intent_final_sha':sha((rt/'ZENODO_STAGE_INTENT.json').read_bytes())})

need(not model.ATTEMPTS,'no actual network/process escape attempt')
out={'mode':MODE,'source_sha256':WS,'operations_sha256':MS,'cases':results,
     'case_count':len(results),'actual_external_mutations':0,
     'real_escape_attempts':model.ATTEMPTS,'allocated_bytes':allocated(),
     'counterexamples':[x['case'] for x in results if x.get('counterexample')]}
write(ROOT/('RESULTS_'+MODE+'.json'),out)
print(json.dumps({'mode':MODE,'cases':len(results),'counterexamples':out['counterexamples'],
                  'allocated_bytes':out['allocated_bytes']}))
