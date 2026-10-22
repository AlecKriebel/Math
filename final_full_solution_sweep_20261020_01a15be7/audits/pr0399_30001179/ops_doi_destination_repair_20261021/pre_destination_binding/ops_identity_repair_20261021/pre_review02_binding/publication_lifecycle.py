#!/usr/bin/env python3
"""PR399 gated Zenodo stage/publish adapter with durable no-blind-retry intents."""
import argparse
import json
from ops_binding import *
from publication_live_gates import collect


class GuardedLifecycleClient:
    """Refresh all live observations before EACH create/upload/update/publish."""
    def __init__(self,action,expected_head,identifier=None,delegate=None):
        self.action,self.expected_head,self.identifier=action,expected_head,identifier
        self.delegate=delegate if delegate is not None else zenodo.ZenodoClient('production',zenodo.token_for('production'))

    def before(self,identifier):
        if identifier!=self.identifier:
            raise RuntimeError('Lifecycle mutation ID differs from exact tracked target')
        require_release_clearance()
        phase='before_stage' if self.action=='stage' else 'before_publish'
        gate,_=collect(phase,self.expected_head,identifier)
        require_release_clearance()
        fresh(gate['started_utc'])

    def create(self,metadata):
        if self.action!='stage' or self.identifier is not None:
            raise RuntimeError('No second draft allocation allowed')
        self.before(None)
        result=self.delegate.create(metadata)
        identifier=result.get('id')
        if type(identifier) is not int or identifier<=0:
            raise RuntimeError('Uncertain create ID; reconcile durable intent and full account')
        self.identifier=identifier
        return result

    def get(self,identifier):
        if identifier!=self.identifier:raise RuntimeError('Unexpected lifecycle read ID')
        return self.delegate.get(identifier)

    def upload(self,bucket,entry):
        if self.action!='stage' or self.identifier is None:raise RuntimeError('Upload lacks tracked draft')
        self.before(self.identifier)
        return self.delegate.upload(bucket,entry)

    def update(self,identifier,metadata):
        if self.action!='stage':raise RuntimeError('Publish may not update metadata')
        self.before(identifier)
        return self.delegate.update(identifier,metadata)

    def publish(self,identifier):
        if self.action!='publish':raise RuntimeError('Stage may not publish')
        self.before(identifier)
        return self.delegate.publish(identifier)


def run_action(action,expected_head,identifier=None):
    if action not in {'stage','publish'}:raise RuntimeError('Unknown lifecycle action')
    require_release_clearance()
    verify_destination()
    integration=json.loads((AUDIT/'PR_MERGE_VERIFIED.json').read_text())
    if (integration.get('merged') is not True or integration.get('head')!=expected_head
            or integration.get('original_files')!=11 or integration.get('publication_files')!=5
            or integration.get('queue_other_bytes_preserved') is not True
            or integration.get('all_unselected_root_unsolved_attempts_siblings_preserved') is not True):
        raise RuntimeError('Exact actual merge preservation receipt absent')
    path=PUBLICATION/'zenodo-deposit.json'
    place,state=zenodo.local_state(path.resolve(),'production')
    if action=='stage':
        if identifier is not None or state is not None:
            raise RuntimeError('Initial stage requires no allocated ID/state; reconcile existing draft explicitly')
    elif (type(identifier) is not int or identifier<=0 or state is None or state['id']!=identifier
          or state.get('manifest')!=str(path.resolve()) or state.get('environment')!='production'):
        raise RuntimeError('Publish requires the exact saved manifest/production ID')
    intent=AUDIT/('ZENODO_'+action.upper()+'_INTENT.json')
    if intent.exists():
        raise RuntimeError('Prior lifecycle intent exists; inspect/reconcile outcome before any retry')
    phase='before_stage' if action=='stage' else 'before_publish'
    gate,acceptance=collect(phase,expected_head,identifier)
    require_release_clearance()
    fresh(gate['started_utc'])
    intent_json(intent,{'timestamp':stamp(),'pr':399,'action':action,'expected_pr_head':expected_head,
        'expected_deposit_id':identifier,'manifest':str(path),'release_manifest_sha256':RELEASE_SHA,
        'gate_receipt':gate['receipt'],'gate_sha256':acceptance['gate_sha256'],
        'uncertain_outcome_rule':'Never blindly repeat. Inspect saved exact draft/full account and reconcile the existing intent.'})
    result=zenodo.run(argparse.Namespace(command=action,manifest=path,sandbox=False,
                                       confirm_id=identifier,check_doi=True),
                      client=GuardedLifecycleClient(action,expected_head,identifier))
    expected='ready_to_publish' if action=='stage' else 'published'
    if result.get('state')!=expected or type(result.get('id')) is not int or result['id']<=0 or (
            identifier is not None and result['id']!=identifier):
        raise RuntimeError('Unexpected lifecycle outcome; preserve intent and reconcile without retry')
    atomic_json(AUDIT/('ZENODO_'+action.upper()+'.json'),result)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['stage','publish'])
    parser.add_argument('--expected-pr-head',required=True)
    parser.add_argument('--deposit-id',type=int)
    args=parser.parse_args()
    print(json.dumps(run_action(args.action,args.expected_pr_head,args.deposit_id),indent=2))


if __name__=='__main__':
    main()
