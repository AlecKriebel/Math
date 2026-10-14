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
pr=api('GET','pulls/248');i=json.loads((D/'INTAKE.json').read_text());merged=json.loads((D.parent/'publication/PR_MERGED.json').read_text());assert pr['merged'] and pr['state']=='closed' and pr['head']['sha']==merged['reviewed_head'] and pr['merge_commit_sha']==merged['merge_commit']
q=api('GET','contents/'+i['Queue_path']+'?ref='+merged['reviewed_head']);row=next(x for x in base64.b64decode(q['content']).decode().splitlines() if '30004630 / OWR-4990378-001' in x);assert row.split('|')[8].strip()=='claimed_solved'
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
preprint_dir=D.parent/'preprint'
for name in ['critical_wave_growth.tex','prepare_verification_package.py','record_package_acceptance.py','metadata.json','deposit.json','FROZEN_CANDIDATE.json','ROOT_PACKAGE_ACCEPTANCE.json','RESEARCH_LOG.md']:
 paths.append(preprint_dir/name)
paths += [f for f in (preprint_dir/'verification_package').rglob('*') if f.is_file() and f.suffix in ['.md','.json','.py','.txt','.tex']]
paths += [preprint_dir/'root_archive_reproduction'/name for name in ['VERIFICATION_RUN.json','stdout.json','stderr.txt']]
paths.append(preprint_dir/'ROOT_REVIEW01_ACCEPTANCE.json')
review_dir=preprint_dir/'fresh_review_01';review_manifest=review_dir/'FINAL_AUDIT_MANIFEST.json';review=json.loads(review_manifest.read_text());assert review['mandatory_issues']==[]
paths.append(review_manifest)
for pin in review['public_authored_relative_paths']:
 item=review_dir/pin['path'];assert item.resolve().is_relative_to(review_dir.resolve()) and item.stat().st_size==pin['bytes'] and hashlib.sha256(item.read_bytes()).hexdigest()==pin['sha256'];paths.append(item)
paths += [preprint_dir/name for name in ['ROOT_REVIEW02_ACCEPTANCE.json','ROOT_EDITORIAL_PACKAGE_ACCEPTANCE.json','EDITORIAL_REFINEMENT.json','validate_editorial_root.py']]
review_dir=preprint_dir/'fresh_review_02';fm=review_dir/'FINAL_AUDIT_MANIFEST.json';m=json.loads(fm.read_text());paths.append(fm)
for pin in m['public_authored_relative_paths']:
 f=review_dir/pin['path'];assert f.stat().st_size==pin['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==pin['sha256'];paths.append(f)
paths += [f for f in (preprint_dir/'root_editorial_reproduction').rglob('*') if f.is_file() and 'extracted' not in f.relative_to(preprint_dir/'root_editorial_reproduction').parts and '__pycache__' not in f.parts]
paths += [f for f in (preprint_dir/'history').rglob('*') if f.is_file() and f.suffix in ['.md','.json','.tex']]
paths+=list((P/'next_selection_after_pr254_20261013').glob('*.json'))
for name in ['FINAL_CLEARANCE.json','ROOT_REVIEW03_ACCEPTANCE.json','ROOT_EDITORIAL_DELTA_ACCEPTANCE.json']:
 paths.append(preprint_dir/name)
for name in ['fresh_review_03','editorial_delta_review_01']:
 review_dir=preprint_dir/name;fm=review_dir/'FINAL_AUDIT_MANIFEST.json';m=json.loads(fm.read_text());paths.append(fm)
 keys=[k for k in ['public_authored_relative_paths','public_authored_files','authored_files','files'] if k in m];assert len(keys)==1
 pp=m[keys[0]];pp=[{'path':k,**v} for k,v in pp.items()] if isinstance(pp,dict) else pp
 for pin in pp:
  f=review_dir/pin.get('path',pin.get('relative_path'));assert f.stat().st_size==pin['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==pin['sha256'];paths.append(f)
for name in ['PR_PREPARED.json','NATIVE_SCIENTIFIC_READBACK.json','PR_MERGED.json','ZENODO_VERIFIED_PUBLICATION.json','TRACKER_VERIFIED_APPEND.json']:
 paths.append(D.parent/'publication'/name)
entries=[];pins=[]
for f in sorted(set(paths)):
 assert f.resolve().is_relative_to(P.resolve()) and not f.is_symlink();data=f.read_bytes();entries.append({'path':f.relative_to(ROOT).as_posix(),'mode':'100644','type':'blob','content':data.decode()});pins.append({'path':f.relative_to(ROOT).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
for f in sorted((preprint_dir/'pr_update/30004630').rglob('*')):
 if f.is_file():
  data=f.read_bytes();entries.append({'path':i['native_source_prefix']+f.relative_to(preprint_dir/'pr_update/30004630').as_posix(),'mode':'100644','type':'blob','content':data.decode()})
for attempt in range(4):
 parent=api('GET','git/ref/heads/main')['object']['sha'];tree=api('GET','git/commits/'+parent)['tree']['sha'];nt=api('POST','git/trees',{'base_tree':tree,'tree':entries})['sha'];commit=api('POST','git/commits',{'message':'Record PR248 publication, exact tracker readback and confirmed native merge','tree':nt,'parents':[parent]})['sha']
 try:
  assert api('PATCH','git/refs/heads/main',{'sha':commit,'force':False})['object']['sha']==commit;break
 except RuntimeError:
  reject=json.loads((OUT/f'{seq:02d}-stdout.json').read_text());latest=api('GET','git/ref/heads/main')['object']['sha']
  if reject.get('status')!='422' or latest==parent or attempt==3:raise
current=api('GET','git/ref/heads/main')['object']['sha']
if current!=commit:assert api('GET','compare/'+commit+'...'+current)['status']=='ahead'
r={'utc':datetime.now(timezone.utc).isoformat(),'commit':commit,'parent':parent,'readback_main':current,'owned_files':pins,'case_completion_percent':json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())['completion_percent'],'original_PR_head':i['head'],'merged_PR_head':merged['reviewed_head'],'native_QUEUE_mutation':False,'PR_merge':merged['merge_commit'],'Zenodo_publication':merged['doi_url'],'shared_checkout_and_index_mutations':0,'third_party_reading_copies_excluded':True,'transport_receipts':str(OUT)};(OUT/'PUBLICATION_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n');(D/'COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='owned_files'},indent=2))
