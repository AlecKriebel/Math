"""Prepare a reviewable prospective credited finding; never writes live queue/state."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_text())
dump=lambda p,x:p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
snapshot=HERE/'source_snapshot'; sm=load(HERE/'snapshot_manifest.json')
original=[]
for z in sm['files']:
    b=(snapshot/z['path']).read_bytes()
    gb=subprocess.check_output(['git','show',sm['head']+':unsolved_math_prioritization/attempts/7000004/'+z['path']],cwd=ROOT)
    assert len(b)==z['size'] and sha(b)==z['sha256'] and b==gb,z['path'];original.append(z)
assert len(original)==16
diff=(HERE/'pr_input/diff.patch').read_bytes() if (HERE/'pr_input/diff.patch').exists() else None
orig_ready=load(snapshot/'readiness.json')
source=load(snapshot/'source_record.json');prior=load(snapshot/'prior_report.json')
assert orig_ready['review_hash']==sha(json.dumps([source,prior],sort_keys=True).encode())
assert orig_ready['statement_hash']==sha(source['statement'].encode())
old_review=sha((snapshot/'review/REVIEW.md').read_bytes())
assert load(snapshot/'review/verdict.json')['review_sha256']==old_review
for receipt in ['ROOT_DIFFERENTIAL_NEW_ACTUAL_REPLAY.json','ROOT_REMAINING_FAMILY_REPRODUCTION.json']:
    load(HERE/receipt)
dump(HERE/'ROOT_ORIGINAL_AND_CURRENT_SCOPE_VERIFICATION.json',{'utc':NOW,'original_git_members_verified':16,'actual_head':sm['head'],'actual_base':sm['base'],'full_raw_source_pair_hash':orig_ready['review_hash'],'old_review_document_hash':old_review,'distinct_hash_roles_valid':True,'old_artifact_sha256':sha((snapshot/'OBSTRUCTION.md').read_bytes()),'all_original_programs_actual_byte_exact':'ROOT_DIFFERENTIAL_REPLAY_COMPARISON_FAILURE.json diagnostic and ROOT_REMAINING_FAMILY_REPRODUCTION.json actual primary family replay','new_differential_actual_byte_exact':'ROOT_DIFFERENTIAL_NEW_ACTUAL_REPLAY.json','all_remaining_actual_family_replays':'ROOT_REMAINING_FAMILY_REPRODUCTION.json','initial_root_AssertionError_preserved':True,'initial_AssertionError_precise_phase_recovered':False,'scope':'Original bytes and source hash roles correct. Original unsolved scope is superseded, not promoted by its old partial verdict.','workflow_completion_estimate_percent':65})
current=HERE/'reviewed_candidate';assert not current.exists(),'Never overwrite a frozen candidate; create a revision explicitly.'
current.mkdir();shutil.copytree(snapshot,current/'original_archive')
for name in ['source_record.json','prior_report.json','source_checksums.json']:
    shutil.copyfile(snapshot/name,current/name)
shutil.copyfile(HERE/'ROOT_UNIVERSAL_CERTIFICATE.md',current/'RESULT.md')
shutil.copyfile(HERE/'differential_family/COUNTERMODEL_DERIVATION.md',current/'COUNTERMODEL_DERIVATION.md')
shutil.copyfile(HERE/'differential_family/UNIVERSAL_LOCAL_PROOF.md',current/'CURRENT_LOCAL_PROOF.md')
shutil.copyfile(HERE/'differential_family/exact_controls.py',current/'verify.py')
shutil.copyfile(HERE/'differential_family/exact_results.json',current/'exact_results.json')
shutil.copyfile(HERE/'linking_family/CANDIDATE_LINKING_CERTIFICATE.md',current/'INDEPENDENT_LINKING_CERTIFICATE.md')
original_turns=(snapshot/'turns.jsonl').read_bytes();assert len(original_turns.splitlines())==1
turn2={'turn':2,'timestamp':NOW,'mechanism':'New wavy-circle counterexample route, initially charged by ROOT_COUNTEREXAMPLE_CHECKPOINT.md; derive globally injective compatible unit binormal and explicit disk separation.','outcome':'complete_literal_counterexample_credited_prior_construction','artifact':'RESULT.md','completion_estimate_percent':65,'remaining_gap':'No mathematical gap in the literal counterexample or positive prior specialization; NEW whole current adversarial gate and guarded acceptance integration pending. The later strictly negative curvature question is outside the target.','model':'Codex parent agent; model identifier not exposed in this runtime','reasoning_effort':'Not independently exposed in this runtime','original_charge_checkpoint':'ROOT_COUNTEREXAMPLE_CHECKPOINT.md','accounting':'One new substantive research route; independent audit/reproduction adds zero.'}
(current/'turns.jsonl').write_bytes(original_turns+(json.dumps(turn2,ensure_ascii=False)+'\n').encode())
assert (current/'turns.jsonl').read_bytes().startswith(original_turns)
body='''## Credited counterexample to the literal 2019 question

Ghomi Problem 1.4 admits the embedded curve Gamma(t)=(cos t,sin t,cos(2t)/4). Its unit Frenet binormal B=(-cos^3 t,sin^3 t,1)/sqrt(1+cos^6 t+sin^6 t) is smooth and globally injective. For every 0<epsilon<1/3, Gamma+epsilon B is embedded, disjoint from Gamma, and has linking number zero, as proved by an explicit orientation-preserving shear and spanning disk.

The construction is exactly a positive scaling of the printed section 2 curve in Ni, Zhang and Zhang, On questions of Pogorelov and Toponogov, arXiv:2606.29231v1 (2026-06-28). The linking conclusion is our verified elementary consequence of that prior construction; it is not represented as an explicit theorem or Ghomi citation in that paper. Earliest historical recognition is unestablished. Proposed outcome: already_solved, accepted credited partial finding; no new paper, DOI or tracker row.

B has four stationary points, so this does not answer Ghomi–Raffaelli's later strictly negative surface curvature question. Source-qualified original conditional facts remain archived. The original partial review and local checks do not certify the new result.

Two substantive attempts used in total: original1 plus new counterexample route1; verification0. Three distinct mathematical/source approach families and actual root reproduction are complete. NEW complete revised-packet adversarial gate is pending. AI tools were used extensively; this is unrefereed AI-audited documentation, not external human peer review or formal proof-assistant verification.
'''
(current/'pr_body.md').write_text(body)
(current/'README.md').write_text('''# 7000004 / AMR-069-0004: credited literal counterexample

Read RESULT.md for the complete proof, exact earlier-construction specialization and scope. The proposed outcome is already_solved, accepted as a credited partial research finding. The literal 2019 universal assertion is false even for an embedded positive-curvature curve with smooth injective unit binormal. No novel preprint, new DOI or tracker row is proposed.

The binormal has four stationary points. The later strictly negative surface curvature question is outside this finding. All original16 artifacts remain byte-exact in original_archive/; their dated unsolved disposition and partial verdict are superseded and are not transferred to this result. Current source_record.json and prior_report.json preserve the entire original raw records, including outdated upstream status, which does not determine the present disposition.

Reproduce the supplemental exact algebra using /usr/bin/python3 verify.py with SymPy1.14.0; it writes exact_results.json beside the program. The complete proof supplies all universal claims. For private reproduction, copy the program before running it. Original local-only diagnostics remain in original_archive/ and do not certify current prose, global linking or priority.

Total substantive budget2/5. Fresh complete current-packet adversarial review and guarded accepted integration remain pending. See readiness.json, current_status.json and CURRENT_PROOF_DEPENDENCIES.json. AI tools were extensively used; no external human review or formal verification is claimed.
''')
(current/'OBSTRUCTION.md').write_text('''# Current disposition of the former obstruction

The original unsolved obstruction is superseded by the complete credited counterexample in RESULT.md. Its exact original text, local verification programs, dated readiness, review and turn1 remain in original_archive/. CURRENT_LOCAL_PROOF.md reconstructs the valid conditional statements, retaining the regular-binormal hypothesis and the absolute torsion sign convention. No old partial PASS is transferred to the present finding.

The literal 2019 target is answered negatively as an elementary consequence of the prior June2026 printed construction. The later strictly negative surface curvature question remains outside this target. Current outcome proposedalready_solved; total2/5; NEW whole review pending; no paper, DOI or tracker row.
''')
(current/'CURRENT_SOURCE_QUALIFICATION.md').write_text('''# Source and review-role qualification

The source is the actual 2019 Ghomi Problem1.4, printed p6. Its continuous injective binormal hypothesis must not be silently strengthened to regular B. Our unit, compatible, smooth example avoids the normalization/immersed-linking ambiguities.

Positive prior: Ni–Zhang–Zhang arXiv2606.29231v1, submitted2026-06-28, section2 printedpp2–3, exact graph and closed curves. RESULT.md proves their equivalence and the elementary zero-linking consequence; the paper does not explicitly name this binormal question or state that linking conclusion. Root fresh PDF329660B SHA0ec8ff7da6224ece69f2beee6e71a39697a2fbc4a0aacb01b384755e69f9bbd2. No certification of that paper's unrelated theorems, worldwide priority or the strictly negative curvature question is made.

Original Ghomi–Raffaelli exactv2 PDF2769655B SHA1329d83437393ff0cf984466a28fc6cf384e8e5b1e38f1ef2a9fcb868e61489a was freshly retrieved and its complete applicable11-page text read. The author-hosted variant has a different date/hash and is not silently substituted. Regular-B differential identities are reconstructed with |tau| in spherical geodesic curvature, avoiding a signed-torsion convention being transferred without its orientation hypothesis. Example4.2 printed n1,n2 lack the notebook's /6 factors; root read the exact primary Second Example In[1] and z definition in notebook551710B SHA89791fab271dacd16351bd21c1162c02ecbe26ee506a0dbffd8d76cda03fbd5d. No independent notebook execution or global linking computation of that separate numerical example is claimed. None of these numerical examples are needed for our counterexample.

The original readiness.review_hash2e49912828f018ce3f85114143f107c8b3315172c5e5538a6231c128efb1d086 is the actual importer SHA256(json.dumps([full raw source,full separate prior report],sort_keys=True).encode()); statement_hash3fba262110a123ef34d75b5cac921d5d24b3964782b23c2618a9725ed6f04d93 binds the exact statement. The old verdict.review_sha2560d8a579e9273e3bd7e5bc170b7964b2754a0404896c35dc47e1512e4f46326a0 binds the separate old review document. These are valid distinct roles. The differential family's alleged stale source hash is withdrawn by its preserved additive qualification; its original incorrect report remains immutable and expressly superseded on this point. Never replace the source-pair hash by the review-document hash.

Brown/Banchoff's teaching page has an earlier-looking exact wavy-circle family, but Last-Modified metadata is not a verified historical publication date. The dated2026 primary construction suffices for current attribution. The original raw source and prior report remain byte-exact and their outdated partial/open summaries remain historical evidence only. All original partial readiness/review and old code are archived, not current complete-result certificates.

Root/source-family setup failures, the first root combined AssertionError of unrecovered precise phase, and all later actual successful unchanged replays are separately retained. No failed invocation is relabeled a pass. Source corpus/SQL and actual queue.score are read only; no legacy queue generator runs.
''')
q=ROOT/'unsolved_math_prioritization/QUEUE.md';before=q.read_bytes();lines=before.decode().splitlines(keepends=True)
header=next(z for z in lines if z.startswith('| Rank |'));names=[x.strip() for x in header.split('|')[1:-1]]
assert names==['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
rows=[z for z in lines if z.startswith('| 47 | 7000004 /')];assert len(rows)==1
row=rows[0];cells=row.split('|');assert len(cells)==14 and cells[8].strip()=='queued' and cells[9].strip()=='0/5' and not cells[10].strip() and not cells[11].strip() and not cells[12].strip()
findings='2026-10-02: Literal Ghomi2019 Problem1.4 has an embedded positive-curvature counterexample with smooth injective unit binormal and zero linking for every0<epsilon<1/3. Exact scaled specialization of Ni-Zhang-Zhang2026 section2; linking is a verified elementary consequence, not their printed theorem. Four binormal stationary points exclude the later strictly negative curvature question. Credited already_solved partial proposed after NEW whole review; substantive2/5, verification0; no paper/newDOI/tracker. PR: https://github.com/AlecKriebel/Math/pull/34.'
newcells=list(cells);newcells[8]=' already_solved ';newcells[9]=' 2/5 ';newcells[11]=' '+findings+' '
newrow='|'.join(newcells);after=before.replace(row.encode(),newrow.encode());assert after!=before
assert all(cells[i]==newcells[i] for i in range(14) if i not in [8,9,11])
dump(current/'CURRENT_QUEUE_PATCH.json',{'utc':NOW,'phase':'prospective only; no live writes before NEW complete gate','whole_queue_preimage_sha256':sha(before),'whole_queue_prospective_sha256':sha(after),'header_names':names,'row_before':row,'row_prospective':newrow,'allowed_named_changes':['Status','Turns','Findings'],'all_other_lines_and_fields_byte_preserved':True})
dump(current/'CURRENT_SOURCE_CONTEXT.json',{'utc':NOW,'id':7000004,'problem_number':source['problem_number'],'raw_source_sha256':sha((current/'source_record.json').read_bytes()),'raw_prior_report_sha256':sha((current/'prior_report.json').read_bytes()),'statement_hash':orig_ready['statement_hash'],'review_hash':orig_ready['review_hash'],'raw_imported_status':source['status'],'current_disposition_proposed':'already_solved','basis':'Fully proved negative answer from a dated earlier exact construction; earliest printed recognition unestablished.','original_head':sm['head'],'actual_base':sm['base'],'raw_record_and_report_unchanged':True,'narrower_negative_curvature_target_resolved':False,'paper_or_new_doi_or_tracker':False})
status={'utc':NOW,'id':7000004,'pr':34,'original_head':sm['head'],'current_gate':'pending_NEW_complete_whole_current_credited_counterexample_adversary','queue_status_proposed':'already_solved','original_budget':'1/5','new_substantive_attempts':1,'cumulative_attempts':'2/5','verification_attempts':0,'workflow_completion_estimate_percent':75,'literal_counterexample_complete':True,'positive_prior_equivalence_complete':True,'earliest_historical_recognition_established':False,'narrower_negative_curvature_target_resolved':False,'paper_doi_tracker':'none'}
dump(current/'current_status.json',status)
ready=dict(orig_ready);ready.update({'status':'current_packet_pending_NEW_complete_adversary','queue_outcome_requested':'already_solved','artifact':'RESULT.md','reviewed_artifact_sha256':sha((current/'RESULT.md').read_bytes()),'remaining_gap':'NEW complete current-packet adversarial gate and acceptance integration pending. No mathematical gap claimed in the literal counterexample; later negative-curvature target outside scope.','completion_estimate_percent':75,'independent_review':'Three distinct original-stage mathematical/source families plus root universal reconstruction and actual replays; these are not yet a NEW whole revised-packet verdict.','prior_attempt_gap':'Original route retained; new wavy-circle counterexample charged as second substantive attempt.','budget':dict(orig_ready['budget'],used_substantive_attempts=2,original_substantive_attempts=1,new_substantive_attempts=1,verification_attempts=0),'primary_sources':orig_ready['primary_sources']+[{'url':'https://arxiv.org/abs/2606.29231v1','location':'Section2 pp2–3 exact prior graph/curve; verified elementary binormal/linking consequence in RESULT.md'}],'positive_novelty_claim':False,'paper_or_new_doi_or_tracker':False})
dump(current/'readiness.json',ready)
log='''# Current research log: PR34 / 7000004

The exact original log and original turn1 are archived without edits. The appended turn2 preserves the original JSONL prefix, records the actual present timestamp, and points to the earlier preserved charging checkpoint rather than inventing a discovery time. New substantive counterexample route1; cumulative2/5; verification0.

'''+NOW+''' — workflow75%: three distinct closed families and root complete literal counterexample/prior equivalence verified. Actual original/differential/linking/source/hash-role replays pass with failures retained. Proposedalready_solved is credited earlier-construction partial, no paper/DOI/tracker. NEW whole current adversarial gate pending. Later strict-negative-curvature question outside scope. AI tools used extensively; unrefereed documentation.
'''
(current/'CURRENT_RESEARCH_LOG.md').write_text(log);(current/'RESEARCH_LOG.md').write_text(log)
(current/'CURRENT_AUDIT_SCOPE.md').write_text('''# Complete revised-packet gate required

This packet binds the original16 artifacts, immutable differential24/linking39/primary17 families, additive hash-role6 qualification, their manifests, root universal/source/reproduction receipts and original Git metadata in CURRENT_PROOF_DEPENDENCIES.json. The new current result has not yet passed a complete revised-packet adversary. Old partial/family verdicts are not transferred. All current math, exact literal source hypotheses, prior equivalence, scope, status/body/queue metadata, both distinct source/document hashes and cumulative2/5 ledger must be attacked anew.

Prospective queue changes touch only named Status, Turns and Findings. Chat/DOI and all other rows remain byte-exact. There are no live queue/state/history writes, no branch changes, no paper/newDOI/tracker or claimed human review at this stage. Accepted administrative integration after a clean gate must preserve all scientific/source/dependency bytes and archive the prospective administrative fields.
''')
deps=[]
for name in ['differential_family','differential_family/qualification_readiness_hash','linking_family','primary_scope_family']:
    f=HERE/name;m=load(f/'MANIFEST.json')
    for z in m.get('members',m.get('files')):
        b=(f/z['path']).read_bytes();assert sha(b)==z['sha256'];deps.append({'path':str((f/z['path']).relative_to(HERE)),'bytes':len(b),'sha256':sha(b),'role':'closed_family_or_additive_qualification'})
    p=f/'MANIFEST.json';deps.append({'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'role':'closed_manifest'})
for p in sorted(HERE.glob('ROOT*')):
    if p.is_file():deps.append({'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'role':'root_proof_or_exact_replay_or_preserved_failure'})
for p in [HERE/'snapshot_manifest.json',HERE/'pr_input.json']+sorted((HERE/'pr_input').glob('*')):
    if p.is_file():deps.append({'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'role':'frozen_git_metadata'})
for z in original:
    p=snapshot/z['path'];deps.append({'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'role':'original_git_artifact'})
for p in [Path(__file__),HERE/'reproduce_root_families.py']+sorted((HERE/'root_replay_revisions').glob('*')):
    deps.append({'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'role':'root_actual_code_or_preserved_revision'})
assert len({z['path'] for z in deps})==len(deps)
dump(current/'CURRENT_PROOF_DEPENDENCIES.json',{'utc':NOW,'base':'../','scope':'All closed original families and qualification, root proofs/replays/failures, original16/Git metadata and actual root code. Ignored foreign source files separately URL/version/hash bound.','files':deps})
members=[]
for p in sorted(current.rglob('*')):
    if p.is_file():members.append({'path':str(p.relative_to(current)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
dump(current/'MANIFEST.json',{'utc':NOW,'scope':'Complete prospective revised credited counterexample packet; self excluding MANIFEST.json; no current complete verdict yet.','files_count':len(members),'files':members})
for z in members:assert sha((current/z['path']).read_bytes())==z['sha256']
inventory=ROOT/'draft_pr_publication_program_20260930/inventory.json';inv=load(inventory)
item=next(z for z in inv['items'] if z['number']==34);item.update({'stage':'current_credited_counterexample_frozen_pending_NEW_complete_gate','workflow_completion_estimate_percent':75,'original_attempts':'1/5','new_substantive_attempts':1,'cumulative_attempts':'2/5','reviewed_candidate_manifest_sha256':sha((current/'MANIFEST.json').read_bytes()),'positive_prior':'Ni-Zhang-Zhang arXiv2606.29231v1 section2; fully verified elementary consequence; no novelty claim.'})
inv['current_pr']=34;inv['updated_at_utc']=NOW;dump(inventory,inv)
with (ROOT/'draft_pr_publication_program_20260930/RESEARCH_LOG.md').open('a') as f:f.write('\n## '+NOW+' — PR34 revised credited literal counterexample frozen\n\nWorkflow75%; original16 byte-exact, closedfamilies86+4manifests, full root universal proof and actual exact differential/linking/prior/source/SQLite/hash-role replays verified. Literal2019 assertion false for embedded Gamma with smooth injective unit B and zero linking every0<epsilon<1/3. Exact specialization of June2026 Ni-Zhang-Zhang construction, creditedalready_solved proposed; later negative-curvature target excluded. Original1 plus newcounterexample1 = cumulative2/5; audit0. Preserved false hash-role issue is withdrawn additively; all actual failures retained. NEW complete revised-packet adversary next, no paper/newDOI/tracker. Program23/180=12.7778%;18/20holds remain.\n')
print(json.dumps({'current_members':len(members),'dependency_members':len(deps),'manifest_sha256':sha((current/'MANIFEST.json').read_bytes()),'status':'already_solved proposed','budget':'2/5','live_queue_state_writes':0}))
