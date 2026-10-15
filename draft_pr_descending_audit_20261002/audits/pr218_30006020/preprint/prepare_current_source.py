"""Prepare only PR218's owned current files; never mutate a provider or local Git."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

R = Path(__file__).resolve().parent
D = R.parent / 'initial_review_20261015'
S = D / 'submitted/unsolved_math_prioritization/attempts/30006020'
U = R / 'pr_update/30006020'
H = U / 'history/original_submission_20261001'
U.mkdir(parents=True, exist_ok=True)
pins = []
for p in sorted(S.rglob('*')):
    if not p.is_file():
        continue
    q = H / p.relative_to(S)
    q.parent.mkdir(parents=True, exist_ok=True)
    if q.exists():
        assert q.read_bytes() == p.read_bytes()
    else:
        shutil.copyfile(p, q)
    pins.append({'path': str(p.relative_to(S)), 'bytes': p.stat().st_size,
                 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
assert len(pins) == 22

original = (S / 'CANDIDATE.md').read_text()
text = original.replace(
    '**30006020 / OWR-14298589-005. Unreviewed full candidate, author turn 1.** The source\'s iterated sampling limit and principal-stratum scope are essential. No novelty or priority guarantee is made.',
    '**30006020 / OWR-14298589-005. Current credit revision, 2026-10-15.** Author proof turn 1/5. The mathematical core passed the separate source and proof audits; the credited preprint package is undergoing fresh sequential review. The source\'s iterated sampling limit and principal-stratum scope are essential. No universal first-priority guarantee is made. The complete original submission and its historical reviews are preserved byte-for-byte in `history/original_submission_20261001/`. Current status is in `FINAL_DISPOSITION.md`.'
)
anchor = 'These substantial geometric/enumerative results are credited inputs, not proved here. We derive the mesoscopic statements and the uniform-integrability transfer explicitly below.'
assert anchor in text
text = text.replace(anchor, anchor + '''

**Exact prior model and probability credit.** The composition law (1) is precisely DGZZ's existing weighted permutation law P_(n,∞,1/2), equations (1.7)–(1.8) and Lemma3.6, equations (3.20)–(3.23). The whole-area TV comparison is an extraction from DL's positive uniform monomial expansion, not a new geometric enumeration. Aggarwal's uniform intersection-number estimates underlie DL's coefficient input. Arratia–Tavaré (1994), Lemma5/(126), supplies the classical factorial identity (19). Arratia–Barbour–Tavaré (2000), Theorem3.1, already implies the unmarked mesoscopic Poisson conclusion at every q→∞, q=o(n), under the uniform logarithmic condition verified by Poisson means a_j. The elementary derivations below expose the uniformity; they are not claims of new assembly theory. The added consequence is the geometric all-rate Gamma-marked limit and its count-moment transfer.

**Earlier announcements and bounded priority finding.** Delecroix–Liu announced microscopic small-components work in DL p.5098 and OWR reference5, in preparation. Liu's 2022 thesis, *Random multi-geodesics on hyperbolic surfaces*, Remark1.5.9/p22, gives the all-multiplicity microscopic intensity and fixed windows at scale 1/(6g−6). His February2025 Durham slides26/195 concern primitive multigeodesics and label a microscopic version a conjecture. A fixed-window limit and its intensity tail do not themselves establish growing-window uniformity. The extensive public audit through 2026-10-15 did not locate a complete Small components manuscript or an explicit earlier same-ensemble geometric intermediate-window theorem. Unavailable contents remain a specific priority uncertainty. This supports a carefully credited consequence note answering the written intermediate-area question, not a universal first-priority certificate.
''')
text = text.replace('The macroscopic Poisson–Dirichlet law and the microscopic law cited in the source remain credited prior results, not new claims here.', 'The macroscopic Poisson–Dirichlet law is prior work; the microscopic theorem announced in the source and the thesis is also fully credited and is not a new claim here. No inference from its fixed-window formulation to moving windows is assumed.')
text += '''

[AT] R. Arratia and S. Tavaré, Independent process approximations for random combinatorial structures, Adv. Math.104 (1994),90–154. https://www.columbia.edu/cu/simontavare/STpapers-pdf/AT94.pdf

[ABT] R. Arratia, A.D. Barbour and S. Tavaré, Limits of logarithmic combinatorial structures, Ann. Probab.28 (2000),1620–1644. https://doi.org/10.1214/aop/1019160500

[Liu] M. Liu, Random multi-geodesics on hyperbolic surfaces, doctoral thesis, Université Paris Cité,2022. https://www.imj-prg.fr/theses/pdf/mingkun_liu.pdf

[Slides] M. Liu, Durham seminar slides,February2025,slides26/195. https://www.math.univ-paris13.fr/~mingkun.liu/talks/Durham.pdf

**Research status and assistance.** This is unrefereed research with no external human peer review or proof-assistant formalization. AI tools were used extensively in development, derivation, computation, literature research, writing and independent internal adversarial checking. Internal AI checking is not human peer review. The named human author is responsible for the submitted work; cited researchers did not participate in or endorse it.
'''
for start, end in [('## 3.', '## 10.')]:
    assert text[text.index(start):text.index(end)] == original[original.index(start):original.index(end)]
(U / 'CANDIDATE.md').write_text(text)
(U / 'SOURCE_AUDIT.md').write_text('''# Current source and priority boundary, 2026-10-15

The mathematical source target is accepted for the exact principal-quadratic iterated ensemble. The complete historical audit is preserved in history/original_submission_20261001/SOURCE_AUDIT.md; it is not resealed as a current review.

The current CANDIDATE.md and seven-page preprint give exact DGZZ1.7–1.8/Lemma3.6 credit for the composition law, DL3.2/6.1/Lemma6.4 credit for its geometric Gamma/Dirichlet extraction, DGZZ1.12/5.2 credit for exceptional counts, and Aggarwal credit through DL for uniform intersection numbers. AT1994 Lemma5/(126) and ABT2000 Theorem3.1 are prior probability inputs, not new discoveries here. The elementary probability proof remains self-contained.

The announced Delecroix–Liu Small components project, Liu2022 thesis Remark1.5.9 and Durham2025 primitive slides are explicitly credited. A complete public manuscript under that title was not located in the bounded audit. No inspected primary passage positively covers the same geometric moving-window conclusion; negative searches do not certify novelty, and unavailable contents remain a priority uncertainty. The final priority synthesis permits a credited consequence note, not universal first priority.

The natural exact Gamma total is6g−6. The unused OWR microscopic summary prints4g−4; the two fixed microscopic laws are not identified here. No new microscopic theorem, all-stratum theorem, primitive-cover assertion, all-direction joint law, diagonal sampling limit or rare-event relative-error result is claimed. Horizontal maximal cylinders are counted once, areas are normalized by total surface area, heights are unbounded, and N→∞ precedes g→∞.

Actual full-source hashes, proof/source acceptance and the four distinct mathematical review families and four priority comparisons are recorded in the audit directory draft_pr_descending_audit_20261002/audits/pr218_30006020/initial_review_20261015. Complete external payloads remain excluded. Finite computations supplement the proof and do not certify the published geometric inputs. AI tools were used extensively; the note is unrefereed without external human peer review.
''')
(U / 'FINAL_DISPOSITION.md').write_text('''# Current disposition: claimed_solved, publication preparation

The proof of the exact written OWR intermediate-area question passed independent source/mathematical review. Its positive conclusion is the principal-quadratic iterated-limit cylinder-area PPP(dx/(2x)) at every s_g→0, gs_g→∞, with all fixed joint compact-window count moments. The original window count tends to Poisson(log(2)/2), with the same limiting mean/variance.

The exact composition model, unmarked probability theorem and substantial geometric inputs are prior work and are now credited explicitly in CANDIDATE.md and the preprint. Extensive priority work supports a carefully credited consequence note; it does not certify universal first priority. Announced Delecroix–Liu microscopic work is acknowledged, and unavailable manuscript contents remain a specific priority uncertainty. The literal unused microscopic normalization discrepancy is retained.

Author proof budget remains1/5. Status remains claimed_solved. Publication, tracker and merge are pending a finished package and new sequential adversarial manuscript reviews. Historical author/reviewer files are preserved byte-for-byte under history/original_submission_20261001; their hashes and verdicts concern those frozen files, not newly authored credit or manuscript bytes.

This is unrefereed research using AI tools extensively for derivation, computation, literature review, writing and internal independent adversarial checking. No external human peer review or proof-assistant formalization is asserted.
''')
(U / 'README.md').write_text('''# Current source for problem30006020 / OWR-14298589-005

Read FINAL_DISPOSITION.md, CANDIDATE.md and SOURCE_AUDIT.md for the current precisely credited conclusion. The mathematical core CANDIDATE sections3–9 is unchanged from the original accepted proof. Preprint materials are prepared separately and remain unpublished until explicit final clearance.

history/original_submission_20261001 contains all22 original files byte-for-byte, including old manifests and reviews. Run historical hash checks relative to that preserved historical root. Those historical reviews were never silently rewritten or presented as reviews of a different file hash. CURRENT_SOURCE_MANIFEST.json records the new current artifacts and full original archive pins.
''')
(U / 'RESEARCH_LOG.md').write_text(datetime.now(timezone.utc).isoformat() + ' — case55%: mathematical/source PASS; extensive priority audit permits a credited consequence note. This preparation archives all22 original artifacts and corrects exact DGZZ/ABT/AT and announcement credit globally. Proof core unchanged; fresh sequential manuscript review, publication, tracker and merge pending.\n')
manifest = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'credited_current_source_prepared_for_manuscript_review', 'original_PR_head': 'dc457c741c779fbf90fbfdcdc73f750b3716f561', 'proof_core_sections3_to9_byte_identical': True, 'original_submission_files': pins, 'current_files': []}
for p in sorted(U.iterdir()):
    if p.is_file() and p.name != 'CURRENT_SOURCE_MANIFEST.json':
        manifest['current_files'].append({'path': p.name, 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
(U / 'CURRENT_SOURCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'original_files_archived': len(pins), 'current_files_prepared': len(manifest['current_files']), 'proof_core_byte_identical': True}))
