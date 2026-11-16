from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib,json,re,stat,struct,sys
O=Path(__file__).resolve().parent;P=O.parent.parent
T=P/'verification/focal-kato-supercritical-stage-sol-20261116';C=T/'candidate'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com');M=P.parent
checks={};detail={}
def digest(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'SHA256':digest(b),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
def check(k,v):checks[k]=bool(v)
def typed(v):
 if v is None:return ['null']
 if isinstance(v,bool):return ['bool',v]
 if isinstance(v,str):return ['string',v]
 if isinstance(v,int):return ['integer',str(v)]
 if isinstance(v,float):return ['float',repr(v)]
 if isinstance(v,list):return ['array',[typed(x) for x in v]]
 if isinstance(v,dict):return ['object',[[k,typed(x)] for k,x in v.items()]]
 raise ValueError(type(v))
def tj(v):return digest(json.dumps(typed(v),ensure_ascii=False,separators=(',',':')).encode())
class Page(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.meta={};self.links=[];self.refs=[];self.ids=[];self.text=[];self.iframes=[]
 def handle_data(self,s):self.text.append(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='meta':self.meta[a.get('name',a.get('property'))]=a.get('content')
  if tag=='link':self.links.append(a)
  if tag in ['a','link','iframe']:self.refs.append(a.get('href',a.get('src','')))
  if tag=='iframe':self.iframes.append(a)
def plain(s):
 q=Page();q.feed(s);return ' '.join(''.join(q.text).split())
def script(s):return json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',s).group(1))
def mainfrag(s):return re.search(r'<main id="main">[\s\S]*?</main>',s).group(0)
def rawitems(s):
 raw=re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',s).group(1);dec=json.JSONDecoder();i=raw.index('[',raw.index('"itemListElement"'))+1;out=[]
 while True:
  while raw[i].isspace() or raw[i]==',':i+=1
  if raw[i]==']':return out
  value,end=dec.raw_decode(raw,i);out.append(raw[i:end]);i=end
def head(root):
 s=(root/'.git/HEAD').read_text().strip()
 if not s.startswith('ref: '):return s
 ref=s[5:];p=root/'.git'/ref
 if p.is_file():return p.read_text().strip()
 return next(x.split(' ',1)[0] for x in (root/'.git/packed-refs').read_text().splitlines() if x.endswith(' '+ref))
prep=json.loads((O/'PREPARATION_SEAL.json').read_bytes())
check('own_preparation_seal',pin(O/'PREPARATION_SEAL.json')['SHA256']=='65f30a2d5978ce266a7c9adda21717d49a8e60f0c7a62d058c183fcbed7a0500')
check('own_preparation_payloads',all(all(pin(O/z['path'])[k]==z[k] for k in ['bytes','SHA256','mode']) for z in prep['finite_payload']))
check('actual_stage_FINAL_handoff',pin(T/'FINAL.json')['bytes']==12024 and pin(T/'FINAL.json')['SHA256']=='11a3680b7ca11330f5611ece3d58d12fea78c3679b679242ea9f1dba2da41972')
check('actual_stage_manifest_handoff',pin(T/'OWNED_MANIFEST.json')['bytes']==12982 and pin(T/'OWNED_MANIFEST.json')['SHA256']=='94278491e5c497f8692b4d1d93da2687ec07f1dceecf459bc89c0eb7015fd3d2')
check('actual_PUBLIC_PAYLOADS_handoff',pin(T/'PUBLIC_PAYLOADS.json')['bytes']==5806 and pin(T/'PUBLIC_PAYLOADS.json')['SHA256']=='86a5fe4307a934b42db03ee73e5e42e05fbc220cc67106926c4e6a23b0b8faa8')
manifest=json.loads((T/'OWNED_MANIFEST.json').read_bytes());final=json.loads((T/'FINAL.json').read_bytes());payloads=json.loads((T/'PUBLIC_PAYLOADS.json').read_bytes())
paths=list(T.rglob('*'));files={p.relative_to(T).as_posix() for p in paths if p.is_file()};dirs={p.relative_to(T).as_posix() for p in paths if p.is_dir()}
check('finite65_files7_dirs',len(files)==65 and files=={z['path'] for z in manifest['files']}|{'FINAL.json','OWNED_MANIFEST.json'} and dirs==set(manifest['child_directories']) and len(dirs)==7)
check('exact_terminal_controls',manifest['root_controls_excluded_from_own_list']==['OWNED_MANIFEST.json','FINAL.json'])
check('no_stage_symlinks_or_specials',all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in paths))
check('all63_stage_payload_hashes_lengths_modes',all(pin(T/z['path'])['bytes']==z['bytes'] and pin(T/z['path'])['SHA256']==z['SHA256'] and oct(stat.S_IMODE((T/z['path']).stat().st_mode))==z['mode'] for z in manifest['files']))
base=json.loads((O/'BASELINE_PUBLIC_FILES.json').read_bytes());agg=json.loads((O/'BASELINE_AGGREGATES.json').read_bytes());meta=json.loads((O/'BASELINE_GIT_AND_TEMPLATE.json').read_bytes())
actual={p.relative_to(W).as_posix() for p in (W/'public').rglob('*') if p.is_file()};actualdirs={p.relative_to(W).as_posix():format(stat.S_IMODE(p.stat().st_mode),'04o') for p in (W/'public').rglob('*') if p.is_dir()}
check('all699_actual_W_files_unchanged',actual=={z['path'] for z in base['files']} and all(all(pin(W/z['path'])[k]==z[k] for k in ['bytes','SHA256','mode']) for z in base['files']))
check('all356_W_directory_modes_unchanged',actualdirs=={z['path']:z['mode'] for z in base['directories']})
check('W_HEAD_tree_index_unchanged',head(W)==meta['HEAD'] and all(pin(Path(meta['native_Git_index']['path']))[k]==meta['native_Git_index'][k] for k in ['bytes','SHA256','mode']))
indices={}
for root,key in [(W,'W'),(M,'Math')]:
 z=final[key]['index'];p=Path(z['path']);b=p.read_bytes();header=struct.unpack('>4sII',b[:12]);indices[key]={'bytes':len(b),'SHA256':digest(b),'mode':oct(stat.S_IMODE(p.stat().st_mode)),'version':header[1],'records':header[2]}
 check(key+'_native_HEAD_index_header',head(root)==final[key]['HEAD'] and header[0]==b'DIRC' and all(indices[key][k]==z[k] for k in ['bytes','SHA256','mode','version','records']))
check('selected_W_config_guards',all(pin(Path(final['W'][k]['path']))['SHA256']==final['W'][k]['SHA256'] for k in ['git_config','firebase_config']))
inputs=json.loads((T/'BUILD_INPUTS.json').read_bytes())
check('selected27_source_guards_unchanged',len(inputs['source_guards'])==27 and all(pin(Path(z['path']))['bytes']==z['bytes'] and pin(Path(z['path']))['SHA256']==z['SHA256'] and ('mode' not in z or oct(stat.S_IMODE(Path(z['path']).stat().st_mode))==z['mode']) for z in inputs['source_guards']))
adopts=json.loads((O/'ADOPTION_PINS.json').read_bytes())['adoptions']
check('three_actual_root_adoptions_unchanged',all(all(pin(Path(z['pin']['path']))[k]==z['pin'][k] for k in ['bytes','SHA256','mode']) for z in adopts))
cp={p.relative_to(C).as_posix() for p in C.rglob('*') if p.is_file()};declared={z['path'] for z in payloads['candidate_pins']};mods={'public/research/index.html','public/research/sitemap.xml'}
check('exact14_candidate12A2M',len(cp)==14 and cp==declared and cp&actual==mods and len(cp-actual)==12)
check('all14_candidate_payload_pins',all(pin(C/z['path'])['bytes']==z['bytes'] and pin(C/z['path'])['SHA256']==z['SHA256'] and oct(stat.S_IMODE((C/z['path']).stat().st_mode))==z['mode']=='0o644' for z in payloads['candidate_pins']))
check('projected711_public_files',len(actual|cp)==711)
old=(W/'public/research/index.html').read_text();new=(C/'public/research/index.html').read_text();oldj=script(old);newj=script(new);newitems=newj['mainEntity']['itemListElement'];olditems=oldj['mainEntity']['itemListElement'];oldli=re.findall(r'<li>[\s\S]*?</li>',old);newli=re.findall(r'<li>[\s\S]*?</li>',new)
check('frozen_old_aggregates_and_stage_snapshots',digest(old.encode())==agg['index_pin']['SHA256'] and (T/'BASELINE_RESEARCH_INDEX.html').read_bytes()==old.encode() and (T/'BASELINE_SITEMAP.xml').read_bytes()==(W/'public/research/sitemap.xml').read_bytes())
check('all111_ordered_typed_items_preserved',len(newitems)==114 and tj(newitems[:111])==agg['all_ordered_typed_items_SHA256']==tj(olditems) and all(tj(x)==z['ordered_typed_object_SHA256'] for x,z in zip(newitems[:111],agg['ordered_prior_items_and_visible_li'])))
check('all111_raw_JSON_objects_preserved',len(rawitems(new))==114 and rawitems(new)[:111]==rawitems(old))
check('all111_visible_items_preserved',len(newli)==114 and newli[:111]==oldli and all(digest(x.encode())==z['visible_li_SHA256'] for x,z in zip(newli[:111],agg['ordered_prior_items_and_visible_li'])))
check('index_outer_schema_and_count',tj({k:v for k,v in newj.items() if k!='mainEntity'})==tj({k:v for k,v in oldj.items() if k!='mainEntity'}) and list(newj['mainEntity'])==list(oldj['mainEntity']) and type(newj['mainEntity']['numberOfItems']) is int and newj['mainEntity']['numberOfItems']==114 and newj['mainEntity']['@type']==oldj['mainEntity']['@type'])
masked=re.sub(r'(<script type="application/ld\+json">)[\s\S]*?(</script>)',r'\1[SCHEMA]\2',new);masked=re.sub(r'(<ul>)[\s\S]*?(</ul>)',r'\1[ITEMS]\2',masked)
check('index_wrapper_preserved',digest(masked.encode())==agg['index_wrapper_masked_schema_and_list_SHA256'])
sitemap=(C/'public/research/sitemap.xml').read_text();nodes=re.findall(r'<url>[\s\S]*?</url>',sitemap)
check('all112_raw_sitemap_nodes_preserved',len(nodes)==115 and all(digest(x.encode())==z['raw_SHA256'] for x,z in zip(nodes[:112],agg['ordered_prior_sitemap_nodes'])))
check('sitemap_wrapper_preserved',sitemap[:sitemap.index('<url>')]==agg['sitemap_prefix'] and sitemap[sitemap.rindex('</url>')+6:]==agg['sitemap_suffix'])
expected=[(23573603,'supercritical-nonuniqueness-square-lattice',13363,'4e6c8a6ba658262bbce6132f8ae6031a5abc65ab7660e2b533bd96c47a1cf53e','ec82523475a25c370c929368405904bf75e2d49b4fd8b01c011a1ba2cb314393'),(23191247,'focal-antipedal-sum-invariant',12019,'ecc56322f381f86fec5c3e05cfd9656c8e1c96d932696ef93eab06daf34be019','eedb30aa78b5f9e58e907740f31be7afb033e1dde6f8889aaff847b75af64136'),(23444050,'three-summand-kato-kernel-counterexample',11952,'bb58ccd950759a586bcea7ccdbadf714e1814ddeeb1f207c8a46a4ae83dc3832','333c95f7d3c10d9eb14dbe0f7174ca13a65280407f676f3ee065ff2b9334594e')]
articles=[]
for i,(rid,slug,n,h,sourcehash) in enumerate(expected):
 prefix='public/research/'+slug+'/';body=(C/prefix/'index.html').read_text();page=Page();page.feed(body);schema=script(body);main=mainfrag(body);source=(P/f'papers/{rid}/reviews/editorial/preview/index.html').read_text();originalschema=script(source);record=json.loads((P/f'papers/{rid}/sources/record.response.body').read_bytes());nativefiles=json.loads((P/f'papers/{rid}/sources/files-{rid}.response.body').read_bytes());canonical='https://aleckriebel.com/research/'+slug+'/'
 check(str(rid)+':exact_whole_approved_MAIN',digest(source.encode())==sourcehash and len(main.encode())==n and digest(main.encode())==h and main==mainfrag(source))
 visible=plain(re.search(r'<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)</p>',body).group(1))
 check(str(rid)+':whole_abstract_four_surfaces',visible==schema['abstract']==page.meta['DC.description']==originalschema['abstract'])
 exempt=['@id','url','mainEntityOfPage','encoding']
 check(str(rid)+':all_other_schema_fields_unchanged',tj({k:v for k,v in schema.items() if k not in exempt})==tj({k:v for k,v in originalschema.items() if k not in exempt}))
 check(str(rid)+':native_title_date_version_DOI_ORCID',schema['name']==page.meta['citation_title']==record['metadata']['title'] and schema['datePublished']==record['metadata']['publication_date'] and schema['version']==page.meta['citation_version']==record['metadata']['version'] and page.meta['citation_doi']==record['doi'] and page.meta['citation_author_orcid']=='https://orcid.org/0009-0001-9320-500X' and page.meta['citation_publication_date']==schema['datePublished'].replace('-','/'))
 check(str(rid)+':public_canonical_schema_OG',{'rel':'canonical','href':canonical} in page.links and page.meta['og:url']==schema['url']==schema['mainEntityOfPage']['@id']==canonical and schema['@id']==canonical+'#article' and page.meta['robots']=='index, follow, max-image-preview:large')
 check(str(rid)+':current_wrapper_style_nav_footer',{'rel':'stylesheet','href':'/research/research.css'} in page.links and {'rel':'icon','href':'/favicon.ico'} in page.links and '<style' not in body and re.search(r'<header>[\s\S]*?</header>',body).group(0)==meta['shared_article_header_literal'] and re.search(r'<footer>[\s\S]*?</footer>',body).group(0)==meta['shared_article_footer_literal'])
 keys=[z['key'] for z in record['files']];downloads=re.findall(r'<li><a href="([^"]+)"',re.search(r'<ol id="native-downloads">([\s\S]*?)</ol>',body).group(1))
 check(str(rid)+':native_PDF_ZIP_order',keys==downloads==[z['key'] for z in nativefiles['entries']]==[z['name'] for z in schema['encoding']] and len(keys)==2 and keys[0].endswith('.pdf'))
 check(str(rid)+':native_asset_bytes_checksums_encodings',all((C/prefix/z['key']).read_bytes()==(P/f'papers/{rid}/sources/assets'/z['key']).read_bytes() and (C/prefix/z['key']).stat().st_size==z['size'] and 'md5:'+hashlib.md5((C/prefix/z['key']).read_bytes()).hexdigest()==z['checksum'] and schema['encoding'][j]['contentUrl']==canonical+z['key'] and schema['encoding'][j]['sameAs']==z['links']['self'] and schema['encoding'][j]['contentSize']==str(z['size'])+' bytes' for j,z in enumerate(record['files'])))
 check(str(rid)+':PDF_reader_citation_and_Bib',page.meta['citation_pdf_url']==canonical+keys[0] and len(page.iframes)==1 and page.iframes[0]['src']==keys[0]+'#view=FitH' and bool(page.iframes[0].get('title')) and (C/prefix/'citation.bib').read_bytes()==(P/f'papers/{rid}/reviews/editorial/preview/citation.bib').read_bytes())
 missing=[]
 for ref in page.refs:
  if not ref:continue
  u=urlsplit(ref)
  if u.scheme and not(u.scheme in ['http','https'] and u.hostname=='aleckriebel.com'):continue
  if not u.path:
   if u.fragment and u.fragment not in page.ids:missing.append(ref)
   continue
  name='public'+unquote(u.path) if u.path.startswith('/') else prefix+unquote(u.path)
  if name.endswith('/'):name+='index.html'
  if not ((C/name).is_file() or (W/name).is_file()):missing.append(ref)
 check(str(rid)+':all_local_overlay_targets_and_unique_ids',not missing and len(page.ids)==len(set(page.ids)))
 check(str(rid)+':new_index_and_sitemap_identity',newitems[111+i]=={'@type':'ListItem','position':112+i,'url':canonical,'name':record['metadata']['title']} and '/research/'+slug+'/' in newli[111+i] and record['metadata']['title'] in plain(newli[111+i]) and '<loc>'+canonical+'</loc><lastmod>2026-11-16</lastmod>' in nodes[112+i])
 articles.append({'record':rid,'slug':slug,'MAIN_bytes':n,'MAIN_SHA256':h,'candidate_HTML':pin(C/prefix/'index.html'),'local_target_failures':missing})
render=json.loads((T/'RENDER_RESULT.json').read_bytes());build=json.loads((T/'BUILD_EXECUTION.json').read_bytes());rex=json.loads((T/'RENDER_EXECUTION.json').read_bytes());legacy=json.loads((T/'LEGACY_SEARCH.stdout.json').read_bytes());lex=json.loads((T/'LEGACY_EXECUTION.json').read_bytes())
check('literal_render_receipts_no_error_upgrade',build['exit']==rex['exit']==0 and rex['invocations']==1 and all(render[k]==[] for k in ['blockedExternalHTTP','missingOverlayPaths','consoleErrors','pageErrors','requestFailures']) and len(render['views'])==6 and all(v['viewport']==v['documentWidth'] for v in render['views']) and render['downloadClicks']==0 and render['liveReaderOrDownloadCertification']==False)
check('literal_success_streams_empty_stderr',all((T/name).read_bytes()==b'' for name in ['BUILD.stderr.txt','RENDER.stderr.txt','LEGACY_SEARCH.stderr.txt']) and (T/'RENDER.stdout.json').read_bytes()==(T/'RENDER_RESULT.json').read_bytes())
check('legacy_exact47_scope_and_preserved_failures',legacy['HTML_count']==len(legacy['rows'])==47 and legacy['whole_HTML_bytes']==sum(z['bytes'] for z in legacy['rows'])==612221 and legacy['hits']==[] and legacy['docs_tree']=='e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0' and lex['prior_exits']==[1,1] and lex['exit']==0 and (T/'FIRST_LEGACY_SEARCH.stderr.txt').stat().st_size==741 and (T/'SECOND_LEGACY_SEARCH.stderr.txt').stat().st_size==858)
failures=[k for k,v in checks.items() if not v]
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'verdict':'NO_GO' if failures else 'PASS','scope':'One independent bounded read-only private-stage data/copy/custody comparison','checks':checks,'failures':failures,'candidate_files':sorted(cp),'counts_before':[699,111,112],'projected_counts':[711,114,115],'articles':articles,'native_indices':indices,'own_script':pin(Path(__file__)),'own_invocations':1,'stage_helpers_renderers_legacy_queries_native_science_executions':0,'writes_outside_owned_audit':0,'functions_actually_run':'digest,pin,check,typed,tj,Page HTMLParser methods,plain,script,mainfrag,rawitems,head; standard-library data/hash/stat/URL/index-header operations only','legacy_limit':'Static exact47-body result/receipts read, not rerun or global-absence certification','saved_views_personally_seen':6,'limits':['Stage desktop captures partial first PDF pages only; mobile screenshots show result sections, not PDF surfaces','No full/native/mobile/live reader, clicked open/download, external link or production serving certification','No installation, publication, redirect, Sheet or AA authority']},indent=2))
sys.exit(1 if failures else 0)
