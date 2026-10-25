#!/usr/bin/env python3
"""Source-bound editorial preparation only; no rendering or external writes."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import re

PAPER=Path(__file__).resolve().parents[2]
ROOT=PAPER.parents[1]
OUT=Path(__file__).resolve().parent
ID=PAPER.name
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def write(p,o):
    with p.open('x') as f:f.write(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
assert ID=='23224103'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
clearpath=ROOT/'verification/root-clearance-23224103-20261025.json'
assert sha(clearpath)=='9968ef5b5eec175ae7fcf2ffba58b143d56f5aa3221bbc29d92507573ae8c569'
clear=load(clearpath)
candidate_path=PAPER/'reviews/scope/content.json'
candidate=load(candidate_path)
record=load(PAPER/'sources/record.json')
receipt=load(PAPER/'sources/receipt.json')
texpath=PAPER/'sources/support/brownian_first_visit.tex'
abstract_tex=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',texpath.read_text(),re.S).group(1).strip()
assert abstract_tex==candidate['abstract_original_tex'].strip()
assert re.sub(r'\s+',' ',abstract_tex).replace("Georgakopoulos's",'Georgakopoulos’s')==candidate['abstract']
url='https://aleckriebel.com/research/'+candidate['slug']+'/'
publication={key:copy.deepcopy(candidate[key]) for key in [
    'title','slug','description','abstract','plain_language','result','why_it_works','limitations',
    'background','collaboration','follow_up','followup_rationale','publication_date','version',
    'doi','author','orcid','pdf_filename','supplement_filename']}
publication.update({
    'abstract_heading':'Original abstract','abstract_is_original':True,
    'description':'An explicit deterministic integral series determines the joint law of first-visit territory lengths for any finite number of Brownian particles on a circle.',
    'plain_language':[
        'Imagine several independent particles moving randomly around a circle. Each point belongs to the particle that reaches it first. The question is how all their territory lengths vary together. The particles keep moving through encounters and already visited territory.',
        'This paper describes the entire joint distribution through a Laplace transform. Its coefficients are finite sums of ordinary deterministic integrals built from classical Brownian interval-exit kernels. Tracking a particle’s cumulative elapsed time preserves the correlations between its visits to different points.',
        'The formula covers every finite number of particles, arbitrary fixed distinct labeled starting points, equally spaced starts and independent uniform labeled starts. A uniform factorial bound controls truncation of the outer series. The coefficient integrals can be high-dimensional; no fast evaluator or compact density is claimed.'
    ],
    'result':[
        'Let k≥1 be a finite integer and let p₁,…,p_k be distinct fixed labeled points on the unit circle 𝕋=ℝ/ℤ. The particles are independent standard Brownian motions with generator ½d²/dx² and continue through every encounter and prior visit. Write T_i(x) for particle i’s first physical hitting time of x, assign x to the least label attaining min_i T_i(x), and let L_i be the Lebesgue length of its territory. Almost surely, L lies in the compact simplex {l_i≥0:∑_i l_i=1}.',
        'For real θ_i≥0, set θ_*=max_i θ_i. The joint Laplace transform is ℒ_p(θ)=E_p exp(−∑_i θ_iL_i)=∑_{m=0}∞(−1)^m M_m(θ;p)/m!, with M₀=1. Every coefficient is completely specified by finite permutation and label sums and ordinary spatial/time integrals of explicit scalar interval-exit kernels in equations (2)–(9). No unknown Brownian hitting probability or conditional law remains inside those definitions.',
        'For m queries, a particle’s ordered density is the product of its successive remaining-target kernels. If its discovery order is π_i and elapsed increments are u_ir, its physical hitting time of query j is h_ij=∑_{r≤π_i⁻¹(j)}u_ir. The integration region for owner labels a_j is given by h_(a_j,j)<h_ij for every competing i. These are explicit strict linear inequalities in cumulative clocks, retaining dependence among one walker’s query visits.',
        'For every m≥0, 0≤M_m≤θ_*^m, and the series converges absolutely. For every integer N≥0, |ℒ_p(θ)−∑_{m=0}^N(−1)^m M_m(θ;p)/m!|≤θ_*^(N+1)/(N+1)!. This outer-series bound is uniform over all admissible seed vectors. The entire family of homogeneous coefficient polynomials determines all mixed moments and hence the full joint Borel probability measure on the simplex.',
        'Equally spaced starts use p_i=(i−1)/k. For independent uniform labeled seeds, integrate each fixed-p coefficient over 𝕋^k; the same outer bound holds. Sorting the seeds before assigning labels instead requires the corresponding ordered seed law.'
    ],
    'why_it_works':[
        'Before reaching the next unvisited query point, one walker stays in an arc whose lift is an interval. The classical killed heat kernel gives its two endpoint exit-time densities. With a single query left, both lifted endpoints represent the same target and their fluxes are added, with total mass one.',
        'The strong Markov property at successive finite discovery times gives each walker’s joint order-and-increment density. Removing a reached query changes only the auxiliary stopping targets: the actual particle continues and can cross earlier queries. Products across independent walkers and comparisons of their cumulative physical clocks give every finite-query ownership probability.',
        'Joint measurability and Fubini show that tie locations have zero spatial measure almost surely; the least-label convention still specifies an owner. Spatial integration gives M_m=E_p Z^m for Z=∑_i θ_iL_i. Since 0≤Z≤θ_*, the exponential expansion is absolutely convergent and Taylor’s theorem gives the exact factorial outer remainder.',
        'All homogeneous moment polynomials recover every mixed moment. Polynomial density on the compact simplex then makes the joint measure unique. The uniform bounds also justify averaging over independent uniform labeled seeds. These are classical heat-kernel, strong-Markov, moment and determinacy tools applied to the explicit cumulative-clock construction.'
    ],
    'limitations':[
        'The model uses finitely many independent continuing Brownian particles with a common diffusivity. Stopping, coalescing or absorption at painted territory changes the model. Common positive diffusivity changes rescale all clocks equally; invariance under different per-particle diffusivities is not asserted.',
        'Fixed starting points must be distinct and labeled. No extension to deterministically coincident seeds is claimed. Random-seed collisions, repeated query points and query/seed coincidences are discarded only on their appropriate Lebesgue-null sets.',
        'Ties have zero spatial measure almost surely. This does not say that ties are absent simultaneously at every point. One particle’s different query hitting times remain correlated throughout.',
        'The scalar spectral kernels are summed at each positive time before improper time integration. The factorial bound controls only the outer series for real nonnegative θ; it supplies no inner Fourier-tail, numerical quadrature or coefficient-evaluation certificate.',
        'No compact or named density, efficient numerical algorithm, large-k asymptotic or discrete-to-Brownian convergence theorem is claimed. The Brownian result follows directly from the analytic construction; finite-model and high-precision diagnostics are supplementary evidence.',
        'Independent uniform labeled starts have full permutation exchangeability. Equally spaced labeled starts have cyclic and dihedral symmetry; unrestricted permutation symmetry is not asserted. Both have mean territory length 1/k. A circle of circumference c has lengths cL_i, so its transform uses cθ.',
        'First-arrival painting, interval kernels, strong Markov iteration, moment expansion and compact-support determinacy are established prior methods. Earlier lattice painting, interface, competitive-range and multitime span results receive credit. Historical priority, full novelty, independent discovery and worldwide current-open status remain unverified; incomplete coverage of the Gomes article and Dicker thesis does not support an exhaustive absence claim.',
        'This preprint was prepared with extensive AI assistance and is unrefereed. Internal AI-assisted checks are neither independent human or journal peer review nor formal proof-assistant certification.'
    ],
    'collaboration':'Substantive collaboration on independent verification, extensions with a clear mathematical payoff, or development toward journal submission is welcome. Authorship and responsibilities would be discussed by mutual agreement and would reflect actual research and writing contributions.',
    'supplement_label':'Complete source and supporting materials (ZIP)',
    'additional_assets':[],
    'related_resources':[
        {'label':'Download the complete source and supporting materials (ZIP)','url':url+candidate['supplement_filename']},
        {'label':'Zenodo original source and supporting materials (ZIP)','url':'https://zenodo.org/records/'+ID+'/files/'+candidate['supplement_filename']}
    ],
    'status':'Unrefereed preprint; Zenodo metadata version 1.0, manuscript dated 7 October 2026. Prepared with extensive AI assistance; no human or journal peer review or formal proof-assistant certification is claimed.',
    'ai_disclosure':'AI tools were used extensively in mathematical development, research, checking and writing. Internal AI-assisted review does not constitute independent human or journal peer review. This preprint is unrefereed and has no formal proof-assistant certification. The named author is responsible for its claims, materials and citations.',
    'license':'CC BY 4.0','publication_date_label':'Manuscript and declared publication date',
    'edition_label':'Zenodo metadata version 1.0','citation_edition_label':'Version 1.0, 7 October 2026',
    'edition_note':'The manuscript and Zenodo’s declared publication date are 7 October 2026. Version 1.0 is recorded in Zenodo and support metadata; the manuscript prints the date without a version number. Zenodo created the record on 7 October 2026 UTC. Its later metadata update does not identify a different manuscript edition. These edition dates do not establish historical priority.',
    'bibtex_note':'Unrefereed preprint; version 1.0, manuscript dated 7 October 2026. Zenodo record created 7 October 2026 UTC. Prepared with extensive AI assistance.',
    'canonical_url':url,'pdf_pages':6,
    'keywords':['Brownian first-visit cells','joint Laplace transform','circle','competing random walks','interval-exit kernels','cumulative hitting times','mixed moments','stochastic geometry']
})
for ref in publication['background']:
    if ref['title'].startswith('Peter Mörters'):
        ref['note']='Theorem 2.16 in the 2010 book gives the classical strong Markov property used at successive finite query-discovery times.'
    if ref['title'].startswith('S. R. Gomes'):
        ref['note']='Prior periodic first-arrival painting and one-point/interface calculations are credited. Its full text remains outside the bounded literature coverage supporting the historical comparison.'
publication['source_binding']={
    'record_id':ID,'concept_record_id':str(record['conceptrecid']),'record_url':record['links']['self_html'],
    'doi':record['doi'],'concept_doi':record['conceptdoi'],'version':'1.0','zenodo_version':'1.0','manuscript_version':None,
    'version_source':'Zenodo and support metadata; manuscript prints the date without a version label.',
    'zenodo_publication_date':'2026-10-07','manuscript_date':'7 October 2026',
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
    'frozen_scope_gate':'Original mathematical_verdict=null, mathematical_clearance=false, publication_clearance=false, page_promotion_permission=false and held candidate history remain unchanged; later root authority is separate.',
    'reviewed_documents':[{'source':'standalone','source_relative_path':publication['pdf_filename'],'pages':6,'bytes':88322,'sha256':clear['pdf_sha256'],'editorial_read_scope':'Complete deposited PDF text freshly extracted and read, plus complete deposited TeX. No page rendering, browser or live verification in this assignment.'}],
    'unique_reader_pdf_count':1,'archive_regular_file_count':52,'nested_archive_count':0,'archive_embedded_pdf_count':0,
    'embedded_assets':[],'additional_reader_pdfs':[],
    'archive_reader_note':'The six-page reader is the standalone deposited PDF. The complete support ZIP has no embedded PDF or nested archive. Copy the original ZIP unchanged; ignored third-party primary-cache texts are not website assets.',
    'review_boundary':'All original sources, receipts, scope candidate, reports, complete custom verdicts and seals remain unchanged. Later root scientific disposition resolves the gate separately.',
    'publication_state':'BINDINGS_READY_RENDERING_PENDING'
}
publication['review_metadata']={
    'prepared_utc':now,'completion_percent':100,'scientific_clearance_received':True,
    'root_clearance_file':str(clearpath.relative_to(ROOT)),'root_clearance_sha256':sha(clearpath),
    'publication_state':'BINDINGS_READY_RENDERING_PENDING','rendered':False,'deployed':False,
    'editor_authorization':'Previously absent paper-specific publication/promotion configs and new reviews/editorial artifacts only. Prior two editorial packages remain untouched. No source/review/seal/shared-script/site/Git/Sheet/release/deploy/UI/external-communication mutation. Root retains rendered-copy, local/live HTTP, browser and native publication gates.'
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
    'root_clearance':'Later root scientific disposition only. Complete original custom verdict objects and pending scope fields remain unchanged. This is not a rendered/live/browser/native-publication PASS.',
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
    value=publication[key];sections.append({'id':id,'heading':heading,'paragraphs':[value] if isinstance(value,str) else value})
sections += [
    {'id':'status','heading':'Status and AI use','paragraphs':[publication['ai_disclosure'],publication['edition_note']]},
    {'id':'paper','heading':'Read the paper','paragraphs':['Read the complete six-page paper in the on-page PDF reader.'],
     'links':[{'label':'Open the PDF','url':url+publication['pdf_filename']},{'label':'Download the PDF','url':url+publication['pdf_filename'],'download':True},{'label':'Zenodo original PDF','url':'https://zenodo.org/records/'+ID+'/files/'+publication['pdf_filename']}],
     'iframe':{'src':publication['pdf_filename']+'#view=FitH','title':publication['title']+' — complete paper PDF','loading':'lazy'}},
    {'id':'materials','heading':'Supporting materials','links':[{'label':publication['supplement_label'],'url':url+publication['supplement_filename'],'download':True},{'label':'Zenodo original ZIP','url':'https://zenodo.org/records/'+ID+'/files/'+publication['supplement_filename']}]},
    {'id':'collaborate','heading':'Collaborate on this result','paragraphs':[publication['collaboration']]},
    {'id':'cite','heading':'Cite this paper','paragraphs':['Kriebel, Alec. (2026). '+publication['title']+' (Version 1.0, 7 October 2026) [Preprint]. Zenodo. https://doi.org/'+publication['doi']],
     'links':[{'label':'Download BibTeX','url':url+'citation.bib'}]},
    {'id':'background','heading':'Background and prior work','references':publication['background']}
]
bibtex='@misc{kriebel2026brownianfirstvisit,\n  author = {Kriebel, Alec},\n  title = {'+publication['title']+'},\n  year = {2026},\n  month = oct,\n  doi = {'+publication['doi']+'},\n  url = {'+url+'},\n  version = {1.0},\n  publisher = {Zenodo},\n  note = {'+publication['bibtex_note']+'}\n}\n'
with (OUT/'citation.bib').open('x') as f:f.write(bibtex)
write(OUT/'public-sections.json',{
    'record_id':ID,'state':'PROPOSED_PUBLIC_COPY_NOT_RENDERED','canonical_url':url,
    'header':{'title':publication['title'],'author':publication['author'],'orcid':publication['orcid'],'publication_date':publication['publication_date'],'version':publication['version'],'edition_label':publication['edition_label'],'status':'Unrefereed preprint','description':publication['description']},
    'metadata':{'title':publication['title'],'description':publication['description'],'canonical':url,'citation_title':publication['title'],'citation_author':'Alec Kriebel','citation_author_orcid':publication['orcid'],'citation_publication_date':'2026/10/07','citation_doi':publication['doi'],'citation_pdf_url':url+publication['pdf_filename'],'scholarly_type':'ScholarlyArticle','abstract':publication['abstract'],'license':'https://creativecommons.org/licenses/by/4.0/','creativeWorkStatus':'Unrefereed preprint'},
    'sections':sections,'bibtex':bibtex,'follow_up':None,'native_sheet_aa_url':None
})
lines=['# '+publication['title'],'','By [Alec Kriebel](https://orcid.org/0009-0001-9320-500X), independent researcher. ORCID: 0009-0001-9320-500X.','','Manuscript and declared publication date: 7 October 2026 · Zenodo metadata version 1.0 · Unrefereed preprint','','Canonical URL: '+url,'','Search description: '+publication['description'],'','[Research home](https://aleckriebel.com/research/) · [Zenodo record](https://zenodo.org/records/'+ID+') · [DOI](https://doi.org/'+publication['doi']+') · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)','']
for section in sections:
    lines += ['## '+section['heading'],'']
    for paragraph in section.get('paragraphs',[]):lines += [paragraph,'']
    if section.get('links'):lines += [' · '.join('['+x['label']+']('+x['url']+')' for x in section['links']),'']
    for reference in section.get('references',[]):lines += ['- ['+reference['title']+']('+reference['url']+'): '+reference['note'],'']
    if section['id']=='cite':lines += ['```bibtex',bibtex.rstrip(),'```','']
with (OUT/'PUBLIC_COPY.md').open('x') as f:f.write('\n'.join(lines).rstrip()+'\n')
print(json.dumps({'record_id':ID,'publication_sha256':sha(PAPER/'publication.json'),'promotion_sha256':sha(PAPER/'promotion.json')}))
