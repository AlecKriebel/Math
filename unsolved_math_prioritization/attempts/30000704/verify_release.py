#!/usr/bin/env python3
"""Portable fail-closed verification of the corrected, bound partial-result package."""
from pathlib import Path, PurePosixPath
import hashlib,json,os,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
ARCHIVES={
 'author-packet.zip':(22660,'ea164a4cbc04f39fcb2f1f398ea84e4b44d79e01beb2686681503b029327ab84','', 'safe'),
 'audit-packet.zip':(19126,'2ec19fe3239a01c2c0d606c7ff07abf47e60b0250f31c1abe4daa85a3485ef16','rank660-30000704-audit-safe/', 'audit')}
PINS={'safe/SHA256SUMS.json':'860f342d02acf761c40c3bca59f959fd1e4e3d3e7c028292ccdcf7b3dca46255','audit/SHA256SUMS.json':'9c4374c53cb79c667566b592f07b5168340b89bc37787b84c6c3e0430a019184','audit/CORRECTIONS.md':'444cd56afbc9497bf5d20c17e4257a548417feedb9af2afbb6f3e27750c17f92'}
def require(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def inventory(root):
 result=set()
 for p in root.rglob('*'):
  require(not p.is_symlink(),'symlink rejected')
  require(p.is_file() or p.is_dir(),'special file rejected')
  if p.is_file():result.add(p.relative_to(root).as_posix())
 return result
def run(p,*args):
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
 return subprocess.run([sys.executable,'-B',str(p),*map(str,args)],cwd=p.parent,env=env,capture_output=True,check=True).stdout
def main():
 require(sys.flags.optimize==0,'Use unoptimized Python; -O/-OO/PYTHONOPTIMIZE rejected')
 rows=json.loads((ROOT/'RELEASE_MANIFEST.json').read_text())['files'];names=[x['path'] for x in rows]
 require(len(names)==len(set(names)),'duplicate manifest path')
 for name in names:
  p=PurePosixPath(name);require(not p.is_absolute() and '..' not in p.parts and str(p)==name,'unsafe manifest path')
 require(inventory(ROOT)==set(names)|{'RELEASE_MANIFEST.json'},'release inventory mismatch')
 for row in rows:
  b=(ROOT/row['path']).read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'],'release hash/size mismatch: '+row['path'])
 for name,pin in PINS.items():require(sha((ROOT/name).read_bytes())==pin,'frozen pin mismatch: '+name)
 archive_counts={}
 for name,(size,pin,prefix,dest) in ARCHIVES.items():
  b=(ROOT/name).read_bytes();require(len(b)==size and sha(b)==pin,'frozen archive mismatch')
  with zipfile.ZipFile(ROOT/name) as z:
   zn=z.namelist();require(len(zn)==len(set(zn)),'duplicate archive member')
   require(set(zn)=={prefix+p[len(dest)+1:] for p in names if p.startswith(dest+'/')},'archive member set mismatch')
   for info in z.infolist():
    p=PurePosixPath(info.filename);require(not p.is_absolute() and '..' not in p.parts and str(p)==info.filename,'unsafe archive path')
    require((info.external_attr>>16)&0o170000!=0o120000,'archive symlink')
    require(z.read(info)==(ROOT/dest/info.filename[len(prefix):]).read_bytes(),'archive/extracted bytes mismatch')
   archive_counts[name]=len(zn)
 s=json.loads((ROOT/'safe/STATUS.json').read_text());require(s['substantive_approaches']==5 and s['maximum_approaches']==5 and not s['full_resolution'] and not s['claimed_solved'] and not s['novelty_established'],'wrong status')
 turns=[json.loads(x) for x in (ROOT/'safe/turns.jsonl').read_text().splitlines()];require([t['approach_number'] for t in turns]==list(range(1,6)),'wrong turns')
 correction=(ROOT/'audit/CORRECTIONS.md').read_text().split('Replace the abbreviated statement with:\n\n')[1].split('\n\nReason:')[0]
 guide=(ROOT/'README.md').read_text();require(correction in guide and 'audit/CORRECTIONS.md#c1-' in guide and 'controls and supersedes' in guide,'missing controlling correction')
 author_manifest=json.loads(run(ROOT/'safe/verify_manifest.py'));audit_manifest=json.loads(run(ROOT/'audit/verify_audit.py',ROOT/'safe'))
 author=run(ROOT/'safe/controls/verify.py');independent=run(ROOT/'audit/controls/adversarial.py')
 require(author==(ROOT/'safe/CONTROL_RESULTS.json').read_bytes()==(ROOT/'audit/AUTHOR_CONTROL_REPLAY.json').read_bytes(),'author replay changed')
 require(independent==(ROOT/'audit/ADVERSARIAL_RESULTS.json').read_bytes(),'independent replay changed')
 with tempfile.TemporaryDirectory(prefix='conformal-replay-') as tmp:
  out=Path(tmp)
  for name,(_,_,prefix,dest) in ARCHIVES.items():
   with zipfile.ZipFile(ROOT/name) as z:
    for member in z.namelist():
     p=out/dest/member[len(prefix):];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(member))
  run(out/'safe/verify_manifest.py');run(out/'audit/verify_audit.py',out/'safe')
  require(run(out/'safe/controls/verify.py')==author,'fresh author replay changed');require(run(out/'audit/controls/adversarial.py')==independent,'fresh audit replay changed')
 print(json.dumps({'status':'PASS','problem_id':30000704,'queue_status':'unsolved','turns':'5/5','full_resolution':False,'required_C1_included_and_controlling':True,'files_verified':len(rows),'archive_members':archive_counts,'author_manifest':author_manifest,'audit_manifest':audit_manifest,'author_controls':22,'independent_controls':27,'control_outputs':'byte-identical','clean_archive_replay':'PASS','assertions_enabled':True},sort_keys=True,indent=2))
if __name__=='__main__':main()
