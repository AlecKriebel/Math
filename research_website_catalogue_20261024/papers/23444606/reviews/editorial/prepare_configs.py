#!/usr/bin/env python3
"""Prepare only this paper's previously absent editorial publication bindings."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import re

PAPER = Path(__file__).resolve().parents[2]
ROOT = PAPER.parents[1]
OUT = Path(__file__).resolve().parent
ID = PAPER.name

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path):
    return json.loads(path.read_text())

def write(path, obj):
    with path.open('x') as handle:
        handle.write(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

assert ID == '23444606'
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
clearpath = ROOT/'verification'/f'root-clearance-{ID}-20261025.json'
assert sha(clearpath) == '8f9acb77adf26af8699a42bfdc1f706e2c77978ae722083f8be50d63f8e89aa1'
clear = load(clearpath)
candidate_path = PAPER/'reviews/scope/candidate.json'
candidate = load(candidate_path)
record = load(PAPER/'sources/record.json')
receipt = load(PAPER/'sources/receipt.json')
texpath = PAPER/'sources/published-source/initial-omnific-models-source-and-verification/main.tex'
abstract_tex = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', texpath.read_text(), re.S).group(1).strip()
assert re.sub(r'\s+', ' ', abstract_tex) == candidate['abstract']
url = 'https://aleckriebel.com/research/'+candidate['slug']+'/'
publication = {key: copy.deepcopy(candidate[key]) for key in [
    'title','slug','description','abstract','plain_language','result','why_it_works',
    'limitations','background','collaboration','follow_up','followup_rationale',
    'publication_date','version','doi','author','orcid','pdf_filename']}
publication.update({
    'abstract_heading': 'Original abstract',
    'abstract_is_original': True,
    'description': 'Every discrete initial additive surreal group has an order-preserving additive copy inside the omnific integers that is initial in the ambient surreal numbers.',
    'plain_language': [
        'The surreal numbers contain real numbers, infinite quantities and infinitesimals. Each also has a sign sequence describing its position in a construction tree. An initial group contains every proper sign-sequence prefix of each of its elements.',
        'This paper considers actual additive subgroups of the surreal numbers with that closure property and a smallest positive element. It constructs an equivalent copy inside the omnific integers. The copy remains initial in the ambient surreal numbers, and the equivalence preserves addition and numerical order.',
        'The construction relabels the exponents in the normal forms already present and rescales the lowest coefficient group. It applies to sets and proper classes while keeping each individual support set-sized.'
    ],
    'result': [
        'Work in NBG set theory with global choice. Let G be an actual initial ordered additive subgroup of No, with addition and order inherited from No. If G is nonzero, assume that it has a least positive element. Then there is an order-group isomorphism T:G→H onto an actual subgroup H⊆Oz that is initial in No. The statement includes set and proper-class groups; the zero group uses the identity.',
        'Here initial means closure under all proper ordinal-length sign-sequence prefixes in the ambient No. It is distinct from convexity in numerical order. The isomorphism is required to preserve addition and numerical order; it need not preserve simplicity or multiplication.',
        'For nonzero G, its least occurring exponent is m=−α for a set ordinal α, with bottom pure coefficient group R_m=2^(−n)ℤ for a nonnegative integer n. The explicit exponent map sends m to zero, and T multiplies only its bottom coefficients by 2^n. Thus H=T[G] has nonnegative exponents and pure coefficient group ℤ at zero.',
        'This supplies an affirmative answer to the discrete additive-group question in Kaplan’s 2015 thesis, Kaplan’s joint-work contribution with Ehrlich in the 2016 Oberwolfach report, and Question 9.1 of the Ehrlich–Kaplan author manuscript. Those historical formulations do not establish a first-discovery claim.'
    ],
    'why_it_works': [
        'Write a=(−)^α and let e be the empty sequence. On the ray s≥a, the map sends a to e; sends s>a to (+)s when s does not extend a; and sends a(+)t to (+)at. Ordered concatenation of sign blocks makes this a strictly increasing map with initial image of minimum zero, including limit ordinal lengths and empty tails.',
        'The map reflects target right-simplicity-predecessor obligations. Since zero cannot be a right predecessor in its nonnegative image, normalizing the bottom coefficient group to ℤ creates no new requirement for dyadic coefficients there.',
        'Increasing exponent relabeling and positive coefficient scaling preserve addition, cancellation and leading-term order. The construction transports precisely the actual set-sized supports in G. Truncations and pure coefficient groups are tracked directly; the credited Ehrlich–Kaplan characterization then gives ambient initiality, and the standard omnific normal-form criterion gives H⊆Oz.',
        'The published appendix supplies a detailed sufficiency proof for that credited characterization. It adjoins pure terms, then actual limit-length supports through legal integer-perturbation cuts, and orders those adjunctions by support length. For a proper class, it applies the set argument to each actual support together with its exponent prefixes. Standard surreal arithmetic, simplicity, normal-form and monomial/pure-multiple/limit-series cut facts remain explicit classical inputs.'
    ],
    'limitations': [
        'The theorem assumes an actual discrete initial additive subgroup of No. It gives no embedding theorem for arbitrary abstract ordered groups or arbitrary noninitial surreal subgroups. It does not say that the original G is already contained in Oz or that H equals all of Oz.',
        'No ring, field, multiplicative or simplicity-preserving isomorphism is asserted. H is the actual image T[G]; no full Hahn completion is adjoined.',
        'The setting is NBG with global choice. A group or exponent domain may be a proper class, but every individual normal-form support is a set. The argument uses no class-sized support, sum or cut and no stronger class-recursion principle.',
        'The initial-group characterization and real-coefficient and least-positive classifications are prior work of Ehrlich–Kaplan. The negative-ordinal minimum observation and general exponent-relabeling/positive-scaling mechanisms also have established antecedents. The contribution presented here is the particular sign operation, its right-prefix control and its application to the actual subgroup, together with the published dependency argument.',
        'Historical priority, full novelty and worldwide current-open status remain unverified. Bounded literature coverage, including unread full texts of the 2001 predecessor and Ehrlich’s 2024 handbook chapter, does not support an exhaustive absence-of-prior-work claim. Numbering of the main classical interfaces refers to the cited author manuscript; identity with every publisher edition is not asserted.',
        'Finite verification programs are supplementary diagnostics. The arbitrary-ordinal, infinite-support and proper-class assertions depend on the written proof and its explicitly cited classical foundations. This is an unrefereed preprint prepared with extensive AI assistance, without human or journal peer review or formal proof-assistant certification.'
    ],
    'collaboration': 'Substantive collaboration on independent verification, comparison with prior work, or development toward journal submission is welcome. Authorship and responsibilities would be discussed by mutual agreement and would reflect actual research and writing contributions.',
    'supplement_filename': 'initial-omnific-models-source-and-verification.zip',
    'supplement_label': 'Complete source and verification materials (ZIP)',
    'additional_assets': [],
    'related_resources': [
        {'label': 'Download the complete source and verification materials (ZIP)', 'url': url+'initial-omnific-models-source-and-verification.zip'},
        {'label': 'Zenodo original source and verification materials (ZIP)', 'url': 'https://zenodo.org/records/'+ID+'/files/initial-omnific-models-source-and-verification.zip'}
    ],
    'status': 'Unrefereed preprint; Zenodo metadata version 1.0.0, manuscript dated 17 October 2026. Prepared with extensive AI assistance; no human or journal peer review or formal proof-assistant certification is claimed.',
    'ai_disclosure': 'AI tools were used extensively in mathematical development, research, checking and writing. Internal AI-assisted review does not constitute independent human or journal peer review. This preprint is unrefereed and has no formal proof-assistant certification. The named author is responsible for its claims, materials and citations.',
    'license': 'CC BY 4.0',
    'publication_date_label': 'Manuscript and declared publication date',
    'edition_label': 'Zenodo metadata version 1.0.0',
    'citation_edition_label': 'Version 1.0.0, 17 October 2026',
    'edition_note': 'The manuscript and Zenodo’s declared publication date are 17 October 2026. Version 1.0.0 is the Zenodo metadata label; the manuscript prints the date without a version number. Zenodo created the record on 18 October 2026 UTC. These edition dates do not establish historical priority.',
    'bibtex_note': 'Unrefereed preprint; Zenodo metadata version 1.0.0, manuscript dated 17 October 2026. Zenodo record created 18 October 2026 UTC. Prepared with extensive AI assistance.',
    'canonical_url': url,
    'pdf_pages': 7,
    'keywords': ['surreal numbers','initial additive subgroups','omnific integers','ordinal sign sequences','ordered abelian groups','normal forms','Hahn groups','NBG with global choice']
})
publication['background'][2]['note'] = 'The author manuscript supplies the canonical normal-form correspondence, initial-group characterization, real-coefficient and omnific criteria, and Question 9.1. Numbered statements here refer to that author edition; the related journal publication is JSL 83 (2018), 617–633, DOI 10.1017/jsl.2017.9.'
publication['background'][3]['note'] = 'Lemma 3.2 in this 2016 arXiv edition records the negative-ordinal minimum observation for an initial exponent set.'
publication['background'][4]['note'] = 'Proposition 3.9 and Construction 3.10 describe established exponent-relabeling and positive coefficient-scaling mechanisms. The specific initial-image requirement is proved in the present note.'
binding = copy.deepcopy(candidate['source_binding'])
binding.update({
    'version': publication['version'],
    'concept_doi': record['conceptdoi'],
    'metadata_path': 'sources/record.json', 'record_path': 'sources/record.json', 'receipt_path': 'sources/receipt.json',
    'metadata_sha256': sha(PAPER/'sources/record.json'),
    'source_receipt_sha256': sha(PAPER/'sources/receipt.json'),
    'source_retrieved_utc': receipt['retrieved_utc'],
    'supplement_sha256': clear['supplement_sha256'],
    'abstract_tex': abstract_tex,
    'abstract_tex_sha256': hashlib.sha256(abstract_tex.encode()).hexdigest(),
    'abstract_source': str(texpath.relative_to(PAPER)),
    'abstract_source_sha256': sha(texpath),
    'abstract_normalization': 'Whitespace normalization only; every word and sentence is retained.',
    'abstract_pdf_source': 'sources/'+publication['pdf_filename']+'#page=1',
    'original_abstract_field': 'abstract', 'abstract_display_heading': 'Original abstract',
    'frozen_scope_content_path': str(candidate_path.relative_to(PAPER)),
    'frozen_scope_content_sha256': sha(candidate_path),
    'frozen_scope_abstract_field': 'abstract',
    'frozen_scope_gate': 'Original SCOPE_COMPLETE_PENDING_MATHEMATICAL_REVIEW, mathematical_pass=null, root_publication_clearance=false and candidate_only=true remain unchanged; later root authority is separate.',
    'reviewed_documents': [{'source': 'standalone','source_relative_path': publication['pdf_filename'],'pages': 7,'bytes': (PAPER/'sources'/publication['pdf_filename']).stat().st_size,'sha256': clear['pdf_sha256'],'editorial_read_scope': 'Complete deposited PDF text freshly extracted and read against complete deposited TeX, including published appendix. No rendering, browser or live verification in this assignment.'}],
    'unique_reader_pdf_count': 1, 'archive_regular_file_count': 145,
    'nested_archive_count': 0, 'archive_embedded_pdf_count': 1,
    'embedded_assets': [], 'additional_reader_pdfs': [],
    'archive_reader_note': 'The sole embedded reader equals the standalone seven-page PDF. The complete deposited ZIP must be copied unchanged; third-party primary-cache texts are not website assets.',
    'review_boundary': 'All original sources, scope candidate, receipts, custom verdicts and seals are preserved. Later root scientific disposition resolves the gate separately.',
    'publication_state': 'BINDINGS_READY_RENDERING_PENDING'
})
publication['source_binding'] = binding
publication['review_metadata'] = {
    'prepared_utc': now,'completion_percent': 100,'scientific_clearance_received': True,
    'root_clearance_file': str(clearpath.relative_to(ROOT)),'root_clearance_sha256': sha(clearpath),
    'publication_state': 'BINDINGS_READY_RENDERING_PENDING','rendered': False,'deployed': False,
    'editor_authorization': 'Previously absent paper-specific publication/promotion configs and new reviews/editorial artifacts only. No source/review/seal/shared-script/site/Git/Sheet/release/deploy/UI/external-communication mutation. Root retains rendered-copy, local/live HTTP, browser and native publication gates.'
}
write(PAPER/'publication.json', publication)
reviews = {}
for role, item in clear['reviews'].items():
    reportpath, verdictpath = ROOT/item['report'], ROOT/item['verdict']
    assert sha(reportpath) == item['report_sha256']
    assert sha(verdictpath) == item['verdict_sha256']
    reviews[role] = {'report': str(reportpath.relative_to(PAPER)),'sha256': item['report_sha256'],'verdict_file': str(verdictpath.relative_to(PAPER)),'verdict_sha256': item['verdict_sha256'],'verdict': load(verdictpath),'root_disposition': 'SCOPE_COMPLETE' if role == 'scope' else clear['status']}
promotion = {
    'record_id': ID,'status': clear['status'],'disposition_by': clear['disposition_by'],'created_utc': now,
    'approved_scope': clear['approved_scope'],
    'root_clearance': 'Later root scientific disposition only. Full original custom verdict objects and the pending scope fields remain unchanged. This is not a rendered/live/browser/native-publication PASS.',
    'root_clearance_file': str(clearpath.relative_to(ROOT)),'root_clearance_sha256': sha(clearpath),'root_clearance_record': clear,
    'pdf_sha256': clear['pdf_sha256'],'supplement_sha256': clear['supplement_sha256'],
    'publication_sha256': sha(PAPER/'publication.json'),
    'source_receipt_sha256': sha(PAPER/'sources/receipt.json'),'source_receipt_record': receipt,
    'metadata_path': 'sources/record.json','metadata_sha256': sha(PAPER/'sources/record.json'),
    'source_files': receipt['files'],
    'source_receipts': {'sources/receipt.json': {'sha256': sha(PAPER/'sources/receipt.json'),'files': len(receipt['files']),'record_sha256': receipt['record_sha256']}},
    'root_custody_receipt': clear['root_custody_receipt'],'root_custody_receipt_sha256': clear['root_custody_receipt_sha256'],
    'root_seal_bindings_rehashed': clear['root_seal_bindings_rehashed'],
    'reviews': reviews,'scope_gate_resolution': clear['scope_gate_resolution'],
    'source_repair': False,'human_peer_review': False,'formal_machine_verification': False,'follow_up': None,
    'preparation_state': 'BINDINGS_READY_RENDERING_PENDING','rendered_copy_verified': False,'live_verified': False,'browser_verified': False,'native_sheet_aa_url': None
}
write(PAPER/'promotion.json', promotion)
sections = [
    {'id':'abstract','heading':'Original abstract','paragraphs':[publication['abstract']]},
    {'id':'plain-language','heading':'The idea in plain English','paragraphs':publication['plain_language']},
    {'id':'result','heading':'The precise result','paragraphs':publication['result']},
    {'id':'proof','heading':'Why the result holds','paragraphs':publication['why_it_works']},
    {'id':'limits','heading':'Scope and limitations','paragraphs':publication['limitations']},
    {'id':'status','heading':'Status and AI use','paragraphs':[publication['ai_disclosure'],publication['edition_note']]},
    {'id':'paper','heading':'Read the paper','paragraphs':['Read the complete seven-page paper in the on-page PDF reader.'],'links':[
        {'label':'Open the PDF','url':url+publication['pdf_filename']},
        {'label':'Download the PDF','url':url+publication['pdf_filename'],'download':True},
        {'label':'Zenodo original PDF','url':'https://zenodo.org/records/'+ID+'/files/'+publication['pdf_filename']}],
     'iframe':{'src':publication['pdf_filename']+'#view=FitH','title':publication['title']+' — complete paper PDF','loading':'lazy'}},
    {'id':'materials','heading':'Supporting materials','links':[
        {'label':publication['supplement_label'],'url':url+publication['supplement_filename'],'download':True},
        {'label':'Zenodo original ZIP','url':'https://zenodo.org/records/'+ID+'/files/'+publication['supplement_filename']}]},
    {'id':'collaborate','heading':'Collaborate on this result','paragraphs':[publication['collaboration']]},
    {'id':'cite','heading':'Cite this paper','paragraphs':['Kriebel, Alec. (2026). '+publication['title']+' (Version 1.0.0, 17 October 2026) [Preprint]. Zenodo. https://doi.org/'+publication['doi']],
     'links':[{'label':'Download BibTeX','url':url+'citation.bib'}]},
    {'id':'background','heading':'Background and prior work','references':publication['background']}
]
bibtex = '@misc{kriebel2026initialomnific,\n  author = {Kriebel, Alec},\n  title = {'+publication['title']+'},\n  year = {2026},\n  month = oct,\n  doi = {'+publication['doi']+'},\n  url = {'+url+'},\n  version = {1.0.0},\n  publisher = {Zenodo},\n  note = {'+publication['bibtex_note']+'}\n}\n'
with (OUT/'citation.bib').open('x') as handle: handle.write(bibtex)
write(OUT/'public-sections.json', {
    'record_id':ID,'state':'PROPOSED_PUBLIC_COPY_NOT_RENDERED','canonical_url':url,
    'header':{'title':publication['title'],'author':publication['author'],'orcid':publication['orcid'],'publication_date':publication['publication_date'],'version':publication['version'],'edition_label':publication['edition_label'],'status':'Unrefereed preprint','description':publication['description']},
    'metadata':{'title':publication['title'],'description':publication['description'],'canonical':url,'citation_title':publication['title'],'citation_author':'Alec Kriebel','citation_author_orcid':publication['orcid'],'citation_publication_date':'2026/10/17','citation_doi':publication['doi'],'citation_pdf_url':url+publication['pdf_filename'],'scholarly_type':'ScholarlyArticle','abstract':publication['abstract'],'license':'https://creativecommons.org/licenses/by/4.0/','creativeWorkStatus':'Unrefereed preprint'},
    'sections':sections,'bibtex':bibtex,'follow_up':None,'native_sheet_aa_url':None
})
lines = ['# '+publication['title'],'','By [Alec Kriebel](https://orcid.org/0009-0001-9320-500X), independent researcher. ORCID: 0009-0001-9320-500X.','','Manuscript and declared publication date: 17 October 2026 · Zenodo metadata version 1.0.0 · Unrefereed preprint','','Canonical URL: '+url,'','Search description: '+publication['description'],'','[Research home](https://aleckriebel.com/research/) · [Zenodo record](https://zenodo.org/records/'+ID+') · [DOI](https://doi.org/'+publication['doi']+') · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)','']
for section in sections:
    lines += ['## '+section['heading'],'']
    for paragraph in section.get('paragraphs',[]): lines += [paragraph,'']
    if section.get('links'): lines += [' · '.join('['+x['label']+']('+x['url']+')' for x in section['links']),'']
    for reference in section.get('references',[]): lines += ['- ['+reference['title']+']('+reference['url']+'): '+reference['note'],'']
    if section['id']=='cite': lines += ['```bibtex',bibtex.rstrip(),'```','']
with (OUT/'PUBLIC_COPY.md').open('x') as handle: handle.write('\n'.join(lines).rstrip()+'\n')
print(json.dumps({'record_id':ID,'publication_sha256':sha(PAPER/'publication.json'),'promotion_sha256':sha(PAPER/'promotion.json')}))
