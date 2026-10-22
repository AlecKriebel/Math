"""Minimal06 overlay: known-unattempted original stage, then existing-ID publish/ledger.
No integration, alternate manifest, approval authoring or automatic write retry.
"""
if not globals().get('_OPS06_VERIFIED',False):raise RuntimeError('Use verified06 bootstrap')
from pathlib import Path
import argparse,hashlib,json,re

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
def pinned(path,pin):
    need(not path.is_symlink() and not path.parent.is_symlink(),'Context symlink')
    b=path.read_bytes();need({'bytes':len(b),'sha256':sha(b)}==pin,'Preserved context changed: '+path.name)
    return b

def local_context(args,action):
    """Pure local adoption/context check, repeated AFTER every long live guard."""
    need(args.operations_sha256==CONTEXT['sources_sha256'],'External06 source anchor mismatch')
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
    stage=old['ZENODO_STAGE_INTENT.json'];recon=old['ROOT_STAGE_FAILURE_READONLY_RECONCILIATION.json']
    oldsha=F['prior_runtime_files']['ZENODO_STAGE_INTENT.json']['sha256']
    need(stage['action']=='stage' and stage['head']==HEAD and stage['id'] is None
         and stage['manifest']==str(pl.MANIFEST.resolve())
         and stage['manifest_sha256']==sha(pl.MANIFEST.read_bytes()),'Original stage intent target changed')
    need(recon['original_intent_sha256']==oldsha and recon['original_intent_preserved'] is True
         and recon['state_absent'] is True and recon['no_service_mutation'] is True
         and recon['no_retry_performed'] is True,'Known-unattempted reconciliation changed')
    need(re.fullmatch('[a-f0-9]{64}',args.clearance_sha256 or ''),'External06 root clearance hash required')
    path=RUNTIME/'ROOT_OPERATIONAL_CLEARANCE06.json'
    need(not path.is_symlink() and not RUNTIME.is_symlink(),'Root06 clearance symlink')
    raw=path.read_bytes();need(sha(raw)==args.clearance_sha256,'Root06 adoption revoked/changed')
    ad=c.strict_json(raw)
    need(ad['pr']==1131 and ad['head']==HEAD and ad['merge_commit']==MERGE
         and ad['operations06_sources_sha256']==CONTEXT['sources_sha256']
         and ad['bootstrap06_sha256']==CONTEXT['bootstrap_sha256']
         and ad['source_freeze_sha256']==sha((CONTEXT['source_root']/'SOURCE_FREEZE.json').read_bytes())
         and ad['prior_operations_manifest_sha256']==F['prior_operations_manifest_sha256']
         and ad['scientific_clearance_sha256']==F['scientific_clearance_sha256']
         and ad['original_stage_intent_sha256']==oldsha
         and ad['readonly_reconciliation_sha256']==F['prior_runtime_files']['ROOT_STAGE_FAILURE_READONLY_RECONCILIATION.json']['sha256']
         and ad['prior_merge_receipt_sha256']==F['prior_runtime_files']['MERGE_VERIFIED.json']['sha256'],
         'Root06 approval source/old context mismatch')
    need(ad['publication_ready'] is True and ad['whole06_review_adopted'] is True
         and ad['unresolved_findings']==[] and ad['root_confirmed_failure_before_delegate_create'] is True
         and ad['initial_create_attempt_was_sent'] is False,'Root06 known-unattempted authority incomplete')
    permitted={'resume-stage','publish','ledger'}
    need(isinstance(ad['allowed_actions'],list) and set(ad['allowed_actions'])<=permitted
         and len(ad['allowed_actions'])==len(set(ad['allowed_actions'])),'Unknown/duplicate06 action')
    mapped='resume-stage' if action=='stage' else action
    need(mapped in ad['allowed_actions'],'Action06 not cleared')
    need(ad['spreadsheet_id']==c.SHEET and type(ad['sheet_id']) is int and ad['sheet_id']==c.SHEET_ID
         and ad['sheet_title']==c.SHEET_TITLE and ad['account_identity_contract']==c.ACCOUNT_IDENTITY_CONTRACT,'Root06 ledger/account binding changed')
    need(not (RUNTIME/'RESUME_STAGE_FAILURE.json').exists(),'Prior06 stage failure: GET-only reconcile; no retry')
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
             'Exact06 staged ID/receipt missing')
    local_context(args,action)
    return ad

def verify_merged_payload():
    """GET-only check of the accepted immutable merge's selected frozen subtree."""
    pkg=c.package();_,changes=c.proposal()
    expected={n:pkg['source']['original/'+n] for n in c.ORIGINALS}
    expected.update({p[len(c.PROBLEM)+1:]:b for p,b in changes.items()})
    got=ir.leaves(MERGE,c.PROBLEM)
    need(got=={n:('100644','blob',ir.blob_sha(b)) for n,b in expected.items()},'Accepted merged scientific/kit payload changed')

class EdgeDelegate:
    """A local check and durable one-write intent directly at each delegate edge."""
    def __init__(self,delegate,args,action):
        self.delegate,self.args,self.action=delegate,args,action;self.known_id=args.deposit_id
    @property
    def base(self):return self.delegate.base
    def get(self,i):return self.delegate.get(i)
    def native_get(self,*a,**k):return self.delegate.native_get(*a,**k)
    def request(self,method,url):
        need(method=='GET','Unexpected direct native mutation');return self.delegate.request(method,url)
    def mutation(self,kind,*args):
        need(self.guard.edge_gate is not None and not self.guard.edge_used,'No fresh unused native/account guard for delegated write')
        self.guard.edge_used=True
        local_context(self.args,self.action)
        key=kind
        if kind=='upload':key+='_'+sha(args[1]['name'].encode())
        c.durable(RUNTIME/('WRITE_'+self.action+'_'+key+'_INTENT.json'),{
            'at':c.stamp(),'action':self.action,'kind':kind,'known_id':self.known_id,
            'sources_sha256':CONTEXT['sources_sha256'],'clearance_sha256':self.args.clearance_sha256,
            'original_stage_intent_sha256':F['prior_runtime_files']['ZENODO_STAGE_INTENT.json']['sha256'],
            'rule':'One delegated attempt only. Any ambiguous outcome consumes this intent; GET-only reconcile, never retry.'})
        local_context(self.args,self.action)
        c.fresh(self.guard.edge_gate['at_start'])
        if self.guard.snapshot is not None:c.fresh(self.guard.snapshot['observed_at'],seconds=30)
        result=getattr(self.delegate,kind)(*args)
        if kind=='create' and isinstance(result,dict) and type(result.get('id')) is int and result['id']>0:
            self.known_id=result['id']
        local_context(self.args,self.action)
        return result
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
    c.durable(RUNTIME/'RESUME_STAGE_INTENT.json',{'at':c.stamp(),'head':HEAD,
        'sources_sha256':CONTEXT['sources_sha256'],'clearance_sha256':args.clearance_sha256,
        'original_stage_intent_sha256':F['prior_runtime_files']['ZENODO_STAGE_INTENT.json']['sha256'],
        'manifest':str(pl.MANIFEST.resolve()),'known_unattempted_initial_failure':True,
        'rule':'Exactly one explicit first-create resumption for the preserved old intent; any exception consumes this attempt.'})
    client=pl.GuardedClient(args,'stage',None)
    try:
        result=c.zenodo.run(argparse.Namespace(command='stage',manifest=pl.MANIFEST,sandbox=False,confirm_id=None,check_doi=True),client=client)
        need(result.get('state')=='ready_to_publish' and type(result.get('id')) is int and result['id']>0,'Stage06 outcome unconfirmed')
        _,state=c.zenodo.local_state(pl.MANIFEST.resolve(),'production')
        need(state is not None and state['id']==result['id'] and state['manifest']==str(pl.MANIFEST.resolve())
             and state['environment']=='production','Exact original-manifest state missing')
        require_action(args,'stage');local_context(args,'stage')
        c.fresh(client.snapshot['observed_at'],seconds=30)
        c.durable(RUNTIME/'RESUME_STAGE_VERIFIED.json',{'at':c.stamp(),'id':result['id'],
            'sources_sha256':CONTEXT['sources_sha256'],
            'original_stage_intent_sha256':F['prior_runtime_files']['ZENODO_STAGE_INTENT.json']['sha256']})
        local_context(args,'stage')
        c.durable(RUNTIME/'ZENODO_STAGE_VERIFIED.json',result)
    except BaseException as exc:
        c.durable(RUNTIME/'RESUME_STAGE_FAILURE.json',{'at':c.stamp(),'exception_type':type(exc).__name__,
            'client_target_id':client.identifier,'delegate_known_id':client.delegate.known_id,
            'null_id_does_not_prove_no_attempt':True,'unknown_outcome_requires_GET_only_reconciliation':True,
            'no_mutation_retry_authorized':True})
        raise
    return {k:result.get(k) for k in ['id','state','doi','doi_url','record_url']}

def install():
    global c,pl,live,ir
    c=LOAD05('ops_common');pl=LOAD05('publish_and_ledger');live=LOAD05('collect_live');ir=LOAD05('integrate_remote')
    for m in [c,pl,live,ir,LOAD05('native_policy')]:
        m.RUNTIME=RUNTIME;m.PRIVATE=PRIVATE
    live.semantic=lambda text:PR_POLICY.semantic(text,live.decoded)
    original_guard=pl.GuardedClient
    class Guard06(original_guard):
        def __init__(self,args,action,identifier,delegate=None):
            actual=delegate if delegate is not None else c.zenodo.ZenodoClient('production',c.zenodo.token_for('production'))
            edge=EdgeDelegate(actual,args,action)
            super().__init__(args,action,identifier,edge)
            edge.guard=self;self.edge_gate=None;self.edge_used=True
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
    pl.GuardedClient=Guard06;pl.require_action=require_action

def main(arguments=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['resume-stage','publish','verify-public','ledger'])
    p.add_argument('--expected-pr-head',required=True);p.add_argument('--deposit-id',type=int)
    p.add_argument('--clearance-sha256',required=True)
    a=p.parse_args(arguments);a.operations_sha256=CONTEXT['sources_sha256']
    if a.action=='resume-stage':result=resume_stage(a)
    else:
        require_action(a,'ledger' if a.action in {'verify-public','ledger'} else 'publish')
        verify_merged_payload()
        result=pl.verify_public(a) if a.action=='verify-public' else pl.append_ledger(a) if a.action=='ledger' else pl.lifecycle(a)
    print(json.dumps(result,indent=2));return result
