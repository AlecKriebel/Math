#!/usr/bin/env python3
"""Strict complete publication inventory and byte-identical archive replay."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import zipfile

ANCHORS = {
 'author': ('EXCHANGEABLE_FACTORIZATIONS_30001176_AUTHOR_SAFE_FREEZE.zip',19258,'5ef49e21dcf98df08e666029d52644e5fad9cce431bdefef46eca56b6c0fbf37',12,'ac3dda15164e477a08030c32c9003b5efa048abc5a28166fa4bd876aa8120a29'),
 'audit': ('EXCHANGEABLE_FACTORIZATIONS_30001176_INDEPENDENT_AUDIT_SAFE.zip',21975,'4da5ad2f3aff078cfb837566046292132247199742e5cd6914ac6429416ed195',15,'15ef266535dc51c46c2940bf9937de67567057057e64f16bd74ce91c4a7aaf68'),
}
def require(value,message):
 if not value: raise RuntimeError(message)
def fingerprint(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def unique(pairs):
 result={}
 for key,value in pairs:
  require(key not in result,'duplicate JSON key: '+key); result[key]=value
 return result
def read_json(path):return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)
def inventory(root):
 files=set();dirs=set()
 def walk(folder):
  for path in folder.iterdir():
   name=path.relative_to(root).as_posix();mode=path.lstat().st_mode
   require(path.name!='__pycache__','cache inventory node')
   if stat.S_ISDIR(mode):dirs.add(name);walk(path)
   elif stat.S_ISREG(mode):files.add(name)
   else:raise RuntimeError('nonregular inventory node: '+name)
 walk(root)
 return files,dirs
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--integrity-only',action='store_true');args=parser.parse_args()
 root=Path(__file__).resolve().parent
 files,dirs=inventory(root)
 manifest=read_json(root/'PUBLICATION_MANIFEST.json');require(manifest.get('schema')==1,'manifest schema')
 entries=manifest['files'];require(isinstance(entries,dict),'manifest mapping')
 require(files==set(entries)|{'PUBLICATION_MANIFEST.json'},'complete file inventory mismatch')
 require(dirs==set(manifest['directories']),'complete directory inventory mismatch')
 for name,expected in entries.items():
  p=Path(name);require(not p.is_absolute() and '..' not in p.parts and p.as_posix()==name,'unsafe manifest path')
  require(fingerprint((root/name).read_bytes())==expected,'hash/size mismatch: '+name)
 pins=read_json(root/'PUBLICATION_CODE_PINS.json')['files']
 require(set(pins)=={'verify_publication.py','test_publication.py'},'publication code-pin inventory')
 for name,pin in pins.items(): require(fingerprint((root/name).read_bytes())==pin,'publication code pin: '+name)
 for folder,(name,size,sha,count,msha) in ANCHORS.items():
  archive=root/'archives'/name;require(fingerprint(archive.read_bytes())=={'bytes':size,'sha256':sha},'archive anchor: '+folder)
  require(fingerprint((root/folder/'MANIFEST.json').read_bytes())['sha256']==msha,'frozen manifest anchor: '+folder)
  with zipfile.ZipFile(archive) as z:
   infos=z.infolist();names=[i.filename for i in infos]
   require(len(infos)==count and len(set(names))==count,'ZIP member inventory: '+folder)
   require(set(names)=={p.name for p in (root/folder).iterdir()},'archive/directory inventory: '+folder)
   for i in infos:
    require(Path(i.filename).name==i.filename and i.filename not in ('','.','..'),'unsafe ZIP path')
    require(stat.S_ISREG(i.external_attr>>16),'nonregular ZIP member')
    require(z.read(i)==(root/folder/i.filename).read_bytes(),'ZIP/extracted byte mismatch: '+i.filename)
 verdict=read_json(root/'VERDICT.json')
 require(verdict['source_status']=='unsolved' and verdict['turns']=='1/5','source disposition')
 require(verdict['full_source_solved'] is False and verdict['unqualified_historical_conjecture_resolution'] is False,'scope overclaim')
 require(verdict['socket_fixture']=='ENV_DENIED_NOT_RUN','socket historical status')
 reports={}
 if not args.integrity_only:
  for folder,script,key,count in [('author','verify_package.py','finite_checks',2900842),('audit','verify_audit.py','independent_finite_checks',303279)]:
   cmd=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+[str(root/folder/script)]
   run=subprocess.run(cmd,cwd='/tmp',env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,timeout=180,check=False)
   require(run.returncode==0,folder+' replay failed: '+run.stderr.decode(errors='replace'))
   result=json.loads(run.stdout);require(result['status']=='PASS' and result[key]==count,folder+' replay result')
   reports[folder]=result
 print(json.dumps({'schema':1,'problem_id':30001176,'status':'PASS','scope':'Package integrity'+(' only' if args.integrity_only else ' and finite diagnostic replay')+'; not mathematical certification.','files':len(files),'directories':len(dirs),'source_status':'unsolved','turns':'1/5','frozen_archives_byte_identical':True,'replays':reports},sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as error:
  print('FAIL: '+str(error),file=sys.stderr);sys.exit(1)
