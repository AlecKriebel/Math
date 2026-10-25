"""One-time private editorial preparation, never a source/programme replay.

Writes only this new folder and the two previously absent paper configs.
Do not rerun after final sealing.
"""
from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json, re

O=Path(__file__).resolve().parent
T=O.parent.parent
P=T.parent.parent
UTC=datetime.now(timezone.utc).isoformat()
ROOT=P/'verification/root-clearance-23124601-20261025.json'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path): return json.loads(path.read_text())
def write(name,obj): (O/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def need(value,msg):
    if not value: raise RuntimeError(msg)

need(not (T/'publication.json').exists() and not (T/'promotion.json').exists(),
     'Refusing existing paper configs')
need(sha(ROOT)=='61b359b6474c370fa985cac952d391134815e7af8ae243f025417343b470b626',
     'Wrong scientific authority')
ready=load(T/'sources/SOURCE_READY.json')
raw=load(T/'sources/record.raw.json')
root=load(ROOT)
transport=load(T/'sources/transport-receipts.json')
tex=(T/'sources'/ready['controlling_TeX']['path']).read_text()
abstract_tex=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
(O/'ORIGINAL_ABSTRACT.tex').write_text(abstract_tex)
replacements={
 r'\(B_6/\normal{ch^{-1}}\)':'B₆/⟨⟨ch⁻¹⟩⟩',
 r'\(c^2\)':'c²',
 r'\(c=(a_1a_2a_3a_4)^5\)':'c=(a₁a₂a₃a₄)⁵',
 r'\(h=a_5a_4a_3a_2a_1^2a_2a_3a_4a_5\)':'h=a₅a₄a₃a₂a₁²a₂a₃a₄a₅',
 r'\(20,30,40\)':'20, 30, 40',r'\(40\)':'40',r'\(810\)':'810',
 r'\(20\)':'20',r'\(30\)':'30'
}
abstract=abstract_tex
for a,b in replacements.items(): abstract=abstract.replace(a,b)
abstract=' '.join(abstract.split())
need('\\' not in abstract,'Unconverted original abstract notation')
title=raw['metadata']['title']
slug='fixed-generator-artin-a5'
description=('Classifies fixed-generator positive words in Wajnryb’s Artin A5 quotient: '
             'lengths 20, 30, 40, with four strict Hurwitz classes and three up to conjugation.')
plain=[
 'A positive braid word is built from a fixed list of elementary crossings. This paper classifies all such words representing one specified element of Wajnryb’s quotient of the six-strand braid group.',
 'There are two equivalence conventions. Strict Hurwitz moves rearrange adjacent factors while preserving their product. A broader equivalence also permits conjugating every factor by the same group element. The distinction changes the answer: four strict classes become three classes under the broader convention.'
]
result=[
 'Let a₁,…,a₅ be the five standard generators of B₆, and put c=(a₁a₂a₃a₄)⁵, h=a₅a₄a₃a₂a₁²a₂a₃a₄a₅ and z=(a₁a₂a₃a₄a₅)⁶. Work in G=B₆/⟨⟨ch⁻¹⟩⟩. The full-twist identity gives c²=h²=z in G, with z central.',
 'For every literal positive word in these five fixed generators whose product in G is c², its length is 20, 30 or 40. At length 20 there is one strict Hurwitz class, represented by h². At length 30 there is one, represented by z. At length 40 there are exactly two, represented by (a₁a₂a₃a₄)¹⁰ and (a₂a₃a₄a₅)¹⁰.',
 'The length-20 inputs are exactly the ten distinct cyclic rotations of h² as literal words. Simultaneous conjugation identifies the two length-40 classes, leaving exactly one class at each of the three lengths. This gives the three models in Wajnryb’s question under that broader equivalence.',
 'A strict Hurwitz move replaces adjacent factors (x,y) by (xyx⁻¹,x), or applies its inverse. Intermediate tuples may contain conjugates of generators. The classified inputs remain literal positive words in the five fixed standard generators.'
]
why=[
 'Classical chain relations map the quotient to the genus-two mapping class group with one boundary component. The positive boundary-twist length theorem bounds the word length by 40. Abelianization and signed pure-braid linking constraints then rule out lengths 0 and 10 and restrict the crossing patterns at the other three lengths. These constraints are necessary conditions, rather than complete braid invariants.',
 'At length 20, the crossing pattern reduces all inputs to a finite walk problem. A quotient-compatible free-group action rejects the other candidates; centrality separately proves that the ten surviving rotations are genuine and strictly equivalent. At length 30, full free-word identities along every relevant edge of a finite crossing graph prove equality with the full twist. Equal crossing counts alone would not prove this.',
 'At length 40, the noncrossing strand must be an endpoint. The classical four-chain embedding and positive braid relations give one class at each endpoint. Their generated subgroups have different permutation images, so strict moves keep them distinct; an explicit simultaneous conjugation merges them.'
]
limits=[
 'The theorem concerns these five fixed standard-generator inputs in this specific six-strand quotient. It does not classify arbitrary products of conjugates of generators, arbitrary nonseparating Dehn-twist factorizations, other ranks or other quotients. Allowing conjugates in intermediate Hurwitz moves does not enlarge the input universe.',
 'The quotient geometry, length spectrum, faithful Artin action, positive monoid embedding and chain embedding are classical inputs. Elrifai–Morton report Casson’s general twice-per-labelled-pair assertion; the note supplies an exact certificate in the required six-strand case. Historical priority of the complete fixed-input classification is not certified, and no current worldwide-open-problem claim is made.',
 'The finite proof depends on complete candidate coverage and literal free-word equalities, together with the stated classical theorems. Equal crossing counts alone do not establish braid equality.'
]
background=[
 {'title':'B. Wajnryb, Relations in the mapping class group (2006), Chapter 8',
  'url':'https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf#page=129',
  'note':'The source of the fixed-positive-word quotient question and the stated Perron–Vannier regular-neighborhood chain embedding theorem.'},
 {'title':'D. Auroux, Mapping class group factorizations and symplectic 4-manifolds: some open problems (2006), Chapter 9',
  'url':'https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf#page=138',
  'note':'Distinguishes strict Hurwitz moves from simultaneous global conjugation.'},
 {'title':'R. I. Baykur, N. Monden and J. Van Horn-Morris, Positive factorizations of mapping classes (2017)',
  'url':'https://doi.org/10.2140/agt.2017.17.1527',
  'note':'Theorem A supplies the classical maximum length 40 for a positive nonseparating factorization of the genus-two, one-boundary twist.'},
 {'title':'J. González-Meneses, Basic results on braid groups (2011)',
  'url':'https://www.numdam.org/article/AMBP_2011__18_1_15_0.pdf',
  'note':'The faithful Artin free-group representation and positive braid monoid embedding are established tools used by the proof.'},
 {'title':'M. Matsumoto, A presentation of mapping class groups in terms of Artin groups and geometric monodromy of singularities (2000)',
  'url':'https://doi.org/10.1007/s002080050336',
  'note':'Credits the classical genus-two quotient presentation. The original 1997 institutional manuscript is also cited in the paper.'},
 {'title':'Y. Sato, 2-Spheres of Square −1 and the Geography of Genus-2 Lefschetz Fibrations (2008)',
  'url':'https://www.ms.u-tokyo.ac.jp/journal/pdf/jms150403.pdf',
  'note':'The earlier geography result already gives the length spectrum 20, 30, 40 in the corresponding square−1-section, no-reducible-fibre setting.'},
 {'title':'E. A. Elrifai and H. R. Morton, Algorithms for positive braids (1994)',
  'url':'https://doi.org/10.1093/qmath/45.4.479',
  'note':'Reports Casson’s general crossing assertion on page 496, without a proof or separate Casson reference. The six-strand certificate is additional evidence for that known assertion.'}
]
ai=('AI tools were used extensively in research, proof development, code, literature work and writing. '
    'This is an unrefereed preprint without external human peer review or formal proof-assistant certification; '
    'the named author is responsible for the work.')
collab=('Substantive proof checks, counterexamples and precise comparisons with prior work are welcome. '
        'Authorship and acknowledgments would reflect actual research contributions and mutual agreement. '
        'Citations credit prior work and imply no participation or endorsement.')
status=('Unrefereed preprint, Zenodo version 1.0. Extensive AI assistance; '
        'no external human peer review or formal proof-assistant certification.')
bibnote='Unrefereed preprint; extensive AI assistance; no external human peer review or formal proof-assistant certification'
bib=("@misc{Kriebel2026FixedGeneratorArtinA5,\n"
     "  author = {Kriebel, Alec},\n"
     "  title = {"+title+"},\n"
     "  year = {2026},\n  month = {oct},\n  day = {3},\n  date = {2026-10-03},\n"
     "  version = {1.0},\n  publisher = {Zenodo},\n  doi = {10.5281/zenodo.23124601},\n"
     "  url = {https://zenodo.org/records/23124601},\n  note = {"+bibnote+"},\n"
     "  orcid = {0009-0001-9320-500X}\n}\n")
(O/'CITATION.bib').write_text(bib)
pdf=ready['assets'][1]; archive=ready['assets'][0]
pdfurl=pdf['native_file_object']['links']['self']; zipurl=archive['native_file_object']['links']['self']
root_rel=str(ROOT.relative_to(P))
source_binding={
 'record_id':'23124601','concept_record_id':raw['conceptrecid'],'record_url':raw['links']['self_html'],
 'doi':raw['doi'],'version':'1.0','version_field_present':True,'zenodo_version':'1.0',
 'manuscript_version':None,'manuscript_version_printed':False,
 'version_provenance':'Actual Zenodo metadata declares 1.0; actual PDF/TeX print October 3, 2026 and no version label.',
 'zenodo_publication_date':ready['declared_publication_date'],'manuscript_date':'2026-10-03',
 'record_created_utc':ready['actual_created'],'record_updated_utc':ready['actual_updated'],
 'raw_record_path':'sources/record.raw.json','raw_record_sha256':sha(T/'sources/record.raw.json'),
 'source_receipt_path':'sources/SOURCE_READY.json','source_receipt_sha256':sha(T/'sources/SOURCE_READY.json'),
 'source_receipt_schema':'Original assets/native_file_object/relative paths/lowercase md5 and sha256; metadata_version/declared_publication_date/actual_created/actual_updated; ZIP then PDF.',
 'source_receipt_original':copy.deepcopy(ready),'source_assets_field':'assets','assets':copy.deepcopy(ready['assets']),
 'published_file_objects':copy.deepcopy(raw['files']),'published_asset_count':2,
 'recursive_archive_inventory_path':'sources/archive-custody.json',
 'recursive_archive_inventory_sha256':sha(T/'sources/archive-custody.json'),
 'transport_receipt_path':'sources/transport-receipts.json',
 'transport_receipt_sha256':sha(T/'sources/transport-receipts.json'),
 'transport_receipt_original':copy.deepcopy(transport),'transport_receipt_entry_count':6,
 'asset_root_path':'sources','pdf_sha256':pdf['sha256'],'supplement_sha256':archive['sha256'],
 'source_tex_path':'sources/'+ready['controlling_TeX']['path'],'source_tex_sha256':ready['controlling_TeX']['sha256'],
 'abstract_tex':abstract_tex,'abstract_source':'reviews/editorial/ORIGINAL_ABSTRACT.tex',
 'abstract_source_sha256':sha(O/'ORIGINAL_ABSTRACT.tex'),
 'abstract_normalization':{'whitespace':'fold consecutive whitespace into one ordinary space',
                         'exact_presentational_replacements':replacements,'no_word_or_sentence_omission':True},
 'public_page_reader_pdf_count':1,'archive_outer_regular_file_count':60,
 'archive_regular_member_occurrences':67,'archive_container_count':8,'nested_gzip_stream_count':7,
 'nested_zip_tar_count':0,'archive_embedded_pdf_count':0,'total_distinct_reader_pdf_count':1,
 'reader_intro':'Read the complete 6-page deposited paper in the on-page PDF reader.',
 'prepared_bibtex_path':'reviews/editorial/CITATION.bib','prepared_bibtex_sha256':sha(O/'CITATION.bib'),
 'license_provenance':'Native record metadata.license.id is cc-by-4.0. The actual package README was read and contains no separate license grant; none is invented.',
 'publication_state':'EDITORIAL_CONFIGS_READY_RENDERING_PENDING',
 'review_boundary':'Original custom verdicts and runtime/primary limits remain whole; qualified root scientific adoption is separate from editorial/publication authority.'
}
gates={'rendered':False,'deployed':False,'rendered_public_copy_approved':False,
       'local_http_verified':False,'live_http_verified':False,'browser_verified':False,
       'native_sheet_publication_verified':False,'public_page_published':False,
       'native_sheet_aa_url':None,'root_editorial_clearance_received':False}
pub={'title':title,'slug':slug,'description':description,'abstract':abstract,
     'abstract_heading':'Original abstract','abstract_is_original':True,
     'plain_language':plain,'result':result,'why_it_works':why,'limitations':limits,
     'background':background,'ai_disclosure':ai,'collaboration':collab,
     'follow_up':None,'followup_rationale':'Default none; no substantial independently supported follow-up added.',
     'AA':None,'canonical_url':None,'publication_date':'2026-10-03','version':'1.0',
     'version_field_present':True,'doi':raw['doi'],'author':'Alec Kriebel',
     'orcid':'https://orcid.org/0009-0001-9320-500X','pdf_filename':pdf['path'],'pdf_pages':6,
     'supplement_filename':archive['path'],'supplement_label':'Complete source and verification archive (ZIP)',
     'additional_assets':[],'related_resources':[{'label':'Zenodo original PDF','url':pdfurl},
                                             {'label':'Zenodo original complete ZIP','url':zipurl}],
     'status':status,'license':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/',
     'publication_date_label':'Manuscript and declared publication date',
     'edition_label':'Zenodo version 1.0','citation_edition_label':'Zenodo version 1.0',
     'edition_note':'Manuscript and declared publication date: 3 October 2026. Zenodo records version 1.0; the manuscript prints no version number.',
     'reader_intro':source_binding['reader_intro'],'bibtex_note':bibnote,'prepared_bibtex':bib,
     'source_binding':source_binding,
     'review_metadata':{'prepared_utc':UTC,'completion_percent':100,'scientific_clearance_received':True,
                        'scientific_clearance_status':root['status'],'root_clearance_file':root_rel,
                        'root_clearance_sha256':sha(ROOT),'publication_state':'EDITORIAL_CONFIGS_READY_RENDERING_PENDING',**gates}}
(T/'publication.json').write_text(json.dumps(pub,indent=2,ensure_ascii=False)+'\n')
reviews={}
for family,entry in root['reviews'].items():
    original=load(P/entry['verdict'])
    need(original==entry['whole_original_custom_verdict'],'Root original verdict mismatch')
    reviews[family]={'report':entry['report'],'report_sha256':entry['report_sha256'],
                     'verdict_path':entry['verdict'],'verdict_sha256':entry['verdict_sha256'],
                     'verdict':copy.deepcopy(original),'root_authority_entry':copy.deepcopy(entry)}
promotion={'record_id':'23124601','status':root['status'],'disposition_by':'root','created_utc':UTC,
           'approved_scope':root['scope'],'root_clearance_file':root_rel,'root_clearance_sha256':sha(ROOT),
           'root_clearance_record':copy.deepcopy(root),'publication_sha256':sha(T/'publication.json'),
           'pdf_sha256':pdf['sha256'],'supplement_sha256':archive['sha256'],
           'source_receipt_path':'sources/SOURCE_READY.json','source_receipt_sha256':sha(T/'sources/SOURCE_READY.json'),
           'source_receipt_schema':source_binding['source_receipt_schema'],
           'source_receipt_original':copy.deepcopy(ready),'transport_receipt_original':copy.deepcopy(transport),
           'reviews':reviews,'AA':None,'canonical_url':None,'follow_up':None,**gates}
(T/'promotion.json').write_text(json.dumps(promotion,indent=2,ensure_ascii=False)+'\n')
sections={k:copy.deepcopy(pub[k]) for k in ['title','description','status','edition_label','edition_note',
           'abstract_heading','abstract','plain_language','result','why_it_works','limitations','background',
           'ai_disclosure','collaboration','reader_intro']}
sections['citation']=f"Alec Kriebel (2026). {title}. Zenodo version 1.0, 3 October 2026. https://doi.org/10.5281/zenodo.23124601."
sections['license']='CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/ (Zenodo deposit license).'
write('public-sections.json',sections)
route='/research/'+slug+'/'
requirements={'planned_path':route,'pdf_local_href':route+pdf['path'],'zip_local_href':route+archive['path'],
 'pdf_original_href':pdfurl,'zip_original_href':zipurl,'pdf_iframe_count':1,
 'pdf_iframe_title':title+' — complete 6-page paper','pdf_iframe_uses_unchanged_local_bytes':True,
 'required_links':[{'label':'Open PDF','href':route+pdf['path'],'download':False},
                   {'label':'Download PDF','href':route+pdf['path'],'download':True},
                   {'label':'Download original PDF from Zenodo','href':pdfurl,'download':True},
                   {'label':'Download complete ZIP','href':route+archive['path'],'download':True},
                   {'label':'Download original complete ZIP from Zenodo','href':zipurl,'download':True},
                   {'label':'Download BibTeX','href':route+'citation.bib','download':True}],
 'article_assets':['index.html',pdf['path'],archive['path'],'citation.bib'],'extra_assets':[],
 'layout':'Existing white Arial/Helvetica single-column article',
 'canonical_contract':'Exact self canonical, h1 self link and schema/OG URL from configured origin plus planned_path; canonical_url/AA remain null until separate gates.',
 'navigation_contract':'Named Research navigation must point exactly to /research/.',
 'license_header_and_schema':'CC BY 4.0; https://creativecommons.org/licenses/by/4.0/',
 'prepared_bibtex':bib,'later_exact_visible_text_checks':['Complete original abstract, one indexable paragraph',
 'All public paragraphs and full AI/unrefereed status','3 October 2026 manuscript/declared date',
 'Zenodo version 1.0, distinct from unprinted manuscript version','Exact citation edition',
 'Strict 1/1/2 versus simultaneous-conjugation 1/1/1 counts and exactly ten literal length-20 inputs']}
write('READER_REQUIREMENTS.json',requirements)
parts=['# '+title,'Alec Kriebel · Independent researcher · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)',
       '3 October 2026 · Zenodo version 1.0 · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)',status,pub['edition_note']]
for heading,body in [('Overview',plain),('Original abstract',[abstract]),('The classification',result),
                     ('Why the proof works',why),('Scope and prior work',limits)]:
    parts.append('## '+heading);parts.extend(body)
parts.append('## References and credit')
for ref in background: parts.append('['+ref['title']+']('+ref['url']+'). '+ref['note'])
parts.extend(['## AI and review status',ai,'## Collaboration',collab,'## Read the paper and source',
              pub['reader_intro']])
parts.extend('['+x['label']+']('+x['href']+')' for x in requirements['required_links'])
parts.extend(['## Citation',sections['citation'],'```bibtex\n'+bib.rstrip()+'\n```'])
(O/'PUBLIC_COPY.md').write_text('\n\n'.join(parts)+'\n')
originals=[T/'sources'/n for n in ['SOURCE_READY.json','SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json',
           'record.raw.json','latest.raw.json','versions.raw.json','files.raw.json',
           'transport-receipts.json','archive-custody.json']]
originals += [ROOT,T/'reviews/root/ROOT_REVIEW.md',T/'reviews/root/custody-recheck-20261025.json']
originals += [P/x['verdict'] for x in root['reviews'].values()]
(O/'original-objects').mkdir(exist_ok=True)
copies=[]
for i,path in enumerate(originals):
    name=f'{i+1:02d}-'+path.name
    (O/'original-objects'/name).write_bytes(path.read_bytes())
    copies.append({'original':str(path),'copy':'original-objects/'+name,'bytes':path.stat().st_size,'sha256':sha(path)})
write('ORIGINAL_OBJECT_COPIES.json',{'objects':copies,'custody_copies_not_source_aliases':True})
write('INTAKE_RECORD.json',{'utc':UTC,'record_id':'23124601','scientific_authority_complete_at_intake':True,
 'root_clearance_sha256':sha(ROOT),'root_scientific_status':root['status'],
 'no_invented_pending_phase':True,'original_configs_absent':True,'original_abstract_full':True,
 'read_whole_actual_PDF_pages':6,'full_controlling_TeX_read':True,'all_three_complete_reports_and_verdicts_read':True,
 'full_root_review_and_clearance_read':True,'no_source_program_or_mathematical_control_executed':True,
 'metadata_licence':'cc-by-4.0','README_separate_licence_grant':False,'follow_up':None,**gates})
with (O/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'{UTC} — checkpoint70%: whole six-page paper/TeX, all full reports/custom verdicts, root review/authority and native metadata/receipts read. New configs and complete copy prepared at literal full scope; no source programmes run. Static consistency/changed-input controls and immutable seal remain.\n')
print(json.dumps({'status':'PRIVATE_CONFIGS_AND_COPY_PREPARED','record_id':'23124601',
                  'public_copy_words':len((O/'PUBLIC_COPY.md').read_text().split()),
                  'original_object_copies':len(copies),'publication_sha256':sha(T/'publication.json')},indent=2))
