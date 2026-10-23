"""Read-only scoped review of the exact candidate02 field mapping. No actor/service/writes."""
from pathlib import Path
import argparse,base64,hashlib,json,stat
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');A=R/'audits';P=A/'pr1131_30005455';W=A/'final_reconciliation_new_independent_adversary01';D=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
def load(p,h):
 b=p.read_bytes();assert H(b)==h
 n={'__file__':str(p),'__name__':'_readonly_candidate_mapping_'+p.stem};exec(compile(b,str(p),'exec',optimize=0),n);return n
I=load(W/'independent_checks.py','63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a')
eq=I['typed'];strict=I['strict'];pins=[]
def raw(p,h):
 b=p.read_bytes();assert H(b)==h and not any(q.is_symlink()for q in[p,*p.parents]);pins.append({'path':str(p),'bytes':len(b),'sha256':h});return b
def read(p,h):return strict(raw(p,h))
def native(p,h):
 v=read(p,h);assert type(v['returncode'])is int and v['returncode']==0 and v.get('error')is None and base64.b64decode(v['stderr_base64'],validate=True)==b''
 return strict(base64.b64decode(v['stdout_base64'],validate=True))
def closed(h):
 p=D/'MANIFEST.json';m=read(p,h);assert m['schema']=='independent-external1131-candidate02-mapping-review-1'
 actual={str(q.relative_to(D)):q for q in D.rglob('*')};assert set(actual)==set(m['files'])|{'MANIFEST.json'}
 for name,pin in m['files'].items():
  q=actual[name];s=q.lstat();assert stat.S_ISREG(s.st_mode)and not q.is_symlink()and s.st_nlink==pin['nlink']and stat.S_IMODE(s.st_mode)==pin['mode']and s.st_mtime_ns==pin['mtime_ns']
  b=q.read_bytes();assert len(b)==pin['bytes']and H(b)==pin['sha256']
 return True
def proof():
 builder=raw(A/'ROOT_PR1131_EXTERNAL_GET_ONLY_COMPLETION_CANDIDATE_BUILDER02.py','f3adc7b842839e9d64fc2fe1e62f3bb74b5f438584ecb490c6dc269443940148')
 cand=read(P/'get_only_external_completion_candidate02/ROOT_CANDIDATE_RECEIPT.json','dbd6438050b1def49b13f433bd1eb3d0bc1cab10a14404282ed23759d88d5127')
 assert cand['kind']=='ROOT_EXTERNAL_COMPLETION_RECEIPT_DATA_JOIN_CANDIDATE_NOT_R_COMPLETION'and all(cand[k]is True for k in['ROOT_final_adoption_pending','no_R_completion_receipt_written','no_actor_or_service_calls','no_base_LEDGER_VERIFIED_created'])
 result=native(W/'NATIVE_ACTUAL1131_READONLY_RECONCILIATION_ORIGINAL_TRANSPORT03.json','428d19f2f9284b0147585d63cfc6eef68c161e9d78db48e972024a847428abe2')
 checker=load(W/'check_actual1131_readonly_reconciliation03.py','2a923d9f36abe654a9ea8fd0e9cf119271a93686fdfb3e45e620ed5dadd41d30')
 assert eq(checker['main'](),result)
 rootcold=native(A/'ROOT_PR1131_EXTERNAL_GET_ONLY_PROOF_ACTUAL_COLD_NATIVE01.json','4835c9bf8b67c81684263e24990b000a6212e9795f4b037627ff2311b32d89a7');assert eq(rootcold,result)
 secondary=native(A/'ROOT_PR1131_POSTAPPEND_REVIEW_ACTUAL_COLD_NATIVE01.json','24e862ed3d29ae273f45536fd13ca9eb17301a99a94a7e9f768087831cd60b26')
 assert secondary['status']=='PASS'and secondary['independent_actual_kernel_controls']==42 and secondary['semantic_falsifiers']==21 and secondary['actor_certification']is False and secondary['Root_receipt_builder_reviewed']is False and secondary['actual_effects']==0
 r=cand['receipt'];assert r['at']==cand['at']and r['complete']is True and r['pr']==1131 and r['problem_id']=='30005455'
 assert r['doi']==result['doi']and r['record']==result['record']==23592692 and r['concept']==23592691 and r['owner']==1789874
 assert r['ledger_row']==result['sheet_row']==287 and r['ledger_new_row']is True
 intent=read(P/'operations19/runtime/LEDGER_APPEND_INTENT.json','fa72b5f4b46faaf7ce707046ec184d9626247c1d9952d6afba42e3c5b159f1d2')
 assert eq(r['ledger_new_four_literal_cells'],intent['values'])
 assert r['integrated_head']=='9601e1e768c94522bc8ad105db4dfae4770bad75'and r['merge_commit']=='67915a3df87d3bdd19be74ac04b1a39fd0ce89f3'
 assert r['successful_actor_actions']==3 and r['ledger_actor_returncode']==1 and r['append_attempts']==1 and r['append_retries']==0 and r['future_service_write_allowance']==0
 assert all(r[k]is False for k in['all_four_actor_actions_succeeded','ledger_actor_certification','base19_LEDGER_VERIFIED_exists','actor_ledger_parsed_exists','final_global_reconciliation_complete'])
 assert r['original_Completion05_permanently_inapplicable']is True and r['no_GitHub_release_or_duplicate_record_created']is True
 assert r['publication_verification_mode']=='EXTERNAL_GET_ONLY_READBACK_AFTER_ACKNOWLEDGED_APPEND_AND_PRESERVED_ACTOR_POSTWRITE_FRESHNESS_FAILURE'
 assert r['actual_effect_counts']=={'new_deposition_POST':1,'PDF_PUT':1,'source_ZIP_PUT':1,'metadata_PUT':1,'publication_POST':1,'atomic_ledger_append':1}
 assert eq(r['evidence'],result['external_inputs'])
 for pin in r['evidence']:b=raw(Path(pin['path']),pin['sha256']);assert len(b)==pin['bytes']
 sciencepin=r['scientific_and_base_whole_review_adoption'];science=read(Path(sciencepin['path']),'96cb0f067e342578b7b4e426471da2308be62d8b6ea0c8ba51168eba8f0f0890')
 assert eq(r['qualified_theorem'],science['mathematical_scope'])and eq(r['priority'],science['priority'])
 manifest=read(P/'operations/proposed/preprint/zenodo-deposit.json','0ca12e07eee0ed88da4f94b82a2404eed4341aaa1f08f9100ecb630014fed6fe')
 assert r['title']==manifest['metadata']['title']and r['canonical_manifest_sha256']=='0ca12e07eee0ed88da4f94b82a2404eed4341aaa1f08f9100ecb630014fed6fe'
 primary=native(W/'NATIVE_PR1131_PRIMARY_PACKAGE_ORIGINAL_TRANSPORT.json','6bc29800e341b84e8638251aca2ceb9ce1cdfe34fde01d1114a24711556d6c56');assert eq(r['public_download_payloads'],primary['files'])
 dates=r['dated_observations'];assert eq(dates['sheet_original_full43_reads'],result['full287_original_native_observations'])and dates['public_readback_completed_at']==result['latest_public_original_after']
 assert all(dates[k]is True for k in['sheet_observed_at_is_start','separate_dated_observations_not_original_Source19_facts_fresh_bundle','no_atomic_cross_service_claim'])
 assert r['sheet_representation_qualification']==result['representation_qualification']
 assert r['doi_destination']==r['url']=='https://zenodo.org/records/23592692'
 assert 'At the retained ledger child finish12:34:19.937837UTC'in r['postappend_failure']and 'exact guard evaluation timestamp was not logged'in r['postappend_failure']
 assert 'no formal independent human peer review'in r['ai_and_preprint_disclosures']
 assert len(r['required_native_checks'])==13 and all(type(v)is bool and v for v in r['required_native_checks'].values())
 for k in['actual_source21_joint_adoption','actual_ROOT_execution_adoption','original_failed_ledger_parent','independent_external_actual_proof','ROOT_external_proof_separate_cold','read_only_public_acceptance']:
  pin=r[k];b=raw(Path(pin['path']),pin['sha256']);assert len(b)==pin['bytes']
 for pin in r['independent_complete_postappend_review'].values():b=raw(Path(pin['path']),pin['sha256']);assert len(b)==pin['bytes']
 return {'status':'CLEAN_EXACT_CANDIDATE02_EXTERNAL_COMPLETION_FIELD_MAPPING','candidate_sha256':'dbd6438050b1def49b13f433bd1eb3d0bc1cab10a14404282ed23759d88d5127','builder_sha256':H(builder),'publication_and_row_proof':'428d19f2f9284b0147585d63cfc6eef68c161e9d78db48e972024a847428abe2','second_actual_kernel_controls':42,'second_semantic_falsifiers':21,'remaining_substantive_mapping_concerns':[],'historical_precision_qualification_preserved':True,'successful_actor_actions':3,'failed_actor_action_returncode':1,'acknowledged_append':1,'no_fabricated_actor_certificate':True,'actual_service_effects_by_this_review':0,'ROOT_receipt_adoption_still_required':True,'final_global_inventory_numeric_QUEUE_review_still_required':True,'final_clearance':False}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256');a=ap.parse_args()
 verified=closed(a.manifest_sha256)if a.manifest_sha256 else False;r=proof();r['closed_review_namespace_verified']=verified;print(json.dumps(r,sort_keys=True,indent=2))
if __name__=='__main__':main()
