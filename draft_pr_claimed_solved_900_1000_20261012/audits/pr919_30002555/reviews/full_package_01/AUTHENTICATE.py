#!/usr/bin/env python3
"""Read-only candidate authentication against independently supplied anchors and Git objects."""
import argparse, datetime, hashlib, json, os, stat, subprocess, sys, zipfile
from pathlib import Path, PurePosixPath
R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr919_30002555'
P=A/'publication/reviewed_candidates/candidate01'
HEAD='704685791ec0053dc0a52590fdef49ed4aae61d9'
F='416e87c09e37e7cc8ef5e03fe7a725f4300ba6e9c362b1ea4ba920ba6b80ecf1'
M='e2b2f091451dddc4e69032d05ba94b46fddaf49bd9e610f61a43692cb2ffc487'
Z='5ee644529e25b3ef47e39680a362bff8af2bb6d7d3739643a4280071586afb68'
def need(v,m):
 if not v: raise RuntimeError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p):
 need(stat.S_ISREG(p.lstat().st_mode),f'not regular: {p}')
 return p.read_bytes()
def git(*args): return subprocess.check_output(['git','-C',str(R),*args])
def run(candidate=None):
 global P
 if candidate is not None: P=Path(candidate).absolute()
 fb=read(P/'PREPUBLICATION_FREEZE.json'); need(sha(fb)==F,'freeze anchor'); f=json.loads(fb)
 need(len(f['files'])==14,'freeze file count')
 files={}
 for name,meta in f['files'].items():
  b=read(P/name); need(len(b)==meta['bytes'] and sha(b)==meta['sha256'],f'freeze payload {name}'); files[name]=meta
 snap=json.loads(read(A/'ORIGINAL_SNAPSHOT.json')); need(snap['head']==HEAD,'snapshot head')
 prefix='unsolved_math_prioritization/attempts/30002555/'
 gt=git('ls-tree','-r','--name-only',HEAD,'--',prefix).decode().splitlines()
 need(set(gt)==set(snap['files']) and len(gt)==27,'Git closed original inventory')
 original={}
 for name,digest in snap['files'].items():
  b=read(A/'original'/name); g=git('show',f'{HEAD}:{name}')
  need(b==g and sha(g)==digest,f'original Git payload {name}')
  original[name]={'bytes':len(b),'sha256':sha(b),'git_blob':git('rev-parse',f'{HEAD}:{name}').decode().strip()}
 disk={str(p.relative_to(A/'original')) for p in (A/'original').rglob('*') if not p.is_dir()}
 need(disk==set(gt),'closed original disk inventory')
 zb=read(P/'rotational-veech-source-verification-v1.0.zip');need(sha(zb)==Z,'zip anchor')
 with zipfile.ZipFile(P/'rotational-veech-source-verification-v1.0.zip') as z:
  names=z.namelist();need(len(names)==len(set(names))==129,'zip duplicate/count')
  need(all(not n.endswith('/') and str(PurePosixPath(n))==n and not n.startswith('/') and '..' not in PurePosixPath(n).parts for n in names),'zip canonical inventory')
  for x in z.infolist(): need(stat.S_IFMT(x.external_attr>>16) in (0,stat.S_IFREG),'zip special entry')
  mb=z.read('PACKAGE_MANIFEST.json'); need(sha(mb)==M,'package manifest external anchor'); manifest=json.loads(mb)
  need(set(names)==set(manifest['files'])|{'PACKAGE_MANIFEST.json'},'closed zip inventory')
  for n,m in manifest['files'].items():
   b=z.read(n);need(len(b)==m['bytes'] and sha(b)==m['sha256'],f'zip payload {n}')
  for n in gt: need(z.read('original_packet/'+n.removeprefix(prefix))==git('show',f'{HEAD}:{n}'),f'zip original Git {n}')
  need(z.read('note.pdf')==read(P/'output/pdf/note.pdf'),'separate PDF equal')
 helpers=json.loads(read(Path(__file__).resolve().parent/'HELPER_INSPECTION.json'))['inspected_helpers']
 for n,m in helpers.items():
  b=read(Path(__file__).resolve().parent/m['review_copy']);g=git('show',m['checkpoint_commit']+':'+m['repository_path'])
  need(b==g and len(b)==m['bytes'] and sha(b)==m['sha256'],f'inspected future helper {n}')
 return {'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'freeze_sha256':F,'original_head':HEAD,'freeze_files':files,'original_files':original,'archive_sha256':Z,'package_manifest_sha256':M,'archive_members':129,'archive_payloads':128,'all_originals_git_and_disk_and_archive_equal':True,'helpers':helpers,'branch':git('branch','--show-current').decode().strip(),'index_sha256':sha(read(Path(git('rev-parse','--git-path','index').decode().strip()).absolute()))}
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate',type=Path,default=P);ap.add_argument('--output',type=Path);args=ap.parse_args()
 result=run(args.candidate); data=json.dumps(result,indent=2)+'\n'
 if args.output: args.output.write_text(data)
 else: print(data,end='')
