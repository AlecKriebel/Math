#!/usr/bin/env python3
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=BASE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
now=dt.datetime.now(dt.timezone.utc).isoformat()
bind=read(HERE/'INPUT_BINDING.json')
for path,item in bind['all_input_files'].items():
    assert sha(ROOT/path)==item['sha256'],path
assert sha(HERE/'FIRST_PASS.md')==read(HERE/'FIRST_PASS_SEAL.json')['first_pass_sha256']
assert sha(BASE/'reviewed_candidate/PARTIAL_RESULTS.md')==bind['candidate_proof_sha256']
assert sha(BASE/'reviewed_candidate/MANIFEST.json')==bind['candidate_manifest_sha256']
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
replay=read(HERE/'REPRODUCTION.json')
assert replay['all_math_fields_equal'] and replay['all_inputs_untouched']
assert [r['assertions'] for r in replay['replays']]==[135,6,10351,99,35]
fresh=read(HERE/'FALSIFICATION_RESULTS.json')
assert fresh['status']=='passed' and fresh['assertions']==89

verdict={'completed_at_utc':now,'audit_completion_percent':100,'target':'30000224 / OWR-824-008','pr':17,
 'candidate_commit':'2db4c39ced71a0f25beeb50e6466628a83303149',
 'candidate_proof_sha256':bind['candidate_proof_sha256'],'candidate_manifest_sha256':bind['candidate_manifest_sha256'],
 'original_frozen_head':bind['frozen_head'],'original_proof_sha256':'8d6995c10f48640f33afc5a437766eaccead99808e7b3c7f770bb52a8e900444',
 'verdict':'PASS_CURRENT_RESTRICTED_PARTIAL; FAIL_UNRESTRICTED_RESOLUTION',
 'mandatory_candidate_corrections':[],'fatal_mathematical_findings':[],
 'exact_target_preserved':'Any ideal b, no homogeneity requirement, radical a, global Cohen-Macaulay quotient, arbitrary characteristic-zero K',
 'strongest_verified':['No binomial CM thickening over any characteristic-zero field','No arbitrary CM thickening containing actual q=wz-xy','Generic length one impossible without homogeneity','Homogeneous generic length two impossible; conormal O(-7)^2 gives at least11 quadratic sections versus10','Both CI linkage colons hold; no unconditional preservation follows','At the vertex: H1 depth0, Z1 depth3, B1 depth1, Z2 depth2 and pdim2; Hassanzadeh cycle/SD hypotheses fail under all generator padding'],
 'exact_remaining_gap':'Non-binomial a-primary b with nonzero nilpotent q; homogeneous generic length>=3, arbitrary nonhomogeneous generic length>=2. No construction or universal exclusion, and no CM-preserving homogenization reduction.',
 'original_target_solved':False,'original_attempts_used':4,'original_attempt_limit':5,'new_central_attempt_consumed':False,
 'historical_review_transferred_to_current_hash':False,'new_independent_first_pass_sealed_before_old_or_sibling_conclusions':True,
 'original14file_snapshot_verified':True,'all154_inputs_untouched':True,'geometry_cache_relocation_hashes_verified':True,
 'author_assertions_reproduced':135,'historical_groups_reproduced':6,'new_family_assertions_reproduced':[10351,99,35],
 'fresh_exact_falsification_assertions':89,'fresh_exact_falsification_groups':7,
 'full_relevant_primary_preprint_theorem_proofs_checked':True,'Hassanzadeh_complete_published_version_compared':False,
 'worldwide_openness_certified':False,'novelty_claim':False,'human_peer_review_or_formal_certification':False,
 'actual_main_queue_during_audit':'queued0/5, expected before parent integration after PR16','proposed_integrated_disposition':'unsolved4/5 / partial_stalled',
 'integration_required':['After PR16 in authorized order','Final integrated proof/hash binding; current pending/workflow status updated without altering historical records','Canonical queue unsolved4/5, original turns preserved without reset','Final PR metadata accurately describes clarified partial result; historical REVIEW not repurposed','No paper, deposit, DOI or tracker promotion; preserve source-access and scope qualifications'],
 'optional_improvements':['Add a short pointer to universal generator-padding proof','Label preserved historical date/branch/readiness fields even more visibly','Minor line wrapping/spacing'],
 'audit_writes_restricted_to':str(HERE.relative_to(ROOT)),'git_or_live_PR_mutations_by_this_auditor':False,
 'canonical_or_candidate_or_environment_mutations_by_this_auditor':False,'external_individual_contacts':False,
 'paper_or_deposit_or_tracker_created':False,'report_sha256':sha(HERE/'REPORT.md')}
(HERE/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
with (HERE/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'\n- {now} — 100% complete. Fresh complete current-hash audit passes restricted partial content and unsolved disposition, fails unrestricted resolution gate. No mandatory candidate correctness correction. Every154 bound input remains unchanged; original14 files and4/5 ledger preserved. Source loci/version metadata and full relevant preprint proofs checked; no complete published Hassanzadeh text comparison, no worldwide-open or novelty claim. Parent integration after PR16 must update final current gate/hash/queue metadata; no merge, paper, deposit, tracker, outreach, or new central proof attempt by auditor.\n')
files=sorted(p for p in HERE.rglob('*') if p.is_file() and 'tmp' not in p.relative_to(HERE).parts and p.name!='MANIFEST.json')
manifest={'created_at_utc':now,'self_hash_policy':'MANIFEST excludes itself; all public audit artifacts included; ignored tmp execution/source files are bound by evidence receipts and INPUT_BINDING',
 'input_binding_sha256':sha(HERE/'INPUT_BINDING.json'),'candidate_proof_sha256':bind['candidate_proof_sha256'],
 'candidate_manifest_sha256':bind['candidate_manifest_sha256'],
 'files':{str(p.relative_to(HERE)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in files}}
(HERE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert all(sha(HERE/path)==item['sha256'] for path,item in manifest['files'].items())
print(json.dumps({'verdict':verdict['verdict'],'mandatory_corrections':0,'artifacts':len(files),'manifest_sha256':sha(HERE/'MANIFEST.json'),'report_sha256':sha(HERE/'REPORT.md'),'audit_completion_percent':100},indent=2))
