#!/usr/bin/env python3
"""Replay the frozen packet in an ignored private copy; retain every full output."""
from pathlib import Path
import argparse, subprocess, shutil, json, hashlib, datetime, os, sys
p=argparse.ArgumentParser();p.add_argument('--python',required=True);a=p.parse_args()
r=Path(__file__).resolve().parent;snapshot=r.parent/'snapshot';prefix='problems/30006025_geometric_chapuy';src=snapshot/prefix
out=r/'outputs';out.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest=json.loads((r.parent/'snapshot_manifest.json').read_text());assert manifest['head']=='51fddd150e8da33f4cf17b1a642a0ffd3466bf5d'
readrows=[]
for row in manifest['files']:
 b=(snapshot/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'];assert blob(b)==row['git_blob_sha']
 if row['path'].startswith(prefix+'/'):
  readrows.append({'path':row['path'][len(prefix)+1:],'bytes':len(b),'sha256':sha(b),'git_blob_sha1':blob(b),'json_complete_parse':json.loads(b) if row['path'].endswith('.json') else None})
# The full parsed records stay private, since they repeat author/history inputs.
(r/'private/complete_input_read_receipt.json').write_text(json.dumps(readrows,indent=2)+'\n')
(out/'INPUT_READ_RECEIPT.json').write_text(json.dumps({'utc':stamp(),'snapshot_head':manifest['head'],'target_files':len(readrows),'files':[{k:v for k,v in row.items() if k!='json_complete_parse'} for row in readrows],'complete_json_files_parsed':[row['path'] for row in readrows if row['json_complete_parse'] is not None],'read_order':'Primary-source baseline and mathematical verdict sealed before this code/history processing.'},indent=2)+'\n')
D=r/'private/author_replay';assert not D.exists();shutil.copytree(src,D)
checks=[]
for rel,base,keys in [('FINAL_AUTHOR_MANIFEST.json',D,('bytes','sha256','git_blob_sha1')),('PUBLICATION_MANIFEST.json',D,('bytes','sha256','git_blob_sha1')),('independent_review/REVIEW_MANIFEST.json',D/'independent_review',('bytes','sha256',None)),('independent_review/REMOTE_BINDING.json',D,('size',None,'sha'))]+[(f'TURN_{i}_MANIFEST.json',D,('bytes','sha256','git_blob_sha1')) for i in range(1,6)]:
 m=json.loads((D/rel).read_text());rows=[]
 for row in m['files']:
  b=(base/row['path']).read_bytes();assert len(b)==row[keys[0]]
  if keys[1]:assert sha(b)==row[keys[1]]
  if keys[2]:assert blob(b)==row[keys[2]]
  rows.append({'path':row['path'],'bytes':len(b),'sha256':sha(b),'git_blob_sha1':blob(b)})
 if 'previous_manifest_sha256' in m:
  n=m['turn'];assert sha((D/f'TURN_{n-1}_MANIFEST.json').read_bytes())==m['previous_manifest_sha256']
 checks.append({'manifest':rel,'entries':len(rows),'rows':rows,'verified':True})
(out/'MANIFEST_CHECKS.json').write_text(json.dumps({'utc':stamp(),'groups':checks,'total_entries':sum(x['entries'] for x in checks),'note':'Local frozen bytes checked against historical records. No claim of fresh remote state is made.'},indent=2)+'\n')
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
runs=[]
def run(name,argv,expected=None):
 started=stamp();cp=subprocess.run(argv,cwd=D,env=env,capture_output=True)
 for stream in ['stdout','stderr']:(out/f'{name}.{stream}').write_bytes(getattr(cp,stream))
 row={'name':name,'started_utc':started,'finished_utc':stamp(),'argv':argv,'cwd':'private/author_replay','exit_code':cp.returncode,'stdout_bytes':len(cp.stdout),'stderr_bytes':len(cp.stderr),'stdout_sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr)}
 if name!='historical_review_verifier':
  parsed=json.loads(cp.stdout);(out/f'{name}.json').write_bytes(cp.stdout);row['assertions']=parsed.get('assertions');row['whole_json_retained']=True
 if expected:
  exp=(D/expected).read_bytes();row['matches_frozen_receipt_byte_for_byte']=cp.stdout==exp;assert cp.stdout==exp
 assert cp.returncode==0 and not cp.stderr
 runs.append(row);(out/'AUTHOR_REPLAY_RECEIPT.json').write_text(json.dumps({'utc':stamp(),'runs':runs,'total_author_assertions':sum(x.get('assertions',0) or 0 for x in runs if x['name'].startswith('turn')),'status':'IN_PROGRESS' if len(runs)<7 else 'PASS'},indent=2)+'\n')
 print(json.dumps(row),flush=True)
 return cp.stdout
for i in range(1,6):
 b=run(f'turn{i}',[a.python,f'verify_turn{i}.py'],f'TURN_{i}_CHECKS.json')
 if i==1:(D/'TURN_1_CHECKS.json').write_bytes(b) # Feed fresh, identical output into turn 3.
run('historical_independent_checks',[a.python,'independent_review/independent_checks.py'],'independent_review/INDEPENDENT_CHECKS.json')
run('historical_review_verifier',[a.python,'independent_review/verify_review.py','--author-dir',str(D)])
assert all((D/row['path']).read_bytes()==(src/row['path']).read_bytes() for row in readrows)
print('PASS: all private author files remain byte-identical to the frozen input; seven commands retained.',flush=True)
