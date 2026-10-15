"""Freeze the credited prior-method classification; no shared input writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

A = Path(__file__).resolve().parent
ROOT = A.parents[2]
C = A / 'reviewed_candidate'
assert not C.exists(), 'Do not overwrite a frozen candidate.'
UTC = datetime.now(timezone.utc).isoformat()
HEAD = 'a92af24e2e6015893787e0c55cd4618f7098917e'
OLDHASH = '501c9a536246ad06b29e16720c613bcb292c863857849f837bb0250c45a58050'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def bind(p,base,role=None):
    d={'path':p.relative_to(base).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
    if role: d['role']=role
    return d
shutil.copytree(A/'source_snapshot',C)
for n in ['CANDIDATE.md','README.md','SOURCES.md','readiness.json','status.json']:
    shutil.copyfile(C/n,C/('ORIGINAL_'+n))
(C/'ORIGINAL_PR_BODY.md').write_text(json.loads((A/'pr_input.json').read_text())['body'])
original=(C/'CANDIDATE.md').read_text()
marker='## 1. Statement\n'
prefix,body=original.split(marker,1)
assert sha(C/'ORIGINAL_CANDIDATE.md')==OLDHASH
current_prefix='''# 6800007: credited integral classification from prior methods

**Current outcome: already_solved as an application of earlier published classification machinery.** The full mathematical classification below is sound in its stated regular-homotopy convention, including integral torsion and noncompact/nonorientable boundaryless sources. Taylor's principal-fibration theorem and the standard integral characteristic calculations give the entire formula by routine substitution. This is a priority correction, not a new solution or a novel general theorem. An earlier publication printing the exact ordered-flag coordinates has not been identified; historical recognition of this particular example remains unlocated.

The following statement, proof and examples retain the original scientific body byte-for-byte. CURRENT_PRIOR_APPLICATION.md gives the complete checked substitution into the published theorem, and CURRENT_CREDITED_CLASSIFICATION.md records the independent root verification and precise priority limits. Original mathematical/source/readiness/review bytes are archived. A NEW complete review of this edited current package is pending before partial acceptance. No paper, DOI, release or publication-sheet row follows from an already_solved result.

The object is a fixed smooth second-countable real3-manifold without boundary and ordinary homotopies through totally real immersions into the ordered integrable complex flag. Source diffeomorphisms, properness, embeddings and the neighboring real-form uniformization question are outside this explicit convention. Ordinary integral cohomology is retained.

'''
(C/'CANDIDATE.md').write_text(current_prefix+marker+body)
assert (C/'CANDIDATE.md').read_text().split(marker,1)[1]==body
shutil.copyfile(A/'ROOT_PRIORITY_DECISION.md',C/'CURRENT_CREDITED_CLASSIFICATION.md')
shutil.copyfile(A/'priority_topology_family/SPECIALIZATION_CERTIFICATE.md',C/'CURRENT_PRIOR_APPLICATION.md')
manifests=['hprinciple_family/MANIFEST.json','integral_action_family/artifact_manifest.json',
           'primary_scope_family/MANIFEST.json','priority_flag_family/MANIFEST.json','priority_topology_family/MANIFEST.json']
deps=[]
for name in manifests:
    m=A/name;d=json.loads(m.read_text());entries=d.get('files',d.get('members'))
    for e in entries:
        p=m.parent/e['path'];assert p.stat().st_size==e.get('bytes',e.get('size')) and sha(p)==e['sha256']
        deps.append(bind(p,A,'closed_family_first_party_or_frozen_input_copy'))
    deps.append(bind(m,A,'closed_family_manifest'))
assert len(deps)==156
roots=['ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json','ROOT_SOURCE_RETRIEVAL.json','ROOT_RECONSTRUCTION.md',
       'ROOT_FAMILY_INTEGRITY_AND_REPRODUCTION.json','ROOT_PRIMARY_REPLAY_COMPARISON_FAILURE.json',
       'ROOT_RECONSTRUCTION_SEAL.json','ROOT_ADDITIONAL_PRIOR_RETRIEVAL.json',
       'ROOT_PRIORITY_REPRODUCTION.json','ROOT_PRIORITY_DECISION.md','ROOT_PRIORITY_SEAL.json']
for n in roots: deps.append(bind(A/n,A,'root_proof_or_actual_reproduction_source_scope_receipt'))
for n in ['snapshot_manifest.json','ORIGINAL_COMPARISON.json','pr_input.json','pr_input/pr.json','pr_input/diff.patch']:
    deps.append(bind(A/n,A,'frozen_original_git_metadata'))
for p in sorted((A/'source_snapshot').rglob('*')):
    if p.is_file(): deps.append(bind(p,A,'immutable_original_numeric_artifact'))
assert len(deps)==186 and len({d['path'] for d in deps})==186
js(C/'CURRENT_PROOF_DEPENDENCIES.json',{'utc':UTC,'base':'../','scope':'102original mathematical family members +3manifests;49deep priority members +2manifests;10root;5Git metadata;15original numeric artifacts.','files':deps,'foreign_sources':'Ignored local primary inputs, separately hash/URL/version bound; not first-party findings.'})

queue=ROOT/'unsolved_math_prioritization/QUEUE.md';qb=queue.read_bytes();lines=qb.decode().splitlines(keepends=True)
headers=[l for l in lines if l.startswith('| Rank |')];assert len(headers)==1
names=[x.strip() for x in headers[0].strip().split('|')[1:-1]]
assert names==['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
rows=[(i,l) for i,l in enumerate(lines) if l.startswith('| ') and len(l.split('|'))==14 and l.split('|')[2].strip().startswith('6800007 / ')]
assert len(rows)==1;i,row=rows[0];parts=row.rstrip('\n').split('|');before=dict(zip(names,[x.strip() for x in parts[1:-1]]));assert before['Status']=='queued' and before['Turns']=='0/5'
note=('2026-10-02: Full ordered-integrable-flag totally real regular-homotopy classification audited, including integral torsion/noncompact/nonorientable source scope. Deep priority check derives the entire quotient by routine substitution into Taylor2012 and classical integral characteristic machinery; credited prior-method application, no certified novel result. Earlier exact printed flag formula/historical recognition unlocated. already_solved partial acceptance pending NEW complete gate; original1/5, verification0; no paper/newDOI/tracker. PR: https://github.com/AlecKriebel/Math/pull/32.')
for key,val in {'Status':'already_solved','Turns':'1/5','Findings':note}.items(): parts[names.index(key)+1]=' '+val+' '
after='|'.join(parts)+'\n';ql=lines[:];ql[i]=after
for key in names:
    if key not in ('Status','Turns','Findings'): assert parts[names.index(key)+1]==row.rstrip('\n').split('|')[names.index(key)+1]
js(C/'CURRENT_QUEUE_PATCH.json',{'utc':UTC,'phase':'prospective only; clean NEW complete gate and acceptance wording required before integration','whole_queue_preimage_sha256':hashlib.sha256(qb).hexdigest(),'whole_queue_prospective_sha256':hashlib.sha256(''.join(ql).encode()).hexdigest(),'header_names':names,'row_before':row,'row_prospective':after,'allowed_named_changes':['Status','Turns','Findings'],'all_other_lines_and_fields_byte_preserved':True})
source=json.loads((C/'source_record.json').read_text());e=json.loads((A/'primary_scope_family/SOURCE_IDENTITY_AUDIT.json').read_text())
assert source['problem']==e['problem'] and source['prior_upstream_report']==e['prior_report']
js(C/'CURRENT_SOURCE_CONTEXT.json',{'utc':UTC,'id':6800007,'code':'AMR-067-0007','original_head':HEAD,'actual_base':'01358d66fc67d1c462bddf31c0d4ee5b120e6737','historical_metadata_base':'c6975ca76f9f667f1250ba403d0e6da2aafe14d0','raw_complete_source_and_prior_pair_sha256':sha(C/'source_record.json'),'review_hash':e['review_hash'],'statement_hash':e['statement_hash'],'hash_meaning':'Actual pinned SQLite importer TEXT serialization of complete raw problem/prior pair; not a mathematical proof or current-status certificate.','current_main':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'current_queue_named_row':before,'original_attempts':'1/5','new_substantive_attempts':0,'original_models':'Self-reported historical metadata.'})
qualification='''# Current source and priority qualification

The embedded full raw problem and prior_upstream_report in source_record.json are unchanged historical source objects. Actual pinned complete files, unique ID/code, full imported report and real SQLite TEXT serialization/review hash were independently checked. OPEN-TRIAGE and problem-list hosting are not proof of worldwide current openness. Original model metadata is self-reported.

The literal university TeX Q7 asks for homotopy classification and credits the h-principle; the preceding real-form uniformization question is separate. The adopted regular-homotopy convention and ordered integrable complex structure are explicit. Boundaryless smooth second-countable M, noncompact/nonorientable scope and ordinary integral cohomology are retained.

The deep flag-lineage audit found no complete prior formula in its inspected specialized corpus and deferred general-theorem equivalence. The distinct topology audit then checked a COMPLETE equivalent routine specialization: Taylor2012 Theorem1.2/full proof on the full unbased mapping spaces (using source S⁰), low integral characteristic spaces, the tangent-root Chern formulas and direct integral loop derivatives. Fixed nontrivial E is normalized by a triangular virtual-Chern coordinate shear; the unimodular final shear yields exactly C⊕coker D. All quantified source cases and torsion survive. Thus already_solved records a verified priority issue and credited application of published machinery, not a novel solution claim. No earlier printed exact flag formula or exhaustive historical recognition is asserted.

Credit the classical totally real h-principle; Duchamp/Forstnerič/Borrelli framing methods; Derdzinski–Januszkiewicz2006 determinant mechanism and explicit dimension3 surjectivity; Borel–Hirzebruch1958 characteristic roots; Bott1959 low unitary groups; Gottlieb1972 bundle-map/gauge framework; Koshkin2009 primary/secondary theory; Taylor2012 lift-isotropy theorem and Nomura1969 integral product machinery; and Falbel–Veloso2020 sphere classes. Exact primary versions, locations, applicable proof reading and source limits are in the closed dependency ledgers and CURRENT_PRIOR_APPLICATION.md. Some Nomura property proofs are explicitly omitted; direct integral expansion verifies the needed substitution, and Taylor's full isotropy proof is available.

Koshkin's simply-connected Theorem3 does not directly apply to the frame target withπ1=Z/2. Its de Rham conclusion about nonorientable integralH3 cannot discard torsion. DJ's surface injectivity proof does not extend to3M; only its explicit n3 surjectivity is credited. Euclidean compact-orientable existence is not every-real3M existence. FV2018v1 lacks the later2020 §8.1; complete public coauthor text was read but not identified with unavailable publisherPDF bytes. The survey's local equivalence and scalar homotopy invariant are not injective full classification.

Earlier seals/failed retrievals remain immutable. DJ's old v4 label is explicitly corrected to only-v1; Nomura's two network receipts differ only in27 second-trailer/ID bytes, with identical mathematical bytes/text; the recovered HAL survey closes its actual main-body access gap. Missing original Whitney/Whitehead/Postnikov/Rutter/James–Thomas full texts and incomplete incoming-citation coverage remain historical printed-priority gaps, not missing central steps in the verified available theorem specialization. No inaccessible proof is represented as read.

The whole current mathematical body after §1 is byte-identical to ORIGINAL_CANDIDATE.md; its prefix, source/readiness/body qualifications are edited and need a NEW complete gate. Old reviews apply only to the archived original proof. Exact algebra outputs are finite diagnostics, not universal proof or novelty certificates. Root actual replays compare all generated fields except identified clocks and preserve earlier failures. Downloaded foreign sources stay ignored research inputs.

Original1/5, audit0. Current main remains queued0/5 before guarded integration. A clean new current gate permits already_solved partial acceptance with preserved named12-column QUEUE fields and only an exact accepted source-bound mirror; no new original turn/history is invented. No new paper, DOI, release or publication-sheet row is justified.
'''
(C/'CURRENT_SOURCE_QUALIFICATION.md').write_text(qualification)
(C/'SOURCES.md').write_text('# Current credited-source audit:6800007\n\n'+qualification.split('\n',1)[1]+'\nThe immutable original bounded source audit is ORIGINAL_SOURCES.md. The present qualification supersedes its unknown-equivalent-prior conclusion.\n')
(C/'CURRENT_AUDIT_SCOPE.md').write_text('''# Prospective credited classification acceptance

Original head a92af24e2e6015893787e0c55cd4618f7098917e has15 numeric artifacts and16 changed paths including QUEUE.md. Actual base01358d66fc67d1c462bddf31c0d4ee5b120e6737 differs from historical metadata basec6975ca76f9f667f1250ba403d0e6da2aafe14d0; both are archived accurately. Original1/5, verification0.

Three complete original mathematical families and root reconstruction clear the full formula. Two distinct deep priority families plus root full equivalent-theorem reconstruction establish already_solved as a credited earlier-method application. An earlier exact printed flag formula remains unlocated. This edited complete current packet and exact186-member closure require a NEW complete adversary; historical verdicts do not transfer automatically. Preserve all original bytes, root failures and sealed prior findings. Guarded queue integration changes only namedStatus/Turns/Findings, preserving every other field/row. Old destructive rank/cache helpers are investigated only in private copies. No paper/newDOI/tracker.
''')
(C/'review/CURRENT_NOTICE.md').write_text('''# Historical review boundary

These original review files and receipts are unchanged. Their reviewed proof hash501c9a… binds ORIGINAL_CANDIDATE.md, not the edited current CANDIDATE.md. The whole scientific body after§1 remains byte-identical, but the new current source/priority/admin package requires a NEW whole-packet verdict. Original readiness/status/source/README/PR-body bytes are archived. Historical pending/draft-only/no-merge statements are superseded by the current human-authorized workflow; no original attempt is removed or added.
''')
state={'utc':UTC,'id':6800007,'pr':32,'original_head':HEAD,'current_gate':'pending_NEW_complete_whole_current_partial_adversary','queue_status_proposed':'already_solved','original_budget':'1/5','new_substantive_attempts':0,'workflow_completion_estimate_percent':75,'classification_complete_in_stated_convention':True,'equivalent_published_method_full_specialization_verified':True,'earlier_exact_printed_flag_formula_identified':False,'positive_novelty_certified':False,'paper_doi_tracker':'none'}
js(C/'current_status.json',state)
old=json.loads((C/'ORIGINAL_status.json').read_text());old.update(state);old.update(status='already_solved_credited_classification_prospective',at_utc=UTC,proof_sha256=sha(C/'CANDIDATE.md'),original_proof_sha256=OLDHASH,full_source_solved=True,new_discovery_claim=False,disposition_note='Entire stated classification supplied by verified routine published-theorem specialization; exact earlier printed flag formula unlocated; NEW complete edited-package gate pending.',review={'historical_verdict':'PASS','historical_applies_to':'ORIGINAL_CANDIDATE.md','historical_proof_sha256':OLDHASH,'current_gate':'pending_NEW_complete_whole_current_partial_adversary'})
js(C/'status.json',old)
old=json.loads((C/'ORIGINAL_readiness.json').read_text());old.update(state);old.update(branch='main',prior_art_gate='Deep priority equivalent full published-method specialization verified; exact earlier printed flag formula unlocated; NEW whole-current gate pending.',publication='already_solved partial only; no paper/newDOI/tracker',current_artifact_sha256=sha(C/'CANDIDATE.md'),source_context='CURRENT_SOURCE_CONTEXT.json',review_hash=e['review_hash'],statement_hash=e['statement_hash'])
js(C/'readiness.json',old)
(C/'README.md').write_text('''# 6800007: credited flag classification

**already_solved: full explicit classification follows from earlier published methods.** The mathematical result is sound in its stated convention; no novel solution or new-paper claim is accepted. An earlier publication printing these exact flag coordinates/historical recognition remains unlocated.

CANDIDATE.md retains the original scientific statement/proof/examples after§1 unchanged, with an updated current prefix. CURRENT_PRIOR_APPLICATION.md supplies the checked complete Taylor/characteristic-space specialization. CURRENT_CREDITED_CLASSIFICATION.md records the independent root verification; CURRENT_SOURCE_QUALIFICATION.md gives exact scope/priority/version limits. CURRENT_PROOF_DEPENDENCIES.json binds186 supporting original/family/root entries; MANIFEST.json binds this edited current packet. All original administration/math and old reviews are preserved; old verdicts bind ORIGINAL_CANDIDATE.md only.

Three original mathematical families, two distinct deep priority families and root actual replays are complete. The NEW complete edited-package adversarial gate is pending. Historical original1/5 remains; audit0. Only guarded already_solved partial acceptance and exact source-bound state import follow a clean new gate. No paper, Zenodo upload, release, DOI or publication-sheet row.

Original exact programs require SymPy1.14.0; root used /usr/bin/python3 with that library. Finite tests validate algebra and selected countercontrols, while universal proof and exact prior-theorem applicability are read independently. RESEARCH_LOG.md/turns.jsonl are original records; CURRENT_RESEARCH_LOG.md records present workflow. Foreign reference bytes remain ignored.
''')
(C/'pr_body.md').write_text('''This is a credited already_solved application of earlier published classification machinery. The full ordered integrable-flag totally real regular-homotopy classification passes universal mathematical review, retaining ordinary integral torsion and noncompact/nonorientable boundaryless sources.

Deep priority review verifies the entire quotient by routine substitution into Taylor2012's principal-fibration theorem and classical low integral characteristic/root calculations. The fixed nontrivial source bundle and unbased loop action are retained; an integer coordinate change yields exactly C⊕coker D. No additional new classification mechanism is required. An earlier publication printing this exact worked flag formula/historical recognition remains unlocated; that limitation does not supply novelty evidence.

Original15 numeric artifacts/16 changed paths, head a92af24e2e6015893787e0c55cd4618f7098917e, actualbase01358d66fc67d1c462bddf31c0d4ee5b120e6737, are preserved. Original proof/readiness/status/source/README/body are archived; the whole scientific body after§1 is unchanged. Three original math families, two deep primary priority families and actual root replays precede a NEW full edited-package gate, pending. Original1/5, verification0. Guarded integration preserves unrelated QUEUE rows and targetChat/DOI fields, then imports only exact accepted source-bound state. Current human authorization supersedes archived draft-only wording. already_solved partial acceptance entails no paper/newDOI/tracker.
''')
(C/'CURRENT_RESEARCH_LOG.md').write_text(f'{UTC} —75%partial-acceptance workflow: original universal formula verified; two deep priority families/root actual theorem and integral substitution checks complete. Edited current already_solved qualification and originals frozen; NEW whole gate next. Exact earlier printed flag formula remains unlocated; classification complete, positive novelty0%, no paper/DOI/tracker. Original1/5,audit0.\n')
members=[bind(p,C) for p in sorted(C.rglob('*')) if p.is_file()]
js(C/'MANIFEST.json',{'utc':UTC,'scope':'Exact edited current credited application/partial acceptance; NEW complete gate pending; self-excludes MANIFEST.json','original_head':HEAD,'file_count':len(members),'files':members})
print(json.dumps({'utc':UTC,'packet_members':len(members),'dependencies':len(deps),'current_candidate_sha256':sha(C/'CANDIDATE.md'),'manifest_sha256':sha(C/'MANIFEST.json'),'shared_queue_unchanged':sha(queue)==hashlib.sha256(qb).hexdigest()},indent=2))
