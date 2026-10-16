#!/usr/bin/env python3
"""Read-only Git/disk authentication of the complete immutable 27-file packet."""
import argparse, datetime, hashlib, json, os, stat, subprocess
from pathlib import Path
HEAD='704685791ec0053dc0a52590fdef49ed4aae61d9'
PREFIX='unsolved_math_prioritization/attempts/30002555/'
EXTERNAL={
 'public/PROOF.md':'78be2da0b8831461e0268eb230cf47273a629a81a9dc2db997234f9fb5036464',
 'public/MANIFEST.json':'f7b959531c352611c5c9b9d0c2cb57bcb865de9399d65dbd66c4fabef3a88e59',
 'PUBLICATION_MANIFEST.json':'a7f24f30d76ca7e53da932dfc1f19deac67f13a675742175274e30ca767832f8',
 'VERIFY_PUBLICATION.py':'07ed9f87820a8cbaa10deec92fbf14b68a61e969e8bf849d8c5484eac4aa5374'}
def need(v,m):
 if not v: raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(repo,*args):return subprocess.run(['git','-C',str(repo),*args],check=True,capture_output=True).stdout
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--packet',required=True);p.add_argument('--snapshot',required=True);p.add_argument('--pinset',required=True);p.add_argument('--phase',choices=['start','end'],required=True);p.add_argument('--output',required=True);a=p.parse_args()
 root=Path(a.packet); need(root.is_absolute() and str(root)==os.path.realpath(root),'Noncanonical root')
 for x in [root,*root.parents]:need(stat.S_ISDIR(x.lstat().st_mode),'Symlink/non-directory ancestor')
 entries=git(a.repo,'ls-tree','-r','-z',HEAD,'--',PREFIX).split(b'\0');files={}
 for e in entries:
  if not e:continue
  meta,rawpath=e.split(b'\t',1);mode,typ,blob=meta.decode().split();path=rawpath.decode();need(mode in ('100644','100755') and typ=='blob','Nonregular Git member');name=path[len(PREFIX):];data=git(a.repo,'cat-file','blob',blob);files[name]={'bytes':len(data),'sha256':sha(data),'git_mode':mode,'git_blob':blob}
 need(len(files)==27,'Git count not 27')
 disk={};dirs=set()
 for directory,subdirs,names in os.walk(root,followlinks=False):
  for name in subdirs+names:
   x=Path(directory)/name;r=x.relative_to(root).as_posix();mode=x.lstat().st_mode
   if stat.S_ISDIR(mode):dirs.add(r)
   else:
    need(stat.S_ISREG(mode),'Nonregular/symlink member '+r);disk[r]=x.read_bytes()
 expected_dirs={str(x) for n in files for x in Path(n).parents if str(x)!='.'}
 need(set(disk)==set(files) and dirs==expected_dirs,'Closed inventory mismatch')
 for n,meta in files.items():need(len(disk[n])==meta['bytes'] and sha(disk[n])==meta['sha256'],'Git/disk mismatch '+n)
 snapshot=json.loads(Path(a.snapshot).read_bytes());need(snapshot['head']==HEAD and len(snapshot['files'])==27,'Snapshot identity mismatch')
 need({PREFIX+n:m['sha256'] for n,m in files.items()}==snapshot['files'],'Supplied snapshot differs from actual Git')
 for n,h in EXTERNAL.items():need(files[n]['sha256']==h,'External pin mismatch '+n)
 pins={'schema':'pr919-computation-immutable-git-v1','head':HEAD,'problem_id':30002555,'git_prefix':PREFIX,'files':files}
 pinraw=(json.dumps(pins,indent=2,sort_keys=True)+'\n').encode();pinpath=Path(a.pinset)
 if a.phase=='start':pinpath.write_bytes(pinraw)
 else:need(pinpath.read_bytes()==pinraw,'Pinset changed or Git mismatch')
 report={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':a.phase,'immutable_head':HEAD,'actual_git_files':len(files),'actual_disk_files':len(disk),'actual_disk_directories':sorted(dirs),'git_disk_supplied_snapshot_external_pins_agree':True,'pinset_sha256':sha(pinraw),'current_branch':git(a.repo,'branch','--show-current').decode().strip(),'current_head':git(a.repo,'rev-parse','HEAD').decode().strip(),'files':files}
 need(report['current_branch']=='main','Branch is not main')
 Path(a.output).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2,sort_keys=True))
if __name__=='__main__':main()
