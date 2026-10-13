"""Prepare this expository note's source and authored-audit package once."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
PUB = HERE / 'publication'
TITLE = 'Original-ball paths in Teichmüller space: an elementary corollary of Lenzhen–Rafi'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    if (PUB / 'metadata.json').exists():
        raise RuntimeError('Package already prepared; preserve review state')
    for name in ('research_note.tex', 'research_note.pdf'):
        if not (PUB / name).is_file():
            raise RuntimeError('Compile the authored note first')
    evidence = PUB / 'evidence'
    evidence.mkdir(exist_ok=True)
    shutil.copytree(HERE / 'submitted', evidence / 'submitted')
    copied = []
    root_names = ('SUBMITTED_PINS.json', 'ROOT_MATH_AUDIT.md', 'ROOT_METRIC_DERIVATION.md',
                  'ROOT_MATH_ACCEPTANCE.json', 'ROOT_PRIORITY_ADOPTION.json',
                  'history/ROOT_MATH_AUDIT_before_title_correction.md')
    pairs = [(HERE / n, evidence / n) for n in root_names]
    for family in ('metric_01', 'teich_source_01', 'priority_01'):
        directory = HERE / 'reviews' / family
        for source in sorted(directory.rglob('*')):
            if not source.is_file():
                continue
            relative = source.relative_to(directory)
            if {'raw', '__pycache__', '.venv', 'render', 'tmp'} & set(relative.parts):
                continue
            if source.suffix in {'.pdf', '.png', '.zip', '.pyc'}:
                continue
            pairs.append((source, evidence / family / relative))
    for source, target in pairs:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        copied.append({'path': target.relative_to(PUB).as_posix(),
                       'audit_source_path': source.relative_to(HERE).as_posix(),
                       'bytes': target.stat().st_size, 'sha256': sha(target)})
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(evidence / 'AUDIT_COPY_MANIFEST.json', {
        'utc': now, 'copied_authored_bytes_unchanged': True,
        'third_party_raw_bodies_omitted': True,
        'historical_manifests_describe_their_input_stages': True, 'files': copied})
    (PUB / 'README.md').write_text('''# Original-ball paths in Teichmüller space: an elementary corollary of Lenzhen–Rafi

Alec Kriebel, independent researcher; ORCID
[0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).
Version 1.0, 13 October 2026. Unrefereed expository preprint.

The [paper](research_note.pdf) and [TeX source](research_note.tex) spell out
an elementary consequence of Lenzhen–Rafi's established uniform radial
quasiconvexity theorem. For each fixed closed oriented genus g >= 2,
every original closed Teichmüller ball contains a continuous rectifiable
path between every pair x,y, of length at most d_T(x,y) + 4c_g. One finite
c_g works for every center, radius and pair at that genus. This gives an
affirmative derivation of Farb's Question 3.5 from prior geometry.

The work is explicitly expository. No new substantive Teichmüller theorem,
historical firstness, current worldwide openness, numerical constant,
genus-uniform bound or optimal Teichmüller constant is claimed. The
general retreat lemma's publication priority is also unestablished.
See the [scope and source supplement](SUPPLEMENT.md),
[evidence index](evidence/INDEX.md), [metadata](metadata.json) and
[file inventory](PACKAGE_MANIFEST.json).

The original submission is theoretical and includes no executable checker.
The verification materials are complete written derivations, independent
adversarial reports, source identities and locators, boundary models, and
byte-preserved original documents. They require reading the proof and
cited published theorem interfaces; they do not promise a computational
or proof-assistant certificate. Third-party paper bodies are omitted.

AI tools were used extensively in deriving, verifying, source auditing and
preparing the result. AI adversarial reviews are not conventional human
peer review or journal acceptance. A NEW independent whole-package review
and any resulting repair loops remain pending before immutable publication.
''')
    (PUB / 'SUPPLEMENT.md').write_text('''# Scope, prior theorem and verification supplement

This supplement accompanies the version 1.0 expository note dated
13 October 2026. Its extensive-AI and unrefereed disclosures apply throughout.

The exact setting is marked Teichmüller space of a fixed closed oriented
surface of genus g >= 2, with the actual half-log metric. All original
closed balls, centers, finite radii and endpoint pairs are included. The
constructed path has length at most the ambient distance plus 4c_g, where
c_g can be half the logarithm of Lenzhen–Rafi's topology-only extremal-length
constant K_g >= 1. No numerical or genus-uniform value is supplied.

For R >= c_g, retreat each endpoint radially by the lesser of its radial
distance and c_g. The new endpoints have radius at most R - c_g. Their
minimizing segment stays in radius R by the established radial theorem;
the radial ends also stay in that original ball. The total length is at
most d(x,y) + 2alpha + 2beta <= d(x,y) + 4c_g. For R < c_g, the path
through the center suffices. R = c_g, R = 0, c_g = 0, coincident endpoints,
collapsed middle segments and endpoints at the center are covered. An
actual path is constructed; no intrinsic-distance infimum is assumed attained.

Lenzhen–Rafi's title is *Length of a curve is quasi-convex along a
Teichmüller geodesic*, JDG 88 (2011), 267–295. The published extremal-length
and ball theorems are 15 and 17; the earlier arXiv:1002.3939v1 body uses
13 and 15. Uniformity is over every curve and every geodesic endpoint and
intermediate point at the fixed topology, with no thickness restriction.
Kerckhoff's distance formula, checked also at Fortier Bourque–Rafi v3
Section 2, equation (2.2), gives the non-strict radial inequality by taking
curve suprema. No maximizing curve or foliation is required. The external
foundational source proofs are not all reproved here.

The complete theorem is a straightforward implicit corollary of that prior
geometry. A bounded priority audit with 45 queries and 26 inspected source
page renders located no explicit full-scope predecessor in the bodies
checked. This is not proof of absence, firstness or current openness.
Cannon's original 1987 body was inaccessible; the general lemma's
historical priority and exhaustive coverage remain unestablished. Those
gaps preclude novelty claims and are retained in the authored audit.

Farb's original distance-two question is on printed pages 24–25 of the
2006 book. Nonconvex minimizing segments from Fortier Bourque–Rafi are
compatible with the three-piece path. Petyt–Zalloum's 2024/2026 Theorem I
gives N(k) = k + 6 in a dual wall metric, whose map from the original
space is quasiisometric. It does not identify original Teichmüller balls
or continuous path lengths. There is no cross-metric constant improvement
claim. The generic circle model in the separate metric review is an
adversarial boundary model, not a novelty or Teichmüller-optimality claim
of this preprint.

All eight authored original files at PR #1033 head
6322305d37b8131f034a1b4c3c5e861e4b04844f are preserved byte-for-byte.
The root and two distinct fresh mathematical families verified the
metric construction and exact source interface; their conditional
obligations are mutually discharged. The new priority family independently
compared prior bodies before the old priority verdict. Original acceptance
labels and historical reports are stage records, not current publication
gates. A bibliographic title error in the root record was corrected;
the before-stage bytes are retained for the frozen priority input pins.

The [evidence index](evidence/INDEX.md) maps current and historical records.
Source byte identities establish which editions were inspected, not
mathematical truth. No original computation was submitted or replayed.
Raw third-party PDF/text/images and local own-PDF renders are excluded.
The supporting package remains subject to a NEW whole-package adversarial
review and repair loop before immutable publication.
''')
    (evidence / 'INDEX.md').write_text('''# Evidence index and stage mapping

Links are relative to this file. The eight original documents are preserved
unchanged. Fresh authored audit records preserve their original input stages;
absolute local locators and omitted raw-body paths are historical provenance,
not portable file dependencies or claimed included third-party papers.

- [Original pins](SUBMITTED_PINS.json), [original proof](submitted/PROOF.md),
  [original audited version](submitted/PROOF_AUDITED.md) and
  [original source identities](submitted/SOURCES.json).
- [Root metric derivation](ROOT_METRIC_DERIVATION.md),
  [combined mathematical audit](ROOT_MATH_AUDIT.md),
  [mathematical acceptance](ROOT_MATH_ACCEPTANCE.json).
- [Independent metric report](metric_01/REPORT.md),
  [derivation](metric_01/DERIVATION.md),
  [adversarial boundary models](metric_01/ADVERSARIAL_MODELS.md),
  [verdict](metric_01/VERDICT.json).
- [Independent exact-source report](teich_source_01/REPORT.md),
  [source derivation](teich_source_01/DERIVATION.md),
  [verdict](teich_source_01/VERDICT.json),
  [primary source manifest](teich_source_01/SOURCE_MANIFEST.json).
- [New bounded priority report](priority_01/REPORT.md),
  [verdict](priority_01/VERDICT.json), [query ledger](priority_01/QUERY_LEDGER.json),
  [source manifest](priority_01/SOURCE_MANIFEST.json),
  [root expository framing adoption](ROOT_PRIORITY_ADOPTION.json).
- [Root audit before title correction](history/ROOT_MATH_AUDIT_before_title_correction.md)
  supplies the before-stage bytes pinned by the priority review. The
  current audit corrects only the Lenzhen–Rafi title; the mathematics is unchanged.
- [Unchanged authored-copy pins](AUDIT_COPY_MANIFEST.json),
  [current review state](CURRENT_REVIEW_STATE.json),
  [current layout receipt](PDF_LAYOUT_RECEIPT.json),
  [paper](../research_note.pdf), [source](../research_note.tex),
  [supplement](../SUPPLEMENT.md), [metadata](../metadata.json),
  [inventory](../PACKAGE_MANIFEST.json).

The root mathematical acceptance's output hashes describe its earlier review
stage. The current copy manifest pins the authored copies actually included.
The current paper is an expository corollary of the established LR theorem.
No earlier PASS or acceptance constitutes current zero-issue package clearance;
a NEW full package review remains pending.
''')
    metadata = {
        'title': TITLE, 'upload_type': 'publication', 'publication_type': 'preprint',
        'creators': [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher',
                      'orcid': '0009-0001-9320-500X'}],
        'access_right': 'open', 'license': 'cc-by-4.0', 'publication_date': '2026-10-13',
        'version': '1.0', 'language': 'eng',
        'keywords': ['Teichmüller metric', 'closed balls', 'almost convexity',
                     'Farb Question 3.5', 'geodesic paths', 'expository corollary', 'unrefereed preprint'],
        'description': (
            '<p>An explicitly expository original-ball path corollary of Lenzhen–Rafi’s established uniform quasiconvexity theorem. For each fixed closed oriented surface of genus at least two, every pair of points in any original closed half-log Teichmüller ball has a continuous rectifiable path inside that same ball with length at most its ambient distance plus 4c_g. One finite topology-dependent c_g works for all centers, radii and pairs. Radial endpoint retreat followed by a minimizing segment gives the deduction and an affirmative derivation of Farb’s Question 3.5 from prior geometry.</p>'
            '<p>All substantive Teichmüller estimates are credited to Lenzhen–Rafi. Historical priority for the elementary lemma and exact corollary is unestablished; no new substantive theorem, worldwide firstness, current openness, numerical or genus-uniform constant, or optimal Teichmüller bound is claimed. Kerckhoff’s formula and Fortier Bourque–Rafi’s metric and nonconvexity interfaces are credited. Petyt–Zalloum’s 2024/2026 dual wall-space almost convexity uses a different metric, with no comparison of numerical constants. A bounded priority audit does not certify absence of prior work.</p>'
            '<p>The deposit includes the full proof, TeX source, scope supplement, byte-preserved theoretical original and authored independent adversarial mathematical and source audits. No original executable was submitted; these are written verification materials, not a computational or proof-assistant certificate. Third-party paper bodies are omitted. AI tools were used extensively in deriving, verifying, adversarial review, source auditing and preparation. This is an unrefereed expository preprint; conventional human peer review and journal acceptance are not claimed.</p>'),
        'references': [
            'B. Farb, Some problems on mapping class groups and moduli space, in Problems on Mapping Class Groups and Related Topics (2006), pp. 24–25, Question 3.5. https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf',
            'A. Lenzhen and K. Rafi, Length of a curve is quasi-convex along a Teichmüller geodesic, J. Differential Geom. 88 (2011), 267–295, Theorems C, 15 and 17. https://www.math.toronto.edu/rafi/Papers/Convexity.pdf',
            'S. P. Kerckhoff, The asymptotic geometry of Teichmüller space, Topology 19 (1980), 23–41. https://doi.org/10.1016/0040-9383(80)90029-4',
            'M. Fortier Bourque and K. Rafi, Non-convex balls in the Teichmüller metric, J. Differential Geom. 110 (2018), 379–412; arXiv:1606.05170v3 (2017). https://arxiv.org/abs/1606.05170v3',
            'H. Petyt and A. Zalloum, Constructing metric spaces from systems of walls, Math. Ann. 396, article 38 (2026), Theorem I; arXiv:2404.12057v1 (2024) and v2 (2026). https://doi.org/10.1007/s00208-026-03534-1'],
    }
    save(PUB / 'metadata.json', metadata)
    save(evidence / 'CURRENT_REVIEW_STATE.json', {
        'utc': now, 'math': 'Root and two fresh distinct mathematical families passed',
        'priority': 'Eligible as expository corollary only; historical firstness unestablished',
        'required_global_expository_framing_applied': True,
        'fresh_package_reviews': [], 'all_actionable_issues_resolved': False,
        'preprint_ready_for_immutable_publication': False, 'published': False,
        'next_gate': 'NEW independent whole-package review 01'})
    save(evidence / 'PDF_LAYOUT_RECEIPT.json', {
        'utc': now, 'source_sha256': sha(PUB / 'research_note.tex'),
        'pdf_sha256': sha(PUB / 'research_note.pdf'), 'pdf_bytes': (PUB / 'research_note.pdf').stat().st_size,
        'pages': 3, 'all_pages_rendered_and_viewed_by_root': True,
        'desktop_compiler': 'SUCCESS', 'terminal_export': 'tectonic 0.16.9 SUCCESS',
        'actual_warnings_undefined_or_overfull': [],
        'package_infwarerr_information_line_is_not_a_warning': True,
        'current_paper_status': 'Unrefereed exposition; fresh whole-package review pending'})
    print(json.dumps({'copied_authored_records': len(copied), 'original_files': 8,
                      'title': TITLE, 'pdf_sha256': sha(PUB / 'research_note.pdf')}))


if __name__ == '__main__':
    main()
