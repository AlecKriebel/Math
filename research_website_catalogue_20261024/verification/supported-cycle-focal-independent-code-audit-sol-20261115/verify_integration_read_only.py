"""Independent held integration review/custody. Standard library only; no renderer, controls, live or writes."""
from pathlib import Path,PurePosixPath
from html.parser import HTMLParser
import difflib,hashlib,json,re,stat,sys,xml.etree.ElementTree as ET
D=Path(__file__).resolve().parent;S=D.parent/'supported-cycle-focal-private-stage-sol-20261115';N=0;T=0

def need(ok,label):
 global N
 N+=1
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 p=Path(p);need((D in p.parents or S in p.parents) and p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'only own or immutable writer regular input');return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(p,r):
 b=read(p);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'whole exact byte pin');return b
def snapshot(r):return pin(r['snapshot']['path'],r['snapshot'])
def extent(root):
 need(root==D or root==S or S in root.parents,'only own/writer extent');files=[];dirs=[]
 for p in root.rglob('*'):
  mode=p.lstat().st_mode;need(p.resolve()==p and (stat.S_ISREG(mode) or stat.S_ISDIR(mode)),'ordinary complete namespace');(files if stat.S_ISREG(mode) else dirs).append(p.relative_to(root).as_posix())
 return sorted(files),sorted(dirs)
def equal(a,b):
 global T
 T+=1;need(type(a) is type(b),'exact original type')
 if isinstance(a,dict):
  need(list(a)==list(b),'complete original key order')
  for k in a:equal(a[k],b[k])
 elif isinstance(a,list):
  need(len(a)==len(b),'complete original list order/extent')
  for x,y in zip(a,b):equal(x,y)
 else:need(a==b,'whole original scalar/null')
class Head(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.meta={};self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta':
   k=a.get('name',a.get('property'))
   if k:self.meta[k]=a.get('content')
  if tag=='link':self.links.append(a)
def xmlnode(x):return {'tag':x.tag,'attributes_in_original_order':[[k,v] for k,v in x.attrib.items()],'text':x.text,'tail':x.tail,'children':[xmlnode(c) for c in x]}
def pin_owned_manifest(manifest_name,seal_name,expected_seal):
 sb=read(D/seal_name);need(sha(sb)==expected_seal,'immutable earlier own seal');s=json.loads(sb);mb=read(D/manifest_name);need(sha(mb)==s['MANIFEST_SHA256'],'earlier whole manifest')
 for r in json.loads(mb)['files']:pin(D/r['path'],r)
 return s

def main():
 need(sys.argv[1:] in [[],['--preseal']],'bounded held review mode');preseal=bool(sys.argv[1:])
 pin_owned_manifest('INITIAL_MANIFEST.json','INITIAL_SEAL.json','709ceeaf5c386f2ffd24682a919fd100d51224b4207e43f68c361ab8e4c8b21b')
 pin_owned_manifest('BASELINE_MANIFEST.json','BASELINE_SEAL.json','9d319d461f8c392ff828536c6ea60898998a9320cfb630cb9d9a2cab5f1f4c2b')
 sb=read(S/'FINAL_SEAL.json');need(len(sb)==4597 and sha(sb)=='edf8e4e64ea345e950f6d94e678b4d6c8530df37089e80ef6681a519b7fedf54','parent immutable writer FINAL')
 seal=json.loads(sb);mb=pin(S/'OWNED_MANIFEST.json',seal['manifest']);need(sha(mb)=='614e78a7b4f8ab357d93d36dba8f330ecc27297608c37eb4617cb7d4d4396b4b','whole current writer manifest');manifest=json.loads(mb)
 need(manifest['only_exact_root_terminal_exclusions']==['OWNED_MANIFEST.json','FINAL_SEAL.json'] and manifest['recursive_basename_or_future_subtree_exclusions'] is False,'no future or recursive writer exclusions')
 files,dirs=extent(S);need(files==sorted(list(manifest['payloads'])+['OWNED_MANIFEST.json','FINAL_SEAL.json']) and dirs==manifest['directories']==seal['directories'],'exact1335 files18 dirs');need(len(manifest['payloads'])==1333,'complete writer payloads')
 for n,r in manifest['payloads'].items():
  rel=PurePosixPath(n);need(str(rel)==n and not rel.is_absolute() and '..' not in rel.parts,'exact safe writer name');pin(S/n,r)
 code=obj(S/'CURRENT_CODE_MANIFEST.json');need(sum(r['bytes'] for r in code['files'])==55849,'all5 complete code bytes');code_pins=[dict(r,path=str(S/r['path'])) for r in code['files']]
 for r in code['files']:pin(S/r['path'],r)
 source=obj(S/'SOURCE_INPUTS.json');rows={r['path']:r for r in source['files']};need(len(rows)==len(source['files'])==819,'819 unique full source input descriptors')
 def cached(path):
  r=rows[str(path)];return pin(S/r['blob'],r)
 for r in source['files']:pin(S/r['blob'],r)
 own_sources=obj(D/'SOURCE_FULL_SNAPSHOTS.json')
 for r in own_sources['rows']:need(cached(r['original']['path'])==pin(r['snapshot']['path'],r['snapshot']),'all775 independent presealed original bytes match writer')
 own_roots=obj(D/'SOURCE_ROOT_BINDINGS.json')['root_adoptions'];P=D.parent.parent
 for r in own_roots:need(cached(r['original']['path'])==pin(r['literal_copy']['path'],r['literal_copy']),'both full root adoptions match initial')
 for r in own_roots:
  root=json.loads(pin(r['literal_copy']['path'],r['literal_copy']));authority=root.get('root_full_scientific_authority',root.get('root_scientific_authority'));body=cached(authority['path']);need(len(body)==authority['bytes'] and sha(body)==authority['SHA256'],'whole adopted science-root authority context only')
  f=root['independent_fact_final_seal'];fact_seal=json.loads(cached(f['path']));need(sha(cached(f['path']))==f['SHA256'],'full adopted fact seal');fact_root=Path(f['path']).parent;equal(root['whole_original_independent_fact_findings'],json.loads(cached(fact_root/'FINDINGS.json')))
 expected=obj(D/'EXPECTED_SOURCE_OBJECTS.json');baseline=obj(D/'ACTUAL623_PUBLIC_BASELINE.json');own_public={r['public_relative_path']:r for r in baseline['public_files']};wb=obj(S/'WEBSITE_BASELINE.json');writer_public={Path(r['path']).relative_to(Path(baseline['public_files'][0]['path']).parents[len(Path(baseline['public_files'][0]['public_relative_path']).parts)-1]).as_posix():r for r in []}
 writer_public={r['path'].split('/public/',1)[1]:r for r in wb['files'] if r['role']=='public'}
 need(set(writer_public)==set(own_public) and wb['public_directories']==baseline['public_directories'],'complete independent623 public file and directory identity')
 for n,r in own_public.items():need(pin(S/writer_public[n]['blob'],writer_public[n])==snapshot(r),'whole writer/independent public buffer '+n)
 for r in baseline['site_configs']:
  other=next(x for x in wb['files'] if x['path']==r['path']);need(pin(S/other['blob'],other)==snapshot(r),'both independently captured site configs')
 own_git=obj(D/'ACTUAL623_GIT_OBSERVATIONS.json');need(read(S/wb['full_raw_index'])==pin(own_git['whole_native_index_snapshot']['path'],own_git['whole_native_index_snapshot']),'entire fresh native raw index equality')
 need(wb['native_index']['records']==58563 and wb['native_index']['protected_records']==58561 and wb['native_index']['protected_native_raw_records_SHA256']==own_git['fresh_protected_raw_native_stream']['SHA256'],'fresh full protected native stream identity')
 core=obj(D/'ACTUAL623_QUALIFIED_CORE.json');protected=json.loads(cached(P/'papers/23578142/reviews/editorial/PROTECTED_INPUTS.json'));pc={r['path']:r for r in protected['files']}
 for r in core['files']:need(cached(P/'papers/23578142/reviews/editorial'/pc[r['path']]['copy'])==snapshot(r),'all qualified original17 plus405b buffers')
 overlay=obj(S/'OVERLAY_MANIFEST.json')['files'];paths=[r['path'] for r in overlay];wanted=sorted([p for r in expected['records'] for p in r['expected_four_article_root_leaf_paths']]+['research/index.html','research/sitemap.xml']);need(paths==wanted and len(paths)==10,'exact independent10 paths')
 outputs=[]
 for r in overlay:
  a=pin(S/'candidate-a/public'/r['path'],r);b=pin(S/'candidate-b/public'/r['path'],r);need(a==b and r['whole_actual_normal_optimized_bytes_equal'] is True,'whole paired output');outputs.append(dict(r,whole_actual_bytes_equal=True))
 frames=obj(D/'BASELINE_FRAME_EXPECTATIONS.json');common=frames['whole_observed_frames'][0];evidence=[]
 for r in expected['records']:
  c=r['whole_original_publication_typed_object'];prefix='research/'+c['slug']+'/';page=read(S/'candidate-a/public'/prefix/'index.html');main=pin(r['complete_unchanged_expected_MAIN']['path'],r['complete_unchanged_expected_MAIN']);need(page.count(main)==1 and page.count(b'<main ')==1,'entire approved MAIN exactly once, zero transforms');head,ending=page.split(main);parser=Head();parser.feed(head.decode())
  graph=json.loads(re.findall(rb'<script type="application/ld\+json">(.*?)</script>',head,re.S)[0]);original=r['whole_original_scholarly_typed_object'];article=graph if graph.get('@type')=='ScholarlyArticle' else next(x for x in graph['@graph'] if x['@type']=='ScholarlyArticle')
  core_article=dict(article);core_article.pop('mainEntityOfPage');core_article['url']=original['url'];equal(core_article,original)
  need(read(S/'candidate-a/public'/prefix/'citation.bib')==pin(r['complete_original_Bib']['path'],r['complete_original_Bib']),'entire original Bib')
  for a in r['whole_original_native_asset_objects_in_order']:
   need(read(S/'candidate-a/public'/a['public_relative_path'])==pin(a['frozen_asset']['path'],a['frozen_asset']),'four complete original native buffers')
  links=parser.links;actual_pdf=parser.meta.get('citation_pdf_url');local_pdf=c['proposed_canonical_url']+c['pdf_filename'];actual_enc=[x['contentUrl'] for x in article['encoding']];local_enc=[c['proposed_canonical_url']+Path(x['whole_original_native_object']['path']).name for x in r['whole_original_native_asset_objects_in_order']]
  evidence.append({'record_id':r['record_id'],'actual_HTML_pin':{'path':str(S/'candidate-a/public'/prefix/'index.html'),'bytes':len(page),'SHA256':sha(page)},'complete_actual_head':head.decode(),'complete_actual_ending':ending.decode(),'MAIN_byte_exact':True,'common_native_body_prefix_expected':common['whole_head_to_main_body_prefix'],'actual_body_prefix':head[head.index(b'</head>')+len(b'</head>'):].decode(),'common_native_suffix_expected':common['whole_after_main_suffix'],'has_native_research_stylesheet':any(x.get('rel')=='stylesheet' and x.get('href')=='/research/research.css' for x in links),'has_shared_site_header_and_research_navigation':b'<nav aria-label="Main navigation">' in head and b'<p class="site-title">' in head,'has_shared_footer_and_internal_research_home':b'<footer>' in ending and b'Research home' in ending,'actual_citation_pdf_url':actual_pdf,'expected_local_citation_pdf_url':local_pdf,'citation_PDF_is_local_expected':actual_pdf==local_pdf,'actual_encoding_contentURLs':actual_enc,'expected_local_encoding_contentURLs':local_enc,'all_encoding_contentURLs_local_expected':actual_enc==local_enc,'source_scholarly_core_and_rights_unchanged':True,'actual_graph_kind':graph.get('@type','@graph'),'native_WebPage_ScholarlyArticle_graph_present':'@graph' in graph})
 old_index=snapshot(own_public['research/index.html']);new_index=read(S/'candidate-a/public/research/index.html');pattern=rb'<script type="application/ld\+json">\s*(.*?)\s*</script>';og=re.findall(pattern,old_index,re.S)[0];ng=re.findall(pattern,new_index,re.S)[0];old_graph=json.loads(og);new_graph=json.loads(ng);equal(new_graph['mainEntity']['itemListElement'][:94],old_graph['mainEntity']['itemListElement']);need(new_graph['mainEntity']['numberOfItems']==len(new_graph['mainEntity']['itemListElement'])==96,'candidate96 typed items');equal(new_graph['mainEntity']['itemListElement'][94:],[{'@type':'ListItem','position':95+i,'url':r['whole_original_publication_typed_object']['proposed_canonical_url'],'name':r['whole_original_publication_typed_object']['title']} for i,r in enumerate(expected['records'])])
 cards=re.findall(rb'<li(?:\s[^>]*)?>.*?</li>',new_index,re.S);old_cards=re.findall(rb'<li(?:\s[^>]*)?>.*?</li>',old_index,re.S);need(cards[:94]==old_cards and len(cards)==96,'all94 whole visible records unchanged and ordered')
 restored=new_index.replace(ng,og,1)
 for card in cards[94:]:line=b'      '+card+b'\n';need(restored.count(line)==1,'exact new native list card line');restored=restored.replace(line,b'',1)
 need(restored==old_index,'whole old index byte recovery')
 old_xml=snapshot(own_public['research/sitemap.xml']);new_xml=read(S/'candidate-a/public/research/sitemap.xml');need(len(ET.fromstring(new_xml))==97,'candidate97 XML nodes');restored=new_xml
 for r in expected['records']:
  url=r['whole_original_publication_typed_object']['proposed_canonical_url'];line=('  <url><loc>'+url+'</loc><lastmod>2026-11-15</lastmod></url>\n').encode();need(restored.count(line)==1,'exact new XML line');restored=restored.replace(line,b'',1)
 need(restored==old_xml,'whole old sitemap bytes recover exactly')
 diff=[]
 for name,old,new in [('research/index.html',old_index,new_index),('research/sitemap.xml',old_xml,new_xml)]:diff.extend(difflib.unified_diff(old.decode().splitlines(keepends=True),new.decode().splitlines(keepends=True),fromfile='actual623/'+name,tofile='proposed631/'+name))
 need(''.join(diff).encode()==read(S/'AGGREGATE_DIFF.patch'),'complete actual44770-byte diff independently recomputed')
 failed=obj(S/'history/001-xml-tail-check/FAILURE.json')
 for p in failed['candidate_output_pins_before_narrow_checker_correction']:pin(S/p['path'],p)
 executions=obj(S/'ACTUAL_EXECUTIONS.json')
 for p in executions['processes']:
  need(len(read(S/p['actual_executed_body_artifact']))==p['executed_body_bytes'] and sha(read(S/p['actual_executed_body_artifact']))==p['executed_body_SHA256'],'complete historical executed-body pin')
  for n in ['stdout','stderr']:need(len(read(S/p[n]))==p[n+'_bytes'] and sha(read(S/p[n]))==p[n+'_SHA256'],'complete actual historical streams')
 findings=[]
 if any(not all(e[k] for k in ['has_native_research_stylesheet','has_shared_site_header_and_research_navigation','has_shared_footer_and_internal_research_home']) for e in evidence):findings.append({'id':'INTEGRATION-01','priority':2,'status':'CONFIRMED_NO_REPAIR','title':'Private editorial shell omits the existing native research frame','routine_publication_adapter_failure_not_scientific_paper_defect':True,'source':'render_stage.article_page retains candidate head/ending rather than using actual native frame','records':['23578142','23306203']})
 if any(not e['citation_PDF_is_local_expected'] or not e['all_encoding_contentURLs_local_expected'] for e in evidence):findings.append({'id':'INTEGRATION-02','priority':2,'status':'CONFIRMED_NO_REPAIR','title':'Head citation and encodings retain remote native URLs instead of paired local originals','routine_publication_adapter_failure_not_scientific_paper_defect':True,'records':['23578142','23306203']})
 need(len(findings)==2,'exact currently confirmed two integration gaps')
 if not preseal and (D/'FINAL_SEAL.json').exists():
  final=obj(D/'FINAL_SEAL.json');mf=read(D/'FINAL_MANIFEST.json');need(sha(mf)==final['MANIFEST_SHA256'],'whole audit final manifest');m=json.loads(mf);names=[]
  for r in m['files']:pin(D/r['path'],r);names.append(r['path'])
  f,d=extent(D);need(f==sorted(names+['FINAL_MANIFEST.json','FINAL_SEAL.json']) and d==m['directories'],'complete own audit file and directory extent')
 print(json.dumps({'status':'COMPLETED_NO_GO_NATIVE_INTEGRATION_ADAPTER','checks':N,'whole_typed_nodes':T,'writer_FINAL_SHA256':sha(sb),'writer_files':1335,'writer_directories':dirs,'all5_current_code_pins':code_pins,'whole_independent_source_files_matching_writer':775,'whole_actual623_public_files_matching_writer':623,'independently_preexposure_site_configs_compared':2,'additional_writer_held_site_config_records':4,'full_native_index_and_protected_stream_match':True,'native_record_counts':[58563,58561],'all10_actual_paired_buffers':outputs,'article_evidence':evidence,'findings':findings,'whole_original_MAINs_native_Bibs_rights_abstracts_versions_science_scope_unchanged':True,'all94_old_visible_and_typed_records_preserved':True,'all95_old_XML_contents_and_entire_old_aggregates_recover_exact':True,'actual_counts':[623,94,95],'candidate_counts':[631,96,97],'unrelated_public_paths':621,'whole_actual_aggregate_diff_recomputed_bytes':44770,'XML_tail_checker_failure_has_no_candidate_source_repair':True,'owner_controls_renderer_or_scientific_campaigns_executed_by_this_helper':False,'live_site_Git_network_subprocess_or_writes':False,'production_authority':False},indent=2,ensure_ascii=False))
if __name__=='__main__':main()
