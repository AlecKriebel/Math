#!/usr/bin/env python3
"""Apply the actual reviewed patch to a disposable author extraction and replay."""
import hashlib,json,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).absolute().parent
def need(v,m):
 if not v:raise ValueError(m)
def h(b):return hashlib.sha256(b).hexdigest()
def run(p,script,opt):
 r=subprocess.run([sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(p/script)],cwd=p,text=True,capture_output=True,timeout=240)
 need(r.returncode==0,'corrected replay: '+r.stderr);d=json.loads(r.stdout);need(d['status']=='pass','nonpass corrected replay');return d

def main():
 archive=ROOT/'archives/SHORT_CUSP_30006464_AUTHOR_SAFE_FREEZE.zip';before=archive.read_bytes();need(h(before)=='29e8aa1e0ffe71c40132a437da8ce8d442032aaf330a73d144048899fc78b675','author archive pin')
 correction=json.loads((ROOT/'audit/CORRECTION.json').read_text());patch=ROOT/'audit/GRAM_ZERO_DIMENSION.patch';need(h(patch.read_bytes())==correction['patch_sha256']=='372dea806ab051b5d9241f89165384bdda743b7fe07e764e9efdb5e7f9c654d6','patch pin')
 with tempfile.TemporaryDirectory(prefix='actual short cusp correction ') as td:
  d=Path(td)/'corrected author';d.mkdir()
  with zipfile.ZipFile(archive) as z:z.extractall(d)
  old=(d/'PROOFS.md').read_bytes();need(h(old)==correction['original_proof_sha256'] and len(old)==correction['original_proof_bytes'],'preimage')
  r=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(patch)],cwd=d,text=True,capture_output=True);need(r.returncode==0 and 'offset' not in r.stdout and 'fuzz' not in r.stdout,'actual patch application')
  new=(d/'PROOFS.md').read_bytes();need(h(new)==correction['corrected_proof_sha256']=='c0a3ab24c6281c69a29b035eb6a7e1c3f0485242e4ac5339b00327ca91fa8ad0' and len(new)==9718,'postimage')
  changed=[]
  with zipfile.ZipFile(archive) as z:
   for n in z.namelist():
    if z.read(n)!=(d/n).read_bytes():changed.append(n)
  need(changed==['PROOFS.md'],'unexpected patch scope')
  m=json.loads((d/'MANIFEST.json').read_text());m['PROOFS.md']={'bytes':len(new),'sha256':h(new)};(d/'MANIFEST.json').write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')
  checks={}
  for script in ['verify.py','test_packet.py']:
   normal=run(d,script,False);optimized=run(d,script,True);need(normal==optimized,'corrected optimized mismatch');checks[script]=normal
  relocated=Path(td)/'relocated corrected copy with spaces';shutil.copytree(d,relocated)
  for opt in [False,True]:need(run(relocated,'verify.py',opt)==checks['verify.py'],'corrected relocation')
 need(archive.read_bytes()==before,'immutable archive changed')
 print(json.dumps({'status':'PASS','actual_patch_command_applied':True,'patch_fuzz':0,'only_proof_changed_before_reseal':True,'corrected_proof_bytes':9718,'corrected_proof_sha256':h(new),'normal_optimized_relocation_agree':True,'corrected_author_exact_controls':checks['verify.py']['total_exact_controls'],'corrected_author_mutation_cases':checks['test_packet.py']['mutation_cases_rejected'],'immutable_archive_unchanged':True,'corrected_derivative_published':False},sort_keys=True,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
