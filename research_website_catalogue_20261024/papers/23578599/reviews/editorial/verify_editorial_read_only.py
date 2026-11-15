#!/usr/bin/env python3
"""Import-safe, offline, read-only editorial custody/consistency verifier. No source imports or execution."""
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,re,copy,zipfile,zlib,sys
P=Path(__file__).resolve().parent
S=P.parent.parent/'sources'
EX={'MANIFEST.json','CLOSURE_PRESEAL.json','SEAL.json'}
FLAGS=['rendered','deployed','rendered_public_copy_approved','rendered_copy_verified','local_http_verified','live_http_verified','live_verified','browser_verified','native_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received','production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified','private_batch_integration_authorized','all203_complete_claimed']
def sha(b):return hashlib.sha256(b).hexdigest()
def js(q):return json.loads(Path(q).read_text())
def abstract_plain(t):
 def sub(m):
  s=m.group(1)
  for a,b in [(r'\C','ℂ'),('^2','²'),(r'\ord','ord'),(r'\geq','≥'),(r'\leq','≤'),(r'\lceil','⌈'),(r'\rceil','⌉'),(r'\{','{'),(r'\}','}'),('\\ ',' ')]:s=s.replace(a,b)
  return re.sub(r'([≥≤⌈])\s+',r'\1',s)
 return' '.join(re.sub(r'\\\((.*?)\\\)',sub,t,flags=re.S).replace("Fern\\'andez",'Fernández').replace('~',' ').split())
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.meta={};self.links=[];self.iframes=[];self.section=None;self.paragraph=False;self.parts={};self.jsons=[];self.script=False;self.data='';self.visible=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta':self.meta[a.get('name',a.get('charset',''))]=a.get('content','')
  if tag in['a','link']:self.links.append((tag,a))
  if tag=='iframe':self.iframes.append(a)
  if tag=='section':self.section=a.get('id');self.parts.setdefault(self.section,[])
  if tag=='p':self.paragraph=True
  if tag=='script'and a.get('type')=='application/ld+json':self.script=True;self.data=''
 def handle_endtag(self,tag):
  if tag=='p':self.paragraph=False
  if tag=='section':self.section=None
  if tag=='script'and self.script:self.jsons.append(json.loads(self.data));self.script=False
 def handle_data(self,data):
  if self.script:self.data+=data
  else:
   self.visible.append(data)
   if self.section and self.paragraph:self.parts[self.section].append(data)
def publication_facts(pub,prom,sec,abstract):
 try:
  text=' '.join(x for a in sec['sections'].values()for x in a)
  return all([pub['version']=='1.0.0',pub['publication_date']=='2026-10-22',pub['native_record_created']=='2026-10-22T21:24:54.317246+00:00',pub['native_record_updated']=='2026-10-22T21:24:54.772321+00:00',pub['doi']=='10.5281/zenodo.23578599',pub['license']=='CC BY 4.0',pub['code_license']=='MIT',pub['status']=='Unrefereed preprint',pub['abstract']==sec['abstract']==abstract,pub['canonical_url']is None,pub['AA']is None,pub['native_sheet_aa_url']is None,prom['canonical_url']is None,prom['AA']is None,prom['native_sheet_aa_url']is None,pub['follow_up']is None,prom['follow_up']is None,pub['publication_authority']is False,prom['publication_authority']is False,all(pub[k]is False and prom[k]is False for k in FLAGS),prom['actual_scientific_review_cardinality']==2,pub['scientific_review_cardinality']==2,all(pub[k]==sec['sections'][k]for k in ['plain_language','result','why_it_works','limitations','background']),pub['collaboration']==sec['sections']['collaboration'][0],pub['ai_disclosure']==sec['sections']['status'][0],pub['normalizations']==sec['normalizations'],len(sec['normalizations'])==5,'For every n≥3 and 2≤k<n'in text,'every coefficient tuple'in text,'aₖ≠0'in text,'For every positive j and q'in text,'Neither threshold pair is (q,jq) for any positive integers j,q'in text,'exactly when k divides n'in text,'It is not equality of nonreduced coefficient schemes'in text,'other primitive toric divisors'in text,'No unique author-intended correction'in text,'Historical firstness, continuous openness'in text,'Authorship would be discussed in relation to actual contributions'in text,'not independent human peer review'in text,'formal proof-assistant certification'in text])
 except(KeyError,TypeError,IndexError):return False

def verify(preseal=False):
 checks=0;fail=[]
 def ck(v,n):
  nonlocal checks
  checks+=1
  if not v:fail.append(n)
 def bind(e,path=None):
  q=Path(path or e['path']);b=q.read_bytes();ck(len(b)==e['bytes'],'bytes '+str(q));ck(sha(b)==e['SHA256'],'SHA256 '+str(q));return b
 prot=js(P/'PROTECTED_INPUTS.json')
 for e in prot['files']:bind(e)
 ck(len(prot['files'])==183,'whole protected input count')
 manifest=js(P/'MANIFEST.json')
 ck({str(q.relative_to(P))for q in P.rglob('*')if q.is_file()and str(q.relative_to(P))not in EX}=={e['path']for e in manifest['files']},'whole owned footprint')
 for e in manifest['files']:bind(e,P/e['path'])
 for e in js(P/'RAW_BYTE_COPIES.json')['files']:ck(bind(e['original'])==(P/e['copy_path']).read_bytes(),'whole exact raw-native copy')
 protocol=js(P/'SOURCE_PROTOCOL_BINDINGS.json')
 for key in ['whole_original_SOURCE_READY','whole_original_transport_aggregate','whole_archive_custody','whole_root_clearance']:
  e=protocol[key];ck(js(e['path'])==e['whole_literal_object'],'whole original typed object '+key);bind(e)
 for key in ['whole_source_terminal_objects','whole_original_native_API_objects','whole_current_two_scientific_verdicts','whole_current_scientific_seals']:
  for e in protocol[key]:ck(js(e['path'])==e['whole_literal_object'],'whole literal '+key);bind(e)
 ready=protocol['whole_original_SOURCE_READY']['whole_literal_object'];authority=protocol['whole_root_clearance']['whole_literal_object']
 ck(sha((S/'SOURCE_READY.json').read_bytes())=='c38e49d39bef6213a4703ee624be84eb110f1479a9c7b7e27b331bc39d417df4','READY exact anchor')
 ck(protocol['whole_root_clearance']['SHA256']=='d851e27fd7d81f74b55dc76d58969d46de918f9874f2ca8f2667565d9ae65130','root authority exact anchor')
 vs=protocol['whole_current_two_scientific_verdicts'];ck(len(vs)==2 and vs[0]['whole_literal_object']==authority['whole_independent_scope_VERDICT']and vs[1]['whole_literal_object']==authority['whole_independent_analytic_CUSTOM_VERDICT'],'both literal custom verdicts retained without PASS projection')
 tr=protocol['whole_original_transport_aggregate']['whole_literal_object'];ck(type(tr)is dict and len(tr['receipts'])==7 and[x['HTTP_status']for x in tr['receipts']]==[200,301,200,200,200,200,200],'whole seven native transports/order/301 preserved')
 for x in tr['receipts']:
  b=Path(x['body_path']).read_bytes();ck(len(b)==x['body_bytes']and sha(b)==x['body_SHA256'],'whole transport body');ck(type(x['response_headers_in_received_order'])is list,'ordered headers retain duplicates')
 objs={e['role']:e['whole_literal_object']for e in protocol['whole_original_native_API_objects']}
 ck(objs['record']['swh']=={}and objs['latest']['swh']=={}and objs['versions_page001']['hits']['hits'][0]['swh']is None and objs['files']['order']==[]and objs['files']['default_preview']is None,'native empty/null distinction')
 ck(ready['completion_percent_at_preseal']==95 and ready['printed_title_date_version_inspected']is False and ready['publication_authority']is False and ready['source_programmes_executed']==[],'historical source95/unread/authority flags unchanged')
 ck([x['original_api_file_object']['key']for x in ready['all_native_assets_in_original_order']]==['free-chain-nash-intersections.pdf','free-chain-nash-intersections-source-and-verification.zip'],'native PDF then ZIP order')
 for x in ready['all_native_assets_in_original_order']:
  b=bind(x);ck('md5:'+hashlib.md5(b).hexdigest()==x['original_api_file_object']['checksum'],'native asset MD5');ck(b==(P/'candidate/assets'/x['original_api_file_object']['key']).read_bytes(),'candidate unchanged complete original asset')
 ac=protocol['whole_archive_custody']['whole_literal_object'];c=ac['containers'][0];total=0
 with zipfile.ZipFile(c['path'])as z:
  ck(len(z.infolist())==21 and z.testzip()is None,'complete21-payload ZIP CRC')
  for zi,e in zip(z.infolist(),ac['all_safe_regular_occurrences']):
   b=z.read(zi);total+=len(b);ck(zi.filename==e['original_member_name']and len(b)==e['bytes']and sha(b)==e['SHA256']and format(zlib.crc32(b)&0xffffffff,'08x')==e['CRC32'],'whole original payload CRC/hash');ck(b==Path(e['extracted_path']).read_bytes(),'whole original extracted payload')
 ck(total==161736,'full expanded payload bytes')
 tex=Path(ready['controlling_TeX']['extracted_path']).read_text();raw=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0];abstract=abstract_plain(raw)
 ck(raw==(P/'abstract-source.tex').read_text(),'verbatim original abstract TeX');ck(abstract==(P/'abstract-text.txt').read_text().strip(),'abstract words/punctuation after math-only transcoding')
 pub=js(P/'config/publication.json');prom=js(P/'config/promotion.json');sec=js(P/'public-sections.json');ck(publication_facts(pub,prom,sec,abstract),'full-scope public copy/rights/date/private flags')
 ck(prom['publication_config_SHA256']==sha((P/'config/publication.json').read_bytes()),'private publication config binding')
 ck(pub['source_protocol_bindings_SHA256']==prom['source_protocol_bindings_SHA256']==sha((P/'SOURCE_PROTOCOL_BINDINGS.json').read_bytes()),'whole protocol adapter binding')
 for x in protocol['whole_license_and_README_texts']:ck(Path(x['path']).read_text()==x['text']and sha(Path(x['path']).read_bytes())==x['SHA256'],'actual rights/README whole text binding')
 page=Page();body=(P/'candidate/index.html').read_text();page.feed(body)
 ck(page.meta['robots']=='noindex,nofollow'and not any(a.get('rel')=='canonical'for tag,a in page.links),'private noindex/no canonical publication claim')
 ck(''.join(page.parts['abstract'])==abstract,'full original abstract is visible HTML not just metadata')
 for k,ps in sec['sections'].items():ck(''.join(page.parts[k])==''.join(ps),'complete indexable section '+k)
 ck(page.meta['citation_title']==pub['title']and page.meta['citation_doi']==pub['doi']and page.meta['citation_version']=='1.0.0'and page.meta['citation_publication_date']=='2026/10/22','scholarly citation metadata')
 ck(len(page.jsons)==1 and page.jsons[0]['@type']=='ScholarlyArticle'and page.jsons[0]['abstract']==abstract and page.jsons[0]['identifier']['value']==pub['doi']and page.jsons[0]['datePublished']=='2026-10-22','scholarly structured metadata')
 ck(len(page.iframes)==1 and page.iframes[0]['src'].startswith('assets/free-chain-nash-intersections.pdf'),'complete unchanged PDF reader')
 ck('background:#fff'in body and'Arial,sans-serif'in body and'max-width:780px'in body and'@media(max-width:600px)'in body,'plain white Arial responsive single-column CSS')
 for tag,a in page.links:
  u=a.get('href','')
  if u.startswith('assets/'):ck((P/'candidate'/u).is_file(),'local asset link '+u)
 ck(any('download'in a and a.get('href')=='assets/free-chain-nash-intersections.pdf'for tag,a in page.links),'direct PDF download')
 ck(all(x not in body for x in ['2026-11-15','root-clearance','SHA256','1068 checks','741 checks']),'no internal audit chronology or hashes in public HTML')
 search=js(P/'PDF_SEARCHABILITY.json');ck(search['searchable_text']is True and search['page_form_feeds']==5 and search['extracted_SHA256']==sha((P/'actual-published.txt').read_bytes()),'actual full PDF searchable5-page extraction')
 mutants=[]
 def mut(index,f):
  args=copy.deepcopy([pub,prom,sec]);f(args[index]);mutants.append(args)
 mut(0,lambda x:x.update(version='1.0'))
 mut(0,lambda x:x.update(publication_date='2026-11-15'))
 mut(0,lambda x:x.update(license='MIT'))
 mut(0,lambda x:x.update(code_license='CC BY 4.0'))
 mut(0,lambda x:x.update(canonical_url=x['proposed_canonical_url']))
 mut(0,lambda x:x.update(AA=x['proposed_canonical_url']))
 mut(0,lambda x:x.update(abstract=x['abstract'][:-1]))
 mut(1,lambda x:x.update(deployed=True))
 mut(1,lambda x:x.update(rendered=True))
 mut(1,lambda x:x.update(native_verified=True))
 mut(1,lambda x:x.update(root_editorial_clearance_received=True))
 mut(1,lambda x:x.update(follow_up={}))
 mut(1,lambda x:x.update(actual_scientific_review_cardinality=3))
 mut(2,lambda x:x['sections']['limitations'].__setitem__(1,'Equality of nonreduced schemes is asserted.'))
 mut(2,lambda x:x['sections']['result'].__setitem__(4,'For a few positive j,q only.'))
 mut(2,lambda x:x['normalizations'].pop())
 for i,a in enumerate(mutants):ck(not publication_facts(*a,abstract),'meaningful in-memory falsifier '+str(i))
 guard=js(P/'ABSENCE_GUARD.json');ck(guard['editorial_preexisting']is False and guard['outside_configs_written']is False,'historical absence/write guard')
 if not preseal:
  seal=js(P/'SEAL.json')
  for key,n in [('MANIFEST_SHA256','MANIFEST.json'),('PROTECTED_INPUTS_SHA256','PROTECTED_INPUTS.json'),('CLOSURE_SHA256','CLOSURE_PRESEAL.json'),('REPORT_SHA256','REPORT.md'),('VERDICT_SHA256','VERDICT.json'),('verifier_SHA256','verify_editorial_read_only.py')]:ck(seal[key]==sha((P/n).read_bytes()),'terminal seal '+n)
  ck(seal['completion_percent']==100 and seal['public_install_authorized']is False,'private final completion')
 return{'status':'PASS'if not fail else'FAIL','checks':checks,'failures':fail,'protected_inputs':len(prot['files']),'owned_files':len(manifest['files']),'native_ZIP_payloads':21,'in_memory_falsifiers':len(mutants),'mode':'preseal'if preseal else'final','network':False,'writes':False,'source_imports_or_scientific_execution':False}
def main():
 if sys.argv[1:]not in[[],['--preseal']]:raise SystemExit('Use no arguments or --preseal')
 try:r=verify(sys.argv[1:]==['--preseal'])
 except Exception as e:r={'status':'FAIL','failures':[type(e).__name__+': '+str(e)],'network':False,'writes':False,'source_imports_or_scientific_execution':False}
 print(json.dumps(r,indent=2));return 0 if r['status']=='PASS'else 1
if __name__=='__main__':raise SystemExit(main())
