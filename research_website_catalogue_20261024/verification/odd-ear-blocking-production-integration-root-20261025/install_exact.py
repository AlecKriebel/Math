"""One-time exact installation of fourteen separately root-approved files."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
O=Path(__file__).resolve().parent;P=O.parents[1];V=P/'verification'
S=V/'local-odd-ear-blocking-stage-sol-20261025'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
def need(x,m):
    if not x:raise RuntimeError(m)
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snap(root):return {str(p.relative_to(root)):{'bytes':p.stat().st_size,'sha256':H(p)} for p in root.rglob('*') if p.is_file()}
need(not (O/'installation.json').exists(),'one-time installation')
authority=V/'root-odd-ear-blocking-private-stage-20261025.json'
need(H(authority)=='8a55e860c15b73ffa496b9fc35982b8e12c498c9ebd1966294fc897b920bb725','exact root authority')
a=json.loads(authority.read_text());need(a['production_integration_authorized'] is True,'explicit integration authority')
need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip()=='0171f8e3234e44aa7e57b1f5a5050c80465aeb74','unchanged site base')
need(H(W/'public/index.html')=='29df4a71d2c35ca53fae49b63e2a11954d9e6665b0655a70279c45c47752b0b7','actual unrelated public homepage baseline')
base=json.loads((S/'BASELINE.json').read_text())
for r in base['files']:
    p=Path(r['path']);need(p.stat().st_size==r['bytes'] and H(p)==r['sha256'],'fresh pre-install protected '+str(p))
need(len(base['files'])==3863,'full protected baseline')
before=snap(W/'public');need(len(before)==516 and set(before)==set(base['public_file_set']),'exact public516')
for name,h in a['accepted_proposals'].items():need(H(S/name)==h,'exact approved proposal '+name)
overlay=[p for p in (S/'public').rglob('*') if p.is_file()];need(len(overlay)==10,'exact ten public outputs')
copies=[(S/'odd_ear_blocking_source.py',P/'scripts/odd_ear_blocking_source.py'),(S/'oeb_body_contract.py',P/'scripts/oeb_body_contract.py'),(S/'render_page.proposed.py',P/'scripts/render_page.py'),(S/'final-content-check.proposed.py',V/'final-content-check.py')]
copies += [(p,W/'public'/p.relative_to(S/'public')) for p in overlay]
need(len(copies)==len({d for s,d in copies})==14,'exact unique installation list')
allowed={P/'scripts/render_page.py',V/'final-content-check.py',W/'public/research/index.html',W/'public/research/sitemap.xml'}
need({d for s,d in copies if d.exists()}==allowed,'only four approved existing files overwritten')
records=[{'source':str(s),'destination':str(d),'bytes':s.stat().st_size,'sha256':H(s),'previous_sha256':H(d) if d.exists() else None} for s,d in copies]
# Every dependency and overwrite check above completes before any destination write.
for source,dest in copies:
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
for r in records:need(Path(r['destination']).stat().st_size==r['bytes'] and H(Path(r['destination']))==r['sha256'],'copied exact bytes')
after=snap(W/'public');changed={'research/index.html','research/sitemap.xml'}
need(len(after)==524 and all(after[n]==r for n,r in before.items() if n not in changed),'all514other old public files preserved')
need(H(W/'public/index.html')=='29df4a71d2c35ca53fae49b63e2a11954d9e6665b0655a70279c45c47752b0b7','unrelated homepage preserved')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXACT_ROOT_APPROVED14_FILES_INSTALLED','root_authority_sha256':H(authority),'copies':records,'before_public_file_count':516,'after_public_file_count':524,'old_unmodified_public_files':514,'all_other_old_public_bytes_unchanged':True,'unrelated_public_homepage_sha256':H(W/'public/index.html'),'renderer_executed':False,'HTTP_browser_download_native_gates_pending':True,'AA_written':False,'all203_complete':False}
with (O/'installation.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':result['status'],'copies':14,'public_files':524,'other_old_public_files_preserved':514,'renderer_executed':False}))
