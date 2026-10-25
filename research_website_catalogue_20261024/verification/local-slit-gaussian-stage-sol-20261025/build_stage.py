"""Owned private staging only. Original inputs are read, never written."""
from pathlib import Path
import ast, datetime, difflib, hashlib, json, re, shutil, warnings
O=Path(__file__).resolve().parent
R=O.parents[1]
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
S=O/'public'
IDS=['23383961','23430906']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
 p=O/name;p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():
  old=O/'iterations'/sha(p)/name;old.parent.mkdir(parents=True,exist_ok=True)
  if not old.exists():shutil.copyfile(p,old)
 p.write_text(value if isinstance(value,str) else json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def patch(name,a,b,an,bn):save(name,''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=an,tofile=bn)))
def replace(s,a,b):
 assert s.count(a)==1,a
 return s.replace(a,b,1)
inputs=set(p for p in LIVE.rglob('*') if p.is_file())
inputs.update([R/'scripts/render_page.py',R/'scripts/bosonic_source.py',R/'scripts/published_assets.py',R/'verification/final-content-check.py',R.parent/'AGENTS.md'])
for rid in IDS:
 p=R/'papers'/rid
 inputs.update(x for x in (p/'sources').rglob('*') if x.is_file())
 inputs.update([p/'publication.json',p/'promotion.json'])
 inputs.update(x for x in (p/'reviews').rglob('*') if x.is_file() and (x.name in ['REVIEW.md','verdict.json','SEAL.json','FINAL_SEAL.json','ROOT_REVIEW.md','root-custody-recheck.json','custody-recheck-20261025.json'] or x.parent.name=='editorial' and x.suffix in ['.json','.md','.py','.sha256']))
 inputs.update([R/f'verification/root-clearance-{rid}-20261025.json',R/f'verification/root-editorial-{rid}-20261025.json'])
for name in ['REPORT.md','final-site-manifest.json','evidence-manifest.json']:
 inputs.add(R/'verification/approved-three-production-integration-sol-20261025'/name)
baseline={str(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(inputs)}
if not (O/'inputs-before.json').exists():
 save('inputs-before.json',{'utc':now(),'completion_percent':15,'bindings':baseline,'actual_site_files':sum(str(p).startswith(str(LIVE)+'/') for p in inputs)})
 save('RESEARCH_LOG.md','# Private slit / Gaussian stage log\n\n'+now()+' — 15%: Read exact editorial copies, configs, adapters and root clearances. Captured lean original-site/source/authority baseline. Production frozen.\n')
else:assert json.loads((O/'inputs-before.json').read_text())['bindings']==baseline
for name,path in [('render_page.py',R/'scripts/render_page.py'),('final-content-check.py',R/'verification/final-content-check.py'),('bosonic_source.py',R/'scripts/bosonic_source.py'),('published_assets.py',R/'scripts/published_assets.py')]:
 (O/'inputs').mkdir(exist_ok=True);shutil.copyfile(path,O/'inputs'/name)
for rid in IDS:
 for name in ['REPORT.md','PUBLIC_COPY.md','SCHEMA_ADAPTER.json']:
  dest=O/'inputs'/rid/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/'papers'/rid/'reviews/editorial'/name,dest)
 for name in ['publication.json','promotion.json']:
  shutil.copyfile(R/'papers'/rid/name,O/'inputs'/rid/name)
 sections=R/'papers'/rid/'reviews/editorial/public-sections.json'
 if sections.exists():shutil.copyfile(sections,O/'inputs'/rid/'public-sections.json')
for rel in ['research/index.html','research/research.css','research/sitemap.xml','robots.txt','index.html','blog/index.html','favicon.ico']:
 d=S/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(LIVE/rel,d)
original=(O/'inputs/render_page.py').read_text();renderer=original
renderer=replace(renderer,"sections=section('abstract','Abstract',c['abstract'].split('\\n\\n'))", "abstract_heading=c.get('abstract_heading','Abstract') if paper.name in ('23383961','23430906') else 'Abstract'\nsections=section('abstract',abstract_heading,c['abstract'].split('\\n\\n'))")
renderer=replace(renderer,"if paper.name=='23203100' else ''", "if paper.name in ('23203100','23383961','23430906') else ''")
renderer=replace(renderer,"if paper.name=='23203100':\n    download_links.append", "if paper.name in ('23203100','23383961','23430906'):\n    download_links.append")
renderer=replace(renderer,"sections+=f'<section id=\"paper\"><h2>Read the paper</h2>","paper_intro={'23383961':'The full five-page PDF appears in the on-page reader.','23430906':'Read the full seven-page paper in the on-page PDF reader.'}.get(paper.name)\npaper_intro_html=f'<p>{h(paper_intro)}</p>' if paper_intro else ''\nsections+=f'<section id=\"paper\"><h2>Read the paper</h2>{paper_intro_html}")
renderer=replace(renderer,"if c.get('related_resources'):\n    sections+=", "if paper.name in ('23383961','23430906'):\n    sections+=f'<section id=\"materials\"><h2>Supporting materials</h2><ul><li><a href=\"{h(c[\"supplement_filename\"])}\" download>{h(c[\"supplement_label\"])}</a> · <a href=\"https://zenodo.org/records/{record_id}/files/{h(c[\"supplement_filename\"])}\">Zenodo original ZIP</a></li></ul></section>'\nelif c.get('related_resources'):\n    sections+=")
save('render_page.proposed.py',renderer)
patch('proposed-shared-renderer.diff',original,renderer,'a/scripts/render_page.py','b/scripts/render_page.py')
stage=renderer.replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = Path('+repr(str(R))+')').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",'SITE = Path('+repr(str(S/'research'))+')')
stage=replace(stage,'from published_assets import','sys.path.insert(0, '+repr(str(R/'scripts'))+')\nfrom published_assets import')
save('render_page.stage.py',stage);patch('renderer-staging-overrides.diff',renderer,stage,'production proposal','private execution copy')
checker=(O/'inputs/final-content-check.py').read_text();original_checker=checker
checker=replace(checker," '23306332':'published-source/", " '23383961':'published-source/verification_package/support_slit_verification/support_slit.tex',\n '23430906':'support/paper.tex',\n '23306332':'published-source/")
normalizers=r'''SLIT_GAUSSIAN_IDS={'23383961','23430906'}
def normalized_slit_gaussian_abstract(rid,body):
 replacements=[('P.~L.~Duren','P. L. Duren'),('Problem~6.72','Problem 6.72'),('Hayman--Lingham','Hayman–Lingham'),(r'\(a_2+i10^{-24}(a_4-3a_3)\)','a₂+i10⁻²⁴(a₄−3a₃)')] if rid=='23383961' else [(r'$H\in(1/4,1)$','H ∈ (1/4,1)'),(r'$X_T=\int_0^T B^1_s\,dB^2_s$','X_T = ∫₀ᵀ B¹_s dB²_s'),('$n$','n'),('$[0,T]$','[0,T]'),('$c_HT^{2H}n^{1/2-2H}$','c_H T^(2H)n^(1/2−2H)'),('$H$','H'),('$T>0$','T > 0'),(r'$n\ge1$','n ≥ 1'),('$L^2$','L²')]
 for old,new in replacements:body=body.replace(old,new)
 if '\\' in body or '$' in body:raise ValueError('Unrecognized slit/Gaussian abstract command')
 return ' '.join(body.split())
'''
checker=replace(checker,'def normalized_quadratic_abstract(body):',normalizers+'def normalized_quadratic_abstract(body):')
checker=replace(checker,'def abstract_tokens(tex,record_id=None):\n','def abstract_tokens(tex,record_id=None):\n if record_id in SLIT_GAUSSIAN_IDS:return wt(normalized_slit_gaussian_abstract(record_id,tex))\n')
# The new pages deliberately render the approved labels rather than the config's
# differently worded related-resource labels. Test their exact asset link set below.
checker=replace(checker," if c.get('related_resources'):\n  materials=", " if c.get('related_resources') and rid not in SLIT_GAUSSIAN_IDS:\n  materials=")
checker=replace(checker," result['papers'][rid]={'checks':checks,",(O/'new-record-checks.block.txt').read_text()+" result['papers'][rid]={'checks':checks,")
save('final-content-check.proposed.py',checker)
patch('proposed-shared-checker.diff',original_checker,checker,'a/verification/final-content-check.py','b/verification/final-content-check.py')
stage=checker.replace("sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))",'sys.path.insert(0, '+repr(str(R/'scripts'))+')').replace('R=Path(__file__).resolve().parents[1]','R=Path('+repr(str(R))+')')
save('final-content-check.stage.py',stage);patch('checker-staging-overrides.diff',checker,stage,'production proposal','private execution copy')
for name in ['render_page.proposed.py','render_page.stage.py','final-content-check.proposed.py','final-content-check.stage.py']:
 with warnings.catch_warnings(record=True) as caught:
  warnings.simplefilter('always');compile((O/name).read_text(),name,'exec')
 assert not caught,[str(x.message) for x in caught]
assert all('local-slit-gaussian-stage' not in (O/name).read_text() for name in ['render_page.proposed.py','final-content-check.proposed.py','proposed-shared-renderer.diff','proposed-shared-checker.diff'])
save('integration-static-checks.json',{'utc':now(),'status':'PASS','completion_percent':35,'original_renderer_sha256':sha(R/'scripts/render_page.py'),'original_checker_sha256':sha(R/'verification/final-content-check.py'),'syntax_warnings':[],'no_private_paths_in_production_proposals':True,'no_source_config_or_shared_writes':True})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 35%: Built bounded production proposals and explicit private execution copies. All original branches retained. Syntax clean.\n')
print('Private tools built; no original files written.')
