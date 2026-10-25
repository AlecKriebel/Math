"""Fresh ordinary HTTPS intake. No source program is executed."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
from io import BytesIO
import hashlib,json,stat,tarfile,urllib.request,zipfile,re
S=Path(__file__).resolve().parent;RID='22395326'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,x):(S/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
receipts=[]
def fetch(url,name):
 start=now();req=urllib.request.Request(url,headers={'User-Agent':'IndependentResearchSourceIntake/1.0','Accept-Encoding':'identity'})
 with urllib.request.urlopen(req,timeout=90) as r:
  data=r.read(100000001)
  if len(data)>100000000:raise RuntimeError('download_bound')
  receipt={'requested_url':url,'started_utc':start,'completed_utc':now(),'status':r.status,'reason':r.reason,'final_url':r.url,'response_http_version':r.version,'response_headers_in_original_order':list(r.getheaders()),'path':str(S/name),'bytes':len(data),'sha256':sha(data)}
 (S/name).write_bytes(data);receipts.append(receipt);save('api-receipts.json',receipts);return data
if (S/'SOURCE_READY.json').exists():raise RuntimeError('immutable_source_ready_exists')
raw=fetch('https://zenodo.org/api/records/'+RID,'record.raw.json');api=json.loads(raw)
latest=json.loads(fetch(api['links']['latest'],'latest.raw.json'))
versions=json.loads(fetch(api['links']['versions'],'versions.raw.json'))
if str(api['id'])!=RID or api['status']!='published':raise RuntimeError('wrong_actual_record')
assets=[]
for obj in api['files']:
 name=obj['key']
 if Path(name).name!=name or name in ('','.','..') or '\\'in name:raise RuntimeError('asset_basename')
 data=fetch(obj['links']['self'],name);md5=hashlib.md5(data).hexdigest()
 if len(data)!=obj['size'] or obj['checksum']!='md5:'+md5:raise RuntimeError('actual_API_size_checksum_mismatch')
 assets.append({'original_api_file_object':obj,'path':str(S/name),'bytes':len(data),'md5':md5,'sha256':sha(data)})
save('actual-assets.json',assets)
rows=[];containers=[];expanded=0
def relative(name,isdir=False):
 original=name;name=name[:-1] if isdir and name.endswith('/') else name;p=PurePosixPath(name)
 if not name or p.is_absolute() or '..'in p.parts or '.'in p.parts or str(p)!=name or '\\'in name or re.match(r'^[A-Za-z]:',name) or '\x00'in name:raise RuntimeError('unsafe_member:'+original)
 return name

def kind(data,name):
 if zipfile.is_zipfile(BytesIO(data)):return 'zip'
 if name.lower().endswith(('.tar','.tar.gz','.tgz','.tar.bz2','.tbz2','.tar.xz','.txz')):
  try:
   with tarfile.open(fileobj=BytesIO(data),mode='r:*'):return 'tar'
  except tarfile.TarError:raise RuntimeError('named_tar_not_readable:'+name)
 return None

def visit(data,container,base,depth,k):
 global expanded
 if depth>8 or len(containers)>=100:raise RuntimeError('archive_recursion_bound')
 containers.append({'container':container,'kind':k,'depth':depth,'bytes':len(data),'sha256':sha(data),'extraction_root':str(base)})
 seen=set();payloads=[]
 if k=='zip':
  with zipfile.ZipFile(BytesIO(data)) as z:
   for info in z.infolist():
    name=relative(info.filename,info.is_dir())
    if name in seen:raise RuntimeError('duplicate_canonical_path:'+container+'::'+name)
    seen.add(name)
    if info.is_dir():continue
    mode=info.external_attr>>16
    if info.flag_bits&1 or stat.S_ISLNK(mode) or stat.S_IFMT(mode) not in (0,stat.S_IFREG):raise RuntimeError('nonregular_or_encrypted')
    if info.file_size>50000000:raise RuntimeError('member_bound')
    b=z.read(info);payloads.append((name,b,{'CRC32':f'{info.CRC:08x}','compressed_bytes':info.compress_size}))
 else:
  with tarfile.open(fileobj=BytesIO(data),mode='r:*') as t:
   for info in t:
    name=relative(info.name,info.isdir())
    if name in seen:raise RuntimeError('duplicate_canonical_path:'+container+'::'+name)
    seen.add(name)
    if info.isdir():continue
    if not info.isfile() or info.issym() or info.islnk() or info.size>50000000:raise RuntimeError('nonregular_tar')
    b=t.extractfile(info).read();payloads.append((name,b,{'tar_type':info.type.decode('ascii','backslashreplace'),'tar_header_checksum':info.chksum}))
 for name,b,extra in payloads:
  expanded+=len(b)
  if expanded>100000000:raise RuntimeError('total_expansion_bound')
  path=base/name
  if not path.resolve().is_relative_to(S.resolve()):raise RuntimeError('extraction_escape')
  row={'container':container,'member':name,'extracted_path':str(path),'bytes':len(b),'sha256':sha(b),'safe_regular_member':True,**extra};rows.append(row)
  path.parent.mkdir(parents=True,exist_ok=True)
  if path.exists():raise RuntimeError('never_overwrite_extraction')
  path.write_bytes(b)
  nested=kind(b,name)
  if nested:visit(b,container+'::'+name,S/'nested-source'/sha((container+'::'+name).encode())[:16],depth+1,nested)
for x in assets:
 name=x['original_api_file_object']['key'];data=(S/name).read_bytes();k=kind(data,name)
 if k:visit(data,name,S/'published-source'/name,0,k)
save('archive-members.json',{'UTC':now(),'all_containers':containers,'container_count':len(containers),'safe_regular_member_occurrences':len(rows),'expanded_bytes_all_depths':expanded,'all_ZIP_CRC_payloads_read':True,'members':rows})
print(json.dumps({'status':'ACTUAL_API_ASSETS_AND_SAFE_ARCHIVES_ACQUIRED','title':api['metadata']['title'],'assets':assets,'archive_containers':len(containers),'regular_member_occurrences':len(rows),'expanded_bytes':expanded},indent=2))
