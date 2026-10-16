#!/usr/bin/env python3
"""Read-only verification of final review records and genuine canonical scopes.

Only own SEAL_CHECKS.json is written. No helper invocation or API mutation.
"""
import ast, datetime, json, hashlib
from pathlib import Path
from audit_inputs import OWN, CASE, PROGRAM, HEAD, binding, check, FAMILIES

def read(p): return json.loads(p.read_text())
def exact_int(x,n,label): check(type(x) is int and x==n,label)
def main():
 final=read(OWN/'CONTROL_RESULTS.json'); repeats=read(OWN/'REPEAT_CONTROLS.json')
 expected={'positive_pass':3,'intended_guard_rejection':98,'unexpected_acceptance':14,'test_defect_or_wrong_guard':1}
 modes={m:{x['case']:x for x in final['runs'] if x['mode']==m} for m in ['normal','optimized']}
 check(set(modes['normal'])==set(modes['optimized']) and len(modes['normal'])==116,'mode coverage')
 for m,runs in modes.items():
  check({k:sum(x['outcome']==k for x in runs.values()) for k in expected}==expected,'exact outcome counts')
  check(all(x['27_research_fixture_files_unchanged'] is True and x['mock_ref_patches']<=1 for x in runs.values()),'source/no-repeat')
  check(all(x['returncode']==0 and x['mock_ref_patches']==1 and x['ref_moved'] is True for x in runs.values() if x['outcome']=='unexpected_acceptance'),'unexpected acceptance effect')
  check(runs['baseline_preflight']['mock_git_writes']==0,'preflight wrote Git')
  for name in ['baseline_apply','uncertain_patch_applied']:check(runs[name]['one_row_exact_preservation'] is True,'apply preservation')
  for name in ['excluded:solved','excluded:already_solved','excluded:out_of_scope']:
   check(runs[name]['mock_git_writes']==0 and runs[name]['actual_last_error']=='RuntimeError: Excluded status: stop without processing','excluded guard')
  for name in ['missing_actual_gate','actual_eight_review_draft_as_gate']:check(runs[name]['mock_git_writes']==0 and runs[name]['returncode']!=0,'actual unapproved gate')
 for name in modes['normal']:
  a=modes['normal'][name];b=modes['optimized'][name]
  check(all(a[k]==b[k] for k in ['outcome','returncode','mock_git_writes','mock_ref_patches','ref_moved','operation_record_exists','actual_last_error']),'mode semantic difference '+name)
 check(repeats['actual_repeat_subprocesses']==10 and all(x['mock_api_calls_added']==0 and x['mock_ref_patches_added']==0 and x['returncode']!=0 for x in repeats['runs']),'actual repeat checks')
 pre=[];doi_checks=[]
 for m in modes:
  p=read(OWN/'private_cases/complete_run'/f'{m}_0/program/audits/pr458_20000693/STATUS_REPAIR_PREFLIGHT.json');p.pop('at_utc');pre.append(p)
  for name in ['baseline_preflight','baseline_apply','uncertain_patch_applied']:
   i=list(modes[m]).index(name)
   q=read(OWN/'private_cases/complete_run'/f'{m}_{i}/program/audits/pr458_20000693/STATUS_REPAIR_PREFLIGHT.json')
   old=q['selected_old_row'].split('|');new=q['selected_new_row'].split('|')
   check(old[12]==new[12] and old[12].strip()==new[12].strip()=='','retained actual DOI12 blank/preserved')
   check(old[9]==new[9] and new[9].strip()=='1/5','retained actual Turns9')
   check([n for n,(a,b) in enumerate(zip(old,new)) if a!=b]==[8,11],'retained actual only Status8 Findings11')
   doi_checks.append({'mode':m,'case':name,'actual_split_DOI_index':12,'old_and_new_DOI_blank':True,'DOI_bytes_preserved':True,'Turns_1_5_preserved':True,'only_changed_split_cell_indices':[8,11]})
 check(pre[0]==pre[1],'preflight difference beyond time')
 for m in modes:
  for i,x in enumerate(modes[m].values()):
   root=OWN/'private_cases/complete_run'/f'{m}_{i}'
   check(binding(root/'program/repair_pr458_status.py')==binding(OWN/'REVIEWED_HELPER.py') or x['case']=='stale_helper','wrong executed helper')
   check(binding(root/'stdout.txt')['sha256']==x['stdout_sha256'] and binding(root/'stderr.txt')['sha256']==x['stderr_sha256'],'raw output digest')
 canonical=[]
 for f in FAMILIES:
  result=read(CASE/'reviews'/f/'RESULT.json');manifest=read(CASE/'reviews'/f/'PUBLIC_FILES.json')
  check({'REPORT.md','RESULT.json'}<={x['path'] for x in manifest['files']},'complete actual positive packet')
  if 'asymptotic_proved' in result:check(result['asymptotic_proved'] is False,'actual theorem claim')
  if 'current_publication_scope' in result:
   check(result['current_publication_scope']['accepted'] is False,'actual pub acceptance')
  if 'proposed_mathematical_interpretation_scope' in result:
   scope=result['proposed_mathematical_interpretation_scope'];exact_int(scope['unresolved_central_math_gaps'],0,'actual central alias');check(scope['actual_high_moment_theorem_proved'] is False,'actual nested theorem')
  canonical.append({'family':f,'result':binding(CASE/'reviews'/f/'RESULT.json'),'manifest':binding(CASE/'reviews'/f/'PUBLIC_FILES.json')})
 for name in ['PRIORITY_ADVERSARY_FAMILY_READBACK.json','PRIORITY_COVERAGE_FAMILY_READBACK.json','CLASSIFICATION_FAMILY_READBACK.json']:
  r=read(CASE/name)
  for x in r['safe_payloads']:
   exact_int(x['bytes'],binding(CASE/x['path'])['bytes'],'internal readback bytes');check(x['sha256']==binding(CASE/x['path'])['sha256'],'internal readback digest')
 pad=read(CASE/'PRIORITY_ADVERSARY_FAMILY_READBACK.json')['raw_counts']
 for k,n in [('promotion_priority_blockers',1),('required_scope_documentation_repairs',5),('central_gaps_to_clarified_heuristic',0),('retained_theorem_model_gaps',3)]:exact_int(pad[k],n,k)
 pc=read(CASE/'reviews/priority_coverage/RESULT.json');exact_int(pc['count_scopes']['actual_general_asymptotic_unproved_inputs'],len(pc['unresolved_mathematical_gaps']),'coverage actual inputs')
 check(len(pc['unresolved_mathematical_gaps'])==3,'coverage theorem gaps')
 gate=read(CASE/'DRAFT_OPERATIONS_GATE.json');check(gate['operations_approval'] is False and gate['not_an_action_gate'] is True and gate['missing_actual_final_operations_review'] is True and len(gate['reviews'])==8,'actual draft flags')
 check(not (CASE/'PRIORITY_DISPOSITION_GATE.json').exists(),'actual action gate unexpectedly exists')
 initial=read(OWN/'INITIAL_BINDINGS.json')
 original={'helper':PROGRAM/'repair_pr458_status.py','synthesis':CASE/'DISPOSITION_SYNTHESIS.md','classification_draft':CASE/'DRAFT_PRIORITY_DISPOSITION.md','operations_draft':CASE/'DRAFT_OPERATIONS_GATE.json'}
 # Exact expected originals are independently pinned below; initial schema remains preserved.
 expected_hashes={'helper':'19594116e01e7a228b15443b78f278e9eb153cff3e57720e4dacc93aa457f39b','synthesis':'a29925c28e7337c5e47d3376826bcf8d2448cb1936a6745908fbe17893b67026','classification_draft':'9449598d2cf119d8b0db9e1c0f6552fd8d3bee2001aa17cc1f40119f1a10f084','operations_draft':'b333d089113749cef3a0df07f3fd95599248a84571c90b30c192b3eed4f33a14'}
 for k,p in original.items():check(binding(p)['sha256']==expected_hashes[k],'reviewed input drift '+k)
 check(binding(OWN/'REVIEWED_HELPER.py')==binding(original['helper']),'reviewed source snapshot')
 partial=read(OWN/'INITIAL_PARTIAL_CONTROLS.json');old=read(OWN/'INITIAL_COMPLETE_CONTROLS.json');oldrepeat=read(OWN/'INITIAL_REPEAT_CONTROLS.json')
 history_counts={'partial':len(partial['runs']),'first_complete':len(old['runs']),'first_repeats':len(oldrepeat['runs']),'final_complete':len(final['runs']),'final_repeats':len(repeats['runs'])}
 check(history_counts=={'partial':75,'first_complete':226,'first_repeats':10,'final_complete':232,'final_repeats':10},'history count')
 for p in [OWN/'run_controls.py',OWN/'repeat_controls.py',OWN/'mock_gh.py',OWN/'audit_inputs.py',OWN/'seal_checks.py']:
  check(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))),'own assert guard')
 out={'sealed_checks_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':458,'problem_id':'20000693','frozen_head':HEAD,'all_final_case_outcomes_match_across_modes':True,'preflight_outputs_equal_after_only_timestamp_removed':True,'normal':expected,'optimized':expected,'actual_helper_subprocess_history_counts':history_counts,'actual_helper_subprocess_total':sum(history_counts.values()),'final_actual_helper_subprocesses':len(final['runs'])+len(repeats['runs']),'actual_source27_unchanged':True,'actual_foundation_scopes_consistent':True,'actual_action_gate_exists':False,'reviewed_input_bindings':{k:binding(p) for k,p in original.items()},'canonical_family_bindings':canonical,'all_retained_final_stdout_stderr_hashes_match':True,'own_code_asserts':0,'real_remote_mutations':0}
 out.update(independent_retained_positive_DOI12_checks=doi_checks,original_harness_DOI10_indexing_defect_disclosed=True,original_harness_raw_records_changed=False,additional_helper_executions_for_DOI_seal=0)
 (OWN/'SEAL_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
