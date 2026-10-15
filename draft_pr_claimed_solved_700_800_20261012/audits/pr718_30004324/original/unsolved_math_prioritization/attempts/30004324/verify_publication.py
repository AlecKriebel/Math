#!/usr/bin/env python3
"""Strict portable publication replay; finite controls do not prove geometry."""
from pathlib import Path, PurePosixPath
import collections,difflib,hashlib,json,os,shutil,stat,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).absolute().parent
V2='tangent_seshadri_30004324_v2'
DELTA='tangent_seshadri_30004324_v2_delta_acceptance'
PINS={
'TANGENT_SESHADRI_30004324_AUTHOR_SAFE_FREEZE.zip':'6483242536c534a84072815ae4c3aa9de57fd2769386eb2e5e1ad85041cc6a01',
'TANGENT_SESHADRI_30004324_V2_SAFE_FREEZE.zip':'5c698341bff90fc5308d54115853c96c75ea326ce3a2deaa161b18c8e555ba9c',
'TANGENT_SESHADRI_30004324_V2_FROM_V1.patch':'16bec841b55f8b0e3d27add239e2868d4e2a35af0efa2e07734fb04ced131cca',
'TANGENT_SESHADRI_30004324_V2_DELTA.json':'916fdfa26e6bc1df456526c83e5c76a3427cc9d6a3758e47fe14022124627991',
V2+'/MANIFEST.json':'76d4c422d368cf1a91881edaa0429abbc32e5910ea3ad3415b20921d8ee0e024',
DELTA+'/MANIFEST.json':'c405c7534e03e37618620b2497b6b87afa738cd3e9104c26169d06fc868f88f3',
'AUDIT_LAYOUTS.json':'b74fbaa9aea9609ab50a17a0885f9451bb2500a04f16fb25467e162a3498fe8b',
'PUBLICATION_STATUS.json':'2e6f43bf43a142fee97a11ebfbb1e21f630fbf28eb19ebebf997080c3f9dc734',
}
AUDIT_PINS={'tangent_seshadri_30004324_independent_audit':'c848b60407c788e1971d3d189e4d032b85c37f7bbe8af64a7c8e527d833f722b','tangent_seshadri_30004324_second_audit':'919e2d6ab43d5921db7e65bf9f8fcac72626f98e548415301911b1f8dd508484'}
V1_MANIFEST='4869e62250a25e64fc6e4096ea56842a7b23400789f3ba00c14ba81c2c8cd8f7'
REPLAY_HASH='5bcf561ce80764d9fd53f91ddba06471d7d06a52788f4288dabe748ccd79ac54'
def require(c,m):
 if not c:raise ValueError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def info(b):return {'bytes':len(b),'sha256':digest(b)}
def safe(s):
 require(isinstance(s,str) and s and '\\' not in s and not PurePosixPath(s).is_absolute() and all(x not in ('','.','..') for x in s.split('/')) and str(PurePosixPath(s))==s,'Unsafe path')
 return s
def inventory(root):
 require(not root.is_symlink() and root.is_dir(),'Linked or missing root')
 files={};dirs=set()
 for p in root.rglob('*'):
  rel=p.relative_to(root).as_posix();mode=p.lstat().st_mode
  if stat.S_ISDIR(mode):dirs.add(rel)
  else:
   require(stat.S_ISREG(mode),'Nonregular object: '+rel);files[rel]=p.read_bytes()
 implied={str(a) for f in files for a in PurePosixPath(f).parents if str(a)!='.'}
 require(dirs==implied,'Unexpected empty directory')
 return files
def run(path,args=(),optimized=False,cwd=None):
 env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONOPTIMIZE']='1' if optimized else '0'
 cmd=[sys.executable]+(['-O'] if optimized else [])+[str(path)]+list(map(str,args))
 r=subprocess.run(cmd,cwd=cwd or path.parent,env=env,capture_output=True)
 require(r.returncode==0,'Replay failed: '+path.name+' '+r.stderr.decode(errors='replace'))
 return r.stdout
def exact_manifest(root,pin):
 require(digest((root/'MANIFEST.json').read_bytes())==pin,'Manifest pin mismatch')
 for opt in (False,True):run(ROOT/V2/'verify_manifest.py',[root,pin],opt)
def extract(archive,dest):
 dest.mkdir();seen=set()
 with zipfile.ZipFile(ROOT/archive) as z:
  for i in z.infolist():
   name=safe(i.filename);require(name not in seen and not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16),'Invalid archive entry');seen.add(name)
   p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(i))
 return inventory(dest)
def historical_control(opt):
 with tempfile.TemporaryDirectory() as td:
  p=Path(td);b=b'clean fixture\n';(p/'payload.txt').write_bytes(b)
  (p/'MANIFEST.json').write_text(json.dumps({'files':[{'path':'payload.txt',**info(b)}]}))
  old=ROOT/V2/'historical/v1_verify_manifest.py';new=ROOT/V2/'verify_manifest.py'
  run(old,[p],opt);run(new,[p],opt)
  (p/'extra').mkdir();(p/'extra/MANIFEST.json').write_text('unlisted\n');run(old,[p],opt)
  env=os.environ.copy();env['PYTHONOPTIMIZE']='1' if opt else '0'
  r=subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(new),str(p)],env=env,capture_output=True)
  require(r.returncode!=0,'Historical bypass still accepted by authoritative verifier')
def main():
 all_files=inventory(ROOT);manifest_raw=all_files['PUBLICATION_MANIFEST.json'];m=json.loads(manifest_raw)
 if len(sys.argv)>1:require(digest(manifest_raw)==sys.argv[1],'External publication manifest mismatch')
 listed={}
 for item in m['files']:
  require(set(item)=={'path','bytes','sha256'},'Invalid publication entry');p=safe(item['path']);require(p not in listed and p!='PUBLICATION_MANIFEST.json','Duplicate or self path');listed[p]=item
 require(set(all_files)==set(listed)|{'PUBLICATION_MANIFEST.json'},'Closed publication inventory mismatch')
 for p,item in listed.items():require(info(all_files[p])=={k:item[k] for k in ('bytes','sha256')},'Publication file mismatch: '+p)
 for p,pin in PINS.items():require(digest(all_files[p])==pin,'Frozen external pin mismatch: '+p)
 s=json.loads(all_files['PUBLICATION_STATUS.json']);require((s['status'],s['turns'],s['disposition'])==('claimed_solved','2/5','complete_candidate_only'),'Candidate disposition changed')
 exact_manifest(ROOT/V2,PINS[V2+'/MANIFEST.json']);exact_manifest(ROOT/DELTA,PINS[DELTA+'/MANIFEST.json'])
 accepted=json.loads(all_files[DELTA+'/DELTA_ACCEPTANCE.json'])
 require(all(accepted[k]=='PASS' for k in ('proof_delta_verdict','tooling_delta_verdict','exact_frozen_derivative_verdict')),'Delta acceptance changed')
 expected=(ROOT/DELTA/'INDEPENDENT_REPLAY.json').read_bytes();require(digest(expected)==REPLAY_HASH,'Replay pin mismatch')
 layouts=json.loads(all_files['AUDIT_LAYOUTS.json'])['packages'];require({x['package'] for x in layouts}==set(AUDIT_PINS),'Audit set mismatch')
 with tempfile.TemporaryDirectory() as td:
  t=Path(td);original=t/'v1';relocated=t/'v2';v1=extract('TANGENT_SESHADRI_30004324_AUTHOR_SAFE_FREEZE.zip',original);v2=extract('TANGENT_SESHADRI_30004324_V2_SAFE_FREEZE.zip',relocated)
  require(v2==inventory(ROOT/V2) and len(v1)==13 and len(v2)==27,'Archive inventories disagree')
  exact_manifest(original,V1_MANIFEST);exact_manifest(relocated,PINS[V2+'/MANIFEST.json'])
  bindings=json.loads((ROOT/V2/'original_bindings.json').read_bytes())['files']
  require({x['path'] for x in bindings}==set(v1),'Original bindings file set mismatch')
  for x in bindings:require(info(v1[x['path']])=={k:x[k] for k in ('bytes','sha256')},'Original file binding mismatch')
  audits={}
  for layout in layouts:
   dest=t/layout['package'];dest.mkdir();seen=set()
   require(layout['manifest_sha256']==AUDIT_PINS[layout['package']],'Independent manifest pin changed')
   for x in layout['files']:
    name=safe(x['original_path']);require(name not in seen,'Duplicate mapped file');seen.add(name);b=all_files[safe(x['stored_path'])]
    require(info(b)=={k:x[k] for k in ('bytes','sha256')},'Mapped file changed');(dest/name).write_bytes(b)
   exact_manifest(dest,AUDIT_PINS[layout['package']]);audits[layout['package']]=dest
  first=audits['tangent_seshadri_30004324_independent_audit']
  for opt in (False,True):
   require(run(ROOT/V2/'replay.py',optimized=opt)==expected,'Main replay byte mismatch')
   require(run(relocated/'replay.py',optimized=opt)==expected,'Relocated replay byte mismatch')
   require(run(first/'independent_controls.py',optimized=opt)==(first/'independent_results.json').read_bytes(),'Independent finite controls mismatch')
   require(json.loads(run(first/'test_manifest_adversarial.py',optimized=opt))==json.loads((first/'integrity_results.json').read_bytes()),'Fourteen mutation controls mismatch')
   historical_control(opt)
  rows=[];diff=[];counts=collections.Counter()
  for name in sorted(set(v1)|set(v2)):
   old=v1.get(name);new=v2.get(name)
   change='added' if old is None else 'deleted' if new is None else 'unchanged' if old==new else 'modified';counts[change]+=1
   rows.append({'path':name,'change':change,'old':info(old) if old is not None else None,'new':info(new) if new is not None else None})
   if old!=new:diff.extend(difflib.unified_diff((old or b'').decode().splitlines(True),(new or b'').decode().splitlines(True),fromfile='a/'+name if old is not None else '/dev/null',tofile='b/'+name if new is not None else '/dev/null'))
  delta=json.loads(all_files['TANGENT_SESHADRI_30004324_V2_DELTA.json']);require(rows==delta['files'],'Machine delta differs');require({k:counts[k] for k in ('unchanged','modified','added','deleted')}==delta['counts'],'Delta counts differ')
  require(''.join(diff).encode()==all_files['TANGENT_SESHADRI_30004324_V2_FROM_V1.patch'],'Regenerated patch differs')
  patched=t/'patched';shutil.copytree(original,patched)
  r=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(ROOT/'TANGENT_SESHADRI_30004324_V2_FROM_V1.patch')],cwd=patched,capture_output=True);require(r.returncode==0,'Zero-fuzz patch failed')
  require(inventory(patched)==v2,'Patched v2 bytes differ')
  for opt in (False,True):require(run(patched/'replay.py',optimized=opt)==expected,'Patched replay byte mismatch')
  require(inventory(original)==v1 and inventory(relocated)==v2,'Replay mutated original or relocated tree')
 require(inventory(ROOT)==all_files,'Replay mutated publication')
 print(json.dumps({'result':'PASS','problem_id':'30004324','status':'claimed_solved','turns':'2/5','scope':'complete candidate only; no geometry formal verification','packet_files':len(all_files),'original_files':13,'v2_files':27,'reconstructed_independent_audits':2,'author_finite_controls':909136,'independent_finite_controls':85247,'strict_mutations_rejected':14,'normal_and_optimized':True,'relocated_and_patched_replays_byte_exact':True,'historical_verifier_verdict':'REVISE_REQUIRED','publication_manifest_sha256':digest(manifest_raw)},indent=2,sort_keys=True))
if __name__=='__main__':main()
