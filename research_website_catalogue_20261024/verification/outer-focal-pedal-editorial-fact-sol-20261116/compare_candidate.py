"""One bounded data-only comparison. Reads pinned artifacts; prints JSON; no writes/imports of project programs."""
from pathlib import Path
from html.parser import HTMLParser
import datetime, hashlib, html, json, re, stat
P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/outer-focal-pedal-editorial-fact-sol-20261116'
S = P / 'papers/23398175/sources'
C = P / 'papers/23398175/reviews/editorial'
checks = []
def check(name, value, detail=None):
    checks.append({'check': name, 'PASS': bool(value), 'detail': detail})
def load(q):
    return json.loads(q.read_text())
def digest(q):
    b = q.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'mode': stat.S_IMODE(q.stat().st_mode)}
def matches(q, pin):
    d = digest(q)
    mode = pin.get('mode', d['mode'])
    mode = int(mode, 8) if isinstance(mode, str) else mode
    return q.is_file() and not q.is_symlink() and d['bytes'] == pin['bytes'] and d['sha256'] == pin.get('sha256', pin.get('SHA256')) and d['mode'] == mode
def extent(q):
    all_paths = list(q.rglob('*'))
    return sorted(str(x.relative_to(q)) for x in all_paths if x.is_file()), sorted(str(x.relative_to(q)) for x in all_paths if x.is_dir()), any(x.is_symlink() for x in all_paths)
def text(markup):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', markup))).strip()
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
f = load(C/'FINAL.json')
m = load(C/'OWNED_MANIFEST.json')
model = load(C/'PAGE_MODEL.json')
facts = load(O/'SOURCE_FACTS.json')
check('Concrete handoff FINAL pin', matches(C/'FINAL.json', {'bytes':7482,'sha256':'b122a708bafd6d4a407cde58ff6f66afe12d8e22073ec26e28e95603be60069b'}))
check('Concrete handoff manifest pin', matches(C/'OWNED_MANIFEST.json', {'bytes':7323,'sha256':'c7c44196d06058be080bb56cc839adce14b2ae4cd0d142c0c9919b8a404fe968'}))
cf, cd, cs = extent(C)
check('Exact candidate finite 35 files / 2 dirs, no symlinks', len(cf)==35 and len(cd)==2 and not cs and cf==f['finite_extent']['files']==m['finite_extent']['files'] and cd==f['finite_extent']['directories']==m['finite_extent']['directories'])
check('All 33 candidate payload byte/mode pins', len(m['payloads'])==33 and all(matches(C/x['path'], x) for x in m['payloads']) and set(cf)=={x['path'] for x in m['payloads']}|{'FINAL.json','OWNED_MANIFEST.json'})
seal = load(O/'INITIAL_SEAL.json')
check('All five own immutable INITIAL payloads', len(seal['payloads'])==5 and all(matches(O/x['path'],x) for x in seal['payloads']))
check('Own INITIAL seal and authority continuation unchanged', matches(O/'INITIAL_SEAL.json',{'bytes':1549,'sha256':'52edf75e7fb1c20ebc0413dbf7fae80bb83ac7ea370e522e85400e53df9c84a4'}) and matches(O/'AUTHORITY_RECONCILIATION.md',{'bytes':5714,'sha256':'161c4d33c0f80a9dd32a859303e90f775363366730d5f33911e162c88d0c4d13'}))
sp = load(O/'SOURCE_PINS.json')
check('All sixteen source-first reference pins', len(sp['entries'])==16 and all(matches(P/x['path'], x) for x in sp['entries']))
sm = load(S/'SOURCE_MANIFEST.json')
sf, sd, ss = extent(S)
check('Entire source finite 206 files / 25 dirs unchanged', len(sf)==206 and len(sd)==25 and not ss and sd==sm['directories'] and set(sf)=={x['path'] for x in sm['files']}|set(sm['exact_terminal_exclusions']) and all(matches(S/x['path'],x) for x in sm['files']))
raw = (C/'preview/index.html').read_text()
main = re.search(r'<main\b[^>]*>[\s\S]*?</main>',raw).group()
head = re.search(r'<head\b[^>]*>[\s\S]*?</head>',raw).group()
check('Exact complete MAIN file equals personally read page fragment', (C/'MAIN.html').read_bytes()==main.encode() and len(main.encode())==10749 and hashlib.sha256(main.encode()).hexdigest()=='9aae1b970a481558c051dbb9e2dace4696c4b9d632d464342baab422c3b4871d')
check('Whole page/head model bindings', all(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'] for b,pin in [(raw.encode(),model['whole_page']),(head.encode(),model['whole_head']),(main.encode(),model['whole_MAIN'])]))
page = Page(); page.feed(raw)
metas = {a.get('name',a.get('property')):a['content'] for t,a in page.tags if t=='meta' and 'content' in a}
article = json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',head).group(1))
source_tex = (S/'published-source/container-001/tree/k605a_outer_focal_pedal_product/manuscript.tex').read_text()
abstract_tex = re.search(r'\\begin\{abstract\}\s*([\s\S]*?)\s*\\end\{abstract\}',source_tex).group(1)
abstract = ' '.join(abstract_tex.split()).replace('$k_{605,a}$','k605,a').replace('$k_{606}$','k606')
visible = re.search(r'<section id="original-abstract">[\s\S]*?<p>([\s\S]*?)</p>',main).group(1)
check('Full actual source abstract exact in visible / schema / DC', abstract_tex==facts['abstract_tex_exact']==model['abstract_tex'] and abstract==model['abstract']==article['abstract']==metas['DC.description']==text(visible))
r = load(S/'record.response.body'); fa = load(S/'files-23398175.response.body')
am = load(S/'published-source/container-001/tree/k605a_outer_focal_pedal_product/metadata.json')
check('Whole native/authored metadata and file objects literal', model['native_metadata_original']==r['metadata'] and model['native_record_files']==r['files'] and model['native_files_response']==fa and model['authored_metadata_original']==am)
check('Distinct Description retained, no duplicate visible full Description', model['native_description_original']==facts['native_description_exact']==r['metadata']['description'] and model['visible_duplicate_description'] is False and r['metadata']['description'] not in main)
check('Original title / identity / date / version / printed-version distinction', article['name']==r['metadata']['title']==metas['citation_title'] and article['author']['identifier']=='https://orcid.org/0009-0001-9320-500X' and article['identifier']['value']==r['doi']=='10.5281/zenodo.23398175' and article['datePublished']==r['metadata']['publication_date']=='2026-10-15' and article['version']==r['metadata']['version']=='1.0' and metas['citation_publication_date']=='2026/10/15' and model['printed_version'] is None and model['native_created']==r['created']=='2026-10-15T14:26:52.483806+00:00')
check('Private noindex and null canonical/base/production/AA/follow-up', metas['robots']=='noindex, nofollow, noarchive' and all(model[x] is None for x in ['canonical_url','base_url','production_url','AA','follow_up']) and model['publication_authority'] is False and not any(t=='base' or (t=='link' and a.get('rel')=='canonical') or (t=='meta' and a.get('property')=='og:url') for t,a in page.tags))
check('Native/authored CC BY 4.0, no MIT inference', r['metadata']['license']=={'id':'cc-by-4.0'} and am['license']=='cc-by-4.0' and article['license']=='https://creativecommons.org/licenses/by/4.0/' and not re.search(r'\bMIT\b',main))
ids = [a['id'] for t,a in page.tags if 'id' in a]
check('One semantic MAIN id=main / H1 and unique identifiers', len([1 for t,a in page.tags if t=='main' and a.get('id')=='main'])==1 and len([1 for t,a in page.tags if t=='main'])==1 and len([1 for t,a in page.tags if t=='h1'])==1 and len(ids)==len(set(ids)))
local_links = []
for t,a in page.tags:
    for attr in ['href','src']:
        u = a.get(attr)
        if not u or u.startswith('https://') or u in ['/','/research/']:
            continue
        local_links.append((u, u[1:] in ids if u.startswith('#') else '/' not in u.split('#')[0] and (C/'preview'/u.split('#')[0]).is_file()))
check('Every actual local resource target/fragment exists', all(ok for u,ok in local_links), local_links)
order = [x['key'] for x in r['files']]
ordered = re.findall(r'<li><a href="([^"]+)" download>', re.search(r'<ol id="native-downloads">([\s\S]*?)</ol>',main).group(1))
check('Native order / unchanged bytes / MD5 / schema encodings', order==ordered==model['native_asset_order']==['k605a-outer-focal-pedal-areas.pdf','k605a-source-verification.zip'] and all((C/'preview'/x['key']).read_bytes()==(S/'assets'/x['key']).read_bytes() and hashlib.md5((C/'preview'/x['key']).read_bytes()).hexdigest()==x['checksum'][4:] and article['encoding'][i]['contentUrl']==x['key'] and article['encoding'][i]['sameAs']==x['links']['self'] for i,x in enumerate(r['files'])))
check('Titled native FitH iframe / direct open / download / citation PDF', any(t=='iframe' and a.get('src')==order[0]+'#view=FitH' and a.get('title') for t,a in page.tags) and any(t=='a' and a.get('href')==order[0] and a.get('target')=='_blank' for t,a in page.tags) and metas['citation_pdf_url']==order[0])
bib = (C/'preview/citation.bib').read_text()
check('BibTeX exact visible/download and correct scholarly edition', bib.strip()==html.unescape(re.search(r'<pre>([\s\S]*?)</pre>',main).group(1)).strip() and all(x in bib for x in ['Kriebel, Alec',r['metadata']['title'],'day = {15}','version = {1.0}',r['doi'],'CC-BY-4.0']))
check('Exact style pin and readable white Arial rules', matches(C/'preview/research.css',{'bytes':1170,'sha256':'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'}) and 'pre { white-space: pre-wrap; overflow-wrap: anywhere; }' in head)
rr = load(C/'RENDER_RECEIPT.json'); er = load(C/'EXECUTION_RECEIPTS.json'); stream = load(C/'render.stdout.json')
check('All six personally viewed saved image pins', len(rr['captures'])==6 and all(matches(C/x['path'],x) for x in rr['captures']))
check('Literal writer render streams/receipt agree, no error erasure', stream['render']==rr and stream['check']==load(C/'CHECK_RECEIPT.json') and len((C/'render.stderr.txt').read_bytes())==0==er['stderr_bytes'] and er['actual_exit']==0 and er['meaningful_helper_invocations']==1 and len(rr['diagnostics']['console_errors'])==11 and len(rr['diagnostics']['failed_requests'])==11 and len(rr['diagnostics']['nonlocal_page_routes_aborted'])==11 and rr['diagnostics']['page_errors']==[] and rr['actual_embedded_PDF_display_certified'] is False)
check('Writer helper body read statically, not executed by this lane', matches(C/'preview_tools.mjs',{'bytes':15334,'sha256':'0f89b312f33a01af99e39ebe170b4bb2507b32b08a91e43713707daf011ad2b9'}))
result = {'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if all(x['PASS'] for x in checks) else 'NO_GO','role':'bounded data comparison only; semantic full-copy review and image inspection are separately personal','checks':checks,'checks_count':len(checks),'writer_diagnostics_literal':rr['diagnostics'],'own_native_or_science_or_writer_helper_or_render_executions':0,'actual_PDF_or_download_or_live_certification':False,'follow_up':None,'publication_authority':False}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['status']=='PASS' else 1)
