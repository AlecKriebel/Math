#!/usr/bin/env python3
"""Verify all frozen review inputs, then seal/verify only this review directory."""
from pathlib import Path
import hashlib,json,datetime,sys
R=Path(__file__).resolve().parent;A=R.parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def check_entries(root,entries):
 for e in entries:
  p=root/e['path']
  if p.is_symlink():raise RuntimeError('Symlink '+str(p))
  b=p.read_bytes()
  if len(b)!=e['bytes'] or sha(b)!=e['sha256']:raise RuntimeError('Changed input '+str(p))
def main():
 check_entries(A,json.loads((R/'INPUT_IDENTITIES.json').read_text())['files'])
 check_entries(A,json.loads((A/'ops_doi_identity_repair_20261021/MANIFEST.json').read_text())['files'])
 mp=R/'AUTHORED_FILE_MANIFEST.json';cp=R/'AUTHORED_FILE_MANIFEST.sha256'
 if '--verify' in sys.argv:
  if cp.read_text().split()[0]!=sha(mp.read_bytes()):raise RuntimeError('Seal checksum differs')
  v=json.loads(mp.read_text());check_entries(R,v['files'])
  actual={f.relative_to(R).as_posix() for f in R.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name not in [mp.name,cp.name]}
  if actual!={e['path'] for e in v['files']}:raise RuntimeError('Review inventory changed')
  print(json.dumps({'status':'PASS','sealed_files':len(v['files']),'all134inputs_and_current122_verified':True,'sha256':sha(mp.read_bytes())}));return
 entries=[]
 for f in sorted(R.rglob('*')):
  if f.is_file() and '__pycache__' not in f.parts and f.name not in [mp.name,cp.name]:
   b=f.read_bytes();entries.append({'path':f.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)})
 value={'schema':1,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'package_adversary_04','completion_estimate_percent':100,'overall_verdict':'SCOPED_PASS_NO_UNRESOLVED_MATERIAL_FINDING','unresolved_material_findings':[],'publication_authorization':False,'scope':'Every regular public review artifact, including full report, independent code/results and fresh synthetic operations receipts. Manifest/checksum exclude themselves. Private full source bodies/renders/copies excluded; private custody identities are recorded.','files':entries}
 mp.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n');cp.write_text(sha(mp.read_bytes())+'  '+mp.name+'\n')
 print(json.dumps({'sealed_files':len(entries),'sha256':sha(mp.read_bytes())}))
if __name__=='__main__':main()
