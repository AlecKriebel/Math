"""One root-adopted first stage attempt after a proven pre-create read failure.
No retry, source edit, alternate deposition, or existing-intent deletion.
"""
from pathlib import Path
import argparse,hashlib,json,sys
OPS=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455/operations')
BOOT='960b33e83135968ab40ef069b1b8876df47b70d1c4ef528bf0d8c836213ac58b'
OPSHA='eab69e53e9d32510bbf00d74c1b94b70542a8b29cf326c42f5d974e510f09d00'
CLEAR='866ffab146f1e649cbbbb8ccc1a499813b7c8e887ffe6db844d04bea52859f8d'
HEAD='9601e1e768c94522bc8ad105db4dfae4770bad75'
REVIEW='7db321ecc269474d73eefe6d25eff68566db8f31bd46642102b163596c52b6eb'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(b):
    def pairs(xs):
        d={}
        for k,v in xs:
            need(k not in d,'duplicate JSON key');d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs)
def resume(args,load):
    common=load('ops_common');pl=load('publish_and_ledger')
    src=Path(__file__).read_bytes();need(sha(src)==args.source_sha256,'resumption source drift')
    old=OPS/'runtime/ZENODO_STAGE_INTENT.json';oldbytes=old.read_bytes();oldj=strict(oldbytes)
    adoptionpath=OPS/'runtime/ROOT_KNOWN_UNATTEMPTED_STAGE_RESUMPTION_ADOPTION.json'
    adoptionbytes=adoptionpath.read_bytes();need(sha(adoptionbytes)==args.adoption_sha256,'root resumption adoption drift')
    ad=strict(adoptionbytes)
    need(ad['wrapper_sha256']==sha(src) and ad['original_stage_intent_sha256']==sha(oldbytes),'adoption/source/old-intent mismatch')
    need(ad['operations_manifest_sha256']==OPSHA and ad['whole_operations_review_sha256']==REVIEW,'reviewed source/dependency mismatch')
    need(ad['pr']==1131 and ad['head']==HEAD and ad['allowed_action']=='FIRST_CREATE_FOR_ORIGINAL_STAGE_INTENT_ONLY','wrong target/action adoption')
    need(ad['root_confirmed_failure_before_delegate_create'] is True and ad['initial_create_attempt_was_sent'] is False and ad['unresolved_findings']==[],'known-unattempted stage not established')
    reconciliation=OPS/'runtime/ROOT_STAGE_FAILURE_READONLY_RECONCILIATION.json'
    need(sha(reconciliation.read_bytes())==ad['readonly_reconciliation_sha256'],'reconciliation changed')
    recon=strict(reconciliation.read_bytes())
    need(recon['original_intent_sha256']==sha(oldbytes) and recon['original_intent_preserved'] is True and recon['state_absent'] is True and recon['no_service_mutation'] is True and recon['no_retry_performed'] is True,'reconciliation not accepted no-attempt case')
    need(oldj['action']=='stage' and oldj['head']==HEAD and oldj['id'] is None and oldj['manifest']==str(pl.MANIFEST) and oldj['manifest_sha256']==sha(pl.MANIFEST.read_bytes()),'original intent target drift')
    need(not (OPS/'runtime/ZENODO_STAGE_VERIFIED.json').exists(),'stage already verified')
    need(not (OPS/'runtime/ROOT_STAGE_RESUMPTION_INTENT.json').exists(),'resumption already entered; GET-only reconcile')
    a=argparse.Namespace(action='stage',expected_pr_head=HEAD,deposit_id=None,clearance_sha256=CLEAR,operations_sha256=OPSHA)
    pl.require_action(a,'stage')
    _,state=common.zenodo.local_state(pl.MANIFEST.resolve(),'production')
    need(state is None,'existing target state; GET-only reconcile, never allocate')
    common.durable(OPS/'runtime/ROOT_STAGE_RESUMPTION_INTENT.json',{'at':common.stamp(),'pr':1131,'head':HEAD,'root_adoption_sha256':args.adoption_sha256,'wrapper_sha256':sha(src),'old_stage_intent_sha256':sha(oldbytes),'old_intent_preserved':True,'rule':'Exactly one entry. Unchanged GuardedClient performs full live account/ledger/PR/native gate immediately before every delegated write. Any exception preserves this intent; never retry.'})
    client=pl.GuardedClient(a,'stage',None)
    try:
        result=common.zenodo.run(argparse.Namespace(command='stage',manifest=pl.MANIFEST,sandbox=False,confirm_id=None,check_doi=True),client=client)
        need(result.get('state')=='ready_to_publish' and type(result.get('id')) is int and result['id']>0,'stage outcome not confirmed')
        common.durable(OPS/'runtime/ZENODO_STAGE_VERIFIED.json',result)
    except BaseException as exc:
        # An ID here is custody evidence, never proof that an absent ID means no POST.
        common.durable(OPS/'runtime/ROOT_STAGE_RESUMPTION_FAILURE.json',{'at':common.stamp(),'exception_type':type(exc).__name__,'client_target_id':client.identifier,'unknown_outcome_requires_GET_only_reconciliation':True,'no_mutation_retry_authorized':True})
        raise
    need(old.read_bytes()==oldbytes,'old stage intent altered')
    common.durable(OPS/'runtime/ROOT_STAGE_RESUMPTION_VERIFIED.json',{'at':common.stamp(),'id':result['id'],'state':result['state'],'old_intent_preserved':True,'stage_receipt':'ZENODO_STAGE_VERIFIED.json'})
    return {k:result.get(k) for k in ['id','state','doi','doi_url','record_url']}
def main():
    p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--source-sha256',required=True);p.add_argument('--adoption-sha256',required=True);a=p.parse_args()
    need(a.execute,'explicit root-adopted execution flag required')
    need(sys.flags.isolated and sys.flags.no_site,'isolated standard-library runtime required')
    need(sha(Path(__file__).read_bytes())==a.source_sha256,'externally pinned wrapper mismatch')
    boot=OPS/'bootstrap.py';b=boot.read_bytes();need(sha(b)==BOOT,'bootstrap changed')
    ns={'__file__':str(boot),'__name__':'source_verified_bootstrap'};exec(compile(b,str(boot),'exec'),ns)
    load,_=ns['load_verified'](OPS,OPSHA,BOOT)
    print(json.dumps(resume(a,load),indent=2))
if __name__=='__main__':main()
