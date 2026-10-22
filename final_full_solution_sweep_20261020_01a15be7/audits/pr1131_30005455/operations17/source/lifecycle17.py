"""Minimal15 overlay: known-unattempted original stage, then existing-ID publish/ledger.
No integration, alternate manifest, approval authoring or automatic write retry.
"""
if not globals().get('_OPS17_VERIFIED',False):raise RuntimeError('Use verified17 bootstrap')
from pathlib import Path
from urllib.parse import quote
import argparse,hashlib,json,re,os,uuid,stat

ROOT=CONTEXT['source_root'].parent
PRIOR=ROOT.parent/'operations'
PRIOR_RUNTIME=PRIOR/'runtime'
RUNTIME=ROOT/'runtime'
PRIVATE=ROOT/'private'
F=CONTEXT['freeze']
HEAD=F['integrated_head']
MERGE=F['merge_commit']
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
OWN_RUNTIME=None
STATE_BINDING=None
ACTION_ARGS=None
ACTION=None
def bind_runtime():
    global OWN_RUNTIME
    need(RUNTIME.is_dir() and not RUNTIME.is_symlink(),'Root15 runtime/approval absent')
    OWN_RUNTIME={}
    for p in RUNTIME.iterdir():
        need(p.is_file() and not p.is_symlink(),'Unexpected runtime entry')
        OWN_RUNTIME[p.name]=c.pin(p.read_bytes())
def runtime_exact():
    need(OWN_RUNTIME is not None,'No parsed action runtime binding')
    need({p.name for p in RUNTIME.iterdir()}==set(OWN_RUNTIME),'Own action history inventory changed')
    for name,pin in OWN_RUNTIME.items():pinned(RUNTIME/name,pin)
def record(path,value):
    """Bind EXPECTED bytes, never adopt whatever an altered writer left behind."""
    need(path.parent==RUNTIME,'Action history outside own runtime')
    need(OWN_RUNTIME is not None and path.name not in OWN_RUNTIME,'Prior action history exists; no retry')
    body=(json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    wanted=c.pin(body);c.durable(path,value);pinned(path,wanted);OWN_RUNTIME[path.name]=wanted
def certify(args,action,name,value,facts):
    """Prepare/fsync evidence privately, then check authority before atomic O_EXCL commit."""
    value={**value,'sources_sha256':CONTEXT['sources_sha256'],'certification_approval_sha256':args.clearance_sha256,
           'original_stage_intent_sha256':F['prior_runtime_files']['ZENODO_STAGE_INTENT.json']['sha256']}
    body=(json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode();wanted=c.pin(body)
    pending=PRIVATE/('certificate_'+uuid.uuid4().hex+'.json');c.durable(pending,value);pinned(pending,wanted)
    local_context(args,action);facts_fresh(facts)
    target=RUNTIME/name;need(name not in OWN_RUNTIME,'Existing final receipt; no overwrite')
    pinned(pending,wanted)  # Expected bytes AFTER the final long authority check.
    os.link(pending,target);OWN_RUNTIME[name]=wanted
    fd=os.open(RUNTIME,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
    local_context(args,action);facts_fresh(facts)
def state_exact(identifier,absent=False):
    state_binding_exact()
    _,state=c.zenodo.local_state(pl.MANIFEST.resolve(),'production')
    if absent:need(state is None,'Original manifest already has state; GET-only reconcile')
    else:need(state is not None and type(state['id']) is int and state['id']==identifier
              and state['manifest']==str(pl.MANIFEST.resolve()) and state['environment']=='production','Original manifest state identity changed')
    return state
def state_place():
    return c.zenodo.state_path(pl.MANIFEST.resolve(),'production')
def state_bytes():
    place=state_place()
    need(not place.parent.is_symlink(),'Canonical state directory symlink')
    try:
        info=place.lstat()
    except FileNotFoundError:return None
    need(stat.S_ISREG(info.st_mode) and not place.is_symlink(),'Canonical state is not a regular file')
    return place.read_bytes()
def bind_state():
    global STATE_BINDING
    raw=state_bytes();STATE_BINDING=None if raw is None else c.pin(raw)
    if raw is not None:
        value=c.strict_json(raw)
        need(isinstance(value,dict) and value.get('manifest')==str(pl.MANIFEST.resolve())
             and value.get('environment')=='production' and type(value.get('id')) is int
             and value['id']>0,'Invalid canonical state binding')
def state_binding_exact():
    raw=state_bytes()
    need((raw is None and STATE_BINDING is None) or (raw is not None and STATE_BINDING==c.pin(raw)),
         'Canonical shared state changed; preserve it and GET-only reconcile known service facts')
def guarded_save_state(place,value):
    """Never replace shared state. Atomic exclusive first install; private later receipts.

    Other processes need not honor any lock. Existing canonical bytes are immutable
    to this actor. Publication summaries remain durable in this action's private
    runtime rather than overriding unknown canonical fields or a concurrent identity.
    """
    global STATE_BINDING
    need(ACTION_ARGS is not None and place==state_place(),'Unbound/noncanonical state save')
    need(isinstance(value,dict) and value.get('manifest')==str(pl.MANIFEST.resolve())
         and value.get('environment')=='production' and type(value.get('id')) is int
         and value['id']>0,'State save identity malformed')
    identifier=value['id']
    local_context(ACTION_ARGS,ACTION)
    if ACTION=='stage':
        need(STATE_BINDING is None and 'publication' not in value,'Initial state already installed; no replacement')
        fact=c.strict_json((RUNTIME/'CREATE_RETURNED_KNOWN_ID.json').read_bytes())
        need(fact['id']==identifier,'Created ID/state save mismatch')
        pending=PRIVATE/('state_initial_'+uuid.uuid4().hex+'.json')
        body=(json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode();wanted=c.pin(body)
        c.durable(pending,value);pinned(pending,wanted)
        local_context(ACTION_ARGS,ACTION);pinned(pending,wanted)
        place.parent.mkdir(mode=0o700,exist_ok=True)
        fd=os.open(place.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            # O_EXCL namespace installation: a late competitor wins without losing
            # a byte. No precheck+replace and no cleanup/removal of foreign state.
            os.link(pending,place.name,dst_dir_fd=fd,follow_symlinks=False)
            os.fsync(fd)
        finally:os.close(fd)
        STATE_BINDING=wanted
        state_binding_exact();local_context(ACTION_ARGS,ACTION)
        record(RUNTIME/'CANONICAL_STATE_INSTALLED.json',{'at':c.stamp(),'id':identifier,
            'canonical_path':str(place),'pin':wanted,'exclusive_initial_install':True})
    else:
        need(ACTION=='publish' and STATE_BINDING is not None,'Only publication may save a later private receipt')
        state_exact(identifier)
        existing=c.strict_json(state_bytes())
        need('publication' in value and SHEET_POLICY.typed_equal({k:v for k,v in value.items() if k!='publication'},
             {k:v for k,v in existing.items() if k!='publication'}),'Publication save changed canonical unknown fields')
        names=[n for n in OWN_RUNTIME if n.startswith('PRIVATE_PUBLICATION_STATE_')]
        name='PRIVATE_PUBLICATION_STATE_'+str(len(names)+1).zfill(2)+'.json'
        record(RUNTIME/name,{'at':c.stamp(),'id':identifier,'canonical_path':str(place),
            'canonical_pin':STATE_BINDING,'requested_state':value,'shared_state_unchanged_by_actor':True})
        local_context(ACTION_ARGS,ACTION);state_exact(identifier)

def pinned(path,pin):
    need(not path.is_symlink() and not path.parent.is_symlink(),'Context symlink')
    b=path.read_bytes();need({'bytes':len(b),'sha256':sha(b)}==pin,'Preserved context changed: '+path.name)
    return b

def local_context(args,action):
    """Pure local adoption/context check, repeated AFTER every long live guard."""
    runtime_exact()
    need(not any(n.startswith('CONSUMED_RESPONSE17_HOLD_')for n in OWN_RUNTIME),'Consumed response/context is on HOLD; preserve known outcome and reconcile by GET only outside this actor')
    state_binding_exact()
    need(args.operations_sha256==CONTEXT['sources_sha256'],'External15 source anchor mismatch')
    CONTEXT['check_sources']()
    original=(PRIOR/'OPERATIONS_MANIFEST.json').read_bytes()
    need(sha(original)==F['prior_operations_manifest_sha256'],'Immutable05 source seal changed')
    manifest=c.strict_json(original)
    need(c.public_files(PRIOR)==set(manifest['files']),'Immutable05 source closure changed')
    for n,p in manifest['files'].items():c.read_pinned(c.safe(PRIOR,n),p)
    c.package();c.proposal()
    need(not (PRIOR_RUNTIME/'ROOT_OPERATIONAL_CLEARANCE.json').exists(),'Revoked05 authority was revived')
    need({p.name for p in PRIOR_RUNTIME.iterdir()}==set(F['prior_runtime_files']),'Preserved05 runtime inventory changed')
    old={n:c.strict_json(pinned(PRIOR_RUNTIME/n,p)) for n,p in F['prior_runtime_files'].items()}
    for n,p in F['prior_wrapper_files'].items():pinned(ROOT.parent/'stage_known_unattempted_resumption01'/n,p)
    for n,p in F['held06_context'].items():pinned(ROOT.parent/n,p)
    need(not (ROOT.parent/'operations06/runtime').exists(),'Held06 runtime appeared; no authority resurrection')
    for n,p in F['held07_context'].items():pinned(ROOT.parent/n,p)
    for n,p in F['held08_context'].items():pinned(ROOT.parent/n,p)
    for n,p in F['held09_context'].items():pinned(ROOT.parent/n,p)
    for n,p in F['held10_context'].items():pinned(ROOT.parent/n,p)
    for n,p in F['held11_context'].items():pinned(ROOT.parent/n,p)
    for n,p in F['held12_context'].items():pinned(ROOT.parent/n,p)
    for n,p in F['held13_context'].items():pinned(ROOT.parent/n,p)
    for n,p in F['held14_context'].items():pinned(ROOT.parent/n,p)
    for n,p in F['held15_context'].items():pinned(ROOT.parent/n,p)
    for n,p in F['held16_context'].items():pinned(ROOT.parent/n,p)
    need(not (ROOT.parent/'operations16/runtime').exists(),'Held16 runtime appeared; no old authority resurrection')
    need(not (ROOT.parent/'operations15/runtime').exists(),'Held15 runtime appeared; no old authority resurrection')
    need(not (ROOT.parent/'operations11/runtime').exists(),'Held11 runtime appeared')
    for n,p in F['actual_phase_reference_inputs'].items():pinned(ROOT.parent.parent/n,p)
    need(not (ROOT.parent/'operations10/runtime').exists(),'Held10 runtime appeared')
    need(not (ROOT.parent/'operations09/runtime').exists(),'Held09 runtime appeared')
    need(not (ROOT.parent/'operations08/runtime').exists(),'Held08 runtime appeared')
    need(not (ROOT.parent/'operations07/runtime').exists(),'Held07 runtime appeared; no authority resurrection')
    stage=old['ZENODO_STAGE_INTENT.json'];recon=old['ROOT_STAGE_FAILURE_READONLY_RECONCILIATION.json']
    oldsha=F['prior_runtime_files']['ZENODO_STAGE_INTENT.json']['sha256']
    need(stage['action']=='stage' and stage['head']==HEAD and stage['id'] is None
         and stage['manifest']==str(pl.MANIFEST.resolve())
         and stage['manifest_sha256']==sha(pl.MANIFEST.read_bytes()),'Original stage intent target changed')
    need(recon['original_intent_sha256']==oldsha and recon['original_intent_preserved'] is True
         and recon['state_absent'] is True and recon['no_service_mutation'] is True
         and recon['no_retry_performed'] is True,'Known-unattempted reconciliation changed')
    need(re.fullmatch('[a-f0-9]{64}',args.clearance_sha256 or ''),'External15 root clearance hash required')
    path=RUNTIME/'ROOT_OPERATIONAL_CLEARANCE17.json'
    need(not path.is_symlink() and not RUNTIME.is_symlink(),'Root15 clearance symlink')
    raw=path.read_bytes();need(sha(raw)==args.clearance_sha256,'Root15 adoption revoked/changed')
    ad=c.strict_json(raw)
    need(ad['pr']==1131 and ad['head']==HEAD and ad['merge_commit']==MERGE
         and ad['operations17_sources_sha256']==CONTEXT['sources_sha256']
         and ad['bootstrap17_sha256']==CONTEXT['bootstrap_sha256']
         and ad['source_freeze_sha256']==sha((CONTEXT['source_root']/'SOURCE_FREEZE.json').read_bytes())
         and ad['prior_operations_manifest_sha256']==F['prior_operations_manifest_sha256']
         and ad['scientific_clearance_sha256']==F['scientific_clearance_sha256']
         and ad['original_stage_intent_sha256']==oldsha
         and ad['readonly_reconciliation_sha256']==F['prior_runtime_files']['ROOT_STAGE_FAILURE_READONLY_RECONCILIATION.json']['sha256']
         and ad['prior_merge_receipt_sha256']==F['prior_runtime_files']['MERGE_VERIFIED.json']['sha256'],
         'Root15 approval source/old context mismatch')
    need(ad['publication_ready'] is True and ad['whole17_review_adopted'] is True
         and ad['unresolved_findings']==[] and ad['root_confirmed_failure_before_delegate_create'] is True
         and ad['initial_create_attempt_was_sent'] is False,'Root15 known-unattempted authority incomplete')
    permitted={'resume-stage','publish','ledger'}
    need(isinstance(ad['allowed_actions'],list) and set(ad['allowed_actions'])<=permitted
         and len(ad['allowed_actions'])==len(set(ad['allowed_actions'])),'Unknown/duplicate08 action')
    mapped='resume-stage' if action=='stage' else action
    need(mapped in ad['allowed_actions'],'Action08 not cleared')
    need(ad['spreadsheet_id']==c.SHEET and type(ad['sheet_id']) is int and ad['sheet_id']==c.SHEET_ID
         and ad['sheet_title']==c.SHEET_TITLE and ad['account_identity_contract']==c.ACCOUNT_IDENTITY_CONTRACT,'Root15 ledger/account binding changed')
    need(not (RUNTIME/'RESUME_STAGE_FAILURE.json').exists(),'Prior08 stage failure: GET-only reconcile; no retry')
    return ad

def require_action(args,action):
    ad=local_context(args,action)
    need(args.expected_pr_head==HEAD,'Only the accepted actual merged head is permitted')
    receipt=c.strict_json(pinned(PRIOR_RUNTIME/'MERGE_VERIFIED.json',F['prior_runtime_files']['MERGE_VERIFIED.json']))
    need(receipt['head']==HEAD and receipt['commit']==MERGE and receipt['tree']==F['merge_tree']
         and receipt['merged'] is True and receipt['unselected_siblings_and_queue_preserved'] is True
         and receipt['original_files']==8 and receipt['preprint_files']==5 and receipt['framing_replacements']==3,'Prior accepted merge receipt differs')
    pr=c.gh('pulls/1131');c.validate_pr(pr,HEAD,True);c.validate_description(pr,HEAD)
    need(pr['merge_commit_sha']==MERGE,'Actual PR merge identity changed')
    actual=c.gh('git/commits/'+MERGE)
    need(actual['sha']==MERGE and actual['tree']['sha']==receipt['tree']
         and [p['sha'] for p in actual['parents']]==receipt['parents'],'Actual merged parents/tree changed')
    relation=c.gh('compare/'+MERGE+'...main')
    need(relation.get('status') in {'identical','ahead'} and relation['merge_base_commit']['sha']==MERGE,'Current main no longer contains accepted merge')
    if action!='stage':
        stage=c.strict_json((RUNTIME/'ZENODO_STAGE_VERIFIED.json').read_bytes())
        resume=c.strict_json((RUNTIME/'RESUME_STAGE_VERIFIED.json').read_bytes())
        need(type(args.deposit_id) is int and args.deposit_id>0 and stage['id']==resume['id']==args.deposit_id
             and stage['state']=='ready_to_publish' and resume['sources_sha256']==CONTEXT['sources_sha256']
             and resume['original_stage_intent_sha256']==F['prior_runtime_files']['ZENODO_STAGE_INTENT.json']['sha256'],
             'Exact08 staged ID/receipt missing')
    local_context(args,action)
    return ad

def verify_merged_payload():
    """GET-only check of the accepted immutable merge's selected frozen subtree."""
    pkg=c.package();_,changes=c.proposal()
    expected={n:pkg['source']['original/'+n] for n in c.ORIGINALS}
    expected.update({p[len(c.PROBLEM)+1:]:b for p,b in changes.items()})
    got=ir.leaves(MERGE,c.PROBLEM)
    need(got=={n:('100644','blob',ir.blob_sha(b)) for n,b in expected.items()},'Accepted merged scientific/kit payload changed')

class ConsumedResponseError(RuntimeError):
    """Never caught by the unchanged tool's inspect-after-DepositError recovery."""

class EdgeDelegate:
    """A local check and durable one-write intent directly at each delegate edge."""
    def __init__(self,delegate,args,action):
        self.delegate,self.args,self.action=delegate,args,action;self.known_id=args.deposit_id;self.poisoned=False;self.last_response=None;self.responses=[]
    @property
    def base(self):return self.delegate.base
    def usable(self):
        need(not self.poisoned,'Consumed response already rejected; no recovery or further use')
        local_context(self.args,self.action)
    def reject(self,kind,exc):
        self.poisoned=True
        name='CONSUMED_RESPONSE17_HOLD_'+uuid.uuid4().hex+'.json'
        record(RUNTIME/name,{'at':c.stamp(),'kind':kind,'known_id':self.known_id,
            'exception_type':type(exc).__name__,'original_response':self.last_response,
            'all_consumed_response_custody':self.responses,
            'rule':'Consumed response/context rejected. No success, phase certificate, publication summary or mutation retry; preserve IDs/intents and reconcile by GET only outside this actor.'})
        raise ConsumedResponseError('Actual consumed '+kind+' response/context rejected; known outcome preserved, no automatic recovery or retry')from exc
    def capture(self,kind,result,known_fact=None):
        """First receipt is one durable full return AND known service fact.

        Register its intended path before IO. Even its own post-fsync integrity
        rejection must leave that receipt discoverable in persistent HOLD.
        Flags distinguish intended custody, returned durable IO and verification;
        neither a failed write nor altered expected bytes becomes certification.
        """
        path=PRIVATE/('service_original_'+uuid.uuid4().hex+'.json')
        value={'at':c.stamp(),'kind':kind,'requested_or_known_id':self.known_id,'response':result}
        if known_fact is not None:value['known_service_fact']=known_fact
        # ASCII escapes preserve EVERY parsed JSON string, including unmatched
        # surrogate code units admitted by the unchanged SDK json.loads path.
        # No normalization or Unicode-scalar assumption precedes durable IO.
        body=(json.dumps(value,sort_keys=True,ensure_ascii=True,indent=2)+'\n').encode('ascii');wanted=c.pin(body)
        self.last_response={'path':str(path),'pin':wanted,'kind':kind,
            'contains_known_service_fact':known_fact is not None,
            'durable_write_returned':False,'expected_integrity_verified':False}
        self.responses.append(self.last_response)
        c.durable(path,value)
        self.last_response['durable_write_returned']=True
        pinned(path,wanted)
        self.last_response['expected_integrity_verified']=True
        return c.strict_json(body)['response'],path,wanted
    def checked_record(self,kind,result,identifier,published=None,required=None,captured=None):
        frozen,path,pin=self.capture(kind,result)if captured is None else captured
        pinned(path,pin);start=c.stamp()
        need(type(identifier)is int and identifier>0,'No exact known positive response target; GET-only account reconciliation required')
        need(type(frozen)is dict and type(frozen.get('submitted'))is bool,'Recognized legacy response/state type')
        if published is None:published=frozen['submitted']
        native=self.delegate.native_get(identifier,draft=not published)
        suffix=''if published else'/draft'
        files=self.delegate.request('GET',self.base+'/api/records/'+str(identifier)+suffix+'/files')
        context=PRIVATE/('response_context_'+uuid.uuid4().hex);context.mkdir(mode=0o700)
        c.durable(context/'native.json',native);c.durable(context/'files.json',files)
        if required is None and(self.action=='publish'or published):required={e['name']for e in self.guard.uploads}
        verified=LOAD05('native_policy').validate_target(frozen,native,files,self.guard.metadata,self.guard.uploads,identifier,published,required)
        verified['observed_at']=start;c.durable(context/'checked_original.json',verified)
        local_context(self.args,self.action);c.fresh(start,seconds=30);pinned(path,pin)
        record(RUNTIME/('RESPONSE_CHECK_'+uuid.uuid4().hex+'.json'),{'at':c.stamp(),'kind':kind,'record':identifier,
            'original':self.last_response,'fresh_context':str(context),'actual_original_validated':True})
        local_context(self.args,self.action);c.fresh(start,seconds=30)
        return c.strict_json(pinned(path,pin))['response'],verified
    def get(self,i):
        try:
            self.usable()
            result=self.delegate.get(i)
            return self.checked_record('get',result,i)[0]
        except BaseException as exc:self.reject('get',exc)
    def native_get(self,*a,**k):return self.delegate.native_get(*a,**k)
    def request(self,method,url):
        need(method=='GET','Unexpected direct native mutation');return self.delegate.request(method,url)
    def mutation(self,kind,*args):
        self.usable()
        need(self.guard.edge_gate is not None and not self.guard.edge_used,'No fresh unused native/account guard for delegated write')
        self.guard.edge_used=True
        local_context(self.args,self.action)
        action_intent='RESUME_STAGE_INTENT.json' if self.action=='stage' else 'ZENODO_PUBLISH_INTENT.json'
        need(action_intent in OWN_RUNTIME,'Missing bound action intention')
        state_exact(self.guard.identifier,absent=kind=='create')
        key=kind
        if kind=='upload':key+='_'+sha(args[1]['name'].encode())
        record(RUNTIME/('WRITE_'+self.action+'_'+key+'_INTENT.json'),{
            'at':c.stamp(),'action':self.action,'kind':kind,'known_id':self.known_id,
            'sources_sha256':CONTEXT['sources_sha256'],'clearance_sha256':self.args.clearance_sha256,
            'original_stage_intent_sha256':F['prior_runtime_files']['ZENODO_STAGE_INTENT.json']['sha256'],
            'rule':'One delegated attempt only. Any ambiguous outcome consumes this intent; GET-only reconcile, never retry.'})
        local_context(self.args,self.action)
        state_exact(self.guard.identifier,absent=kind=='create')
        # Re-observe AFTER the actual durable perwrite intent and long local
        # checks. The old snapshot's age alone never substitutes for this read.
        if kind!='create':
            required=set(self.guard.snapshot['files'])
            _,edge=self.guard.observation(False,required)
            family(self.guard.edge_gate,edge)
        else:
            ad=require_action(self.args,self.action)
            gate,_,_=pl.collect('before_stage',self.args.expected_pr_head,None,cleared=ad)
            self.guard.edge_gate=gate
        local_context(self.args,self.action);runtime_exact()
        state_exact(self.guard.identifier,absent=kind=='create')
        c.fresh(self.guard.edge_gate['at_start'])
        if self.guard.snapshot is not None:c.fresh(self.guard.snapshot['observed_at'],seconds=30)
        self.guard.pending_transition=kind
        try:result=getattr(self.delegate,kind)(*args)
        except BaseException as exc:self.reject(kind+'_unknown_outcome',exc)
        try:
            positive=result.get('id')if type(result)is dict and type(result.get('id'))is int and result['id']>0 else None
            if kind=='create' and positive is not None:self.known_id=positive
            fact={'kind':kind,'requested_or_known_id':self.known_id,
                'returned_positive_id':positive,
                'returned_submitted':result.get('submitted')if type(result)is dict else None,
                'manifest':str(pl.MANIFEST),'sources_sha256':CONTEXT['sources_sha256'],
                'rule':'Returned service fact only, combined with the complete actual original in this first receipt. Not phase certification; preserve outcome and consumed intent, GET-only reconcile, never retry.'}
            # One unique first receipt contains BOTH full actual return and
            # known outcome. No narrower fact recorder/pin check precedes it.
            captured=self.capture(kind,result,known_fact=fact)
            # Fixed-name history is secondary, retaining the first receipt's
            # reference. Failure of its own integrity check cannot lose body or
            # durable known fact already in the combined first receipt.
            if kind=='create' and positive is not None:
                record(RUNTIME/'CREATE_RETURNED_KNOWN_ID.json',{'at':c.stamp(),'id':self.known_id,
                    'manifest':str(pl.MANIFEST.resolve()),'sources_sha256':CONTEXT['sources_sha256'],
                    'original_response':self.last_response,
                    'rule':'Secondary known service fact, not stage certification. Full original and known fact already retained together; GET-only reconcile, no new create.'})
            if kind=='publish':
                record(RUNTIME/'PUBLISH_RETURNED_SERVICE_FACT.json',{'at':c.stamp(),'requested_id':self.known_id,
                    'returned_positive_id':positive,
                    'returned_submitted':result.get('submitted')if type(result)is dict else None,
                    'original_response':self.last_response,
                    'rule':'Secondary returned POST fact, not publication certification. Full original and known fact already retained together; preserve known target and consumed intention.'})
            local_context(self.args,self.action)
            if kind!='create':state_exact(self.guard.identifier)
            if kind=='upload':
                frozen,path,pin=captured
                acknowledgement=self.last_response
                # An upload ACK has no record id. Its independently returned
                # legacy context is checked as its own original response.
                _,verified=self.checked_record('upload_context_get',self.delegate.get(self.known_id),self.known_id,False)
                self.last_response=acknowledgement
                NATIVE_POLICY.PHASE.upload_ack(frozen,args[1],args[0],verified)
                local_context(self.args,self.action);c.fresh(verified['observed_at'],seconds=30);pinned(path,pin)
                record(RUNTIME/('RESPONSE_CHECK_'+uuid.uuid4().hex+'.json'),{'at':c.stamp(),'kind':'upload',
                    'record':self.known_id,'original':acknowledgement,'actual_bucket_ack_validated':True})
                local_context(self.args,self.action);c.fresh(verified['observed_at'],seconds=30)
                return c.strict_json(pinned(path,pin))['response']
            names=set()if kind=='create'else{e['name']for e in self.guard.uploads}
            return self.checked_record(kind,result,self.known_id,kind=='publish',names,captured=captured)[0]
        except BaseException as exc:self.reject(kind,exc)
    def create(self,metadata):return self.mutation('create',metadata)
    def upload(self,bucket,entry):return self.mutation('upload',bucket,entry)
    def update(self,i,metadata):return self.mutation('update',i,metadata)
    def publish(self,i):return self.mutation('publish',i)

def resume_stage(args):
    require_action(args,'stage');verify_merged_payload();local_context(args,'stage')
    need(args.deposit_id is None,'Known-unattempted first stage cannot accept an existing ID')
    _,state=c.zenodo.local_state(pl.MANIFEST.resolve(),'production')
    need(state is None,'Existing original-manifest state: GET-only reconcile, never allocate')
    need(not (RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Already staged')
    record(RUNTIME/'RESUME_STAGE_INTENT.json',{'at':c.stamp(),'head':HEAD,
        'sources_sha256':CONTEXT['sources_sha256'],'clearance_sha256':args.clearance_sha256,
        'original_stage_intent_sha256':F['prior_runtime_files']['ZENODO_STAGE_INTENT.json']['sha256'],
        'manifest':str(pl.MANIFEST.resolve()),'known_unattempted_initial_failure':True,
        'rule':'Exactly one explicit first-create resumption for the preserved old intent; any exception consumes this attempt.'})
    client=pl.GuardedClient(args,'stage',None)
    try:
        result=c.zenodo.run(argparse.Namespace(command='stage',manifest=pl.MANIFEST,sandbox=False,confirm_id=None,check_doi=True),client=client)
        need(result.get('state')=='ready_to_publish' and type(result.get('id')) is int and result['id']>0,'Stage08 outcome unconfirmed')
        _,state=c.zenodo.local_state(pl.MANIFEST.resolve(),'production')
        need(state is not None and state['id']==result['id'] and state['manifest']==str(pl.MANIFEST.resolve())
             and state['environment']=='production','Exact original-manifest state missing')
        record(RUNTIME/'STAGE_SERVICE_OUTCOME.json',result)
        facts=final_facts(args,'stage',result['id'],False)
        certify(args,'stage','RESUME_STAGE_VERIFIED.json',{'at':c.stamp(),'id':result['id'],
            'sources_sha256':CONTEXT['sources_sha256'],
            'original_stage_intent_sha256':F['prior_runtime_files']['ZENODO_STAGE_INTENT.json']['sha256']},facts)
        certify(args,'stage','ZENODO_STAGE_VERIFIED.json',result,facts)
    except BaseException as exc:
        record(RUNTIME/'RESUME_STAGE_FAILURE.json',{'at':c.stamp(),'exception_type':type(exc).__name__,
            'client_target_id':client.identifier,'delegate_known_id':client.delegate.known_id,
            'null_id_does_not_prove_no_attempt':True,'unknown_outcome_requires_GET_only_reconciliation':True,
            'no_mutation_retry_authorized':True})
        raise
    return {k:result.get(k) for k in ['id','state','doi','doi_url','record_url']}

def observe17(identifier,published):
    metadata,uploads=c.zenodo.load_manifest(pl.MANIFEST)
    client=c.zenodo.ZenodoClient('production',c.zenodo.token_for('production'))
    return pl.observe_target(client,identifier,published,metadata,uploads,{v['name'] for v in uploads})
def same_native(first,last):
    NATIVE_POLICY.compare(first,last)
def family(gate,native):
    need(gate['family_ids']==sorted({native['record'],native['concept']}),'Account/native target families disagree; root reconciliation required')
def facts_fresh(facts):
    c.fresh(facts['gate']['at_start'])
    c.fresh(facts['sheet']['observed_at'],seconds=30)
    c.fresh(facts['native']['observed_at'],seconds=30)
    if facts.get('public') is not None:c.fresh(facts['public']['at'])
def gate17(args,action,identifier):
    ad=require_action(args,action)
    g,_,rows=pl.collect('before_'+action,args.expected_pr_head,identifier,cleared=ad,allow_target=action=='ledger')
    local_context(args,action)
    snapshot=c.strict_json((Path(g['private_capture'])/'ledger.json').read_bytes())
    need(SHEET_POLICY.typed_equal(snapshot['values'],rows) and c.digest(rows)==g['ledger_sha256'],'Captured ledger/gate differs')
    return g,snapshot,rows
def final_facts(args,action,identifier,published,prior_native=None,public=None):
    """Long complete account gate FIRST, then new exact native/sheet observations."""
    g,before,rows=gate17(args,action,identifier)
    _,native=observe17(identifier,published);local_context(args,action);family(g,native)
    if prior_native is not None:same_native(prior_native,native)
    sheet,current=c.gws_read();local_context(args,action)
    SHEET_POLICY.preserve(before,sheet,rows)
    need(SHEET_POLICY.typed_equal(rows,current),'Ledger changed after complete gate')
    _,latest=observe17(identifier,published);local_context(args,action)
    same_native(native,latest);family(g,latest);state_exact(identifier)
    facts={'gate':g,'sheet':sheet,'rows':current,'native':latest,'public':public}
    facts_fresh(facts);return facts

def verify_public17(args):
    started=c.stamp();require_action(args,'ledger');identifier=args.deposit_id;state_exact(identifier)
    metadata,uploads=c.zenodo.load_manifest(pl.MANIFEST)
    legacy,first=observe17(identifier,True);local_context(args,'ledger')
    doi='10.5281/zenodo.'+str(identifier);need(legacy.get('doi')==doi,'Unexpected exact DOI')
    raw=PRIVATE/('public17_'+uuid.uuid4().hex);raw.mkdir(mode=0o700)
    data,status,url=pl.fetch('https://zenodo.org/api/records/'+str(identifier),16*1024*1024)
    public=c.strict_json(data);c.durable(raw/'record.json',public);local_context(args,'ledger')
    need(status==200 and type(public.get('id')) is int and public['id']==identifier and public['doi']==doi,'Public record identity mismatch')
    projection=pl.public_projection(public,metadata,first)
    c.durable(raw/'public_projection.json',{'raw_public':public,'compatibility_projection':projection,
        'verified_native_owner':first['owner'],'rule':'Only strictly checked observed owner object becomes the canonical integer owner for immutable05 projector; complete raw object retained.'})
    local_context(args,'ledger')
    c.zenodo.verify(projection,metadata,uploads)
    checked=[]
    for entry in uploads:
        body,code,destination=pl.fetch('https://zenodo.org/records/'+str(identifier)+'/files/'+quote(entry['name'],safe='')+'?download=1',entry['size']+1)
        local_context(args,'ledger')
        need(code==200 and len(body)==entry['size'] and sha(body)==entry['sha256'] and hashlib.md5(body).hexdigest()==entry['md5'],'Published file bytes differ')
        checked.append({'name':entry['name'],'bytes':len(body),'sha256':sha(body),'md5':entry['md5']})
    _,code,destination=pl.fetch('https://doi.org/'+doi,16*1024*1024);local_context(args,'ledger')
    need(code==200 and destination=='https://zenodo.org/records/'+str(identifier),'DOI does not resolve HTTP200 to exact intended record')
    _,latest=observe17(identifier,True);local_context(args,'ledger');same_native(first,latest)
    state_exact(identifier);c.fresh(latest['observed_at'],seconds=30)
    receipt={'at':started,'record':identifier,'doi':doi,'files':checked,'metadata_verified':True,
             'native_target_verified':latest,'doi_status':code,'doi_destination':destination,'private_capture':str(raw)}
    c.durable(raw/'verification.json',receipt)
    local_context(args,'ledger');c.fresh(latest['observed_at'],seconds=30)
    facts=final_facts(args,'ledger',identifier,True,latest,receipt)
    local_context(args,'ledger');facts_fresh(facts)
    return receipt

def publish17(args):
    require_action(args,'publish');identifier=args.deposit_id;state_exact(identifier)
    gate,_,_=gate17(args,'publish',identifier)
    record(RUNTIME/'ZENODO_PUBLISH_INTENT.json',{'at':c.stamp(),'action':'publish','head':HEAD,'id':identifier,
        'manifest':str(pl.MANIFEST.resolve()),'manifest_sha256':sha(pl.MANIFEST.read_bytes()),
        'sources_sha256':CONTEXT['sources_sha256'],'gate':gate['private_capture'],
        'rule':'Exactly one attempt. Preserve known ID and intent; ambiguous outcome requires GET-only reconciliation, never retry.'})
    local_context(args,'publish')
    client=pl.GuardedClient(args,'publish',identifier)
    try:
        result=c.zenodo.run(argparse.Namespace(command='publish',manifest=pl.MANIFEST,sandbox=False,confirm_id=identifier,check_doi=True),client=client)
        need(result.get('state')=='published' and type(result.get('id')) is int and result['id']==identifier,'Publication08 outcome unconfirmed')
        record(RUNTIME/'PUBLISH_SERVICE_OUTCOME.json',result)
        facts=final_facts(args,'publish',identifier,True)
        certify(args,'publish','ZENODO_PUBLISH_VERIFIED.json',result,facts)
    except BaseException as exc:
        record(RUNTIME/'PUBLISH_FAILURE.json',{'at':c.stamp(),'exception_type':type(exc).__name__,
            'id':identifier,'no_mutation_retry_authorized':True,'GET_only_reconciliation_required':True})
        raise
    return {k:result.get(k) for k in ['id','state','doi','doi_url','record_url','doi_resolution']}

def ledger17(args):
    require_action(args,'ledger');identifier=args.deposit_id;state_exact(identifier)
    public=verify_public17(args)
    facts=final_facts(args,'ledger',identifier,True,public['native_target_verified'],public)
    before=facts['rows'];sheet=facts['sheet'];row=pl.draft_row(identifier)
    families={facts['native']['record'],facts['native']['concept']}
    existing=[(i,r) for i,r in enumerate(before,1) if families&pl.row_ids(r)]
    need(len(existing)<=1 and (not existing or SHEET_POLICY.typed_equal(existing[0][1],row)),'Target row differs or duplicates')
    intent=RUNTIME/'LEDGER_APPEND_INTENT.json'
    if existing:
        if intent.exists():
            prior=c.strict_json(intent.read_bytes())
            need(prior['head']==HEAD and type(prior['record']) is int and prior['record']==identifier
                 and prior['sources_sha256']==CONTEXT['sources_sha256'] and prior['manifest']==str(pl.MANIFEST.resolve())
                 and prior['spreadsheet_id']==c.SHEET and type(prior['sheet_id']) is int and prior['sheet_id']==c.SHEET_ID
                 and prior['sheet_title']==c.SHEET_TITLE and prior['operation']=='spreadsheets.batchUpdate.appendCells'
                 and SHEET_POLICY.typed_equal(prior['values'],row),'Prior append intent target differs')
            original=prior['before_snapshot']
            need(c.digest(original['values'])==prior['before_sha256'] and len(original['values'])==prior['before_rows'],'Prior captured rows differ')
            SHEET_POLICY.preserve(original,sheet,original['values']+[row])
        new=False;position=existing[0][0]
    else:
        need(not intent.exists(),'Prior append intent without exact visible row; GET-only reconcile, no retry')
        need(len(before)<sheet['identity']['row_count'],'No allocated row capacity; no metadata-resizing side effect allowed')
        request={'requests':[{'appendCells':{'sheetId':c.SHEET_ID,'rows':[{'values':[{'userEnteredValue':{'stringValue':cell}} for cell in row]}],'fields':'userEnteredValue'}}],'includeSpreadsheetInResponse':True,'responseIncludeGridData':False}
        record(intent,{'at':c.stamp(),'head':HEAD,'record':identifier,'sources_sha256':CONTEXT['sources_sha256'],
            'manifest':str(pl.MANIFEST.resolve()),'spreadsheet_id':c.SHEET,'sheet_id':c.SHEET_ID,'sheet_title':c.SHEET_TITLE,
            'operation':'spreadsheets.batchUpdate.appendCells','columns':'A:D','values':row,'request':request,
            'before_sha256':c.digest(before),'before_rows':len(before),'before_snapshot':sheet,
            'gate':facts['gate']['private_capture'],'rule':'One append attempt only. Lost response: GET-only exact reconciliation; never append again.'})
        # This is the ACTUAL GWS write adapter. No inherited append bypasses it.
        # A stale durable intention cannot be made fresh by silently refreshing it.
        local_context(args,'ledger');facts_fresh(facts);require_action(args,'ledger');facts_fresh(facts)
        edge_sheet,edge_rows=c.gws_read();local_context(args,'ledger');facts_fresh(facts)
        SHEET_POLICY.preserve(sheet,edge_sheet,before)
        need(SHEET_POLICY.typed_equal(before,edge_rows),'Ledger changed after append intent')
        _,edge_native=observe17(identifier,True);local_context(args,'ledger')
        same_native(facts['native'],edge_native);family(facts['gate'],edge_native)
        edge_facts={**facts,'sheet':edge_sheet,'native':edge_native}
        state_exact(identifier);runtime_exact();facts_fresh(edge_facts)
        result=c.command(['gws','sheets','spreadsheets','batchUpdate','--params',json.dumps({'spreadsheetId':c.SHEET}),'--json',json.dumps(request,ensure_ascii=False)])
        record(RUNTIME/'LEDGER_APPEND_RESPONSE.json',result)
        local_context(args,'ledger');SHEET_POLICY.append_response(result,sheet)
        record(RUNTIME/'LEDGER_APPEND_ACKNOWLEDGED.json',{'at':c.stamp(),'record':identifier,
            'spreadsheet_id':c.SHEET,'sheet_id':c.SHEET_ID,'operation':'spreadsheets.batchUpdate.appendCells',
            'request_sha256':c.digest(request),'response_sha256':c.digest(result),
            'rule':'Server acknowledged exactly one append request. Position/postcondition still unverified; preserve both writers and reconcile by GET only, never retry.'})
        after,rows=c.gws_read();local_context(args,'ledger')
        SHEET_POLICY.preserve(sheet,after,before+[row])
        need(SHEET_POLICY.typed_equal(rows,before+[row]),'Append changed unrelated rows or exact appended values')
        new=True;position=len(rows)
    # All long postwrite/public/account/metadata reads precede final authority.
    final=final_facts(args,'ledger',identifier,True,facts['native'],public)
    SHEET_POLICY.preserve(sheet,final['sheet'],before+[row] if new else before)
    found=[(i,r) for i,r in enumerate(final['rows'],1) if families&pl.row_ids(r)]
    need(len(found)==1 and found[0][0]==position and SHEET_POLICY.typed_equal(found[0][1],row),'Final unique literal target row differs')
    value={'at':c.stamp(),'record':identifier,'spreadsheet_id':c.SHEET,'sheet_id':c.SHEET_ID,'sheet_title':c.SHEET_TITLE,
        'row':position,'values':row,'new_row':new,'read_back_exact':True,'unique_target_family':True,
        'all_other_rows_and_full_raw_metadata_preserved':True,'gate':final['gate']['private_capture']}
    certify(args,'ledger','LEDGER_VERIFIED.json',value,final)
    return {'record':identifier,'spreadsheet_id':c.SHEET,'sheet_id':c.SHEET_ID,'sheet_title':c.SHEET_TITLE,'row':position,'new_row':new,'verified':True}

def install():
    global c,pl,live,ir
    c=LOAD05('ops_common');pl=LOAD05('publish_and_ledger');live=LOAD05('collect_live');ir=LOAD05('integrate_remote')
    for m in [c,pl,live,ir,LOAD05('native_policy')]:
        m.RUNTIME=RUNTIME;m.PRIVATE=PRIVATE
    prior_durable=c.durable
    def durable_with_original_ascii(path,value):
        """Same exclusive/fsynced receipt contract; only originals use ASCII.

        Keep immutable05 bytes and every other writer/representation unchanged.
        The first original/fact payload uses the exact encoding capture pins.
        """
        if path.parent!=PRIVATE or not(path.name.startswith('service_original_')and path.suffix=='.json'):
            return prior_durable(path,value)
        need(path.parent in {c.RUNTIME,c.PRIVATE}or c.PRIVATE in path.parents,'Receipt outside assigned private/runtime directory')
        need(not any(p.is_symlink()for p in [c.OPS,c.RUNTIME,PRIVATE,path.parent]),'Receipt symlink rejected')
        path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        body=(json.dumps(value,sort_keys=True,ensure_ascii=True,indent=2)+'\n').encode('ascii')
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'wb')as stream:
            stream.write(body);stream.flush();os.fsync(stream.fileno())
        fd=os.open(path.parent,os.O_RDONLY)
        try:os.fsync(fd)
        finally:os.close(fd)
    c.durable=durable_with_original_ascii
    live.semantic=lambda text:PR_POLICY.semantic(text,live.decoded)
    SHEET_POLICY.C=c
    c.gws_read=live.gws_read=pl.gws_read=SHEET_POLICY.read
    NATIVE_POLICY.install(c,pl,LOAD05('native_policy'),SHEET_POLICY.typed_equal)
    original_guard=pl.GuardedClient
    class Guard17(original_guard):
        def __init__(self,args,action,identifier,delegate=None):
            actual=delegate if delegate is not None else c.zenodo.ZenodoClient('production',c.zenodo.token_for('production'))
            edge=EdgeDelegate(actual,args,action)
            super().__init__(args,action,identifier,edge)
            edge.guard=self;self.edge_gate=None;self.edge_used=True;self.pending_transition=None
        def protected(self,kind,fn,*args):
            try:
                self.delegate.usable()
                return fn(*args)
            except ConsumedResponseError:raise
            except BaseException as exc:self.delegate.reject(kind+'_guard_context',exc)
        def get(self,*args):return self.protected('get',super().get,*args)
        def create(self,*args):return self.protected('create',super().create,*args)
        def upload(self,*args):return self.protected('upload',super().upload,*args)
        def update(self,*args):return self.protected('update',super().update,*args)
        def publish(self,*args):return self.protected('publish',super().publish,*args)
        def accept(self,snapshot,added=None):
            if self.snapshot is not None:
                NATIVE_POLICY.compare(self.snapshot,snapshot,transition=self.pending_transition,added=added)
            self.snapshot=snapshot;self.pending_transition=None
        def before(self,identifier,required_names=None):
            # Same immutable05 ordering and exact family equality; retain its
            # actual gate timestamp for another freshness check at the edge.
            need(identifier==self.identifier,'Lifecycle ID changed')
            ad=require_action(self.args,self.action)
            gate,_,_=pl.collect('before_'+self.action,self.args.expected_pr_head,identifier,cleared=ad)
            require_action(self.args,self.action)
            snapshot=None
            if identifier is not None:
                _,snapshot=self.observation(False,required_names)
                need(gate['family_ids']==sorted({snapshot['record'],snapshot['concept']}),'Account/native target families disagree; root reconciliation required')
            self.edge_gate=gate;self.edge_used=False
            local_context(self.args,self.action)
            if snapshot is not None:c.fresh(snapshot['observed_at'],seconds=30)
            c.fresh(gate['at_start'])
            return snapshot
    pl.GuardedClient=Guard17;pl.require_action=require_action
    c.zenodo.save_state=guarded_save_state

def main(arguments=None):
    global ACTION_ARGS,ACTION
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['resume-stage','publish','verify-public','ledger'])
    p.add_argument('--expected-pr-head',required=True);p.add_argument('--deposit-id',type=int)
    p.add_argument('--clearance-sha256',required=True)
    a=p.parse_args(arguments);a.operations_sha256=CONTEXT['sources_sha256'];bind_runtime()
    ACTION_ARGS=a;ACTION='stage' if a.action=='resume-stage' else 'ledger' if a.action in {'ledger','verify-public'} else 'publish'
    bind_state()
    if a.action=='resume-stage':result=resume_stage(a)
    else:
        require_action(a,'ledger' if a.action in {'verify-public','ledger'} else 'publish')
        verify_merged_payload()
        result=verify_public17(a) if a.action=='verify-public' else ledger17(a) if a.action=='ledger' else publish17(a)
    local_context(a,'stage' if a.action=='resume-stage' else 'ledger' if a.action in {'ledger','verify-public'} else 'publish')
    print(json.dumps(result,indent=2));return result
