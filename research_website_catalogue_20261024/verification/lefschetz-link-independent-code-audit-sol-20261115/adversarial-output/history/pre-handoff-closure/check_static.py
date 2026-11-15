"""Independent static output check; stdlib only. No stage/source/owner imports,
scientific execution, rendering, network, subprocess, bytecode or writes.
Parent fixed expectations and held baseline are read before actual outputs.
"""
from pathlib import Path,PurePosixPath
from hashlib import sha256
from html.parser import HTMLParser
from html import unescape
import json,re
HERE=Path(__file__).resolve().parent;A=HERE.parent;S=A.parent/'lefschetz-link-private-stage-sol-20261115'
checks=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise ValueError(label)
def read(p):
 need(p.is_file() and not p.is_symlink(),'regular nonlink '+str(p));return p.read_bytes()
def obj(p):return json.loads(read(p))
def binding(b):return {'bytes':len(b),'SHA256':sha256(b).hexdigest()}
def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def ld(t):
 found=list(re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',t,re.S));need(len(found)==1,'one JSONLD script');return found[0],json.loads(found[0][1])
def namespace(p):
 allp=list(p.rglob('*'));need(not any(q.is_symlink() for q in allp),'no namespace links');return sorted(str(q.relative_to(p)) for q in allp if q.is_file())
class Head(HTMLParser):
 def __init__(self):super().__init__();self.meta={};self.links=[];self.title='';self.intitle=False
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='meta':
   k=a.get('name',a.get('property','charset'));need(k not in self.meta,'unique metadata '+k);self.meta[k]=a.get('content',a.get('charset'))
  if t=='link':self.links.append(a)
  if t=='title':self.intitle=True
 def handle_endtag(self,t):
  if t=='title':self.intitle=False
 def handle_data(self,t):
  if self.intitle:self.title+=t
# Validate fixed parent boundaries before using any expected value.
need(binding(read(A/'INITIAL_SEAL.json'))['SHA256']=='b8c8a28283a56d5108d351952fb5171043811888e17c52522e6457e4a0e3c44e','parent independent initialseal pin')
for sealname,mname in [('INITIAL_SEAL.json','INITIAL_MANIFEST.json'),('BASELINE_SEAL.json','BASELINE_MANIFEST.json')]:
 seal=obj(A/sealname);manifest=obj(A/mname);need(binding(read(A/mname))==seal['manifest'],'parent whole manifest seal')
 for p,b in manifest['payloads'].items():need(binding(read(A/p))==b,'whole independent held input payload')
E=obj(A/'EXPECTED_OUTPUTS.json');B=obj(A/'BASELINE.json');C=obj(A/'WHOLE_NATIVE_AND_EDITORIAL_CONTRACT.json')
need(E['derivation']['overlay_paths']==11 and B['actual_counts']==[605,90,91],'independent 11/60590/91 requirements')
need(binding(read(S/'FINAL_SEAL.json'))['SHA256']=='b42073395a01c7a60c733627212df7d56f484023662119a215a8b6cb57b89575','exact writer finalseal')
buffers={}
for name in ['candidate-a','candidate-b']:
 p=S/name/'public';need(namespace(p)==E['exact_overlay_paths'],'complete actual11 namespace '+name)
 got={q:read(p/q) for q in E['exact_overlay_paths']}
 if not buffers:buffers=got
 else:
  for q,v in got.items():need(v==buffers[q],'whole actual normal/-O rendered buffer identity '+q)
# These are recorded renderer receipts, not replayed rendering or optimized checker tests.
ledger=obj(S/'EXECUTION_LEDGER.json');receiptrows=[]
for prefix,opt,candidate in [('BUILD_NORMAL',0,'candidate-a'),('BUILD_OPTIMIZED',1,'candidate-b')]:
 r=next(q for q in ledger['runs'] if q['name']==prefix);out=read(S/r['stdout']);err=read(S/r['stderr']);d=json.loads(out)
 need(r['exit_code']==0 and r['stderr_bytes']==0 and err==b'','actual renderer exit0 empty stderr '+prefix)
 need(len(out)==r['stdout_bytes'] and sha256(out).hexdigest()==r['stdout_SHA256'],'whole actual stdout receipt identity')
 need(d['optimization_level']==opt and d['candidate']==candidate and d['actual_all_eleven_buffers_written'] is True,'actual render optimization and all11 writing')
 need(('-O' in r['command_arguments'])==(opt==1) and 'render_stage.py' in r['command_arguments'],'recorded actual render invocation')
 receiptrows.append({'name':prefix,'actual_exit_code':r['exit_code'],'optimization_level':opt,'stdout':binding(out),'stderr':binding(err)})
article_results=[]
for i,(expect,rec) in enumerate(zip(E['records'],C['records'])):
 base='research/'+expect['slug']+'/';url=expect['canonical_proposal'];text=buffers[base+'index.html'].decode();pub=rec['publication_config_whole_literal']
 mains=re.findall(r'<main\b[^>]*>.*?</main>',text,re.S);need(len(mains)==text.count('<main')==text.count('</main>')==1,'one actual whole main')
 main=mains[0];need(main==rec['expected_main_with_only_missing_id'] and binding(main.encode())==expect['main_expected_binding'],'complete approved main preserved onlymissingid')
 need(main.startswith('<main id="main">') and 'href="#main"' in text,'skip target exists')
 h=Head();h.feed(text.split('</head>',1)[0]);need(h.title==pub['title']+' | Alec Kriebel','actual browser title')
 meta={'description':pub['description'],'author':'Alec Kriebel','robots':'index,follow','citation_title':pub['title'],'citation_author':'Alec Kriebel','citation_author_orcid':'https://orcid.org/0009-0001-9320-500X','citation_publication_date':pub['publication_date'].replace('-','/'),'citation_version':pub['version'],'citation_doi':pub['doi'],'citation_pdf_url':url+'assets/'+pub['pdf_filename'],'citation_language':'en','og:type':'article','og:title':pub['title'],'og:description':pub['description'],'og:url':url,'og:site_name':'Alec Kriebel','article:published_time':pub['publication_date']}
 for k,v in meta.items():need(h.meta.get(k)==v,'accurate '+rec['record_id']+' metadata '+k)
 for rel,href in [('canonical',url),('icon','/favicon.ico'),('stylesheet','/research/research.css')]:need(len([l for l in h.links if l.get('rel')==rel and l.get('href')==href])==1,'existing wrapper '+rel)
 need('noindex' not in text and text.count('<script')==1,'indexable no executable script')
 abstract=re.findall(r'<h2>Original abstract</h2>\s*<p>(.*?)</p>',main,re.S);need(len(abstract)==1 and unescape(abstract[0])==expect['whole_original_abstract'],'whole original visible abstract')
 _,g=ld(text);need(g.get('@context')=='https://schema.org' and len(g.get('@graph',[]))==2,'two node scholarly graph')
 page,article=g['@graph'];need(page['@type']=='WebPage' and article['@type']=='ScholarlyArticle','accurate graph types')
 need(page['@id']==url+'#page' and article['@id']==url+'#article' and page['mainEntity']=={'@id':article['@id']} and article['mainEntityOfPage']=={'@id':page['@id']},'mutually linked page/article identity')
 need(page['dateCreated']==page['dateModified']=='2026-11-15' and article['datePublished']==expect['datePublished'],'original dates separate build dates')
 need(article['abstract']==expect['whole_original_abstract'] and article['version']==expect['native_version'],'whole scholarly abstract/nativeversion')
 for k,v in rec['original_full_scholarly_object'].items():
  if k not in {'@id','url','mainEntityOfPage','inLanguage','isAccessibleForFree','encoding'}:need(k in article and same(v,article[k]),'whole preserved original scholarly field '+k)
 need(article['license']=='https://creativecommons.org/licenses/by/4.0/','article actual CC BY')
 encoding=article['encoding'];need(len(encoding)==len(expect['native_order'])==2+i,'native encoding scope includes standalone TeX')
 for enc,asset,name in zip(encoding,rec['native_assets_in_literal_order'],expect['native_order']):
  need(enc['contentUrl']==url+'assets/'+name and enc['sameAs']=='https://zenodo.org/api/records/'+rec['record_id']+'/files/'+name+'/content','native encoding literalorder/local/original URLs')
  need(enc['encodingFormat']=={'.zip':'application/zip','.pdf':'application/pdf','.tex':'application/x-tex'}[PurePosixPath(name).suffix],'native MIME type')
  if i==0 and name.endswith('.zip'):need('license' not in enc,'mixed127ZIP blanket encodinglicense absent')
  else:need(enc.get('license')=='https://creativecommons.org/licenses/by/4.0/','actual native asset CC BY grant')
  need(binding(buffers[base+'assets/'+name])==asset['binding'],'complete unchanged native bytes '+name)
 need(binding(buffers[base+'assets/citation.bib'])==rec['BibTeX']['binding'],'whole original BibTeX bytes')
 for local in re.findall(r'(?:href|src)="(assets/[^"#]+)(?:#[^"]*)?"',text):need(base+unescape(local) in buffers,'actual assets link resolves '+local)
 ids=re.findall(r'\bid="([^"]+)"',text);need(len(ids)==len(set(ids)),'unique HTML ids')
 frames=re.findall(r'<iframe\b[^>]*>',main);need(frames==[expect['actual_candidate_iframe_tag']],'whole actual reader attributes preserved')
 css=re.findall(r'<style>(.*?)</style>',text,re.S);need(len(css)==1,'one bounded supplement stylesheet')
 need(not re.search(r'display\s*:\s*none|visibility|opacity|position|overflow\s*:\s*hidden|font-size',css[0]),'no hiding/clipping/math-font CSS')
 need('main p,main li,main td,main th{overflow-wrap:anywhere}' in css[0] and 'main iframe{display:block;width:100%;height:80vh;min-height:500px;' in css[0],'wrapping and responsive reader supplement')
 need('<footer>' in text.split('</main>',1)[1] and 'Research home' in text and '© 2013–2026 Kriebel LLC.' in text,'simple existing footer')
 if i==0:need('Width one is a separate case' in main and '𝔽ₚ(t)' in main and 'MIT licensed' in main,'127 boundary/fixedfield/actualsoftware rights')
 else:need('prints no version number; 1.0 is the Zenodo version.' in main and 'including split links' in main and 'ordinary, uncompleted' in main and 'does not decide its radical/vanishing-ideal question' in main,'128 edition/split/uncompleted/indexedideal qualification')
 article_results.append({'record_id':rec['record_id'],'whole_main':binding(main.encode()),'native_order':expect['native_order'],'native_and_Bib_leaves':3+i,'native_version':expect['native_version'],'printed_version':expect['printed_version']})
# Full independent old-byte restoration; no writer addition string is used.
oldindex=read(A/'baseline/index.html').decode();index=buffers['research/index.html'].decode();om,oldschema=ld(oldindex);nm,newschema=ld(index)
items=newschema['mainEntity']['itemListElement'];need(type(newschema['mainEntity']['numberOfItems']) is int and newschema['mainEntity']['numberOfItems']==len(items)==92,'actual92index')
need(same(items[:90],B['old90typedorderedItemList']),'all90whole typed/key/list/order oldItemLists')
lis=re.findall(r'<li>.*?</li>',index,re.S);need(len(lis)==92 and lis[:90]==B['old90visible_li_bytes'],'all90visible oldentrybytes')
restored=index
for number,(rec,li) in enumerate(zip(C['records'],lis[90:]),91):
 need(same(items[number-1],{'@type':'ListItem','position':number,'url':rec['canonical_proposal'],'name':rec['title']}),'new exact index identity')
 need(rec['description'] in unescape(li) and '/research/'+rec['slug']+'/' in li,'new visible index title/description/link')
 restored,n=re.subn(r'(?m)^ *'+re.escape(li)+r'\n','',restored,count=1);need(n==1,'one independent removable new li')
rm,_=ld(restored);need(restored[:rm.start(1)]+om[1]+restored[rm.end(1):]==oldindex,'whole old index byteexact restoration')
oldsm=read(A/'baseline/sitemap.xml').decode();sm=buffers['research/sitemap.xml'].decode();nodes=re.findall(r'<url>.*?</url>',sm,re.S)
need(len(nodes)==93 and nodes[:91]==B['old91wholeXMLnodebytes'],'all91whole XMLnodebytes/date/order')
restored=sm
for rec,node in zip(C['records'],nodes[91:]):
 need(node=='<url><loc>'+rec['canonical_proposal']+'</loc><lastmod>2026-11-15</lastmod></url>','new sitemap node correct')
 restored,n=re.subn(r'(?m)^ *'+re.escape(node)+r'\n','',restored,count=1);need(n==1,'one independently removable new XMLnode')
need(restored==oldsm,'whole old sitemap exact byte restoration')
basepaths={str(Path(r['original']).relative_to(Path(B['website_root'])/'public')) for r in B['public_files']}
need(len(basepaths)==605 and len(basepaths|set(buffers))==614 and basepaths&set(buffers)=={'research/index.html','research/sitemap.xml'} and len(basepaths-set(buffers))==603,'614union with9newleaves/2aggregate replacements/603nonaggregates')
css=read(A/'baseline/research.css').decode();need('Arial' in css and ('#fff' in css or 'white' in css),'shared held white Arial stylesheet')
print(json.dumps({'scope':'independent adversarial static output support','checks':checks,'material_static_output_defects':[],'whole_paired_normal_optimized_buffers':11,'actual_renderer_receipts':receiptrows,'articles':article_results,'old_typed_and_visible_entries_preserved':90,'old_whole_XMLnodes_preserved':91,'old_index_and_sitemap_entire_byte_restoration':True,'virtual_counts':[614,92,93],'native_assets':5,'BibTeX_assets':2,'no_stage_source_owner_science_import_execution_rendering_network_subprocess_or_writes':True,'browser_or_live_verified':False,'publication_authority':False,'canonical_url':None,'AA':None,'follow_up':None},ensure_ascii=False,indent=2))
