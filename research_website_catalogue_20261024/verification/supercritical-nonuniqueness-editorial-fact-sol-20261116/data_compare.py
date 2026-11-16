"""One bounded standard-library data/copy/custody comparison; no helper execution."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime,timezone
import hashlib,json,re,stat,sys
O=Path(__file__).resolve().parent
P=O.parent.parent
W=P/'papers/23573603/reviews/editorial'
S=P/'papers/23573603/sources'
checks={}
def digest(b):return hashlib.sha256(b).hexdigest()
def check(name,ok):checks[name]=bool(ok)
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':digest(b)}
def norm(s):return ' '.join(s.split())
class Text(HTMLParser):
 def __init__(self):super().__init__();self.data=[];self.metas={};self.ids=[];self.hrefs=[]
 def handle_data(self,s):self.data.append(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if 'href' in a:self.hrefs.append(a['href'])
  if tag=='meta' and 'name' in a:self.metas[a['name']]=a.get('content')
def plain(s):
 p=Text();p.feed(s);return norm(''.join(p.data))
facts=json.loads((O/'SOURCE_FACTS.json').read_bytes())
initial=json.loads((O/'INITIAL_SEAL.json').read_bytes())
check('own_initial_seal_pin',digest((O/'INITIAL_SEAL.json').read_bytes())=='cbd7cbbe4abbc05f22730e61e4983809ed3ec8940703f9b2fcdf89da63d5e015')
for z in initial['finite_payload']:
 b=(O/z['path']).read_bytes();check('own_initial:'+z['path'],len(b)==z['bytes'] and digest(b)==z['sha256'])
final=json.loads((W/'FINAL.json').read_bytes());manifest=json.loads((W/'OWNED_MANIFEST.json').read_bytes())
check('actual_handoff_FINAL_pin',pin(W/'FINAL.json')['sha256']=='dd7971395d3c925ca9da6ff52d46c971b0416c5b8073fa9e62827942e3daa794' and (W/'FINAL.json').stat().st_size==5686)
check('actual_handoff_manifest_pin',pin(W/'OWNED_MANIFEST.json')['sha256']=='3e50b468e0e24e278a2b474004b2dc88a73d152dc16ca6cede7b0b658ded37ac' and (W/'OWNED_MANIFEST.json').stat().st_size==6072)
actual_files={p.relative_to(W).as_posix() for p in W.rglob('*') if p.is_file()}
actual_dirs={p.relative_to(W).as_posix() for p in W.rglob('*') if p.is_dir()}
check('finite_writer_file_set',actual_files=={z['path'] for z in manifest['files']}|{'OWNED_MANIFEST.json','FINAL.json'} and len(actual_files)==32)
check('finite_writer_directory_set',actual_dirs==set(manifest['child_directories'])=={'preview','renders'})
check('no_writer_symlinks',not any(p.is_symlink() for p in W.rglob('*')))
check('exact_writer_terminal_controls',manifest['terminal_controls']==['OWNED_MANIFEST.json','FINAL.json'])
for z in manifest['files']:
 p=W/z['path'];b=p.read_bytes();check('writer_payload:'+z['path'],len(b)==z['bytes'] and digest(b)==z['SHA256'] and format(stat.S_IMODE(p.stat().st_mode),'04o')==z['mode'])
body=(W/'preview/index.html').read_text();main=re.findall(r'<main id="main">[\s\S]*?</main>',body);head=re.findall(r'<head>[\s\S]*?</head>',body)
check('whole_MAIN_head_unique',len(main)==len(head)==1)
main=main[0];head=head[0]
check('whole_HTML_pin',len(body.encode())==19247 and digest(body.encode())=='ec82523475a25c370c929368405904bf75e2d49b4fd8b01c011a1ba2cb314393')
check('exact_MAIN_fragment',len(main.encode())==13363 and digest(main.encode())=='4e6c8a6ba658262bbce6132f8ae6031a5abc65ab7660e2b533bd96c47a1cf53e' and (W/'MAIN.html').read_text()==main+'\n')
check('exact_head_fragment',len(head.encode())==5480 and digest(head.encode())=='985ca9cb83627b853532800bafaaa28f131fb78e4d358a4875fb02a71b143f1b')
page=Text();page.feed(body)
model=json.loads((W/'PAGE_MODEL.json').read_bytes())
schema=json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',body).group(1))
abstract=norm(facts['full_original_abstract_tex'].replace('$',''))
visible=plain(re.search(r'<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)</p>',body).group(1))
check('whole_original_abstract_visible',visible==abstract)
check('whole_original_abstract_schema_DC_model',schema['abstract']==page.metas['DC.description']==model['full_original_abstract']==abstract)
check('native_Description_not_duplicated',facts['native_description_html_distinct_from_abstract'] not in body and all(x not in body for x in ['2048','4392','2116','RENDER_RECEIPT','ROOT_REVIEW','SOURCE_PINS']))
check('fixed_p_exact_quantitative_claim',all(x in main for x in ['19/20','9/10','2200741829/6461571200','143/245','27/107648','C = 100','99 new internal vertices','positive-probability nonuniqueness at one fixed parameter']))
check('declared_quantifier_near_one_limits',all(x in main for x in ['explicitly declared interpretation','each fixed p','sufficiently near one','not almost-sure multiplicity','simultaneous-in-p','critical nonuniqueness']))
native=model['native_metadata'];record=json.loads((S/'record.response.body').read_bytes())
check('native_edition_date_creation',native['version']==facts['native_declared_version']=='1.0.0' and native['publication_date']==facts['publication_date_native']=='2026-10-22' and native['created']==facts['native_created_literal'])
check('native_absence_order_type',native['is_published']=={'present':False,'original_value':None} and 'is_published' not in record and native['state']==record['state']=='done' and native['resource_type']==record['metadata']['resource_type'] and native['original_custom_file_order']==facts['files_endpoint_order_literal']==[])
check('native_creator',native['creator']==record['metadata']['creators'][0])
keys=facts['native_file_order'];downloads=re.findall(r'<li><a href="([^"]+)"',re.search(r'<ol id="native-downloads">([\s\S]*?)</ol>',body).group(1))
check('asset_order_all_surfaces',downloads==keys==[x['key'] for x in model['native_assets_in_order']]==[x['name'] for x in schema['encoding']])
for row in model['native_assets_in_order']:
 b=(W/row['path']).read_bytes();original=(S/'assets'/row['key']).read_bytes()
 check('native_asset:'+row['key'],b==original and len(b)==row['bytes'] and digest(b)==row['SHA256'] and hashlib.md5(b).hexdigest()==row['native_MD5'])
check('reader_title_embed_direct_links','src="supercritical-nonuniqueness.pdf#view=FitH"' in body and 'title="Original five-page manuscript:' in body and 'Open the original PDF' in body and 'Download the PDF' in body)
check('native_DOI_date_version_SEO',schema['version']=='1.0.0' and schema['datePublished']=='2026-10-22' and page.metas['citation_doi']==facts['doi'] and page.metas['citation_publication_date']=='2026/10/22')
check('private_nulls_no_canonical',page.metas['robots']=='noindex, nofollow, noarchive' and not re.search(r'<link[^>]*rel="canonical"',head) and all(model[k] is None for k in ['canonical_url','base_url','production_url','AA','follow_up']) and model['publication_authority'] is False)
check('rights_AI_and_collaboration',all(x in main for x in ['CC BY 4.0','MIT licensed','Third-party works retain','not assigned one blanket license','AI tools were used extensively','unrefereed preprint','Internal AI reviews do not supply','authorship would reflect actual scholarly contributions']))
bib=(W/'preview/citation.bib').read_text()
check('Bib_native_metadata',all(x in bib for x in ['author = {Kriebel, Alec}','year = {2026}','day = {22}','version = {1.0.0}','doi = {10.5281/zenodo.23573603}']))
receipt=json.loads((W/'RENDER_RECEIPT.json').read_bytes());execution=json.loads((W/'EXECUTION_RECEIPT.json').read_bytes())
check('saved_render_literal_limits',receipt['render_invocations']==1 and all(v['iframeObservation']['accessible'] is False for v in receipt['views']) and all(receipt[k]==[] for k in ['remote_page_requests','failed_requests','page_errors','console_errors','cleanup_errors']) and receipt['fatal_exception'] is None)
check('literal_streams_and_single_writer_receipts',(W/'default.stderr.txt').read_bytes()==(W/'render.stderr.txt').read_bytes()==b'' and (W/'render.stdout.txt').read_bytes()==(W/'RENDER_RECEIPT.json').read_bytes() and execution['data_check']['invocations']==execution['offline_HTML_render']['invocations']==1 and execution['data_check']['exit_code']==execution['offline_HTML_render']['exit_code']==0)
failures=[k for k,v in checks.items() if not v]
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'record_id':23573603,'verdict':'PASS' if not failures else 'NO_GO','comparison_kind':'One bounded data-only source/copy/finite-custody comparison after complete personal copy/helper reading and six saved views','checks':checks,'failures':failures,'writer_FINAL':pin(W/'FINAL.json'),'writer_manifest':pin(W/'OWNED_MANIFEST.json'),'own_script':pin(Path(__file__)),'source_or_writer_writes':0,'helper_native_science_renderer_imports_or_executions':0,'functions_actually_run':'digest,pin,check,norm,Text HTMLParser methods,plain; standard JSON/re/stat/path data operations only','saved_views_personally_seen':receipt['screenshots'],'limits':['No native/live PDF reading or download behavior certificate','Mobile frame blank; desktop viewer/title portion only; both accessible-document observations false','Finite data checks do not reverify mathematics or historical priority']},indent=2))
sys.exit(1 if failures else 0)
