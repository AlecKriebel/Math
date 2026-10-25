"""Build bounded private production proposals from the exact frozen inputs."""
from pathlib import Path
import datetime,difflib,hashlib,json,shutil,warnings
O=Path(__file__).resolve().parent;R=O.parents[1]
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public');S=O/'public'
IDS=['23390551','23430326']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,obj):
 p=O/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def patch(name,a,b,an,bn):save(name,''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=an,tofile=bn)))
assert sha(R/'scripts/render_page.py')=='61b0e3045a87e14834ac81c092fd1150989d2a3923e843ff4b6b1e6150114bca'
assert sha(R/'verification/final-content-check.py')=='507fa9ef6eb61cda3af4cba2d58ed5c1d84b727c881b37595695005219cf5662'
configs={rid:json.loads((R/'papers'/rid/'publication.json').read_text()) for rid in IDS}
if not (O/'inputs-before.json').exists():
 inputs={p for p in LIVE.rglob('*') if p.is_file()};assert len(inputs)==464,len(inputs)
 inputs.update([R.parent/'AGENTS.md',R/'scripts/render_page.py',R/'scripts/bosonic_source.py',R/'scripts/published_assets.py',R/'verification/final-content-check.py'])
 for rid in IDS:
  p=R/'papers'/rid;c=configs[rid];g=json.loads((p/'promotion.json').read_text())
  inputs.update(x for x in (p/'sources').rglob('*') if x.is_file())
  inputs.update([p/'publication.json',p/'promotion.json',p/c['source_binding']['frozen_scope_content_path'],R/g['root_clearance_file'],R/g['root_custody_receipt'],R/f'verification/root-editorial-{rid}-20261025.json',p/'reviews/root/ROOT_REVIEW.md'])
  for role,item in g['reviews'].items():inputs.update([p/item['report'],p/item['verdict_file']])
  inputs.update(x for x in (p/'reviews/editorial').iterdir() if x.is_file())
 prior=[]
 for name in ['local-quadratic-stage-sol-20261025','local-bosonic-stage-sol-20261025','local-slit-gaussian-stage-sol-20261025','local-surreal-cone-brownian-stage-sol-20261025']:
  root=R/'verification'/name;manifest=root/'stage-readiness-manifest.json';d=json.loads(manifest.read_text());owned=d.get('owned_output_bindings',d.get('artifacts'))
  assert isinstance(owned,dict)
  for relative,b in owned.items():
   path=root/relative;assert path.stat().st_size==b['bytes'] and sha(path)==b['sha256'],path;inputs.add(path)
  inputs.add(manifest);prior.append({'manifest':str(manifest),'sha256':sha(manifest),'owned_outputs':len(owned),'all_rehashed':True})
 save('protected-prior-packages.json',prior)
 save('inputs-before.json',{'utc':now(),'actual_site_files':464,'bindings':{str(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(inputs)}})
 with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 20%: Complete final editorial reports/copies/sections/configs/adapters/seals, root proof/authority objects read. Full464-file site and bounded source/core inputs plus four prior owned package seals/outputs rehashed and bound; no asset-tree copies.\n')
for name,path in [('render_page.py',R/'scripts/render_page.py'),('final-content-check.py',R/'verification/final-content-check.py'),('bosonic_source.py',R/'scripts/bosonic_source.py'),('published_assets.py',R/'scripts/published_assets.py')]:
 (O/'inputs').mkdir(exist_ok=True);shutil.copyfile(path,O/'inputs'/name)
for relative in ['research/index.html','research/research.css','research/sitemap.xml','robots.txt','index.html','blog/index.html','favicon.ico']:
 target=S/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(LIVE/relative,target)
changes=[]
def rep(text,old,new,count=1):
 assert text.count(old)==count,(old,text.count(old),count);changes.append((old,new,count));return text.replace(old,new)
original=(O/'inputs/render_page.py').read_text();renderer=original
renderer=rep(renderer,'from bosonic_source import bosonic_source_view','from bosonic_source import bosonic_source_view\nfrom dipole_source import dipole_source_view')
renderer=rep(renderer,"if paper.name == '23203100':","if paper.name == '23390551':\n    raw_receipt, receipt, asset_root = dipole_source_view(paper, c, gate)\n    receipt_path = paper/c['source_binding']['receipt_path']\nelif paper.name == '23203100':")
for tup,count in [("('23383961','23430906','23444606','23440119','23224103')",2),("('23203100','23383961','23430906','23444606','23440119','23224103')",2),("('23444606','23440119','23224103')",3)]:renderer=rep(renderer,tup,tup[:-1]+",'23390551','23430326')",count)
renderer=rep(renderer,"'23224103':'Read the complete six-page paper in the on-page PDF reader.'","'23224103':'Read the complete six-page paper in the on-page PDF reader.','23390551':'Read the complete 11-page paper in the on-page PDF reader.','23430326':'Read the complete 9-page paper in the on-page PDF reader.'")
renderer=rep(renderer,"paper_intro_html=f'<p>{h(paper_intro)}</p>' if paper_intro else ''","paper_intro_html=f'<p>{h(paper_intro)}</p>' if paper_intro else ''\npdf_reader_word='complete' if paper.name in ('23390551','23430326') else 'full'")
renderer=rep(renderer,' — full paper PDF"',' — {pdf_reader_word} paper PDF"')
renderer_changes=changes[:];changes=[]
save('render_page.proposed.py',renderer);patch('proposed-shared-renderer.diff',original,renderer,'a/scripts/render_page.py','b/scripts/render_page.py')
patch('proposed-dipole-source.diff','',(O/'dipole_source.py').read_text(),'/dev/null','b/scripts/dipole_source.py')
stage=renderer.replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = Path('+repr(str(R))+')').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",'SITE = Path('+repr(str(S/'research'))+')').replace('from published_assets import','sys.path.insert(0, '+repr(str(O))+')\nsys.path.insert(0, '+repr(str(R/'scripts'))+')\nfrom published_assets import',1)
save('render_page.stage.py',stage);patch('renderer-staging-overrides.diff',renderer,stage,'production proposal','explicit private execution copy')
pins={}
for rid in IDS:
 p=R/'papers'/rid;c=configs[rid];g=json.loads((p/'promotion.json').read_text())
 pins[rid]={'publication':sha(p/'publication.json'),'promotion':sha(p/'promotion.json'),'root':sha(R/g['root_clearance_file']),'editorial':sha(R/f'verification/root-editorial-{rid}-20261025.json'),'seal':sha(p/'reviews/editorial/SEAL.json'),'tex':c['source_binding']['source_tex_sha256'],'receipt':g['source_receipt_sha256'],'metadata':g['metadata_sha256'],'created':c['source_binding']['record_created_utc'],'pages':c['pdf_pages'],'display_date':'15 October 2026' if rid=='23390551' else '16 October 2026'}
original_checker=(O/'inputs/final-content-check.py').read_text();checker=original_checker
checker=rep(checker,'from bosonic_source import bosonic_source_view','from bosonic_source import bosonic_source_view\nfrom dipole_source import dipole_source_view')
checker=rep(checker,'SURREAL_CONE_BROWNIAN_IDS=',(O/'new-abstract-normalizer.txt').read_text()+'\nDL_PINS='+repr(pins)+'\nSURREAL_CONE_BROWNIAN_IDS=')
maps=''.join(' '+repr(rid)+':'+repr(configs[rid]['source_binding']['source_tex_path'].removeprefix('sources/'))+',\n' for rid in IDS)
checker=rep(checker," '23444606':'published-source/",maps+" '23444606':'published-source/")
checker=rep(checker,'def abstract_tokens(tex,record_id=None):\n','def abstract_tokens(tex,record_id=None):\n if record_id in DIPOLE_LANGLANDS_IDS:return wt(normalized_dipole_langlands_abstract(record_id,tex))\n')
checker=rep(checker," if rid=='23203100':\n  gate=json.loads((p/'promotion.json').read_text());raw_receipt,receipt,asset_root=bosonic_source_view(p,c,gate);receipt_file=p/c['source_binding']['receipt_path']", " if rid=='23390551':\n  gate=json.loads((p/'promotion.json').read_text());raw_receipt,receipt,asset_root=dipole_source_view(p,c,gate);receipt_file=p/c['source_binding']['receipt_path']\n elif rid=='23203100':\n  gate=json.loads((p/'promotion.json').read_text());raw_receipt,receipt,asset_root=bosonic_source_view(p,c,gate);receipt_file=p/c['source_binding']['receipt_path']")
checker=rep(checker,"'metadata.json' if rid=='23306332' else 'record/zenodo_record.json'", "'zenodo_record.json' if rid=='23390551' else 'metadata.json' if rid=='23306332' else 'record/zenodo_record.json'")
checker=rep(checker,"if rid in SURREAL_CONE_BROWNIAN_IDS else c['author']","if rid in SURREAL_CONE_BROWNIAN_IDS or rid in DIPOLE_LANGLANDS_IDS else c['author']")
checker=rep(checker,'unescape(h) if rid in SURREAL_CONE_BROWNIAN_IDS else h','unescape(h) if rid in SURREAL_CONE_BROWNIAN_IDS or rid in DIPOLE_LANGLANDS_IDS else h')
checker=rep(checker,"if c.get('related_resources') and rid not in SLIT_GAUSSIAN_IDS and rid not in SURREAL_CONE_BROWNIAN_IDS:","if c.get('related_resources') and rid not in SLIT_GAUSSIAN_IDS and rid not in SURREAL_CONE_BROWNIAN_IDS and rid not in DIPOLE_LANGLANDS_IDS:")
checker=rep(checker," result['papers'][rid]={'checks':checks,",(O/'new-record-checks.block.txt').read_text()+" result['papers'][rid]={'checks':checks,")
save('final-content-check.proposed.py',checker);patch('proposed-shared-checker.diff',original_checker,checker,'a/verification/final-content-check.py','b/verification/final-content-check.py')
stage=checker.replace("sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))",'sys.path.insert(0, '+repr(str(O))+')\nsys.path.insert(0, '+repr(str(R/'scripts'))+')').replace('R=Path(__file__).resolve().parents[1]','R=Path('+repr(str(R))+')')
save('final-content-check.stage.py',stage);patch('checker-staging-overrides.diff',checker,stage,'production proposal','explicit private execution copy')
for name,base,edits in [('renderer',original,renderer_changes),('checker',original_checker,changes)]:
 restored=renderer if name=='renderer' else checker
 for old,new,count in reversed(edits):assert restored.count(new)==count;restored=restored.replace(new,old)
 assert restored==base
save('reversible-proposal-edits.json',{'renderer':renderer_changes,'checker':changes})
for name in ['dipole_source.py','render_page.proposed.py','render_page.stage.py','final-content-check.proposed.py','final-content-check.stage.py']:
 with warnings.catch_warnings(record=True) as caught:
  warnings.simplefilter('always');compile((O/name).read_text(),name,'exec')
 assert not caught,[str(x.message) for x in caught]
assert not any(str(O) in (O/name).read_text() for name in ['dipole_source.py','render_page.proposed.py','final-content-check.proposed.py','proposed-shared-renderer.diff','proposed-shared-checker.diff','proposed-dipole-source.diff'])
save('integration-static-checks.json',{'utc':now(),'status':'PASS','entire_current_scripts_recovered_by_exact_edit_reversal':True,'existing_helpers_unchanged':{x:sha(R/'scripts'/x) for x in ['bosonic_source.py','published_assets.py']},'production_proposals_no_private_paths':True,'new_TEX_PATHS':{rid:configs[rid]['source_binding']['source_tex_path'] for rid in IDS},'syntax_warnings':[]})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 40%: Complete bounded production helper/renderer/checker proposals and explicit private overrides built. Exact edit reversal recovers current shared renderer/checker; helper originals unchanged. No actual production mutation.\n')
print('Private stage tools built; production frozen and unchanged.')
