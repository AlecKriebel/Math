"""Build only owned private artifacts from exact current production inputs."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,re,shutil,warnings
O=Path(__file__).resolve().parent;R=O.parents[1]
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public');S=O/'public'
IDS=['23444606','23440119','23224103']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,obj):
 p=O/name;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(obj if isinstance(obj,str) else json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def patch(name,a,b,an,bn):save(name,''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=an,tofile=bn)))
changes=[]
def rep(s,a,b,count=1):
 assert s.count(a)==count,(a,s.count(a),count)
 changes.append((a,b,count));return s.replace(a,b)
assert sha(R/'scripts/render_page.py')=='20286458f1740817c01ffeac00f6861688ea5e538b30c40294312a91f2d68780'
assert sha(R/'verification/final-content-check.py')=='a91d622212b26a28bb777852796af2af51cc536a9c2c2e7d0a0ae2136eb45124'
if not (O/'inputs-before.json').exists():
 inputs=set(p for p in LIVE.rglob('*') if p.is_file())
 assert len(inputs)==452,len(inputs)
 inputs.update([R.parent/'AGENTS.md',R/'scripts/render_page.py',R/'scripts/bosonic_source.py',R/'scripts/published_assets.py',R/'verification/final-content-check.py'])
 for rid in IDS:
  p=R/'papers'/rid;g=json.loads((p/'promotion.json').read_text());c=json.loads((p/'publication.json').read_text())
  inputs.update(x for x in (p/'sources').rglob('*') if x.is_file())
  inputs.update([p/'publication.json',p/'promotion.json',p/c['source_binding']['frozen_scope_content_path'],R/g['root_clearance_file'],R/g['root_custody_receipt'],R/f'verification/root-editorial-{rid}-20261025.json'])
  for v in g['reviews'].values():inputs.update([p/v['report'],p/v['verdict_file']])
  inputs.update(x for x in (p/'reviews/editorial').iterdir() if x.is_file())
  inputs.update(x for x in (p/'reviews').rglob('*') if x.is_file() and x.name.lower() in ['seal.json','final_seal.json','final-seal.json'])
 for name in ['receipt.json','final-site.json','target-two.json','legacy49.json']:
  inputs.add(R/'verification/slit-gaussian-production-integration-root-20261025'/name)
 baseline={str(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(inputs)}
 save('inputs-before.json',{'utc':now(),'completion_percent':15,'actual_site_files':452,'bindings':baseline})
 save('RESEARCH_LOG.md','# Private surreal / cone / Brownian staging log\n\n'+now()+' — 15%: Complete editorial configs/copies/sections/adapters/seals and separate root authorities read. Exact current52-site/script baseline captured. Production frozen.\n')
for name,path in [('render_page.py',R/'scripts/render_page.py'),('final-content-check.py',R/'verification/final-content-check.py'),('bosonic_source.py',R/'scripts/bosonic_source.py'),('published_assets.py',R/'scripts/published_assets.py')]:
 (O/'inputs').mkdir(exist_ok=True);shutil.copyfile(path,O/'inputs'/name)
for rel in ['research/index.html','research/research.css','research/sitemap.xml','robots.txt','index.html','blog/index.html','favicon.ico']:
 d=S/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(LIVE/rel,d)
configs={rid:json.loads((R/'papers'/rid/'publication.json').read_text()) for rid in IDS}
original=(O/'inputs/render_page.py').read_text();renderer=original
renderer=rep(renderer,"('23383961','23430906')","('23383961','23430906','23444606','23440119','23224103')",2)
renderer=rep(renderer,"('23203100','23383961','23430906')","('23203100','23383961','23430906','23444606','23440119','23224103')",2)
renderer=rep(renderer,"'23430906':'Read the full seven-page paper in the on-page PDF reader.'", "'23430906':'Read the full seven-page paper in the on-page PDF reader.','23444606':'Read the complete seven-page paper in the on-page PDF reader.','23440119':'Read the complete five-page paper in the on-page PDF reader.','23224103':'Read the complete six-page paper in the on-page PDF reader.'")
renderer=rep(renderer,"if c['version'] is None: article.pop('version')", "if c['version'] is None: article.pop('version')\nif paper.name in ('23444606','23440119','23224103'): article['license']='https://creativecommons.org/licenses/by/4.0/'")
renderer=rep(renderer,"download_links.append(f'<a href=\"{doi}\">Zenodo record</a>')", "download_links.append(f'<a href=\"{doi}\">Zenodo record</a>')\nif paper.name in ('23444606','23440119','23224103'): download_links.append('<a href=\"https://creativecommons.org/licenses/by/4.0/\">CC BY 4.0</a>')")
renderer=rep(renderer,"(out/'citation.bib').write_text(bib)","if paper.name in ('23444606','23440119','23224103'): bib=(paper/'reviews/editorial/citation.bib').read_text()\n(out/'citation.bib').write_text(bib)")
renderer_changes=changes[:];changes=[]
save('render_page.proposed.py',renderer);patch('proposed-shared-renderer.diff',original,renderer,'a/scripts/render_page.py','b/scripts/render_page.py')
stage=renderer.replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = Path('+repr(str(R))+')').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",'SITE = Path('+repr(str(S/'research'))+')').replace('from published_assets import','sys.path.insert(0, '+repr(str(R/'scripts'))+')\nfrom published_assets import',1)
save('render_page.stage.py',stage);patch('renderer-staging-overrides.diff',renderer,stage,'production proposal','private execution copy')
checker=(O/'inputs/final-content-check.py').read_text();original_checker=checker
maps=''.join(' '+repr(rid)+':'+repr(configs[rid]['source_binding']['source_tex_path'].removeprefix('sources/'))+',\n' for rid in IDS)
checker=rep(checker,'SLIT_GAUSSIAN_IDS=',"SURREAL_CONE_BROWNIAN_IDS={'23444606','23440119','23224103'}\n"+(O/'new-abstract-normalizer.txt').read_text()+'SLIT_GAUSSIAN_IDS=')
checker=rep(checker," '23383961':'published-source/",maps+" '23383961':'published-source/")
checker=rep(checker,'def abstract_tokens(tex,record_id=None):\n','def abstract_tokens(tex,record_id=None):\n if record_id in SURREAL_CONE_BROWNIAN_IDS:return wt(normalized_surreal_cone_brownian_abstract(record_id,tex))\n')
checker=rep(checker,"if c.get('related_resources') and rid not in SLIT_GAUSSIAN_IDS:","if c.get('related_resources') and rid not in SLIT_GAUSSIAN_IDS and rid not in SURREAL_CONE_BROWNIAN_IDS:")
checker=rep(checker,"[c['title'],c['author'],c['doi'],(c['bibtex_note']", "[c['title'],('Kriebel, Alec' if rid in SURREAL_CONE_BROWNIAN_IDS else c['author']),c['doi'],(c['bibtex_note']")
checker=rep(checker,"test('background_links',all(x['url'] in h and", "test('background_links',all(x['url'] in (unescape(h) if rid in SURREAL_CONE_BROWNIAN_IDS else h) and")
checker=rep(checker," result['papers'][rid]={'checks':checks,",(O/'new-record-checks.block.txt').read_text()+" result['papers'][rid]={'checks':checks,")
save('final-content-check.proposed.py',checker);patch('proposed-shared-checker.diff',original_checker,checker,'a/verification/final-content-check.py','b/verification/final-content-check.py')
stage=checker.replace("sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))",'sys.path.insert(0, '+repr(str(R/'scripts'))+')').replace('R=Path(__file__).resolve().parents[1]','R=Path('+repr(str(R))+')')
save('final-content-check.stage.py',stage);patch('checker-staging-overrides.diff',checker,stage,'production proposal','private execution copy')
for name,base,rs in [('renderer',original,renderer_changes),('checker',original_checker,changes)]:
 restored=renderer if name=='renderer' else checker
 for old,new,count in reversed(rs):
  assert restored.count(new)==count,(name,new);restored=restored.replace(new,old)
 assert restored==base
save('reversible-proposal-edits.json',{'renderer':renderer_changes,'checker':changes})
for name in ['render_page.proposed.py','render_page.stage.py','final-content-check.proposed.py','final-content-check.stage.py']:
 with warnings.catch_warnings(record=True) as caught:
  warnings.simplefilter('always');compile((O/name).read_text(),name,'exec')
 assert not caught,[str(x.message) for x in caught]
assert not any('local-surreal-cone-brownian-stage' in (O/name).read_text() for name in ['render_page.proposed.py','final-content-check.proposed.py','proposed-shared-renderer.diff','proposed-shared-checker.diff'])
save('integration-static-checks.json',{'utc':now(),'status':'PASS','completion_percent':35,'entire_original_scripts_recovered_by_exact_edit_reversal':True,'production_proposals_no_private_paths_or_fallbacks':True,'syntax_warnings':[],'new_TEX_PATHS':{rid:configs[rid]['source_binding']['source_tex_path'] for rid in IDS},'original_script_hashes':{'renderer':sha(R/'scripts/render_page.py'),'checker':sha(R/'verification/final-content-check.py')}})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 35%: Bounded production proposals and private execution overrides built; exact edit reversal recovers entire current renderer/checker. No source/config or shared mutation.\n')
print('Private tools built; production unchanged.')
