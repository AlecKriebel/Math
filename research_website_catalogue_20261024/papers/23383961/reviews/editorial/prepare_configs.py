"""Prepare only absent, source-bound editorial configs for Zenodo 23383961."""
from pathlib import Path
import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT / 'papers/23383961'
OUT = PAPER / 'reviews/editorial'

def read(p):
    return json.loads(p.read_text())

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(p, obj):
    with p.open('x') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

assert not (PAPER / 'publication.json').exists()
assert not (PAPER / 'promotion.json').exists()
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
clearance_path = ROOT / 'verification/root-clearance-23383961-20261025.json'
assert digest(clearance_path) == '2a9214e52b408d2a67a4aef4d6887b8cf86f8eb46f99423ad977c4a8cf847122'
clearance = read(clearance_path)
record = read(PAPER / 'sources/record.json')
receipt = read(PAPER / 'sources/receipt.json')
candidate = read(PAPER / 'reviews/scope/candidate.json')
texpath = PAPER / 'sources/published-source/verification_package/support_slit_verification/support_slit.tex'
tex = texpath.read_text()
abstract_tex = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
slug = 'nonmonotone-argument-radial-angle-support-slit'
url = 'https://aleckriebel.com/research/' + slug + '/'
files = [{k: item[k] for k in ['name', 'url', 'bytes', 'sha256', 'zenodo_checksum', 'retrieved_utc']} for item in receipt['files']]

publication = {
    'title': record['metadata']['title'],
    'slug': slug,
    'description': 'A fixed coefficient functional has genuine univalent support points whose omitted slits have nonmonotone polar argument and signed and unsigned radial angles.',
    'abstract': candidate['original_abstract'],
    'abstract_heading': 'Original abstract',
    'abstract_is_original': True,
    'plain_language': [
        'A univalent function maps the unit disk into the complex plane without folding it over itself. A support point is such a map that maximizes a linear measurement of the function. Classical results show that its image leaves out a single analytic arc, running from a finite tip to infinity.',
        'Two questions attributed to P. L. Duren ask whether that omitted arc must turn monotonically in its polar direction, and whether the angle between its radius and its tangent must change monotonically. Here monotone allows either increasing or decreasing behavior.',
        'This note chooses one particular measurement of the second, third and fourth Taylor coefficients. Global maximizers exist, and every one of them has an actual omitted slit for which both proposed monotonicity properties fail. The radial-angle failure holds for both the signed outward angle and the ordinary nonnegative angle.',
        'The proof controls all maximizers at once. It does not need to write down a maximizing function or show that it is unique. The polar direction, the tangent direction and the angle between them are different quantities; the theorem addresses the first and the third.'
    ],
    'result': [
        'Let S be the analytic injective maps on the unit disk normalized by f(0) = 0 and f′(0) = 1, with f(z) = z + Σₙ≥₂ aₙ(f)zⁿ. Set ε = 10⁻²⁴ and L(f) = a₂(f) + iε(a₄(f) − 3a₃(f)). Global maximizers of Re L on S exist. Every such maximizer omits an actual analytic slit Γ whose continuous polar argument, signed outward radial angle and ordinary unsigned outward radial angle are all nonmonotone.',
        'The polar argument is a continuous real-valued lift along Γ. The tangent used for the signed radial angle points from the finite tip toward infinity. The ordinary radial angle is the nonnegative angle between that outward tangent and the radius vector. Both nondecreasing and nonincreasing behavior are excluded for each of the three quantities.',
        'This supplies counterexamples to the two support-slit monotonicity properties recorded as Hayman–Lingham Problem 6.72. No explicit maximizing map or uniqueness theorem is required.'
    ],
    'why_it_works': [
        'Compactness of S gives genuine global maximizers. Comparing any maximizer with the Koebe function and using the classical coefficient inequalities gives uniform control of its first coefficients. An odd-root version of the area theorem then controls an analytic tail and places the actual omitted slit tip inside radius 3/10.',
        'The Schiffer differential is expanded exactly for the chosen functional. A controlled inverse natural coordinate constructs a regular arc with modulus greater than 25/81. It agrees with the actual omitted slit near infinity. The separation from the actual tip and local trajectory uniqueness extend that agreement across the tested subarc. This identifies a subarc of each genuine support slit; it does not infer extremality from an arbitrary differential trajectory.',
        'Writing this subarc as W(t) = −V(t)⁻², with 0 < t ≤ 7/4, and Z = tV′/V, the proof bounds Z − 1 − iεq(t) by 2000εη, where η = 10⁻¹² and q(t) = t² − 2t⁴/5. The values q(1) = 3/5 and q(7/4) = −441/640 force opposite strict signs for Im Z and hence opposite signs of the polar-argument derivative.',
        'Increasing t points inward, so the outward tangent is −W′ and its signed radial angle is β = arg Z. This angle tends to zero at infinity and takes both positive and negative values; those facts exclude both monotone directions. Its continuity gives an interior zero between nonzero endpoint values, so the ordinary angle |β| is separately nonmonotone.'
    ],
    'limitations': [
        'The theorem concerns the stated normalized schlicht class, the particular degree-four coefficient functional and the fixed value ε = 10⁻²⁴. It is not a conclusion about every coefficient functional or every support slit. At ε = 0 the strict reversal disappears; no claim for arbitrary larger perturbations is made.',
        'The existence and every-maximizer conclusions do not provide an explicit maximizing function, uniqueness, a numerical extremal solver or a computed extremizer.',
        'The proof uses established compactness, Bieberbach coefficient bounds, the area theorem and classical support-slit and Schiffer geometry. Finite rational checks and numerical diagnostics supplement the analytic estimates; they do not formally certify the universal theorem or the classical foundations.',
        'The historical comparisons are bounded. The manuscript identifies later Duren commentary and Hibschweiler’s 1995 paper as uninspected. No historical firstness, exhaustive priority clearance or claim that the questions remained open worldwide in 2026 is made.',
        'This is an unrefereed preprint developed with extensive AI assistance. Internal AI reviews are not independent human or journal peer review, and no formal proof-assistant certification is claimed.'
    ],
    'background': [
        {'title': 'Hayman and Lingham (2018), Research Problems in Function Theory, Problem 6.72', 'url': 'https://arxiv.org/abs/1809.07200v2', 'note': 'Records the two questions attributed to P. L. Duren about polar argument and radial-angle monotonicity of the actual omitted arc of a support point. The dated problem collection does not establish present open status.'},
        {'title': 'Pfluger (1971), Lineare Extremalprobleme bei schlichten Funktionen', 'url': 'https://doi.org/10.5186/aasfm.1971.489', 'note': 'Provides classical compactness, the functional framework and the geometry of actual support slits. The differential sign is converted to Duren’s convention in this note.'},
        {'title': 'Duren (1981), Arcs omitted by support points of univalent functions', 'url': 'https://doi.org/10.1007/BF02566218', 'note': 'Supplies the omitted-arc differential and outward radial-angle convention, and proves positive monotonicity results for restricted evaluation families. The support-slit geometry and Schiffer methods are classical inputs.'},
        {'title': 'Brown (1979), Geometric properties of a class of support points of univalent functions', 'url': 'https://doi.org/10.1090/S0002-9947-1979-0546923-8', 'note': 'Establishes positive monotonicity results for point-evaluation support points. This is a restricted family of functionals.'},
        {'title': 'de Branges (1985), A proof of the Bieberbach conjecture', 'url': 'https://doi.org/10.1007/BF02392821', 'note': 'The classical coefficient bound |aₙ| ≤ n supplies the bounds for n = 2, 3 and 4 used in the proof.'},
        {'title': 'Friedland and Schiffer (1977), On coefficient regions of univalent functions', 'url': 'https://doi.org/10.1007/BF02813301', 'note': 'Credited in the manuscript for the earlier coefficient and control framework. The note’s wider historical comparisons do not constitute exhaustive priority clearance.'}
    ],
    'collaboration': 'I welcome substantive collaboration on independent verification of the every-maximizer estimates and actual-slit continuation, meaningful extensions supported by proof, or development of a journal submission. Authorship and responsibilities would be discussed by mutual agreement and would reflect actual research and writing contributions.',
    'follow_up': None,
    'followup_rationale': 'No precise follow-up has cleared the required mathematical and focused primary-literature threshold for a substantial potential contribution. The bounded historical reading does not certify worldwide openness.',
    'publication_date': '2026-10-14',
    'version': '1.0',
    'doi': record['doi'],
    'author': 'Alec Kriebel',
    'orcid': 'https://orcid.org/0009-0001-9320-500X',
    'pdf_filename': 'support_slit.pdf',
    'supplement_filename': 'verification_package.zip',
    'supplement_label': 'Manuscript source and verification materials (ZIP)',
    'additional_assets': [],
    'related_resources': [],
    'status': 'Unrefereed preprint; Zenodo version 1.0, dated 14 October 2026. Developed with extensive AI assistance; no independent human or journal peer review or formal proof-assistant certification is claimed.',
    'ai_disclosure': 'AI tools were used extensively in mathematical development, derivation, writing, reproduction, adversarial verification and subsequent review. Internal AI review is not independent human or journal peer review. This is an unrefereed preprint without formal proof-assistant certification. The named author is responsible for its claims, materials and citations.',
    'license': 'CC BY 4.0',
    'publication_date_label': 'Manuscript and declared publication date',
    'edition_label': 'Zenodo version 1.0',
    'citation_edition_label': 'Version 1.0, 14 October 2026',
    'edition_note': 'The manuscript and Zenodo’s declared publication date are 14 October 2026. Zenodo created the record on 15 October 2026. These dates identify the archived edition and do not establish historical priority.',
    'bibtex_note': 'Unrefereed preprint; version 1.0, dated 14 October 2026. Zenodo record created 15 October 2026. Developed with extensive AI assistance.',
    'canonical_url': url,
    'pdf_pages': 5,
    'keywords': ['univalent functions', 'schlicht class', 'support points', 'omitted slit', 'nonmonotone polar argument', 'radial angle', 'Schiffer differential', 'Hayman–Lingham Problem 6.72'],
    'source_binding': {
        'record_id': '23383961', 'concept_record_id': '23383960',
        'record_url': record['links']['self_html'], 'doi': record['doi'], 'concept_doi': record['conceptdoi'],
        'version': '1.0', 'zenodo_version': '1.0', 'manuscript_version': '1.0',
        'zenodo_publication_date': '2026-10-14', 'manuscript_date': '14 October 2026',
        'record_created_utc': record['created'], 'record_updated_utc': record['updated'],
        'source_retrieved_utc': receipt['retrieved_utc'],
        'metadata_path': 'sources/record.json', 'record_path': 'sources/record.json',
        'metadata_sha256': digest(PAPER / 'sources/record.json'), 'record_sha256': digest(PAPER / 'sources/record.json'),
        'receipt_sha256': digest(PAPER / 'sources/receipt.json'), 'source_receipt_sha256': digest(PAPER / 'sources/receipt.json'),
        'pdf_sha256': clearance['pdf_sha256'], 'supplement_sha256': clearance['supplement_sha256'],
        'files': files,
        'source_tex_path': str(texpath.relative_to(PAPER)), 'source_tex_sha256': digest(texpath),
        'abstract_source': str(texpath.relative_to(PAPER)), 'abstract_source_sha256': digest(texpath),
        'abstract_pdf_source': 'sources/support_slit.pdf#page=1',
        'abstract_tex': abstract_tex, 'abstract_tex_sha256': hashlib.sha256(abstract_tex.encode()).hexdigest(),
        'abstract_normalization': 'Complete original abstract, word-for-word with only mathematical typography, TeX macros, dashes and whitespace normalized. Matched to the actual standalone reader and full released TeX; no sentence omitted or scope silently rewritten.',
        'original_abstract_field': 'abstract', 'abstract_display_heading': 'Original abstract',
        'frozen_scope_content_path': 'reviews/scope/candidate.json', 'frozen_scope_content_sha256': digest(PAPER / 'reviews/scope/candidate.json'),
        'frozen_scope_abstract_field': 'original_abstract',
        'frozen_scope_gate': 'SCOPE_COMPLETE_PENDING_INDEPENDENT_MATHEMATICAL_REVIEW; mathematical_pass=false; scientific_verdict=null; ready_to_publish=false. Preserved as original source/scope disposition, separately resolved by later root mathematical clearance.',
        'reviewed_documents': [{'source': 'standalone', 'source_relative_path': 'support_slit.pdf', 'pages': 5, 'bytes': 92949, 'sha256': clearance['pdf_sha256'], 'editorial_read_scope': 'All five pages read by fresh extraction and visual inspection; complete released TeX read. No rendered website, live or browser publication pass is implied.'}],
        'unique_reader_pdf_count': 1, 'archive_regular_file_count': 255, 'hidden_archive_members': 12,
        'nested_archive_count': 0, 'archive_embedded_pdf_count': 0,
        'embedded_assets': [], 'additional_reader_pdfs': [],
        'archive_reader_note': 'The unchanged standalone PDF is the sole published reader. Preserve the complete deposited ZIP unchanged; research caches of third-party full texts are not public website assets.',
        'review_boundary': 'Original source, report, verdict and seal objects remain unchanged. Later separately bound root scientific clearance governs this draft; the original scope-only null/false/pending fields are not converted into a mathematical verdict.',
        'publication_state': 'BINDINGS_READY_RENDERING_PENDING'
    },
    'review_metadata': {
        'prepared_utc': now, 'completion_percent': 100, 'scientific_clearance_received': True,
        'root_clearance_file': str(clearance_path.relative_to(ROOT)), 'root_clearance_sha256': digest(clearance_path),
        'publication_state': 'BINDINGS_READY_RENDERING_PENDING', 'rendered': False, 'deployed': False,
        'editor_authorization': 'Only absent paper-specific publication/promotion configs and new reviews/editorial artifacts. No original source/review/seal edits, shared checker/renderer/site changes, Git, Sheet, browser, deployment, release or outreach. Root retains actual rendered-copy, local/live HTTP, browser and native-tracker gates. Native AA URL remains blank until verified live.'
    }
}
write(PAPER / 'publication.json', publication)
reviews = {}
for role, obj in clearance['reviews'].items():
    verdict_path = ROOT / obj['verdict']
    reviews[role] = {
        'report': str((ROOT / obj['report']).relative_to(PAPER)),
        'sha256': obj['report_sha256'],
        'verdict_file': str(verdict_path.relative_to(PAPER)),
        'verdict_sha256': obj['verdict_sha256'],
        'verdict': read(verdict_path),
        'root_disposition': 'SCOPE_COMPLETE' if role == 'scope' else 'PASS'
    }
promotion = {
    'record_id': '23383961', 'status': 'PASS', 'disposition_by': 'root', 'created_utc': now,
    'approved_scope': clearance['approved_scope'],
    'root_clearance': 'Later root scientific clearance controls the exact stated scope; original scope-only pending/null/false verdict fields are preserved. This source-bound config remains unrendered and unpublished.',
    'root_clearance_file': str(clearance_path.relative_to(ROOT)), 'root_clearance_sha256': digest(clearance_path),
    'root_clearance_record': clearance,
    'pdf_sha256': clearance['pdf_sha256'], 'supplement_sha256': clearance['supplement_sha256'],
    'publication_sha256': digest(PAPER / 'publication.json'),
    'source_receipt_sha256': digest(PAPER / 'sources/receipt.json'),
    'metadata_path': 'sources/record.json', 'metadata_sha256': digest(PAPER / 'sources/record.json'),
    'source_files': files, 'source_receipts': clearance['source_receipts'],
    'root_custody_receipt': clearance['root_custody_receipt'],
    'root_custody_receipt_sha256': clearance['root_custody_receipt_sha256'],
    'review_seals': clearance['root_review_seals_rehashed'], 'reviews': reviews,
    'scope_gate_resolution': clearance['scope_gate_resolution'],
    'source_repair': False, 'human_peer_review': False, 'formal_machine_verification': False,
    'follow_up': None, 'preparation_state': 'BINDINGS_READY_RENDERING_PENDING',
    'rendered_copy_verified': False, 'live_verified': False, 'native_sheet_aa_url': None
}
write(PAPER / 'promotion.json', promotion)
print(json.dumps({'record_id':'23383961','canonical_url':url,'publication_sha256':digest(PAPER/'publication.json'),'promotion_sha256':digest(PAPER/'promotion.json')}))
