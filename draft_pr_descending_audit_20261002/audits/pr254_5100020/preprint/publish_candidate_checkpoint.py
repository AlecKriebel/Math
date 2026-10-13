"""Publish narrowly owned candidate evidence without touching the checkout/index."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json,subprocess
ROOT=Path('/Users/alec/Documents/Math');P=ROOT/'draft_pr_descending_audit_20261002';HERE=Path(__file__).resolve().parent;D=HERE.parent/'initial_review_20261013'
OUT=HERE/'tmp'/('candidate-publication-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));OUT.mkdir(parents=True,exist_ok=False)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';seq=0;BASE='repos/AlecKriebel/Math/'
def api(method,path,payload=None):
 global seq
 seq+=1;args=[GH,'api','--method',method,BASE+path]
 if payload is not None:
  f=OUT/f'{seq:02d}-request.json';f.write_text(json.dumps(payload));args+=['--input',str(f)]
 r=subprocess.run(args,capture_output=True);(OUT/f'{seq:02d}-stdout.json').write_bytes(r.stdout);(OUT/f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
 if r.returncode:raise RuntimeError(f'Native API {seq} failed; receipts retained')
 return json.loads(r.stdout)
pr=api('GET','pulls/254');intake=json.loads((D/'INTAKE.json').read_text());assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==intake['head']
q=api('GET','contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['head']['sha']);row=next(x for x in base64.b64decode(q['content']).decode().splitlines() if '5100020 / AMR-050-0020' in x);assert row.split('|')[8].strip()=='claimed_solved'
paths=[P/'RESEARCH_LOG.md',P/'CURRENT_GOAL_SELECTION_20261013.json',D/'RESEARCH_LOG.md']
paths += [x for x in HERE.iterdir() if x.is_file() and x.suffix in ['.md','.py','.json','.tex','.txt','.zip']]+[HERE/'LICENSE',HERE/'output/pdf/odd_origin_area_product.pdf',HERE/'tmp/portable_verification.json']
paths += [x for x in (HERE/'verification').rglob('*') if x.is_file() and '__pycache__' not in x.parts]
# Review reports are separately published only when finalized, never inside the ZIP.
for folder in HERE.glob('review_*'):
 if (folder/'FINAL_MANIFEST.json').exists():
  paths += [x for x in folder.glob('*') if x.is_file() and x.suffix in ['.md','.json','.py']]
paths=list(dict.fromkeys(paths));entries=[];pins=[]
for f in paths:
 assert f.resolve().is_relative_to(P) and not f.is_symlink()
 data=f.read_bytes();e={'path':f.relative_to(ROOT).as_posix(),'mode':'100644','type':'blob'}
 if f.suffix in ['.pdf','.zip']:
  e['sha']=api('POST','git/blobs',{'content':base64.b64encode(data).decode(),'encoding':'base64'})['sha']
 else:e['content']=data.decode()
 entries.append(e);pins.append({'path':e['path'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
for attempt in range(4):
 parent=api('GET','git/ref/heads/main')['object']['sha'];tree=api('GET','git/commits/'+parent)['tree']['sha']
 newtree=api('POST','git/trees',{'base_tree':tree,'tree':entries})['sha']
 commit=api('POST','git/commits',{'message':'Checkpoint k403a candidate note and portable verification; manuscript reviews pending','tree':newtree,'parents':[parent]})['sha']
 try:
  assert api('PATCH','git/refs/heads/main',{'sha':commit,'force':False})['object']['sha']==commit;break
 except RuntimeError:
  reject=json.loads((OUT/f'{seq:02d}-stdout.json').read_text());latest=api('GET','git/ref/heads/main')['object']['sha']
  if reject.get('status')!='422' or latest==parent or attempt==3:raise
current=api('GET','git/ref/heads/main')['object']['sha']
if current!=commit:assert api('GET','compare/'+commit+'...'+current)['status']=='ahead'
x={'utc':datetime.now(timezone.utc).isoformat(),'commit':commit,'parent':parent,'readback_main':current,'owned_files':pins,'case_completion_percent':json.loads((HERE/'PACKAGE_STATE.json').read_text())['overall_completion_percent'],'candidate_only':True,'Zenodo_publication':False,'PR_merge':False,'shared_checkout_and_index_mutations':0,'third_party_reading_copies_excluded':True,'transport_receipts':str(OUT)}
(HERE/'CANDIDATE_CHECKPOINT_RECEIPT.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps({k:v for k,v in x.items() if k!='owned_files'},indent=2))
