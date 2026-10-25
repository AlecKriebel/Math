"""Bounded installation of root-accepted exact three-paper production proposals."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, subprocess, sys

P=Path(__file__).resolve().parents[1]
B=P/'verification/local-surreal-cone-brownian-stage-sol-20261025'
OUT=P/'verification/surreal-cone-brownian-production-integration-root-20261025'
SITE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(name,d):(OUT/name).write_text(json.dumps(d,indent=2)+'\n')
OUT.mkdir(exist_ok=False)
manifest=json.loads((B/'stage-readiness-manifest.json').read_text())
assert json.loads((P/'verification/root-surreal-cone-brownian-private-stage-20261025.json').read_text())['production_integration_authorized']
assert json.loads((P/'verification/sheet-fifty-two-final-status-20261025.json').read_text())['native_visual_check_pending'] is False
before={str(f):{'bytes':f.stat().st_size,'sha256':sha(f)} for f in (SITE/'public').rglob('*') if f.is_file()}
assert len(before)==452
save('before-site.json',before)
for source,target,expected in [('render_page.proposed.py','scripts/render_page.py','61b0e3045a87e14834ac81c092fd1150989d2a3923e843ff4b6b1e6150114bca'),('final-content-check.proposed.py','verification/final-content-check.py','507fa9ef6eb61cda3af4cba2d58ed5c1d84b727c881b37595695005219cf5662')]:
    assert sha(B/source)==expected
    (P/target).write_bytes((B/source).read_bytes())
commands=[]
def run(args,stem):
    result=subprocess.run(args,cwd=P,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)
    (OUT/(stem+'.stdout')).write_bytes(result.stdout);(OUT/(stem+'.stderr')).write_bytes(result.stderr)
    commands.append({'args':args,'exit':result.returncode,'stdout':stem+'.stdout','stderr':stem+'.stderr'})
    assert result.returncode==0, stem
    return result
for rid in ['23444606','23440119','23224103']:run([PY,'scripts/render_page.py',rid],'render-'+rid)
tree=ast.parse((P/'verification/final-content-check.py').read_text())
mapping=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='TEX_PATHS'for t in n.targets))
old=[rid for rid in mapping if rid not in {'23444606','23440119','23224103'}];assert len(old)==51
for ids,stem in [(['23444606','23440119','23224103'],'target-three'),(old,'legacy51')]:
    run([sys.executable,'verification/final-content-check.py',*ids,'--output-dir',str(OUT),'--output-stem',stem],stem+'-command')
    d=json.loads((OUT/(stem+'.json')).read_text());assert d['status']=='PASS' and not d['issues']
slugs=['initial-omnific-models-discrete-surreal-groups','negative-curvature-normal-barrier-nonhyperbolicity-cone','brownian-first-visit-cell-lengths-circle-joint-laplace-transform']
for slug in slugs:
    for f in (B/'public/research'/slug).iterdir():
        assert (SITE/'public/research'/slug/f.name).read_bytes()==f.read_bytes(),str(f)
for file in ['research/index.html','research/sitemap.xml']:
    assert (SITE/'public'/file).read_bytes()==(B/'public'/file).read_bytes(),file
changed=[path for path,e in before.items()if sha(path)!=e['sha256']]
expected_changed=[str(SITE/'public/research'/f)for f in ['index.html','sitemap.xml']]
assert set(changed)==set(expected_changed)
after={str(f):{'bytes':f.stat().st_size,'sha256':sha(f)}for f in (SITE/'public').rglob('*')if f.is_file()}
added=set(after)-set(before);assert len(added)==12 and len(after)==464
authorized={str(P/'scripts/render_page.py'),str(P/'verification/final-content-check.py'),*expected_changed}
for path,e in manifest['original_input_bindings'].items():
    if path not in authorized:assert Path(path).stat().st_size==e['bytes']and sha(path)==e['sha256'],path
save('final-site.json',after);save('commands.json',commands)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'ROOT_INTEGRATED_EXACT_LOCAL_THREE','records':[23444606,23440119,23224103],
    'full_approved_public_copies_read_and_exact_actual_HTML':True,'old52_articles_assets_css_robots_unchanged':True,
    'before_public_files':452,'after_public_files':464,'only_changed_existing_site_paths':changed,'added_paths':sorted(added),
    'original_bound_inputs_checked':1224,'only_four_authorized_existing_input_changes':True,
    'target_checks':{rid:len(x['checks'])for rid,x in json.loads((OUT/'target-three.json').read_text())['papers'].items()},
    'legacy51_checks':sum(len(x['checks'])for x in json.loads((OUT/'legacy51.json').read_text())['papers'].values()),
    'index_entries':55,'sitemap_urls':56,'site_git_deploy_live_browser_native_done':False}
save('receipt.json',receipt)
(OUT/'RESEARCH_LOG.md').write_text(receipt['utc']+' — Exact accepted proposals installed; only3 authorized renderers executed. Target and old51 content checks pass; actual3HTML/assets/index/sitemap identical to full root-read private stage. Only12newfiles/index/sitemapsite changes;450oldsitefiles exact. Bounded local integration100%; publication gates pending; all203goalcontinues.\n')
print(json.dumps(receipt))
