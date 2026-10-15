#!/usr/bin/env python3
import hashlib,json,os,stat,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
D=Path(__file__).resolve().parent; A=D.parents[1]; P=A/'publication'; REPO=A.parents[2]
PINS={'freeze':'c2c04a478b9f865655fb71b2b87945f01a2f4e41b4a78140e2eea42157f422cd','archive':'01f1568c27b41164903a599c86a82b431675f834c4d5d425f2f758a79fdecaa5','manifest':'b1881fcc385141e3f54a24dcc04cc35d4b76365a588cd18c2e832a4a4efb8364','pdf':'2dbc93a8666dce37eb250d4626106ae938cf7a7f2c6f113504c23d31f42a13d3','proof':'78be2da0b8831461e0268eb230cf47273a629a81a9dc2db997234f9fb5036464','original_manifest':'a7f24f30d76ca7e53da932dfc1f19deac67f13a675742175274e30ca767832f8'}
HEAD='704685791ec0053dc0a52590fdef49ed4aae61d9'; PREFIX='unsolved_math_prioritization/attempts/30002555/'
def require(x,s):
 if not x: raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def fp(p):
 require(stat.S_ISREG(p.lstat().st_mode),'nonregular '+str(p));b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def run(candidate=None):
 global P
 if candidate is not None:P=Path(candidate).resolve()
 branch=git('branch','--show-current').decode().strip();require(branch=='main','branch');idx=Path(git('rev-parse','--git-path','index').decode().strip());idx=idx if idx.is_absolute() else REPO/idx
 shared={'branch':branch,'head':git('rev-parse','HEAD').decode().strip(),'index':fp(idx)}
 freeze_raw=(P/'PREPUBLICATION_FREEZE.json').read_bytes();require(sha(freeze_raw)==PINS['freeze'],'freeze anchor');freeze=json.loads(freeze_raw);require(len(freeze['files'])==14,'14 freeze');frozen={}
 for name,r in freeze['files'].items():require(fp(P/name)==r,'freeze member '+name);frozen[name]=r
 archive=P/'rotational-veech-source-verification-v1.0.zip';require(fp(archive)['sha256']==PINS['archive'],'archive pin')
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();require(len(names)==134 and len(set(names))==134,'closed zip count');mraw=z.read('PACKAGE_MANIFEST.json');require(sha(mraw)==PINS['manifest'],'package anchor');m=json.loads(mraw);require(set(names)==set(m['files'])|{'PACKAGE_MANIFEST.json'} and len(m['files'])==133,'zip inventory');payloads={}
  for i in z.infolist():
   q=PurePosixPath(i.filename);require(not q.is_absolute() and q.as_posix()==i.filename and all(x not in ('','.','..') for x in i.filename.split('/')),'unsafe zip path');require(stat.S_ISREG(i.external_attr>>16),'zip nonregular')
   if i.filename!='PACKAGE_MANIFEST.json':
    b=z.read(i);r={'bytes':len(b),'sha256':sha(b)};require(r==m['files'][i.filename],'zip fingerprint');payloads[i.filename]=r
  files=git('ls-tree','-r','--name-only',HEAD,'--',PREFIX).decode().splitlines();require(len(files)==27,'git27');original={}
  diskfiles=set();diskdirs=set();origroot=A/'original'/PREFIX
  for folder,ds,ns in os.walk(origroot,followlinks=False):
   for name in ds+ns:
    item=Path(folder)/name;mode=item.lstat().st_mode;rel=item.relative_to(origroot).as_posix()
    if stat.S_ISDIR(mode):diskdirs.add(rel)
    else:require(stat.S_ISREG(mode),'original nonregular');diskfiles.add(PREFIX+rel)
  expected_dirs={p.as_posix() for name in files for p in PurePosixPath(name[len(PREFIX):]).parents if p.as_posix()!='.'}
  require(diskfiles==set(files) and diskdirs==expected_dirs,'original closed inventory')
  for name in files:
   b=git('show',HEAD+':'+name);require((A/'original'/name).read_bytes()==b,'original git '+name);require(z.read('original_packet/'+name[len(PREFIX):])==b,'zip original git '+name);original[name]={'bytes':len(b),'sha256':sha(b)}
  require(original[PREFIX+'public/PROOF.md']['sha256']==PINS['proof'],'proof pin');require(original[PREFIX+'PUBLICATION_MANIFEST.json']['sha256']==PINS['original_manifest'],'orig manifest pin')
  for src,dest in [('note.tex','note.tex'),('README.md','README.md'),('requirements.txt','requirements.txt'),('verify_package.py','verify_package.py'),('run_checked.py','run_checked.py'),('output/pdf/note.pdf','note.pdf')]:require((P/src).read_bytes()==z.read(dest),'candidate zip correspondence '+src)
 from datetime import datetime,timezone
 return {'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'candidate_pins':PINS,'shared':shared,'frozen_files':frozen,'archive_members':134,'payloads':payloads,'original_git_objects':original,'original_head':HEAD,'repository':str(REPO)}
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('output',nargs='?');ap.add_argument('--candidate',type=Path);args=ap.parse_args();r=run(args.candidate);target=Path(args.output) if args.output else None
 if target:target.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':r['status'],'original_git_files':len(r['original_git_objects']),'archive_members':r['archive_members'],'shared':r['shared']},indent=2))
