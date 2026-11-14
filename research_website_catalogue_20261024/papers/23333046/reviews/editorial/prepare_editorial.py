"""One-time private editorial preparation. Refuses existing paper configs.

Uses the preceding article's presentation fields only; every scientific,
source, metadata and adoption object is specific to this record.
"""
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,json
O=Path(__file__).resolve().parent;T=O.parent.parent;P=T.parent.parent
ROOT=P/'verification/root-clearance-23333046-20261025.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def write(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def need(v,msg):
 if not v:raise RuntimeError(msg)
need(not (T/'publication.json').exists() and not (T/'promotion.json').exists(),'Existing configs')
need(sha(ROOT)=='56a4dbb028c9017b4df3a559ffb5eefd087dbe312b511c10afee0a2f73d24ff6','Wrong root authority')
now=datetime.now(timezone.utc).isoformat();ready=load(T/'sources/SOURCE_READY.json');raw=load(T/'sources/record.raw.json');root=load(ROOT);transport=load(T/'sources/api-receipts.json')
texpath=T/'sources/published-source/local_deformation_devissage_v1/research_note.tex'
tex=texpath.read_text();original=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
(O/'ORIGINAL_ABSTRACT.tex').write_text(original)
replacements={r'$\F_4$':'F₄',r'$t\mapsto t/(1+at)$':'t↦t/(1+at)',r'$\F_2$':'F₂','restriction--induction':'restriction–induction'}
abstract=original
for a,b in replacements.items():abstract=abstract.replace(a,b)
abstract=' '.join(abstract.split());need('\\' not in abstract and '$' not in abstract,'Unconverted abstract notation')
title=raw['metadata']['title'];slug='characteristic-two-local-devissage'
plain=[
 'Dévissage asks whether deformations of a group action can be assembled from deformations of a subgroup and its quotient. This note gives a characteristic-two action for which the proposed formally smooth fibre-product factorization fails.',
 'The obstruction rules out every prorepresentable recipient in the stated category, regardless of tangent dimension. It combines a known involution deformation pathology with an injective tangent restriction map. The precise coordinate-equivalence category is essential.'
]
result=[
 'Let k=F₄=F₂[u]/(u²+u+1), G=(k,+), N=(F₂,+), Q=G/N, and ρ(a)(t)=t/(1+at). This is the standard weakly ramified additive action on k[[t]].',
 'Work with local Artinian W(k)-algebras with identified residue field k. D_H consists of lifts of the given local action modulo all coordinate changes reducing to the identity, including changes with nilpotent constant terms. D_N^Q is the actual fixed subfunctor of D_N.',
 'There is no prorepresentable recipient F=h_R, with R a complete Noetherian local W(k)-algebra with residue k, and no choice of natural maps f:D_N^Q→F←D_Q:g that makes the actual restriction–induction map D_G→D_N^Q×_F D_Q formally smooth. This holds for every tangent dimension of F, including the one-dimensional recipient prescribed in the refined question.',
 'The theorem uses the actual deformation functors and their fixed subfunctor. It does not replace either component by a versal hull or assume a formula for the tangent maps of arbitrary natural transformations.'
]
why=[
 'The invariant parameter y=t²/(1+t) identifies the subgroup-fixed ring with k[[y]], and the quotient acts by σ(y)=y/(1+y). A nonzero quotient tangent is represented by (y+ε)/(1+y) over k[ε]/ε². The known involution conjugacy, or the known collision under an injection of coefficient rings, forces every natural map to a prorepresentable Hom-functor to send this tangent to the residue basepoint.',
 'Separately, invariant derivations restrict precisely to M=y k[[y]]∂y. With z=y²/(1+y), the quotient action on the complete module M=y k[[z]]∂y⊕y²k[[z]]∂y has kernel equal to image for its characteristic-two cohomology differential. Thus H¹(Q,Θ^N)=0, giving injectivity of tangent restriction. This is a full formal-series argument.',
 'For any proposed recipient maps, the pair (0_N,v) is therefore a genuine point of the fibre product over the dual numbers, with v nonzero. Formal smoothness would lift it to a G-deformation with zero restriction and nonzero induction. Injective restriction forces that deformation to be zero, whose induction is zero, giving a contradiction already over k[ε]/ε²→k.'
]
limits=[
 'The statement concerns this specific F₄ additive action and its F₂ subgroup in the original unframed category. Fixing the zero section, choosing a framed category, replacing actual functors by hulls, using global deformation functors, or allowing arbitrary nonprorepresentable recipients changes the problem.',
 'The separate variant assuming that both the subgroup and quotient deformation functors are prorepresentable remains unaddressed. The example uses the exceptional nonprorepresentable involution component and does not contradict the conditional obstruction-space theorems.',
 'The additive action, involution parameter-shift conjugacy, failure to preserve injections and resulting all-recipient tangent collapse are established antecedents. The note combines them with the restriction-kernel calculation to obstruct the proposed factorization. Historical first priority and continued worldwide openness through 2026 are not certified.',
 'Finite exact calculations support explicit identities. The all-formal-series and all-natural-transformation quantifiers depend on the written proof; they do not follow from finite-jet experiments.'
]
background=[
 {'title':'J. Byszewski, Dévissage for local deformation functors, Oberwolfach Reports 54/2008, pp. 3038–3040',
  'url':'https://ems.press/content/serial-article-files/46200',
  'note':'The unrestricted question on page 3039 is distinct from Theorem 3, which adds component-prorepresentability hypotheses.'},
 {'title':'J. Byszewski, Cohomological aspects of equivariant deformation theory, Utrecht Ph.D. thesis (2009)',
  'url':'https://dspace.library.uu.nl/handle/1874/33749',
  'note':'Question 6.4.4 and the separate conditional result provide the thesis formulation of the same question.'},
 {'title':'J. Byszewski, Deformation functors of local actions, arXiv:1112.0352v1 (2011)',
  'url':'https://arxiv.org/abs/1112.0352v1',
  'note':'Supplies the deformation-category, actual fixed-functor, restriction/induction and tangent-cohomology framework. Question 4.4 and Remark 4.5 keep the unrestricted and conditional formulations separate.'},
 {'title':'J. Byszewski and G. Cornelissen, Which weakly ramified group actions admit a universal formal deformation? (2009)',
  'url':'https://doi.org/10.5802/aif.2450',
  'note':'The additive action and exceptional involution pathology are prior work. Proposition 4.1 gives the parameter-shift conjugacy; Proposition 6.1 gives the injection collision, from which all-recipient tangent collapse follows by naturality.'}
]
ai=('AI tools were used extensively in research, proof development, code, literature work and writing. '
    'This is an unrefereed research note without external human peer review, journal acceptance or formal proof-assistant certification; '
    'the named author is responsible for the work.')
collab=('Substantive proof checks, counterexamples and precise comparisons with prior work are welcome. '
        'Authorship and acknowledgments would reflect actual research contributions and mutual agreement. '
        'Citations credit prior work and imply no participation or endorsement.')
status=('Unrefereed research note, Zenodo version 1.0. Extensive AI assistance; '
        'no external human peer review, journal acceptance or formal proof-assistant certification.')
description='For a standard characteristic-two local action, no prorepresentable recipient makes restriction–induction formally smooth, in any tangent dimension.'
note='Unrefereed research note; extensive AI assistance; no external human peer review or formal proof-assistant certification'
bib=("@misc{Kriebel2026CharacteristicTwoDevissage,\n  author = {Kriebel, Alec},\n  title = {"+title+"},\n"
     "  year = {2026},\n  month = {oct},\n  day = {12},\n  date = {2026-10-12},\n  version = {1.0},\n"
     "  publisher = {Zenodo},\n  doi = {10.5281/zenodo.23333046},\n  url = {https://zenodo.org/records/23333046},\n"
     "  note = {"+note+"},\n  orcid = {0009-0001-9320-500X}\n}\n")
(O/'CITATION.bib').write_text(bib)
archive,pdf=ready['all_assets_in_original_order'];pdfname=pdf['original_api_file_object']['key'];zipname=archive['original_api_file_object']['key']
pu=pdf['original_api_file_object']['links']['self'];zu=archive['original_api_file_object']['links']['self']
sb={'record_id':'23333046','concept_record_id':raw['conceptrecid'],'record_url':raw['links']['self_html'],'doi':raw['doi'],
 'version':'1.0','version_field_present':True,'zenodo_version':'1.0','manuscript_version':None,'manuscript_version_printed':False,
 'version_provenance':'Actual Zenodo metadata and original README declare1.0; actual PDF/TeX print12October2026(research note), with no version label.',
 'zenodo_publication_date':'2026-10-12','manuscript_date':'2026-10-12','record_created_utc':ready['created'],'record_updated_utc':ready['updated'],
 'metadata_path':'sources/normalized-metadata.json','metadata_sha256':sha(T/'sources/normalized-metadata.json'),
 'metadata_provenance':'Existing explicitly derivative object; native raw record/readiness remain authoritative and unchanged.',
 'raw_record_path':'sources/record.raw.json','raw_record_sha256':sha(T/'sources/record.raw.json'),
 'source_receipt_path':'sources/SOURCE_READY.json','source_receipt_sha256':sha(T/'sources/SOURCE_READY.json'),
 'source_receipt_schema':'Original all_assets_in_original_order/original_api_file_object/absolute paths/lowercase hashes; ZIP then PDF; five original HTTP_status/body receipt objects.',
 'source_receipt_original':copy.deepcopy(ready),'source_assets_field':'all_assets_in_original_order',
 'all_assets_in_original_order':copy.deepcopy(ready['all_assets_in_original_order']),
 'published_file_objects':copy.deepcopy(raw['files']),'published_asset_count':2,
 'recursive_archive_inventory_path':'sources/archive-members.json','recursive_archive_inventory_sha256':sha(T/'sources/archive-members.json'),
 'transport_receipt_path':'sources/api-receipts.json','transport_receipt_sha256':sha(T/'sources/api-receipts.json'),
 'transport_receipt_original':copy.deepcopy(transport),'transport_receipt_entry_count':5,'asset_root_path':'sources',
 'pdf_sha256':pdf['sha256'],'supplement_sha256':archive['sha256'],
 'source_tex_path':str(texpath.relative_to(T)),'source_tex_sha256':sha(texpath),
 'abstract_tex':original,'abstract_source':'reviews/editorial/ORIGINAL_ABSTRACT.tex','abstract_source_sha256':sha(O/'ORIGINAL_ABSTRACT.tex'),
 'abstract_normalization':{'whitespace':'fold consecutive whitespace into one ordinary space','exact_presentational_replacements':replacements,'no_word_or_sentence_omission':True},
 'public_page_reader_pdf_count':1,'archive_outer_regular_file_count':154,'archive_regular_member_occurrences':154,
 'archive_container_count':1,'nested_archive_count':0,'archive_embedded_pdf_count':1,'total_distinct_reader_pdf_count':1,
 'reader_intro':'Read the complete 5-page deposited paper in the on-page PDF reader.',
 'prepared_bibtex_path':'reviews/editorial/CITATION.bib','prepared_bibtex_sha256':sha(O/'CITATION.bib'),
 'license_provenance':'Actual native metadata cc-by-4.0 and actual original README Licence: CC BY 4.0; third-party works retain their own rights.',
 'publication_state':'EDITORIAL_CONFIGS_READY_RENDERING_PENDING','review_boundary':'Original family/source false/null history and known-antecedent/category/priority limits preserved whole; exact root scientific adoption separate.'}
gates={'rendered':False,'deployed':False,'rendered_public_copy_approved':False,'local_http_verified':False,'live_http_verified':False,
 'browser_verified':False,'native_sheet_publication_verified':False,'public_page_published':False,
 'native_sheet_aa_url':None,'root_editorial_clearance_received':False}
pub={'title':title,'slug':slug,'description':description,'abstract':abstract,'abstract_heading':'Original abstract','abstract_is_original':True,
 'plain_language':plain,'result':result,'why_it_works':why,'limitations':limits,'background':background,'ai_disclosure':ai,'collaboration':collab,
 'follow_up':None,'followup_rationale':'Default none; no independently supported substantial follow-up added.','AA':None,'canonical_url':None,
 'publication_date':'2026-10-12','version':'1.0','version_field_present':True,'doi':raw['doi'],'author':'Alec Kriebel','orcid':'https://orcid.org/0009-0001-9320-500X',
 'pdf_filename':pdfname,'pdf_pages':5,'supplement_filename':zipname,'supplement_label':'Complete source and verification archive (ZIP)',
 'additional_assets':[],'related_resources':[{'label':'Zenodo original PDF','url':pu},{'label':'Zenodo original complete ZIP','url':zu}],
 'status':status,'license':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/',
 'publication_date_label':'Manuscript and declared publication date','edition_label':'Zenodo version 1.0','citation_edition_label':'Zenodo version 1.0',
 'edition_note':'Manuscript and declared publication date: 12 October 2026. Zenodo records version 1.0; the manuscript prints no version number.',
 'reader_intro':sb['reader_intro'],'bibtex_note':note,'prepared_bibtex':bib,'source_binding':sb,
 'review_metadata':{'prepared_utc':now,'completion_percent':100,'scientific_clearance_received':True,'scientific_clearance_status':root['status'],
 'root_clearance_file':str(ROOT.relative_to(P)),'root_clearance_sha256':sha(ROOT),'publication_state':'EDITORIAL_CONFIGS_READY_RENDERING_PENDING',**gates}}
(T/'publication.json').write_text(json.dumps(pub,indent=2,ensure_ascii=False)+'\n')
reviews={}
for family,entry in root['reviews'].items():
 verdict=load(P/entry['verdict']);need(verdict==entry['whole_original_custom_verdict'],'Original verdict mismatch')
 reviews[family]={'report':entry['report'],'report_sha256':entry['report_sha256'],'verdict_path':entry['verdict'],
 'verdict_sha256':entry['verdict_sha256'],'verdict':copy.deepcopy(verdict),'root_authority_entry':copy.deepcopy(entry)}
prom={'record_id':'23333046','status':root['status'],'disposition_by':'root','created_utc':now,'approved_scope':root['claim'],
 'approved_category':root['category'],'root_clearance_file':str(ROOT.relative_to(P)),'root_clearance_sha256':sha(ROOT),
 'root_clearance_record':copy.deepcopy(root),'publication_sha256':sha(T/'publication.json'),'pdf_sha256':pdf['sha256'],'supplement_sha256':archive['sha256'],
 'source_receipt_path':'sources/SOURCE_READY.json','source_receipt_sha256':sha(T/'sources/SOURCE_READY.json'),'source_receipt_schema':sb['source_receipt_schema'],
 'source_receipt_original':copy.deepcopy(ready),'transport_receipt_original':copy.deepcopy(transport),'reviews':reviews,'AA':None,'canonical_url':None,'follow_up':None,**gates}
(T/'promotion.json').write_text(json.dumps(prom,indent=2,ensure_ascii=False)+'\n')
sec={k:copy.deepcopy(pub[k]) for k in ['title','description','status','edition_label','edition_note','abstract_heading','abstract','plain_language','result','why_it_works','limitations','background','ai_disclosure','collaboration','reader_intro']}
sec['citation']=f'Alec Kriebel (2026). {title}. Zenodo version 1.0, 12 October 2026. https://doi.org/10.5281/zenodo.23333046.'
sec['license']='CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/'
write('public-sections.json',sec)
route='/research/'+slug+'/'
req={'planned_path':route,'pdf_local_href':route+pdfname,'zip_local_href':route+zipname,'pdf_original_href':pu,'zip_original_href':zu,
 'pdf_iframe_count':1,'pdf_iframe_title':title+' — complete 5-page paper','pdf_iframe_uses_unchanged_local_bytes':True,
 'required_links':[{'label':'Open PDF','href':route+pdfname,'download':False},{'label':'Download PDF','href':route+pdfname,'download':True},
 {'label':'Download original PDF from Zenodo','href':pu,'download':True},{'label':'Download complete ZIP','href':route+zipname,'download':True},
 {'label':'Download original complete ZIP from Zenodo','href':zu,'download':True},{'label':'Download BibTeX','href':route+'citation.bib','download':True}],
 'article_assets':['index.html',pdfname,zipname,'citation.bib'],'extra_assets':[],'layout':'Existing white Arial/Helvetica single-column article',
 'canonical_contract':'Exact self canonical/h1 self-link/schema/OG URL from configured origin plus planned_path; AA/canonical remain null until separate gates.',
 'navigation_contract':'Named Research navigation points exactly to /research/.','license_header_and_schema':'CC BY 4.0; https://creativecommons.org/licenses/by/4.0/',
 'prepared_bibtex':bib,'later_exact_visible_text_checks':['Entire original abstract, one indexable paragraph','All full public/status paragraphs',
 '12 October2026 declared/manuscript date; API1.0 distinct from unprinted manuscript version','Complete all-recipient theorem with actual category/fixed functor and conditional-variant limit']}
write('READER_REQUIREMENTS.json',req)
parts=['# '+title,'Alec Kriebel · Independent researcher · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)',
 '12 October 2026 · Zenodo version 1.0 · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)',status,pub['edition_note']]
for h,b in [('Overview',plain),('Original abstract',[abstract]),('The result',result),('Why the proof works',why),('Scope and limits',limits)]:parts+=['## '+h,*b]
parts+=['## References and credit']
parts+=['['+r['title']+']('+r['url']+'). '+r['note'] for r in background]
parts+=['## AI and review status',ai,'## Collaboration',collab,'## Read the paper and source',pub['reader_intro']]
parts+=['['+r['label']+']('+r['href']+')' for r in req['required_links']]
parts+=['## Citation',sec['citation'],'```bibtex\n'+bib.rstrip()+'\n```']
(O/'PUBLIC_COPY.md').write_text('\n\n'.join(parts)+'\n')
originals=[T/'sources'/n for n in ['SOURCE_READY.json','SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json','SOURCE_FINAL_MANIFEST.json','SOURCE_FINAL_SEAL.json',
 'record.raw.json','latest.raw.json','versions.raw.json','normalized-metadata.json','api-receipts.json','archive-members.json']]
originals += [ROOT,T/'reviews/root/ROOT_REVIEW.md',T/'reviews/root/custody-recheck-20261025.json']+[P/x['verdict'] for x in root['reviews'].values()]
(O/'original-objects').mkdir(exist_ok=True);copies=[]
for i,path in enumerate(originals):
 n=f'{i+1:02d}-'+path.name;(O/'original-objects'/n).write_bytes(path.read_bytes());copies.append({'original':str(path),'copy':'original-objects/'+n,'bytes':path.stat().st_size,'sha256':sha(path)})
write('ORIGINAL_OBJECT_COPIES.json',{'objects':copies,'custody_copies_not_source_aliases':True})
write('INTAKE_RECORD.json',{'utc':now,'record_id':'23333046','scientific_authority_complete_at_intake':True,'root_scientific_status':root['status'],
 'no_invented_pending_phase':True,'configs_absent_at_intake':True,'whole_PDF_TeX_three_reports_and_verdicts_root_authority_read':True,
 'source_programs_executed':0,'mathematical_controls_executed':0,'AA':None,'canonical':None,'follow_up':None,**gates})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(f'{now} — checkpoint70%: full manuscript/controlTeX/root/all3reports/customobjects/nativeAPI/transports/README licence read; fullscope copy and absent configs prepared, original objects retained. Static controls/custody/report/seal remain.\n')
print(json.dumps({'prepared':True,'public_words':len((O/'PUBLIC_COPY.md').read_text().split()),'original_object_copies':len(copies)},indent=2))
