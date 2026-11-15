"""One-time independent prewriter freeze for127128. No stage or website access.
Only original source/editorial and complete root science inputs are read. This
preparation writes inside its newly assigned directory, never project sources.
"""
from pathlib import Path
from hashlib import sha256,md5
from datetime import datetime,timezone
from html.parser import HTMLParser
import json,re
A=Path(__file__).resolve().parent;B=A.parents[1]
IDS=['23570763','23331295'];CONFIGS=['config/',''];EXPECTED_COUNTS=[(65,41),(65,60)]
def utc():return datetime.now(timezone.utc).isoformat()
def need(ok,why):
 if not ok:raise ValueError(why)
def digest(b):return {'bytes':len(b),'SHA256':sha256(b).hexdigest()}
def save(n,o):
 p=A/n;need(not p.exists(),'refuse input overwrite '+n);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def listing(root):
 p=list(root.rglob('*'));need(not any(q.is_symlink() for q in p),'noinputsymlinks');return sorted(q for q in p if q.is_file())
need(read_ignore:=(A/'.gitignore').read_text().splitlines()==['raw/'],'entireraw ignored before creation')
need(not (A/'raw').exists(),'rawfoldernew');(A/'raw').mkdir()
manifest={};namespaces={};records=[];comparisons=[];descriptors=[]
def snapshot(p):
 p=p.resolve();need(str(p).startswith(str(B)+'/'),'onlycatalogueoriginalinputs')
 rel=str(p.relative_to(B));b=p.read_bytes();r={**digest(b),'original':str(p),'copy':'raw/'+rel}
 if rel in manifest:need(manifest[rel]==r,'same repeated originalbinding');return r
 dest=A/r['copy'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);need(dest.read_bytes()==b,'freshrawcopy');manifest[rel]=r;return r
class Head(HTMLParser):
 def __init__(self):super().__init__();self.meta={};self.links=[];self.title='';self.intitle=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='meta':self.meta[a.get('name',a.get('property','charset'))]=a.get('content',a.get('charset'))
  if t=='link':self.links.append(a)
  if t=='title':self.intitle=True
 def handle_endtag(self,t):
  if t=='title':self.intitle=False
 def handle_data(self,d):
  if self.intitle:self.title+=d
def compared(label,left,right,origin=None,pointer=None):
 need(same(left,right),'whole typed/key/list/header/order/null comparison '+label)
 comparisons.append({'label':label,'same_types_keyorder_listorder_values':True,'original':origin,'container_pointer':pointer,'whole_value_SHA256':sha256(json.dumps(left,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()})
for rid,cfg,counts in zip(IDS,CONFIGS,EXPECTED_COUNTS):
 p=B/'papers'/rid;ed=p/'reviews/editorial';src=p/'sources'
 for folder,count in [(src,counts[0]),(ed,counts[1])]:
  paths=listing(folder);need(len(paths)==count,'actualcomplete namespace '+str(folder));namespaces[str(folder)]={'count':count,'relative_files':[str(q.relative_to(folder)) for q in paths]}
  for q in paths:snapshot(q)
 ready=json.loads((src/'SOURCE_READY.json').read_text());rootfile=B/'verification'/f'root-clearance-{rid}-20261115.json';root=json.loads(rootfile.read_text());snapshot(rootfile)
 adoptionfile=B/'verification'/f'root-editorial-{rid}-20261115.json';adoption=json.loads(adoptionfile.read_text());snapshot(adoptionfile)
 expected_adoption_pin='2d0d6f6ee869787cb707995351cf39e2509dfa3d66a19d2111a8381cbe3ca175' if rid==IDS[0] else '6bbd8861012b089a3b39376b4a1dc731509ecadff744f17e769c37576f5d8287'
 need(sha256(adoptionfile.read_bytes()).hexdigest()==expected_adoption_pin and adoption['root_editorial_adopted'] is True,'finalrooteditorialauthority')
 rr=Path(root['root_review']['path']);rr=rr if rr.is_absolute() else B/rr;snapshot(rr)
 # Pin current heterogeneous scientific verdict/seal files as opaque whole JSON.
 for name in ['scope/VERDICT.json','scope/SEAL.json','scope/FINAL_SEAL.json','adversarial/VERDICT.json','adversarial/SEAL.json','adversarial/FINAL_SEAL.json']:
  q=p/'reviews'/name
  if q.exists():snapshot(q)
 pubfile=ed/(cfg+'publication.json');promfile=ed/(cfg+'promotion.json');pub=json.loads(pubfile.read_text());promotion=json.loads(promfile.read_text());adapter=json.loads((ed/'SCHEMA_ADAPTER.json').read_text());protocol=json.loads((ed/'SOURCE_PROTOCOL_BINDINGS.json').read_text());rights=json.loads((ed/'RIGHTS_AND_IDENTITY.json').read_text())
 html=(ed/'candidate/index.html').read_text();mm=re.findall(r'<main\b[^>]*>.*?</main>',html,re.S);need(len(mm)==1,'onecompleteowner main');main=mm[0];expected_main=main.replace('<main>','<main id="main">',1) if main.startswith('<main>') else main
 block=re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',html,re.S);need(len(block)==1,'oneownerJSONLD');ld=json.loads(block[0]);article=next(x for x in ld['@graph'] if x.get('@type')=='ScholarlyArticle') if '@graph' in ld else ld
 h=Head();h.feed(html.split('</head>',1)[0]);abstract=re.search(r'<h2>Original abstract</h2>\s*<p>(.*?)</p>',main,re.S);need(abstract is not None,'onevisiblewholeabstract')
 from html import unescape
 compared(rid+'/visibleabstract',unescape(abstract[1]),pub['abstract']);compared(rid+'/scholarlyabstract',article['abstract'],pub['abstract'])
 compared(rid+'/originalarticlepublication',article['datePublished'],pub['publication_date']);compared(rid+'/nativeversion',ready['version'],pub['version'])
 need(pub['canonical_url'] is None and pub['AA'] is None and pub['follow_up'] is None,'literalprivatepublicationnulls')
 assets=ready['all_native_assets_in_original_order'];native_objects=[json.loads(Path(d['path']).read_text()) for d in ready['whole_native_API_objects']];transports=json.loads(Path(ready['actual_transport_receipts']['path']).read_text());schema=json.loads(Path(ready['native_schema_types']['path']).read_text());archive=json.loads(Path(ready['whole_archive_custody']['path']).read_text())
 need(type(transports) is list and len(transports)==(7 if rid==IDS[0] else 8),'literalnative orderedtransportlist')
 need(type(schema) is list,'literal native schema list')
 order=[q['original_api_file_object']['key'] for q in assets]
 need(order==(['periodic-lefschetz-source-and-verification.zip','periodic-lefschetz.pdf'] if rid==IDS[0] else ['nullstellensatz.tex','verification-package.zip','nullstellensatz.pdf']),'exactnativeorder')
 asset_rows=[]
 for q in assets:
  name=q['original_api_file_object']['key'];nb=Path(q['path']).read_bytes();cb=(ed/'candidate/assets'/name).read_bytes();need(nb==cb and digest(nb)=={'bytes':q['bytes'],'SHA256':q['SHA256']} and 'md5:'+md5(nb).hexdigest()==q['original_api_file_object']['checksum'],'wholenativeasset/candidate')
  asset_rows.append({'native_original_object':q,'candidate_relative':'assets/'+name,'binding':digest(nb)})
 bib=(ed/'candidate/assets/citation.bib').read_bytes();need(bib==(ed/'citation.bib').read_bytes(),'wholeBiboriginal')
 # Recursively compare every descriptor-wrapped original object, without
 # interpreting or normalizing custom status field names.
 containers=[('protocol',protocol),('publication',pub),('promotion',promotion),('adapter',adapter),('rootclearance',root)]
 def scan(node,pointer,label):
  if isinstance(node,dict):
   if 'path' in node and 'whole_literal_object' in node:
    q=Path(node['path']);q=q if q.is_absolute() else B/q
    need(q.exists(),'descriptororiginalexists');b=q.read_bytes();need(len(b)==node['bytes'] and sha256(b).hexdigest()==node['SHA256'],'wholeoriginaldescriptorpin');actual=json.loads(b);snapshot(q);compared(rid+'/'+label+':'+str(pointer),node['whole_literal_object'],actual,str(q),pointer+['whole_literal_object']);descriptors.append({'record_id':rid,'container':label,'pointer':pointer,'original':str(q),'binding':digest(b)})
   if 'path' in node and 'whole_literal_text' in node:
    q=Path(node['path']);q=q if q.is_absolute() else B/q
    snapshot(q);compared(rid+'/'+label+'/literaltext',node['whole_literal_text'],q.read_text(),str(q),pointer+['whole_literal_text'])
   for k,v in node.items():
    lower=k.lower()
    if lower in {'whole_original_source_ready','full_original_source_ready'} and isinstance(v,dict) and 'schema' in v:compared(rid+'/'+label+'/'+k,v,ready,str(src/'SOURCE_READY.json'),pointer+[k])
    if 'transport' in lower and isinstance(v,list) and v and isinstance(v[0],dict) and 'HTTP_status' in v[0]:compared(rid+'/'+label+'/'+k,v,transports,str(Path(ready['actual_transport_receipts']['path'])),pointer+[k])
    if 'native_api' in lower and isinstance(v,list) and len(v)==4 and isinstance(v[0],dict) and 'id' in v[0]:compared(rid+'/'+label+'/'+k,v,native_objects,None,pointer+[k])
    if 'archive_custody' in lower and isinstance(v,dict) and 'containers' in v:compared(rid+'/'+label+'/'+k,v,archive,str(Path(ready['whole_archive_custody']['path'])),pointer+[k])
    if 'schema' in lower and isinstance(v,list) and v and isinstance(v[0],dict) and len(v)==len(schema):compared(rid+'/'+label+'/'+k,v,schema,str(Path(ready['native_schema_types']['path'])),pointer+[k])
    scan(v,pointer+[k],label)
  elif isinstance(node,list):
   for i,v in enumerate(node):scan(v,pointer+[i],label)
 for label,o in containers:scan(o,[],label)
 # Unique complete config/adapter embeddings are heterogenous by design.
 if rid==IDS[0]:
  compared(rid+'/adapter source_binding',adapter['whole_original_source_binding'],pub['source_binding']);compared(rid+'/adapter review_metadata',adapter['whole_original_review_metadata'],pub['review_metadata']);compared(rid+'/promotion rootclearance',promotion['whole_root_scientific_clearance_record'],root)
 else:
  compared(rid+'/adapter whole protocol',adapter['whole_actual_source_protocol'],protocol);compared(rid+'/adapter fullpublication',adapter['unique_publication_config'],pub);compared(rid+'/adapter fullpromotion',adapter['promotion_config'],promotion);compared(rid+'/adapter source_binding',adapter['source_binding_complete'],pub['source_binding']);compared(rid+'/adapter review_metadata',adapter['review_metadata_complete'],pub['review_metadata'])
 canonical='https://aleckriebel.com/research/'+pub['slug']+'/'
 frames=re.findall(r'<iframe\b[^>]*>',main);need(len(frames)==1,'one actualreader');md=(ed/'PUBLIC_COPY.md').read_text()
 rec={'record_id':rid,'row':127 if rid==IDS[0] else 128,'title':pub['title'],'slug':pub['slug'],'canonical_proposal':canonical,'description':pub['description'],'full_original_abstract':pub['abstract'],'datePublished':pub['publication_date'],'native_version':pub['version'],'printed_version':pub['printed_version'],'printed_version_field_present':True if rid==IDS[0] else pub['printed_version_field_present'],'original_main':main,'expected_main_with_only_missing_id':expected_main,'main_expected_binding':digest(expected_main.encode()),'original_candidate_head_metadata':h.meta,'original_candidate_links':h.links,'original_full_scholarly_object':article,'native_assets_in_literal_order':asset_rows,'BibTeX':{'candidate_relative':'assets/citation.bib','binding':digest(bib)},'native_order':order,'source_ready_whole_literal':ready,'native_API_whole_literal':native_objects,'transport_aggregate_whole_literal':transports,'native_schema_whole_literal':schema,'archive_custody_whole_literal':archive,'publication_config_whole_literal':pub,'promotion_config_whole_literal':promotion,'adapter_whole_literal':adapter,'source_protocol_whole_literal':protocol,'root_scientific_clearance_whole_literal':root,'root_editorial_authority_whole_literal':adoption,'rights_whole_literal':rights,'actual_candidate_iframe_tag':frames[0],'PUBLIC_COPY_reader_has_width_height':bool(re.search(r'<iframe[^>]*width="100%"[^>]*height="850"',md)),'candidate_main_raw_width_height_present':('width=' in frames[0] or 'height=' in frames[0]),'editorial_seal':digest((ed/'SEAL.json').read_bytes())}
 records.append(rec)
# Recheck all namespaces across the full rawcopy operation, including terminals.
for root,n in namespaces.items():need([str(p.relative_to(root)) for p in listing(Path(root))]==n['relative_files'],'whole source/editorialnamespace unchangedacrosscopy')
for rel,row in manifest.items():need(Path(row['original']).read_bytes()==(A/row['copy']).read_bytes(),'all originalsfreshcopy unchanged')
save('INPUT_MANIFEST.json',{'UTC':utc(),'raw_ignored_before_creation':True,'files':manifest,'complete_namespaces':namespaces,'website_or_stage_content_read':False})
save('WHOLE_NATIVE_AND_EDITORIAL_CONTRACT.json',{'UTC':utc(),'scope':'Independent original expectations before writer output and before website GO; final rooteditorial adoptions received; websiteGO stillpending','records':records,'whole_objects_not_normalized':True})
save('COMPARISON_RECEIPTS.json',{'UTC':utc(),'whole_typed_ordered_comparisons':comparisons,'count':len(comparisons),'whole_descriptor_originals':descriptors,'original_files_copied':len(manifest),'source_and_editorial_namespace_files':231,'all_equal':True})
paths=[]
for rec in records:
 base='research/'+rec['slug']+'/'
 paths.append(base+'index.html');paths.extend(base+q['candidate_relative'] for q in rec['native_assets_in_literal_order']);paths.append(base+rec['BibTeX']['candidate_relative'])
paths+=['research/index.html','research/sitemap.xml'];need(len(paths)==len(set(paths))==11,'derived11overlaypaths')
save('EXPECTED_OUTPUTS.json',{'UTC':utc(),'independent_before_writer':True,'records':[{'record_id':r['record_id'],'slug':r['slug'],'canonical_proposal':r['canonical_proposal'],'main_expected_binding':r['main_expected_binding'],'native_order':r['native_order'],'datePublished':r['datePublished'],'native_version':r['native_version'],'printed_version':r['printed_version'],'printed_version_field_present':r['printed_version_field_present'],'asset_relative_paths':[q['candidate_relative'] for q in r['native_assets_in_literal_order']]+['assets/citation.bib'],'whole_original_abstract':r['full_original_abstract'],'actual_candidate_iframe_tag':r['actual_candidate_iframe_tag']} for r in records],'exact_overlay_paths':sorted(paths),'derivation':{'record127_leaves':4,'record128_leaves_including_nativeTeX':5,'new_leaves':9,'aggregate_replacements':2,'overlay_paths':11},'future_requested_baseline_only_not_captured':[605,90,91],'conditional_virtual_counts_if_futurebaseline_confirmed':[614,92,93],'website_baseline_captured':False,'website_GO_received':False,'root_editorial_adoptions_received':True,'main_rule':'Whole original candidate main, only missing id=main added if needed; no prose/formula/Unicode/order/link/attribute change without later explicit root authority','head_and_wrapper_requirements':['Existingresearch.css/favicon/sitepattern white Arial singlecolumn','indexfollow/canonical/citation/ORCID accurate for proposed publicoutput','mutuallylinkedWebPage/ScholarlyArticle graph andwholeoriginalabstract','original22/12Octoberpublicationdates separatefrombuilddate','128Zenodoversion1.0 explicitlydistinctfromabsentprintedversion','everywhole nativeassetinoriginalorder,localandoriginaldownloadlinks,unchangedBib','old90typed/visibleindexand91wholeXMLnodes exactretentiononlyafteractualfutureGO'],'rights':{'23570763':'CCBY4prose/source;MITauthoredcode;rootexplicitlyrequiresomittingmixedZIPencodinglicense;articleandPDFCCBYvisiblemixedrights' ,'23331295':'broadCCBY4allauthoredpaperTeXcode;separatecodeinstrumentnull;noMITdefault'},'private_original_flags':'Allhistoricalfalse/null/nativeacquisition100 andheterogeneouscustomstatuses retainedwhole; newauditdoesnotpromotethem','publication_authority':False,'canonical_url':None,'AA':None,'follow_up':None})
print(json.dumps({'source_editorial_namespace_counts':[n['count'] for n in namespaces.values()],'original_files':len(manifest),'whole_typed_ordered_comparisons':len(comparisons),'derived_overlay_paths':len(paths),'new_leaves':9,'native_orders':[r['native_order'] for r in records],'writer_and_site_unread':True,'root_editorial_received_websiteGO_pending':True}))
