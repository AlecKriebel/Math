"""Independent metadata coverage verifier; no builder imports/network/Git."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
H=Path(__file__).resolve().parent
V=H.parent/'durable_facing_v02'
B=H.parent.parent
checks=[]
def ck(ok,label):
 assert ok,label
 checks.append(label)
def rawpin(p):
 ck(p.is_file() and not p.is_symlink(),'regular:'+str(p))
 raw=p.read_bytes()
 return raw,{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
             'git_blob_oid':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
def matches(p,item):
 raw,pin=rawpin(p)
 ck(all(pin[k]==item[k] for k in ['bytes','sha256']),'size/SHA:'+str(p))
 if 'git_blob_oid' in item:ck(pin['git_blob_oid']==item['git_blob_oid'],'native blob:'+str(p))
 return raw
inv=json.loads((H/'EXHAUSTIVE_V02_249_FILE_INVENTORY.json').read_bytes())
add=json.loads((H/'OUTER_COVERAGE_ADDENDUM.json').read_bytes())
evidence=json.loads((H/'FRESH_REVIEW_AND_ROOT_FAILURE_BINDINGS.json').read_bytes())
records={r['path']:r for r in inv['files']}
actual={p.relative_to(V).as_posix():p for p in V.rglob('*') if p.is_file()}
ck(len(records)==len(inv['files'])==inv['actual_file_count']==len(actual)==249,'exact249 file count')
ck(set(records)==set(actual),'exhaustive249 actual path inventory, no other omissions or extras')
ck(not any(p.is_symlink() for p in V.rglob('*')),'no symlink path elision')
for rel,item in records.items():
 ck('..' not in Path(rel).parts and not Path(rel).is_absolute(),'safe inventory path:'+rel)
 matches(actual[rel],item)
outer=json.loads(matches(V/'FINAL_MANIFEST.json',add['original_outer_manifest_pin']))
old={r['path']:r for r in outer['files']}
ck(len(old)==len(outer['files'])==247,'247 original listed entries')
for rel,item in old.items():
 ck(rel in records,'original listed path present:'+rel)
 ck(all(records[rel][k]==item[k] for k in ['bytes','sha256']),'all247 original entry pins authenticated:'+rel)
nested='payloads/draft_pr_descending_audit_20261002/audits/pr259_5100026/initial_review_20261012/elliptic_centroid_adversary/FINAL_MANIFEST.json'
omitted=sorted(set(actual)-set(old))
ck(omitted==['FINAL_MANIFEST.json',nested] and not (set(old)-set(actual)),'only original self and selected nested omissions')
ck([x['path'] for x in add['exact_omissions_from_original_outer_manifest']]==omitted,'exact explicit metadata addendum exclusions')
ck(add['other_omissions']==[] and add['original_phantom_entries']==[],'no undeclared gaps')
ck(add['exact_omissions_from_original_outer_manifest'][0]['original_self_exclusion_declared'] is True and add['exact_omissions_from_original_outer_manifest'][1]['original_outer_second_exclusion_declared'] is False,'original exclusion semantics preserved honestly')
for row in add['exact_omissions_from_original_outer_manifest']:matches(V/row['path'],row['pin'])
plan=json.loads(matches(V/'SCOPED_FILE_PLAN.json',add['existing_selection_bindings']['SCOPED_FILE_PLAN.json']))
ck(plan['selected_count']==231 and plan['selected_bytes']==4152796,'231 scientific files4152796bytes unchanged')
planrows={r['payload_relative_path']:r for r in plan['paths']}
ck(len(planrows)==len(plan['paths'])==231,'unique selected payload paths')
for rel,r in planrows.items():ck(all(records[rel][k]==r[k] for k in ['bytes','sha256','git_blob_oid']),'all231 exact selected payloads unchanged:'+rel)
prefix='payloads/draft_pr_descending_audit_20261002/audits/pr259_5100026/initial_review_20261012/'
pub=json.loads(matches(V/(prefix+'PUBLIC_FINDINGS_EXPORT_MANIFEST.json'),add['existing_selection_bindings']['PUBLIC_FINDINGS_EXPORT_MANIFEST.json']))
pubrows={prefix+r['audit_relative_path']:r for r in pub['files']}
ck(len(pubrows)==len(pub['files'])==230 and set(pubrows)==set(planrows)-{prefix+'PUBLIC_FINDINGS_EXPORT_MANIFEST.json'},'public exact selection self exclusion only')
for rel,r in pubrows.items():ck(all(records[rel][k]==r[k] for k in ['bytes','sha256','git_blob_oid']),'public selection binding:'+rel)
n=add['exact_omissions_from_original_outer_manifest'][1]
ck(n['existing_scoped_plan_entry']==planrows[nested] and n['existing_public_selection_manifest_entry']==pubrows[nested],'nested exact original plan/public selected entries bound')
historic=matches(B/'elliptic_centroid_adversary/FINAL_MANIFEST.json',n['historical_family_original_pin'])
ck(historic==(V/nested).read_bytes(),'nested selected manifest original historical bytes authentic')
canon=json.loads(matches(V/'CANONICAL_PUBLIC_MAP_PINS.json',add['existing_selection_bindings']['CANONICAL_PUBLIC_MAP_PINS.json']))
ck(len(canon['pins'])==len(add['six_canonical_author_facing_payloads_unchanged'])==6,'six canonical maps/documents/helper pins')
for r in add['six_canonical_author_facing_payloads_unchanged']:
 ck(all(r[k]==canon['pins'][r['name']][k] for k in ['bytes','sha256','git_blob_oid']),'canonical original pin preserved:'+r['name'])
 matches(V/r['path'],r)

f=Path(evidence['complete_fresh_review_root']);review={r['path']:r for r in evidence['complete_fresh_review_files']};real={p.relative_to(f).as_posix() for p in f.rglob('*') if p.is_file()}
ck(len(review)==len(evidence['complete_fresh_review_files'])==evidence['complete_fresh_review_file_count']==38 and set(review)==real,'all38 complete fresh review files bound')
for rel,item in review.items():matches(f/rel,item)
freshmf=json.loads(matches(f/'PUBLIC_MANIFEST.json',evidence['complete_fresh_review_manifest_pin']))
fm={r['path']:r for r in freshmf['files']}
ck(len(fm)==37 and set(review)-set(fm)=={'PUBLIC_MANIFEST.json'},'fresh review original manifest sole self exclusion')
for rel,item in fm.items():ck(all(review[rel][k]==item[k] for k in ['bytes','sha256']),'complete fresh review original entry:'+rel)
decision=json.loads(matches(f/'DECISION.json',evidence['fresh_decision_pin']))
ck(decision['scientific_selection_verdict']=='PASS' and decision['completed'] is True,'recorded prior scoped review result')
ck(decision['independent_primary_checker_checks']==5863 and decision['actual_unchanged_core_replays']==4,'recorded review5863 and4 actual cores, not rerun claim')
ck([x['id'] for x in decision['findings']]==['EXPORT-PREP-001'],'prior sole finding preserved')
for row in evidence['direct_input_bindings']:matches(Path(row['path']),row)
ck(len(evidence['all_known_Root_failures_preserved'])==3,'all three known Root failure receipts preserved')
for row in evidence['all_known_Root_failures_preserved']:
 root=B/row['folder'];d=json.loads(matches(root/'FAILURE_RECEIPT.json',row['receipt_pin']));matches(root/'FAILED_CHECKER.py',row['failed_checker_pin'])
 ck(d['completed'] is False and d['observed_exit_code']==1 and d['checker_sha256']==row['failed_checker_pin']['sha256'],'historical Root failure remains failed:'+row['folder'])
rp=json.loads(matches(B/'root_public_export_v02_selection_verification_04/VERIFICATION.json',evidence['later_Root_selection_only_receipt_pin']))
ck(rp['outer_preparation_inventory_exhaustive'] is False and rp['whole_preparation_promotion_acceptance'] is False,'prior bounded Root result not silently promoted')
ck(add['no_original_bytes_modified'] is True and add['all231_scientific_payloads_unchanged'] is True,'addendum only binds existing immutable bytes')
ck(add['no_new_scientific_acceptance'] is True and add['no_promotion_acceptance'] is True and add['no_execution_authority'] is True and add['case_complete'] is False,'no new scientific/promotion/action/case acceptance')
ck(add['provider_actions']==add['shared_git_actions']==add['outside_person_communications']==0,'no provider/Git/outside contact')
receipt={'schema':'pr259-independent-outer-coverage-local-verification-v1','utc':datetime.now(timezone.utc).isoformat(),
 'decision':'PASS_LOCAL_METADATA_COVERAGE_ONLY','check_count':len(checks),'checks':checks,
 'actual_v02_file_count':249,'all_original247_entries_authenticated':True,'only_omissions_in_original_outer_manifest':omitted,
 'all231_scientific_payloads_and_six_author_facing_pins_unchanged':True,'complete_fresh_review_files_bound':38,
 'all_three_known_Root_failure_receipts_preserved':True,'metadata_preparation_completion_percent':100,
 'new_scientific_promotion_execution_or_case_acceptance':False,'provider_actions':0,'shared_git_actions':0,
 'fresh_adversary_and_Root_acceptance_pending':True}
(H/'LOCAL_COVERAGE_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['decision','check_count','actual_v02_file_count','complete_fresh_review_files_bound','new_scientific_promotion_execution_or_case_acceptance']},indent=2))
