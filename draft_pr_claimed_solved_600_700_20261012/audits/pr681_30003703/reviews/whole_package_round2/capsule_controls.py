"""Independent integrity probes use captured trusted verifier, never suspect code."""
import hashlib,json,shutil,sys,tempfile,zipfile
from pathlib import Path
R=Path(__file__).absolute().parent;root=R/'tmp/packet';source=(root/'verify_package.py').read_bytes()
n={'__file__':str(root/'verify_package.py'),'__name__':'trusted_round2_verifier'}
exec(compile(source,str(root/'verify_package.py'),'exec'),n)
checks=[]
def need(x,label):
 if not x:raise RuntimeError(label)
def repin(target,name):
 p=target/name;b=p.read_bytes();manifest=json.loads((target/'PACKAGE_MANIFEST.json').read_bytes())
 for row in manifest['files']:
  if row['path']==name:row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 (target/'PACKAGE_MANIFEST.json').write_bytes(n['json_bytes'](manifest))
def probe(label,name,mutate):
 with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='fresh-capsule-')as d:
  t=Path(d)/'p';shutil.copytree(root,t);mutate(t/name);repin(t,name)
  try:n['verify'](t)
  except(ValueError,OSError)as e:checks.append({'case':label,'outcome':'REJECTED','exception':type(e).__name__});return
  raise RuntimeError('hostile accepted '+label)
for label,name in [
 ('semantic_whitespace_cannot_repin_immutable_priority_receipt','PRIORITY_GATE_ACCEPTANCE.json'),
 ('family_source_comment_cannot_repin_family_freeze','reviews/matrix_ideal_01/matrix_controls.py'),
 ('native_proof_newline_cannot_repin_native_snapshot','native/unsolved_math_prioritization/attempts/30003703/release/PROOF.md'),
 ('metadata_newline_still_breaks_current_QA_binding','zenodo-deposit.json'),
 ('final_freeze_newline_cannot_repin_stable_root_pin','reviews/freegroup_01/FINAL_FREEZE.json'),
]:probe(label,name,lambda p:p.write_bytes(p.read_bytes()+b'\n'))
probe('README_rehashed_classical_credit_removed','README.md',lambda p:p.write_bytes(p.read_bytes().replace(b'Burde',b'XXXXX')))
probe('native_regular_but_mode0600_rejected','native/unsolved_math_prioritization/attempts/30003703/release/verify.py',lambda p:p.chmod(0o600))
with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='fresh-unknown-')as d:
 t=Path(d)/'p';shutil.copytree(root,t);b=b'FAKE raw full-text placeholder, no third-party text\n';(t/'raw-source.txt').write_bytes(b)
 manifest=json.loads((t/'PACKAGE_MANIFEST.json').read_bytes());manifest['files'].append({'path':'raw-source.txt','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()});manifest['files'].sort(key=lambda x:x['path']);manifest['file_count']+=1;(t/'PACKAGE_MANIFEST.json').write_bytes(n['json_bytes'](manifest))
 try:n['verify'](t)
 except ValueError:checks.append({'case':'unknown_source_even_fully_manifested_rejected','outcome':'REJECTED'})
 else:raise RuntimeError('manifested unknown accepted')
# Explicitly check the documented trust boundary: an unsigned manifest can be
# refreshed for an unpinned top-level script. External exact ten-file pins detect it.
with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='fresh-trust-boundary-')as d:
 t=Path(d)/'p';shutil.copytree(root,t);p=t/'verify_package.py';p.write_bytes(p.read_bytes()+b'\n# harmless trust-boundary probe\n');repin(t,'verify_package.py')
 need(n['verify'](t)['status']=='PASS','unsigned manifest expected semantics')
 frozen=json.loads((R.parent.parent/'WHOLE_PACKAGE_REVIEW_INPUTS.json').read_bytes())
 need(hashlib.sha256(p.read_bytes()).hexdigest()!=frozen['publication_files']['verify_package.py']['sha256'],'external pin failed')
 checks.append({'case':'unsigned_manifest_is_not_signature_external_script_pin_detects_refresh','outcome':'DOCUMENTED_BOUNDARY_CONFIRMED'})
# Repacking with changed ZIP timestamps has identical payload but a different
# exact artifact hash, and therefore cannot reuse the accepted publication pin.
with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='fresh-repack-')as d:
 p=Path(d)/'repacked.zip'
 with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_DEFLATED)as z:
  for name in sorted(n['inventory'](root)):
   info=zipfile.ZipInfo(name,(2026,10,16,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;z.writestr(info,(root/name).read_bytes())
 pin=json.loads((R.parent.parent/'WHOLE_PACKAGE_REVIEW_INPUTS.json').read_bytes())['publication_files']['satoh_filtration_verification.zip']
 need(hashlib.sha256(p.read_bytes()).hexdigest()!=pin['sha256'],'repacked hash unchanged')
 checks.append({'case':'benign_repack_requires_new_external_artifact_pin','outcome':'DOCUMENTED_BOUNDARY_CONFIRMED'})
print(json.dumps({'schema':'pr681-round2-capsule-controls-v1','status':'PASS','count':len(checks),'checks':checks,'untrusted_packet_code_executed':False,'trusted_verifier_sha256':hashlib.sha256(source).hexdigest()},indent=2,sort_keys=True))
