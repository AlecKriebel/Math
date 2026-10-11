"""Freeze reviewable PR35 partial findings without writing shared acceptance state."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
H=Path(__file__).resolve().parent;R=H.parents[2];C=H/'reviewed_candidate';S=H/'source_snapshot'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def dump(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
assert not C.exists(),'Never overwrite a frozen candidate'
sm=load(H/'snapshot_manifest.json');root=load(H/'ROOT_CLOSED_FAMILY_ACTUAL_REPRODUCTION.json')
assert root['closed_first_party_members_verified_before_and_after']==83 and len(root['actual_unchanged_outer_runs'])==9
assert root['original_program_replays_byte_exact_in_each_family'] and root['attempts_added']==0
for z in sm['files']:
    b=(S/z['path']).read_bytes();assert len(b)==z['size'] and sha(b)==z['sha256']
    assert b==subprocess.check_output(['git','show',sm['head']+':unsolved_math_prioritization/attempts/2744/'+z['path']],cwd=R)
assert len(sm['files'])==15
p=load(S/'source_record.json');prior=load(H/'pinned_prior_report.json');assert prior=={}
rh=sha(json.dumps([p,prior],sort_keys=True).encode());sth=sha(p['statement'].encode())
assert rh=='f1e027d879447ba7fe2692009e5e226437de60fbc0234c2d316b7e290ffdc28e'
assert sth=='1ef73aeb08729350a05e422c05c3f4d5b080490819d2e52a0ce0cc373517158e'
shutil.copytree(S,C);shutil.copytree(S,C/'original_archive')
shutil.copyfile(H/'pinned_prior_report.json',C/'prior_report.json')
shutil.copyfile(H/'ROOT_UNIVERSAL_CERTIFICATE.md',C/'CURRENT_UNIVERSAL_CERTIFICATE.md')
for family,src,dst in [('algebraic_family','UNIVERSAL_NORMALIZATION_PROOF.md','CURRENT_NORMALIZATION_PROOF.md'),('cone_family','PROOF.md','CURRENT_CONE_CRITERION_PROOF.md'),('primary_scope_family','UNIVERSAL_SCOPE_CERTIFICATE.md','CURRENT_SCOPE_CERTIFICATE.md')]:shutil.copyfile(H/family/src,C/dst)
body='''# KP-1.85: audited unresolved partial findings

The full target remains unresolved in this attempt: a nonconstant SO(3) character arc on the specified complete-holonomy PSL2(C) component for every hyperbolic knot in S3. The retained finite-quotient normalization and conditional real-component obstruction are correct. Known Euclidean-cone and two-bridge cases are credited earlier results. No universal cone existence, canonical-component bridge or qualifying knot counterexample is supplied.

OBSTRUCTION.md remains the exact original mathematical artifact. CURRENT_UNIVERSAL_CERTIFICATE.md and the independent normalization/cone/scope certificates document the full retained deductions and exact gap, including the cone angle-pi boundary and imported analytic theorem hypotheses. Finite exact controls reproduce the original21/21/121 results; they do not validate arbitrary prose or prove the universal knot problem.

Proposed outcomeunsolved, accepted partial findings. Original1/5 substantive response, newresearch0, verification0. No paper, newDOI or tracker row. Three distinct independently sealed approach families and actual parent replay are complete; a NEW whole-current-package review remains pending. AI tools were extensively used; documentation is unrefereed AI-audited, without claimed external human review or formal proof-assistant verification.
'''
(C/'README.md').write_text(body+'\nAll original15 artifacts and original dated model/provenance/log/turn metadata are byte-exact in original_archive/. Top-level turns.json and source_record.json also remain byte-exact historical records; their dates/model fields do not describe this current parent audit. independent_review/ is the historical original review and has not been transferred as a current complete gate. New current readiness/provenance/status are independently scoped.\n\nPrivate reproduction: copy check_controls.py and independent_review/independent_checks.py before running them with /usr/bin/python3 and SymPy1.14.0. The independent program writes independent_results.json beside its copied implementation. See CURRENT_PROOF_DEPENDENCIES.json; its ../ base resolves from the frozen audit packet in draft_pr_publication_program_20260930/audits/pr35_2744, the explicit source anchor recorded there.\n')
(C/'PR_DRAFT.md').write_text(body);(C/'pr_body.md').write_text(body)
qualification='''# Exact source and imported-proof qualification

The literal K3 Problem1.85 is printedpp76–77 of the official author PDF. The fixed oriented projective complete-holonomy component and a character arc are essential. Source_record preserves the complete pinned raw record and dated background triage. There is no separate KP-1.85 prior-report dictionary entry: the actual importer joins{}. A missing separate entry does not erase the embedded background literature. Raw imported open status is historical data, not a current worldwide open-status certificate.

Heusener–Porti v2 §4.1 first quotients the liftable locus; hyperbolic knot asphericity and H2/UCT prove all projective representations lift here. Complete-cusp smoothness is independently sourced to Porti2017 §3 and Heusener–Porti AppendixB. Exceptional quotient fibres and sign-versus-orientation distinctions are retained. Porti2017's then-known uniqueness remark is historical; Boyle–Rouse2024 supplies two sign-exchanged SL canonical components, with identical projective images. Its generic finite-index proof exponent n requires n! for nonnormal subgroups; actualindex2 application is valid. This source slip does not invalidate its theorem or the original normalization.

CRS corrected arxivv3 and the published primary text retain additional hypotheses and the general conjecture. The initialv1 additional no-real-points equivalence was removed; it is not imported. The general existence result recalled there gives a unitary character curve somewhere, which still does not prove membership in the specified canonical component. Long–Reid general one-cusped examples are not S3 knot counterexamples, and invariant trace field differs from curve definition field. Bounded later source searches are not exhaustive worldwide priority certification.

Dix2024 complete operative Section3.3 and its corollary proof were read in the official primary web PDF throughlines951; Chapter5 retains geometric/Montesinos future work. Direct fresh byte retrieval403 is preserved: the historical9328a5 PDF hash is not claimed newly retrieved. Complete later Porti–Weiss operative cohomology/integrability/regeneration proofs, Kojima marked continuation, and Heusener–Porti AppendicesA/B are checked with precise hypotheses. The unavailable full old Porti1998 lemma is not claimed read: the angle-pi boundary is instead independently excluded using the knot double-cover odd homology and six orientable flat types. The original full HK analytic proof was not retrieved; its precise published Kojima restatement is imported. Foundational L2, Artin, compactness/Culler–Shalen and flat-classification inputs are explicitly imported, not newly proved or certified by diagnostic counts. Unused printed slips in Porti–Weiss and Porti2004 are separately qualified in the cone family's complete ledger.

All historical and current source/report/artifact/review-document hash roles remain distinct. Initial source-join, literal-Findings-link and SymPy failures are retained as failed invocations with actual corrected replays; none is relabelled an initialPASS. All original15 artifacts, the original1/5 turn ledger, raw source and mathematical OBSTRUCTION are unchanged. No current parent model identifier/effort is exposed, and no new deadline is assigned. Original dated model/effort and source-check metadata describe only the original response. This current revision has no transferred clean verdict and requires a NEW whole reviewer.
'''
(C/'CURRENT_SOURCE_QUALIFICATION.md').write_text(qualification)
oldpro=load(S/'provenance.json');t=load(S/'turns.json')
assert t['substantive_turns_used']==1 and t['turn_limit']==5
pro={'utc':now,'problem_id':2744,'original_head':sm['head'],'actual_base':sm['base'],'raw_source_sha256':sha((C/'source_record.json').read_bytes()),'raw_prior_report_sha256':sha((C/'prior_report.json').read_bytes()),'review_hash':rh,'statement_hash':sth,'original_artifact_sha256':sha((C/'OBSTRUCTION.md').read_bytes()),'current_universal_certificate_sha256':sha((C/'CURRENT_UNIVERSAL_CERTIFICATE.md').read_bytes()),'historical_original_provenance':oldpro,'historical_original_provenance_scope':'Original dated source/model/review metadata only; original_archive/provenance.json byte-exact. No old partial verdict transferred.','current_parent_model':'Identifier not independently exposed in this runtime','current_parent_reasoning_effort':'Not independently exposed in this runtime','current_source_checks':'Actual fresh primary receipts and precise operative reading ledgers bound; Dix fresh web proof reading but no fresh local byte SHA; source-qualified imports explicit.','status':'unsolved_proposed_pending_NEW_complete_gate','new_substantive_attempts':0,'verification_attempts':0,'cumulative_attempts':'1/5','paper_or_new_doi_or_tracker':False}
dump(C/'provenance.json',pro)
ready={'utc':now,'id':2744,'problem_number':'KP-1.85','review_hash':rh,'statement_hash':sth,'exact_claim':'Every hyperbolic S3 knot: the specified oriented complete-holonomy PSL2(C) irreducible component contains a nonconstant SO3 character arc.','artifact':'OBSTRUCTION.md','reviewed_artifact_sha256':sha((C/'OBSTRUCTION.md').read_bytes()),'supporting_universal_certificate':'CURRENT_UNIVERSAL_CERTIFICATE.md','supporting_certificate_sha256':sha((C/'CURRENT_UNIVERSAL_CERTIFICATE.md').read_bytes()),'queue_outcome_requested':'unsolved','status':'current_packet_pending_NEW_complete_adversary','remaining_gap':'No general compact arc on the specified component, universal qualifying cone metric, or qualifying knot counterexample.','literature_checked_at':now,'literature_check_scope':'Current actual primary source/audit/replay checkpoint, as bound by source ledgers; bounded search only, no exhaustive worldwide-open or novelty claim.','budget':{'maximum_substantive_attempts':5,'used_substantive_attempts':1,'original_substantive_attempts':1,'new_substantive_attempts':0,'verification_attempts':0,'time_cap_utc':None,'scope':'Persistent human-authorized audit; no replacement deadline assigned; original turn/model metadata historical only.','model':'Current parent identifier not independently exposed in this runtime','reasoning_effort':'Not independently exposed in this runtime'},'original_turns_sha256':sha((C/'turns.json').read_bytes()),'historical_original_turn_metadata':t,'independent_review':'Three initially independent approach families closed and root actual nine outer runs reproduced. NEW whole current packet gate pending; original/family verdicts do not certify future edits.','positive_novelty_claim':False,'paper_or_new_doi_or_tracker':False,'workflow_completion_estimate_percent':75,'full_resolution_completion_estimate_percent':0}
dump(C/'readiness.json',ready)
dump(C/'current_status.json',{'utc':now,'id':2744,'pr':35,'original_head':sm['head'],'queue_status_proposed':'unsolved','current_gate':'pending_NEW_complete_current_package_adversary','cumulative_attempts':'1/5','new_substantive_attempts':0,'verification_attempts':0,'worldwide_open_status_exhaustively_certified':False,'literal_problem_resolved':False,'paper_or_new_doi_or_tracker':False,'workflow_completion_estimate_percent':75})
q=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();lines=q.decode().splitlines(keepends=True)
names=[v.strip() for v in next(z for z in lines if z.startswith('| Rank |')).split('|')[1:-1]]
assert names==['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
rows=[z for z in lines if len(z.split('|'))==14 and z.split('|')[2].strip()=='2744 / KP-1.85'];assert len(rows)==1
before=rows[0];bc=before.split('|');assert bc[8].strip()=='queued' and bc[9].strip()=='0/5' and not any(bc[i].strip() for i in [10,11,12])
ac=list(bc);ac[8]=' unsolved ';ac[9]=' 1/5 ';ac[11]=' 2026-10-02: Audited finite-quotient/compact-lifting normalization and conditional conjugation obstruction; credited Dix cone criterion and hyperbolic two-bridge cases. No general SO3 arc on the specified oriented complete PSL2 component, universal cone existence or qualifying knot counterexample. Proposed accepted unsolved partial after NEW whole gate; original1/5, verification0; no paper/newDOI/tracker. PR: https://github.com/AlecKriebel/Math/pull/35. '
after='|'.join(ac);prospective=q.replace(before.encode(),after.encode())
assert all(bc[i]==ac[i] for i in range(14) if i not in [8,9,11])
dump(C/'CURRENT_QUEUE_PATCH.json',{'utc':now,'phase':'Dated prospective review snapshot only; no live writes. Any intervening accepted target must be preserved by guarded named-row rebase at integration, with separate receipt.','header_names':names,'whole_queue_preimage_sha256':sha(q),'whole_queue_prospective_sha256':sha(prospective),'row_before':before,'row_prospective':after,'allowed_named_changes':['Status','Turns','Findings'],'all_unrelated_bytes_and_Chat_DOI_preserved':True})
log='# Current PR35 research/audit log\n\n'+now+' — workflow75%: original15 and mathematical OBSTRUCTION unchanged; all three closed independent families and root universal reconstruction agree on correctly scoped unsolved partial. Actual nine outer replay programs pass; original21/21/121 BYTE exact and24 actual mathematical mutants rejected across families. Full proof/source/version/boundary qualifiers bound. Original1/5, newresearch0, verification0. NEW whole current review pending; no paper/newDOI/tracker; no external human review. Original log/model/turn metadata archival only.\n'
(C/'RESEARCH_LOG.md').write_text(log)
(C/'CURRENT_AUDIT_SCOPE.md').write_text('All current scientific/supporting proof/source/metadata/ledger/body/status/queue fields require a NEW complete adversary. Original and family PASS are restricted historical findings, not transferred. All raw sources and original fifteen artifacts are exact. Supplemental counts never certify the universal conjecture. The dated queue preimage snapshot is prospective; later guarded integration must preserve every intervening unrelated acceptance. Dependencies are anchored at the original audit folder recorded below, including when copied into an accepted canonical folder.\n')
private=H/'tmp/current_replay';private.mkdir(exist_ok=True)
for rel,out,want in [('check_controls.py','check_results.json','check_results.json'),('independent_review/independent_checks.py','independent_results.json','independent_review/independent_results.json')]:
    code=private/Path(rel).name;shutil.copyfile(C/rel,code);x=subprocess.run(['/usr/bin/python3',str(code)],capture_output=True,timeout=120)
    assert x.returncode==0 and not x.stderr and (private/out).read_bytes()==(S/want).read_bytes()
assert sha((C/'OBSTRUCTION.md').read_bytes())=='99a09c92911e10ee1cba5de34f4ab78274cb8e211fa0f1456ed80b640819f872'
assert (C/'turns.json').read_bytes()==(S/'turns.json').read_bytes()
dump(H/'ROOT_CURRENT_INPUT_VERIFICATION.json',{'utc':now,'original15_git_bytes_verified':True,'mathematical_obstruction_and_source_and_turns_unchanged':True,'current_actual_21_and_121_results_byte_exact':True,'original_budget':'1/5','new_substantive_attempts':0,'current_whole_gate_pending':True,'workflow_completion_estimate_percent':75})
deps=[]
def add(path,role):
    b=path.read_bytes();deps.append({'path':str(path.relative_to(H)),'bytes':len(b),'sha256':sha(b),'role':role})
for family in ['algebraic_family','cone_family','primary_scope_family']:
    f=H/family
    for z in load(f/'MANIFEST.json')['files']:
        b=(f/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256'];add(f/z['path'],'closed_original_stage_family')
    add(f/'MANIFEST.json','closed_self_excluding_manifest')
for z in sm['files']:add(S/z['path'],'original_git_artifact')
for path in sorted(H.glob('ROOT*')):
    if path.is_file():add(path,'root_universal_source_replay_or_preserved_failure')
for path in [H/'snapshot_manifest.json',H/'pinned_prior_report.json',Path(__file__),H/'reproduce_root_families.py']+sorted((H/'pr_input').glob('*')):add(path,'actual_code_or_git_source_metadata')
assert len({z['path'] for z in deps})==len(deps)
dump(C/'CURRENT_PROOF_DEPENDENCIES.json',{'utc':now,'base':'../','dependency_anchor_repository_relative':str(H.relative_to(R)),'scope':'All three closed original-stage83members/3manifests, original15, root universal/source/replay/failure receipts and actual preparation/replay/Git metadata. Paths resolve from this frozen audit anchor, including copied accepted packets.','files':deps})
members=[{'path':str(path.relative_to(C)),'bytes':path.stat().st_size,'sha256':sha(path.read_bytes())} for path in sorted(C.rglob('*')) if path.is_file()]
dump(C/'MANIFEST.json',{'utc':now,'scope':'Complete prospective source-qualified unsolved partial packet; self excluding, NEW whole gate pending.','files_count':len(members),'files':members})
for z in members:
    b=(C/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
ip=R/'draft_pr_publication_program_20260930/inventory.json';inv=load(ip);item=next(z for z in inv['items'] if z['number']==35)
item.update(stage='source_qualified_unsolved_current_frozen_pending_NEW_whole_gate',workflow_completion_estimate_percent=75,original_attempts='1/5',new_substantive_attempts=0,cumulative_attempts='1/5',reviewed_candidate_manifest_sha256=sha((C/'MANIFEST.json').read_bytes()))
inv['updated_at_utc']=now;dump(ip,inv)
with (H/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+log.split('\n\n',1)[1])
with (R/'draft_pr_publication_program_20260930/RESEARCH_LOG.md').open('a') as f:f.write('\n## '+now+' — PR35 unsolved partial packet frozen\n\nWorkflow75%. Three independent closed algebraic/cone/primary families83members, root all nine actual outer programs and original21/21/121 byte-exact. Full normalization proof, known cone criterion, pi boundary and operative primary foundations checked; exact universal canonical-arc gap retained. All original15 science/source/turn bytes archived and mathematicalOBSTRUCTION unchanged. Original1/5,new0,audit0. Fresh whole reviewer next; no paper/newDOI/tracker. PR34 separate fresh literal-first reviewer pending. Program23/180=12.7778%,18/20holds remain.\n')
print(json.dumps({'members':len(members),'dependencies':len(deps),'manifest_sha256':sha((C/'MANIFEST.json').read_bytes()),'status':'unsolved','attempts':'1/5','live_queue_state_history_writes':0},indent=2))
