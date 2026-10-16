"""Assemble first candidate, preserving authored provenance and source metadata."""
import datetime
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUB = HERE / 'publication'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def copy_tree(source, destination):
    for path in source.rglob('*'):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        if 'raw' in relative.parts or '__pycache__' in relative.parts:
            continue
        if path.suffix in {'.png', '.pdf', '.zip', '.pyc'}:
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())


def main():
    if (PUB / 'evidence/CURRENT_REVIEW_STATE.json').exists():
        raise RuntimeError('Candidate already assembled; do not reset review state')
    evidence = PUB / 'evidence'
    copy_tree(HERE / 'submitted', evidence / 'submitted')
    for name in ('SUBMITTED_PINS.json', 'ROOT_MATH_AUDIT.md',
                 'ROOT_MATH_NOTES.md', 'ROOT_PRIORITY_ADOPTION.json'):
        (evidence / name).parent.mkdir(parents=True, exist_ok=True)
        (evidence / name).write_bytes((HERE / name).read_bytes())
    for source, target in [('geometry_01', 'geometry_review_01'),
                           ('sos_lift_01', 'sos_lift_review_01'),
                           ('priority_01', 'priority_review_01')]:
        copy_tree(HERE / 'reviews' / source, evidence / target)
    copy_tree(HERE / 'root_reproduction', evidence / 'root_reproduction')
    (PUB / 'checks').mkdir(exist_ok=True)
    (PUB / 'expected').mkdir(exist_ok=True)
    for name in ('audit_exact_embedding.py', 'EMBEDDING_CERTIFICATE.json'):
        (PUB / 'checks' / name).write_bytes((HERE / 'submitted/current' / name).read_bytes())
    (PUB / 'expected/ROOT_FINITE_REPRODUCTION.json').write_bytes(
        (HERE / 'root_reproduction/FINITE_REPRODUCTION.json').read_bytes())
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(evidence / 'CURRENT_REVIEW_STATE.json', {
        'utc': now, 'math': 'root plus independent geometry and SOS/source families passed',
        'priority': 'bounded no-match; all nine required credit/framing fixes adopted',
        'fresh_package_reviews': [], 'preprint_ready_for_immutable_publication': False,
        'all_actionable_issues_resolved': False, 'published': False,
        'next_gate': 'NEW independent whole-package adversarial review'})
    adoption = json.loads((HERE / 'ROOT_PRIORITY_ADOPTION.json').read_text())
    adoption['global_paper_adoption_complete'] = True
    adoption['fresh_whole_package_review_required'] = True
    adoption['current_artifacts'] = ['research_note.tex', 'research_note.pdf',
                                   'README.md', 'SUPPLEMENT.md', 'metadata.json']
    save(HERE / 'ROOT_PRIORITY_ADOPTION.json', adoption)
    save(evidence / 'ROOT_PRIORITY_ADOPTION.json', adoption)
    metadata = {
        'title': 'An application of separable-state nonrepresentability to Grassmann orbitopes and calibrations',
        'upload_type': 'publication', 'publication_type': 'preprint',
        'description': '<p>An application of Fawzi’s established finite-semidefinite-lift obstruction for normalized complex separable states to the oriented real Grassmann orbitope C(4,12), the mass ball in the fourth exterior power of R12. Two affine hyperplanes select a section real-linearly isomorphic to Sep(3,3). Thus this mass ball admits no finite projected semidefinite lift of any size. A compact first-moment argument refutes the universal degree-at-most-one supporting sum-of-squares assertion in Sanyal’s Oberwolfach Report13/2015, pp.708–709, in joint work with Rostalski. It gives a negative answer in general to Harvey–Lawson Question6.5: some constant closed comass-one four-form on R12 has no pointwise or local norm completion.</p><p>The conclusion is existential. A failing unnormalized functional with rational coefficients exists, but no explicit coefficient list, exact comass, rational normalized calibration, least dimension or low-dimensional classification is supplied. Classical Wirtinger/Kähler faces, established fermionic projector bodies, Vrana–Lévay’s tensor-to-wedge decomposability lemma, theta-body/moment and lift frameworks, and the earlier Sanyal–Rostalski equivalence are credited. The decisive no-lift theorem is Fawzi’s, public in2019 and published in2021; it is not reproved. Nearby quadratic Grassmann cones and unprojected-LMI obstructions have distinct embeddings or conclusions. A bounded84-query/25-primary-PDF priority comparison found no full target predecessor in inspected bodies; worldwide priority and current worldwide openness remain unestablished.</p><p>The deposit includes the proof, TeX source, scope/priority supplement, authored independent adversarial audits and portable exact symbolic arithmetic verification (Python3.10 or later, standard library only). Coordinate identities and defective-certificate controls corroborate the elementary bridge; finite checks do not replace the written proof or Fawzi’s theorem. AI tools were used extensively in solving, verifying, source auditing and preparation. This is an unrefereed preprint with AI adversarial reviews; conventional human peer review, journal acceptance and formal proof-assistant certification are not claimed.</p>',
        'creators': [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher',
                      'orcid': '0009-0001-9320-500X'}],
        'access_right': 'open', 'license': 'cc-by-4.0',
        'publication_date': '2026-10-12', 'version': '1.0', 'language': 'eng',
        'keywords': ['Grassmann orbitope', 'mass ball', 'calibration', 'Harvey-Lawson Question6.5',
                     'semidefinite lift', 'separable states', 'affine sum of squares',
                     'Kähler face', 'theta body', 'unrefereed preprint'],
        'references': [
            'R. Sanyal, Grassmann orbitopes, Oberwolfach Report13/2015,707–709. https://ems.press/content/serial-article-files/46561',
            'R. Harvey and H. B. Lawson,Jr., Calibrated geometries, Acta Math.148(1982),47–157; Question6.5.',
            'H. Fawzi, The set of separable states has no finite semidefinite representation except in dimension3x2, Commun.Math.Phys.386(2021),1319–1335; Theorem1. https://doi.org/10.1007/s00220-021-04163-2; arXiv:1905.02575v1(2019).',
            'A. Barvinok and G. Blekherman, Convex geometry of orbits, MSRIPublications52(2005),51–78.',
            'P. Vrana and P. Lévay, Special entangled quantum systems and the Freudenthal construction, arXiv:0902.2269v2(2009),Section3.1.',
            'J. Grabowski,M. Kuś and G. Marmo, Segre maps and entanglement for multipartite systems of indistinguishable particles, J.Phys.A45(2012),105301.',
            'J. Gouveia,P. A. Parrilo and R. R. Thomas, Theta bodies for polynomial ideals, SIAMJ.Optim.20(2010),2097–2118; Lifts of convex sets and cone factorizations, Math.Oper.Res.38(2013),248–264.',
            'P. Rostalski, SDP relaxations for the Grassmann orbitope, BIRSslides,15February2010; J. Gouveia and R. R. Thomas, Spectrahedral approximations of convex hulls of algebraic sets, SIAMbookchapter7(2013),p323.',
            'R. G. Bettiol,M. Kummer and R. A. E. Mendes, Convex algebraic geometry of curvature operators, SIAMJ.Appl.AlgebraGeom.5(2021),200–228; Corollary4.2.',
            'G. Blekherman,G. G. Smith and M. Velasco, Sums of squares and varieties of minimal degree, JAMS29(2016),893–913.',
            'R. Sanyal,F. Sottile and B. Sturmfels, Orbitopes, Mathematika57(2011),275–314; Theorem7.6.',
            'H. Fawzi,J. Gouveia,P. A. Parrilo,J. Saunderson and R. R. Thomas, Lifting for simplicity: concise descriptions of convex sets, SIAMReview64(2022); arXiv:2002.09788v2.']}
    save(PUB / 'metadata.json', metadata)
    print(json.dumps({'assembled': True, 'original_files': 29,
                      'fresh_package_review_pending': True,
                      'third_party_raw_redistributed': False}))


if __name__ == '__main__':
    main()
