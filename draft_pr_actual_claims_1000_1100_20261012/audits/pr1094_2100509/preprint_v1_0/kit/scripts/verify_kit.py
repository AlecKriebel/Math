import argparse
import json
import sys
sys.dont_write_bytecode=True
from safety import verify_payload, binding_check, require, load_json, member, record

def terminal_accounting():
    # Additive stage semantics only. Existing payload, binding, mathematical
    # and filesystem guards remain the unchanged safety.py contracts.
    t=load_json(member('TERMINAL_ACCOUNTING_20261016.json'))
    require(t['schema']==1 and t['pr']==1094 and
            t['head_oid']=='954dd70b49458026e29b8dae63243391249008d8' and
            t['original_submitted_files']==8, 'terminal identity')
    require(type(t['completed_new_whole_package_reviews']) is int and
            type(t['minimum_new_whole_package_reviews']) is int and
            t['completed_new_whole_package_reviews']==t['minimum_new_whole_package_reviews']==2
            and t['new_complete_whole_review_required'] is False,
            'terminal whole-review counts')
    for key in ('publication_ready','issues_resolved','published',
                'root_terminal_integrity_adopted','external_human_peer_review',
                'formal_proof_assistant_certification','final_readiness_seal_issued'):
        require(t[key] is False, 'terminal false flag: '+key)
    for key in ('root_terminal_integrity_required','root_whole02_adopted',
                'extensive_AI_assistance','unrefereed'):
        require(t[key] is True, 'terminal true flag: '+key)
    require(t['ordered_services_hold_pr']==1032 and t['service_actions_permitted'] is False,
            'terminal service hold')
    for key in ('full_result_priority','construction_method_priority','novelty',
                'worldwide_preexisting_openness'):
        require(t[key]=='UNKNOWN', 'terminal priority: '+key)
    require(t['mathematical_scope']==
            'All n>=1; globally smooth compactly supported real Nijenhuis tensor; prescribed numerical real Jordan matrix in a commuting smooth local frame on a nonempty open domain iff all spectrum is real; type, rank and eigenvalues may change outside; no fixed Cartesian matrix, global regularity or analytic compact support.',
            'terminal mathematical scope')
    require(t['stage']=='TERMINAL_ACCOUNTING_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY' and
            t['not_another_whole_review'] is True, 'terminal pending stage')
    require(all(type(t['latest_whole_review'][k]) is int for k in ('number','P0','P1','P2','P3')) and
            t['latest_whole_review']=={'number':2,'complete':True,'repair_only':False,
                                    'P0':0,'P1':0,'P2':0,'P3':0},
            'terminal latest whole review')
    ledger=load_json(member('TERMINAL_SOURCE_COPY_LEDGER.json'))
    origins=[r['original_path'] for r in ledger['copies']]
    require(len(origins)==len(set(origins))==10, 'terminal copy ledger count')
    for r in ledger['copies']:
        require(record(member(r['copy_path']),r['original_path'])==
                {'path':r['original_path'],'bytes':r['bytes'],'sha256':r['sha256']},
                'terminal authored copy hash')
    by_origin={r['original_path']:r for r in ledger['copies']}
    require(set(t['evidence'])=={'report','derivation','source_ledger','verdict',
                               'output_pins','seal','root_adoption'},
            'terminal evidence roles')
    expected={'report':'reviews/package_02/REPORT.md',
              'derivation':'reviews/package_02/INDEPENDENT_DERIVATION.md',
              'source_ledger':'reviews/package_02/SOURCE_READ_LEDGER.json',
              'verdict':'reviews/package_02/VERDICT.json',
              'output_pins':'reviews/package_02/OUTPUT_PINS.json',
              'seal':'reviews/package_02/SEAL.json',
              'root_adoption':'ROOT_WHOLE_PACKAGE_REVIEW_02.json'}
    require(set(by_origin)==set(expected.values())|{'preprint_v1_0/README.md',
            'preprint_v1_0/kit/README.md','preprint_v1_0/kit/scripts/verify_kit.py'},
            'terminal exact selection origins')
    for role,origin in expected.items():
        require(t['evidence'][role]==by_origin[origin], 'terminal evidence locator: '+role)
    def evidence(role): return load_json(member(t['evidence'][role]['copy_path']))
    v=evidence('verdict'); s=evidence('seal'); root=evidence('root_adoption')
    pins=evidence('output_pins')
    for e in (v,s):
        require(e['pr']==1094 and e['head_oid']==t['head_oid'] and
                e['original_submitted_files']==8, 'terminal evidence identity')
    for key in ('full_result_priority','construction_method_priority','novelty',
                'worldwide_preexisting_openness'):
        require(v[key]=='UNKNOWN', 'terminal verdict priority')
    require(v['complete_whole_review'] is True and v['repair_only_review'] is False and
            v['actionable_findings']==[] and
            all(type(v[k]) is int and v[k]==0 for k in ('P0','P1','P2','P3')),
            'terminal verdict semantics')
    require(s['full_review'] is True and s['input_count']==388 and s['output_count']==27 and
            s['actionable_findings']==0 and all(s[k]==0 for k in ('P0','P1','P2','P3')),
            'terminal seal semantics')
    actual=record(member(t['evidence']['output_pins']['copy_path']),'OUTPUT_PINS.json')
    require(s['output_pins']==actual and root['output_pins_sha256']==actual['sha256'] and
            len(pins['records'])==27, 'terminal review seal hash binding')
    pinmap={r['path']:r for r in pins['records']}
    for role in ('report','derivation','source_ledger','verdict'):
        e=t['evidence'][role]; name=e['original_path'].split('/')[-1]
        require(pinmap[name]=={'path':name,'bytes':e['bytes'],'sha256':e['sha256']},
                'terminal selected review-output binding')
    require(root['status']=='ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN'
            and root['whole_reviews_completed']==root['minimum_whole_reviews']==2
            and root['actionable_P0_P1_P2_P3']==0
            and root['terminal_administrative_reconciliation_and_root_final_integrity_required'] is True,
            'terminal root adoption semantics')
    for e in (v,s,root):
        require(e['publication_ready'] is False and e['published'] is False,
                'terminal evidence readiness')
    require(v['ordered_services_hold_pr']==s['ordered_services_hold_pr']==root['services_held_after_pr']==1032,
            'terminal evidence service hold')
    require(root['full_result_and_method_priority_novelty_worldwide_openness']=='UNKNOWN',
            'terminal root priority')
    old=t['preserved_repair_status']
    require(record(member('CURRENT_STATUS.json'),'CURRENT_STATUS.json')==old,
            'terminal captured repair status binding')
    dated=load_json(member('CURRENT_STATUS.json'))
    require(dated['completed_new_whole_package_reviews']==1 and
            dated['new_complete_whole_review_required'] is True,
            'terminal dated repair status')
    require(ledger['prior_partitions_unchanged']==[171,309] and
            ledger['no_omitted_code_replay_claim'] is True,
            'terminal historical partition semantics')
    return {'status':'PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY',
            'completed_whole_reviews':2,'minimum_whole_reviews':2,
            'publication_ready':False,'issues_resolved':False,'published':False,
            'ordered_services_hold_pr':1032}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--binding');parser.add_argument('--require-binding',action='store_true');args=parser.parse_args()
    data=verify_payload()
    terminal=terminal_accounting()
    print(json.dumps({'status':'PASS','payload_files':len(data['records']),
                      'terminal_accounting':terminal,
                      'binding':binding_check(args.binding,args.require_binding)},sort_keys=True))
if __name__=='__main__': main()
