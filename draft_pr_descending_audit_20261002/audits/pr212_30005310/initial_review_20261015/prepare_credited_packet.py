"""Prepare only after primary priority acceptance; never mutates a provider."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,shutil
D=Path(__file__).resolve().parent;S=D/'submitted/unsolved_math_prioritization/attempts/30005310';C=D/'corrected_packet'
A=json.loads((D/'ROOT_PRIORITY_ACCEPTANCE.json').read_text())
assert A['status']=='PASS_EXACT_PRIOR_COVERAGE' and A['mathematics']=='PASS'
C.mkdir(exist_ok=False);now=datetime.now(timezone.utc).isoformat();intake=json.loads((D/'INTAKE.json').read_text())
for row in intake['original_source_files']:
 rel=row['native_path'].split('attempts/30005310/',1)[1];raw=(S/rel).read_bytes()
 assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
 q=C/'original_submission'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
old=(S/'PROOF.md').read_text();core=old.split('## 2. Model, statistics and sample convention',1)[1].split('## 8. What is and is not resolved',1)[0]
intro='''# Credited counterexample to the printed numerical threshold scenarios

30005310 / OWR-11695865-009. **Mathematics PASS; historical classification
already_solved for the full literal numerical question.** Author turn1/5.
The negative answer is covered by established results before this candidate.
No certified new solution of the original bare SOS/intersection conjecture
is claimed. That separate question remains unresolved here.

All20 original files, old reviews and manifests are preserved byte for byte
under original_submission/. Mathematical Sections2–7 below are unchanged.
Those historical review verdicts apply to their frozen inputs. The current
credit, source scope and disposition are explained in PRIORITY_AUDIT.md.
AI tools were used extensively; this record is unrefereed and has had no
human peer review. It is not a new preprint or Zenodo deposit.

## 1. Exact original target and prior coverage

Homs's contribution with Kuznetsova in OWR55/2022, printed3146–3149,
DOI10.4171/OWR/2022/55, defines unrestricted colored concentration models.
Proposition3 assumes I(G,n)nonzero and I(G,n+1)=0. Its second bullet
asserts WMLT=n if a positive-definite matrix has statistics in V(I(G,n));
both full numerical scenarios also assert MLT=n+1. Conjecture4 refers
back to the two cases. A numerical error in these assertions is distinct
from the bare claim that one of their two algebraic mechanisms holds.

For singleton K4,4, Gross–Sullivant's2015 primary version, Section5,
Corollary5.3 and explicit bipartite specialization already gives WMLT2.
Blekherman–Sinn's2017 primary version, Theorems2.1 and2.7, already gives
generic completion rank4 and MLT4. These results combine to the exact
singleton counterexample below atn=3. The algebraic ideal bridge is also
proved directly in the unchanged mathematics. The rank-two completion
construction is the bipartition instance of the earlier splitting lemma.

Independently, Homs–Kuznetsova–Stolz, arXiv2609.02382v1, public2September2026,
Proposition3.26, gives an equally vertex-colored C4 with four individually
colored edges, generic completion rank2 and MLT1. Proposition3.9 identifies
generic completion rank as the first zero elimination ideal. Thus atn=1
it contradicts both printed numerical scenarios, which require MLT2.
This earlier same-author theorem decides the literal universal numerical
question even within a four-cycle class. It does not assert a solution of
the bare mechanisms alternative. Both prior routes precede the present
candidate's1October2026 record.

The verified K4,4 construction has WMLT2, I3nonzero and I4zero and remains
valid after tying K11=K22. Exact MLT4 is asserted only for the singleton
model. Earlier exact publication of the tied variant, and earlier explicit
recognition of the2022report's error, have not been established. Those
limitations do not erase the earlier negative answer to the full numerical
question and are not grounds for a new first-solution claim.

## 2. Model, statistics and sample convention'''
end='''## 8. Current disposition and exact remaining gap

The displayed ideal, likelihood and weak-threshold proofs pass three fresh
independent mathematical/source families and root reproduction. No
mathematical repair is required. The numerical implication is false, but
its negative answer is already covered by the primary results identified
above. Status already_solved records that historical finding for the full
literal numerical question; it does not certify all readings of Conjecture4.

The example satisfies the positive-definite-intersection mechanism. It
cannot refute a bare SOS-or-intersection alternative. That route remains
unresolved here and cannot be repaired by merely changing the description
of this same example. The K4,4 example itself does not address a four-cycle
restriction; the earlier2026 coloredC4 theorem separately refutes the full
numerical assertion there. Neither route answers the bare mechanism problem.

Under the active claimed_solved-only workflow, skip this corrected open
draft. No new paper, DOI, upload, tracker row, merge, closure or PR comment
accompanies this credit correction. Preserve author1/5 and all original
mathematical evidence. Exact probabilities, the tied model's exact MLT,
and a historical first-recognition certificate remain unclaimed.
'''
(C/'PROOF.md').write_text(intro+core+end)
(C/'README.md').write_text('''# 30005310 / OWR-11695865-009

**Mathematics PASS; already_solved for the full literal numerical question.**
Earlier Gross–Sullivant/Blekherman–Sinn results cover the singleton K4,4
negative answer. Homs–Kuznetsova–Stolz2609.02382v1 independently covers a
coloredC4 negative answer before this candidate. The bare SOS/intersection
alternative remains unresolved here. Exact earlier tied-variant publication
and explicit prior recognition of the2022error are not certified.

PROOF.md retains mathematical Sections2–7 unchanged. PRIORITY_AUDIT.md
gives the exact primary-source bridges and limits. All20 original files,
reviews/checkers/manifests are archived in original_submission/ byte for byte.
Run `python3 verify.py` with SymPy1.14.0 to reproduce188 exact controls against
the current proof hash; original receipts remain archived separately.

Author1/5 preserved. Skip corrected open draft; no new paper, upload, tracker
row, merge, closure or PRcomment. AI tools used extensively; unrefereed,
without human peer review. This credited verification record has no DOI.
''')
(C/'PUBLICATION_STATUS.md').write_text('''# Current publication and catalog status

already_solved for the full literal numerical question; mathematics PASS.
Earlier primary theorems already supply a negative answer. Bare
SOS/intersection exhaustiveness remains unresolved here. No novel original
open-problem resolution, exact tied-variant anticipation, or first-recognition
priority is certified. Author1/5 preserved.

No preprint clearance, manuscript, Zenodo record, DOI or tracker entry.
The corrected PR remains open/draft and is skipped under the active goal.
Earlier PASS reviews and pending-review labels are historical in
original_submission/; current manifests bind this contextualized packet.
''')
audit=(D/'ROOT_PRIORITY_AUDIT.md').read_text();(C/'PRIORITY_AUDIT.md').write_text(audit)
(C/'SOURCES.md').write_text('''# Current source scope and historical credit

PRIORITY_AUDIT.md is the current primary-source comparison. It covers the
complete original Homs/Kuznetsova contribution, Gross–Sullivant Section5,
Blekherman–Sinn Theorems2.1/2.7 with proofs, and the theoretical sections of
Homs–Kuznetsova–Stolz2609.02382v1, especially Propositions3.9/3.26. External
reading PDFs and rendered pages are private and are not redistributed.

The original unrestricted partitions include singleton and K11=K22 models.
Its statistic edge sums differ from the2026 trace-pairing convention by a
factor2; that invertible coordinate change affects no ideal or likelihood
statement. Knownzero mean/scatter-rank indexing is fixed throughout.

Historical source_record.json remains byte-identical, including its older
literature triage. It records upstream curation, not current priority truth.
The original source audit and all older reviews are archived separately.
No external individual was contacted or outreach prepared.
''')
for name in ['source_record.json','prior_imported_report.json','verify.py']:shutil.copyfile(S/name,C/name)
sm=json.loads((S/'source_manifest.json').read_text());sm.update(current_priority_checked_UTC=now,classification='already_solved for full literal numerical question; bare mechanisms unresolved',original_source_pins_preserved=True)
for name,url in [('gross_sullivant_v3','https://arxiv.org/pdf/1404.6989v3'),('homs_kuznetsova_stolz_v1','https://arxiv.org/pdf/2609.02382v1')]:
 q=D/'private_reading'/(name+'.pdf');sm['sources'].append(dict(file=name+'.pdf',url=url,bytes=q.stat().st_size,sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
(C/'source_manifest.json').write_text(json.dumps(sm,indent=2)+'\n')
(C/'metadata.json').write_text(json.dumps(dict(problem_id=30005310,code='OWR-11695865-009',status='already_solved',classification_meaning='Earlier primary theorems cover negative answer to full literal numerical scenarios; bare SOS/intersection alternative unresolved here',mathematics='PASS',author_turns=1,claimed_new_original_open_problem_solution=False,prior_exact_tied_variant_anticipation_established=False,prior_explicit_error_recognition_established=False,bare_mechanism_alternative_resolved=False,preprint_clearance=False,AI_tools_used_extensively=True,human_peer_review=False,DOI=None,original_head=intake['head'],author='Alec Kriebel',ORCID='https://orcid.org/0009-0001-9320-500X'),indent=2)+'\n')
(C/'RESEARCH_LOG.md').write_text('# Current credited packet log\n\n'+now+' —65% of eligible-intake credit disposition. All20 originals archived and mathematical Sections2–7 unchanged. Earlier exact primary coverage independently verified. Local packet proposed; final independent whole-packet adversary and guarded native application/readback pending. No provider mutation, paper, deposit or tracker action.\n')
(C/'VERIFICATION.md').write_text('''# Verification boundaries

Original188 author and1808 inherited exact controls replay byte for byte
in isolated copies. Three new independent families contribute16+3333+188
exact controls, all replayed by root, alongside full analytic derivations.
The finite checks are supporting controls, not probability simulations.

Current verify.py is byte-identical to the original author program and
computes SHA256 of its actual adjacent PROOF.md. Its currentverification.json
is newly reproduced; only its proof hash differs from the historical receipt.
The inherited independent_check.py hardcodes the old proof hash, so that
program and its receipt remain historical inside original_submission/.
All20 originals have separate actual byte/size/Git-object-hash intake binding.
Old manifests certify their exact archive, not the contextual current text.

Fresh current MANIFEST.json and PUBLICATION_MANIFEST.json bind the current
credit context, proof, checks and original archive. Main campaign evidence
holds full new adversarial reports and exact source/version reading receipts.
Actual reproduction runtime: Python3.14.6 with SymPy1.14.0. No human peer
review is claimed, and this packet is not a new preprint.
''')
py='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'
r=subprocess.run([py,str(C/'verify.py')],capture_output=True,text=True,timeout=180);assert r.returncode==0,r.stderr
v=json.loads((C/'verification.json').read_text());oldv=json.loads((S/'verification.json').read_text());assert v.pop('proof_sha256')==hashlib.sha256((C/'PROOF.md').read_bytes()).hexdigest();oldv.pop('proof_sha256');assert v==oldv
assert (C/'PROOF.md').read_text().split('## 2. Model, statistics and sample convention',1)[1].split('## 8. Current disposition and exact remaining gap',1)[0]==core
for name in ['MANIFEST.json','PUBLICATION_MANIFEST.json']:
 rows=[]
 for q in sorted(C.rglob('*')):
  if q.is_file():
   raw=q.read_bytes();rows.append(dict(path=q.relative_to(C).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
 (C/name).write_text(json.dumps(dict(utc=now,status='already_solved',scope='Current credited packet; own hash excluded; historical original_submission manifests bind their original bytes',files=rows),indent=2)+'\n')
rows=[]
for q in sorted(C.rglob('*')):
 if q.is_file():
  raw=q.read_bytes();rows.append(dict(path=q.relative_to(C).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
manifest=dict(utc=now,PR=212,original_head=intake['head'],status='PROPOSED_NOT_APPLIED',classification='already_solved for literal numerical question only',archive_files=20,mathematical_core_sections='2–7',mathematical_core_sha256=hashlib.sha256(core.encode()).hexdigest(),files=rows)
(D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
oldrow=intake['queue_row'];cols=oldrow.split('|');assert cols[8].strip()=='claimed_solved';cols[8]=' already_solved '
cols[11]=' 2026-10-15: Mathematics PASS; literal numerical classification already refuted by earlier Gross–Sullivant/Blekherman–Sinn results and Homs–Kuznetsova–Stolz2609.02382v1 Prop3.26. Bare SOS/intersection alternative unresolved here; no exact tied-variant or first-recognition priority claim. Author1/5 retained; skip corrected open draft. See [current priority audit](attempts/30005310/PRIORITY_AUDIT.md). '
newrow='|'.join(cols);assert newrow.split('|')[9].strip()=='1/5'
body='''The exact counterexample mathematics passes three fresh independent mathematical/source audit families and root reproduction. This is a credited verification record of an earlier-covered negative answer to the full literal numerical scenarios, classified already_solved. Gross–Sullivant2015 plus Blekherman–Sinn2017 cover the singletonK4,4 triple; Homs–Kuznetsova–Stolz arXiv2609.02382v1 Proposition3.26 separately gives a coloredC4 counterexample before the current candidate.

This does not resolve the bare SOS-versus-PD-intersection alternative, establish earlier publication of the exact tied variant, or certify who first recognized the2022printed error. All20 original files are preserved byte for byte and mathematical Sections2–7 are unchanged. Author1/5 preserved. Extensive AI use; unrefereed, no human peer review.

Under the active claimed_solved-only workflow this corrected draft remains open and is skipped. No new preprint, DOI, deposit, tracker row, merge, closure or PRcomment. See unsolved_math_prioritization/attempts/30005310/PRIORITY_AUDIT.md and the dedicated campaign audit on main for exact evidence.
'''
plan=dict(PR=212,branch=intake['branch'],original_head=intake['head'],old_row=oldrow,new_row=newrow,title='30005310: Credited prior counterexamples to literal numerical scenarios',body=body,planned_source_files=len(rows),original_archive_files=20,packet_manifest_sha256=hashlib.sha256((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_bytes()).hexdigest(),native_mutations_performed=False)
(D/'PROPOSED_NATIVE_CHANGES.json').write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps({'status':'PROPOSED_NOT_APPLIED','files':len(rows),'archive_files':20,'mathematical_core_SHA256':manifest['mathematical_core_sha256'],'current_author_188_replay':True},indent=2))
