"""Publish only this effort's authored checkpoint on fresh main, without checkout/index changes."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json,subprocess
ROOT=Path('/Users/alec/Documents/Math');P=ROOT/'draft_pr_descending_audit_20261002';D=Path(__file__).resolve().parent
OUT=D/'checkpoint_transport'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');OUT.mkdir(parents=True,exist_ok=False)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';B='repos/AlecKriebel/Math/';seq=0

def api(method,path,payload=None):
 global seq
 seq+=1;args=[GH,'api','--method',method,B+path]
 if payload is not None:
  f=OUT/f'{seq:02d}-request.json';f.write_text(json.dumps(payload));args+=['--input',str(f)]
 r=subprocess.run(args,capture_output=True);(OUT/f'{seq:02d}-stdout.json').write_bytes(r.stdout);(OUT/f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
 if r.returncode:raise RuntimeError(f'Native call {seq} failed; receipts retained, reconcile before any uncertain mutation retry')
 return json.loads(r.stdout)
pr=api('GET','pulls/248');i=json.loads((D/'INTAKE.json').read_text());assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==i['head']
q=api('GET','contents/'+i['Queue_path']+'?ref='+i['head']);row=next(x for x in base64.b64decode(q['content']).decode().splitlines() if '30004630 / OWR-4990378-001' in x);assert row.split('|')[8].strip()=='claimed_solved'
paths=[P/'RESEARCH_LOG.md',P/'CURRENT_GOAL_SELECTION_20261013.json']
paths += [x for x in D.iterdir() if x.is_file() and x.suffix in ['.md','.json','.py'] and not x.name.endswith('RECEIPT.json')]
paths += [x for x in (D/'submitted').rglob('*') if x.is_file()]
paths += [x for x in (D/'root_reproduction').rglob('*') if x.is_file() and '__pycache__' not in x.parts]
for folder,manifestname,key in [(D/'source_pde_adversary_02','FINAL_AUDIT_MANIFEST.json','public_authored_relative_paths'),(D/'variational_adversary_02','FINAL_AUDIT_MANIFEST.json','files'),(D/'source_pde_adversary_02/addendum_review','FINAL_ADDENDUM_MANIFEST.json','public_authored_relative_paths')]:
 fm=folder/manifestname
 if fm.exists():
  m=json.loads(fm.read_text());paths.append(fm)
  for pin in m[key]:
   f=folder/pin['path'];assert f.resolve().is_relative_to(folder.resolve()) and f.stat().st_size==pin['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==pin['sha256'];paths.append(f)
for folder,key in [('priority_classical_adversary_01','authored_files'),('priority_recent_adversary_01','public_authored_files'),('priority_bridge_falsifier_01','public_authored_relative_paths'),('priority_attribution_falsifier_01','public_authored_relative_paths')]:
 audit_dir=D/folder;fm=audit_dir/'FINAL_AUDIT_MANIFEST.json';m=json.loads(fm.read_text());pins=m[key];pins=[{'path':k,**v} for k,v in pins.items()] if isinstance(pins,dict) else pins
 paths.append(fm)
 for pin in pins:
  f=audit_dir/pin.get('path',pin.get('relative_path'));assert f.resolve().is_relative_to(audit_dir.resolve()) and f.stat().st_size==pin['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==pin['sha256'];paths.append(f)
paths.append(D/'root_priority_final_version_check/FINAL_VERSION_RETRIEVAL.json')
paths+=list((P/'next_selection_after_pr254_20261013').glob('*.json'))
entries=[];pins=[]
for f in sorted(set(paths)):
 assert f.resolve().is_relative_to(P.resolve()) and not f.is_symlink();data=f.read_bytes();entries.append({'path':f.relative_to(ROOT).as_posix(),'mode':'100644','type':'blob','content':data.decode()});pins.append({'path':f.relative_to(ROOT).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
for attempt in range(4):
 parent=api('GET','git/ref/heads/main')['object']['sha'];tree=api('GET','git/commits/'+parent)['tree']['sha'];nt=api('POST','git/trees',{'base_tree':tree,'tree':entries})['sha'];commit=api('POST','git/commits',{'message':'Accept bounded priority audit of explicit critical-wave counterexample; prepare credited note','tree':nt,'parents':[parent]})['sha']
 try:
  assert api('PATCH','git/refs/heads/main',{'sha':commit,'force':False})['object']['sha']==commit;break
 except RuntimeError:
  reject=json.loads((OUT/f'{seq:02d}-stdout.json').read_text());latest=api('GET','git/ref/heads/main')['object']['sha']
  if reject.get('status')!='422' or latest==parent or attempt==3:raise
current=api('GET','git/ref/heads/main')['object']['sha']
if current!=commit:assert api('GET','compare/'+commit+'...'+current)['status']=='ahead'
r={'utc':datetime.now(timezone.utc).isoformat(),'commit':commit,'parent':parent,'readback_main':current,'owned_files':pins,'case_completion_percent':json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())['completion_percent'],'original_PR_head_unchanged':i['head'],'native_QUEUE_mutation':False,'PR_merge':False,'Zenodo_publication':False,'shared_checkout_and_index_mutations':0,'third_party_reading_copies_excluded':True,'transport_receipts':str(OUT)};(OUT/'PUBLICATION_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n');(D/'PRIORITY_CHECKPOINT_PUBLICATION_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='owned_files'},indent=2))
