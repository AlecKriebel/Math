"""Apply the two frozen first-review prose repairs, preserving mathematics."""
import datetime
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUB = HERE / 'publication'
EVIDENCE = PUB / 'evidence'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    if (EVIDENCE / 'REPAIR_RECORD_01.json').exists():
        raise RuntimeError('Repairs already applied; do not reset review state')
    review = HERE / 'reviews/package_01'
    verdict = json.loads((review / 'VERDICT.json').read_text())
    if verdict['status'] != 'REPAIR_REQUIRED' or {r['id'] for r in verdict['issues']} != {'PK01', 'PK02'}:
        raise RuntimeError('Frozen review differs')
    frozen_paths = [PUB / 'research_note.tex', PUB / 'research_note.pdf',
                    PUB / 'run_checks.py', *sorted((PUB / 'checks').rglob('*'))]
    before = {p.relative_to(PUB).as_posix(): sha(p) for p in frozen_paths if p.is_file()}
    old_metadata_sha = sha(PUB / 'metadata.json')
    copied = []
    for source in sorted(review.rglob('*')):
        if not source.is_file():
            continue
        relative = source.relative_to(review)
        if any(part in relative.parts for part in ('raw', 'extracted', 'render', '__pycache__')):
            continue
        if source.suffix in {'.pdf', '.png', '.zip', '.pyc'}:
            continue
        target = EVIDENCE / 'package_review_01' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        copied.append({'path': target.relative_to(PUB).as_posix(),
                       'bytes': target.stat().st_size, 'sha256': sha(target)})
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(EVIDENCE / 'PACKAGE_REVIEW_01_COPY.json', {
        'utc': now, 'all_copied_bytes_unchanged': True,
        'excluded': 'raw third-party bodies, own-PDF renders, duplicate extracted input archive and caches',
        'historical_manifests_describe_original_review_inputs': True, 'files': copied})
    supplement = PUB / 'SUPPLEMENT.md'
    text = supplement.read_text()
    old = ('They are certificate faults, not defective-source algorithm mutations. Modes')
    if old not in text:
        raise RuntimeError('Expected certificate-fault scope marker differs')
    scope_old = ('Faults alter actual embedding/minor/projector certificate values\n'
                 'and must reject for the intended mathematical reason, not an unrelated crash.')
    scope_new = ('The faults alter embedding coefficients or certificate structure and metadata,\n'
                 'and must reject for the intended reason, not an unrelated crash. The three\n'
                 'unchanged baselines also check the full polynomial projector and mixed-minor\n'
                 'identities. The fifteen fault families comprise six coordinate faults and\n'
                 'nine structure/metadata faults; they reject before those latter identity checks.')
    if text.count(scope_old) != 1:
        raise RuntimeError('Coverage repair anchor differs')
    supplement.write_text(text.replace(scope_old, scope_new))
    replacements = {
        'Version1.0': 'Version 1.0', 'version1.0': 'version 1.0',
        '12October2026': '12 October 2026', 'Question6.5': 'Question 6.5',
        'OWR13/2015': 'OWR 13/2015', 'catalogue30002816': 'catalogue 30002816',
        'pp708': 'pp. 708', 'n<=7': 'n <= 7', 'Theorem1': 'Theorem 1',
        'published2021': 'published 2021', 'public2019': 'public 2019',
        'all225Hermitian': 'all 225 Hermitian', 'one quarter in': 'one quarter in',
        'C6': 'C^6', 'C3+C3': 'C^3 + C^3', '2009Section3.1exact': '2009 Section 3.1 exact',
        'the2010slides': 'the 2010 slides', '2013chapter': '2013 chapter',
        'a496-square': 'a 496-square', 'trace to2': 'trace to 2',
        'All29original': 'All 29 original', 'all29original': 'all 29 original',
        'All29authored': 'All 29 authored', 'complete29file': 'complete 29-file',
        'All29': 'All 29', '29authored': '29 authored',
        'all25425upper-triangle': 'all 25,425 upper-triangle',
        'full495coordinate': 'full 495-coordinate', 'with11760nonzero': 'with 11,760 nonzero',
        'in24real': 'in 24 real', 'and16hostile': 'and 16 hostile',
        '48executions': '48 executions', '3unchanged': '3 unchanged',
        '45executed': '45 executed', 'fifteen families': 'fifteen families',
        'three baselines and45': 'three baselines and 45',
        'the48run': 'the 48-run', 'the48-run': 'the 48-run',
        '48run': '48-run', 'full receipt': 'full receipt',
        'Python3.10': 'Python 3.10', 'Python3.14': 'Python 3.14',
        'Pythonflags': 'Python flags', 'Python3.10+standardlibrary': 'Python 3.10+ standard library',
        'Python 3.10+standardlibrary': 'Python 3.10+ standard library',
        'UID1000': 'UID 1000', 'specialUID': 'special UID',
        'ran84focused': 'ran 84 focused', 'records84focused': 'records 84 focused',
        'and25successful': 'and 25 successful', 'all84queries': 'all 84 queries',
        'first-Moment': 'first-moment', 'at(k,n)': 'at (k,n)',
        'splits as': 'splits as', 'All29original pins': 'All 29 original pins',
        'all 29original': 'all 29 original', 'Root48run': 'Root 48-run',
        'Root48-run': 'Root 48-run', 'NEWwhole': 'NEW whole',
        'coefficient list': 'coefficient list',
    }
    for filename in ('README.md', 'SUPPLEMENT.md', 'evidence/INDEX.md'):
        path = PUB / filename
        text = path.read_text()
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text)
    metadata = json.loads((PUB / 'metadata.json').read_text())
    metadata['description'] = (
        '<p>An application of Fawzi’s established finite semidefinite lift obstruction for normalized complex separable states to the oriented real Grassmann orbitope C(4,12), the mass ball in the fourth exterior power of real 12-space. Two affine hyperplanes select a section real-linearly isomorphic to Sep(3,3). This mass ball has no finite projected semidefinite lift of any size. A compact first-moment argument refutes the universal degree-at-most-one supporting sum-of-squares assertion in Sanyal’s Oberwolfach Report 13/2015, pp. 708–709, in joint work with Rostalski. It gives a negative answer in general to Harvey–Lawson Question 6.5: some constant closed comass-one four-form has no pointwise or local norm completion.</p>'
        '<p>The conclusion is existential. A failing unnormalized functional with rational coefficients exists, but no explicit coefficient list, exact comass, rational normalized calibration, least dimension or low-dimensional classification is supplied. Classical Wirtinger and Kähler faces, established fermionic projector bodies, Vrana–Lévay’s tensor-to-wedge decomposability lemma, theta-body and lift frameworks, and the earlier Sanyal–Rostalski equivalence are credited. Fawzi supplies the decisive no-lift theorem, public in 2019 and published in 2021; it is not reproved. Nearby quadratic Grassmann cones and unprojected LMI obstructions concern different embeddings or conclusions. A bounded priority comparison, with 84 queries and 25 primary PDF retrievals, found no full target predecessor in inspected bodies. Worldwide priority and current worldwide openness remain unestablished.</p>'
        '<p>The deposit includes the proof, TeX source, scope and priority supplement, authored independent adversarial audits and portable exact symbolic arithmetic verification (Python 3.10 or later, standard library only). The three unchanged symbolic baselines verify the full coordinate, polynomial projector and mixed-minor identities. Forty-five defective-certificate executions test embedding coefficients and certificate structure or metadata; they reject before the latter identity checks. Finite checks do not replace the written proof or Fawzi’s theorem. AI tools were used extensively in solving, verifying, source auditing and preparation. This is an unrefereed preprint with AI adversarial reviews; conventional human peer review, journal acceptance and formal proof-assistant certification are not claimed.</p>')
    metadata['keywords'] = [item.replace('Question6.5', 'Question 6.5') for item in metadata['keywords']]
    metadata['references'] = [
        'R. Sanyal, Grassmann orbitopes, Oberwolfach Report 13/2015, 707–709. https://ems.press/content/serial-article-files/46561',
        'R. Harvey and H. B. Lawson, Jr., Calibrated geometries, Acta Math. 148 (1982), 47–157; Question 6.5.',
        'H. Fawzi, The set of separable states has no finite semidefinite representation except in dimension 3x2, Commun. Math. Phys. 386 (2021), 1319–1335; Theorem 1. https://doi.org/10.1007/s00220-021-04163-2; arXiv:1905.02575v1 (2019).',
        'A. Barvinok and G. Blekherman, Convex geometry of orbits, MSRI Publications 52 (2005), 51–78.',
        'P. Vrana and P. Lévay, Special entangled quantum systems and the Freudenthal construction, arXiv:0902.2269v2 (2009), Section 3.1.',
        'J. Grabowski, M. Kuś and G. Marmo, Segre maps and entanglement for multipartite systems of indistinguishable particles, J. Phys. A 45 (2012), 105301.',
        'J. Gouveia, P. A. Parrilo and R. R. Thomas, Theta bodies for polynomial ideals, SIAM J. Optim. 20 (2010), 2097–2118; Lifts of convex sets and cone factorizations, Math. Oper. Res. 38 (2013), 248–264.',
        'P. Rostalski, SDP relaxations for the Grassmann orbitope, BIRS slides, 15 February 2010; J. Gouveia and R. R. Thomas, Spectrahedral approximations of convex hulls of algebraic sets, SIAM book chapter 7 (2013), p. 323.',
        'R. G. Bettiol, M. Kummer and R. A. E. Mendes, Convex algebraic geometry of curvature operators, SIAM J. Appl. Algebra Geom. 5 (2021), 200–228; Corollary 4.2.',
        'G. Blekherman, G. G. Smith and M. Velasco, Sums of squares and varieties of minimal degree, J. Amer. Math. Soc. 29 (2016), 893–913.',
        'R. Sanyal, F. Sottile and B. Sturmfels, Orbitopes, Mathematika 57 (2011), 275–314; Theorem 7.6.',
        'H. Fawzi, J. Gouveia, P. A. Parrilo, J. Saunderson and R. R. Thomas, Lifting for simplicity: concise descriptions of convex sets, SIAM Review 64 (2022); arXiv:2002.09788v2.']
    save(PUB / 'metadata.json', metadata)
    with (PUB / 'README.md').open('a') as file:
        file.write('\nThe first NEW whole-package review verified the complete mathematics and\n'
                   'found two P3 prose repairs: precise negative-control coverage and spacing.\n'
                   'Both have been applied; a NEW second independent review is required.\n')
    with (EVIDENCE / 'INDEX.md').open('a') as file:
        file.write('\n[First fresh package review](package_review_01/REVIEW.md),\n'
                   '[verdict](package_review_01/VERDICT.json),\n'
                   '[unchanged copy pins](PACKAGE_REVIEW_01_COPY.json) and\n'
                   '[current prose repairs](REPAIR_RECORD_01.json) record this stage.\n'
                   'Input manifests describe the original review candidate. Raw source bodies,\n'
                   'own render images and duplicate extracted packages are omitted.\n'
                   'The current paper and arithmetic bytes remain unchanged; metadata and\n'
                   'prose have been repaired. A NEW second package review remains pending.\n')
    save(EVIDENCE / 'REPAIR_RECORD_01.json', {
        'utc': now, 'issues_applied': ['PK01', 'PK02'],
        'PK01': 'Accurate six coordinate/nine structure-metadata certificate fault coverage; full polynomial identities checked by unchanged baselines, not directly faulted by the portable negatives.',
        'PK02': 'Current README, supplement, index and metadata copyedited; deposit wrapper synchronized by deterministic builder.',
        'mathematical_source_pdf_checkers_unchanged': before,
        'old_metadata_sha256': old_metadata_sha, 'new_metadata_sha256': sha(PUB / 'metadata.json'),
        'historical_and_original_bytes_unchanged': True,
        'independent_recheck_pending': True})
    state = json.loads((EVIDENCE / 'CURRENT_REVIEW_STATE.json').read_text())
    state['fresh_package_reviews'] = [{'round': 1, 'status': 'REPAIR_REQUIRED',
        'actionable_P3_issues': 2, 'root_repairs': 'REPAIR_RECORD_01.json',
        'input_archive_sha256': verdict['zip_sha256']}]
    state['next_gate'] = 'NEW independent whole-package review 02'
    save(EVIDENCE / 'CURRENT_REVIEW_STATE.json', state)
    if any(sha(PUB / name) != value for name, value in before.items()):
        raise RuntimeError('Mathematical source/PDF/checker bytes changed')
    print(json.dumps({'repairs_applied': ['PK01', 'PK02'],
                      'unchanged_review_files_copied': len(copied),
                      'mathematics_pdf_checkers_unchanged': True}))


if __name__ == '__main__':
    main()
