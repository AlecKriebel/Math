"""Minimal prospective external completion data join. No actor or service calls."""
from pathlib import Path
import json,hashlib,base64,datetime,os
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');A=R/'audits';P=A/'pr1131_30005455';RT=P/'operations19/runtime';OUT=P/'root_actual21_known23592692_actions01'
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda v:json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
SECOND_REVIEW_PINS=json.loads('{"ROOT_separate_cold": {"bytes": 4393, "path": "/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/ROOT_PR1131_POSTAPPEND_REVIEW_ACTUAL_COLD_NATIVE01.json", "sha256": "24e862ed3d29ae273f45536fd13ca9eb17301a99a94a7e9f768087831cd60b26"}, "checker": {"bytes": 7210, "path": "/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455/known23592692_postappend_get_only_review01/verify_postappend_review.py", "sha256": "043b144c73bfdad8f156d8868f83feceb3090099a841d0bb41e948dcd9730a0c"}, "manifest": {"bytes": 125972, "path": "/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455/known23592692_postappend_get_only_review01/MANIFEST_POSTAPPEND_REVIEW.json", "sha256": "e45f121a1067340497566ff5733e6d50235df825ec7d4368c19b998f993be8a3"}, "report": {"bytes": 9577, "path": "/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455/known23592692_postappend_get_only_review01/REPORT_POSTAPPEND_REVIEW.md", "sha256": "71bfc8d6dab3bde6bfc2f5a711b7cfe310e9be06aee12057398b8552f922161d"}}')
SECOND_COLD_EXPECTED=json.loads('{"Root_receipt_builder_reviewed": false, "actor_certification": false, "actual_effects": 0, "external_files": 165, "external_trees": 8, "independent_actual_kernel_controls": 42, "limits": "Dated separate12:40 sheet and12:44 public captures; no old facts_fresh renewal, fourth rc0 or base ledger certificate.", "manifest_sha256": "e45f121a1067340497566ff5733e6d50235df825ec7d4368c19b998f993be8a3", "original_native_envelopes": 7, "own_directories": 1, "own_files": 38, "semantic_falsifiers": 21, "status": "PASS"}')
def pin(p,h=None):
 b=p.read_bytes()
 if h is not None:assert H(b)==h,(p,H(b))
 assert p.is_file()and not any(q.is_symlink()for q in[p,*p.parents])
 return {'path':str(p),'bytes':len(b),'sha256':H(b)}
def strict(b):
 def pairs(xs):
  d={}
  for k,v in xs:assert k not in d;d[k]=v
  return d
 def bad(x):raise ValueError('Nonfinite JSON')
 return json.loads(b,object_pairs_hook=pairs,parse_constant=bad)
def read(p,h=None):
 b=p.read_bytes()
 if h is not None:assert H(b)==h
 assert p.is_file()and not any(q.is_symlink()for q in[p,*p.parents])
 return strict(b)
def decoded_native(p,h):
 v=read(p,h);assert type(v['returncode'])is int and v['returncode']==0 and v['error']is None and base64.b64decode(v['stderr_base64'],validate=True)==b''
 return v,strict(base64.b64decode(v['stdout_base64'],validate=True))
coldp=A/'ROOT_PR1131_EXTERNAL_GET_ONLY_PROOF_ACTUAL_COLD_NATIVE01.json'
cold,facts=decoded_native(coldp,'4835c9bf8b67c81684263e24990b000a6212e9795f4b037627ff2311b32d89a7')
assert facts['status']=='PASS_INDEPENDENT_EXTERNAL_GET_ONLY_PR1131_PUBLICATION_AND_ROW_WITH_FAILED_LEDGER_ACTOR_PRESERVED'
assert facts['record']==23592692 and facts['doi']=='10.5281/zenodo.23592692'and facts['sheet_row']==facts['sheet_rows']==287
assert facts['successful_actor_actions']==3 and facts['ledger_actor_returncode']==1 and facts['failed_actor_action']=='ledger'and facts['append_retried']is False
assert facts['base_LEDGER_VERIFIED_exists']is False and facts['actor_ledger_parsed_exists']is False and facts['root_completion_adoption_pending']is True
for key in ['actual_append_acknowledged','full286_typed_prefix_preserved','published_record_and_metadata_exact','both_complete_public_payloads_equal_local','downloaded_source_ZIP_45_CRCs','all272_nonempty_data_C_values_unique','no_new_actor_or_service_calls']:assert facts[key]is True
for item in facts['external_inputs']:assert pin(Path(item['path']),item['sha256'])==item
secondary={}
for name,spec in SECOND_REVIEW_PINS.items():secondary[name]=pin(Path(spec['path']),spec['sha256']);assert secondary[name]==spec
secondcold,secondfacts=decoded_native(Path(SECOND_REVIEW_PINS['ROOT_separate_cold']['path']),SECOND_REVIEW_PINS['ROOT_separate_cold']['sha256'])
assert C(secondfacts)==C(SECOND_COLD_EXPECTED)
assert not(RT/'LEDGER_VERIFIED.json').exists()and not(OUT/'ledger.parsed.json').exists()
assert len(list(RT.glob('LEDGER_APPEND_INTENT.json')))==1 and len(list(RT.glob('WRITE_stage_create_INTENT.json')))==1 and len(list(RT.glob('WRITE_stage_upload_*_INTENT.json')))==2
assert(RT/'WRITE_stage_update_INTENT.json').is_file()and(RT/'WRITE_publish_publish_INTENT.json').is_file()
gpath=P/'known23592692_operations21_authority01/ROOT_EXECUTION_ADOPTION21.json'
g=read(gpath,'bb7a8af3131f7244a9b5c7b68b1e0b870ccb10336e95642d12959e9f048bdd09')
def utc(s):
 t=datetime.datetime.fromisoformat(s.replace('Z','+00:00'));assert t.utcoffset()==datetime.timedelta(0);return t
for phase in facts['phase_originals']:assert utc(g['not_before'])<=utc(phase['before'])<=utc(phase['after'])<utc(g['expires_at'])
intent=read(RT/'LEDGER_APPEND_INTENT.json','fa72b5f4b46faaf7ce707046ec184d9626247c1d9952d6afba42e3c5b159f1d2')
ack=read(RT/'LEDGER_APPEND_ACKNOWLEDGED.json','f8c9dad35e72dfa3b302619a0570a74feb666cd26e24c45bc6dd34c0b982b76a')
response=read(RT/'LEDGER_APPEND_RESPONSE.json','36de7b610cf3ff13493cb6311dea41cf83a9ca71502e176db6bb08a14e6ee28a')
assert ack['request_sha256']==H(C(intent['request']))and ack['response_sha256']==H(C(response))
row=intent['values'];assert type(row)is list and len(row)==4 and all(type(x)is str for x in row)
assert row[0].startswith('30005455 / OWR-12697708-008:')and row[1]==''and row[2]=='https://doi.org/10.5281/zenodo.23592692'
sciencep=P/'ROOT_FINAL_JOINT_WHOLE20_SCIENTIFIC_SOURCE_AND_ACTION_REVIEW_ADOPTION.json'
science=read(sciencep,'96cb0f067e342578b7b4e426471da2308be62d8b6ea0c8ba51168eba8f0f0890')
joint=pin(P/'ROOT_FINAL_KNOWN21_JOINT_WHOLE_SCIENTIFIC_SOURCE_AND_ACTION_ADOPTION.json','fd82555ab54500650d131328c247b3d02b8dd745b21457debb7412e66d96f95b')
manifestp=P/'operations/proposed/preprint/zenodo-deposit.json'
manifest=read(manifestp,'0ca12e07eee0ed88da4f94b82a2404eed4341aaa1f08f9100ecb630014fed6fe')
pub=read(P/'known23592692_readonly_reconciliation06_postappend_public/ROOT_COMPLETE_PUBLIC_GET_ONLY_ACCEPTANCE.json','81d1302e754cb2c944503e26e10c1fcf69c4cda83a0d6473bcf44764aaaa815e')
assert pub['published']is True and pub['submitted']is True and pub['record']==23592692 and pub['concept']==23592691 and pub['owner']==1789874 and pub['doi_status']==200 and pub['doi_destination']=='https://zenodo.org/records/23592692'
expected=[{'name':'finite-warm-thresholds.pdf','bytes':91613,'sha256':'42c5c632de7e942df6b7c407fb95d877a165281f215e4aa7d1dfa862b08b2157','md5':'845715d7fffb5aba43baddb039692933'},{'name':'finite-warm-thresholds-source-and-verification.zip','bytes':211840,'sha256':'e92f6fa13245686525a0dd8fc4c5327bd03e58a1f02ae7dcae918668c16c5fee','md5':'513e0c50bc16dfe669473fb83695dbca'}]
assert[{k:f[k]for k in ['name','bytes','sha256','md5']}for f in pub['downloads']]==expected
for f in expected:
 b=(P/'operations/proposed/preprint'/f['name']).read_bytes();assert len(b)==f['bytes']and H(b)==f['sha256']and hashlib.md5(b).hexdigest()==f['md5']
checks={key:True for key in ['three_successful_actual_native_publication_phases','original_failed_postappend_actor_and_raw_streams_preserved','one_acknowledged_append_exact_request_response_and_ACK','fresh_GET_only_full43_pair_metadata_values_FORMULA_readback','all286_prior_rows_and_full_raw_metadata_preserved','unique_canonical_literal_and_record_concept_row287','all272_nonempty_data_C_values_unique','fresh_complete_published_native_core_phase_UI_and_file_identity_verified','both_complete_public_payloads_match_reviewed_local_PDF_ZIP','DOI200_exact_published_record_destination','unchanged_scientific_package_and_source21_provenance_bound','two_independent_actual_readonly_proofs_and_ROOT_colds_adopted','no_actor_retry_second_create_or_base_LEDGER_certificate_fabrication']}
receipt={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':1131,'problem_id':'30005455','title':manifest['metadata']['title'],'doi':'10.5281/zenodo.23592692','record':23592692,'concept':23592691,'owner':1789874,'url':'https://zenodo.org/records/23592692','complete':True,'merge_commit':'67915a3df87d3bdd19be74ac04b1a39fd0ce89f3','integrated_head':'9601e1e768c94522bc8ad105db4dfae4770bad75','ledger_row':287,'ledger_new_row':True,'ledger_new_four_literal_cells':row,'canonical_manifest':str(manifestp.relative_to(R)),'canonical_manifest_sha256':H(manifestp.read_bytes()),'qualified_theorem':science['mathematical_scope'],'scope_limits':'No stochastic equality alpha=4/3, sharp whisker interval, infinite graphs, noninteger or zero initial-count claim. Published stochastic support/convergence and earlier bounds credited.','priority':science['priority'],'ai_and_preprint_disclosures':'Extensive AI research, proof development, computational verification, literature investigation, manuscript preparation and adversarial auditing. Unrefereed preprint; no formal independent human peer review or proof-assistant certification.','actual_effect_counts':{'new_deposition_POST':1,'PDF_PUT':1,'source_ZIP_PUT':1,'metadata_PUT':1,'publication_POST':1,'atomic_ledger_append':1},'public_download_payloads':expected,'doi_destination':pub['doi_destination'],'required_native_checks':checks,'scientific_and_base_whole_review_adoption':pin(sciencep),'actual_source21_joint_adoption':joint,'actual_ROOT_execution_adoption':pin(gpath),'publication_verification_mode':'EXTERNAL_GET_ONLY_READBACK_AFTER_ACKNOWLEDGED_APPEND_AND_PRESERVED_ACTOR_POSTWRITE_FRESHNESS_FAILURE','successful_actor_actions':3,'all_four_actor_actions_succeeded':False,'ledger_actor_returncode':1,'ledger_actor_certification':False,'base19_LEDGER_VERIFIED_exists':False,'actor_ledger_parsed_exists':False,'append_attempts':1,'append_retries':0,'future_service_write_allowance':0,'original_failed_ledger_parent':pin(P/'root_actual21_known23592692_activation01/ROOT_ledger_ORIGINAL_PARENT_NATIVE.json','abdd342f0ca42d24c8fc11adec93aa356bdb97bba93073830c7a0f60e77af605'),'postappend_failure':'At the retained ledger child finish12:34:19.937837UTC, original public.at12:31:14.571709UTC was185.366128s old. The actual lifecycle19.py line569 final_facts guard reported Expired/future observation under its180s default, after acknowledged append and immediate full287 preservation; the exact guard evaluation timestamp was not logged. No original freshness threshold, timestamp, stream, returncode or certificate was changed.','dated_observations':{'sheet_original_full43_reads':facts['full287_original_native_observations'],'sheet_observed_at_is_start':True,'public_readback_completed_at':facts['latest_public_original_after'],'separate_dated_observations_not_original_Source19_facts_fresh_bundle':True,'no_atomic_cross_service_claim':True},'sheet_representation_qualification':facts['representation_qualification'],'original_Completion05_permanently_inapplicable':True,'independent_external_actual_proof':pin(A/'final_reconciliation_new_independent_adversary01/NATIVE_ACTUAL1131_READONLY_RECONCILIATION_ORIGINAL_TRANSPORT03.json','428d19f2f9284b0147585d63cfc6eef68c161e9d78db48e972024a847428abe2'),'ROOT_external_proof_separate_cold':pin(coldp),'independent_complete_postappend_review':secondary,'read_only_public_acceptance':pin(P/'known23592692_readonly_reconciliation06_postappend_public/ROOT_COMPLETE_PUBLIC_GET_ONLY_ACCEPTANCE.json'),'evidence':facts['external_inputs'],'no_GitHub_release_or_duplicate_record_created':True,'final_global_reconciliation_complete':False,'overall_percent':97}
D=P/'get_only_external_completion_candidate02'
assert not(R/'PR1131_PUBLICATION_VERIFICATION.json').exists()and not D.exists()
D.mkdir(mode=0o700)
candidate={'kind':'ROOT_EXTERNAL_COMPLETION_RECEIPT_DATA_JOIN_CANDIDATE_NOT_R_COMPLETION','at':receipt['at'],'receipt':receipt,'ROOT_final_adoption_pending':True,'no_R_completion_receipt_written':True,'no_actor_or_service_calls':True,'no_base_LEDGER_VERIFIED_created':True}
out=D/'ROOT_CANDIDATE_RECEIPT.json';b=(json.dumps(candidate,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
with out.open('xb')as f:os.fchmod(f.fileno(),0o600);f.write(b);f.flush();os.fsync(f.fileno())
print(json.dumps({'candidate':pin(out),'actual_service_writes':0,'R_receipt_written':False,'root_adoption_pending':True}))
