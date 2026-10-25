"""Create absent source-bound configs and proposed copy; no website writes."""
from pathlib import Path
import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT / 'papers/23430906'
OUT = PAPER / 'reviews/editorial'

def load(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, obj):
    with path.open('x') as handle:
        handle.write(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

assert not (PAPER/'publication.json').exists()
assert not (PAPER/'promotion.json').exists()
clearpath = ROOT/'verification/root-clearance-23430906-20261025.json'
assert sha(clearpath) == '86a8ceed51423cf9c79c71b41389c644361d9b75b54b6bce9093ff9fa0307e8d'
clear = load(clearpath)
assert clear['status'] == 'PASS' and clear['disposition_by'] == 'root'
record = load(PAPER/'sources/record.json')
receipt = load(PAPER/'sources/receipt.json')
candidate = load(PAPER/'reviews/scope/content.json')
texpath = PAPER/'sources/support/paper.tex'
tex = texpath.read_text()
abstract_tex = re.search(r'\\begin\{abstract\}\n(.*?)\\end\{abstract\}', tex, re.S).group(1)
assert abstract_tex == candidate['abstract_original_tex']
assert sha(texpath) == clear['source_tex_sha256']
assert sha(PAPER/'sources/receipt.json') == clear['source_receipt_sha256']
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
slug = candidate['slug']
url = 'https://aleckriebel.com/research/' + slug + '/'

publication = {
    'title': record['metadata']['title'],
    'slug': slug,
    'description': 'An explicit lower bound for estimating fractional Brownian iterated area from uniform samples, proved with a localized Gaussian witness for every grid estimator.',
    'abstract': candidate['abstract'],
    'abstract_heading': 'Original abstract',
    'abstract_is_original': True,
    'plain_language': [
        'Suppose two independent fractional Brownian paths are recorded at equally spaced times. How accurately can those observations determine the integral of one path against changes in the other?',
        'This note gives a positive lower bound on the root mean-square error of every estimator using both sampled paths. It applies to nonlinear estimators as well as linear ones, and to the conditional expectation that minimizes the error. There are n observations in each component, including the final time T.',
        'For each fixed Hurst parameter H between 1/4 and 1, the lower bound is c_H T^(2H)n^(1/2−2H), with an explicit positive constant depending only on H. The statement holds for every positive T and every integer n ≥ 1.',
        'The proof constructs an auxiliary Gaussian witness that the sampled values cannot detect but that still pairs with the iterated integral. The exact Brownian optimum and the smooth-range asymptotic rate were known previously; this note presents an attributed localized-witness proof.'
    ],
    'result': [
        'Fix H ∈ (1/4,1). Let B¹ and B² be independent centered standard fractional Brownian motions with the same Hurst parameter and covariance R_H(s,t) = (s^(2H) + t^(2H) − |s−t|^(2H))/2. Let X_T = ∫₀ᵀ B¹_s dB²_s be the canonical iterated integral, defined by the L² limit of piecewise-linear lifts.',
        'For T > 0 and an integer n ≥ 1, let G_(T,n) = σ(Bⁱ_(jT/n): i=1,2; j=1,…,n). Thus both complete deterministic uniform grids are observed, including T, with n observations per component and deterministic Bⁱ_0 = 0. Every F ∈ L²(G_(T,n)), including every nonlinear square-integrable estimator, satisfies ‖X_T−F‖₂ ≥ c_H T^(2H)n^(1/2−2H).',
        'The explicit positive constant is c_H = 2πa/(D_H√(P̄_fP̄_g)), where a = 4/45045 and D_H = ∫_ℝ |e^(iξ)−1|²|ξ|^(−1−2H) dξ. Put φ(x) = x⁴(1−x)⁴ on [0,1], zero elsewhere, f = φ′, g = φ, α = 2H+1, L_r = ‖r‖₁ and N_r = ‖r‴‖₁, using weak derivatives of the zero extensions. Then P̄_r = π^α L_r² + 2N_r²π^(α−6)(1 + 1/[2(5−α)]) for r=f,g.',
        'Taking F = E[X_T | G_(T,n)] gives the same bound for the optimal conditional root mean-square error. The theorem uses this iterated-integral convention throughout.'
    ],
    'why_it_works': [
        'Two polynomial covariance paths are placed inside each grid cell and vanish at every observation time. The joint Gaussian structure makes the resulting witness vector independent of both complete observation grids.',
        'A Fourier periodization estimate controls the variance of the sum of witness products by a quantity proportional to n. The argument allows dependence between cells and signed off-diagonal covariances.',
        'For a fixed observation grid, refinement of finite left sums gives an exact deterministic pairing with the iterated integral. That pairing is n a(T/n)^(2H). Cauchy–Schwarz converts the nonzero pairing and variance bound into the displayed error inequality.',
        'Canonical-area existence and identification with the polygonal lift are established external inputs. The paper gives sufficient L² convergence without relying on exact Euler-error coefficients from the pinned arXiv v1 of Neuenkirch–Tindel–Unterberger. It distinguishes that version from the journal-formatted author copy.'
    ],
    'limitations': [
        'The theorem assumes independent standard components with the same fixed H ∈ (1/4,1), observed on both complete deterministic uniform grids. It does not cover unequal Hurst parameters, correlated components, or nonuniform or adaptive sampling.',
        'The positive constant depends on H. No sharp constant, exact normalized-error limit, limiting law, constant uniform in H, or endpoint result is asserted. The statement includes n=1 and all T>0.',
        'The halved antisymmetric area A_T = (I₁₂−I₂₁)/2 equals X_T−B¹_TB²_T/2. The endpoint product is observed, so A_T has the same optimal conditional residual as X_T. The unhalved antisymmetric difference has twice that residual.',
        'The exact Brownian optimum T/(2√n), the smooth H>1/2 asymptotic rate, and Fourier-localization and Gaussian-projection methods are credited prior work. Historical theorem and method priority, full novelty, and worldwide current-open status remain unverified. Broader implications of the Dickinson and Jackowski methods remain unverified; they are attribution limits rather than missing steps in this direct proof.',
        'This is an unrefereed preprint prepared with extensive AI assistance. Finite checks supplement the analytic argument; they do not constitute human peer review or formal proof-assistant certification.'
    ],
    'background': [
        {'title': 'Neuenkirch (2012), A conjecture on the optimal approximation of the fractional Lévy area', 'url': 'https://doi.org/10.4171/owr/2012/41', 'note': 'Records the same iterated-integral and uniform-vector-observation question and the Brownian optimum in the Clark–Cameron lineage. Its historical conjecture does not establish present-day openness.'},
        {'title': 'Neuenkirch, Tindel and Unterberger (2010), Discretizing the fractional Lévy area', 'url': 'https://doi.org/10.1016/j.spa.2009.10.007', 'note': 'Provides the established area construction and polygonal identification, and bounds for discretization schemes. The paper distinguishes the institutional journal-formatted author copy from the pinned arXiv v1; no publisher-byte identity or current journal-error claim is made.'},
        {'title': 'Neuenkirch and Shalaiko (2016), The maximum rate of convergence for the approximation of the fractional Lévy area at a single point', 'url': 'https://doi.org/10.1016/j.jco.2015.09.008', 'note': 'Establishes positive normalized liminf and finite limsup for the optimal uniform-grid error when H>1/2. The inspected author mathematical text is dated July 2015.'},
        {'title': 'Neuenkirch (2009), Optimal Pointwise Approximation of SDEs driven by Fractional Brownian Motion', 'url': 'https://drops.dagstuhl.de/storage/16dagstuhl-seminar-proceedings/dsp-vol09391/DagSemProc.09391.1/DagSemProc.09391.1.pdf', 'note': 'Earlier primary announcement of smooth-range approximation results, in the seminar abstract on page 15.'},
        {'title': 'Shalaiko (2015), Stochastic analysis of mixed models', 'url': 'https://uacademic.info/download/file/0416U000568/dis.pdf', 'note': 'Section 3.2 and Theorem 3.3 provide thesis context for the smooth H>1/2 optimal rate.'},
        {'title': 'Wu and Xiao, Geometric Properties of Fractional Brownian Sheets', 'url': 'https://www.stt.msu.edu/~xiaoyimi/XW91.pdf', 'note': 'The sectorial local-nondeterminism proof uses a harmonizable Gaussian representation and localized Fourier bumps, antecedents of the method used here.'},
        {'title': 'Xiao (2006), Properties of local-nondeterminism of Gaussian and stable random fields and their applications', 'url': 'https://doi.org/10.5802/afst.1117', 'note': 'Provides spectral and Gaussian-projection antecedents for local nondeterminism.'},
        {'title': 'Dickinson (2007), Optimal Approximation of the Second Iterated Integral of Brownian Motion', 'url': 'https://doi.org/10.1080/07362990701540592', 'note': 'A Brownian Gaussian-Hilbert-space approximation antecedent. Its complete method body and broader implications, as well as those of the named later diagonalization work, remain unverified here.'},
        {'title': 'Jackowski (1991), Complexity of multilinear problems in the average case setting', 'url': 'https://doi.org/10.1016/0885-064X(91)90047-2', 'note': 'General multilinear average-case approximation provides relevant methodological context. Complete formula-body and rough-space implications remain unverified.'}
    ],
    'collaboration': 'I welcome substantive collaboration on independent verification of the Gaussian-witness argument, a meaningful extension with a clear mathematical payoff, or development of a journal submission. Authorship and responsibilities would be discussed by mutual agreement and would reflect actual research and writing contributions.',
    'follow_up': None,
    'followup_rationale': candidate['followup_rationale'],
    'publication_date': '2026-10-14',
    'version': '1.0',
    'doi': record['doi'],
    'author': 'Alec Kriebel',
    'orcid': 'https://orcid.org/0009-0001-9320-500X',
    'pdf_filename': 'paper.pdf',
    'supplement_filename': 'PR1071_preprint_v1_0_support.zip',
    'supplement_label': 'Manuscript source and supporting materials (ZIP)',
    'additional_assets': [],
    'related_resources': [
        {'label': 'Download the complete supporting materials (ZIP)', 'url': url+'PR1071_preprint_v1_0_support.zip'},
        {'label': 'Zenodo original supporting materials (ZIP)', 'url': 'https://zenodo.org/records/23430906/files/PR1071_preprint_v1_0_support.zip'}
    ],
    'status': 'Unrefereed preprint; Zenodo version 1.0, dated 14 October 2026. Prepared with extensive AI assistance; no independent human or journal peer review or formal proof-assistant certification is claimed.',
    'ai_disclosure': 'AI tools were used extensively in mathematical development, checking, literature review and writing. Internal AI-assisted review is not independent human or journal peer review. This is an unrefereed preprint without formal proof-assistant certification. The named author is responsible for its claims, materials and citations.',
    'license': 'CC BY 4.0',
    'publication_date_label': 'Manuscript and declared publication date',
    'edition_label': 'Zenodo version 1.0',
    'citation_edition_label': 'Version 1.0, 14 October 2026',
    'edition_note': 'The manuscript and Zenodo’s declared publication date are 14 October 2026, version 1.0. Zenodo created the record on 17 October 2026 UTC. These dates identify the archived edition and do not establish historical priority.',
    'bibtex_note': 'Unrefereed preprint; version 1.0, dated 14 October 2026. Zenodo record created 17 October 2026 UTC. Prepared with extensive AI assistance.',
    'canonical_url': url,
    'pdf_pages': 7,
    'keywords': ['fractional Brownian motion', 'fractional iterated area', 'Gaussian witness', 'uniform sampling', 'optimal approximation', 'root mean-square lower bound', 'Hurst parameter', 'conditional expectation'],
    'source_binding': {
        'record_id': '23430906', 'concept_record_id': '23430905',
        'record_url': record['links']['self_html'], 'doi': record['doi'], 'concept_doi': record['conceptdoi'],
        'version': '1.0', 'zenodo_version': '1.0', 'manuscript_version': '1.0',
        'zenodo_publication_date': '2026-10-14', 'manuscript_date': '14 October 2026',
        'record_created_utc': record['created'], 'record_updated_utc': record['updated'],
        'source_retrieved_utc': receipt['retrieved_utc'],
        'metadata_path': 'sources/record.json', 'record_path': 'sources/record.json', 'receipt_path': 'sources/receipt.json',
        'metadata_sha256': sha(PAPER/'sources/record.json'), 'record_sha256': sha(PAPER/'sources/record.json'),
        'record_raw_path': 'sources/record-raw.json', 'record_raw_sha256': sha(PAPER/'sources/record-raw.json'),
        'receipt_sha256': sha(PAPER/'sources/receipt.json'), 'source_receipt_sha256': sha(PAPER/'sources/receipt.json'),
        'pdf_sha256': clear['pdf_sha256'], 'supplement_sha256': clear['supplement_sha256'],
        'files': receipt['files'],
        'source_tex_path': str(texpath.relative_to(PAPER)), 'source_tex_sha256': sha(texpath),
        'abstract_source': str(texpath.relative_to(PAPER)), 'abstract_source_sha256': sha(texpath),
        'abstract_pdf_source': 'sources/paper.pdf#page=1',
        'abstract_tex': abstract_tex, 'abstract_tex_sha256': hashlib.sha256(abstract_tex.encode()).hexdigest(),
        'abstract_normalization': candidate['abstract_source'],
        'original_abstract_field': 'abstract', 'abstract_display_heading': 'Original abstract',
        'frozen_scope_content_path': 'reviews/scope/content.json', 'frozen_scope_content_sha256': sha(PAPER/'reviews/scope/content.json'),
        'frozen_scope_abstract_field': 'abstract',
        'frozen_scope_gate': 'SCOPE_COMPLETE_ATTRIBUTION_QUALIFIED_MATHEMATICAL_GATE_PENDING; mathematical_verdict=null; substantive_defect_found=null; promotion_authorized=false. Complete original object is preserved, separately resolved by later root scientific clearance.',
        'reviewed_documents': [{'source': 'standalone', 'source_relative_path': 'paper.pdf', 'pages': 7, 'bytes': 93113, 'sha256': clear['pdf_sha256'], 'editorial_read_scope': 'Full actual PDF and complete TeX read during the same agent’s immediately preceding source/scope assignment; all seven rendered PDF pages inspected there. Fresh editorial text extraction and unchanged identity checked. This does not imply a website render or live pass.'}],
        'unique_reader_pdf_count': 1, 'archive_regular_file_count': 225,
        'nested_archive_count': 0, 'archive_embedded_pdf_count': 1,
        'embedded_assets': [], 'additional_reader_pdfs': [],
        'archive_reader_note': 'The embedded paper.pdf is byte-identical to the standalone seven-page reader. Copy the complete deposited ZIP unchanged; no third-party primary-cache file is a public website asset.',
        'review_boundary': 'Original source, receipt, report, custom verdict and seal bytes remain unchanged. The later separately bound root clearance resolves the scientific gate without changing the original scope-only pending verdict.',
        'publication_state': 'BINDINGS_READY_RENDERING_PENDING'
    },
    'review_metadata': {
        'prepared_utc': now, 'completion_percent': 100, 'scientific_clearance_received': True,
        'root_clearance_file': str(clearpath.relative_to(ROOT)), 'root_clearance_sha256': sha(clearpath),
        'publication_state': 'BINDINGS_READY_RENDERING_PENDING', 'rendered': False, 'deployed': False,
        'editor_authorization': 'Only previously absent paper-specific publication/promotion configs and new reviews/editorial artifacts. No frozen source/review edits, shared-script or site mutation, Git, Sheet, deployment, release, UI or external communication. Root retains actual rendered-copy, local/live HTTP, browser and native tracker gates.'
    }
}
write(PAPER/'publication.json', publication)

reviews = {}
for role, item in clear['reviews'].items():
    reportpath, verdictpath = ROOT/item['report'], ROOT/item['verdict']
    assert sha(reportpath) == item['report_sha256']
    assert sha(verdictpath) == item['verdict_sha256']
    reviews[role] = {
        'report': str(reportpath.relative_to(PAPER)), 'sha256': item['report_sha256'],
        'verdict_file': str(verdictpath.relative_to(PAPER)), 'verdict_sha256': item['verdict_sha256'],
        'verdict': load(verdictpath),
        'root_disposition': 'SCOPE_COMPLETE' if role == 'scope' else 'PASS'
    }
promotion = {
    'record_id': '23430906', 'status': clear['status'], 'disposition_by': clear['disposition_by'], 'created_utc': now,
    'approved_scope': clear['approved_scope'],
    'root_clearance': 'Later root scientific disposition only. Exact original reviewer objects and the original scope pending fields remain preserved. Website rendering, live, browser and native tracker gates are not passed by this config.',
    'root_clearance_file': str(clearpath.relative_to(ROOT)), 'root_clearance_sha256': sha(clearpath),
    'root_clearance_record': clear,
    'pdf_sha256': clear['pdf_sha256'], 'supplement_sha256': clear['supplement_sha256'],
    'publication_sha256': sha(PAPER/'publication.json'),
    'source_receipt_sha256': sha(PAPER/'sources/receipt.json'),
    'source_receipt_record': receipt,
    'metadata_path': 'sources/record.json', 'metadata_sha256': sha(PAPER/'sources/record.json'),
    'source_files': receipt['files'],
    'source_receipts': {'sources/receipt.json': {'sha256': sha(PAPER/'sources/receipt.json'), 'files': len(receipt['files']), 'record_raw_sha256': receipt['record_raw_sha256']}},
    'root_custody_receipt': clear['root_custody_receipt'], 'root_custody_receipt_sha256': clear['root_custody_receipt_sha256'],
    'root_final_seal_bindings_rehashed': clear['root_final_seal_bindings_rehashed'],
    'reviews': reviews,
    'scope_gate_resolution': clear['scope_gate_resolution'], 'source_repair': False,
    'human_peer_review': False, 'formal_machine_verification': False,
    'follow_up': None, 'preparation_state': 'BINDINGS_READY_RENDERING_PENDING',
    'rendered_copy_verified': False, 'live_verified': False, 'browser_verified': False, 'native_sheet_aa_url': None
}
write(PAPER/'promotion.json', promotion)

sections = [
    {'id': 'abstract', 'heading': 'Original abstract', 'paragraphs': [publication['abstract']]},
    {'id': 'plain-language', 'heading': 'The idea in plain English', 'paragraphs': publication['plain_language']},
    {'id': 'result', 'heading': 'The precise result', 'paragraphs': publication['result']},
    {'id': 'proof', 'heading': 'Why the result holds', 'paragraphs': publication['why_it_works']},
    {'id': 'limits', 'heading': 'Scope and limitations', 'paragraphs': publication['limitations']},
    {'id': 'status', 'heading': 'Status and AI use', 'paragraphs': [publication['ai_disclosure'], publication['edition_note']]},
    {'id': 'paper', 'heading': 'Read the paper', 'links': [
        {'label': 'Open the unchanged PDF', 'url': url+'paper.pdf'},
        {'label': 'Download the unchanged PDF', 'url': url+'paper.pdf', 'download': True},
        {'label': 'Zenodo original PDF', 'url': 'https://zenodo.org/records/23430906/files/paper.pdf'}
    ], 'iframe': {'src': 'paper.pdf#view=FitH', 'title': publication['title']+' — full paper PDF', 'loading': 'lazy'}, 'paragraphs': ['Read the full seven-page paper in the on-page PDF reader.']},
    {'id': 'materials', 'heading': 'Supporting materials', 'links': [
        {'label': publication['supplement_label'], 'url': url+publication['supplement_filename'], 'download': True},
        {'label': 'Zenodo original ZIP', 'url': 'https://zenodo.org/records/23430906/files/'+publication['supplement_filename']}
    ]},
    {'id': 'collaborate', 'heading': 'Collaborate on this result', 'paragraphs': [publication['collaboration']]},
    {'id': 'cite', 'heading': 'Cite this paper', 'paragraphs': ['Kriebel, Alec. (2026). '+publication['title']+' (Version 1.0, 14 October 2026) [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.23430906'], 'links': [{'label': 'Download BibTeX', 'url': url+'citation.bib'}]},
    {'id': 'background', 'heading': 'Background and prior work', 'references': publication['background']}
]
write(OUT/'public-sections.json', {'record_id': '23430906', 'state': 'PROPOSED_PUBLIC_COPY_NOT_RENDERED', 'canonical_url': url, 'header': {'title': publication['title'], 'author': publication['author'], 'orcid': publication['orcid'], 'publication_date': publication['publication_date'], 'version': publication['version'], 'status': 'Unrefereed preprint', 'description': publication['description']}, 'sections': sections, 'follow_up': None, 'native_sheet_aa_url': None})

lines = ['# '+publication['title'], '', 'By Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X', '', 'Manuscript and declared publication date: 14 October 2026 · Zenodo version 1.0 · Unrefereed preprint', '', 'Canonical URL: '+url, '', 'Search description: '+publication['description'], '', '[Research home](https://aleckriebel.com/research/) · [Zenodo record](https://zenodo.org/records/23430906) · [DOI](https://doi.org/10.5281/zenodo.23430906) · License: CC BY 4.0', '']
for section in sections:
    lines += ['## '+section['heading'], '']
    for paragraph in section.get('paragraphs', []):
        lines += [paragraph, '']
    if section.get('links'):
        lines += [' · '.join('['+x['label']+']('+x['url']+')' for x in section['links']), '']
    for reference in section.get('references', []):
        lines += ['- ['+reference['title']+']('+reference['url']+'): '+reference['note'], '']
with (OUT/'PUBLIC_COPY.md').open('x') as handle:
    handle.write('\n'.join(lines).rstrip()+'\n')
print(json.dumps({'record_id': '23430906', 'canonical_url': url, 'publication_sha256': sha(PAPER/'publication.json'), 'promotion_sha256': sha(PAPER/'promotion.json')}))
