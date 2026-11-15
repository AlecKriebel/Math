#!/usr/bin/env python3
"""Pure offline editorial custody/copy checks; no project imports, network, subprocesses or writes."""
from pathlib import Path,PurePosixPath
import hashlib,html,json,re,sys
E=Path(__file__).resolve().parent
S=E.parents[1]/'sources'
P=E.parents[3]
N=0;T=0;W=0
EXCLUDE={'MANIFEST.json','SEAL.json'}
def need(ok,why):
 global N
 N+=1
 if not ok:raise RuntimeError(why)
def read(p):
 p=Path(p);need(p.is_file()and not p.is_symlink(),'regular file '+str(p));return p.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(p):return json.loads(read(p))
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b)and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def pin(row):
 b=read(Path(row['path']));need(len(b)==row['bytes']and sha(b)==row['SHA256'],'whole protected original');return b
def walk(x,path):
 global T,W
 if isinstance(x,dict):
  if {'copy','original','bytes','SHA256','whole_literal_object'}<=set(x):
   q=PurePosixPath(x['copy']);need(not q.is_absolute()and '..'not in q.parts,'safe raw copy path');b=read(E/q)
   need(len(b)==x['bytes']and sha(b)==x['SHA256']and b==pin(x['original']),'whole actual raw wrapper '+path)
   need(same(json.loads(b),x['whole_literal_object']),'complete typed/key/list/null/history object '+path);T+=1;W+=1
  for k,v in x.items():walk(v,path+'/'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path+'/'+str(i))
def abstract_surface(tex):
 # Presentation conversion only; ORIGINAL_ABSTRACT.tex remains byte-identical to the TeX slice.
 for a,b in[(r'\R^5','ℝ⁵'),(r'D\times I','D × I'),(r'(-D)\times I','(−D) × I'),(r'\ldots','…')]:tex=tex.replace(a,b)
 tex=tex.replace('$','').replace("Payne's",'Payne’s').replace('I=[0,1]','I = [0,1]')
 return ' '.join(tex.split())
def main(preseal):
 global T
 protected=obj(E/'PROTECTED_INPUTS.json');need(len(protected['source_files'])==81,'whole81 original source files')
 actual=sorted(str(p)for p in S.rglob('*')if p.is_file());need(actual==[r['path']for r in protected['source_files']]and not any(p.is_symlink()for p in S.rglob('*')),'exact original source namespace')
 for r in protected['source_files']+protected['other_files']:pin(r)
 rootpath=P/'verification/root-clearance-23440943-20261115.json';b=read(rootpath);need(len(b)==49928 and sha(b)=='2778005501abc4ae691c0b17e75915edf91917f36c8180021b1a3030c5553da1','exact root clearance')
 c=json.loads(b);ready=obj(S/'SOURCE_READY.json');record=obj(S/'record.response.body');pub=obj(E/'publication.json');pro=obj(E/'promotion.json');protocol=obj(E/'SOURCE_PROTOCOL_BINDINGS.json')
 for name in['publication.json','promotion.json','SOURCE_PROTOCOL_BINDINGS.json']:walk(obj(E/name),name)
 need(same(c['source_ready_whole_original'],ready)and same(pub['source_binding']['whole_original_source_ready'],ready),'whole original SOURCE_READY, not normalized')
 need(same(pub['review_metadata']['root_authority']['whole_literal_object'],c)and same(pro['whole_root_scientific_authority']['whole_literal_object'],c),'entire actual root authority')
 verdicts={f:obj(P/'papers/23440943/reviews'/f/'VERDICT.json')for f in['scope','adversarial']}
 need(same(verdicts,c['whole_original_scientific_verdicts'])and same(verdicts,pub['review_metadata']['whole_original_scientific_verdicts'])and same(verdicts,pro['whole_original_scientific_verdicts']),'entire unique scientific dict objects retain types/order')
 need(same(pub['source_binding'],pro['whole_source_binding']),'whole source binding shared by configs')
 need(verdicts['scope']['root_comparison_gate_at_verdict']=='CLOSED'and verdicts['adversarial']['independence']['root131_gate_at_completion']=='CLOSED','historical CLOSED preserved')
 need(ready['printed_title_date_version_inspected']is False and ready['printed_date']is None and ready['scientific_verdict']is None,'historical acquisition-unread/null preserved')
 need(same(pub['source_binding']['native_assets_in_original_order'],ready['all_native_assets_in_original_order']),'whole native asset original list order')
 api=protocol['native_API_objects_in_original_order'];need(same(api,pub['source_binding']['whole_native_API_objects'])and len(api)==len(ready['whole_native_API_objects'])==4,'complete native API wrapper order')
 for original,wrapped in zip(ready['whole_native_API_objects'],api):need(same(original,wrapped['whole_original_binding'])and wrapped['role']==original['role'],'actual original API role/binding association')
 need(read(E/'inputs/ROOT_REVIEW_20261115.md')==read(Path(c['root_review']['path'])),'whole original root review raw copy')
 need([a['key']for a in record['files']]==['totally-mixed-face-posets-source-and-verification.zip','totally-mixed-face-posets.pdf'],'actual native ZIP then PDF')
 arc=obj(S/'ARCHIVE_CUSTODY.json');need(arc['whole_regular_payload_occurrences']==29 and arc['top_level_archive_count']==1 and arc['nested_archive_count']==0,'whole original29-payload archive extent')
 for a in ready['all_native_assets_in_original_order']:
  original=a['original_api_file_object'];raw=read(Path(a['path']));algorithm,expected=original['checksum'].split(':',1)
  need(len(raw)==original['size']and hashlib.new(algorithm,raw).hexdigest()==expected and sha(raw)==a['SHA256'],'original native size/checksum/SHA')
  need(read(E/'candidate'/original['key'])==raw,'candidate entire unchanged original native asset')
 need(record['metadata']['version']==pub['version']==pub['printed_version']=='1.0.0'and pub['version_field_present']is True and pub['printed_version_field_present']is True,'literal native/printed version')
 need(record['metadata']['publication_date']==pub['publication_date']=='2026-10-17'and pub['native_record_created']==record['created']and pub['native_record_updated']==record['updated'],'publication date separate from created/updated')
 tex=read(Path(ready['controlling_TeX']['extracted_path'])).decode();abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S)[1]
 need(read(E/'ORIGINAL_ABSTRACT.tex')==abstract.encode(),'whole original TeX abstract retained')
 need(abstract_surface(abstract)==pub['abstract'],'full unchanged abstract content after mathematical presentation only')
 mainhtml=read(E/'PUBLIC_MAIN.html').decode();candidate=read(E/'candidate/index.html').decode();copy=read(E/'PUBLIC_COPY.md').decode()
 need(candidate.count(mainhtml)==1 and candidate.count('<main>')==candidate.count('</main>')==1,'whole actual candidate main')
 visible=html.unescape(re.search(r'<h2>Original abstract</h2><p>(.*?)</p>',mainhtml,re.S)[1]);need(visible==pub['abstract']and pub['abstract']in copy,'complete visible and markdown abstract')
 graph=re.findall(r'<script type="application/ld\+json">(.*?)</script>',candidate,re.S);need(len(graph)==1 and same(json.loads(graph[0]),obj(E/'SCHOLARLY_METADATA.json')),'whole embedded scholarly object')
 scholarly=obj(E/'SCHOLARLY_METADATA.json');need(scholarly['abstract']==pub['abstract']and scholarly['datePublished']=='2026-10-17'and scholarly['version']=='1.0.0','accurate complete scholarly abstract/date/version')
 need([x['contentUrl']for x in scholarly['encoding']]==[x['links']['self']for x in record['files']],'scholarly original ZIP/PDF encoding order')
 need('noindex,nofollow,noarchive'in candidate and '<link rel="canonical"'not in candidate,'private candidate gate, no false site canonical')
 for key,value in[('citation_title',pub['title']),('citation_author','Alec Kriebel'),('citation_publication_date','2026/10/17'),('citation_version','1.0.0'),('citation_doi',record['doi'])]:need('<meta name="'+key+'" content="'+html.escape(value,quote=True)+'">'in candidate,'accurate citation '+key)
 need(read(E/'citation.bib')==read(E/'candidate/citation.bib')==pub['prepared_bibtex'].encode(),'entire prepared BibTeX bytes')
 need('version = {1.0.0}'in pub['prepared_bibtex']and 'day = {17}'in pub['prepared_bibtex'],'precise Bib edition/date')
 sections=obj(E/'public-sections.json')
 for key in['plain_language','result','why_it_works','definitions_and_limits','background']:
  need(same(pub[key],sections[key]),'whole authored section array '+key)
  for text in sections[key]:need('<p>'+html.escape(text)+'</p>'in mainhtml and text in copy,'actual full section paragraph '+key)
 content=html.unescape(mainhtml)
 for phrase in['canonical summands','dim F = dim F₁ + dim F₂','nonempty strict chains','No artificial minimum or maximum','full-dimensional lattice 5-polytopes','K ⊔ K','50 vertices and 60 edges','eleven circles','H₀ = ℚ², H₁ = ℚ²²','pure or standard nonpure shellability','no general-position condition','dim(Σ_{i∈J} Fᵢ) ≥ |J|','facets of the summands','Hiatt–Simpson–Wang–Wu v2','(ℂ*)⁸','zero-dimensional complex is shellable']:need(phrase in content,'retained full claim/definition/credit '+phrase)
 for token in['ROOT_REVIEW','CLOSED','SHA256','custody predicates','root scientific decisions']:need(token not in content,'no public internal review narrative '+token)
 need(pub['code_license']is None and pub['license']=='CC BY 4.0'and 'no separate code-specific instrument'in pub['code_license_basis'],'broad authored CC BY, no invented MIT')
 rights=obj(E/'RIGHTS_AND_IDENTITY.json');need(rights['original_license_whole']==read(Path(c['original_license']['path'])).decode()and rights['original_README_whole']==read(Path(c['original_README']['path'])).decode(),'whole original rights/README')
 need(read(E/'inputs/LICENSE.txt')==read(Path(c['original_license']['path']))and read(E/'inputs/README.md')==read(Path(c['original_README']['path'])),'whole raw rights/README copies')
 for field in['follow_up','canonical_url','AA','native_sheet_aa_url']:need(pub[field]is None and pro[field]is None,'literal null follow-up/private publication '+field)
 for field in['rendered_public_copy_approved','production_installation_authorized','ready_to_publish','installed','deployed','live_verified','browser_verified','local_http_verified','native_verified','native_sheet_publication_verified','public_page_published','all203_complete_claimed']:need(pro[field]is False,'future separate publication gate '+field)
 need(pub['review_metadata']['root_full_copy_config_adoption_pending']is True and pro['source_repair']is False and pro['narrowed_replacement']is False,'complete claim only, adoption separate')
 need(set(p.name for p in(E/'candidate').iterdir())=={'index.html',pub['pdf_filename'],pub['supplement_filename'],'citation.bib'},'complete exact four candidate files')
 if not preseal:
  seal=obj(E/'SEAL.json');need(sha(read(E/'MANIFEST.json'))==seal['manifest']['SHA256'],'final entire manifest seal');m=obj(E/'MANIFEST.json')
  paths={p.relative_to(E).as_posix()for p in E.rglob('*')if p.is_file()}-EXCLUDE
  need(paths=={r['relative_path']for r in m['files']}and len(paths)==len(m['files']),'complete own namespace; only root terminal exclusions')
  for row in m['files']:
   p=E/row['relative_path'];b=read(p);need(len(b)==row['bytes']and sha(b)==row['SHA256'],'whole owned payload')
 print(json.dumps({'status':'PASS_PRIVATE_EDITORIAL_CUSTODY','mode':'preseal'if preseal else'sealed','checks':N,'whole_literal_wrappers':W,'strict_whole_typed_objects':T,'source_original_files':81,'candidate_files':4,'original_native_assets':2,'PDF_pages':4,'original_ZIP_payloads':29,'science_or_owner_program_execution':False,'network':False,'subprocess':False,'writes':False},sort_keys=True))
if __name__=='__main__':
 need(sys.argv[1:]in[[],['--preseal']],'bounded pure closure option');main(sys.argv[1:]==['--preseal'])
