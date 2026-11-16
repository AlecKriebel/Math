"""Single finite data-only comparison; no project imports, subprocesses, network or file writes."""
from pathlib import Path
from html.parser import HTMLParser
import datetime,hashlib,html,json,re,stat
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O=P/'verification/godbillon-vey-editorial-fact-sol-20261116'
S=P/'papers/23357329/sources'
C=P/'papers/23357329/reviews/editorial'
checks=[]
def check(name,value,detail=None):
    checks.append({'check':name,'PASS':bool(value),'detail':detail})
def load(q):
    return json.loads(q.read_text())
def digest(q):
    b=q.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(q.stat().st_mode)}
def matches(q,v):
    d=digest(q); mode=v.get('mode',d['mode'])
    mode=int(mode,8) if isinstance(mode,str) else mode
    return q.is_file() and not q.is_symlink() and d['bytes']==v['bytes'] and d['sha256']==v.get('sha256',v.get('SHA256')) and d['mode']==mode
def extent(q):
    paths=list(q.rglob('*'))
    return sorted(str(x.relative_to(q)) for x in paths if x.is_file()),sorted(str(x.relative_to(q)) for x in paths if x.is_dir()),any(x.is_symlink() for x in paths)
def plain(s):
    return html.unescape(re.sub(r'<[^>]*>','',s))
def canon(s):
    return ' '.join(plain(s).replace('--','–').replace('’',"'").replace('~',' ').split())
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.tags=[]
    def handle_starttag(self,t,a):
        self.tags.append((t,dict(a)))
f=load(C/'FINAL.json'); cm=load(C/'OWNED_MANIFEST.json'); model=load(C/'PAGE_MODEL.json')
facts=load(O/'SOURCE_FACTS.json'); ownseal=load(O/'INITIAL_SEAL.json'); expected=load(C/'EXPECTATIONS.json')
check('Concrete FINAL and manifest handoff pins',matches(C/'FINAL.json',{'bytes':10612,'sha256':'95ee3eb1c38eee121614766aea2ca6ba4e43dc7dfe9850bcf7008ad038ddc339'}) and matches(C/'OWNED_MANIFEST.json',{'bytes':6328,'sha256':'cf6621b9ea0c331b5e3138960af32ed528668d015912753d9f70ce134e6f2d87'}))
cf,cd,cs=extent(C)
check('Exact finite candidate 37 files / 2 dirs, all 35 payload hashes',len(cf)==37 and cd==['preview','renders'] and not cs and len(cm['files'])==35 and set(cf)=={x['path'] for x in cm['files']}|{'FINAL.json','OWNED_MANIFEST.json'} and all(matches(C/x['path'],x) for x in cm['files']))
check('Five own immutable INITIAL payloads and exact seal',len(ownseal['owned_payloads'])==5 and all(matches(O/x['path'],x) for x in ownseal['owned_payloads']) and matches(O/'INITIAL_SEAL.json',{'bytes':1773,'sha256':'c8955f56caf6dc82b80cbde78d7cc56a6b21df99fccf1a2678b0b59593c1e1ef'}))
sp=load(O/'SOURCE_PINS.json')
check('All fifteen source-first reference pins including four reused images',len(sp['references'])==15 and all(matches(P/x['path'],x) for x in sp['references']))
sm=load(S/'SOURCE_MANIFEST.json'); sf,sd,ss=extent(S)
check('Entire source 231 files / 20 dirs and modes unchanged',len(sf)==231 and len(sd)==20 and not ss and sd==sorted(x['path'] for x in sm['directories']) and set(sf)=={x['path'] for x in sm['files']}|set(sm['root_controls_excluded_from_own_list']) and all(matches(S/x['path'],x) for x in sm['files']) and all(stat.S_IMODE((S/x['path']).stat().st_mode)==int(x['mode'],8) for x in sm['directories']))
check('Actual full-original root authority pins',matches(P/'verification/root-clearance-23357329-20261116.json',{'bytes':2780,'sha256':'b90b6495bace1a58b4c8fe973807595340b00f0b0657284f583b46c3d3594dc2'}) and matches(P/'papers/23357329/reviews/root/ROOT_REVIEW.md',{'bytes':8038,'sha256':'a43489206f39a26a254e09ce4cd1b5e4a297b75da2a8ad1708fc0d386e48e53a'}))
raw=(C/'preview/index.html').read_text(); page=Page();page.feed(raw)
main=re.search(r'<main\b[^>]*>[\s\S]*?</main>',raw).group()
head_inner=re.search(r'<head>\n([\s\S]*?)</head>',raw).group(1)
check('Exact personally read whole page / MAIN / head files',matches(C/'preview/index.html',f['whole_page']) and matches(C/'MAIN.html',f['whole_MAIN']) and matches(C/'HEAD.html',f['HEAD']) and (main+'\n').encode()==(C/'MAIN.html').read_bytes() and head_inner.encode()==(C/'HEAD.html').read_bytes())
metas={a.get('name',a.get('property')):a['content'] for t,a in page.tags if t=='meta' and 'content' in a}
article=json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',raw).group(1))
tex=(S/'assets/taut_godbillon_vey.tex').read_text()
a=re.search(r'\\begin\{abstract\}\n([\s\S]*?)\n\\end\{abstract\}',tex).group(1)
visible=re.search(r'<p id="original-abstract">([\s\S]*?)</p>',main).group(1)
check('Full original abstract on body / schema / DC / model',a==facts['abstract_original_TeX'] and canon(a)==canon(visible)==canon(article['abstract'])==canon(metas['DC.description'])==canon(model['abstract']) and article==model['scholarly_article'])
r=load(S/'record.response.body'); files=load(S/'files-23357329.response.body'); versions=load(S/'versions-001.response.body')
check('Native full metadata/file objects literal; distinct Description retained',expected['native_metadata_original']==r['metadata']==facts['native_metadata_entire_object'] and expected['native_record_file_objects_original_order']==r['files'] and expected['native_files_endpoint_complete_original']==files==facts['native_files_API_entire_object'] and r['metadata']['description']==facts['native_Description_HTML_distinct_from_abstract'] and model['full_native_Description_body_duplication'] is False and r['metadata']['description'] not in main)
check('Original literal API null/empty/object shapes retained in source',r['swh']=={} and versions['hits']['hits'][0]['swh'] is None and files['default_preview'] is None and files['order']==[])
check('Title / creator / DOI / dates / native versus absent printed version',article['name']==r['metadata']['title']==model['original_title']==metas['citation_title'] and article['author']['identifier']=='https://orcid.org/0009-0001-9320-500X' and article['identifier']=='https://doi.org/'+r['doi'] and article['datePublished']==r['metadata']['publication_date']=='2026-10-13' and article['dateCreated']==r['created']==model['native_created']=='2026-10-14T04:59:37.522998+00:00' and article['version']==r['metadata']['version']==model['native_version']=='1.0' and metas['citation_publication_date']=='2026/10/13' and model['printed_numeric_version'] is None and model['printed_numeric_version_present'] is False)
check('Private noindex and null canonical/base/production/AA/follow-up',set(metas['robots'].split(','))=={'noindex','nofollow','noarchive'} and all(model[x] is None for x in ['canonical_url','base_url','production_url','AA','follow_up']) and model['publication_authority'] is False and not any(t=='base' or (t=='link' and a.get('rel')=='canonical') or (t=='meta' and a.get('property')=='og:url') for t,a in page.tags))
ids=[a['id'] for t,a in page.tags if 'id' in a]
check('One semantic MAIN id=main and H1; unique IDs',len([1 for t,a in page.tags if t=='main' and a.get('id')=='main'])==1 and len([1 for t,a in page.tags if t=='main'])==1 and len([1 for t,a in page.tags if t=='h1'])==1 and len(ids)==len(set(ids)))
links=[]
for t,attrs in page.tags:
    for key in ['href','src']:
        u=attrs.get(key)
        if not u or u.startswith('https://') or u in ['/','/research/']:continue
        ok=u[1:] in ids if u.startswith('#') else '/' not in u.split('#')[0] and (C/'preview'/u.split('#')[0]).is_file()
        links.append({'target':u,'exists':ok})
check('Every actual local resource / fragment target exists',all(x['exists'] for x in links),links)
order=[x['key'] for x in r['files']]
asset_list=re.search(r'<ol id="native-assets">([\s\S]*?)</ol>',main).group(1)
check('Original ZIP / PDF / TeX order and unchanged native bytes / MD5',order==[x['name'] for x in model['native_assets']]==re.findall(r'<li><a href="([^"]+)" download>',asset_list)==['verification-package.zip','taut_godbillon_vey.pdf','taut_godbillon_vey.tex'] and all((C/'preview'/x['key']).read_bytes()==(S/'assets'/x['key']).read_bytes() and hashlib.md5((C/'preview'/x['key']).read_bytes()).hexdigest()==x['checksum'][4:] for x in r['files']))
check('Original titled FitH iframe / direct open / download / citation PDF',metas['citation_pdf_url']=='taut_godbillon_vey.pdf' and any(t=='iframe' and a.get('src')=='taut_godbillon_vey.pdf#view=FitH' and a.get('title') for t,a in page.tags) and any(t=='a' and a.get('href')=='taut_godbillon_vey.pdf' and 'download' in a for t,a in page.tags))
bib=(C/'citation.bib').read_bytes()
check('BibTeX original edition / rights and identical preview copy',bib==(C/'preview/citation.bib').read_bytes() and all(x in bib.decode() for x in ['Kriebel, Alec','Unbounded {Godbillon-Vey} numbers on a fixed hyperbolic manifold','date = {2026-10-13}','version = {1.0}',r['doi'],'Creative Commons Attribution 4.0']))
licenses=(C/'LICENSES.md').read_text()
check('CC BY native scope / third-party rights; new MIT grant separate',r['metadata']['license']=={'id':'cc-by-4.0'} and article['license']=='https://creativecommons.org/licenses/by/4.0/' and model['rights']['native_MIT_inference'] is False and 'Only the two freshly authored editorial utilities' in licenses and 'No MIT license is inferred for native archive code' in licenses and (C/'LICENSE_CODE.txt').read_text().startswith('MIT License'))
check('Shared white Arial style exact pin',matches(C/'preview/research.css',{'bytes':1170,'sha256':'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'}))
layout=load(C/'renders/LAYOUT_RECEIPT.json')
check('Six personally viewed saved images bound by finite manifest',len(layout['captures'])==6 and all(x['saved'] and x['error'] is None and matches(C/x['path'],next(v for v in cm['files'] if v['path']==x['path'])) for x in layout['captures']))
check('Literal layout receipt / stdout and empty diagnostics preserved', (C/'renders/LAYOUT_RECEIPT.json').read_bytes()==(C/'renders/RENDER.stdout.json').read_bytes() and len((C/'renders/RENDER.stderr.txt').read_bytes())==0 and all(layout[x]==[] for x in ['request_failures','console_errors','page_errors','blocked_HTTP_requests','download_clicks']) and layout['fatal_error'] is None and layout['native_viewer_certification'] is False and [x['document_scroll_width'] for x in layout['measurements']]==[1100,390])
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if all(x['PASS'] for x in checks) else 'NO_GO','role':'finite data comparison; personal semantic review and saved-image review are separate','checks_count':len(checks),'checks':checks,'observed_candidate_modes':sorted(set(stat.S_IMODE((C/x).stat().st_mode) for x in cf)),'candidate_manifest_note':'Writer manifest binds bytes/hash but does not record modes; actual observed modes recorded, no invented historical mode pin.','literal_layout_diagnostics':{x:layout[x] for x in ['request_failures','console_errors','page_errors','blocked_HTTP_requests','fatal_error','download_clicks','native_viewer_certification']},'native_science_writer_helper_render_GET_executions':0,'actual_live_mobile_native_accessible_reader_download_certification':False,'follow_up':None,'publication_authority':False}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['status']=='PASS' else 1)
