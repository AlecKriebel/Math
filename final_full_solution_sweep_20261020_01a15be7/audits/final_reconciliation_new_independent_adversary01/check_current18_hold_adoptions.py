"""Current qualified 18-hold adoption consistency; read-only, no proof/priority rerun."""
from pathlib import Path
import hashlib,json,sys
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
W=R/'audits/final_reconciliation_new_independent_adversary01'
p=W/'independent_checks.py';b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=='63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a'
n={'__name__':'_readonly_current18_adoptions','__file__':str(p)};exec(compile(b,str(p),'exec'),n)
pin={'path':'audits/ROOT_FINAL18_DOCUMENTED_HOLDS_CURRENT_REASON_SUMMARY.json','bytes':9658,'sha256':'f7f2752a940eb2e5e4e29d4041cda44178c6c3e92b01beda0e1bedd753262f13'}
s=n['objpin'](pin);j=n['frozen_join']()['baseline']()
expected={97,615,628,630,1160,1228,1231,1232,1239,1272,1297,1303,1327,1349,1351,1371,1384,1404}
assert len(s['rows'])==s['count']==18 and {x['pr']for x in s['rows']}==expected=={x['pr']for x in j['rows']if x['effective_coverage_bucket']=='documented_priority_scope_or_accounting_hold'}
assert s['no_new_action_or_novelty_clearance']is True and s['preserves_historical_provisional_dispositions_and_later_scoped_adoptions']is True
out=[]
for row in s['rows']:
 pr=row['pr'];a=n['objpin'](row['source']);assert row['new_publication']is False and row['invalidity_not_inferred_from_hold']is True
 if pr in(1228,1231,1232):
  items=[x for x in a['independent_scientific_outcomes_adopted']if x['pr']==pr]
  assert len(items)==1 and 'HOLD'in items[0]['accounting']and items[0]['four_literal_cells']is None and a['new_publication_authorized']is False
  assert str(pr)in a['root_final_corrections']
  evidence={'precise_scope':items[0]['scientific_status'],'accounting':items[0]['accounting'],'remaining_gap':items[0]['remaining_gap'],'later_root_correction':a['root_final_corrections'][str(pr)]}
 else:
  assert a['pr']==pr
  if pr in(97,615,628,630):assert a['new_publication']is False and a['disposition']=='skip_priority_gate_not_met'
  elif pr==1160:assert a['publication_ready']is False and a['no_new_publication_or_row']is True
  elif pr==1239:assert a['new_publication']is False and a['priority_decision']=='DO_NOT_PROMOTE_AS_NOVEL_FULL_OPEN_PROBLEM_RESOLUTION'
  elif pr==1272:assert a['mathematical_correctness_accepted']is True and a['publication_readiness']is False
  elif pr==1297:assert a['literal_unrestricted_counterexample_accepted']is True and a['intended_absolutely_irreducible_conjecture_resolved']is False and a['new_publication']is False
  elif pr==1303:assert a['complete_bounded_theorems_accepted']is True and a['complete_original_scope_accepted']is False and a['no_row_adopted']is True
  elif pr==1327:assert a['publication_ready']is False and a['no_already_solved_finding_without_covering_prior_theorem']is True
  elif pr==1349:assert a['new_publication_eligible']is False and a['publication_ready']is False
  elif pr==1351:assert a['scientific_correctness_accepted']is True and a['new_publication_ready']is False and a['no_existing_publication_row_invented']is True
  elif pr==1371:assert a['mathematical_and_package_verdict']=='TWO_FRESH_PASS_ROOT_ADOPTED'and a['priority_gate']=='HOLD_UNESTABLISHED'and a['new_publication_ready']is False
  elif pr in(1384,1404):assert a['no_paper_publication_or_new_DOI']is True and 'mathematical invalidity'in a['not_inferred']and 'already_solved status'in a['not_inferred']
  else:raise AssertionError('Unhandled hold')
  evidence={k:a[k]for k in('disposition','priority_decision','prior_and_accounting_status','precise_gap','exact_remaining_gap','reason_preventing_publication','novelty_disposition','scope_priority_and_repairs','root_adopted_priority_reason','source_adjudication','source_and_scope_qualifications')if k in a}
 out.append({'pr':pr,'current_reason':row['current_reason'],'source_pin':row['source'],'explicit_later_scoped_evidence':evidence,'invalidity_not_inferred':True})
assert len({x['source_pin']['path']for x in out})==16
print(json.dumps({'status':'PASS_CURRENT18_QUALIFIED_HOLD_SOURCE_AND_MAPPING_CONSISTENCY','count':18,'unique_exact_source_objects':16,'summary_pin':pin,'holds':out,'scope':'All16 full adoption/disposition objects independently read. This checks current accepted reason/coverage consistency, not a new mathematical or literature audit or live PR observation. Full-priority/authorship/category/body-access objections remain binding.','services':0,'new_publications':0,'final_clearance':False},sort_keys=True,ensure_ascii=False,indent=2))
