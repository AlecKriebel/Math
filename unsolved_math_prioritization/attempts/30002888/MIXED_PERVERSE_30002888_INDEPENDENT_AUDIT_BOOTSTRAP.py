"""Check the independently reviewed audit package without extracting or running it."""
import hashlib
import io
import json
import pathlib
import stat
import sys
import zipfile

ARCHIVE_SIZE = 12920
ARCHIVE_SHA = 'aa321a9ae8924ae198223e314d45706ac056ab8111de9d161b611ff71df43d95'
MANIFEST_SIZE = 1416
MANIFEST_SHA = '09389188505de2429983c79e3fa3b236d4a8643d0a68896cfd7137a52a1bf30d'
NAMES = {'acceptance.json','audit.md','integrity.json','source_check_metadata.json','verify_author_freeze.py'}
def need(c, m):
 if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(items):
 d={}
 for k,v in items:
  need(k not in d,'duplicate JSON key');d[k]=v
 return d
def bad_number(_):raise ValueError('nonfinite JSON')
def parse(b):return json.loads(b.decode('utf-8'),object_pairs_hook=pairs,parse_constant=bad_number)
def read(path,size,digest):
 p=pathlib.Path(path);need(not p.is_symlink(),'input symlink');need(p.is_file(),'input not regular');need(p.stat().st_size==size,'size mismatch');b=p.read_bytes();need(len(b)==size and sha(b)==digest,'identity mismatch');return b
try:
 need(len(sys.argv)==3,'usage: bootstrap.py AUDIT.zip MANIFEST.json')
 m=parse(read(sys.argv[2],MANIFEST_SIZE,MANIFEST_SHA));b=read(sys.argv[1],ARCHIVE_SIZE,ARCHIVE_SHA)
 need(m['archive']['sha256']==ARCHIVE_SHA and m['archive']['bytes']==ARCHIVE_SIZE,'manifest anchor')
 need(len(m['files'])==5,'manifest count');expect={x['path']:x for x in m['files']};need(set(expect)==NAMES,'manifest members')
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  names=z.namelist();need(len(names)==len(set(names))==5 and set(names)==NAMES,'ZIP membership')
  for i in z.infolist():
   need(i.filename==i.orig_filename and not i.is_dir(),'member name')
   need(not i.flag_bits&1,'encrypted member');mode=i.external_attr>>16
   need(stat.S_IFMT(mode) in (0,stat.S_IFREG),'member type');need(mode&0o111==0,'member executable bit')
   need(i.file_size==expect[i.filename]['bytes'],'member size')
   raw=z.read(i);need(len(raw)==expect[i.filename]['bytes'] and sha(raw)==expect[i.filename]['sha256'],'member identity');text=raw.decode('utf-8');need('\x00' not in text,'NUL')
   if i.filename.endswith('.json'):parse(raw)
  need(z.testzip() is None,'CRC mismatch')
 print(json.dumps({'ok':True,'archive_bytes':len(b),'archive_sha256':sha(b),'members_verified':5,'archive_code_executed':False},sort_keys=True))
except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as e:
 print(json.dumps({'ok':False,'error':str(e)},sort_keys=True));sys.exit(1)
