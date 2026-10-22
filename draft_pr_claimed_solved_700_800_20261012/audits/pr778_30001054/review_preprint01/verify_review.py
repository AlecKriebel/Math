"""Mtime-independent recursive custody for this fresh review; requires external seal."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,stat,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).absolute().parent
def need(x,m):
 if not x:raise ValueError(m)
def ident(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def unique(items):
 out={}
 for k,v in items:need(k not in out,'duplicate JSON key');out[k]=v
 return out
def parse(raw):return json.loads(raw,object_pairs_hook=unique)
def scan(root):
 need(stat.S_ISDIR(root.lstat().st_mode),'root not regular directory')
 files={};dirs=set()
 def visit(d,prefix=''):
  for e in os.scandir(d):
   name=prefix+e.name;mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):dirs.add(name);visit(Path(e.path),name+'/')
   else:
    need(stat.S_ISREG(mode),'symlink/special '+name)
    if name!='MANIFEST.json':files[name]=ident(Path(e.path).read_bytes())
 visit(root)
 expected={str(p) for n in files for p in PurePosixPath(n).parents if str(p)!='.'}
 need(dirs==expected,'unexpected/empty directory')
 return files
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--inputs',action='store_true');a=ap.parse_args()
raw=(ROOT/'MANIFEST.json').read_bytes();need(ident(raw)['sha256']==a.manifest_sha256,'external seal mismatch')
m=parse(raw);need(set(m)=={'schema','files'} and type(m['schema'])is int and m['schema']==1,'manifest schema')
for n,r in m['files'].items():
 need(type(n)is str and n and not PurePosixPath(n).is_absolute() and '\\' not in n and all(p not in ('','.','..') for p in n.split('/')) and n!='MANIFEST.json','unsafe path')
 need(set(r)=={'bytes','sha256'} and type(r['bytes'])is int and r['bytes']>=0 and type(r['sha256'])is str and len(r['sha256'])==64 and all(c in '0123456789abcdef' for c in r['sha256']),'invalid identity')
need(scan(ROOT)==m['files'],'file/inventory mismatch')
if a.inputs:
 b=parse((ROOT/'INPUT_BINDINGS.json').read_bytes())
 for n,r in b['six'].items():
  p=ROOT.parent/'preprint'/n;need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode),'input alias/special')
  need(ident(p.read_bytes())==r,'reviewed six changed '+n)
 need(ident((ROOT.parent/'private_sources/selected_record.json').read_bytes())['sha256']==b['selected_record_sha256'],'selected record changed')
print(json.dumps({'status':'PASS','authored_files':len(m['files']),'mtime_independent':True,'inputs_checked':a.inputs,'optimization':sys.flags.optimize},sort_keys=True))
