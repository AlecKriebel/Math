from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib, json, re, stat, sys
O=Path(__file__).resolve().parent
P=O.parent.parent
W=P/'papers/23191247/reviews/editorial'
S=P/'papers/23191247/sources'
checks={}
def digest(b): return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes()
 return {'path':str(p),'bytes':len(b),'SHA256':digest(b)}
def check(name, value): checks[name]=bool(value)
def norm(s): return ' '.join(s.split())
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.text=[];self.metas={};self.ids=[];self.hrefs=[]
 def handle_data(self,s):self.text.append(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta' and 'name' in a:self.metas[a['name']]=a.get('content')
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a' and 'href' in a:self.hrefs.append(a['href'])
def plain(s):
 t=Text();t.feed(s);return norm(''.join(t.text))
facts=json.loads((O/'SOURCE_FACTS.json').read_bytes())
seal=json.loads((O/'INITIAL_SEAL.json').read_bytes())
check('own_INITIAL_seal',pin(O/'INITIAL_SEAL.json')['SHA256']=='240b9330b94d321a70bfe1284da0cf8e9ffebc68e52375db6c55a1e6d8dc79a5')
for z in seal['finite_payload']:
 v=pin(O/z['path']);check('own_INITIAL:'+z['path'],v['bytes']==z['bytes'] and v['SHA256']==z['SHA256'])
final=json.loads((W/'FINAL.json').read_bytes())
manifest=json.loads((W/'OWNED_MANIFEST.json').read_bytes())
check('actual_FINAL_pin',pin(W/'FINAL.json')['bytes']==6071 and pin(W/'FINAL.json')['SHA256']=='88ce14501c4dfaa5bc5075a888d0d611193fec37653eba916c281b24d2b39dcc')
check('actual_manifest_pin',pin(W/'OWNED_MANIFEST.json')['bytes']==6065 and pin(W/'OWNED_MANIFEST.json')['SHA256']=='d7240e56141e2678253ad426a960354ccaf11d622f590bad6d99d470434310c3')
paths=list(W.rglob('*'));files={p.relative_to(W).as_posix() for p in paths if p.is_file()};dirs={p.relative_to(W).as_posix() for p in paths if p.is_dir()}
check('exact_file_extent',len(files)==32 and files=={r['path'] for r in manifest['files']}|{'OWNED_MANIFEST.json','FINAL.json'})
check('exact_directory_extent',dirs==set(manifest['child_directories'])=={'preview','renders'})
check('exact_terminal_controls',manifest['terminal_controls']==['OWNED_MANIFEST.json','FINAL.json'])
check('no_symlinks_or_specials',all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in paths))
for z in manifest['files']:
 p=W/z['path'];b=p.read_bytes();check('writer_payload:'+z['path'],len(b)==z['bytes'] and digest(b)==z['SHA256'] and format(stat.S_IMODE(p.stat().st_mode),'04o')==z['mode'])
body=(W/'preview/index.html').read_text();m=re.findall(r'<main id="main">[\s\S]*?</main>',body);h=re.findall(r'<head>[\s\S]*?</head>',body)
check('one_complete_MAIN_head',len(m)==len(h)==1)
main=m[0];head=h[0]
check('whole_HTML_pin',len(body.encode())==17185 and digest(body.encode())=='eedb30aa78b5f9e58e907740f31be7afb033e1dde6f8889aaff847b75af64136')
check('exact_MAIN_and_saved_LF',len(main.encode())==12019 and digest(main.encode())=='ecc56322f381f86fec5c3e05cfd9656c8e1c96d932696ef93eab06daf34be019' and (W/'MAIN.html').read_text()==main+'\n')
check('exact_head',len(head.encode())==4762 and digest(head.encode())=='98161f832cfebc3bca6667b6dbbbb152041f390d975f7c99e3b615ac3b0501ab')
page=Text();page.feed(body)
model=json.loads((W/'PAGE_MODEL.json').read_bytes())
schema=json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',body).group(1))
abstract=norm(facts['full_original_abstract_tex'])
visible=plain(re.search(r'<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)</p>',body).group(1))
check('complete_original_abstract_four_surfaces',visible==abstract==schema['abstract']==page.metas['DC.description']==model['full_original_abstract'])
check('Description_and_internal_logs_not_duplicated',facts['native_description_html_distinct_from_abstract'] not in body and not any(t in body for t in ['RENDER_RECEIPT','ROOT_REVIEW','SOURCE_PINS','358 exact','1e−85','11011']))
check('exact_scope_strings',all(t in main for t in ['ordinary positive Euclidean norms','0 &lt; λ &lt; b²','other caustic tangent','immediate retracing is excluded','finite and strictly positive','every admitted period and winding','odd primitive periods','self-intersecting stars','reversal and repetitions','neither individual sum is claimed constant','original orbit polygon','conditional on a regular closed orbit existing']))
check('actual_norm_increment_and_limits',all(t in main for t in ['q<sub>σ</sub> = (a²h<sub>σ</sub> + b²λ/h<sub>σ</sub>)/K','Γ = c/(ab√λ) · (−a² + b²λ/(b² − λ))','No division by u, vertical displacement or Γ occurs','zero-coefficient caustic','changes to −Γ','Hyperbolic caustics, degenerate caustics, two-bounce limits','circular case a = b']))
check('credit_access_priority_limits',all(t in main for t in ['The observation and the antipedal construction are theirs','May 2020','negative-pedal and polarity geometry','known focal sideline-height product','central inversion','final books and author sources','some historical and experimental material was not read','absolute-first, exhaustive-literature or continued-open-status guarantee']))
record=json.loads((S/'record.response.body').read_bytes());nativefiles=json.loads((S/'files-23191247.response.body').read_bytes());versions=json.loads((S/'versions-001.response.body').read_bytes());native=model['native_metadata']
check('native_dates_edition',native['version']==facts['native_declared_version']==record['metadata']['version']=='1.0' and native['publication_date']==facts['publication_date_native']=='2026-10-06' and native['created']==facts['native_created_literal']==record['created'] and native['updated']==facts['native_updated_literal']==record['updated'])
check('native_absence_type_creator',native['is_published']=={'present':False,'original_value':None} and 'is_published' not in record and native['state']==record['state']=='done' and native['creator']==record['metadata']['creators'][0] and native['resource_type']==record['metadata']['resource_type'] and native['record_license']==record['metadata']['license']['id']=='cc-by-4.0')
check('literal_native_file_controls',native['original_custom_file_order']==nativefiles['order']==[] and native['original_default_preview']==nativefiles['default_preview']==None and record['swh']=={} and versions['hits']['hits'][0]['swh']==None)
keys=facts['native_file_order'];downloads=re.findall(r'<li><a href="([^"]+)"',re.search(r'<ol id="native-downloads">([\s\S]*?)</ol>',body).group(1))
check('PDF_then_ZIP_all_surfaces',keys==downloads==[r['key'] for r in nativefiles['entries']]==[r['key'] for r in versions['hits']['hits'][0]['files']]==[r['key'] for r in model['native_assets_in_order']]==[r['name'] for r in schema['encoding']])
for z in model['native_assets_in_order']:
 b=(W/z['path']).read_bytes();original=(S/'assets'/z['key']).read_bytes();check('native_asset:'+z['key'],b==original and len(b)==z['bytes'] and digest(b)==z['SHA256'] and hashlib.md5(b).hexdigest()==z['native_MD5'])
check('reader_and_direct_targets','src="focal_antipedal_sum.pdf#view=FitH"' in body and 'title="Original four-page manuscript:' in body and 'Open the original PDF' in body and 'Download the PDF' in body and all((W/'preview'/k).is_file() for k in keys))
check('faithful_SEO_Bib',schema['version']=='1.0' and schema['datePublished']=='2026-10-06' and page.metas['citation_doi']==record['doi'] and page.metas['citation_publication_date']=='2026/10/06' and all(t in (W/'preview/citation.bib').read_text() for t in ['author = {Kriebel, Alec}','day = {6}','version = {1.0}','doi = {10.5281/zenodo.23191247}']))
check('private_null_authority',page.metas['robots']=='noindex, nofollow, noarchive' and not re.search(r'<link[^>]*rel="canonical"',head) and all(model[k] is None for k in ['canonical_url','base_url','production_url','AA','follow_up']) and model['publication_authority']==False)
check('rights_AI_contribution_collab',all(t in main for t in ['all original authored support files, including authored code','CC BY 4.0','third-party works retain','AI tools were used extensively','unrefereed','not conventional human peer review','actual scholarly contributions']) and not re.search(r'\bMIT\b',body))
check('HTML_ids_fragments',len(page.ids)==len(set(page.ids)) and all(t[1:] in page.ids for t in page.hrefs if t.startswith('#')))
receipt=json.loads((W/'RENDER_RECEIPT.json').read_bytes());execution=json.loads((W/'EXECUTION_RECEIPT.json').read_bytes())
check('literal_render_errors_and_access_limits',receipt['render_invocations']==1 and receipt['inputs_unchanged']==True and all(v['iframeObservation']['accessible']==False for v in receipt['views']) and all(receipt[k]==[] for k in ['remote_page_requests','failed_requests','page_errors','console_errors','cleanup_errors']) and receipt['fatal_exception']==None)
check('retained_streams_single_writer_invocations',(W/'default.stderr.txt').read_bytes()==(W/'render.stderr.txt').read_bytes()==b'' and (W/'render.stdout.txt').read_bytes()==(W/'RENDER_RECEIPT.json').read_bytes() and execution['data_check']['invocations']==execution['offline_HTML_render']['invocations']==1 and execution['data_check']['exit_code']==execution['offline_HTML_render']['exit_code']==0)
failed=[k for k,v in checks.items() if not v]
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'record_id':23191247,'verdict':'NO_GO' if failed else 'PASS','checks':checks,'failures':failed,'writer_FINAL':pin(W/'FINAL.json'),'writer_manifest':pin(W/'OWNED_MANIFEST.json'),'own_script':pin(Path(__file__)),'own_comparison_invocations':1,'source_or_writer_writes':0,'existing_helper_native_science_renderer_imports_or_executions':0,'functions_actually_run':'digest,pin,check,norm,Text HTMLParser methods,plain; standard-library data/hash/path operations only','saved_views_personally_seen':receipt['screenshots'],'limits':['Desktop partial page 1 and thumbnails; mobile blank frame; both accessible-document flags false','No complete-PDF/native/live reader or browser-download certification','Data fidelity and finite custody only, no new scientific proof or priority review']},indent=2))
sys.exit(1 if failed else 0)
