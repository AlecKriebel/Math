"""Bind root-cleared publication copy to the untouched published edition."""
from pathlib import Path
import datetime, hashlib, json, re, zipfile

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'papers/23180194'
HERE = Path(__file__).resolve().parent
SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, obj): p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
assert not (P/'publication.json').exists()
assert not (P/'promotion.json').exists()
receipt = json.loads((P/'sources/receipt.json').read_text())
record = json.loads((P/'sources/record.json').read_text())
candidate_path = P/'reviews/scope/candidate-content.json'
candidate = json.loads(candidate_path.read_text())
assert receipt['record_sha256'] == sha(P/'sources/record.json')
assert receipt['complete'] and len(receipt['files']) == 2
for asset in receipt['files']:
    path = P/'sources'/asset['name']
    assert sha(path) == asset['sha256']
    assert hashlib.md5(path.read_bytes()).hexdigest() == asset['md5'] == asset['zenodo_checksum'].split(':')[1]
    assert path.stat().st_size == asset['bytes']
tex_rel = 'sources/published-source/mass_stationarity_verification/paper.tex'
tex = (P/tex_rel).read_text()
assert sha(P/tex_rel) == candidate['abstract_source_sha256']
abstract_tex = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1)
abstract = ' '.join(abstract_tex.replace(r'\xi', 'ξ').replace('$', '').replace('--', '–').split())
assert abstract == candidate['abstract'] and len(abstract.split()) == 113
assert r'\date{6 October 2026\quad---\quad Unrefereed research note}' in tex
assert record['metadata']['version'] == candidate['version'] == '1.0'
assert record['metadata']['publication_date'] == candidate['publication_date'] == '2026-10-06'
assert record['metadata']['doi'] == candidate['doi'] == '10.5281/zenodo.23180194'
with zipfile.ZipFile(P/'sources'/candidate['supplement']['filename']) as z:
    assert z.testzip() is None
    members = [i for i in z.infolist() if not i.is_dir()]
    assert len(members) == 19
    for item in members:
        extracted = P/'sources/published-source/mass_stationarity_verification'/item.filename
        assert extracted.read_bytes() == z.read(item)

reviews = {}
for role in ('analytic', 'adversarial', 'scope'):
    rp, vp = f'reviews/{role}/REVIEW.md', f'reviews/{role}/verdict.json'
    verdict = json.loads((P/vp).read_text())
    reviews[role] = {'report': rp, 'sha256': sha(P/rp), 'verdict_file': vp,
                     'verdict_sha256': sha(P/vp), 'verdict': verdict}
assert reviews['analytic']['verdict']['status'] == 'SUPPORTED_AT_STATED_SCOPE'
assert reviews['adversarial']['verdict']['status'] == 'PASS'
assert reviews['scope']['verdict']['verdict'] == 'PASS_SCOPE_ONLY'
assert not reviews['analytic']['verdict']['substantive_defect_found']
assert not reviews['adversarial']['verdict']['substantive_defect_found']
assert reviews['scope']['verdict']['review_sha256'] == reviews['scope']['sha256']
for item in reviews['adversarial']['verdict']['artifacts']:
    assert sha(P/item['path']) == item['sha256']
for name, digest in reviews['scope']['verdict']['artifacts'].items():
    assert sha(P/'reviews/scope'/name) == digest
manifest = json.loads((P/'reviews/analytic/evidence_manifest.json').read_text())
for item in manifest['artifacts']:
    assert sha(P/'reviews/analytic'/item['path']) == item['sha256']
for item in reviews['analytic']['verdict']['source_integrity']['extracted_files']:
    assert sha(P/'sources/published-source/mass_stationarity_verification'/item['path']) == item['sha256']
save(HERE/'site-before.json', {str(p.relative_to(SITE)):sha(p) for p in SITE.rglob('*') if p.is_file()})

content = {
 'title': candidate['title'],
 'slug': candidate['slug_suggestion'],
 'description': 'Measure-only randomized transports characterize mass-stationarity, including periodic random measures and information beyond the mass itself.',
 'abstract': abstract,
 'plain_language': [
  'Imagine a landscape whose mass sits at isolated points, spreads continuously, or does both. A mass-stationary origin is a location that is typical of that mass. This paper gives a way to recognize such an origin using randomized changes of viewpoint.',
  'The allowed rules inspect the mass measure, choose a random displacement, and move the origin. Each rule must respect translations and redistribute the existing mass while preserving that same measure. If every allowed rule leaves the full environment’s governing measure unchanged, the origin is mass-stationary.',
  'The interesting part is that the rules see only the mass, while the conclusion concerns the entire environment. For example, a translation can leave a periodic mass pattern unchanged while moving other information attached to the landscape. The proof accounts for that hidden information too.'
 ],
 'result': [
  'Let G be a locally compact second countable Hausdorff Abelian group acting jointly measurably on an arbitrary measurable space Ω. Let Q be a sigma-finite measure on Ω, and let ξ be a measurable, covariant, locally finite Radon random measure that is nonzero Q-almost everywhere. Q may be infinite; expectations below mean integration with respect to Q.',
  'The test class consists of every invariant, pointwise ξ-preserving, ξ-measurable Markov transport kernel T. Markov means each row has mass one; ξ-measurable means the rule depends on the ambient state only through ξ. Pointwise preservation requires ∫ T(ω,s,B) ξω(ds) = ξω(B) for each state ω and measurable set B. The hypothesis is full ambient invariance: E_Q ∫ f(θ_tω) T(ω,0,dt) = E_Q f for every nonnegative measurable function f on Ω.',
  'This hypothesis implies the joint Mecke identity, or Campbell reversal: E_Q ∫ g(θ_tω, −t) ξω(dt) = E_Q ∫ g(ω,t) ξω(dt) for every nonnegative measurable g on Ω × G. The classical Mecke/Palm and Palm/mass-stationarity equivalences then give mass-stationarity. Together with the known converse transport invariance, this answers Last and Thorisson’s Problem 7.3 from 2009 in the stated setting.'
 ],
 'why_it_works': [
  'The proof separates displacements that change the mass measure from its periods, the translations that leave the measure unchanged. Away from periods, oriented local symmetric transports recover reversal on pieces that can be distinguished by observing the measure. Normalization and a holding probability turn these tests into genuine Markov kernels.',
  'On the remaining set, normalized transports along the period subgroup recover reversal even when a shift changes hidden parts of the environment. The two arguments combine to give the joint identity for the whole ambient state. Standard Borel structure is used for the space of Radon measures; it is not imposed on Ω.'
 ],
 'limitations': [
  'The theorem requires an Abelian group, sigma-finite Q, and a locally finite Radon measure that is nonzero Q-almost everywhere. Atoms, diffuse or mixed mass, periodic measures, infinite total mass and infinite Q are included. There is no finite-intensity assumption and no assumption that the marginal law of ξ is sigma-finite. The theorem does not cover non-Abelian groups or the zero random measure.',
  'The hypothesis tests the full ambient measure against every admissible Markov transport. Invariance of the law of ξ alone is not a substitute. A converse based only on deterministic transports, or on the narrower class arising from Cox allocations, is outside this result.',
  'The new step is deriving joint Mecke reversal from measure-only Markov tests. The Palm equivalences and converse transport theorem are established inputs, and earlier discrete, aperiodic and positive-density cases receive credit in the paper. This page does not certify exhaustive novelty, historical first priority or the present status of related open questions.'
 ],
 'collaboration': 'I welcome collaboration with researchers in Palm theory, random measures and invariant transports who would like to examine the measure-theoretic proof, sharpen its connection with the existing literature, or help develop a journal submission.',
 'background': [
  {'title': 'Last and Thorisson — Invariant transports of stationary random measures and mass-stationarity (2009)',
   'url': 'https://arxiv.org/abs/0906.2062v1',
   'note': 'Problem 7.3 is the question addressed here. Equation (2.7), Theorem 4.1 and Theorem 6.3 supply the credited Mecke, transport-invariance and mass-stationarity interfaces.'},
  {'title': 'Last and Thorisson — Construction and characterisation of stationary and mass-stationary random measures on R^d (retained arXiv version 2)',
   'url': 'https://arxiv.org/abs/1405.7566v2',
   'note': 'The positive-density antecedent uses a joint density field with additional line-integrability hypotheses. The linked author version is the version compared here; its complete final journal body was not checked.'},
  {'title': 'Last and Thorisson — Characterization of mass-stationarity by Bernoulli and Cox transports (2011)',
   'url': 'https://repository.lsu.edu/cosa/vol5/iss2/1/',
   'note': 'Bibliographic context for earlier cases credited in the manuscript. The complete final journal body was unavailable for this comparison.'}
 ],
 'follow_up': None,
 'follow_up_reason': candidate['follow_up_reason'],
 'status': 'Unrefereed preprint developed with extensive AI assistance.',
 'ai_disclosure': 'Discovery, checking and manuscript preparation were extensively AI-assisted. This is an unrefereed preprint without independent human peer review or a formal proof-assistant certificate. The supporting package contains the published source and finite controls; those computations do not prove the general theorem.',
 'author': candidate['author'], 'orcid': candidate['orcid'],
 'publication_date': candidate['publication_date'], 'version': candidate['version'], 'doi': candidate['doi'],
 'pdf_filename': candidate['pdf']['filename'], 'supplement_filename': candidate['supplement']['filename'],
 'source_binding': {
  'record_id': '23180194', 'concept_record_id': str(record['conceptrecid']),
  'record_url': candidate['zenodo_url'], 'doi': candidate['doi'],
  'zenodo_version': '1.0', 'manuscript_version': None,
  'manuscript_date': '6 October 2026', 'publication_date': candidate['publication_date'],
  'version_source': 'Zenodo metadata supplies version 1.0. The title page prints 6 October 2026 and Unrefereed research note, without a numbered manuscript version.',
  'version_discrepancy': False, 'source_retrieved_utc': receipt['retrieved_utc'],
  'pdf_sha256': candidate['pdf']['sha256'], 'supplement_sha256': candidate['supplement']['sha256'],
  'files': receipt['files'], 'embedded_assets': [],
  'reviewed_documents': [{'filename': candidate['pdf']['filename'], 'pages': 7, 'read_scope': 'all pages'}],
  'abstract_source': tex_rel, 'abstract_source_sha256': sha(P/tex_rel),
  'abstract_word_count': 113, 'abstract_normalization': 'Only TeX math delimiters, xi, typographic dash and whitespace normalized; complete original abstract retained.',
  'frozen_scope_content_path': 'reviews/scope/candidate-content.json', 'frozen_scope_content_sha256': sha(candidate_path),
  'primary_import_scope': 'Load-bearing Last–Thorisson 2009 interfaces checked in the primary text. Final-body access limits for historical 2011/2015 antecedents do not replace or weaken those checked imports; no exhaustive priority certification.',
  'review_boundary': 'AI analytic, adversarial and scope review at the stated hypotheses; no human peer-review or formal machine-verification claim.'
 }
}
save(P/'publication.json', content)
gate = {
 'record_id': '23180194', 'status': 'PASS', 'disposition_by': 'root',
 'approved_scope': 'For a jointly measurable action of a locally compact second countable Hausdorff Abelian group on arbitrary measurable Ω, sigma-finite Q and covariant locally finite Radon ξ nonzero Q-almost everywhere, invariance of full ambient Q under every invariant pointwise ξ-preserving ξ-measurable Markov transport implies joint Campbell reversal and, by credited classical equivalences, mass-stationarity. Converse credited to Last–Thorisson 2009. No deterministic-only, Cox-only, marginal-only, non-Abelian, zero-measure or first-priority extension.',
 'root_clearance': 'Explicit root authorization received after reading all three full reports: root individual PASS; publication, promotion, rendering and local QA authorized. No deployment or other public mutation authorized to this editor.',
 'created_utc': stamp(), 'pdf_sha256': candidate['pdf']['sha256'],
 'supplement_sha256': candidate['supplement']['sha256'], 'publication_sha256': sha(P/'publication.json'),
 'source_receipt_sha256': sha(P/'sources/receipt.json'), 'source_files': receipt['files'], 'reviews': reviews,
 'scope_gate_resolution': 'The frozen scope verdict predates the final mathematical gates and retains its then-pending mathematical-review fields. Root subsequently read both completed mathematical reports and authorized this scoped PASS; the scope-only verdict is not represented as a mathematical proof review.',
 'source_repair': False, 'human_peer_review': False, 'formal_machine_verification': False
}
save(P/'promotion.json', gate)
save(HERE/'preflight-bindings.json', {
 'timestamp': stamp(), 'status': 'PASS', 'completion_percent': 80,
 'record_sha256': sha(P/'sources/record.json'), 'receipt_sha256': sha(P/'sources/receipt.json'),
 'assets': receipt['files'], 'source_tex': {'path': tex_rel, 'sha256': sha(P/tex_rel)},
 'abstract_word_count': 113, 'extracted_source_files_checked': 19,
 'reviews': {k:{a:b for a,b in v.items() if a!='verdict'} for k,v in reviews.items()},
 'publication_sha256': sha(P/'publication.json'), 'promotion_sha256': sha(P/'promotion.json')
})
(HERE/'RESEARCH_LOG.md').write_text('# Publication-editor log — 23180194\n\n' + stamp() + ' — 80% complete. Root explicitly cleared the exact main theorem after reading all three reports. Original PDF/ZIP sizes, MD5/SHA-256, all 19 extracted files, complete 113-word abstract, actual TeX path, edition/date and review artifact hashes independently rebound. Publication and promotion records created. Original scope pending-review state preserved with chronological resolution. Remaining: render, structural/content QA, unchanged-file check and root browser handoff. No source repair or external publication.\n')
print(json.dumps({'status':'PASS','completion_percent':80,'publication_sha256':sha(P/'publication.json'),'promotion_sha256':sha(P/'promotion.json')}))
