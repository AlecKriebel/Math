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
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path): return json.loads(path.read_text())
def write(path,obj):
    with path.open('x') as handle: handle.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

assert ID=='23440119'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
clearpath=ROOT/'verification'/f'root-clearance-{ID}-20261025.json'
assert sha(clearpath)=='8b51684b5e6cd6b36d8dd3302e2bbc5f29f261eb29affa753636812fb15cba56'
clear=load(clearpath)
candidate_path=PAPER/'reviews/scope/content.json'
candidate=load(candidate_path)
record=load(PAPER/'sources/record.json')
receipt=load(PAPER/'sources/receipt.json')
texpath=PAPER/'sources/support/main.tex'
abstract_tex=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',texpath.read_text(),re.S).group(1).strip()
assert abstract_tex==candidate['abstract_original_tex'].strip()
url='https://aleckriebel.com/research/'+candidate['slug']+'/'
publication={key:copy.deepcopy(candidate[key]) for key in [
    'title','slug','description','abstract','plain_language','result','why_it_works','limitations',
    'background','collaboration','follow_up','followup_rationale','publication_date','version',
    'doi','author','orcid','pdf_filename','supplement_filename']}
publication.update({
    'abstract_heading':'Original abstract','abstract_is_original':True,
    'description':'An explicit normal barrier with a third-derivative sign certificate on a known algebraic cone that has no defining hyperbolic polynomial in three variables.',
    'plain_language':[
        'Barrier functions grow without bound near the boundary of a feasible region and help optimization methods stay inside it. This paper studies the additional derivative-sign property called negative curvature in conic optimization.',
        'The region is the known cone of nonnegative triples satisfying xy²≥z³. The paper gives a particular logarithmic barrier and proves its sign condition at every interior point, for every direction in the closed cone and every real test vector, including degenerate directions.',
        'It also proves that no homogeneous polynomial of any degree can have this cone as its hyperbolicity cone in the original three-dimensional space. Together, these properties provide the kind of example requested in Tunçel’s 2017 existential question.',
        'The cone and earlier self-concordant barriers were already known. The contribution presented here is the explicit additional third-derivative certificate and the accompanying obstruction, with no first-discovery claim.'
    ],
    'result':[
        'Let K={(x,y,z)∈ℝ³:x,y,z≥0, xy²≥z³}. It is a regular algebraic convex cone: closed, pointed and convex, with nonempty interior, defined by homogeneous polynomial inequalities. Its interior is {x,y,z>0:xy²>z³}.',
        'On the entire interior, F(x,y,z)=−25 log(z(xy²−z³)) is a logarithmically homogeneous self-concordant normal barrier with parameter 100. In particular, F(λa)=F(a)−100 log λ for λ>0, and its squared dual Hessian gradient norm is exactly 100.',
        'For every a∈int K, every h∈K and every u∈ℝ³, D³F(a)[h,u,u]≤0. The direction h ranges over the closed cone, including zero and its boundary; the claim is semidefinite and includes the degenerate cases.',
        'There is no homogeneous real polynomial H of any degree in the same ℝ³ for which K is its hyperbolicity cone. This is an obstruction for every possible defining H and interior hyperbolicity direction, rather than only for the displayed cubic xy²−z³.'
    ],
    'why_it_works':[
        'The weighted geometric mean x^(1/3)y^(2/3) is concave, so its nonnegative hypograph is convex. Writing g=z³/y² and δ=x−g gives a positive Hessian-norm decomposition for f=−log(xy²−z³)−log z. A mixed third-derivative estimate becomes self-concordance after scaling by 25. The degree-four product z(xy²−z³) gives logarithmic homogeneity with parameter 100, and the product tends to zero at every finite boundary point.',
        'A fixed positive diagonal change of coordinates sends any interior base point to (r,1,1), retaining r>1. Every cone direction is a nonnegative combination of (t³,1,t), t≥0, and the x-axis direction. This reduces the mixed sign assertion to an explicit symmetric matrix.',
        'Exact leading-minor and square identities give a positive matrix for t≠1. A separate lower-block certificate at t=1 and a Gram certificate for the x-axis direction supply the semidefinite cases. The reduction includes t=0, h=0 and directions with h_y=0; no strict-definiteness claim is needed there.',
        'Any proposed defining hyperbolic polynomial must vanish on the curved boundary. Substitution x=z³/y² and Gauss’s lemma force the factor p=xy²−z³ to divide it. For every prospective interior direction e, set A=(e_xe_y²)^(1/3)>B=e_z>0. Along v=(0,0,1), the factor p(v+te) has a quadratic factor with discriminant −3A²<0. Multiplication cannot cancel that nonreal root pair, contradicting hyperbolicity.'
    ],
    'limitations':[
        'Negative curvature here means the mixed third-derivative inequality D³F(a)[h,u,u]≤0, equivalently concavity of a↦DF(a)[h] for each fixed h∈K. It does not assert nonpositive sectional curvature of a Hessian metric. Boundary base points are outside the barrier’s domain, while boundary cone directions are included.',
        'The theorem concerns this one-sided nonnegative cone. It makes no assertion for the sign-symmetric power cone, arbitrary exponents or all regular cones. The broader every-regular-cone barrier question remains a separate credited question.',
        'The cone is already in Hildebrand’s classification. Roy–Xiao give a parameter-3 self-concordant barrier on the same cone. Parameter 100 is an explicit sufficient certificate for the displayed barrier and its additional sign property, with no parameter improvement or optimality claim.',
        'The all-degree polynomial obstruction concerns the original three-dimensional ambient space. It does not exclude projections or higher-dimensional lifts. No general new barrier method or practical algorithmic improvement is asserted.',
        'Historical priority, full novelty and worldwide current-open status remain unverified. Bounded literature coverage does not exclude every predecessor or broader method implication; the full 2026 Hildebrand article and related prepublication remain coverage limits.',
        'The universal statements rest on the analytic proof and exact symbolic identities. Finite rational checks are supplementary evidence. This preprint was prepared with extensive AI assistance and is unrefereed, without human or journal peer review or formal proof-assistant certification.'
    ],
    'collaboration':'Substantive collaboration on independent verification, extensions with a clear mathematical payoff, or development toward journal submission is welcome. Authorship and responsibilities would be discussed by mutual agreement and would reflect actual research and writing contributions.',
    'supplement_label':'Complete source and verification materials (ZIP)',
    'additional_assets':[],
    'related_resources':[
        {'label':'Download the complete source and verification materials (ZIP)','url':url+candidate['supplement_filename']},
        {'label':'Zenodo original source and verification materials (ZIP)','url':'https://zenodo.org/records/'+ID+'/files/'+candidate['supplement_filename']}
    ],
    'status':'Unrefereed preprint; version 1.0.0, dated 17 October 2026. Prepared with extensive AI assistance; no human or journal peer review or formal proof-assistant certification is claimed.',
    'ai_disclosure':'AI tools were used extensively in mathematical development, research, checking and writing. Internal AI-assisted review does not constitute independent human or journal peer review. This preprint is unrefereed and has no formal proof-assistant certification. The named author is responsible for its claims, materials and citations.',
    'license':'CC BY 4.0',
    'publication_date_label':'Manuscript and declared publication date',
    'edition_label':'Version 1.0.0',
    'citation_edition_label':'Version 1.0.0, 17 October 2026',
    'edition_note':'The manuscript and Zenodo’s declared publication date are 17 October 2026, version 1.0.0. Zenodo created the record on 17 October 2026 UTC. These edition dates do not establish historical priority.',
    'bibtex_note':'Unrefereed preprint; version 1.0.0, dated 17 October 2026. Zenodo record created 17 October 2026 UTC. Prepared with extensive AI assistance.',
    'canonical_url':url,'pdf_pages':5,
    'keywords':['negative-curvature normal barrier','self-concordant barriers','power cones','algebraic convex cones','hyperbolic polynomials','conic optimization','mixed third derivatives']
})
publication['background'][2]['note']='Sections 2.2 and 3.1 give the matrix self-concordance and directional-gradient concavity conventions; Section 6 asks the broader universal cone question. The cited edition is arXiv v2.'
publication['background'][3]['url']='https://arxiv.org/abs/1305.4814v1'
publication['background'][3]['note']='Theorem 3.2, family 5 already contains this cone with exponents 3 and 3/2 and coordinates (x₁,x₂,x₃)=(x,z,y). Hyperbolic affine-sphere terminology is distinct from polynomial hyperbolicity.'
publication['background'][4]['note']='Theorem 2 supplies a parameter-3 self-concordant barrier on the same nonnegative cone for weights (1/3,2/3). That theorem supplies prior barrier credit; it does not assert the additional cone-direction third-derivative sign proved here.'
publication['source_binding']={
    'record_id':ID,'concept_record_id':str(record['conceptrecid']),'record_url':record['links']['self_html'],
    'doi':record['doi'],'concept_doi':record['conceptdoi'],'version':'1.0.0','zenodo_version':'1.0.0','manuscript_version':'1.0.0',
    'zenodo_publication_date':'2026-10-17','manuscript_date':'17 October 2026',
    'record_created_utc':record['created'],'record_updated_utc':record['updated'],'source_retrieved_utc':receipt['retrieved_utc'],
    'metadata_path':'sources/record.json','record_path':'sources/record.json','receipt_path':'sources/receipt.json',
    'metadata_sha256':sha(PAPER/'sources/record.json'),'record_sha256':sha(PAPER/'sources/record.json'),
    'record_raw_path':'sources/record-raw.json','record_raw_sha256':sha(PAPER/'sources/record-raw.json'),
    'receipt_sha256':sha(PAPER/'sources/receipt.json'),'source_receipt_sha256':sha(PAPER/'sources/receipt.json'),
    'pdf_sha256':clear['pdf_sha256'],'supplement_sha256':clear['supplement_sha256'],'files':receipt['files'],
    'source_tex_path':str(texpath.relative_to(PAPER)),'source_tex_sha256':sha(texpath),
    'abstract_source':str(texpath.relative_to(PAPER)),'abstract_source_sha256':sha(texpath),
    'abstract_pdf_source':'sources/'+publication['pdf_filename']+'#page=1','abstract_tex':abstract_tex,
    'abstract_tex_sha256':hashlib.sha256(abstract_tex.encode()).hexdigest(),
    'abstract_normalization':candidate['abstract_source'],
    'original_abstract_field':'abstract','abstract_display_heading':'Original abstract',
    'frozen_scope_content_path':str(candidate_path.relative_to(PAPER)),'frozen_scope_content_sha256':sha(candidate_path),'frozen_scope_abstract_field':'abstract',
    'frozen_scope_gate':'Original mathematical_verdict=null, page_promotion_permission=false, HELD_PENDING_SEPARATE_FULL_MATHEMATICAL_GATE and candidate status remain unchanged; later root authority is separate.',
    'reviewed_documents':[{'source':'standalone','source_relative_path':publication['pdf_filename'],'pages':5,'bytes':73062,'sha256':clear['pdf_sha256'],'editorial_read_scope':'Complete actual deposited PDF text freshly extracted and read, plus complete deposited TeX. No rendering, browser or live verification in this assignment.'}],
    'unique_reader_pdf_count':1,'archive_regular_file_count':26,'nested_archive_count':0,'archive_embedded_pdf_count':1,
    'embedded_assets':[],'additional_reader_pdfs':[],
    'archive_reader_note':'The sole embedded reader equals the standalone five-page PDF. Copy the complete deposited ZIP unchanged; ignored third-party primary-cache texts are not website assets.',
    'review_boundary':'All original sources, receipts, scope candidate, reports, full custom verdicts and seals remain unchanged. Later root scientific disposition resolves the gate separately.',
    'publication_state':'BINDINGS_READY_RENDERING_PENDING'
}
publication['review_metadata']={
    'prepared_utc':now,'completion_percent':100,'scientific_clearance_received':True,
    'root_clearance_file':str(clearpath.relative_to(ROOT)),'root_clearance_sha256':sha(clearpath),
    'publication_state':'BINDINGS_READY_RENDERING_PENDING','rendered':False,'deployed':False,
    'editor_authorization':'Previously absent paper-specific publication/promotion configs and new reviews/editorial artifacts only. No source/review/seal/shared-script/site/Git/Sheet/release/deploy/UI/external-communication mutation. Root retains rendered-copy, local/live HTTP, browser and native publication gates.'
}
write(PAPER/'publication.json',publication)
reviews={}
for role,item in clear['reviews'].items():
    reportpath,verdictpath=ROOT/item['report'],ROOT/item['verdict']
    assert sha(reportpath)==item['report_sha256']
    assert sha(verdictpath)==item['verdict_sha256']
    reviews[role]={'report':str(reportpath.relative_to(PAPER)),'sha256':item['report_sha256'],'verdict_file':str(verdictpath.relative_to(PAPER)),'verdict_sha256':item['verdict_sha256'],'verdict':load(verdictpath),'root_disposition':'SCOPE_COMPLETE' if role=='scope' else clear['status']}
promotion={
    'record_id':ID,'status':clear['status'],'disposition_by':clear['disposition_by'],'created_utc':now,'approved_scope':clear['approved_scope'],
    'root_clearance':'Later root scientific disposition only. Complete original custom verdict objects and the pending scope fields remain unchanged. This is not a rendered/live/browser/native-publication PASS.',
    'root_clearance_file':str(clearpath.relative_to(ROOT)),'root_clearance_sha256':sha(clearpath),'root_clearance_record':clear,
    'pdf_sha256':clear['pdf_sha256'],'supplement_sha256':clear['supplement_sha256'],'publication_sha256':sha(PAPER/'publication.json'),
    'source_receipt_sha256':sha(PAPER/'sources/receipt.json'),'source_receipt_record':receipt,
    'metadata_path':'sources/record.json','metadata_sha256':sha(PAPER/'sources/record.json'),'source_files':receipt['files'],
    'source_receipts':{'sources/receipt.json':{'sha256':sha(PAPER/'sources/receipt.json'),'files':len(receipt['files']),'record_raw_sha256':receipt['record_raw_sha256']}},
    'root_custody_receipt':clear['root_custody_receipt'],'root_custody_receipt_sha256':clear['root_custody_receipt_sha256'],
    'root_seal_bindings_rehashed':clear['root_seal_bindings_rehashed'],
    'reviews':reviews,'scope_gate_resolution':clear['scope_gate_resolution'],'source_repair':False,'human_peer_review':False,'formal_machine_verification':False,'follow_up':None,
    'preparation_state':'BINDINGS_READY_RENDERING_PENDING','rendered_copy_verified':False,'live_verified':False,'browser_verified':False,'native_sheet_aa_url':None
}
write(PAPER/'promotion.json',promotion)
sections=[]
for id,heading,key in [('abstract','Original abstract','abstract'),('plain-language','The idea in plain English','plain_language'),('result','The precise result','result'),('proof','Why the result holds','why_it_works'),('limits','Scope and limitations','limitations')]:
    value=publication[key]
    sections.append({'id':id,'heading':heading,'paragraphs':[value] if isinstance(value,str) else value})
sections += [
    {'id':'status','heading':'Status and AI use','paragraphs':[publication['ai_disclosure'],publication['edition_note']]},
    {'id':'paper','heading':'Read the paper','paragraphs':['Read the complete five-page paper in the on-page PDF reader.'],
     'links':[{'label':'Open the PDF','url':url+publication['pdf_filename']},{'label':'Download the PDF','url':url+publication['pdf_filename'],'download':True},{'label':'Zenodo original PDF','url':'https://zenodo.org/records/'+ID+'/files/'+publication['pdf_filename']}],
     'iframe':{'src':publication['pdf_filename']+'#view=FitH','title':publication['title']+' — complete paper PDF','loading':'lazy'}},
    {'id':'materials','heading':'Supporting materials','links':[{'label':publication['supplement_label'],'url':url+publication['supplement_filename'],'download':True},{'label':'Zenodo original ZIP','url':'https://zenodo.org/records/'+ID+'/files/'+publication['supplement_filename']}]},
    {'id':'collaborate','heading':'Collaborate on this result','paragraphs':[publication['collaboration']]},
    {'id':'cite','heading':'Cite this paper','paragraphs':['Kriebel, Alec. (2026). '+publication['title']+' (Version 1.0.0, 17 October 2026) [Preprint]. Zenodo. https://doi.org/'+publication['doi']],
     'links':[{'label':'Download BibTeX','url':url+'citation.bib'}]},
    {'id':'background','heading':'Background and prior work','references':publication['background']}
]
bibtex='@misc{kriebel2026negativecurvature,\n  author = {Kriebel, Alec},\n  title = {'+publication['title']+'},\n  year = {2026},\n  month = oct,\n  doi = {'+publication['doi']+'},\n  url = {'+url+'},\n  version = {1.0.0},\n  publisher = {Zenodo},\n  note = {'+publication['bibtex_note']+'}\n}\n'
with (OUT/'citation.bib').open('x') as handle: handle.write(bibtex)
write(OUT/'public-sections.json',{
    'record_id':ID,'state':'PROPOSED_PUBLIC_COPY_NOT_RENDERED','canonical_url':url,
    'header':{'title':publication['title'],'author':publication['author'],'orcid':publication['orcid'],'publication_date':publication['publication_date'],'version':publication['version'],'edition_label':publication['edition_label'],'status':'Unrefereed preprint','description':publication['description']},
    'metadata':{'title':publication['title'],'description':publication['description'],'canonical':url,'citation_title':publication['title'],'citation_author':'Alec Kriebel','citation_author_orcid':publication['orcid'],'citation_publication_date':'2026/10/17','citation_doi':publication['doi'],'citation_pdf_url':url+publication['pdf_filename'],'scholarly_type':'ScholarlyArticle','abstract':publication['abstract'],'license':'https://creativecommons.org/licenses/by/4.0/','creativeWorkStatus':'Unrefereed preprint'},
    'sections':sections,'bibtex':bibtex,'follow_up':None,'native_sheet_aa_url':None
})
lines=['# '+publication['title'],'','By [Alec Kriebel](https://orcid.org/0009-0001-9320-500X), independent researcher. ORCID: 0009-0001-9320-500X.','','Manuscript and declared publication date: 17 October 2026 · Version 1.0.0 · Unrefereed preprint','','Canonical URL: '+url,'','Search description: '+publication['description'],'','[Research home](https://aleckriebel.com/research/) · [Zenodo record](https://zenodo.org/records/'+ID+') · [DOI](https://doi.org/'+publication['doi']+') · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)','']
for section in sections:
    lines += ['## '+section['heading'],'']
    for paragraph in section.get('paragraphs',[]): lines += [paragraph,'']
    if section.get('links'): lines += [' · '.join('['+x['label']+']('+x['url']+')' for x in section['links']),'']
    for reference in section.get('references',[]): lines += ['- ['+reference['title']+']('+reference['url']+'): '+reference['note'],'']
    if section['id']=='cite': lines += ['```bibtex',bibtex.rstrip(),'```','']
with (OUT/'PUBLIC_COPY.md').open('x') as handle: handle.write('\n'.join(lines).rstrip()+'\n')
print(json.dumps({'record_id':ID,'publication_sha256':sha(PAPER/'publication.json'),'promotion_sha256':sha(PAPER/'promotion.json')}))
