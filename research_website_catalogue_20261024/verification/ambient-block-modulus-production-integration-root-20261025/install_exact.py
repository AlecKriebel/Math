"""Install the specifically root-approved18 exact files, once; no rendering."""
from pathlib import Path
import json, hashlib, datetime, shutil, subprocess
O=Path(__file__).resolve().parent;P=O.parents[1]
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com');V=P/'verification'
S=V/'local-ambient-block-modulus-stage-sol-20261025';C=V/'ambient-block-modulus-navigation-correction-sol-20261025'
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snap(base):return {str(p.relative_to(base)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in base.rglob('*') if p.is_file()}
need(not (O/'installation.json').exists(),'one-time installation')
authority=V/'root-ambient-block-modulus-private-stage-20261025.json'
need(sha(authority)=='34c4402f8680be583f44fe42241f5f56a503b7ae1cfb54870edd74fc569bc92a','exact separate root authority')
need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip()=='dcc259dbd4fd4285a65374e20ae65281fa30e852','unchanged site base commit')
need(sha(W/'public/index.html')=='29df4a71d2c35ca53fae49b63e2a11954d9e6665b0655a70279c45c47752b0b7','unrelated public homepage matches fresh recheck baseline')
pins=json.loads((S/'INPUT_PINS.json').read_text())
need(sha(P/'scripts/render_page.py')==pins['current_renderer_SHA256'],'old renderer')
need(sha(V/'final-content-check.py')==pins['current_checker_SHA256'],'old checker')
need(sha(W/'firebase.json')==pins['Firebase_SHA256'],'Firebase unchanged')
before=snap(W/'public');need(len(before)==504,'exact current public504')
baseline=json.loads((V/'ambient-block-modulus-navigation-recheck-sol-20261025/BASELINE.json').read_text())
for r in baseline['files']:
    file=Path(r['path'])
    need(file.stat().st_size==r['bytes'] and sha(file)==r['sha256'],'fresh protected baseline before installation: '+str(file))
overlay=list((S/'public').rglob('*'));overlay=[p for p in overlay if p.is_file()]
need(len(overlay)==14,'exact overlay14')
copies=[(S/'ambient_block_modulus_source.py',P/'scripts/ambient_block_modulus_source.py'),(S/'abm_body_contract.py',P/'scripts/abm_body_contract.py'),(S/'render_page.proposed.py',P/'scripts/render_page.py'),(C/'final-content-check.proposed.py',V/'final-content-check.py')]
copies += [(p,W/'public'/p.relative_to(S/'public')) for p in overlay]
allowed_existing={P/'scripts/render_page.py',V/'final-content-check.py',W/'public/research/index.html',W/'public/research/sitemap.xml'}
need(len(copies)==18 and len({d for s,d in copies})==18,'exact unique copy list')
need({d for s,d in copies if d.exists()}==allowed_existing,'only four approved existing changes')
need(sha(C/'final-content-check.proposed.py')==json.loads(authority.read_text())['accepted_checker_sha256'],'exact corrected checker')
records=[]
for source,dest in copies:
    records.append({'source':str(source),'destination':str(dest),'bytes':source.stat().st_size,'sha256':sha(source),'previous_sha256':sha(dest) if dest.exists() else None})
# All original/current preconditions above are checked before any writes.
for source,dest in copies:
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
for r in records:need(sha(Path(r['destination']))==r['sha256'],'exact copied bytes')
after=snap(W/'public');changed={'research/index.html','research/sitemap.xml'}
need(len(after)==516 and all(after[n]==r for n,r in before.items() if n not in changed),'all502 other old public files preserved')
need(sha(W/'public/index.html')=='29df4a71d2c35ca53fae49b63e2a11954d9e6665b0655a70279c45c47752b0b7','unrelated homepage preserved')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXACT_ROOT_APPROVED18_FILES_INSTALLED','root_authority_sha256':sha(authority),'copies':records,'before_public_file_count':504,'after_public_file_count':516,'old_unmodified_public_files':502,'all_other_old_public_bytes_unchanged':True,'unrelated_index_sha256':sha(W/'public/index.html'),'renderer_executed':False,'browser_live_native_gates_pending':True,'AA_written':False,'overall203_goal_complete':False}
with (O/'installation.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':result['status'],'copies':18,'public_files':516,'unmodified_old_public_files':502,'renderer_executed':False}))
