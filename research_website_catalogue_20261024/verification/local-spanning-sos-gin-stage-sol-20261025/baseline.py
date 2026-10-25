"""Capture fresh actual492 baseline before proposing any renderer/helper changes."""
from pathlib import Path
import ast,datetime,hashlib,json,re,xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent;P=O.parents[1];LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
IDS=['23181280','23442760','23395703']
ED={'23181280':'02e1ec1a4a5d19c648e5670811eb81ac11ec536b4c6f1baa62af29310898e2f8','23442760':'f9fbc0cd6bdf27eccdd562cf488db0fc916d848338b6d1849e2454718474718a','23395703':'5aeba83c3805618f17aa3a7903df7fb0e53e108d6ea9568cae64473b813a6fb5'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
if (O/'protected-before.json').exists():raise RuntimeError('preserve_initial_baseline')
index=(LIVE/'research/index.html').read_text();listing=json.loads(re.search('<script type="application/ld\\+json">(.*?)</script>',index,re.S).group(1))['mainEntity'];urls=[x['url'] for x in listing['itemListElement']]
allpublic=[p for p in LIVE.rglob('*') if p.is_file()];sitemap=[x.text for x in ET.fromstring((LIVE/'research/sitemap.xml').read_text()).iter() if x.tag.endswith('loc')]
if len(allpublic)!=492 or len(urls)!=listing['numberOfItems']!=62 or len(urls)!=62 or len(sitemap)!=63:raise RuntimeError('expected_current492_62_63')
mapped={}
for p in (P/'papers').glob('*/publication.json'):
    c=json.loads(p.read_text());u='https://aleckriebel.com/research/'+c['slug']+'/'
    if u in urls:mapped[u]=p.parent.name
oldids=[mapped[u] for u in urls if u in mapped];checker=P/'verification/final-content-check.py';tree=ast.parse(checker.read_text());tex=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='TEX_PATHS' for x in n.targets))
if len(oldids)!=61 or set(oldids)!=set(tex) or set(oldids)&set(IDS):raise RuntimeError('explicit_current61_configuration_boundary')
protected=set(allpublic)
protected.update(p for p in (P/'scripts').rglob('*') if p.is_file() and '__pycache__' not in p.parts);protected.add(checker)
for rid in oldids:
    protected.update(P/'papers'/rid/n for n in ['publication.json','promotion.json'])
for rid in IDS:
    base=P/'papers'/rid
    protected.update(p for p in base.rglob('*') if p.is_file() and not ({'cache','tmp','__pycache__'}&set(p.relative_to(base).parts)))
    for prefix in ['root-clearance','root-editorial']:
        p=P/('verification/'+prefix+'-'+rid+'-20261025.json');protected.add(p)
        if prefix=='root-editorial' and sha(p)!=ED[rid]:raise RuntimeError('exact_editorial_authority')
for name in ['firebase.json','.firebaserc']:protected.add(LIVE.parent/name)
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
save('protected-before.json',{'UTC':utc,'phase':'FRESH_CURRENT492_BEFORE_ANY_PROPOSAL','production_public_root':str(LIVE),'public_file_count':492,'index_items':62,'sitemap_URLs':63,'native_context':'Native60 remains historical while current2 browser gate is active; this baseline is the actual current62 public articles, not a native gate claim.','followed_historical1113_maps':False,'files':[{'path':str(p),'bytes':p.stat().st_size,'SHA256':sha(p)} for p in sorted(protected)]})
save('FROZEN_INPUT_SET.json',{'UTC':utc,'baseline_index_URLs_in_order':urls,'baseline_sitemap_URLs_in_order':sitemap,'old_configured_record_ids_in_order':oldids,'unmapped_manual_native_URLs':[u for u in urls if u not in mapped],'authorized_new_record_ids':IDS,'expected_index_items':65,'expected_sitemap_URLs':66,'excluded_preparation_configs':'Any ID outside the explicit current61+new3, including97, is out of scope; globs never grant promotion.'})
(O/'inputs').mkdir(exist_ok=True)
for dest,src in [('render_page.py',P/'scripts/render_page.py'),('final-content-check.py',checker)]:
    (O/'inputs'/dest).write_bytes(src.read_bytes())
save('INPUT_PINS.json',{'UTC':utc,'target_pins':{rid:{'publication':sha(P/'papers'/rid/'publication.json'),'promotion':sha(P/'papers'/rid/'promotion.json'),'editorial':ED[rid],'science':sha(P/('verification/root-clearance-'+rid+'-20261025.json')),'editorial_seal':sha(P/'papers'/rid/'reviews/editorial/SEAL.json'),'editorial_manifest':sha(P/'papers'/rid/'reviews/editorial/MANIFEST.json')} for rid in IDS},'current_renderer_SHA256':sha(P/'scripts/render_page.py'),'current_checker_SHA256':sha(checker),'CSS_SHA256':sha(LIVE/'research/research.css'),'Firebase_SHA256':sha(LIVE.parent/'firebase.json')})
(O/'RESEARCH_LOG.md').write_text('* '+utc+' — Full3 final editorial reports/copies/schema requirements and scientific root objects read. Fresh492 public/62index/63sitemap baseline acquired before proposal; explicit current61 configured+one manual+exact3 targets frozen. Native/browser gates not advanced. Completion estimate10%.\n')
print(json.dumps({'status':'FRESH_BASELINE_CAPTURED','protected_files':len(protected),'public_files':492,'old_configured':61,'authorized_new':IDS,'predicted_index':65,'predicted_sitemap':66},indent=2))
