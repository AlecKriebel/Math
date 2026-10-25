"""Capture fresh actual504 baseline before proposing any renderer/helper changes."""
from pathlib import Path
import ast,datetime,hashlib,json,re,xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent;P=O.parents[1];LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
IDS=['23333353','23416806','23441617']
ED={'23333353':'94ab86958620ae8d9f1248fcddcc6b39bd664bba82c6ba68968482c87dc43fb3','23416806':'d6fbc1dbef32e80d435930785c23bb79f6c04deb2abcdaae47cb0d0a743f65dc','23441617':'805412e59a549d658927c85190d451fbf0d0e061edbfa2b5006191fd59f30957'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
if (O/'protected-before.json').exists():raise RuntimeError('preserve_initial_baseline')
index=(LIVE/'research/index.html').read_text();listing=json.loads(re.search('<script type="application/ld\\+json">(.*?)</script>',index,re.S).group(1))['mainEntity'];urls=[x['url'] for x in listing['itemListElement']]
allpublic=[p for p in LIVE.rglob('*') if p.is_file()];sitemap=[x.text for x in ET.fromstring((LIVE/'research/sitemap.xml').read_text()).iter() if x.tag.endswith('loc')]
if len(allpublic)!=504 or len(urls)!=listing['numberOfItems']!=65 or len(urls)!=65 or len(sitemap)!=66:raise RuntimeError('expected_current504_65_66')
mapped={}
for p in (P/'papers').glob('*/publication.json'):
    c=json.loads(p.read_text());u='https://aleckriebel.com/research/'+c['slug']+'/'
    if u in urls:mapped[u]=p.parent.name
oldids=[mapped[u] for u in urls if u in mapped];checker=P/'verification/final-content-check.py';tree=ast.parse(checker.read_text());tex=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='TEX_PATHS' for x in n.targets))
if len(oldids)!=64 or set(oldids)!=set(tex) or set(oldids)&set(IDS):raise RuntimeError('explicit_current64_configuration_boundary')
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
save('protected-before.json',{'UTC':utc,'phase':'FRESH_CURRENT504_BEFORE_ANY_PROPOSAL','production_public_root':str(LIVE),'public_file_count':504,'index_items':65,'sitemap_URLs':66,'native_context':'Native62 remains historical while current3 deploy/browser gates are pending; this baseline is the actual current65 public articles, not a native gate claim.','followed_historical1113_maps':False,'files':[{'path':str(p),'bytes':p.stat().st_size,'SHA256':sha(p)} for p in sorted(protected)]})
save('FROZEN_INPUT_SET.json',{'UTC':utc,'baseline_index_URLs_in_order':urls,'baseline_sitemap_URLs_in_order':sitemap,'old_configured_record_ids_in_order':oldids,'unmapped_manual_native_URLs':[u for u in urls if u not in mapped],'authorized_new_record_ids':IDS,'expected_index_items':68,'expected_sitemap_URLs':69,'excluded_preparation_configs':'Any ID outside the explicit current64+new3, including100/101/103, is out of scope; globs never grant promotion.'})
(O/'inputs').mkdir(exist_ok=True)
for dest,src in [('render_page.py',P/'scripts/render_page.py'),('final-content-check.py',checker)]:
    (O/'inputs'/dest).write_bytes(src.read_bytes())
save('INPUT_PINS.json',{'UTC':utc,'target_pins':{rid:{'publication':sha(P/'papers'/rid/'publication.json'),'promotion':sha(P/'papers'/rid/'promotion.json'),'editorial':ED[rid],'science':sha(P/('verification/root-clearance-'+rid+'-20261025.json')),'editorial_seal':sha(P/'papers'/rid/'reviews/editorial/SEAL.json'),'editorial_manifest':sha(P/'papers'/rid/'reviews/editorial/MANIFEST.json')} for rid in IDS},'current_renderer_SHA256':sha(P/'scripts/render_page.py'),'current_checker_SHA256':sha(checker),'CSS_SHA256':sha(LIVE/'research/research.css'),'Firebase_SHA256':sha(LIVE.parent/'firebase.json')})
(O/'RESEARCH_LOG.md').write_text('* '+utc+' — Full3 final editorial reports/copies/schema requirements and scientific root objects read. Fresh504 public/65index/66sitemap baseline acquired before proposal; explicit current64 configured+one manual+exact3 targets frozen. Native/browser gates not advanced. Completion estimate10%.\n')
print(json.dumps({'status':'FRESH_BASELINE_CAPTURED','protected_files':len(protected),'public_files':504,'old_configured':64,'authorized_new':IDS,'predicted_index':68,'predicted_sitemap':69},indent=2))
