#!/usr/bin/env python3
"""One bounded offline data-only editorial comparison; stdout only, no writes.
No project imports, subprocesses, network, rendering or scientific execution.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import hashlib, json, re, stat
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O=P/'verification/fixed-area-editorial-fact-sol-20261116'
E=P/'papers/23443039/reviews/editorial'
def need(ok,why):
    if not ok: raise ValueError(why)
def read(p):
    need(not any(q.is_symlink() for q in [p,*p.parents]),'no symlink input')
    need(stat.S_ISREG(p.lstat().st_mode),'regular data input')
    return p.read_bytes()
def pin(b): return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def bound(p,size,digest):
    b=read(p);need(pin(b)=={'bytes':size,'SHA256':digest},'exact bound '+str(p));return b
class Parse(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=True);self.tags=[];self.data=[];self.meta={};self.feed(s)
    def handle_starttag(self,t,attrs):
        a=dict(attrs);self.tags.append((t,a))
        if t=='meta' and ('name'in a or 'property'in a):
            key=a.get('name',a.get('property'));need(key not in self.meta,'unique meta key');self.meta[key]=a.get('content')
    def handle_data(self,s):self.data.append(s)
def text(s):return ''.join(Parse(s).data)
def norm(s):return re.sub(r'\s+',' ',s).strip()
initial=json.loads(bound(O/'INITIAL.json',15904,'1ecf2b62bd4a25385cc7dd7f28f121b010b9b0faa4345985df2c5765abd0fb28'))
for a in initial['source_pins']:bound(P/a['path'],a['bytes'],a['SHA256'])
clear=json.loads(bound(P/'verification/root-clearance-23443039-20261116.json',2210,'4754afec4d9e0823d1a4304c1fe89f6da66df357f6e485be6300f858a2bbf697'))
bound(P/'papers/23443039/reviews/root/ROOT_REVIEW.md',7098,'2c00bf86d5eae3ff5a88960d51602a04dbec4d59f2d1e124b901ec020bba4b39')
need(clear['status']=='ROOT_FULL_ORIGINAL_SCIENTIFIC_PASS' and clear['original_claim_preserved'] and not clear['repair_or_narrowing'] and clear['defect_or_unresolved_gap']is None,'actual full original clearance')
final=json.loads(bound(E/'FINAL.json',1642,'e5dcaa48435a11180a27d5412996f680ee735fd94306510a6f1a5af501a2f680'))
manifest=json.loads(bound(E/'OWNED_MANIFEST.json',5089,'a1963d862970a56948a10eeffdb510ecacc440afe8904bea0380c36a0b4efaf9'))
need(set(manifest['only_exact_already_existing_root_controls_excluded'])=={'OWNED_MANIFEST.json','FINAL.json'},'two exact writer terminals')
expected={a['path']for a in manifest['files']}|{'OWNED_MANIFEST.json','FINAL.json'}
for a in manifest['files']:bound(E/a['path'],a['bytes'],a['SHA256'])
nodes=list(E.rglob('*'));need(not any(q.is_symlink()for q in nodes),'no writer symlink')
need({q.relative_to(E).as_posix()for q in nodes if q.is_file()}==expected and len(expected)==32,'whole writer32file namespace')
dirs={'.'}|{q.relative_to(E).as_posix()for q in nodes if q.is_dir()}
need(dirs==set(manifest['directories']) and len(dirs)==4,'writer3childdirs')
raw=read(E/'preview/index.html');page=raw.decode();model=json.loads(read(E/'PAGE_MODEL.json'));bib=read(E/'preview/citation.bib').decode()
main=re.search(rb'<main\b.*?</main>',raw,re.S)[0]
need(pin(main)=={'bytes':11768,'SHA256':'5727bbbb241bd027a62d93b91c4ee91b0d7aa1a4df9793fc54ca94115d6e0f5e'}==final['whole_MAIN']==model['whole_MAIN'],'whole MAIN pin')
head_match=re.search(rb'<head>(.*?)</head>',raw,re.S)
head_variants={'including_head_tags':head_match[0],'inside_head_tags':head_match[1]}
head_style=next((k for k,b in head_variants.items()if pin(b)==final['whole_head']),None)
need(head_style is not None and final['whole_head']==model['whole_head'],'whole actual head pin')
need(pin(raw)==final['whole_page']==model['whole_page'] and pin(read(E/'PAGE_MODEL.json'))==final['page_model'] and pin(read(E/'preview/citation.bib'))==final['BibTeX'],'whole page/model/Bib pins')
record=json.loads(read(P/'papers/23443039/sources/record.response.body'));files_response=json.loads(read(P/'papers/23443039/sources/files-23443039.response.body'))
need(model['native_metadata']==record['metadata']==initial['native_metadata'],'whole original native metadata')
need(model['native_record_files']==record['files'] and model['native_files_response']==files_response,'whole original file objects and response')
for field in ('created','modified','updated'):need(model['native_'+field]==record[field],'original native timestamp')
need(model['native_record_status']==record['status'] and model['native_state']==record['state'] and not model['native_is_published']['present'] and 'is_published'not in record,'native state without invented boolean')
desc=re.search(r'<div id="native-description">(.*?)</div>',page,re.S)[1]
paragraphs=re.findall(r'<p>.*?</p>',desc,re.S)
need(desc==record['metadata']['description'] and paragraphs==initial['native_Description_five_paragraphs'] and len(paragraphs)==5,'all five distinct native Description paragraphs exact')
section=re.search(r'<section id="original-abstract"[^>]*>(.*?)</section>',page,re.S)[1]
abstract_paragraphs=re.findall(r'<p(?: [^>]*)?>(.*?)</p>',section,re.S)
need(len(abstract_paragraphs)==3,'complete three-part visible abstract')
tex=read(P/'papers/23443039/sources/published-source/container-001/tree/main.tex').decode();tex_abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S)[1]
tail=tex_abstract.split('\\]',1)[1].replace('~',' ').replace('--','–')
need(norm(text(abstract_paragraphs[2]))==norm(tail),'entire source abstract prose tail exact modulo TeX typography')
need(norm(text(abstract_paragraphs[0]))=='For every finite positive sum g(z)=∑jλj(z−zj)−2 with ∑jλj=1, we construct a compact set S(g) of area exactly π such that','source abstract hypotheses and fixed set')
need(re.sub(r'\s','',text(abstract_paragraphs[1]))=='∫{|z|<R}∖S(g)|g(z)|dA≤2πlogR+π(log2+e−1)(R>1).','complete original abstract formula')
parsed=Parse(page);meta=parsed.meta;ids=[a['id']for t,a in parsed.tags if'id'in a]
need(len(ids)==len(set(ids)) and sum(t=='h1'for t,a in parsed.tags)==1 and[a.get('id')for t,a in parsed.tags if t=='main']==['main'],'unique IDs/main/H1')
article=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',page,re.S)[1]);native=record['metadata']
need(meta['citation_title']==native['title']==article['name'] and meta['citation_publication_date']=='2026/10/17' and meta['citation_date']=='2026/10/17' and article['datePublished']=='2026-10-17','original title/date')
need(meta['citation_version']==article['version']==model['printed_version']==native['version']=='1.0.0' and model['printed_date']=='17 October 2026','original printed/native version/date')
need(meta['citation_doi']==native['doi']==article['identifier']['value'] and meta['citation_author_orcid']==article['author']['identifier']=='https://orcid.org/0009-0001-9320-500X','DOI/ORCID')
need(article['creativeWorkStatus']=='Unrefereed preprint' and article['license']=='https://creativecommons.org/licenses/by/4.0/','status/rights metadata')
need(meta['robots']=='noindex, nofollow, noarchive' and not any(t=='link'and a.get('rel')=='canonical'for t,a in parsed.tags),'intentional private head')
for k in ('canonical_url','base_url','production_url','AA','follow_up'):need(model[k]is None,'private unset '+k)
need(model['publication_authority']is False and final['publication_authority']is False and clear['publication_authority']is False,'private source/editorial only')
names=[a['key']for a in record['files']];need([a['name']for a in article['encoding']]==names and[a['original_file_object']for a in model['native_assets']]==record['files'],'native asset order/objects')
asset_checks=[]
for a,m in zip(record['files'],model['native_assets']):
    original=read(P/'papers/23443039/sources/assets'/a['key']);copy=read(E/m['path']);need(original==copy and pin(copy)=={k:m[k]for k in ('bytes','SHA256')} and 'md5:'+hashlib.md5(copy).hexdigest()==a['checksum'],'whole original asset')
    asset_checks.append({'name':a['key'],**pin(copy),'native_MD5':a['checksum']})
download_list=re.search(r'<ol id="native-downloads">(.*?)</ol>',page,re.S)[1];need([a['href']for t,a in Parse(download_list).tags if t=='a'and'download'in a]==names,'visible native download order')
need(meta['citation_pdf_url']==names[1] and[a['src']for t,a in parsed.tags if t=='iframe']==[names[1]+'#view=FitH'],'local unchanged PDF citation/embed')
for t,a in parsed.tags:
    for k in ('href','src'):
        if k not in a:continue
        u=urlsplit(a[k])
        if u.scheme or u.netloc or u.path.startswith('/'):continue
        need('..'not in Path(u.path).parts,'no local traversal')
        if u.path:need((E/'preview'/u.path).is_file(),'local link exists')
        if not u.path and u.fragment:need(u.fragment in ids,'local fragment exists')
for key,value in [('author','Kriebel, Alec'),('title',native['title']),('year','2026'),('month','oct'),('doi',native['doi']),('version','1.0.0'),('license','CC-BY-4.0')]:need(re.search(r'\b'+key+r'\s*=\s*(?:\{'+re.escape(value)+r'\}|'+re.escape(value)+r')',bib),'Bib '+key)
need('Published 17 October 2026. Unrefereed.'in bib,'Bib status/date')
outside=page.replace(desc,'');outside_text=norm(text(outside))
for phrase in ['strictly positive real weights','allowing repeated poles','ordinary finite nonnegative Lebesgue integrals','chosen before R','simultaneously for every real R','not claimed optimal','bounded holes','No new general singular-integral theorem','Astala, Sakai','Yongxi Lin and André Guerra','mathematical texts were inaccessible','relevance remains unresolved','not certify historical public visibility or causal independence','including code','Third-party works retain','no external human peer review','authorship would reflect actual scholarly contributions']:
    need(phrase in outside_text,'faithful source/editorial phrase '+phrase)
need(not any(x in outside for x in ['1458','root_control.py','native-control.stdout','three distinct mathematical audits','optimized modes']),'no added detailed verification replay outside exact native Description')
receipt=json.loads(read(E/'RENDER_RECEIPT.json'));need(receipt['inputs']['preview/index.html']==pin(raw) and receipt['method']=='Installed headless Chrome local-file layout; no live/native desktop PDF-viewer certification.','saved render provenance/qualification')
need(all(v['viewport']==v['scroll'] and v['main']==v['h1']==1 and v['description']==desc for v in receipt['views']),'saved desktop/mobile layout facts')
render_names=sorted('renders/'+name for name in ['desktop-full.png','mobile-full.png','desktop-abstract.png','mobile-abstract.png','desktop-result.png','mobile-result.png'])
render_pins=[{'path':name,**pin(read(E/name))}for name in render_names]
need('abstract'not in article,'explicit observed private structured-abstract gap')
result={'status':'PASS_PRIVATE_EDITORIAL_FIDELITY_WITH_PUBLIC_WRAPPER_ABSTRACT_ITEM','scientific_family_review':False,'whole_MAIN':pin(main),'whole_page':pin(raw),'whole_head':final['whole_head'],'head_pin_extent':head_style,'writer_files':32,'writer_child_directories':3,'native_metadata_and_file_objects_whole_equal':True,'native_Description_five_paragraphs_exact':True,'whole_visible_original_abstract_including_formula':True,'actual_abstract_text_for_future_public_wrapper':' '.join(norm(text(p))for p in abstract_paragraphs),'native_assets_in_original_order':asset_checks,'saved_six_renders':render_pins,'saved_render_method':receipt['method'],'fresh_source_page_images_viewed':4,'fresh_saved_candidate_views_read':6,'new_renderer_browser_native_project_or_scientific_execution':False,'public_wrapper_metadata_item':{'ScholarlyArticle.abstract_present_in_private_head':False,'action':'Add complete actual original-abstract section, including formula, as ScholarlyArticle.abstract during public wrapper assembly without rewriting MAIN.','private_fidelity_failure':False},'AA':None,'follow_up':None,'canonical_url':None,'publication_authority':False,'writes':0}
print(json.dumps(result,ensure_ascii=False,indent=2))
