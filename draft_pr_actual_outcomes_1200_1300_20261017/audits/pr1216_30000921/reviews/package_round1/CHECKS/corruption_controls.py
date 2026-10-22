from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'temp/fresh_extract'
CONTROL=HERE.parent/'temp/corruption';CONTROL.mkdir(exist_ok=True)
def save(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
def rebind(root,rel):
 p=root/rel;b=p.read_bytes();m=json.loads((root/'MANIFEST.json').read_text())
 for e in m['files']:
  if e['path']==rel:e.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 save(root/'MANIFEST.json',m)
results=[]
for kind in ['payload_flip','unlisted_extra','missing_member','duplicate_manifest_path','unsafe_manifest_path','original_rebound_only_at_root','current_rebound_only_at_root','expected_diagnostics_rebound_only_at_root']:
 root=CONTROL/kind
 if root.exists():shutil.rmtree(root)
 shutil.copytree(BASE,root)
 if kind=='payload_flip':
  p=root/'CURRENT_SIMULTANEOUS_PROOF.md';p.write_bytes(p.read_bytes()+b'\ncorruption\n')
 elif kind=='unlisted_extra':(root/'unlisted.txt').write_text('unexpected')
 elif kind=='missing_member':(root/'CURRENT_SIMULTANEOUS_PROOF.md').unlink()
 elif kind in ['duplicate_manifest_path','unsafe_manifest_path']:
  p=root/'MANIFEST.json';m=json.loads(p.read_text())
  if kind=='duplicate_manifest_path':m['files'].append(dict(m['files'][0]))
  else:m['files'][0]['path']='../outside.txt'
  save(p,m)
 elif kind in ['original_rebound_only_at_root','current_rebound_only_at_root']:
  rel=('original_submitted' if kind.startswith('original') else 'current_edition')+'/PROOF.md';p=root/rel;p.write_bytes(p.read_bytes()+b'\nchanged\n');rebind(root,rel)
 else:
  rel='EXPECTED_DIAGNOSTICS.json';p=root/rel;m=json.loads(p.read_text());m['root']['z_threshold_cases']=-1;save(p,m);rebind(root,rel)
 r=subprocess.run([sys.executable,'-B',str(root/'verify.py')],capture_output=True,text=True,env=dict(os.environ,TMPDIR=str(HERE.parent/'temp')))
 if r.returncode==0:raise RuntimeError('corruption accepted: '+kind)
 results.append({'case':kind,'rejected':True,'returncode':r.returncode,'last_error':r.stderr.strip().splitlines()[-1]})
(HERE/'corruption_controls.json').write_text(json.dumps({'status':'PASS','controls':results,'scope':'Executed altered archive copies; no original/publication files changed. Root-rebound cases test nested/semantic consistency after the root hash is intentionally recomputed. Root authenticity itself still requires external BUILD_RECEIPT/artifact hashes.'},indent=2)+'\n')
print(json.dumps(results,indent=2))
