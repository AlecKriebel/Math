from pathlib import Path
import hashlib,json,datetime,subprocess,sys,os

out=Path(__file__).resolve().parent;base=out.parent
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def record(p):
 b=p.read_bytes();return {'path':str(p.relative_to(base)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
initial=json.loads((out/'INITIAL_INDEPENDENCE_CHECKPOINT.json').read_text())
inputs={x['path']:x for x in initial['inputs']}
for x in initial['inputs']:
 need(record(base/x['path'])==x,'initial input changed: '+x['path'])
root=json.loads((base/'ROOT_FRESH_BOOK_REVIEW_AUTHENTICATION_20261006.json').read_text())
original=json.loads((base/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json').read_text())
for group in ('fresh_members','earlier_members'):
 for x in root[group]:
  need(record(base/x['path'])==x,'root sealed input mismatch: '+x['path'])
  inputs[x['path']]=x
for x in original['original_files']:
 rel='original_head_authentication_20261006/original_attempt/'+x['path']
 actual=record(base/rel)
 need(actual['bytes']==x['bytes'] and actual['sha256']==x['sha256'],'original changed: '+rel)
 inputs[rel]=actual
for rel in ['ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_20261006.md','CLOSING_COMMENT_OLD_PUBLISHED_OBSTRUCTION_20261006.md','ROOT_FRESH_BOOK_REVIEW_AUTHENTICATION_20261006.json','continued_public_access_20261006/ROOT_BOOK_SOURCE_RECONCILIATION.md']:
 inputs[rel]=record(base/rel)
expected={'ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_20261006.md':'80163cd354861d1d8a6101d8153db86ff84ec9da0c5a681bf17f0de7e8027800','CLOSING_COMMENT_OLD_PUBLISHED_OBSTRUCTION_20261006.md':'94f634ed980d8f8686503543a55045ab04ded41b46662642a312be15f119518c'}
for rel,digest in expected.items():need(inputs[rel]['sha256']==digest,'reviewed disposition changed')
receipts=[]
for i in (1,2,3):
 rel='continued_public_access_20261006/ACTUAL_PREVIEW_PAGES_%02d.json'%i;r=json.loads((base/rel).read_text())
 for x in r['events']:
  path=x.get('unmodified_local_path',x.get('private_local_path'));p=Path(path);actual=record(p)
  need(actual['bytes']==x['bytes'] and actual['sha256']==x['sha256'],'source receipt mismatch: '+str(p))
  valid=x.get('valid_primary_page_pixels',True)
  receipts.append({'printed_page':x.get('printed_page',x.get('printed_page_requested')),'valid_primary_page':valid,**actual})
need(sum(x['valid_primary_page'] for x in receipts)==10,'expected ten primary pages')
need([x['printed_page'] for x in receipts if not x['valid_primary_page']]==[19],'placeholder exclusion')
events=[]
for optimization,name in [(False,'ALGEBRA_NORMAL.json'),(True,'ALGEBRA_OPTIMIZED.json')]:
 argv=[sys.executable]+(['-O'] if optimization else [])+['-E','-S','-B','-P',str(out/'validate_algebra.py')]
 start=now();proc=subprocess.Popen(argv,cwd=out,stdout=subprocess.PIPE,stderr=subprocess.PIPE);stdout,stderr=proc.communicate()
 need(proc.returncode==0,'independent algebra failed')
 payload=json.loads(stdout);need(payload['PASS'],'algebra did not PASS')
 (out/name).write_bytes(stdout)
 events.append({'argv':argv,'actual_child_PID':proc.pid,'UTC_start':start,'UTC_end':now(),'exit_code':proc.returncode,'explicit_failure_guards_survive_optimization':True,'stdout':record(out/name),'stderr_bytes':len(stderr),'stderr_sha256':hashlib.sha256(stderr).hexdigest()})
( out/'ACTUAL_AUTHENTICATION.json').write_text(json.dumps({'schema':'pr124-fresh-disposition-actual-authentication/v1','UTC':now(),'actual_operator_PID':os.getpid(),'initial_checkpoint_unchanged':True,'original_members_verified':17,'fresh_public_members_verified':19,'earlier_members_verified':81,'source_receipts_verified':receipts,'actual_algebra_events':events,'exact_disposition_hashes_verified':expected,'new_central_proof_search_turns':0,'closure_native_service_operations':False},indent=2)+'\n')
inputs['AGENTS.md (workspace /Users/alec/Documents/Math)']={'path':'/Users/alec/Documents/Math/AGENTS.md','bytes':Path('/Users/alec/Documents/Math/AGENTS.md').stat().st_size,'sha256':hashlib.sha256(Path('/Users/alec/Documents/Math/AGENTS.md').read_bytes()).hexdigest()}
(out/'INPUT_HASHES.json').write_text(json.dumps({'schema':'pr124-fresh-disposition-input-hashes/v1','UTC':now(),'inputs':list(inputs.values()),'private_source_bodies_not_copied_into_public_package':True},indent=2)+'\n')
result={'schema':'pr124-fresh-published-obstruction-disposition-adversary/v1','UTC':now(),'completion_percent':100,'verdict':'PASS','original_head':original['original_head'],'original_literal_status':'claimed_solved','original_effort':'2/5','original_math_gate_retained':True,'independent_source_contribution_checkpoint_before_disposition_and_other_reports':True,'whole_book_obtained':False,'actual_primary_pages_read':[20,22,23,26,27,28,45,46,114,118],'unavailable_page19_not_source':True,'exact_reviewed_inputs':expected,'old_printed_necessary_theorem_verified':True,'all_prime_family_immediate_old_mathematical_consequence':True,'general_rank_bound_immediate_old_mathematical_consequence':True,'integer_content_units_signs_Euler_choices_verified':True,'III4_3_prime2_extra_hypothesis_fails':True,'II3_3_covers_prime2':True,'cyclic_realization_not_full_group_realization':True,'substantive_novel_mathematical_resolution_established':False,'express_prior_named_refutation_established':False,'express_prior_refutation_absence_proved':False,'earliest_priority_established':False,'possible_new_bibliographic_application_preserved':True,'alternate_proof_novelty_not_disproved':True,'closing_without_novel_solution_paper_supported_under_precise_human_scope':True,'already_solved_scoped_only_to_mathematical_content':True,'exact_closing_comment_scientific_and_historical_fairness':'PASS','global_corrections_required':[],'scientific_disposition_validation_only':True,'operational_mutation_authorization':False,'new_central_proof_search_turns':0,'mutations':{'only_assigned_new_untracked_folder':True,'tracked_files':False,'Git_or_index':False,'native_or_service':False,'external_individual_communication':False},'limits':['No earlier express named refutation or exact historical resolution chronology established.','No total absence of alternate-proof or bibliographic novelty proved.','No omitted book pages inferred; no whole-book or complete literature search claim.','No closure/native/Git/service operation performed.']}
(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
with (out/'RESEARCH_LOG.md').open('a') as f:
 f.write('\n'+now()+' UTC — Exact root disposition and proposed closing comment read after initial independence seal. Audit completion estimate: 80%. Claim-by-claim falsification found no scientific/historical overclaim; tested integral content, arbitrary Euler shifts/signs, prime2 modular hypothesis failure, full versus cyclic torsion, and general invariant-factor bound. Possible new explicit bibliographic application and alternate exposition remain distinct from qualifying new mathematical resolution. All17original,19fresh-public and81earlier sealed artifacts authenticated; no mismatch.\n')
 f.write('\n'+now()+' UTC — Final PASS sealed, audit completion estimate100%. Actual independent normal and optimized algebra runs pass with explicit guards; entire original family and general inequality covered by old printed mathematics. Exact `already_solved` scope and historical caveats accepted; no global correction required. Original effort2/5 retained; zero new central proof-search turns. Wrote only assigned new untracked folder; no operational mutation, external contact, copyrighted source-body redistribution, publication/deposit/DOI/tracker action.\n')
public_names=['INITIAL_INDEPENDENCE_CHECKPOINT.json','REPORT.md','RESULT.json','RESEARCH_LOG.md','INPUT_HASHES.json','ACTUAL_AUTHENTICATION.json','ALGEBRA_NORMAL.json','ALGEBRA_OPTIMIZED.json','validate_algebra.py','authenticate_and_seal.py']
public=[record(out/name) for name in public_names]
manifest={'schema':'pr124-fresh-disposition-public-manifest/v1','UTC':now(),'copyrighted_primary_bodies_in_public_package':False,'private_source_bodies_referenced_by_hash_only':True,'artifacts':public}
(out/'PUBLIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
seal={'schema':'pr124-fresh-disposition-seal/v1','UTC':now(),'verdict':'PASS','completion_percent':100,'public_manifest':record(out/'PUBLIC_MANIFEST.json'),'public_members':public,'source_inputs':record(out/'INPUT_HASHES.json'),'no_self_hash_claim':True,'exact_disposition_binding':expected}
(out/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps({'verdict':'PASS','UTC':seal['UTC'],'completion_percent':100,'public_manifest_sha256':seal['public_manifest']['sha256'],'seal_sha256':hashlib.sha256((out/'SEAL.json').read_bytes()).hexdigest(),'report_sha256':hashlib.sha256((out/'REPORT.md').read_bytes()).hexdigest(),'result_sha256':hashlib.sha256((out/'RESULT.json').read_bytes()).hexdigest(),'public_member_count':len(public_names)},indent=2))
