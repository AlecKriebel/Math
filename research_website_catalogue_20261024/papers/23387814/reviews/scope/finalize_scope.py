from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parent.parent
SOURCES = PAPER / 'sources'
PACKAGE = SOURCES / 'published-source/seshadri_counterexample_verification'
NOW = datetime.now(timezone.utc).isoformat()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

record = json.loads((SOURCES / 'record.json').read_text())
receipt = json.loads((SOURCES / 'receipt.json').read_text())
texpath = PACKAGE / 'seshadri_counterexample.tex'
tex = texpath.read_text()
rawabstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
(ROOT / 'abstract.tex').write_text(rawabstract + '\n')
abstract = ' '.join(rawabstract.split())
replacements = {
    r'$\eps(S,L;x)\ge (2+|K_S^2|^{1/4})^{-1}$': 'ε(S,L;x) ≥ (2+|K_S²|^(1/4))⁻¹',
    r'$d\ge7$': 'd ≥ 7',
    r'$K_S^2=6(d-1)(d-3)$': 'K_S² = 6(d−1)(d−3)',
    '$L$': 'L',
    '$L^2=6$': 'L² = 6',
    r'$\eps(S,L;x)\le1/(d-1)$': 'ε(S,L;x) ≤ 1/(d−1)',
    '$d=7$': 'd = 7',
}
for before, after in replacements.items():
    assert before in abstract, before
    abstract = abstract.replace(before, after)
assert '\\' not in abstract and '$' not in abstract
(ROOT / 'abstract.txt').write_text(abstract + '\n')
save('abstract-receipt.json', {
    'created_utc': NOW, 'source_tex': str(texpath.relative_to(PAPER)),
    'source_tex_sha256': sha(texpath), 'source_lines': [19, 27],
    'abstract_tex_sha256': sha(ROOT / 'abstract.tex'),
    'abstract_text_sha256': sha(ROOT / 'abstract.txt'),
    'normalization': 'Collapse TeX source whitespace; replace only the seven listed math expressions with Unicode/plain-text notation. No words or sentences omitted.',
    'replacements': replacements, 'normalized_whitespace_word_count': len(abstract.split()),
    'complete': True,
})

checks = []
for item in receipt['files']:
    f = SOURCES / item['name']
    data = f.read_bytes()
    checks.append({'path': str(f.relative_to(PAPER)), 'bytes': len(data),
                   'md5': hashlib.md5(data).hexdigest(), 'sha256': sha(f),
                   'matches_receipt': len(data) == item['bytes'] and sha(f) == item['sha256'] and hashlib.md5(data).hexdigest() == item['md5']})
assert all(x['matches_receipt'] for x in checks)
with zipfile.ZipFile(SOURCES / 'verification_package.zip') as z:
    members = [i for i in z.infolist() if not i.is_dir()]
    member_checks = []
    for info in members:
        f = SOURCES / 'published-source' / info.filename
        data = z.read(info)
        assert f.read_bytes() == data, str(f)
        member_checks.append({'path': info.filename, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'byte_identical_to_zip': True})
manifest = json.loads((PACKAGE / 'MANIFEST.json').read_text())
manifest_pass = True
for name, expected in manifest['files'].items():
    f = PACKAGE / name
    manifest_pass &= f.stat().st_size == expected['bytes'] and sha(f) == expected['sha256']
assert manifest_pass
save('final-source-integrity.json', {'created_utc': NOW, 'files': checks, 'zip_members': member_checks,
    'zip_regular_files': len(members), 'outer_manifest_entries': len(manifest['files']),
    'outer_manifest_hashes_match': manifest_pass, 'published_sources_unchanged': True,
    'boundary': 'Read-only byte/size/hash checks; no scientific verifier or historical recorded verdict was executed or adopted.'})

primary_reading = [
    {'id': 'szemberg0711v1', 'locator': '§4 final question, printed p. 7; context from introduction and §4', 'extent': 'Selected passages, plus visual reading of p. 7', 'interface': 'The challenge asks whether a minimal polarized surface and point can lie strictly below 1/(2+|K²|^(1/4)). Its final question has no Picard-rank restriction despite the paper title.', 'not_verified': 'Full proof of the paper’s separate Picard-rank-one theorem; final journal body.'},
    {'id': 'owr2009-21-publisher', 'locator': 'Szemberg contribution, printed p. 1124, Conjecture 2 and adjacent Theorems 1 and 3', 'extent': 'Selected contribution text and visual reading of PDF page24', 'interface': 'Conjecture 2 expressly allows arbitrary Picard number and an arbitrary point. The additive2 is outside the fourth root. Very-general-point lower bounds are separately stated.', 'not_verified': 'Other contributions and their proofs.'},
    {'id': 'primer0810v2', 'locator': '§2.2, Question2.2.1; §6.1 Question 6.1.6, printed p17', 'extent': 'Selected sections and question context', 'interface': 'Question 6.1.6 repeats the all-minimal-surface bound. §2.2 distinguishes varying varieties from a fixed variety.', 'not_verified': 'Full37-page survey, all bibliography/citation bodies or final journal body.'},
    {'id': 'ein-lazarsfeld1993', 'locator': 'Example 3.1 printed p182; introduction; Problem3.6 / Example3.7 statement', 'extent': 'Selected passages', 'interface': 'Miranda is explicitly credited for a blowup pencil, irreducible fibres, section polarization aD+S and small pointed quotient. Example3.7 concerns unbounded very-ampleness indices on one surface, not this precise bound.', 'not_verified': 'Whole source and full proof of Example3.7.'},
    {'id': 'bauer9903v1', 'locator': '§3 Proposition3.3 and Lemma3.5 with proofs, printed pp11–13; §3 opening', 'extent': 'Selected §3 passages including complete displayed proof of the cited construction through degree choice', 'interface': 'The construction generalizes Miranda on blowups. The degree choice d=m+1 in part(b) is stated asymptotically; the present note supplies its own finite-degree pencil argument rather than importing d=7 from that statement.', 'not_verified': 'Full paper, later canonical-slope calculation or final journal body.'},
    {'id': 'adjoint1011v1', 'locator': 'Introduction and Proposition 2.1 with proof, printed pp1–2', 'extent': 'Selected passages; complete cited proposition/proof', 'interface': 'Every positive rational is realized on a suitable nonminimal blowup using the same polarization E+2C. This credits the classical small-quotient mechanism and is distinct from the minimal-surface construction.', 'not_verified': 'Later adjoint theorems, v2 changes or final journal body.'},
    {'id': 'fuentes0511v2', 'locator': 'Introduction/Theorems1.1–1.2 and §2 opening, printed pp1–3', 'extent': 'Selected passages including all three cover identities at §2 start', 'interface': 'Smooth reduced branch B∼nM gives K_X=π*(K_Y+(n−1)M). For n=2, M=2F the interface is the note’s canonical formula. Its Picard-rank-one / very-general-point or ramification-point results do not assert this special unbranched-fibre bound.', 'not_verified': 'Later Seshadri proofs or final journal body.'},
    {'id': 'canonical0801v1', 'locator': 'Introduction/Theorem1, pp1–2; complete Example1.3, printed p6', 'extent': 'Selected passages', 'interface': 'Earlier double-cover examples produce a curve with canonical degree 1 and multiplicity2, a canonical Seshadri quotient1/2. They address a different polarization and do not by that displayed quotient violate the target denominator.', 'not_verified': 'Whole paper or final journal body.'},
]
save('primary-reading-map.json', {'created_utc': NOW, 'entries': primary_reading,
    'all_read_as_primary_text': True, 'full_literature_priority_clearance': False,
    'standard_geometry_interfaces': ['Bertini/transversality for the complete degree-d system', 'Bézout and blowup intersection rules', 'Nakai–Moishezon for integral divisors on smooth projective surfaces', 'Riemann–Hurwitz / cyclic double-cover formula', 'Finite surjective pullback of ampleness, projection formula, and adjunction'],
    'standard_geometry_boundary': 'Mapped to their uses in the submitted proof; this scope role does not independently certify every classical theorem or its application. Mathematical reviewers own that gate.'})

save('search-ledger.json', {'created_utc': NOW, 'queries': ['"Seshadri" "minimal" "counterexample" "Szemberg"', '"Seshadri constants and related conjectures" "103617"'],
    'inspected_primary_web_metadata': [
        {'url': 'https://ems.press/journals/owr/articles/3471', 'extent': 'Publisher article metadata and linked full report; exact contribution passage acquired separately.'},
        {'url': 'https://www.sciencedirect.com/science/article/abs/pii/S0007449725000430', 'extent': 'Publisher metadata, abstract/introduction and section snippets surfaced by web search only; full body not read.', 'note': 'Bansal–Majumder2025 concerns characteristic-zero fields including non-algebraically-closed cases and SHGH/Nagata formulations. This partial reading does not clear historical priority.'}],
    'limitations': ['No exhaustive forward/backward citation search.', 'Full Roy2019 thesis and other thesis bodies not acquired/read.', 'Final journal bodies not globally compared to the cited arXiv editions.', 'Search snippets from nonprimary sites were not used as mathematical or priority evidence.', 'No inference that the exact problem remained open immediately before this note.']})

binding = {
    'record_id': '23387814', 'concept_record_id': str(record['conceptrecid']),
    'record_url': 'https://zenodo.org/records/23387814', 'doi': record['doi'],
    'metadata_version': '1.0', 'zenodo_version': '1.0', 'manuscript_version': None,
    'manuscript_date': '14 October 2026', 'publication_date': '2026-10-14',
    'source_receipt_sha256': sha(SOURCES / 'receipt.json'), 'record_metadata_sha256': sha(SOURCES / 'record.json'),
    'pdf_sha256': receipt['files'][0]['sha256'], 'supplement_sha256': receipt['files'][1]['sha256'],
    'files': receipt['files'], 'primary_tex_path': str(texpath.relative_to(PAPER)), 'primary_tex_sha256': sha(texpath),
    'mathematical_support_path': str((PACKAGE/'original/unsolved_math_prioritization/attempts/30001232/author/PROOF.md').relative_to(PAPER)),
    'mathematical_support_sha256': sha(PACKAGE/'original/unsolved_math_prioritization/attempts/30001232/author/PROOF.md'),
    'abstract_source': 'Complete sole abstract in published TeX lines19–27, checked against PDF p1; whitespace and math notation normalized only.',
    'main_pdf_pages': 5, 'unique_reader_pdf_count': 1, 'additional_reader_pdfs': [],
    'archive_pdf_copy': None, 'metadata_related_identifiers': record['metadata']['related_identifiers'],
    'review_boundary': 'Acquisition, source/claim scope and editorial candidate only. Mathematical clearance remains separate; no fresh scientific-code execution, human peer review or novelty certification.'}
candidate = {
    'title': record['metadata']['title'], 'slug': 'minimal-surface-seshadri-counterexample',
    'description': 'A family of minimal complex algebraic surfaces violates a proposed Seshadri lower bound, using a classical plane pencil and a double base change.',
    'abstract': abstract,
    'plain_language': [
        'A Seshadri constant measures how positive a line bundle is near one point of an algebraic surface. One way it becomes small is when a curve has little intersection with the line bundle but many branches through that point.',
        'A proposed lower bound tied this local quantity to the surface’s canonical self-intersection. This paper gives a family that falls below that bound, while keeping the line bundle’s self-intersection equal to 6.',
        'The surfaces are minimal in the algebraic-geometric sense: they contain no smooth rational curve of self-intersection −1. The small value occurs at a deliberately chosen singular point of a curve on the smooth surface.'
    ],
    'result': [
        'For every integer d ≥ 7, the paper constructs a smooth integral complex projective surface S with ample canonical bundle K_S, an ample integral line bundle L and a point x such that K_S² = 6(d−1)(d−3), L² = 6 and ε(S,L;x) ≤ 1/(d−1) < 1/(2+(K_S²)^(1/4)).',
        'At d = 7, the displayed curve has L-degree 1 and multiplicity 6 at x. Thus ε(S,L;x) ≤ 1/6, while K_S² = 144 and the proposed lower bound is larger than 1/6.',
        'The target is Szemberg’s arbitrary-point bound for minimal surfaces, restated as Conjecture 2 in Oberwolfach Report 21/2009 and Question 6.1.6 of the cited primer. The additive2 is outside the fourth root.'
    ],
    'why_it_works': [
        'The proof starts from Miranda’s classical pencil construction. A finite-degree argument chooses a plane pencil whose fibres are all integral and reduced. Blowing up its simple base points gives a surface Y with fibre F and a section E₁; the divisor A = 2F+E₁ is ample and has degree 1 on the chosen singular fibre.',
        'A double base change, branched at four smooth fibres and away from the chosen singular fibre, produces a smooth surface with ample canonical bundle. The chosen fibre splits into two isomorphic copies, so its degree 1 and multiplicity d−1 survive on either copy.',
        'Pulling back A gives L² = 6. The curve then supplies the stated upper bound directly from the definition of the Seshadri constant, and the strict comparison holds for every d ≥ 7.'
    ],
    'limitations': [
        'Only an upper bound for ε(S,L;x) is asserted; the paper does not determine its exact value.',
        'The surfaces vary with d and x is a special point. This does not establish vanishing of the infimum on one fixed complex surface, or contradict very-general-point, Picard-rank-one, canonical or adjoint polarization bounds.',
        'The second pencil member and branch values are chosen through nonempty-open existence arguments; the paper does not list explicit coefficients for every choice.',
        'The pencil, polarization and covering methods are classical. Historical priority and the problem’s status immediately before this note have not been fully established.',
        'This is an unrefereed preprint made with extensive AI assistance. Internal AI checks and finite symbolic controls do not constitute human peer review or a proof-assistant certificate.'
    ],
    'background': [
        {'title': 'Tomasz Szemberg, An effective and sharp lower bound on Seshadri constants on surfaces with Picard number 1', 'url': 'https://arxiv.org/abs/0711.0584v1', 'note': 'The final question on p. 7 asks for a minimal polarized surface below the proposed bound; it is broader than the paper’s Picard-rank-one theorem.'},
        {'title': 'Tomasz Szemberg, Seshadri constants and geometry of surfaces (2009)', 'url': 'https://ems.press/journals/owr/articles/3471', 'note': 'Oberwolfach Report 21/2009, p. 1124, Conjecture 2 states the minimal-surface bound for arbitrary points and arbitrary Picard number.'},
        {'title': 'Ein and Lazarsfeld, Seshadri constants on smooth surfaces (1993)', 'url': 'https://numdam.org/item/AST_1993__218__177_0/', 'note': 'Example 3.1 records Miranda’s classical pencil construction and its small local Seshadri quotient.'},
        {'title': 'Bauer and Szemberg, On the Seshadri constants of adjoint line bundles', 'url': 'https://arxiv.org/abs/1011.0979v1', 'note': 'Proposition 2.1 uses the same section-plus-two-fibres polarization on a plane blowup to realize arbitrary positive rational Seshadri values.'},
        {'title': 'Fuentes García, Cyclic coverings and Seshadri constants on smooth surfaces', 'url': 'https://arxiv.org/abs/math/0511547v2', 'note': 'Section 2 recalls the classical cyclic-cover canonical-bundle formula used here.'}
    ],
    'collaboration': 'I welcome independent scrutiny from researchers working on algebraic surfaces and local positivity, especially of the construction and its relation to earlier literature. Substantive verification, corrections or extensions could provide a basis for collaboration and a jointly prepared journal submission.',
    'follow_up': None,
    'followup_rationale': 'No proposed extension has been established here as both substantial and genuinely unresolved. Routine variants, numerical optimization and asking for an exact value without a demonstrated research obstacle do not meet the requested bar.',
    'publication_date': '2026-10-14', 'version': '1.0', 'doi': record['doi'], 'author': 'Alec Kriebel',
    'pdf_filename': 'seshadri_counterexample.pdf', 'supplement_filename': 'verification_package.zip',
    'supplement_label': 'Source and verification package', 'additional_assets': [],
    'status': 'Unrefereed preprint',
    'ai_disclosure': 'AI tools were used extensively in solving, research, writing, source comparison and internal verification. This work has not received human peer review or proof-assistant certification.',
    'source_binding': binding,
}
save('candidate-content.json', candidate)
print(json.dumps({'candidate': str(ROOT/'candidate-content.json'), 'abstract_words': len(abstract.split()), 'zip_files': len(members), 'manifest_entries': len(manifest['files']), 'integrity': 'PASS'}))
