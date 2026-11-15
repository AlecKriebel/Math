from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, shutil, html
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024'); Q=P/'papers/23385145'; E=Q/'reviews/editorial'
def load(p): return json.loads(Path(p).read_text())
def dump(p,v): Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for p in (Q/'publication.json',Q/'promotion.json'):
 if p.exists(): raise RuntimeError('Refusing to replace '+str(p))
auth=load(E/'inputs/root-clearance-23385145-20261115.json'); ready=load(E/'inputs/SOURCE_READY.json')
bind=load(E/'metadata-support/SOURCE_PROTOCOL_BINDINGS.json'); rights=load(E/'metadata-support/RIGHTS_AND_IDENTITY.json')
assert auth['status']=='PASS_FULL_FINITE_UNIT_EDGE_MEDIAN_GRAPH_EXACT_OPERATION_THEOREM_WITH_CREDITED_IMPORT_CORRECTIONS_AND_MODEL_LIMITS'
now=datetime.now(timezone.utc).isoformat(); title=rights['title']; slug='multiplicatively-weighted-centers-median-graphs'; proposed='https://aleckriebel.com/research/'+slug+'/'
abstract="We record a short reduction from multiplicatively weighted center thresholds to additively weighted eccentricities on a graph with bounded integral distances. Combining it with the algorithm of Bergé, Ducoffe and Habib and a known implicit optimization method gives a deterministic O(n log⁵(2n)) algorithm for a center, the optimum radius and all centers of every finite unit-edge median graph. This answers the finite algorithmic form of Open Problem 1 in Ducoffe’s Oberwolfach report, without a bound on cube dimension. The contribution is the threshold observation and its consequence; neither the additive algorithm nor the optimization mechanism is new. We specify the exact comparison model and give explicit corrections to two estimates in the public preprint proof of the imported algorithm."
sections={
'plain_language':[
'A weighted center chooses a vertex that minimizes the worst weighted distance to every vertex of a graph. A larger weight makes distance to that vertex more costly. Median graphs include trees and hypercubes; every three vertices have a unique median on all three pairwise shortest-path intervals.',
'This note turns each multiplicative distance threshold into an additive arrival-time problem, then combines credited algorithms to find the exact optimum and every vertex attaining it. The graph may have arbitrarily large cube dimension, and no embedding is supplied.'
],
'result':[
'Let G=(V,E) be a finite, nonempty, connected, simple graph with unit edge lengths, n=|V| and shortest-path distance d. Each vertex u has a finite nonnegative real weight w(u). For a candidate vertex x define r_w(x)=max_{u∈V} w(u)d(x,u), the optimum ρ=min_{x∈V} r_w(x), and the full center set C_w={x∈V:r_w(x)=ρ}.',
'Theorem 1. Given G by adjacency lists, with the promise that G is median, and any such weight profile, a deterministic algorithm computes the exact radius ρ, one vertex in C_w and the entire set C_w in O(n log⁵(2n)) exact operations. No cube-dimension bound or supplied embedding is required. Operations on the original profile only compare bounded integer multiples k w(u), where 0≤k≤n−1.',
'Zero-weight vertices stay in both the graph and the candidate domain. If n=1 or all weights are zero, the radius is zero and every vertex is a center. The result concerns vertex centers with the original shortest-path distances.'
],
'why_it_works':[
'Put D=n−1. For a nonnegative trial radius R, define b_R(u)=max{k∈{0,…,D}:k w(u)≤R} and a_R(u)=D−b_R(u). When w(u)=0, the budget b_R(u) equals D. Bounded binary search finds each budget using comparisons, without a real-division or unbounded-floor primitive.',
'For every vertex x and every R≥0, w(u)d(x,u)≤R is equivalent to d(x,u)≤b_R(u), hence to d(x,u)+a_R(u)≤D. Taking all u gives the exact identity {x:r_w(x)≤R}={x:E_{a_R}(x)≤D}, where E_a(x)=max_u(d(x,u)+a(u)). This preserves the whole feasible set, rather than only deciding whether it is empty. Negative radii are infeasible.',
'The imported Bergé–Ducoffe–Habib algorithm computes all additive eccentricities for a nonnegative integer arrival profile on a median graph in O(n log⁴(2n)) time, including preprocessing. Here 0≤a_R(u)≤D. The short threshold identity works for bounded integral graph distances; the efficient median-graph conclusion uses this credited additive oracle.',
'The optimum is one of the products k w(u). A known implicit optimization mechanism, credited to Ducoffe, searches the n sorted product rows without materializing their n² entries. The note gives a self-contained comparison-only variant: active intervals include their endpoints, lower row middles are weighted by inclusive interval lengths, and feasible equality is saved in an incumbent with a witness before deletion. These rules cover ties and zero rows. Each step deletes at least one quarter of the active entries, so O(log(2n)) oracle calls suffice; a final query at ρ returns every center.',
'The already published appendix supplies consistent estimates for the recursion in the named author preprint arXiv:2410.10235v1. It uses f(s)=2⌈log₂s⌉ for s≥3, direct base cases for s≤2, and a fixed-root depth estimate. Both original-arrival and fiber-arrival slice calls are retained. Total child volume at each depth is at most the root order and depth is O(log²n), giving the required additive O(n log⁴(2n)) bound. The appendix credits BDH’s algorithm and structural discoveries; it makes no assertion that the inaccessible final SODA chapter contains the same proof errors.'
],
'comparison_model':[
'The operation count is an exact comparison model, not an encoding-independent bit-time bound. The optimum can be stored as a pair (k,u) representing k w(u). Overall the search uses O(n log²(2n)) comparisons of original-weight products, in addition to the imported graph operations.',
'For rational input w(u)=p_u/q_u with positive denominators and numerator and denominator components of at most B bits, comparing k w(u) with j w(v) compares k p_u q_v with j p_v q_u. These integers have O(B+log n) bits; their multiplication and comparison costs, and input reading, must be paid. The additive oracle’s bounded integer labels, including its internal updates, use O(log n) bits. The theorem does not promise unit-cost arbitrary-precision arithmetic or a linear-space oracle.'
],
'limitations':[
'The graph is finite, nonempty, connected, simple and unit-edge, supplied by adjacency lists and promised median. Recognition of median graphs, arbitrary edge lengths, continuous facilities along edges and an unspecified encoding of infinite median graphs are outside the theorem. The separate unimodality question in Ducoffe’s report is not settled by this global threshold algorithm.',
'The accompanying package includes exact reference controls, manuscript source and proof comparisons. Its all-pairs and brute-structure routines check finite cases; they are not a fast general implementation or an experimental proof of the asymptotic bound. Reproduction instructions require normal assertion-enabled execution.',
'The contribution is the short threshold observation and its consequence. The additive algorithm, implicit optimization mechanism and classical median preprocessing are credited prior work. The bounded literature assessment does not establish worldwide firstness or continued open status at a later date. The appendix’s corrections are explicitly limited to the named public author-v1 proof, whose log-base and product estimates it addresses; no claim about errors in the final SODA publication is made.'
],
'background':[
'Ducoffe’s Oberwolfach report asks the finite n-vertex weighted-center algorithmic question, within a discussion that also includes infinite graphs, edge lengths and unimodality. This note answers the finite unit-edge vertex-center form without a cube-dimension bound. It does not claim all the separate questions in that discussion.',
'Bergé, Ducoffe and Habib provide the additive all-eccentricities algorithm and its median-graph structure. Ducoffe’s ESA 2026 Lemma 2, and Lemma 2.2 of its full author-v1 preprint, already supply the decision-to-optimization mechanism. Classical median algorithms and preprocessing, including the work of Bénéteau, Chalopin, Chepoi and Vaxès, remain dependencies.',
'For cube-free median graphs, Chalopin, Chepoi, Dragan, Ducoffe and Vaxès already proved the stronger O(n log²n) bound. The present O(n log⁵(2n)) result does not improve that subclass. Algorithms using a supplied tree-product embedding have a stronger representation promise; the unweighted MFCS theorem and the later weighted consequence in the workshop report are not identified as the same statement.'
],
'collaboration':[
'Substantive mathematical verification, extensions within a clearly stated model and collaboration toward journal submission are welcome. Authorship should reflect actual contributions. This is a passive invitation; no claim of an existing collaboration is implied.'
],
'status':[
'Unrefereed preprint. AI tools were used extensively in solving, developing, writing, reproducing and adversarially verifying the work. Internal AI adversarial reviews are not human peer review; the manuscript has not received human peer review or proof-assistant certification.'
]
}
resources=[
{'title':'Ducoffe, Radius functions in median graphs — Oberwolfach report','url':'https://doi.org/10.4171/OWR/2026/8'},
{'title':'Bergé, Ducoffe and Habib — additive median-graph algorithm','url':'https://doi.org/10.1137/1.9781611978322.52'},
{'title':'Named author preprint arXiv:2410.10235v1 — appendix comparison target','url':'https://arxiv.org/abs/2410.10235v1'},
{'title':'Ducoffe, ESA 2026 — prior decision-to-optimization mechanism','url':'https://doi.org/10.4230/LIPIcs.ESA.2026.133'},
{'title':'Ducoffe, full author-v1 preprint','url':'https://arxiv.org/abs/2607.04287v1'},
{'title':'Chalopin et al. — stronger cube-free result','url':'https://arxiv.org/abs/2503.15011v1'},
{'title':'Ducoffe, MFCS 2021 — supplied tree-product embeddings','url':'https://doi.org/10.4230/LIPIcs.MFCS.2021.43'},
{'title':'Bénéteau et al. — classical median algorithms','url':'https://doi.org/10.1016/j.jcss.2022.01.001'}]
rights_text='The paper and authored supporting materials are released under Creative Commons Attribution 4.0 International (CC BY 4.0), as recorded by Zenodo and the package README. Cited third-party publications retain their own rights. No separate code-license grant is identified.'
status='Unrefereed preprint; extensive AI assistance; no human peer review or proof-assistant certification.'
bib='''@misc{kriebel2026multiplicativelyweightedcenters,
  author = {Kriebel, Alec},
  title = {Multiplicatively Weighted Centers of Median Graphs in Quasilinear Time},
  year = {2026},
  month = oct,
  day = {14},
  doi = {10.5281/zenodo.23385145},
  url = {https://doi.org/10.5281/zenodo.23385145},
  publisher = {Zenodo},
  version = {1.0},
  note = {Zenodo API version 1.0; the manuscript prints October 14, 2026 and no version number. Unrefereed preprint.}
}
'''
whole_verdicts=bind['all_three_whole_literal_scientific_verdicts']
source_binding={
 'whole_original_source_ready':ready,'source_ready_path':str(Q/'sources/SOURCE_READY.json'),'source_ready_sha256':sha(Q/'sources/SOURCE_READY.json'),
 'whole_original_native_api_objects':bind['all_four_native_API_objects_in_source_ready_order'],
 'whole_original_seven_native_transport_objects':bind['all_seven_actual_transport_objects_in_original_collection_order'],
 'whole_original_native_transport_aggregate':bind['actual_transport_aggregate'],
 'whole_original_archive_custody':bind['whole_archive_custody'],'whole_original_native_schema_types':bind['native_schema_types'],
 'complete_protocol_binding_file':'reviews/editorial/metadata-support/SOURCE_PROTOCOL_BINDINGS.json','complete_protocol_binding_sha256':sha(E/'metadata-support/SOURCE_PROTOCOL_BINDINGS.json'),
 'all_93_original_ZIP_payloads_preserved':True,'assets_native_order':[x['original_api_file_object']['key'] for x in ready['all_assets_in_original_order']],
 'rights_and_identity_whole':rights,'explicit_printed_version':None,'native_record_created':ready['created'],'native_record_updated':ready['updated'],
 'historical_unread_flags_preserved_literally':True,'whole_objects_not_normalized':True}
reviewmeta={'root_clearance_file':str(P/'verification/root-clearance-23385145-20261115.json'),'root_clearance_sha256':sha(P/'verification/root-clearance-23385145-20261115.json'),
 'whole_root_scientific_clearance_record':auth,'whole_original_custom_family_verdicts':whole_verdicts,'editorial_role':'Informed editorial preparation after science clearance; not a fresh independent scientific review.',
 'root_editorial_copy_adoption_pending':True,'current_five_stage_integration_authorized':False}
publication={'title':title,'slug':slug,'description':'An exact threshold reduction gives the optimum weighted radius and all vertex centers of finite unit-edge median graphs in O(n log⁵(2n)) exact operations, with credited algorithms and explicit bit-model limits.',
'abstract':abstract,'abstract_heading':'Original abstract','abstract_is_original':True,
**sections,'follow_up':None,'followup_rationale':'No follow-up meets the specified evidentiary bar; no public open-problem section is proposed.',
'publication_date':'2026-10-14','version':'1.0','version_field_present':True,'printed_version':None,'doi':'10.5281/zenodo.23385145',
'author':'Alec Kriebel','orcid':'https://orcid.org/0009-0001-9320-500X','pdf_filename':'weighted_centers.pdf','pdf_pages':5,
'reader_intro':'Read the unchanged, searchable five-page manuscript below, or open or download the original PDF. The complete original verification ZIP is available alongside the citation.',
'supplement_filename':'verification_package.zip','supplement_label':'Complete original verification package (ZIP)','additional_assets':[],
'related_resources':resources,'status':status,'ai_disclosure':sections['status'][0],'license':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/','code_license':None,'rights_notice':rights_text,
'publication_date_label':'14 October 2026','edition_label':'Zenodo version 1.0','citation_edition_label':'Zenodo API version 1.0',
'edition_note':'The manuscript prints 14 October 2026 and no version number. Zenodo identifies this record as version 1.0; the record was created on 15 October 2026, separately from its declared publication date.',
'bibtex_note':'Zenodo API version 1.0; no printed manuscript version.','canonical_url':None,'AA':None,'native_sheet_aa_url':None,'proposed_canonical_url':proposed,
'keywords':['median graphs','multiplicatively weighted center','weighted eccentricity','graph algorithms','exact comparison model','threshold reduction'],
'seo':{'title':title+' | Alec Kriebel','description':'Exact weighted vertex centers on finite unit-edge median graphs: full theorem, threshold reduction, credited algorithms and comparison/bit-model limits.','robots':'noindex, nofollow (private candidate only)'},
'prepared_bibtex':bib,'source_binding':source_binding,'review_metadata':reviewmeta}
publication['result'] += publication.pop('comparison_model')
dump(Q/'publication.json',publication)
promotion={'record_id':'23385145','sheet_row':118,'status':'PRIVATE_EDITORIAL_CANDIDATE_PENDING_ROOT_FULL_COPY_ADOPTION','scientific_status':auth['status'],'disposition_by':'GPT-6.1 Sol Ultra editorial lane','created_utc':now,
'approved_scope':'Full original finite unit-edge promised-median adjacency-list exact-operation theorem, radius, one center and all centers, exact comparison and rational bit-cost model; credited imports and named-author-v1-only appendix limits.',
'whole_original_mathematical_scope_supported':True,'root_clearance_file':reviewmeta['root_clearance_file'],'root_clearance_sha256':reviewmeta['root_clearance_sha256'],'whole_root_scientific_clearance_record':auth,
'reviews':whole_verdicts,'whole_original_custom_family_verdicts':whole_verdicts,'whole_original_source_ready':ready,'source_ready_sha256':source_binding['source_ready_sha256'],
'whole_original_native_transport_receipts':bind['all_seven_actual_transport_objects_in_original_collection_order'],'whole_original_native_transport_aggregate':bind['actual_transport_aggregate'],
'whole_original_native_api_objects':bind['all_four_native_API_objects_in_source_ready_order'],'source_receipt_path':bind['actual_transport_aggregate']['path'],'source_receipt_sha256':bind['actual_transport_aggregate']['sha256'],
'pdf_sha256':rights['complete_original_assets'][0]['sha256'],'supplement_sha256':rights['complete_original_assets'][1]['sha256'],
'source_repair':False,'narrowed_replacement':False,'follow_up':None,'human_peer_review':False,'formal_certification':False,
'private_static_candidate_written':True,'current_five_stage_member':False,
**{k:False for k in ['rendered','deployed','rendered_public_copy_approved','rendered_copy_verified','local_http_verified','live_http_verified','live_verified','browser_verified','native_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received','production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified']},
'canonical_url':None,'AA':None,'native_sheet_aa_url':None,'proposed_canonical_url':proposed,'all203_status':'No global completion or publication authority inferred.','publication_sha256':sha(Q/'publication.json')}
dump(Q/'promotion.json',promotion); dump(E/'public-sections.json',{'title':title,'original_abstract':abstract,'sections':sections,'related_resources':resources,'rights':rights_text})
(E/'citation.bib').write_text(bib)
headings={'plain_language':'What the result means','result':'The full result','why_it_works':'Why the reduction works','comparison_model':'Exact comparisons and bit costs','limitations':'Scope and limitations','background':'Background and credit','collaboration':'Contribution and collaboration','status':'AI and review disclosure'}
copy='# '+title+'\n\nAlec Kriebel · 14 October 2026 · Zenodo version 1.0\n\n'+publication['edition_note']+'\n\n## Original abstract\n\n'+abstract+'\n'
for key,paras in sections.items():copy+='\n## '+headings[key]+'\n\n'+'\n\n'.join(paras)+'\n'
copy+='\n## Read and download\n\n'+publication['reader_intro']+'\n\n- [Open original PDF](assets/weighted_centers.pdf)\n- [Download complete original ZIP](assets/verification_package.zip)\n- [Download BibTeX citation](assets/citation.bib)\n- [Zenodo record](https://doi.org/10.5281/zenodo.23385145)\n'
copy+='\n## Primary background\n\n'+'\n'.join('- ['+x['title']+']('+x['url']+')' for x in resources)+'\n\n## Rights\n\n'+rights_text+'\n'
(E/'PUBLIC_COPY.md').write_text(copy)
C=E/'candidate'; A=C/'assets'; A.mkdir(parents=True)
for asset in rights['complete_original_assets']:shutil.copyfile(asset['path'],A/asset['original_api_file_object']['key'])
shutil.copyfile(E/'citation.bib',A/'citation.bib')
esc=html.escape
body='<header><p class="byline">Alec Kriebel · 14 October 2026 · Zenodo version 1.0</p><h1>'+esc(title)+'</h1><p>'+esc(publication['edition_note'])+'</p></header>'
body+='<section id="abstract"><h2>Original abstract</h2><p>'+esc(abstract)+'</p></section>'
for key,paras in sections.items():body+='<section id="'+key.replace('_','-')+'"><h2>'+headings[key]+'</h2>'+''.join('<p>'+esc(p)+'</p>' for p in paras)+'</section>'
body+='<section id="read"><h2>Read and download</h2><p>'+esc(publication['reader_intro'])+'</p><p><a href="assets/weighted_centers.pdf" target="_blank" rel="noopener">Open original PDF</a> · <a href="assets/weighted_centers.pdf" download>Download PDF</a> · <a href="assets/verification_package.zip" download>Complete original ZIP</a> · <a href="assets/citation.bib" download>BibTeX citation</a> · <a href="https://doi.org/10.5281/zenodo.23385145">Zenodo record</a></p><iframe src="assets/weighted_centers.pdf" title="'+esc(title)+' — original five-page PDF"><p><a href="assets/weighted_centers.pdf">Open the original PDF</a></p></iframe></section>'
body+='<section id="background-links"><h2>Primary background</h2><ul>'+''.join('<li><a href="'+esc(x['url'])+'">'+esc(x['title'])+'</a></li>' for x in resources)+'</ul></section><section id="rights"><h2>Rights</h2><p>'+esc(rights_text)+'</p><p><a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International</a></p></section>'
structured={'@context':'https://schema.org','@type':'ScholarlyArticle','headline':title,'description':publication['description'],'abstract':abstract,'author':{'@type':'Person','name':'Alec Kriebel','sameAs':publication['orcid']},'datePublished':'2026-10-14','identifier':'https://doi.org/10.5281/zenodo.23385145','license':publication['license_url'],'keywords':publication['keywords']}
htmltext='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>'+esc(title)+' | Alec Kriebel</title><meta name="description" content="'+esc(publication['seo']['description'])+'"><meta name="citation_title" content="'+esc(title)+'"><meta name="citation_author" content="Alec Kriebel"><meta name="citation_publication_date" content="2026/10/14"><meta name="citation_doi" content="10.5281/zenodo.23385145"><meta name="citation_pdf_url" content="assets/weighted_centers.pdf"><script type="application/ld+json">'+json.dumps(structured,ensure_ascii=False).replace('<','\\u003c')+'</script><style>body{font-family:Arial,sans-serif;color:#222;background:#fff;max-width:820px;margin:0 auto;padding:28px 22px;line-height:1.65}h1{line-height:1.2;font-size:2rem}h2{line-height:1.3;margin-top:2.2rem;font-size:1.35rem}a{color:#24558b}.byline{color:#555}p{overflow-wrap:anywhere}iframe{width:100%;height:850px;border:1px solid #ddd}li{margin:.55em 0}@media(max-width:600px){body{padding:20px 16px}h1{font-size:1.65rem}iframe{height:65vh}}</style></head><body><main>'+body+'</main></body></html>\n'
(C/'index.html').write_text(htmltext)
adapter={'schema':'private-editorial-source-adapter-23385145-v1','UTC':now,'source_binding_complete':source_binding,'review_metadata_complete':reviewmeta,'whole_complete_protocol_binding':bind,
'public_copy_source':'PUBLIC_COPY.md','unique_publication_prose_file':str(Q/'publication.json'),'promotion_file':str(Q/'promotion.json'),'literal_object_policy':'Whole raw objects and byte copies retained; no coercion of field names, null, empty, lists, ordered headers or historical unread flags.',
'private_candidate':'candidate/index.html','public_page_title':title,'proposed_canonical_url':proposed,'canonical_url':None,'AA':None,'follow_up':None,
'new_shared_core_adapter_written':False,'next_batch_only':True,'current_five_stage_integration_authorized':False,'root_full_copy_and_config_adoption_required':True}
adapter['common_renderer_scope_mapping']={'publication.result':'Full theorem and exact comparison/rational bit-cost paragraphs; no new core section dependency.','public-sections.sections.comparison_model':'Same exact paragraphs, separately headed only in the owned static candidate.','all_other_public_sections':'Existing common publication keys or explicit source/status/rights/resource fields; root must adopt all unique paragraphs.'}
dump(E/'SCHEMA_ADAPTER.json',adapter)
req={'schema':'private-publication-requirements-23385145-v1','UTC':now,'full_original_scientific_scope':promotion['approved_scope'],
'complete_original_abstract':True,'original_abstract_transform':'TeX accents/math typography and whitespace to Unicode only; no sentence omitted.',
'full_exact_comparison_and_rational_bit_cost_model_visible':True,'all_center_output_and_zero_boundaries_visible':True,'finite_unit_edge_promise_and_adjacency_visible':True,'no_dimension_or_embedding_requirement':True,
'credited_imports_and_stronger_cube_free_bound_visible':True,'appendix_already_deposited_named_author_v1_only':True,'no_final_SODA_error_assertion':True,'no_general_fast_implementation_or_firstness_claim':True,
'actual_PDF_pages':5,'PDF_searchable_unchanged':True,'full_ZIP_payloads':93,'native_asset_order':['weighted_centers.pdf','verification_package.zip'],
'native_API_version':'1.0','printed_version':None,'declared_and_printed_date':'2026-10-14','record_created_separate':ready['created'],
'actual_license':'CC BY 4.0','separate_code_license':None,'whole_source_and_three_literal_custom_verdicts_preserved':True,'all_seven_actual_transport_objects_preserved':True,
'layout':'Simple white Arial single column; responsive static candidate with searchable original PDF iframe and direct downloads. No browser/layout verification claimed.',
'seo':'Searchable article title/description, original abstract, citation metadata, DOI, ORCID and primary background links. Private candidate is noindex/nofollow and has no assigned canonical.',
'follow_up':None,'passive_contribution_based_collaboration':True,'public_audit_dates_counts_hashes_internal_status_logs':False,
'root_full_copy_adoption_pending':True,'current_five_stage_member':False,'production_integration_authorized':False,'all_public_browser_native_live_AA_gates':False,'canonical_url':None,'AA':None,
'pending_before_any_later_publication':['Root personally adopts full unique prose and configs.','Separate explicit next-batch integration and publication authority.','Actual desktop/mobile display, native PDF/ZIP download and ordinary HTTP identity checks.','Only then assign canonical/AA and native Sheet status under root authority.']}
dump(E/'PUBLICATION_REQUIREMENTS.json',req)
with (E/'RESEARCH_LOG.md').open('a') as f:f.write('\n- '+now+': Full original abstract, exact finite adjacency/promise/unit-edge/all-center theorem, threshold identity, known optimization, appendix-v1-only and comparison/rational-bit limits drafted in private copy/config/candidate. Complete native source/API/transport/whole literal three verdict bindings retained; native-order assets copied byte-for-byte. No current stage integration or public authority. Completion65%.\n')
print('PRIVATE_EDITORIAL_DRAFT_CREATED',len(copy.split()),'words; candidate/configs independent of current stage.')
