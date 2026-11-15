#!/usr/bin/env python3
"""Pure offline custody and static-copy consistency; no local/native imports or reruns."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,zipfile,html,re
E=Path(__file__).resolve().parent;Q=E.parent.parent;P=Q.parent.parent;S=Q/'sources';checks=0
def need(v,m):
 global checks
 checks+=1
 if not v:raise RuntimeError(m)
def obj(f):return json.loads(f.read_bytes())
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b)and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def match(f,z):
 need(f.is_file()and not f.is_symlink(),'regular '+str(f));need(f.stat().st_size==z['bytes'],'bytes '+str(f));need(sha(f)==z['SHA256'],'SHA256 '+str(f))
class Page(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.links=[];self.frames=[];self.meta={};self.canonical=[];self.main=False;self.maintext=[];self.jsonld=False;self.jsontext=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='main':self.main=True
  if tag=='a':self.links.append(a)
  if tag=='iframe':self.frames.append(a)
  if tag=='meta':self.meta[a.get('name')]=a.get('content')
  if tag=='link'and a.get('rel')=='canonical':self.canonical.append(a)
  if tag=='script'and a.get('type')=='application/ld+json':self.jsonld=True
 def handle_endtag(self,tag):
  if tag=='main':self.main=False
  if tag=='script':self.jsonld=False
 def handle_data(self,data):
  if self.main:self.maintext.append(data)
  if self.jsonld:self.jsontext.append(data)
def abstract_from_tex():
 text=(S/'published-source/main.tex').read_text().split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0].strip()
 def mathpart(m):
  t=m.group(1)
  for a,b in [('\\alpha','α'),('\\beta','β'),('\\ne','≠'),('_1','₁'),('_2','₂'),('_3','₃'),('_4','₄'),('^2','²'),('-','−')]:t=t.replace(a,b)
  return t
 return re.sub(r'\\\((.*?)\\\)',mathpart,text,flags=re.S)
def canon(t):return ''.join(t.replace('’',"'").split())
def main():
 manifest=obj(E/'MANIFEST.json');actual={f.relative_to(E).as_posix()for f in E.rglob('*')if f.is_file()}-{'MANIFEST.json','SEAL.json'}
 need(actual=={z['path']for z in manifest['owned_files']},'closed owned set')
 for z in manifest['owned_files']:match(E/z['path'],z)
 if(E/'SEAL.json').exists():
  seal=obj(E/'SEAL.json');need(sha(E/'MANIFEST.json')==seal['MANIFEST_SHA256'],'manifestseal')
  for key,name in [('REPORT_SHA256','REPORT.md'),('VERDICT_SHA256','VERDICT.json'),('PUBLIC_COPY_SHA256','PUBLIC_COPY.md'),('publication_json_SHA256','configs/publication.json'),('promotion_json_SHA256','configs/promotion.json'),('READ_ONLY_VERIFIER_SHA256','verify_editorial_read_only.py')]:need(sha(E/name)==seal[key],key)
 protected=obj(E/'PROTECTED_INPUTS.json')['preexisting_files']
 for z in protected:match(Path(z['path']),z)
 source_pre={z['path']for z in protected if str(S)+'/'in z['path']};need(source_pre=={str(f)for f in S.rglob('*')if f.is_file()},'exact frozen source set')
 root=P/'verification/root-clearance-23423736-20261115.json';need(sha(root)=='e6b55b150dae5c3860267476e7f34b7971a88a41c13ee338c6f9396acf5e3a26','rootauthoritypin');authority=obj(root)
 need((E/'inputs/root-clearance.json').read_bytes()==root.read_bytes(),'wholeauthoritycopy');need((E/'inputs/ROOT_REVIEW.md').read_bytes()==(Q/'reviews/root/ROOT_REVIEW_20261115.md').read_bytes(),'wholerootreviewcopy')
 ready=obj(S/'SOURCE_READY.json');need(same(ready,authority['whole_original_SOURCE_READY']),'READY wholeliteralrootmatch')
 need(ready['completion_percent_at_preseal']==95 and obj(S/'SOURCE_READY_SEAL.json')['completion_percent']==100,'historical95andfinal100')
 protocol=obj(E/'SOURCE_PROTOCOL_BINDINGS.json');need(same(protocol['whole_original_SOURCE_READY']['whole_literal_object'],ready),'wholeREADYbinding')
 for z in protocol['byte_identical_owned_native_copies']:
  need(Path(z['source']).read_bytes()==Path(z['copy']).read_bytes(),'literalnativebytecopy');match(Path(z['copy']),z)
 apis=protocol['whole_original_native_API_objects'];need(len(apis)==4,'actual4APIobjects')
 for z in apis:match(Path(z['path']),z);need(same(obj(Path(z['path'])),z['whole_literal_object']),'wholeAPIschema/order')
 aggregate=obj(S/'ALL_TRANSPORT_RECEIPTS.json');receipts=protocol['whole_original_seven_transport_objects_in_native_aggregate_order'];need(len(receipts)==len(aggregate['receipts'])==7,'actual7transports')
 for z,r in zip(receipts,aggregate['receipts']):
  match(Path(z['path']),z);need(same(z['whole_literal_object'],r),'whole receiptorder/objects');need(same(obj(Path(z['path'])),r),'actualreceiptfile')
  b=Path(r['body_path']).read_bytes();need(len(b)==r['body_bytes']and hashlib.sha256(b).hexdigest()==r['body_SHA256']and hashlib.md5(b).hexdigest()==r['body_MD5'],'wholetransportresponsebody')
 need([r['HTTP_status']for r in aggregate['receipts']]==ready['HTTP_status_sequence'],'actualHTTPstatushistory')
 dist=ready['native_schema_distinctions'];need(type(dist['record_swh']['original_value'])is dict and not dist['record_swh']['original_value'],'recordemptydict');need(dist['version_hit_swh_fields'][0]['original_value']is None,'versionnull');need(type(dist['files_order']['original_value'])is list and not dist['files_order']['original_value']and dist['files_default_preview']['original_value']is None,'emptylistandnull')
 need(ready['target_PDF_pages_rendered']is False and ready['TeX_preamble_or_mathematical_body_read']is False,'unreadhistoricalflagsnotrewritten')
 need([a['original_api_file_object']['key']for a in ready['all_native_assets_in_original_order']]==['paper.pdf','source-and-verification.zip'],'nativeassetorder')
 for a in ready['all_native_assets_in_original_order']:
  b=Path(a['path']).read_bytes();need(hashlib.md5(b).hexdigest()==a['original_api_file_object']['checksum'].split(':')[1]and hashlib.sha256(b).hexdigest()==a['SHA256'],'nativeassetchecksums')
 archive=obj(S/'ARCHIVE_CUSTODY.json');need(len(archive['containers'])==4 and len(archive['all_safe_regular_occurrences'])==195,'whole4containers195payloads')
 occ={(x['container_id'],x['ordinal_zero_based']):x for x in archive['all_safe_regular_occurrences']};seen=0
 for c in archive['containers']:
  f=Path(c['path']);match(f,c)
  with zipfile.ZipFile(f)as z:
   need(z.testzip()is None,'wholecontainerCRC');need(len(z.infolist())==len(c['whole_original_central_directory']),'centraldirectorywholecount')
   for i,(zi,rec)in enumerate(zip(z.infolist(),c['whole_original_central_directory'])):
    actualmeta={'ordinal_zero_based':i,'filename':zi.filename,'original_filename':zi.orig_filename,'is_directory':zi.is_dir(),'bytes':zi.file_size,'compressed_bytes':zi.compress_size,'CRC32':f'{zi.CRC:08x}','flags':zi.flag_bits,'compression':zi.compress_type,'native_date_time':list(zi.date_time),'external_attr':zi.external_attr,'internal_attr':zi.internal_attr,'create_system':zi.create_system,'create_version':zi.create_version,'extract_version':zi.extract_version,'header_offset':zi.header_offset,'extra_hex':zi.extra.hex(),'comment_hex':zi.comment.hex()}
    need(same(actualmeta,rec),'wholecentralmetadata/order')
    if not zi.is_dir():
     a=occ[(c['container_id'],i)];b=z.read(zi);need(len(b)==a['bytes']and hashlib.sha256(b).hexdigest()==a['SHA256']and b==Path(a['extracted_path']).read_bytes(),'wholeexpandedmemberbytes');seen+=1
 need(seen==195,'allpayloadoccurrencesvisited')
 publication=obj(E/'configs/publication.json');promotion=obj(E/'configs/promotion.json');sections=obj(E/'public-sections.json')
 need(same(publication['source_binding'],protocol),'fullsourcebindingnotflattened');need(same(publication['review_metadata']['whole_root_scientific_clearance_record'],authority),'wholeauthorityinconfig')
 need(same(promotion['whole_root_scientific_clearance_record'],authority),'wholeauthorityinpromotion');need(same(promotion['whole_original_SOURCE_READY'],ready),'wholeREADYpromotion')
 review=publication['review_metadata'];need(review['actual_scientific_review_cardinality']==promotion['actual_scientific_review_cardinality']==2,'exacttwoactualscienceverdicts')
 for i,(lane,sealname)in enumerate([('analytic','SEAL.json'),('adversarial','FINAL_SEAL.json')]):
  v=obj(Q/'reviews'/lane/'VERDICT.json');se=obj(Q/'reviews'/lane/sealname)
  for config in [review,promotion]:
   need(same(config['whole_original_custom_scientific_verdicts'][i]['whole_literal_object'],v),'wholeliteralverdictnotgenericPASS');need(same(config['whole_original_scientific_review_seals'][i]['whole_literal_object'],se),'wholeliteralseal')
 need(publication['abstract']==sections['abstract']and canon(publication['abstract'])==canon(abstract_from_tex()),'fulloriginalabstractexactwordsandmath')
 for k in ['title','description','plain_language','result','why_it_works','limitations','background','collaboration','ai_disclosure','reader_intro']:need(same(publication[k],sections[k]),'uniqueprosecopy '+k)
 need(publication['publication_date']=='2026-10-16'and publication['version']==publication['printed_version']=='1.0','nativeprintededitiondate')
 need(publication['native_record_created']==ready['created']and publication['native_record_updated']==ready['updated'],'creationseparate')
 need(publication['license']=='CC BY 4.0'and publication['code_license']is None and publication['authored_package_license']=='CC BY 4.0','actualrightsnoMITdefault')
 for config in [publication,promotion]:
  need(config['follow_up']is None and all(config[k]is None for k in ['canonical_url','AA','native_sheet_aa_url']),'nullfollowupandcanonicalgates')
 need(promotion['publication_sha256']==sha(E/'configs/publication.json'),'publicationpromotionhash')
 flags=['rendered','deployed','rendered_public_copy_approved','rendered_copy_verified','local_http_verified','live_http_verified','live_verified','browser_verified','native_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received','production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified']
 need(all(promotion[k]is False for k in flags)and promotion['paper_level_configs_written']is False,'allproductionflagsfalse')
 h=(E/'candidate/index.html').read_text();page=Page();page.feed(h);maintext=' '.join(page.maintext)
 need(not page.canonical and page.meta['robots']=='noindex,nofollow','privateHTMLgate')
 for key in ['abstract','plain_language','result','why_it_works','limitations','background','reader_intro','collaboration','ai_disclosure','rights_notice','citation']:
  vals=sections[key]if isinstance(sections[key],list)else[sections[key]]
  for v in vals:need(v in maintext and html.escape(v)in h,'entireHTMLparagraph '+key);need(v in(E/'PUBLIC_COPY.md').read_text(),'entirePUBLICCOPYparagraph '+key)
 need(len(page.frames)==1 and page.frames[0]['src']=='assets/paper.pdf'and'four-page'in page.frames[0]['title'],'fullaccessibleiframe')
 for name in ['paper.pdf','source-and-verification.zip','citation.bib']:need(any(a.get('href')=='assets/'+name and a.get('download')==name for a in page.links),'realdownload '+name)
 for a in page.links:
  if a.get('href','').startswith('assets/'):need((E/'candidate'/a['href']).is_file(),'actualassetlinktarget')
 for name in ['paper.pdf','source-and-verification.zip']:need((E/'candidate/assets'/name).read_bytes()==(S/'assets'/name).read_bytes(),'unchangedfullasset '+name)
 need((E/'candidate/assets/citation.bib').read_bytes()==(E/'citation.bib').read_bytes(),'wholeBibasset')
 need('10.5281/zenodo.23423736'in(E/'citation.bib').read_text()and'day = {16}'in(E/'citation.bib').read_text()and'version = {1.0}'in(E/'citation.bib').read_text(),'Bibidentitydateversion')
 structured=json.loads(''.join(page.jsontext));need(structured['abstract']==sections['abstract']and structured['datePublished']=='2026-10-16'and structured['version']=='1.0','scholarlyfullabstractdate')
 need(page.meta['citation_doi']=='10.5281/zenodo.23423736'and page.meta['citation_publication_date']=='2026/10/16','citationmetadata')
 need('90269-2'not in maintext and '90269-T'in h,'actualAVDOI')
 for forbidden in ['20261115','SOURCE_READY','SHA256','verification/','reviews/','435 preexisting','independent audit passed']:need(forbidden not in maintext,'privateauditnotpublic '+forbidden)
 need(len((E/'actual-published.txt').read_text().split('\f'))-1==4 and'Historical priority remains unresolved'in maintext,'completePDFsearchabilityandpriorityscope')
 print(json.dumps({'status':'PASS_PURE_OFFLINE_CUSTODY_AND_STATIC_COPY_CONSISTENCY','checks':checks,'owned_payloads':len(manifest['owned_files']),'protected_preexisting_inputs_unchanged':len(protected),'whole_recursive_archive_payloads':seen,'actual_scientific_verdicts_retained_whole':2,'actual_transports_retained_whole':7,'scientific_native_or_authoring_code_rerun':False,'optional_semantic_controls_run':False,'network_used':False,'writes_performed':False},indent=2))
if __name__=='__main__':main()
