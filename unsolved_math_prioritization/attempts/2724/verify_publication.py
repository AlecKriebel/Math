#!/usr/bin/env python3
"""Verify exact bounded KP-1.65 publication artifacts; not a global proof."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, subprocess, tempfile, zipfile

ROOT = Path(__file__).resolve().parent
STEM = 'LAGRANGIAN_ELEMENTARY_2724_'
PINS = {
 'AUTHOR_SAFE_FREEZE.zip':(13437,'b497ff458b87d54ba733a05161b6c9e966356041308650180c7808e2662c83c6'),
 'AUTHOR_EXTERNAL_MANIFEST.json':(2162,'73dac4049ead1776d5ba148a82a8159251d743b5c8e7df8d157365528c8c0cb7'),
 'CORRECTED_SAFE.zip':(14001,'1d578f1d9786c5dcf6ec51c81aef636bc68eae2f09f7a6ea7d3f7053f166ea43'),
 'CORRECTED_EXTERNAL_MANIFEST.json':(2370,'9c961ab3567fc90f4b323a27e489a92e7097aa05d1f3d091dee2f357ea34c8f4'),
 'INDEPENDENT_AUDIT_SAFE.zip':(66675,'bb1c049bcb8fd3077bafdfa6e442957e83846adb0f6581d53ee94faf123a6142'),
 'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json':(4989,'0f9afc402a618abfce28c478858543979d3784225f5131bfb59140c3cc4e7e04'),
 'EXACT_ACCEPTANCE_SAFE.zip':(4440,'aa457cca5266f809c0f77854733291298b5dcb4965fc5ac4206281b1cf64e328'),
 'EXACT_ACCEPTANCE_EXTERNAL_MANIFEST.json':(1267,'2c642705db1e19acdfe949d210fd5bd07146331330679ed5fca57c9ac95fc3b9')}

def require(value,message):
 if not value:raise RuntimeError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def check_bytes(b,e):
 require(len(b)==e['bytes'],'byte count mismatch')
 require(sha(b)==e['sha256'],'SHA-256 mismatch')
def manifest(root,filename):
 m=load(root/filename); expected={e['path']:e for e in m['files']}
 actual={str(p.relative_to(root)):p for p in root.rglob('*') if p.is_file() and p!=root/filename}
 require(set(actual)==set(expected),'manifest inventory mismatch')
 for n,p in actual.items():check_bytes(p.read_bytes(),expected[n])
 return len(actual)
def package(tag,leaf):
 name=STEM+tag+('_SAFE_FREEZE.zip' if tag=='AUTHOR' else '_SAFE.zip')
 blob=(ROOT/'archives'/name).read_bytes();m=load(ROOT/'archives'/(STEM+tag+'_EXTERNAL_MANIFEST.json'));check_bytes(blob,m['artifact'])
 expected={e['path']:e for e in m['files']}
 with zipfile.ZipFile(io.BytesIO(blob)) as z:
  require(z.testzip() is None,'archive CRC failure');names=z.namelist()
  require(len(names)==len(set(names)) and set(names)==set(expected),'archive inventory mismatch')
  contents={}
  for n in names:
   p=PurePosixPath(n);require(not p.is_absolute() and '..' not in p.parts,'unsafe archive member')
   b=z.read(n);check_bytes(b,expected[n]);rel=str(PurePosixPath(*p.parts[1:]));contents[rel]=b
   if leaf:require((ROOT/leaf/rel).read_bytes()==b,'extracted member mismatch')
  internal=json.loads(contents['FILE_MANIFEST.json']);require(internal['self_excluded'] is True,'internal manifest exclusion')
  require({e['path'] for e in internal['files']}==set(contents)-{'FILE_MANIFEST.json'},'internal manifest inventory')
  for e in internal['files']:check_bytes(contents[e['path']],e)
  return contents

def patch_replay(original,corrected):
 patch=ROOT/'independent_audit/audit/CORRECTION.patch'
 with tempfile.TemporaryDirectory(prefix='kp2724-publication-') as tmp:
  root=Path(tmp)
  for name,b in original.items():(root/name).write_bytes(b)
  r=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(patch)],cwd=root,capture_output=True,text=True,timeout=30)
  require(r.returncode==0,'actual correction patch failed: '+r.stderr)
  entries=[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(root.iterdir()) if p.name!='FILE_MANIFEST.json']
  (root/'FILE_MANIFEST.json').write_text(json.dumps({'schema_version':1,'self_excluded':True,'files':entries},indent=2,sort_keys=True)+'\n')
  require({p.name for p in root.iterdir()}==set(corrected),'patch result inventory')
  for n,b in corrected.items():require((root/n).read_bytes()==b,'patch result byte mismatch: '+n)
 return {'actual_patch_applied':True,'deterministic_internal_manifest_regenerated':True,'files_exactly_matched':len(corrected)}

def main():
 total=manifest(ROOT,'PUBLICATION_MANIFEST.json')
 for name,(n,h) in PINS.items():check_bytes((ROOT/'archives'/(STEM+name)).read_bytes(),{'bytes':n,'sha256':h})
 original=package('AUTHOR',None); corrected=package('CORRECTED','corrected'); audit=package('INDEPENDENT_AUDIT','independent_audit');acceptance=package('EXACT_ACCEPTANCE','exact_acceptance')
 for sub,tag in [('author_archive','AUTHOR'),('corrected_artifact','CORRECTED')]:
  for n in (STEM+tag+('_SAFE_FREEZE.zip' if tag=='AUTHOR' else '_SAFE.zip'),STEM+tag+'_EXTERNAL_MANIFEST.json'):
   require(audit[sub+'/'+n]==(ROOT/'archives'/n).read_bytes(),'nested archive/manifest mismatch')
 for n in ['EXACT_ACCEPTANCE.json','EXACT_ACCEPTANCE.md']:
  require(acceptance[n]==audit['audit/'+n],'acceptance copy mismatch')
 meta=load(ROOT/'PUBLICATION_METADATA.json'); status=json.loads(corrected['STATUS.json']);acc=json.loads(acceptance['EXACT_ACCEPTANCE.json'])
 for item in [meta,status,acc]:
  require(item['status']=='unsolved' and item['turns_used']==1 and item['turn_limit']==5,'status scope mismatch')
  require(all(item[k] is False for k in ['full_solution','counterexample_to_original_problem','novelty_claim']),'unjustified scope widening')
 require(meta['queue']['changed_cells']==['Status','Turns'],'queue scope')
 require(b'nonempty negative end' in corrected['MATHEMATICAL_AUDIT.md'],'nonempty-end correction missing')
 require(b'Lagrangian concordances associated with Legendrian isotopies' in corrected['MATHEMATICAL_AUDIT.md'],'isotopy correction missing')
 require(b'authored paraphrase' in corrected['MATHEMATICAL_AUDIT.md'],'target paraphrase missing')
 require(b'does not by itself prove that all isotopic embeddings' in corrected['SOURCE_AUDIT.md'],'display/isotopy distinction missing')
 for key in ['correction_patch','independent_audit_report','independent_verifier','optimization_replay_summary','patch_replay','primary_source_review']:
  e=acc[key];check_bytes(audit['audit/'+e['filename']],e)
 result={'status':'PASS','problem_id':2724,'problem_2724_solved':False,'files_in_publication_manifest':total,'top_level_archive_members_verified':sum(map(len,[original,corrected,audit,acceptance])),'nested_archive_members_bound_by_exact_copies':18,'exact_corrected_files':len(corrected),'patch_replay':patch_replay(original,corrected),'scope':'Publication integrity, exact patch replay, and scoped metadata only; not mathematical proof certification.'}
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
