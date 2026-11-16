"""One offline data-only comparison; no imports or execution of project code."""
from pathlib import Path
import hashlib
import html
import json
import re
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
E = P / 'papers/23153134/reviews/editorial'
S = P / 'papers/23153134/sources'
O = P / 'verification/negative-gramian-editorial-fact-sol-20261116'
checks = []

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def need(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

def plain(value):
    return ' '.join(html.unescape(value).split())

need('Exact handed writer FINAL', digest(E/'FINAL.json') == '07afb343fd138db9138e09029f97b988b74bb1fb6dc63fdf6be91601672d5017')
need('Exact handed writer manifest', digest(E/'OWNED_MANIFEST.json') == 'a40bba8f97a4008f082da27443bb59e415e7930a9e085d37f50982b1edd7a157')
manifest = json.loads((E/'OWNED_MANIFEST.json').read_text())
actual_files = sorted(str(q.relative_to(E)) for q in E.rglob('*') if q.is_file())
need('All 48 files, including ignored and empty streams, exactly enumerated', actual_files == sorted(manifest['actual_file_paths_including_controls']) and len(actual_files) == 48)
for entry in manifest['payloads']:
    q = E/entry['path']
    assert q.stat().st_size == entry['bytes'] and digest(q) == entry['sha256']
    assert oct(stat.S_IMODE(q.stat().st_mode)) == entry['mode']
need('All 46 writer payloads match whole bytes and modes', len(manifest['payloads']) == 46)
need('Exact two writer directories and modes', sorted(str(q.relative_to(E)) for q in E.rglob('*') if q.is_dir()) == ['preview','renders'] and all(oct(stat.S_IMODE((E/d['path']).stat().st_mode)) == d['mode'] for d in manifest['directories']))
page = (E/'preview/index.html').read_text()
model = json.loads((E/'PAGE_MODEL.json').read_text())
head = (E/'HEAD.html').read_text().strip()
main = (E/'MAIN.html').read_text().strip()
need('Whole HEAD and MAIN are exact single page constituents', page.count(head) == 1 and page.count(main) == 1)
own = json.loads((O/'SOURCE_PINS.json').read_text())
abstract = own['original_abstract_TeX']
for before, after in [('$\\R^{17}$','ℝ¹⁷'),('$T>0$','T > 0'),('$P_T=T\\pi^*g$','P_T = Tπ*g'),('$-1/T$','−1/T')]:
    abstract = abstract.replace(before,after)
abstract = plain(abstract)
visible = plain(re.search(r'<p id="original-abstract">(.*?)</p>',page,re.S).group(1))
dc = plain(re.search(r'<meta name="DC.description" content="(.*?)">',page,re.S).group(1))
scholarly = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',page,re.S).group(1))
need('Full source abstract equals visible/model/ScholarlyArticle/DC, with explicit math rendering only', visible == model['abstract'] == scholarly['abstract'] == dc == abstract)
expectations = json.loads((E/'EXPECTATIONS.json').read_text())
need('Distinct original Description retained exactly', expectations['full_distinct_native_Description_HTML'] == own['native_metadata']['description'] and own['native_metadata']['description'] not in page)
need('Model and head scholarly metadata agree exactly', model['scholarly_article'] == scholarly)
native = json.loads((S/'files-23153134.response.body').read_text())['entries']
names = [a['key'] for a in native]
ordered_html = re.search(r'<ol id="native-assets">(.*?)</ol>',page,re.S).group(1)
links = re.findall(r'<li><a href="([^"]+)" download>',ordered_html)
for entry in native:
    original = (S/'assets'/entry['key']).read_bytes()
    assert original == (E/'preview'/entry['key']).read_bytes()
    assert len(original) == entry['size'] and 'md5:'+hashlib.md5(original).hexdigest() == entry['checksum']
need('All nine native whole buffers, native MD5/size and API/list/model order', len(names) == 9 and names == links == model['native_asset_order'])
need('Bib copies identical; actual edition, DOI and licence retained', (E/'citation.bib').read_bytes() == (E/'preview/citation.bib').read_bytes() and all(x in (E/'citation.bib').read_text() for x in ['2026-10-05','version = {1.0}','10.5281/zenodo.23153134','CC-BY-4.0']))
need('Private nulls and no-publication state retained', all(model[k] is None for k in ['canonical_url','base_url','production_url','AA','follow_up']) and model['private'] is True and model['publication_authority'] is False and 'noindex,nofollow,noarchive' in head and '<base' not in head and 'rel="canonical"' not in head)
ids = re.findall(r'\bid="([^"]+)"',page)
need('Unique IDs, one main and one H1', len(ids) == len(set(ids)) and page.count('<main id="main">') == 1 and len(re.findall(r'<h1\b',page)) == 1)
for ref in re.findall(r'(?:href|src)="([^"]+)"',page):
    if ref.startswith(('https:','http:','/')):
        continue
    path, _, fragment = ref.partition('#')
    assert not path or (E/'preview'/path).is_file()
    assert path or not fragment or fragment in ids
need('All relative local targets and own-page fragments resolve statically', True)
need('Both writer process stderr streams are literally empty', all((E/n).read_bytes() == b'' for n in ['DATA_CHECK.stderr.txt','RENDER.stderr.txt']))
need('Literal render stdout and saved layout receipt identical', (E/'RENDER.stdout.json').read_bytes() == (E/'renders/LAYOUT_RECEIPT.json').read_bytes())
layout = json.loads((E/'RENDER.stdout.json').read_text())
need('Literal no-error arrays and absent native/download certification recorded', all(layout[k] == [] for k in ['request_failures','console_errors','page_errors','blocked_HTTP_requests','download_clicks']) and layout['fatal_error'] is None and layout['native_viewer_certification'] is False)
for entry in own['source_controls']:
    assert digest(P/entry['path']) == entry['SHA256']
for entry in own['source_images_individually_viewed_in_page_order']:
    assert digest(P/entry['path']) == entry['SHA256']
need('Source controls, source rasters and actual nine native buffers unchanged', True)
print(json.dumps({'status':'PASS','kind':'one offline data-only comparison; no scientific verdict or reader certification','checks':checks,'check_count':len(checks),'writes':0,'native_scientific_helper_render_Git_network_runs':0,'saved_PDF_frame_observation':'Both full-page saved frames blank, personally viewed separately','publication_authority':False},indent=2))
