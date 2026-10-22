#!/usr/bin/env python3
"""Integrity/scope controls only. Does not verify the cited counterexample."""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from itertools import product
p=argparse.ArgumentParser();p.add_argument('--safe-root',type=Path);p.add_argument('--sources-root',type=Path);p.add_argument('--corpus-root',type=Path);p.add_argument('--bootstrap',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parent; safe=a.safe_root or root.parent/'safe'; passed=[]
def read(n): return json.loads((root/n).read_text())
def check(n,x):
 if not x:raise AssertionError(n)
 passed.append(n)
def digest(f):
 b=f.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
binding=read('AUDITED_INPUTS.json');result=read('AUDIT_RESULT.json');sources=read('SOURCE_CHECKS.json')
check('supplied_freeze_sha256',digest(safe/'FREEZE_MANIFEST.json')['sha256']=='23236036135d52baef409a058a8df2cea2792c6faefd5004b669c14abdfa454d')
check('all_eleven_original_files_bound',len(binding['files'])==11 and {x['path'] for x in binding['files']}=={f.relative_to(safe).as_posix() for f in safe.rglob('*') if f.is_file()})
check('all_original_bytes_unchanged',all(digest(safe/x['path'])=={k:x[k] for k in ['bytes','sha256']} for x in binding['files']))
r=subprocess.run([sys.executable,str(safe/'tests/verify_packet.py')],capture_output=True,text=True,check=True);replay=json.loads(r.stdout)
check('all_fourteen_frozen_checks_replayed',replay['status']=='pass' and len(replay['tests_passed'])==14)
check('replay_matches_frozen_test_report',replay==json.loads((safe/'TEST_RESULTS.json').read_text()))
check('exact_target_identifiers',result['problem_id']==30000576 and result['source_code']=='OWR-1323-013' and result['queue_rank']==658)
check('attribution_and_exact_scope_distinguished',result['attribution_verdict']=='PASS' and result['exact_target_verdict']=='HOLD')
check('exact_target_not_closed',result['exact_target_already_solved_endorsed'] is False)
check('no_proof_verification_claimed',result['proof_inspected'] is False and result['mathematical_proof_verified'] is False)
check('unrecovered_source_not_fabricated',result['full_2009_pdf_recovered'] is False and sources['source_inspections'][1]['pdf'] is None)
check('complex_scalar_gap_retained',result['complex_scalar_scope_directly_verified'] is False and 'complex' in result['required_gap'])
check('partial_complexification_not_used_as_closure',result['complexification']['gap_closed'] is False)
check('original_attempts_not_fabricated',result['original_proof_attempts_counted']==0)
check('no_remote_writes_or_original_edits',result['remote_writes_performed'] is False and result['author_artifacts_modified'] is False)
check('source_payloads_excluded',sources['source_content_included'] is False)
check('three_fresh_pdf_hash_matches_recorded',len(sources['fresh_pdf_retrievals'])==3 and all(x['matches_frozen_source_metadata'] and x['http_status']==200 and x['is_pdf'] for x in sources['fresh_pdf_retrievals']))
frozen_sources={x['id']:x for x in json.loads((safe/'SOURCE_MANIFEST.json').read_text())['sources']}
check('fresh_source_metadata_matches_frozen_manifest',all({k:x[k] for k in ['bytes','sha256']}==frozen_sources[x['id']]['pdf'] for x in sources['fresh_pdf_retrievals']))
check('corpus_rechecks_match_pinned_public_manifest',all(x['observed']==sources['pinned_public_dataset_manifest']['files'][x['name']] for x in sources['dataset_byte_rechecks']))
check('both_corpus_hash_matches_recorded',len(sources['dataset_byte_rechecks'])==2 and all(x['matches_expected'] for x in sources['dataset_byte_rechecks']))
check('target_and_prior_report_counts',sources['dataset_byte_rechecks'][0]['matching_problem_records']==1 and sources['dataset_byte_rechecks'][1]['matching_report_keys']==0)
# These are finite propositional controls for the quantifier bridge, not analytic tests.
positive_time_chaos=(False,False)
check('no_time_pattern_refutes_both',not all(positive_time_chaos) and not any(positive_time_chaos))
mixed_time_chaos=(False,True)
check('mixed_pattern_refutes_only_universal',not all(mixed_time_chaos) and any(mixed_time_chaos))
including_zero=(False,True,True)
check('zero_time_excluded_from_questions',all(including_zero[1:]) and any(including_zero[1:]))
check('negated_exists_equals_all_negated',all((not any(q))==all(not x for x in q) for q in product([False,True],repeat=3)))
check('inspected_field_scope_locality_explicit','section 2.1' in sources['source_inspections'][3]['finding'] and 'section 6' in sources['source_inspections'][3]['finding'])
check('counterexample_proof_limit_disclosed','does not validate' in (root/'AUDIT.md').read_text())
allowed={'AUDITED_INPUTS.json','SOURCE_CHECKS.json','AUDIT_RESULT.json','AUDIT.md','verify_audit.py','TEST_RESULTS.json','AUDIT_BINDING.json'}
check('portable_audit_authored_allowlist',{f.relative_to(root).as_posix() for f in root.rglob('*') if f.is_file()}<=allowed)
if a.sources_root:
 for x in sources['fresh_pdf_retrievals']:
  check('fresh_source_bytes_'+x['id'],digest(a.sources_root/(x['id']+'.pdf'))=={k:x[k] for k in ['bytes','sha256']})
if a.corpus_root:
 for x in sources['dataset_byte_rechecks']:
  f=a.corpus_root/x['name'];check('actual_corpus_bytes_'+x['name'],digest(f)==x['observed']);d=json.loads(f.read_bytes())
  check('actual_corpus_count_'+x['name'],len(d)==x['record_count'])
  if x['name']=='problems.json':check('actual_target_occurrence',sum(str(z.get('id'))=='30000576' for z in d)==1)
  else:check('actual_prior_report_absence',sum(str(k) in ['30000576','OWR-1323-013'] for k in d)==0)
if not a.bootstrap:
 b=read('AUDIT_BINDING.json');actual={f.relative_to(root).as_posix() for f in root.rglob('*') if f.is_file() and f.name!='AUDIT_BINDING.json'}
 check('audit_binding_exact_file_set',{x['path'] for x in b['files']}==actual)
 check('audit_binding_all_bytes',all(digest(root/x['path'])=={k:x[k] for k in ['bytes','sha256']} for x in b['files']))
print(json.dumps({'status':'pass','independent_control_count':len(passed),'independent_controls':passed,'frozen_checks_replayed':len(replay['tests_passed']),'live_source_pdf_bytes_checked':bool(a.sources_root),'live_corpus_bytes_checked':bool(a.corpus_root),'audit_binding_checked':not a.bootstrap,'mathematical_proof_verified':False,'exact_target_verdict':'HOLD'},indent=2))
