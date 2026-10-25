"""Independent reading and exact comparison of actual approved fields and overlay."""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import hashlib,json,re,difflib,datetime,xml.etree.ElementTree as ET
E=Path(__file__).resolve().parent;P=E.parents[1];S=P/'verification/local-ambient-block-modulus-stage-sol-20261025';LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def same(a,b):return json.dumps(a,sort_keys=True,ensure_ascii=False,separators=(',',':'))==json.dumps(b,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def norm(s):return ' '.join(s.split())
checks=[];reads=[]
def test(n,v,detail=None):
 checks.append({'check':n,'pass':bool(v),'detail':detail})
def read(p,kind):
 data=p.read_bytes();reads.append({'path':str(p),'kind':kind,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'whole_bytes_read':True});return data
class Page(HTMLParser):
 def __init__(self,txt):
  super().__init__(convert_charrefs=True);self.section=None;self.p=None;self.heading=None;self.tag=None;self.paras={};self.headers={};self.anchors=[];self.current=None;self.attrs=[];self.feed(txt)
 def handle_starttag(self,t,a):
  a=dict(a);self.attrs.append((t,a))
  if t=='section':self.section=a.get('id')
  if t=='p' and self.section:self.p=[]
  if t in ('h1','h2'):self.heading=[];self.tag=t
  if t=='a':self.current=[a,[]]
 def handle_endtag(self,t):
  if t=='p' and self.p is not None:self.paras.setdefault(self.section,[]).append(norm(''.join(self.p)));self.p=None
  if t in ('h1','h2') and self.heading is not None:self.headers.setdefault(self.section or 'article',[]).append(norm(''.join(self.heading)));self.heading=None
  if t=='a' and self.current:self.anchors.append((self.current[0],norm(''.join(self.current[1]))));self.current=None
  if t=='section':self.section=None
 def handle_data(self,x):
  if self.p is not None:self.p.append(x)
  if self.heading is not None:self.heading.append(x)
  if self.current:self.current[1].append(x)
ids=['23333353','23416806','23441617'];facts={}
manifest=json.loads(read(S/'FINAL_MANIFEST.json','stage immutable owned manifest'));seal=json.loads(read(S/'FINAL_SEAL.json','stage immutable seal'))
test('supplied_stage_REPORT_pin',sha(S/'REPORT.md')=='cfbbe0e0def43a578791c057b606786296e081a15396fda2b04657d83f264b57')
test('supplied_stage_manifest_pin',sha(S/'FINAL_MANIFEST.json')=='3d3bac4a08dca77f0530cd376bc879383f4145de0b242695bd997776e863e22c')
test('supplied_stage_seal_pin',sha(S/'FINAL_SEAL.json')=='50b5fbf424fb15066c907435270cf44749ee5c0e71dad05078e58aa43c5979fb')
bad=[]
for x in manifest['files']:
 q=S/x['path']
 if q.stat().st_size!=x['bytes'] or sha(q)!=x['SHA256']:bad.append(x['path'])
test('all_428_stage_owned_bindings',len(manifest['files'])==428 and not bad,bad)
test('stage_seal_to_manifest',seal['manifest_SHA256']==sha(S/'FINAL_MANIFEST.json') and seal['owned_bindings']==428)
for name,current,diff in [('renderer','render_page.py','shared-renderer.diff'),('checker','final-content-check.py','shared-checker.diff')]:
 src=read(S/'inputs'/current,'exact frozen current '+name).decode();pro=read(S/('render_page.proposed.py' if name=='renderer' else 'final-content-check.proposed.py'),'complete proposed '+name).decode();expected=''.join(difflib.unified_diff(src.splitlines(True),pro.splitlines(True),fromfile='current',tofile='proposed'))
 test(name+'_complete_exact_shared_diff',expected==read(S/diff,'complete changed-scope '+name+' diff').decode())
 actual=P/('scripts/render_page.py' if name=='renderer' else 'verification/final-content-check.py');test(name+'_current_equals_frozen_input',actual.read_bytes()==src.encode())
for rid in ids:
 p=P/'papers'/rid;ed=p/'reviews/editorial';c=json.loads(read(p/'publication.json','complete config'));g=json.loads(read(p/'promotion.json','complete gate'));b=c['source_binding'];root=json.loads(read(P/g['root_clearance_file'],'original scientific authority'));editor=json.loads(read(P/f'verification/root-editorial-{rid}-20261025.json','original editorial authority'));original_sections=json.loads(read(ed/'public-sections.json','full original approved public sections'));stage_sections=json.loads(read(S/f'public-sections-{rid}.json','stage full public sections'));req=json.loads(read(ed/'METADATA_READER_SUPPORT_REQUIREMENTS.json','full original selected reader requirements'))
 for n in ['REPORT.md','PUBLIC_COPY.md','SCHEMA_ADAPTER.md','CITATION.bib']:
  read(ed/n,'full original editorial '+n)
 for field in ['source_receipt_path','metadata_path','raw_record_path','transport_receipt_path','source_tex_path']:
  read(p/b[field],'actual complete '+field)
 raw=json.loads((p/b['source_receipt_path']).read_text());api=json.loads((p/b['raw_record_path']).read_text());meta=json.loads((p/b['metadata_path']).read_text());transport=json.loads((p/b['transport_receipt_path']).read_text())
 article=S/'public/research'/c['slug'];html=read(article/'index.html','actual complete proposed HTML').decode();d=Page(html)
 for key,val in original_sections.items():
  if key!='publication_config_sha256':test(rid+':original_editorial_section_'+key,same(c[key],val))
 stage_by_id={x['id']:x for x in stage_sections}
 expected_stage={'abstract':[c['abstract']],'plain-language':c['plain_language'],'result':c['result'],'proof':c['why_it_works'],'limits':c['limitations'],'status':[c['status'],c['ai_disclosure'],c['edition_note']],'collaborate':[c['collaboration'],'Authorship and responsibilities would be discussed in relation to the substantive contributions made.']}
 test(rid+':stage_prose_sections_exact_original_fields',all(stage_by_id[k]['paragraphs']==v for k,v in expected_stage.items()))
 test(rid+':editorial_config_SHA_binding',original_sections['publication_config_sha256']==sha(p/'publication.json'))
 sectionfields={'abstract':[c['abstract']],'plain-language':c['plain_language'],'result':c['result'],'proof':c['why_it_works'],'limits':c['limitations'],'status':[c['status'],c['ai_disclosure'],c['edition_note']],'paper':[c['reader_intro'],'Open PDF in a full window · Download PDF · Download the original from Zenodo'],'collaborate':[c['collaboration'],'Authorship and responsibilities would be discussed in relation to the substantive contributions made.']}
 for key,val in sectionfields.items():test(rid+':complete_actual_paragraphs_'+key,d.paras.get(key)==val,{'paragraphs':len(d.paras.get(key,[]))})
 test(rid+':one_exact_original_abstract',d.headers['abstract']==['Original abstract'] and len(d.paras['abstract'])==1)
 test(rid+':visible_h1_original_title',d.headers['article']==[c['title']])
 test(rid+':actual_h1_self_anchor',re.search(r'<h1><a href="([^"]+)">',html).group(1)=='/research/'+c['slug']+'/')
 test(rid+':actual_Research_anchor',sum(a.get('href')=='/research/' and label=='Research' for a,label in d.anchors)==1)
 test(rid+':four_exact_reader_support_citation_files',{q.name for q in article.iterdir() if q.is_file()}=={'index.html','citation.bib',c['pdf_filename'],c['supplement_filename']})
 test(rid+':entire_prepared_BibTeX',read(article/'citation.bib','actual proposed BibTeX').decode()==c['prepared_bibtex']==(ed/'CITATION.bib').read_text())
 assets=[]
 for name in [c['pdf_filename'],c['supplement_filename']]:
  source=p/'sources'/name;out=article/name;test(rid+':unchanged_original_asset:'+name,sha(source)==sha(out) and source.stat().st_size==out.stat().st_size);assets.append({'name':name,'bytes':out.stat().st_size,'sha256':sha(out)})
 objkey='api_file_object' if rid=='23333353' else 'original_api_file_object';key='all_actual_assets' if rid=='23333353' else 'all_assets'
 test(rid+':whole_original_source_objects',same(raw,b['source_receipt_original']) and same(raw,g['source_receipt_original']) and same(raw[key],b[key]) and same(raw[key],g[key]) and same([x[objkey] for x in raw[key]],api['files']))
 test(rid+':complete_transport_objects',len(transport)==5 and same(transport,b['transport_receipt_original']) and same(transport,g['transport_receipt_original']))
 test(rid+':whole_root_object_literal_status',same(root,g['root_clearance_record']) and g['status']==root['status']==('PASS_WITH_NONCENTRAL_BIBLIOGRAPHIC_DEFECT' if rid=='23441617' else 'PASS'))
 test(rid+':separate_API_edition_and_declared_date',c['version']==api['metadata']['version']=='1.0' and c['publication_date']==api['metadata']['publication_date'] and b['record_created_utc']==api['created'])
 if rid=='23441617':
  disp=json.loads(read(ed/'BIBLIOGRAPHIC_DISPOSITION.json','complete original minor defect disposition'));test(rid+':whole_noncentral_defect',same(root['noncentral_bibliographic_defect'],disp['root_original_disposition']));test(rid+':unprinted_manuscript_version_separate',b['manuscript_version'] is None and b['manuscript_version_printed'] is False and c['version']=='1.0');test(rid+':public_HK181_and_unchanged_TeX180','Acta Math. 181 (1998), 1–61' in unescape(html) and r'Acta Math. \textbf{180}' in (p/b['source_tex_path']).read_text())
 facts[rid]={'title':c['title'],'slug':c['slug'],'pages':c['pdf_pages'],'status':root['status'],'declared_date':c['publication_date'],'API_created':api['created'],'API_version':api['metadata']['version'],'manuscript_version':b['manuscript_version'],'source_asset_order':[x[objkey]['key'] for x in raw[key]],'assets':assets,'section_paragraph_counts':{k:len(v) for k,v in sectionfields.items()},'API_objects_complete':True,'five_transports_whole':True,'authority_only_private_stage':editor['private_staging_authorized'] and not editor['production_integration_authorized']}
index=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',(S/'public/research/index.html').read_text(),re.S).group(1))['mainEntity'];test('proposed_exact_index68',len(index['itemListElement'])==index['numberOfItems']==68)
sm=[x.text for x in ET.fromstring((S/'public/research/sitemap.xml').read_text()).iter() if x.tag.endswith('loc')];test('proposed_exact_sitemap69',len(sm)==69)
for rid in ids:test(rid+':one_exact_proposed_index_title',sum(x['name']==facts[rid]['title'] and x['url']=='https://aleckriebel.com/research/'+facts[rid]['slug']+'/' for x in index['itemListElement'])==1)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if all(x['pass'] for x in checks) else 'ISSUES_FOUND','checks':checks,'facts':facts,'failed':[x for x in checks if not x['pass']]}
(E/'STATIC_COMPARISON_v2.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');(E/'AUTOMATED_WHOLE_READ_LEDGER_v2.json').write_text(json.dumps({'utc':result['utc'],'semantic_read_limit':'Whole byte reads and exact field/paragraph comparisons; not a new independent scientific PDF review. Manual complete code/copy/report reads are separately described in REPORT.','reads':reads},indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'failed':result['failed'],'stage_owned_rehashed':len(manifest['files']),'whole_read_entries':len(reads)},indent=2))
