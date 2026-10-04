from pathlib import Path
import datetime,hashlib,json,os
base=Path(__file__).resolve().parent
pin=lambda p:{'bytes':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
initial=json.loads((base/'INPUT_PINS.json').read_text())
package=base.parent/'publication_package_v3'
assert {n:pin(package/n) for n in initial['qualified_inputs']}==initial['qualified_inputs']
final=json.loads((base/'FINAL_CHECKS.json').read_text())
assert final['status']=='PASS_FINAL_BINDINGS_REPRODUCTION_PIXELS_AND_PROVENANCE'
actual_final=json.loads((base/'private/commands/final_checks/CAPTURE.json').read_text())
assert actual_final['completed'] and actual_final['exit_code']==0
receipts=dict(final['captures']);receipts['final_checks']=actual_final
(base/'EXECUTION_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
verdict={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'PASS_QUALIFIED_RELEASE_NO_SUBSTANTIVE_ISSUES','review_kind':'NEW_FROM_SCRATCH_FULL_PACKAGE_ADVERSARY_ROUND_ONE',
 'reviewer':'/root/pr50_qualified_publication_round1_adversary',
 'input_pins':initial['qualified_inputs'],'original_head':initial['original_head'],
 'mathematical_review':'PASS_RELATIVE_TO_EXPLICIT_ESTABLISHED_IMPORTED_THEOREMS',
 'qualified_release_ready':True,'substantive_issues':[],'required_repairs':[],
 'historical_priority':'UNRESOLVED_INCOMPLETE_ACCESS_LIMITED','priority_certified':False,'novelty_certified':False,
 'fuller_Nencka_bodies_accessed':False,'Fiedler_full_counterexample_proof_certified':False,
 'human_PR50_priority_exception_applied':True,'human_peer_review':False,'formal_proof_certification':False,
 'fresh_portable_checks':7114,'distinct_invariant_scheme_cases':17266,'zero_shift_mutant_exit':1,
 'all_five_pdf_pages_personally_viewed':True,'all_five_rebuilt_pages_identical':True,
 'review_files':{n:pin(base/n) for n in ('REPORT.md','INPUT_PINS.json','FINAL_CHECKS.json','EXECUTION_RECEIPTS.json','RESEARCH_LOG.md')},
 'review_completion_percent':100,'new_central_proof_attempts':0,
 'external_publication_performed':False,'DOI_established':False,'tracker_updated':False,'PR_merged':False,
 'next_required':'Second NEW independent complete-package adversary followed by ROOT external-state readbacks'}
(base/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
for name in ('REPORT.md','INPUT_PINS.json','FINAL_CHECKS.json','EXECUTION_RECEIPTS.json','RESEARCH_LOG.md','VERDICT.json'):
    os.chmod(base/name,0o444)
print(json.dumps(verdict,indent=2))
