"""Prepare PR209's dated publication presentation locally; preserve original bytes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
B=Path(__file__).resolve().parent;D=B.parent/'initial_review_20261016'
O=D/'submitted/unsolved_math_prioritization/attempts/5100015'
V=B/'verification';N=B/'pr_update/5100015';H=N/'history/original_submission_20261016'
assert not (B/'PREPARATION_RECEIPT.json').exists(),'Never overwrite a completed or reviewed package'
V.mkdir(exist_ok=True);N.mkdir(parents=True,exist_ok=True);H.mkdir(parents=True,exist_ok=True)
def save(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def copy(a,b):
 assert a.is_file() and not a.is_symlink();b.parent.mkdir(parents=True,exist_ok=True)
 if b.exists():
  raw=a.read_bytes();old=b.read_bytes()
  if old==raw:return
  assert b==V/'audits/priority_author_updates_01/COMPARISON_CHECK_RESULTS.json' and len(old)<len(raw) and raw.startswith(old),'Unexpected occupied target'
  record=dict(utc=datetime.now(timezone.utc).isoformat(),failure='Initial copy failed ENOSPC; only unfinished duplicate repaired from hash-checked unchanged original',path=str(b.relative_to(B)),partial_bytes=len(old),partial_sha256=hashlib.sha256(old).hexdigest(),source_bytes=len(raw),source_sha256=hashlib.sha256(raw).hexdigest())
  save(B/'PREPARATION_ENOSPC_RECOVERY.json',record)
 shutil.copyfile(a,b);assert a.read_bytes()==b.read_bytes()
def pin(p,base):
 r=p.read_bytes();return dict(path=p.relative_to(base).as_posix(),bytes=len(r),sha256=hashlib.sha256(r).hexdigest())
intake=json.loads((D/'INTAKE.json').read_text());pins=[]
for row in intake['original_source_files']:
 a=D/'submitted'/row['native_path'];r=a.read_bytes();assert len(r)==row['bytes'] and hashlib.sha256(r).hexdigest()==row['sha256']
 rel=a.relative_to(O)
 for target in [V/'original_submission'/rel,N/rel,H/rel]:copy(a,target)
 pins.append(pin(a,O))
assert len(pins)==23
families=['source_domain_adversary_01','physical_geometry_adversary_01','meromorphic_divisor_adversary_01','priority_author_updates_01','priority_classical_general_01']
for family in families:
 folder=D/family;manifest=folder/'AUTHORED_MANIFEST.json';obj=json.loads(manifest.read_text());rows=obj.get('files',obj.get('payloads'))
 for row in rows:
  a=folder/row['path'];assert a.resolve().is_relative_to(folder.resolve()) and not a.is_symlink();r=a.read_bytes();assert len(r)==row['bytes'] and hashlib.sha256(r).hexdigest()==row['sha256'];copy(a,V/'audits'/family/row['path'])
 copy(manifest,V/'audits'/family/manifest.name)
 if family=='priority_author_updates_01':
  s=folder/'AUTHORED_MANIFEST_SUPPLEMENT_TIMESTAMP_CORRECTION.json';obj=json.loads(s.read_text())
  for row in [obj['original_manifest'],*obj['original_payloads_unchanged'],*obj['supplemental_payloads']]:
   a=folder/row['path'];assert hashlib.sha256(a.read_bytes()).hexdigest()==row['sha256'];copy(a,V/'audits'/family/row['path'])
  copy(s,V/'audits'/family/s.name)
for name in ['INTAKE.json','ROOT_MATHEMATICAL_ACCEPTANCE.json','ROOT_MATHEMATICAL_ACCEPTANCE.md','ROOT_ANALYTIC_AUDIT.md','ROOT_PRIMARY_BYTE_VERIFICATION.json','ROOT_PRIORITY_SYNTHESIS.md','ROOT_PRIORITY_ACCEPTANCE.json','ROOT_PRIORITY_SOURCE_BYTE_VERIFICATION.json','ROOT_COMPARISON_SOURCE_BYTES.json','ROOT_CONTEMPORARY_COVERAGE_PRELIMINARY.md','PROGRESS_15_CHECKPOINT_RECEIPT.json','PROGRESS_25_CHECKPOINT_RECEIPT.json','PROGRESS_35_CHECKPOINT_RECEIPT.json']:
 copy(D/name,V/'audit_receipts'/name)
for folder in ['root_reproduction_01','root_reproduction_02','root_reproduction_03','priority_public_chronology_01']:
 for a in sorted((D/folder).rglob('*')):
  if a.is_file():
   if any(t.startswith('private') or t=='__pycache__' for t in a.relative_to(D/folder).parts):continue
   copy(a,V/'root_reproductions'/folder/a.relative_to(D/folder))
copy(D/'root_exact_geometry.py',V/'scope_controls/root_exact_geometry.py')
# Current presentation replaces stale assessments; all inherited bindings remain in history.
proof=(O/'PROOF.md').read_text();start=proof.index('## 1.');stop=proof.index('## 7.')
proof='# The outer center-pedal area product, k303,b\n\nCurrent mathematical presentation, 16 October 2026. Full strict-ellipse theorem; classical and exact contemporary work credited. No novelty, first-proof or historical-independence claim.\n\n'+proof[start:stop]+'''## 7. Current scope, credits and review status

Reversal changes both signed areas' signs. A fixed d-fold traversal multiplies both areas by d and their product by d²; a listed period not divisible by four has primitive divisor not divisible by four. Nondegenerate one/two-bounce strict-ellipse orbits are impossible. Circles follow separately by rigid rotation of fixed-step regular stars. Hyperbolic, focal, collapsed, arbitrary-reference-point and unsigned filled-lobe assertions are not included.

The odd trace lemma is classical: Khare-Lakshminarayan-Sukhatme, arXiv:math-ph/0207019v1 (2002), AppendixA Eq86, product dn=C_q U_q with C_q=product cs²(2Kj/q), gives U_q(z)U_q(z+K)=(k')^q/C_q². Generalized Landen formulas of Khare-Sukhatme (2003/2004) provide another old route. The complete explicit constant is coefficient(21) times r²(k')^q/C_q². The analytic proof above is a reproof of prior elliptic-function facts, not a new identity or method.

Akopyan-Schwartz-Tabachnikov, arXiv:2001.02934v2, Theorem4 proof and Lemma3.1/Remark3.2, already give the unit-velocity/center-foot mechanism and skew hodograph; Bialy-Tabachnikov, arXiv:2001.08469v2, Theorem4.1, gives the actual-foot telescope. This proof makes the same-caustic canonical phase and signed-area normalization explicit. Stachel's canonical theorem, Jacobi identities, conic polarity, and the established complex Poncelet/pole-cancellation method are credited. Chavez-Caliz's Theorem6 concerns the different original/outer area product; an explicit auxiliary-family bridge to trace constancy is in the supplement.

A. Ferudun, *Outer-Pedal Area Products in Elliptic Billiards*, v1.1, DOI10.5281/zenodo.23088516, Theorem2/Section6, proves the exact complete target, including odd and2mod4 lengths and signed repetitions. v1.0 (DOI10.5281/zenodo.23087221) only gives the primitive even arbitrary-point result and hence its centered even subset. The bounded priority audit authenticates earlier GitHub server receipt of this unchanged candidate tree than either Zenodo record, but does not establish historical public availability, exclude earlier website posting, or certify independent non-derivation. Historical ordering and novelty remain undetermined. No exclusive/currently-open/first theorem claim is made.

Original conjecture: Reznik-Garcia-Koiller arXiv2004.12497 (2020; v11Table4p6), published *Fifty New Invariants*, AMJ7(2021),341-355, Table4p346, DOI10.1007/s40598-021-00174-y. The2021 source-year is the journal edition. Source Section2 specifies signed areas and Section3.4 the outer polygon.

Three new mathematical/source families, two priority families, exact original-checker replays and actual Cartesian physical controls have been checked. Finite high-precision diagnostics are not universal or interval proofs. Extensive AI use supported discovery, derivation, source investigation, programming, writing and internal adversarial review. This is unrefereed; no independent human peer review or formal proof verification is claimed. Required whole-package reviews and actual publication outcomes are recorded separately, not self-certified by this dated preparation snapshot.

All23 original files and dated inherited reviews remain byte-exact under history/original_submission_20261016/. Current presentation manifests bind current files; historical manifests and historical receipts bind that archive, not this edited proof. The original author budget remains one of five substantive turns.
'''
(N/'PROOF.md').write_text(proof)
summary='''The signed outer tangent/center-pedal area product k303,b is proved for a strictly nested nondegenerate confocal elliptical caustic and periods not divisible by four, with admissible stars, reversal and fixed-repeat scaling. Actual feet lie on the boundary tangent side lines. Hyperbolic/focal/collapsed caustics and unsigned filled-lobe areas are outside scope.

Classical KLS2002 odd Jacobi product-to-sum, KS2003/2004 Landen, AST2020 velocity/foot and skew-hodograph, BT2020 telescope, Stachel canonical and standard conic/Jacobi/pole methods are credited. Ferudun2026v1.1 Theorem2/Section6 (DOI10.5281/zenodo.23088516) is an exact contemporary full proof; v1.0 covers only the primitive even centered subset via its arbitrary-point result. Historical ordering, independent non-derivation and novelty are undetermined. No first-proof, current-worldwide-open, new-identity or exclusive-resolution claim is made.

Extensive AI assistance; unrefereed, with no independent human peer review or formal proof verification. Full mathematical/source and qualified bounded priority audit are accepted. Whole-package sequential review, final clearance and actual release outcomes are separate later records; this preparation snapshot does not authorize or predict them.
'''
(N/'README.md').write_text('# Current reviewed center-pedal theorem\n\n'+summary+'\nSee PROOF.md, SOURCES.md and PUBLICATION_STATUS.md. All23 original files, old pending assessments and hash bindings remain verbatim in history/original_submission_20261016/. Unchanged verification scripts can overwrite adjacent receipts; use the portable harness in the accompanying source archive, which executes isolated copies. Current verification.json labels the historical author result.\n')
(N/'STATUS.md').write_text('# Current status: mathematical resolution, qualified priority\n\n'+summary+'\nQUEUE classification claimed_solved records a complete mathematical resolution, not historical firstness. Original author turn1/5 retained.\n')
(N/'SOURCES.md').write_text('# Current source and priority map\n\n'+summary+'\nOriginal source: Reznik-Garcia-Koiller, arXiv:2004.12497v11, 29October2020, Table4p6 k303,b; first source version26April2020 Table3p4. Published companion AMJ7(2021),341-355, Table4p346, DOI10.1007/s40598-021-00174-y. Section2 signed area; Section3.4 outer construction.\n\nStachel EJM8(2022),1602-1622, Theorem4.3/Eq4.9p1614, DOI10.1007/s40879-021-00524-2. DLMF22.4/22.6/22.8 period, quarter-shift and addition formulas. KLS arXivmath-ph/0207019v1 AppA Eq86 (v2Eq85), JMP44(2003)1822-1841 DOI10.1063/1.1560856. KS published *Connecting Jacobi elliptic functions with different modulus parameters*, Pramana63(2004)921-936 DOI10.1007/BF02704331; author version *Generalized Landen Transformation Formulas for Jacobi Elliptic Functions*, arXivmath-ph/0312074v1(2003). AST arXiv2001.02934v2 Thm4proof/Lem3.1/Rem3.2 DOI10.1007/s40879-020-00426-9; BT arXiv2001.08469v2 Thm4.1 DOI10.1007/s40879-020-00428-7. Chavez-Caliz AMJ7(2021)91-106 Thm6 DOI10.1007/s40598-020-00154-8. Ferudun v1.1 DOI10.5281/zenodo.23088516, concept23087220; v1.0 DOI23087221.\n\nDetailed actual primary passages, hashes, chronology, failed-access limits and old/current theorem comparisons are in the accompanying audit archive. The2004 publisher PDF was not newly accessed: retained published text plus actual2002/2003 primary PDFs support the comparisons. Source-author abstract screens and missing archive captures do not certify proof absence. No third-party papers, extracted full texts or environments are redistributed. Original source_manifest.json is historical primary-PDF provenance; it is not a current priority certificate.\n')
(N/'PUBLICATION_STATUS.md').write_text('# Dated prepublication snapshot\n\n'+summary+'\nThe standalone manuscript, metadata and portable verification package are prepared with this snapshot. Future FINAL_CLEARANCE and actual release receipts record whole-package review, exact accepted bytes, DOI, tracker and merge. None is claimed by this dated snapshot.\n')
(N/'SOURCE_CHECKPOINT.md').write_text('# Current versus historical source checkpoint\n\nThe complete original checkpoint is preserved under history/original_submission_20261016/. Current scope and credits are in PROOF.md/SOURCES.md; mathematical and qualified priority acceptance are in the case audit. Original author turn1/5. This dated preparation snapshot is not publication clearance.\n')
ready=json.loads((O/'readiness.json').read_text());ready.update(current_assessment='Mathematical/source pass; qualified priority, exact contemporary full theorem and classical mechanisms credited; whole-package review pending',historical_original='history/original_submission_20261016/readiness.json',current_priority='Historical ordering/non-derivation/novelty undetermined; no first-proof claim');save(N/'readiness.json',ready)
save(N/'verification.json',dict(kind='Historical original-author result, not a binding of the edited current proof',original_head=intake['head'],original_proof_sha256=hashlib.sha256((O/'PROOF.md').read_bytes()).hexdigest(),historical_receipt='history/original_submission_20261016/verification.json',original_result=json.loads((O/'verification.json').read_text()),rerun='Portable isolated-copy harness; never run in the frozen archive'))
# The original frozen manifest is archived. Current bindings are constructed by build_bundle.py.
save(N/'FROZEN_MANIFEST.json',dict(role='Current top-level presentation binding is MANIFEST.json/CURRENT_PACKET_MANIFEST.json; original author freeze retained verbatim in history/original_submission_20261016/FROZEN_MANIFEST.json',source_head=intake['head']))
now=datetime.now(timezone.utc).isoformat()
with (N/'RESEARCH_LOG.md').open('a') as f:f.write(f'\n{now} — case45%: dated credited manuscript/current presentation prepared, all23 originals preserved byte-exact in history; 3math/source and2priority audits accepted, whole-package reviews/publication pending. No new author proof turn or historical firstness claim.\n')
save(B/'NATIVE_RELEASE_PLAN.json',dict(schema='pr209-native-plan-v1',original_head=intake['head'],original_queue_blob=intake['Queue_blob'],target_prefix=intake['native_source_prefix'],queue_path=intake['Queue_path'],original_files=pins,guard='Fresh exact open/draft original head and claimed_solved row; preserve unrelated paths/rows, expected-SHA native PR update and merge; no local Git mutations',later_fields='Only actual accepted final reviews, DOI/deposit, one four-cell tracker readback and release receipts after clearance; no prediction in this snapshot'))
save(B/'metadata.json',dict(title='The outer center-pedal area product in elliptic billiards',upload_type='publication',publication_type='preprint',description='For periodic billiards between strictly nested nondegenerate confocal ellipses, the product of the signed areas of the outer tangent polygon and the perpendicular projection of the ellipse center onto its side lines is constant when the period is not divisible by four. The note proves the original k303,b assertion of Reznik-Garcia-Koiller (2020 arXiv;2021 published edition), including admissible coprime stars and fixed repeated traversals, and provides an explicit invariant value. The actual center-foot map is a fixed linear image of a phase-shifted edge-vector polygon. Classical KLS2002 cyclic Jacobi, KS2003/2004 Landen, AST/BT2020 foot-velocity and hodograph, Stachel canonical coordinates, conic polarity and established meromorphic methods are credited. A. Ferudun2026 version1.1, DOI10.5281/zenodo.23088516, Theorem2/Section6, gives the exact complete contemporary theorem. Historical ordering, independent non-derivation and novelty remain undetermined; no first-proof, exclusive-resolution, new-identity or current-worldwide-open claim is made. The deposit includes the concise research note and portable source/verification archive with immutable original submission, scoped audits, exact controls, separately labelled non-interval numerical diagnostics, corrections and reproducibility limitations. Extensive AI tools supported discovery, mathematics, programming, source investigation, writing and internal adversarial checks. Unrefereed preprint; no independent human peer review or formal proof verification is claimed.',creators=[dict(name='Kriebel, Alec',affiliation='Independent researcher',orcid='0009-0001-9320-500X')],access_right='open',license='cc-by-4.0',publication_date='2026-10-16',version='1.0',keywords=['elliptic billiards','Poncelet polygons','center pedal polygons','signed area','Jacobi elliptic functions','AMR-050-0015','k303,b']))
(B/'README.md').write_text('# Outer center-pedal area product: submission package\n\n'+summary+'\nmanuscript.pdf is the research note; manuscript.tex is its standalone editable source. metadata.json is the exact intended Zenodo metadata. k303b-source-verification.zip is built by build_bundle.py from the byte-bound source manifest. verification/README.md describes isolated offline mathematical reproduction. pr_update/5100015 is the prepared native presentation, with every original file in dated history. No external publication, tracker append or PR mutation is performed by preparing or building these files. Final version-bound whole-package reviews and actual release receipts remain alongside this case outside the ZIP, avoiding a self-referential approval seal.\n')
save(B/'PREPARATION_RECEIPT.json',dict(prepared_utc=now,original_files=23,scoped_audits=5,case_completion_estimate=45,source_head=intake['head'],original_pins=pins))
print(json.dumps(dict(prepared_utc=now,original_files=23,scoped_audits=5,case_completion_estimate=45)))
