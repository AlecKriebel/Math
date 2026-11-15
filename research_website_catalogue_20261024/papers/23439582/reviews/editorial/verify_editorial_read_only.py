#!/usr/bin/env python3
"""Standard-library-only offline closure. Imports no source/authoring/stage code;
no network, subprocess, rendering, native tests, fault modules or writes.
Optional --semantic-controls mutates only tiny in-memory editorial copies.
"""
from pathlib import Path
from hashlib import sha256,md5
from html.parser import HTMLParser
from copy import deepcopy
import json,re,sys,zipfile,ast
E=Path(__file__).resolve().parent;Q=E.parent.parent;P=Q.parent.parent;S=Q/'source-resume-20261115';checks=0
def need(v,s):
 global checks
 if not v:raise RuntimeError(s)
 checks+=1
def load(p):return json.loads(Path(p).read_text())
def h(p):return sha256(Path(p).read_bytes()).hexdigest()
def typed(v):
 if isinstance(v,dict):return('dict',tuple((k,typed(x))for k,x in v.items()))
 if isinstance(v,list):return('list',tuple(typed(x)for x in v))
 return(type(v).__name__,v)
class Page(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.tags=[];self.data=[];self.skip=0;self.script=None;self.scripts=[];self.feed(s)
 def handle_starttag(self,t,a):
  self.tags.append((t,dict(a)))
  if t=='script':self.script=''
  if t in ['head','script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t=='script':self.scripts.append(self.script);self.script=None
  if t in ['head','script','style']:self.skip-=1
 def handle_data(self,d):
  if self.script is not None:self.script+=d
  if not self.skip:self.data.append(d)
def abstract():
 def math(m):
  s=m[1]
  for a,b in [('\\Omega','Ω'),('\\wedge','∧'),('\\Gamma_k','Γₖ'),('\\to','→')]:s=s.replace(a,b)
  return ''.join(s.split())
 s=re.sub(r'\\\((.*?)\\\)',math,(E/'abstract-source.tex').read_text(),flags=re.S);return ' '.join(s.split())
def content(c):
 need(c['abstract']==abstract()and c['abstract_is_original']is True,'entire exact native abstract with typography only')
 r=' '.join(c['result']);w=' '.join(c['why_it_works']);b=' '.join(c['background']);l=' '.join(c['limitations'])
 for t in ['any prime p','any field k of characteristic p','any compact Lie group','not p-nilpotent','normal subgroup of order prime to p','Bousfield–Kan','Completion is taken before looping','left modules','full canonical k-cellularization map','ν:ΓₖR→R','every integer n','No adjoint-orientability','nilpotent component-action','spectral-sequence/tensor-collapse','every A-linear map f:M→A','every M∈Loc_A(k)','Koszul signs','infinite total dimension','K∈thick_A(A)∩thick_A(k)','k∈Loc_A(K)','compactness of k is not assumed']:
  need(t in r,'full original theorem/criterion phrase '+t)
 for t in ['each homology class separately','finite-total-dimensional image','graded left ideal','No bijectivity assumption','does not interchange an infinite cochain dual','by contraposition','Field extension preserves','full canonical map ΓₖR→R']:
  need(t in w,'proof boundary '+t)
 for t in ['does not assert a null morphism in the derived category','No general coefficient-ring or noncompact-group extension','class by class','Historical firstness','present worldwide openness']:
  need(t in l,'precise claim/priority limit '+t)
 for t in ['Question 2.2','page 594','Lemma 6.2','Section 6','Sweedler','Lomp','Dwyer','Greenlees','Iyengar','Briggs','Stevenson','Ishiguro','2007 Proposition 1.3(a)']:
  need(t in b,'exact prior credit '+t)
 need(c['version']==c['printed_version']=='1.0.0'and c['publication_date']=='2026-10-17','actual printed/API version and date')
 need(c['license']==c['code_license']=='CC BY 4.0','actual explicit authored-code CC BY grant')
 need(c['canonical_url']is c['AA']is c['native_sheet_aa_url']is c['follow_up']is None,'null native/followup gates')
 s=c['source_binding'];need(s['current_source_ready_path']==str(S/'SOURCE_READY.json')and s['current_source_root']==str(S),'actual resumed source, not old403 absence')
 need(s['whole_original_source_ready']['completion_percent']==95 and s['historical_ready_completion_percent']==95 and s['final_source_seal_completion_percent']==100,'literal READY95/finalsource100 distinction')
 need(s['native_ZIP_fresh_GET_claimed']is False and s['whole_cache_association']['whole_literal_object']['native_GET_of_cached_ZIP_claimed']is False,'no invented native ZIP GET')
 need(s['old403_history_not_current_manuscript_unavailability']is True,'historical failures not current lack of manuscript')
 need('extensively'in c['ai_disclosure']and 'not human peer review'in c['ai_disclosure']and 'no formal proof-assistant certification'in c['ai_disclosure'],'AI/unrefereed/nonhuman/nonformal')
def optional_controls(c):
 mutations=[lambda x:x['result'].__setitem__(0,x['result'][0].replace('any field k of characteristic p','only the prime field F_p')),lambda x:x['result'].__setitem__(0,x['result'][0].replace('any compact Lie group','only a finite group')),lambda x:x['result'].__setitem__(1,x['result'][1].replace('Completion is taken before looping','Looping is taken before completion')),lambda x:x['result'].__setitem__(2,x['result'][2].replace('full canonical k-cellularization map','component-homology projection')),lambda x:x['result'].__setitem__(2,x['result'][2].replace('every integer n','only positive n')),lambda x:x['limitations'].__setitem__(1,x['limitations'][1].replace('does not assert a null morphism','asserts a null morphism')),lambda x:x['result'].__setitem__(3,x['result'][3].replace('infinite total dimension','finite dimension in every degree')),lambda x:x['result'].__setitem__(4,x['result'][4].replace('compactness of k is not assumed','compactness of k is assumed')),lambda x:x['source_binding']['whole_original_source_ready'].update(completion_percent=100),lambda x:x['source_binding'].update(native_ZIP_fresh_GET_claimed=True),lambda x:x.update(code_license='MIT'),lambda x:x.update(canonical_url=x['proposed_canonical_url'])]
 rejected=0
 for f in mutations:
  bad=deepcopy(c);f(bad)
  try:content(bad)
  except RuntimeError:rejected+=1
 need(rejected==len(mutations),'all twelve tiny in-memory editorial losses rejected')
 return{'distinct_editorial_fault_shapes_rejected':rejected,'source_or_science_or_native_execution':False}

pub=load(Q/'publication.json');prom=load(Q/'promotion.json');proto=load(E/'SOURCE_PROTOCOL_BINDINGS.json');ready=load(S/'SOURCE_READY.json');rootpath=P/'verification/root-clearance-23439582-20261115.json';auth=load(rootpath)
need(h(rootpath)=='36df4b069964affe1604451c30844c8464aae90b5fe9597d76f7e492e5a6aaf4','root full science authority SHA256');need(h(S/'SOURCE_READY.json')=='0795e0631373b473f9d50270532ed8f326f68ba793d4f08c1654ea1a4556a244','exact current resumed SOURCE_READY SHA256')
for row in load(E/'PROTECTED_INPUTS.json')['files']:
 p=Path(row['absolute_path']);need(p.stat().st_size==row['bytes']and h(p)==row['sha256'],'225 preexisting/source/cache bytes '+str(p))
def bound(x):
 p=Path(x['path']);need(p.stat().st_size==x['bytes']and h(p)==x['SHA256'],'whole original bytes '+str(p));need(typed(load(p))==typed(x['whole_literal_object']),'whole original type/key/list/header/null order '+str(p))
for key in ['current_SOURCE_READY','root_authority','actual_transport_aggregate','cache_association','whole_archive_custody','native_schema_types','printed_identity']:bound(proto[key])
for key in ['source_terminal_objects','older_incomplete_history_objects','native_API_objects','six_actual_new_transport_objects','three_actual_old_403_transport_objects','whole_two_original_scientific_custom_verdicts','scientific_review_seals']:
 for x in proto[key]:bound(x)
for key in ['actual_license_and_requirements','whole_bound_scientific_derivations','source_reports_preserved']:
 for x in proto[key]:need(Path(x['path']).read_text()==x['whole_literal_text']and h(x['path'])==x['SHA256'],'complete original literal document '+x['path'])
for x in proto['raw_byte_copies']:need(Path(x['original_path']).read_bytes()==(E/x['copy_relative_to_editorial']).read_bytes(),'all original raw byte copies')
need(len(proto['native_API_objects'])==4 and len(proto['six_actual_new_transport_objects'])==6 and len(proto['three_actual_old_403_transport_objects'])==3 and len(proto['whole_two_original_scientific_custom_verdicts'])==2,'actual4API/6new/3old/2science cardinalities')
need(proto['literal_ready_completion']==95 and proto['literal_final_source_completion']==100,'unchanged source progress history')
cache=proto['cache_association']['whole_literal_object'];zipasset,pdf=ready['all_native_assets_in_original_order'];need(Path(cache['candidate_original_path']).read_bytes()==Path(zipasset['path']).read_bytes(),'existing cache equals authenticated native ZIP');need(md5(Path(zipasset['path']).read_bytes()).hexdigest()==zipasset['MD5']and cache['MD5']==zipasset['MD5']and cache['bytes']==zipasset['bytes'],'native size/MD5 cache association')
need(not any(x['whole_literal_object']['requested_url']==zipasset['original_api_file_object']['links']['self']for x in proto['six_actual_new_transport_objects']),'no fresh ZIP HTTP receipt fabricated')
for owner in [pub['source_binding'],prom]:
 need(typed(owner['whole_original_source_ready'])==typed(ready),'whole resumed source READY not flattened')
 for ownkey,key in [('whole_current_source_terminal_objects','source_terminal_objects'),('whole_older_incomplete_history_objects','older_incomplete_history_objects'),('whole_original_native_API_objects','native_API_objects'),('whole_current_transport_aggregate','actual_transport_aggregate'),('whole_six_actual_new_transport_objects','six_actual_new_transport_objects'),('whole_three_historical_403_transport_objects','three_actual_old_403_transport_objects'),('whole_cache_association','cache_association')]:need(typed(owner[ownkey])==typed(proto[key]),'whole exact mixed source interface '+key)
for owner in [pub['review_metadata'],prom]:
 need(typed(owner['whole_root_scientific_clearance_record'])==typed(auth),'whole exact root record');need(typed(owner['whole_original_two_scientific_custom_verdicts'])==typed(proto['whole_two_original_scientific_custom_verdicts']),'two literal scientific verdicts not generic PASS');need(typed(owner['whole_bound_scientific_derivations'])==typed(proto['whole_bound_scientific_derivations']),'whole bound final derivations')
need(pub['source_binding']['source_protocol_binding_sha256']==h(E/'SOURCE_PROTOCOL_BINDINGS.json'),'exact source protocol pin');need(prom['publication_sha256']==h(Q/'publication.json'),'publication config pin')
for key in ['source_repair','narrowed_replacement','human_peer_review','formal_certification','private_batch_integration_authorized','rendered','deployed','rendered_public_copy_approved','rendered_copy_verified','local_http_verified','live_http_verified','live_verified','browser_verified','native_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received','production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified','all203_complete_claimed']:need(prom[key]is False,'false private/public/review gate '+key)
for key in ['canonical_url','AA','native_sheet_aa_url','follow_up']:need(prom[key]is None,'null native/public gate '+key)
content(pub);sections=load(E/'public-sections.json');copy=(E/'PUBLIC_COPY.md').read_text();page=Page((E/'candidate/index.html').read_text());visible=''.join(page.data)
need(len(page.scripts)==1,'single nonexecuting scholarly JSON graph');scholar=json.loads(page.scripts[0]);need(scholar['@type']=='ScholarlyArticle'and scholar['abstract']==pub['abstract']and scholar['name']==pub['title']and scholar['description']==pub['description'],'full exact scholarly title and original abstract');need(scholar['datePublished']==pub['publication_date']and scholar['version']==pub['version']and scholar['identifier']['value']==pub['doi']and scholar['license']==pub['license_url'],'exact scholarly native edition/date/DOI/license');need([x['contentUrl']for x in scholar['encoding']]==[x['original_api_file_object']['links']['self']for x in ready['all_native_assets_in_original_order']],'original ZIP/PDF order in scholarly encoding')
for key,paras in sections['sections'].items():
 for p in paras:need(p in copy and p in visible,'whole visible public paragraph '+key)
for p in [pub['abstract'],pub['edition_note'],pub['reader_intro'],pub['rights_notice']]:need(p in copy and p in visible,'whole visible abstract/edition/reader/rights')
need(any(t=='meta'and a.get('name')=='robots'and a.get('content')=='noindex,nofollow'for t,a in page.tags),'private noindex/nofollow');need(not any(t=='link'and a.get('rel')=='canonical'for t,a in page.tags),'no assigned candidate canonical')
frames=[a for t,a in page.tags if t=='iframe'];need(len(frames)==1 and frames[0]['src'].split('#')[0]=='assets/'+pdf['original_api_file_object']['key']and 'four-page'in frames[0]['title'],'full titled native4page reader')
links=[a for t,a in page.tags if t=='a'];need(any(a.get('href')=='assets/'+pdf['original_api_file_object']['key']and 'download'in a for a in links),'actual full PDF download');need(any(a.get('href')=='assets/'+zipasset['original_api_file_object']['key']and 'download'in a for a in links),'actual complete ZIP download');need(any(a.get('href')=='assets/citation.bib'and 'download'in a for a in links),'actual BibTeX download')
for a in ready['all_native_assets_in_original_order']:need((E/'candidate/assets'/a['original_api_file_object']['key']).read_bytes()==Path(a['path']).read_bytes(),'complete unchanged native asset')
need((E/'candidate/assets/citation.bib').read_text()==(E/'citation.bib').read_text()==pub['prepared_bibtex'],'exact accurate citation copies');need('day = {17}'in pub['prepared_bibtex']and 'version = {1.0.0}'in pub['prepared_bibtex']and pub['doi']in pub['prepared_bibtex'],'native citation date/version/DOI')
with zipfile.ZipFile(E/'candidate/assets'/zipasset['original_api_file_object']['key'])as z:
 need(len(z.infolist())==20 and z.testzip()is None,'full20-member native archive CRC')
 for x in proto['all20_original_member_checks']:need(z.read(x['original_member_name'])==Path(x['path']).read_bytes()and sha256(z.read(x['original_member_name'])).hexdigest()==x['SHA256'],'all20 whole extracted native payloads '+x['original_member_name'])
need(Path(ready['all_embedded_PDFs'][0]['path']).read_bytes()==(E/'candidate/assets'/pdf['original_api_file_object']['key']).read_bytes(),'embedded and standalone native PDF identical')
for term in ['2026-11-15','2026-11-14','SOURCE_READY','SEAL.json','root-clearance','225 preexisting','source-resume-20261115','403','SHA256','sha256']:need(term not in copy and term not in visible,'no internal history/audit leak '+term)
for n in ['PREPARE_EDITORIAL.py','ASSEMBLE_SOURCE_PROTOCOL.py']:ast.parse((E/n).read_text());need(True,'new authoring syntax only '+n)
controls=optional_controls(pub)if'--semantic-controls'in sys.argv else None
sealed=(E/'SEAL.json').exists()
if sealed:
 seal=load(E/'SEAL.json');need(h(E/'MANIFEST.json')==seal['manifest_sha256'],'own final manifest seal');m=load(E/'MANIFEST.json')
 for row in m['files']:
  p=Path(row['absolute_path']);need(p.stat().st_size==row['bytes']and h(p)==row['sha256'],'owned editorial bytes '+str(p))
 need({str(p)for p in E.rglob('*')if p.is_file()}|{str(Q/'publication.json'),str(Q/'promotion.json')}=={x['absolute_path']for x in m['files']}|{str(E/'MANIFEST.json'),str(E/'SEAL.json')},'exact own/editorial config namespace')
else:need('--unsealed'in sys.argv,'final seal required')
print(json.dumps({'literal_status':'PASS_PRIVATE_FULL_CELLULARIZATION_EDITORIAL_AND_RESUMED_NATIVE_CUSTODY','checks':checks,'preexisting_inputs_unchanged':225,'actual_whole_scientific_custom_verdicts':2,'actual_native_API_bodies':4,'actual_new_transports':6,'preserved_old403_history':3,'complete_native_ZIP_members':20,'embedded_PDF_identical':True,'literal_READY95_finalsource100_preserved':True,'invented_fresh_ZIP_GET':False,'optional_tiny_semantic_controls':controls,'own_final_seal_checked':sealed,'network_subprocess_source_science_legacy_or_file_writes':False,'publication_or_native_AA_authority':False},indent=2))
