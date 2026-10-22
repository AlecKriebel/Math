#!/usr/bin/env python3
"""Final local preservation/current/output inventories and separate noncircular seal."""
import sys
sys.dont_write_bytecode=True
import os
import prepare_terminal as p
def main():
    F,A,P,K=p.F,p.A,p.P,p.K
    utc=p.datetime.datetime.now(p.datetime.timezone.utc).isoformat()
    freeze=p.load(F/'INPUT_FREEZE.json')['entries'];before={r['path']:r for r in p.load(F/'BEFORE_BYTES.json')['entries']}
    changes=p.load(F/'CURRENT_CHANGES.json')['changes'];changed={r['path'] for r in changes};rows=[]
    for r in freeze:
        target=A/(before[r['path']]['before_path'] if r['path'] in changed else r['path'])
        p.need(p.pin(target)=={k:r[k] for k in ['bytes','sha256']},'final preservation '+r['path'])
        rows.append({'path':r['path'],'state':'EXACT_CAPTURED_BEFORE_BYTES' if r['path'] in changed else 'EXACT_UNCHANGED_CURRENT_BYTES','resolved_path':target.relative_to(A).as_posix(),**p.pin(target)})
    p.need(len(changed)==7 and len(rows)==683,'bounded mutation count')
    p.write(F/'INPUT_PRESERVATION.json',{'utc':utc,'all_preexisting_identities_preserved':True,'unchanged':676,'minimal_changed_with_exact_before_bytes':7,'entries':rows})
    p.need((P/'TERMINAL_ADMIN.json').read_bytes()==(K/'TERMINAL_ADMIN.json').read_bytes(),'terminal exact interfaces')
    p.need((p.Path('/Users/alec/Documents/Math/.git/HEAD')).read_text().strip()=='ref: refs/heads/main','checkout must remain main')
    inputs=[p.Path('/Users/alec/Documents/Math/AGENTS.md'),p.Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')]
    p.write(F/'ADDITIONAL_INPUT_PINS.json',{'utc':utc,'scope':'Read-only repository instructions and native local-check tool, not redistributed','entries':[{'path':str(q),**p.pin(q)} for q in inputs]})
    current=[{'path':q.relative_to(A).as_posix(),**p.pin(q)} for q in sorted(P.rglob('*')) if q.is_file()]
    p.write(F/'CURRENT_CANDIDATE_PINS.json',{'utc':utc,'scope':'Every current regular preprint file, including unchanged historical artifacts and current external descriptors; not a rewrite of any old OUTPUT_PINS','entries':current})
    validations=p.load(F/'VALIDATION.json');p.need(validations['status']=='PASS' and validations['command_count']==131,'final complete validation missing')
    p.need(validations['archive']==p.pin(P/'pr1097_support_v1_0.zip'),'validation bound to wrong archive')
    with (F/'RESEARCH_LOG.md').open('a') as s:
        s.write('\n'+utc+' — Final refined archive passed all 131 actual commands (21 successful commands and 110 intended rejections). Complete normal/-O math JSON equals EXPECTED_RESULTS. Closed 198-member archive independently reproduced with every local/central header, payload and CRC checked. All683 preexisting identities preserved, seven changed interfaces have exact before bytes, original165 and repair332 partitions and old1127 rows remain unchanged. No compile/render/PDF authoring marker, Git/service/PR/outreach action. Delegated reconciliation completion estimate: 100%; external ROOT final independent reproduction/adoption is still required and not adopted. All writes settle with the following separate evidence seal.\n')
    p.write(F/'VERDICT.json',{'utc':utc,'record_type':'TERMINAL_ADMINISTRATIVE_RECONCILIATION_HANDOFF_ONLY','status':'COMPLETE_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY','delegated_completion_percent':100,
        'substantive_new_defect_found':False,'two_completed_whole_reviews':True,'latest_whole02_zero_actionable_ROOT_adopted':True,
        'no_further_whole_review_currently_required':True,'external_ROOT_final_integrity_required':True,'external_ROOT_final_integrity_adopted':False,
        'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,
        'no_new_compilation_rendering_PDF_authoring_marker':True,'no_Git_index_branch_service_PR_outreach_actions':True,
        'remaining_gap':'ROOT must read the full terminal report and operative diff, independently reproduce and adopt this exact final package before any new readiness seal. A substantive new defect requires hold, repair and new complete whole03.'})
    outputs=[{'path':q.relative_to(F).as_posix(),**p.pin(q)} for q in sorted(F.rglob('*')) if q.is_file() and q not in [F/'OUTPUT_PINS.json',F/'FINAL_SEAL.json']]
    p.write(F/'OUTPUT_PINS.json',{'utc':utc,'scope':'Every owned regular finalization output including exact local old ZIP before bytes; excludes this inventory and separate FINAL_SEAL. Local raw receipts and oldZIP are not distributed in kit.','entries':outputs})
    p.write(F/'FINAL_SEAL.json',{'utc':utc,'state':'ALL_WRITES_SETTLED_TERMINAL_ADMINISTRATIVE_HANDOFF','output_inventory':p.pin(F/'OUTPUT_PINS.json'),'report':p.pin(F/'REPORT.md'),
        'operative_diff':p.pin(F/'COMPLETE_OPERATIVE_CODE_PROSE_DIFF.patch'),'input_freeze':p.pin(F/'INPUT_FREEZE.json'),'current_candidate_inventory':p.pin(F/'CURRENT_CANDIDATE_PINS.json'),
        'paper':p.pin(P/'paper.pdf'),'archive':p.pin(P/'pr1097_support_v1_0.zip'),'kit_manifest':p.pin(K/'MANIFEST.json'),'external_binding':p.pin(P/'DEPOSIT_BINDING.json'),
        'output_files':len(outputs),'delegated_completion_percent':100,'evidence_seal_only_not_readiness_or_publication_authority':True,
        'external_ROOT_final_integrity_required':True,'external_ROOT_final_integrity_adopted':False,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,
        'no_hash_cycle':'Output inventory excludes itself and FINAL_SEAL; seal binds that inventory. Current native metadata/files object unchanged; binding outside ZIP.'})
    print(p.json.dumps(p.load(F/'FINAL_SEAL.json'),indent=2))
if __name__=='__main__':main()
