"""Resume only existing Zenodo23409904 with exact reviewed notes HTML storage.

No create/upload/update path exists. The original repository kit and all six
helpers remain unchanged. A NEW complete postmerge review and updated canonical
approval must explicitly authenticate this additional operator before use.
"""
import sys
if not sys.flags.isolated or not sys.flags.no_site or sys.flags.optimize or not sys.dont_write_bytecode:
    raise RuntimeError('Use Python -I -S -B at optimization zero')
import argparse, copy, hashlib, json
from pathlib import Path

ROOT=Path('/Users/alec/Documents/Math')
P=ROOT/'draft_pr_claimed_solved_900_1000_20261012'
A=P/'audits/pr946_6000001'
D=A/'preprint'
IDENT=23409904
OPS='f4742eca6ddd628ecac1e704fed772a17837d42d4d0fdef42c73d3cda3bed254'
CORE='8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7'
FREEZE='9af8f2570af53b6a6658a7998ac08927829c8747be7c764a8d2c392dc6c6afe1'
ISSUE='PUB946-METADATA-001'

def need(test, reason):
    if not test:
        raise RuntimeError('PR946 exact-ID reconciliation: '+reason)

def normalize_notes(deposit, expected_notes):
    """Accept equality or only the one observed escaped comparison symbol."""
    need(type(deposit) is dict and type(deposit.get('metadata')) is dict,
         'remote metadata object')
    need(type(expected_notes) is str,'expected notes type')
    actual=deposit['metadata'].get('notes')
    need(type(actual) is str,'remote notes type')
    result=copy.deepcopy(deposit)
    changed=False
    if actual != expected_notes:
        need(expected_notes.count('Python>=3.11')==1
             and actual==expected_notes.replace('Python>=3.11','Python&gt;=3.11'),
             'notes differ beyond the exact observed Python comparison escape')
        result['metadata']['notes']=expected_notes
        changed=True
    return result,changed

class ExistingDraftClient:
    """Only exact-ID GET and at most one explicitly authorized publish POST."""
    def __init__(self, client, kit, metadata, files, guard, allow_publish):
        self.client,self.kit,self.metadata,self.files=client,kit,metadata,files
        self.guard,self.allow_publish=guard,allow_publish
        self.posts=0
        self.observations=[]

    def get(self, ident):
        need(type(ident) is int and ident==IDENT,'exact existing ID')
        raw=self.client.get(ident)
        self.kit['validate_record'](raw,IDENT)
        logical,changed=normalize_notes(raw,self.metadata['notes'])
        # The unchanged kit still checks every metadata field and exact
        # file-name set, API size and MD5. No broad HTML decoding occurs.
        self.kit['verify'](logical,self.metadata,self.files)
        self.observations.append({'notes_exact_observed_HTML_escape':changed,
            'raw_notes_sha256':hashlib.sha256(raw['metadata']['notes'].encode()).hexdigest(),
            'submitted':raw['submitted']})
        return logical

    def publish(self, ident):
        need(type(ident) is int and ident==IDENT and self.allow_publish and self.posts==0,
             'one authorized exact-ID publication only')
        self.guard()
        fresh=self.get(ident)
        # Close the intervening external read before either publication or
        # an already-published return. No service call follows this closure.
        self.guard()
        if fresh['submitted']:
            return fresh
        self.posts+=1
        return self.client.publish(ident)

def run(args):
    raw=(P/'accept_pr946.py').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==CORE,'captured core pin')
    N={'__name__':'_reviewed_reconciliation_core_','__file__':str(P/'accept_pr946.py')}
    exec(compile(raw,N['__file__'],'exec',dont_inherit=True,optimize=0),N)
    context=N['capture_inventory'](OPS)
    own=N['read_regular'](Path(__file__))
    need(hashlib.sha256(own).hexdigest()==args.operator_sha256,'external operator pin')
    accepted,freeze=N['accepted_package'](context)
    need(accepted['freeze_sha256']==FREEZE,'unchanged scientific candidate')
    latest=accepted['full_package_reviews'][-1]
    need(latest['round']>=7 and latest['manifest_sha256']==args.review_sha256,
         'NEW complete postmerge review required')
    folder=A/'reviews'/('full_package_%02d'%latest['round'])
    manifest_raw=N['read_regular'](folder/'MANIFEST.json')
    need(N['sha'](manifest_raw)==args.review_sha256,'external complete review seal')
    manifest=N['strict_json'](manifest_raw)
    result=N['strict_json'](N['read_regular'](folder/'RESULT.json',pin=manifest['files']['RESULT.json']))
    need(N['exact'](result.get('inspected_publication_operator'),N['fingerprint'](own))
         and result['prior_issue_resolution'].get(ISSUE,{}).get('verified') is True,
         'complete reviewer must authenticate this operator and exact issue')
    destination=N['merged_gate'](accepted,freeze)
    descriptor,expected=N['descriptor_check'](freeze)
    runtime=N['runtime_upload_copy'](freeze)
    kit={'__name__':'_captured_original_zenodo_kit_','__file__':str(ROOT/N['KIT'])}
    exec(compile(context['captured'][N['KIT']],kit['__file__'],'exec',dont_inherit=True,optimize=0),kit)
    metadata,files=kit['load_manifest'](runtime)
    need(N['exact'](metadata,descriptor['metadata']),'unchanged reviewed metadata')
    place,state=kit['local_state'](runtime.resolve(),'production')
    need(state is not None and type(state['id']) is int and state['id']==IDENT,
         'preserved exact existing draft state')
    action='stage' if args.action=='inspect-stage' else args.action
    intent={'utc':N['utc_now'](),'action':action,'pr':946,'original_pr_head':N['HEAD'],
        'accepted_freeze_sha256':FREEZE,'operations_inventory_sha256':OPS,
        'descriptor_sha256':freeze['files']['zenodo-deposit.json']['sha256'],
        'repository_kit_sha256':context['inventory']['files'][N['KIT']]['sha256'],
        'runtime_manifest':str(runtime.relative_to(ROOT)),
        'merged_commit':destination['merge_commit'],'merged_base':'main',
        'destination_readback':destination,'blind_retry_permitted':False,
        'reviewed_operator_sha256':args.operator_sha256,'operator_review_manifest_sha256':args.review_sha256,
        'exact_existing_record_id':IDENT,'reconciliation_issue':ISSUE}
    if args.action=='publish':
        staged=N['load'](D/'ZENODO_STAGE.json')
        need(staged.get('id')==IDENT and staged.get('state')=='ready_to_publish'
             and N['exact'](staged.get('files'),expected),'exact verified existing stage')
        need(not(D/'ZENODO_PUBLISH_INTENT.json').exists(),'prior publish intent: inspect first')
        N['save'](D/'ZENODO_PUBLISH_INTENT.json',intent,exclusive=True)
    elif args.action=='inspect':
        N['save'](D/'ZENODO_INSPECT_INTENT.json',intent)
    def guard():
        N['accepted_review_check'](accepted,freeze,context)
        N['merged_gate'](accepted,freeze)
        N['accepted_review_check'](accepted,freeze,context)
        # This additional executable is deliberately outside the unchanged
        # seven-source inventory. Refresh its exact external/reviewer identity
        # after the full service and sealed-review closure on every boundary.
        current=N['read_regular'](Path(__file__),pin=N['fingerprint'](own))
        need(N['exact'](result.get('inspected_publication_operator'),N['fingerprint'](current))
             and latest['manifest_sha256']==args.review_sha256,
             'current operator differs from externally sealed inspected identity')
    guard()
    actual=kit['ZenodoClient']('production',kit['token_for']('production'))
    client=ExistingDraftClient(actual,kit,metadata,files,guard,args.action=='publish')
    command='publish' if args.action=='publish' else 'inspect'
    try:
        receipt=kit['run'](argparse.Namespace(command=command,manifest=runtime,sandbox=False,
            confirm_id=IDENT,check_doi=args.action!='inspect-stage'),client=client)
    except Exception as error:
        N['save'](A/('PUBLICATION_RECONCILIATION_'+args.action.upper()+'_FAILURE.json'),
            {**intent,'error':str(error),'publish_POST_count':client.posts,'instruction':'Inspect exact existing state; no blind writing retry.'})
        raise
    need(receipt.get('id')==IDENT and receipt.get('environment')=='production'
         and receipt.get('title')==metadata['title'] and N['exact'](receipt.get('files'),expected),
         'actual unchanged kit result linkage')
    if args.action=='inspect-stage':
        need(receipt.get('state')=='ready_to_publish','unpublished reconciled stage')
    else:
        need(receipt.get('state')=='published' and receipt.get('doi')=='10.5281/zenodo.23409904'
             and receipt.get('record_url')=='https://zenodo.org/records/23409904','actual public exact-ID result')
    receipt['metadata_normalizations'].append({'field':'notes',
        'kind':'only_observed_Python_comparison_gt_HTML_storage','observations':client.observations})
    receipt.update(reviewed_operator_sha256=args.operator_sha256,
        operator_review_manifest_sha256=args.review_sha256,reconciliation_issue=ISSUE,
        publish_POST_count=client.posts,no_create_upload_update_path=True)
    guard()
    N['save'](D/('ZENODO_'+action.upper()+'.json'),receipt,exclusive=args.action in ('inspect-stage','publish'))
    N['save'](A/('PUBLICATION_RECONCILIATION_'+args.action.upper()+'_RECEIPT.json'),
        {**intent,'actual_kit_receipt':receipt,'new_deposits_created':0})
    print(json.dumps({'action':args.action,'id':IDENT,'state':receipt['state'],
        'doi':receipt.get('doi'),'publish_POST_count':client.posts}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['inspect-stage','publish','inspect'])
    parser.add_argument('--operator-sha256',required=True)
    parser.add_argument('--review-sha256',required=True)
    run(parser.parse_args())
