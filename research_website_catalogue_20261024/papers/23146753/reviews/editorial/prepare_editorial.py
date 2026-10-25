"""Create absent private editorial configs and source-bound copy only."""
from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json, re

O=Path(__file__).resolve().parent;D=O.parent.parent;P=D.parent.parent;S=D/'sources'
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(path,value):
    if path.exists():raise RuntimeError('Refusing existing output: '+str(path))
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
ready=read(S/'SOURCE_READY.json');raw=read(S/'record.raw.json');meta=read(S/'normalized-metadata.json')
transport=read(S/'api-and-file-receipts.json');clearpath=P/'verification/root-clearance-23146753-20261025.json';clear=read(clearpath)
if sha(clearpath)!='9f03be990c7b547ebc341908662b241f84b77ffb9b26f9d834d72407d34b7860':raise RuntimeError('Wrong clearance')
if clear['status']!='PASS_WITH_EXPLICIT_PRIMARY_AND_PRIORITY_LIMITS':raise RuntimeError('Wrong exact root status')
texpath=S/'published-source/mtp2_edge_closure.tex';tex=texpath.read_text()
abstract_tex=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
replacements={'MTP$_2$':'MTP₂','Conjecture~1':'Conjecture 1'}
abstract=abstract_tex
for a,b in replacements.items():abstract=abstract.replace(a,b)
abstract=' '.join(abstract.split())
(O/'ORIGINAL_ABSTRACT.tex').write_text(abstract_tex)
title=ready['title'];slug='binary-mtp2-edge-closure';base='/research/'+slug+'/'
pdf='mtp2-edge-closure-note.pdf';archive='mtp2-edge-closure-verification.zip'
pdfurl=next(x['original_api_file_object']['links']['self'] for x in ready['all_assets'] if x['original_api_file_object']['key']==pdf)
zipurl=next(x['original_api_file_object']['links']['self'] for x in ready['all_assets'] if x['original_api_file_object']['key']==archive)
bib='''@misc{Kriebel2026BinaryMTP2EdgeClosure,
  author = {Kriebel, Alec},
  title = {Closedness and attractive approximation of binary MTP2 edge models},
  year = {2026},
  month = {oct},
  day = {4},
  date = {2026-10-04},
  version = {1.0},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23146753},
  url = {https://zenodo.org/records/23146753},
  note = {Unrefereed preprint; extensive AI assistance; no external human peer review or formal proof certification},
  orcid = {0009-0001-9320-500X}
}
'''
(O/'CITATION.bib').write_text(bib)
plain=[
 'A graphical model writes a joint probability distribution as a product of factors attached to vertices and edges. MTP₂ is a positive-dependence condition. This paper asks what happens when some probabilities are zero or when positive attractive Ising models approach the boundary of the probability simplex.',
 'On every fixed finite graph, the MTP₂ distributions that already have finite nonnegative vertex and edge factors are exactly the limits of positive attractive Ising distributions on that same graph. The result includes deterministic coordinates and tied coordinates, while retaining the original edges.',
 'The finite-factor requirement matters. A globally Markov MTP₂ distribution can fail to have such a factorization; the paper explains an earlier four-cycle counterexample and credits its authors.'
]
result=[
 'Fix any finite simple graph G=(V,E) and binary states Ω={0,1}^V. Let F₂(G) consist of normalized probabilities p satisfying p(x∧y)p(x∨y)≥p(x)p(y) for every x,y∈Ω and admitting an actual product of finite nonnegative unary factors and factors on the original edges. Zeros are allowed.',
 'Let A(G) consist of the strictly positive laws proportional to exp(∑ᵢhᵢxᵢ+∑ᵢⱼ∈EJᵢⱼxᵢxⱼ), with arbitrary finite real fields hᵢ and finite nonnegative couplings Jᵢⱼ. Then F₂(G)=closure A(G) in the fixed finite-dimensional probability simplex. In particular, F₂(G) is closed under pointwise limits. No extra edge or hidden variable is introduced.',
 'The note also gives the exact closure corollary for M_I(G)∩M₂(G) in Lauritzen’s 2022 statement, where M_I uses finite real edge factors only. Signs can be removed by absolute values. When E is nonempty, isolated coordinates are jointly uniform and independent under that edge-only convention; these properties survive limits and the remaining unary factors can be absorbed into incident edges.',
 'For nonempty V and no edges, the literal empty product is not a normalized probability, so the source’s literal edge-only family is empty. With a tacit scalar normalization it contains just the uniform law. For V empty the sole mass is 1. These source conventions are distinct from the main unary-and-edge model, which permits arbitrary independent Bernoulli coordinates on an edgeless graph.',
 'For a nonempty edge set, the supplement also shows that a nonempty Boolean sublattice which is facial for the original-edge design is feasible for that same design. In concrete terms, a lattice zero set of a nonnegative finite original-edge energy is recovered from its original-edge projection constraints. This supplies an attributed support-geometric route to the closure corollary.'
]
why=[
 'Finite local factors identify the support from its actual vertex and edge projections. MTP₂ makes that support a lattice. After pinned coordinates are removed, the edge constraints are implications; strongly connected implication classes represent equal coordinates. On the resulting poset, four allowed support states force each aggregate interaction between incomparable classes to be nonnegative. Individual supplied potentials need not be attractive.',
 'The aggregate interactions can be placed on existing edges. Penalizing the original pin and implication violations then gives positive attractive laws converging to the desired distribution. Their mass on the original support has a strictly positive limiting normalizer.',
 'For the reverse direction, a classical cut representation and maximum-flow residual reparameterization give bounded unary and original-edge factors. Their product is W(x)=exp(−E(x)+min E), so max W=1 and 1≤∑ₓW(x)≤2^|V|. Compactness therefore yields limiting finite factors without losing normalization. The argument allows finite real capacities and does not rely on an integer-capacity algorithm terminating.'
]
limits=[
 'This is a finite, binary, pairwise, fixed-graph theorem. It does not assert factorization for every globally Markov MTP₂ law, or extend to arbitrary clique interactions, infinite graphs, nonbinary states, hidden variables or changing graphs. It gives no uniform-in-graph approximation rate or efficient general factor-reconstruction algorithm.',
 'Gandolfi–Lenarda’s earlier four-cycle law illustrates the boundary: its support has x₃=x₄, with mass 2/9 at 1111 and 1/9 at the other seven supported states. It is MTP₂ and globally Markov, but violates an identity obeyed by every original-edge factorization. This is a prior counterexample to separate factorization claims, not a new counterexample or a contradiction to the smaller finite-factor theorem.',
 'The proof uses established toric support geometry, lattice-support ideas, positive-potential theory and graph-cut/flow tools. The comparison with prior work is limited to the cited editions; historical first priority and current worldwide open status are not certified. No new underlying-method or independent-discovery claim is made. Finite computations illustrate examples; the arbitrary-graph theorem rests on the written proof.'
]
background=[
 dict(title='S. Lauritzen, Two open problems in graphical models of algebraic nature, OWR 55/2022, pp. 3125–3127',url='https://doi.org/10.4171/OWR/2022/55',note='Conjecture 1 is the exact edge-only closure question addressed here. The accompanying factorization conjectures are separate.'),
 dict(title='D. Geiger, C. Meek and B. Sturmfels, On the toric algebra of graphical models (2006)',url='https://doi.org/10.1214/009053606000000263',note='The classical distinction between toric closure and finite nonnegative factorization depends on support feasibility and faciality.'),
 dict(title='T. Kahle and S. Sullivant, Lattice supported distributions and graphical models, arXiv:2411.03139v1 (2024)',url='https://arxiv.org/abs/2411.03139v1',note='Their natural-lattice, clique-factor limit theorem and cover/feasibility framework are prior work. Pins, repeated coordinates and the original-edge design require the additional steps stated in this note.'),
 dict(title='S. Lauritzen, C. Uhler and P. Zwiernik, Total positivity in exponential families with application to binary variables (2021)',url='https://doi.org/10.1214/20-AOS2007',note='Binary lattice-support reconstruction and compact extended MTP₂ graphical families provide established background; an extended family is distinct from finite original-edge factors.'),
 dict(title='S. Fallat and coauthors, Total positivity in Markov structures (2017)',url='https://doi.org/10.1214/16-AOS1478',note='The positive-pair-potential criterion is classical. Its cancellation converse is not extended indiscriminately to factors with zero entries.'),
 dict(title='V. Kolmogorov and R. Zabih, What energy functions can be minimized via graph cuts? (2004)',url='https://doi.org/10.1109/TPAMI.2004.1262177',note='The binary submodular cut construction is classical; it represents pairwise interactions without extra nonterminal variables.'),
 dict(title='J.-C. Picard and M. Queyranne, On the structure of all minimum cuts in a network and applications (1979 report; published 1980)',url='https://doi.org/10.1007/BFb0120902',note='Residual reachability and cut-flow identities supply classical foundations for the bounded-factor gauge.'),
 dict(title='V. Kolmogorov and C. Rother, Minimizing nonsubmodular functions with graph cuts—a review (2007)',url='https://doi.org/10.1109/TPAMI.2007.1031',note='Maximum-flow residual updates as energy reparameterizations are established tools; the separate doubled-node QPBO construction is not needed here.'),
 dict(title='A. Gandolfi and P. Lenarda, A note on Gibbs and Markov random fields with constraints and their moments, vol. 4 (nominal 2016), pp. 407–422; published 13 April 2017',url='https://doi.org/10.2140/memocs.2016.4.407',note='Lemma 5.2 gives the exact earlier four-cycle obstruction discussed here. Kahle–Sullivant later give a related equality-support example.')
]
ai='AI tools were used extensively in research, proof development, literature work, writing and code. This is an unrefereed preprint without external human peer review or formal proof-assistant certification; the named author is responsible for the work.'
collab='Substantive proof checks, counterexamples and precise comparisons with prior work are welcome. Authorship and acknowledgments would reflect actual research contributions and mutual agreement. Citations credit prior work and imply no participation or endorsement.'
status='Unrefereed preprint, Zenodo version 1.0. Developed with extensive AI assistance; no external human peer review or formal proof certification.'
publication=dict(title=title,slug=slug,
 description='Binary MTP₂ laws with finite vertex and edge factors are exactly the limits of positive attractive Ising laws on the same finite graph, including zero cells.',
 abstract=abstract,abstract_heading='Original abstract',abstract_is_original=True,plain_language=plain,result=result,why_it_works=why,limitations=limits,background=background,
 ai_disclosure=ai,collaboration=collab,follow_up=None,followup_rationale='Default none; no independently supported substantial research follow-up added.',AA=None,canonical_url=None,
 publication_date='2026-10-04',version='1.0',version_field_present=True,doi='10.5281/zenodo.23146753',author='Alec Kriebel',orcid='https://orcid.org/0009-0001-9320-500X',
 pdf_filename=pdf,pdf_pages=5,supplement_filename=archive,supplement_label='Complete source and verification archive (ZIP)',additional_assets=[],
 related_resources=[dict(label='Zenodo original PDF',url=pdfurl),dict(label='Zenodo original complete ZIP',url=zipurl)],status=status,license='CC BY 4.0',license_url='https://creativecommons.org/licenses/by/4.0/',
 publication_date_label='Manuscript and declared publication date',edition_label='Zenodo version 1.0',citation_edition_label='Zenodo version 1.0',
 edition_note='Manuscript and declared publication date: 4 October 2026. Zenodo records version 1.0; the manuscript prints no version number.',
 reader_intro='Read the complete 5-page deposited paper in the on-page PDF reader.',bibtex_note='Unrefereed preprint; extensive AI assistance; no external human peer review or formal proof certification',prepared_bibtex=bib)
publication['source_binding']=dict(record_id='23146753',concept_record_id=ready['conceptrecid'],record_url='https://zenodo.org/records/23146753',doi=ready['doi'],version='1.0',version_field_present=True,zenodo_version='1.0',manuscript_version=None,manuscript_version_printed=False,
 version_provenance='Actual Zenodo metadata declares1.0; current PDF/TeX print4October2026 and no version label.',zenodo_publication_date='2026-10-04',manuscript_date='2026-10-04',record_created_utc=ready['created'],record_updated_utc=ready['updated'],
 metadata_path='sources/normalized-metadata.json',metadata_sha256=sha(S/'normalized-metadata.json'),raw_record_path='sources/record.raw.json',raw_record_sha256=sha(S/'record.raw.json'),
 source_receipt_path='sources/SOURCE_READY.json',source_receipt_sha256=sha(S/'SOURCE_READY.json'),source_receipt_schema='Original all_assets/original_api_file_object/lowercase md5/sha256; ZIP then PDF; original ready plus separate additive source manifest/seal.',source_receipt_original=copy.deepcopy(ready),source_assets_field='all_assets',all_assets=copy.deepcopy(ready['all_assets']),published_file_objects=copy.deepcopy(raw['files']),published_asset_count=2,
 recursive_archive_inventory_path='sources/archive-members.json',recursive_archive_inventory_sha256=sha(S/'archive-members.json'),transport_receipt_path='sources/api-and-file-receipts.json',transport_receipt_sha256=sha(S/'api-and-file-receipts.json'),transport_receipt_original=copy.deepcopy(transport),transport_receipt_entry_count=5,
 asset_root_path='sources',pdf_sha256=clear['pdf_sha256'],supplement_sha256=clear['supplement_sha256'],source_tex_path='sources/published-source/mtp2_edge_closure.tex',source_tex_sha256=sha(texpath),abstract_tex=abstract_tex,abstract_source='reviews/editorial/ORIGINAL_ABSTRACT.tex',abstract_source_sha256=sha(O/'ORIGINAL_ABSTRACT.tex'),abstract_normalization=dict(whitespace='fold consecutive whitespace into one ordinary space',exact_presentational_replacements=replacements,no_word_or_sentence_omission=True),
 public_page_reader_pdf_count=1,archive_outer_regular_file_count=13,archive_regular_member_occurrences=13,archive_container_count=1,nested_archive_count=0,archive_embedded_pdf_count=1,total_distinct_reader_pdf_count=1,reader_intro=publication['reader_intro'],prepared_bibtex_path='reviews/editorial/CITATION.bib',prepared_bibtex_sha256=sha(O/'CITATION.bib'),publication_state='EDITORIAL_CONFIGS_READY_RENDERING_PENDING',review_boundary='Complete root scientific authority separately adopted; original family/source objects and false/null history retained whole.')
publication['review_metadata']=dict(prepared_utc=utc(),completion_percent=100,scientific_clearance_received=True,scientific_clearance_status=clear['status'],root_clearance_file=str(clearpath.relative_to(P)),root_clearance_sha256=sha(clearpath),publication_state='EDITORIAL_CONFIGS_READY_RENDERING_PENDING',rendered=False,deployed=False,rendered_public_copy_approved=False,local_http_verified=False,live_http_verified=False,browser_verified=False,native_sheet_publication_verified=False,public_page_published=False,native_sheet_aa_url=None,root_editorial_clearance_received=False)
write(D/'publication.json',publication)
reviews={}
for fam,r in clear['reviews'].items():
 verdict=read(P/r['verdict'])
 if verdict!=r['whole_original_custom_verdict']:raise RuntimeError('Whole verdict mismatch')
 reviews[fam]=dict(report=str((P/r['report']).relative_to(D)),report_sha256=r['report_sha256'],verdict_file=str((P/r['verdict']).relative_to(D)),verdict_sha256=r['verdict_sha256'],verdict=copy.deepcopy(verdict),root_authority_entry=copy.deepcopy(r))
promotion=dict(record_id='23146753',status=clear['status'],disposition_by='root',created_utc=utc(),approved_scope=clear['approved_scope'],root_clearance_file=str(clearpath.relative_to(P)),root_clearance_sha256=sha(clearpath),root_clearance_record=copy.deepcopy(clear),publication_sha256=sha(D/'publication.json'),pdf_sha256=clear['pdf_sha256'],supplement_sha256=clear['supplement_sha256'],
 source_receipt_path='sources/SOURCE_READY.json',source_receipt_sha256=sha(S/'SOURCE_READY.json'),source_receipt_schema=publication['source_binding']['source_receipt_schema'],source_receipt_original=copy.deepcopy(ready),all_assets=copy.deepcopy(ready['all_assets']),published_file_objects=copy.deepcopy(raw['files']),metadata_path='sources/normalized-metadata.json',metadata_sha256=sha(S/'normalized-metadata.json'),raw_record_path='sources/record.raw.json',raw_record_sha256=sha(S/'record.raw.json'),transport_receipt_path='sources/api-and-file-receipts.json',transport_receipt_sha256=sha(S/'api-and-file-receipts.json'),transport_receipt_original=copy.deepcopy(transport),
 root_custody_receipt=clear['root_custody_receipt'],root_custody_receipt_sha256=clear['root_custody_receipt_sha256'],reviews=reviews,version='1.0',source_repair=False,human_peer_review=False,formal_machine_verification=False,follow_up=None,canonical_url=None,AA=None,preparation_state='SCIENTIFICALLY_CLEARED_EDITORIAL_READY_RENDERING_PENDING',rendered_public_copy_approved=False,local_http_verified=False,live_http_verified=False,browser_verified=False,native_sheet_publication_verified=False,public_page_published=False,native_sheet_aa_url=None,root_editorial_clearance_received=False)
write(D/'promotion.json',promotion)
fields=['title','description','abstract_heading','abstract','plain_language','result','why_it_works','limitations','background','status','ai_disclosure','collaboration','reader_intro','edition_label','citation_edition_label','edition_note','license','license_url']
write(O/'public-sections.json',{k:publication[k] for k in fields})
reader=dict(planned_path=base,pdf_local_href=base+pdf,zip_local_href=base+archive,pdf_original_href=pdfurl,zip_original_href=zipurl,
 pdf_iframe_count=1,pdf_iframe_title=title+' — complete 5-page paper',pdf_iframe_uses_unchanged_local_bytes=True,
 required_links=[dict(label='Open PDF',href=base+pdf,download=False),dict(label='Download PDF',href=base+pdf,download=True),dict(label='Download original PDF from Zenodo',href=pdfurl,download=True),dict(label='Download complete ZIP',href=base+archive,download=True),dict(label='Download original complete ZIP from Zenodo',href=zipurl,download=True),dict(label='Download BibTeX',href=base+'citation.bib',download=True)],
 article_assets=['index.html',pdf,archive,'citation.bib'],extra_assets=[],layout='Existing white Arial/Helvetica single-column article',canonical_contract='Exact self canonical, h1 self link and schema/OG URL from configured origin plus planned_path; canonical_url/AA remain null until separate gates.',license_header_and_schema='CC BY 4.0; https://creativecommons.org/licenses/by/4.0/',prepared_bibtex=bib,
 later_exact_visible_text_checks=['complete original abstract one indexable paragraph','full public paragraphs','4 October2026 manuscript/declared date','Zenodo version1.0 distinct from unprinted manuscript version','exact prepared citation edition','complete AI/unrefereed/human/formal status paragraphs'])
write(O/'READER_REQUIREMENTS.json',reader)
parts=['# '+title,'Alec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)',
 'Manuscript and declared publication date: 4 October 2026 · Zenodo version 1.0 · Unrefereed preprint · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)',publication['edition_note'],'## Original abstract',abstract]
for heading,paras in [('In plain language',plain),('The precise result',result),('Why it works',why),('Scope and limitations',limits)]:parts += ['## '+heading,*paras]
parts += ['## Background and prior work',*[f"[{x['title']}]({x['url']}) {x['note']}"for x in background], '## Research status',status,ai,'## Contributions',collab,'## Read the paper',publication['reader_intro']]
parts += [' · '.join(f"[{x['label']}]({x['href']})"for x in reader['required_links']), '[Selected Zenodo edition](https://zenodo.org/records/23146753)',
 '## Cite this paper',f'Alec Kriebel. (2026). {title} (Zenodo version 1.0) [Preprint]. Zenodo. [DOI 10.5281/zenodo.23146753](https://doi.org/10.5281/zenodo.23146753).']
(O/'PUBLIC_COPY.md').write_text('\n\n'.join(parts)+'\n')
write(O/'INTAKE_RECORD.json',dict(utc=utc(),science_complete_at_intake=True,root_clearance_status=clear['status'],root_clearance_sha256=sha(clearpath),fake_pending_scientific_history_created=False,publication_previously_absent=True,promotion_previously_absent=True,editorial_scope_only=True,all_later_gates_false=True))
print(json.dumps(dict(created=['publication.json','promotion.json','PUBLIC_COPY.md','public-sections.json','READER_REQUIREMENTS.json','CITATION.bib'],description_characters=len(publication['description']),public_words=len((O/'PUBLIC_COPY.md').read_text().split()),original_transport_entries=len(transport),root_status=promotion['status']),indent=2))
