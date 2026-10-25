"""Fresh official record acquisition with immutable asset and safe ZIP receipts."""
from pathlib import Path, PurePosixPath
import datetime,hashlib,json,stat,urllib.request,zipfile
P=Path(__file__).resolve().parents[2]
S=P/'sources';S.mkdir(exist_ok=True)
assert not (S/'receipt.json').exists(), 'Do not overwrite completed acquisition'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b):return hashlib.sha256(b).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 research-publication-source-review'})
 with urllib.request.urlopen(req,timeout=60) as r:return r.read(),r.url
url='https://zenodo.org/api/records/23387814';body,resolved=fetch(url);record=json.loads(body)
assert str(record['id'])=='23387814'
(S/'record.json').write_bytes(body)
save(S/'metadata-receipt.json',{'url':url,'resolved_url':resolved,'retrieved_utc':utc(),'bytes':len(body),'sha256':digest(body)})
files=[];archive_results=[]
for item in record['files']:
 name=item['key'];assert PurePosixPath(name).name==name and name not in ('.','..')
 f=S/name;assert not f.exists()
 data,final=fetch(item['links']['self']);md5=hashlib.md5(data).hexdigest()
 assert len(data)==item['size'];assert item['checksum']=='md5:'+md5
 f.write_bytes(data)
 files.append({'name':name,'url':item['links']['self'],'resolved_url':final,'retrieved_utc':utc(),'bytes':len(data),'md5':md5,'zenodo_checksum':item['checksum'],'sha256':digest(data),'integrity':'PASS'})
 if name.endswith('.zip'):
  dest=S/'published-source';dest.mkdir(exist_ok=True)
  members=[];names=set()
  with zipfile.ZipFile(f) as z:
   info=z.infolist();assert len(info)<=10000 and sum(i.file_size for i in info)<=500_000_000
   for i in info:
    n=PurePosixPath(i.filename);assert not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename
    assert i.filename not in names;names.add(i.filename)
    mode=i.external_attr>>16;assert not stat.S_ISLNK(mode)
    assert stat.S_IFMT(mode) in (0,stat.S_IFREG,stat.S_IFDIR)
    target=dest.joinpath(*n.parts);assert target.resolve().is_relative_to(dest.resolve())
    if i.is_dir():target.mkdir(parents=True,exist_ok=True);continue
    b=z.read(i);assert len(b)==i.file_size
    target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();target.write_bytes(b)
    members.append({'path':i.filename,'bytes':len(b),'sha256':digest(b),'crc32':format(i.CRC,'08x'),'archive_crc_read':'PASS'})
   assert z.testzip() is None
  archive_results.append({'archive':name,'archive_sha256':digest(data),'safe_paths_and_types':'PASS','members':members})
save(S/'extraction-integrity.json',archive_results)
save(S/'receipt.json',{'record_id':'23387814','complete':True,'retrieved_utc':utc(),'record_sha256':digest(body),'files':files})
print(json.dumps({'status':'ACQUIRED','title':record['metadata']['title'],'version':record['metadata'].get('version'),'publication_date':record['metadata']['publication_date'],'files':files,'extracted_files':sum(len(x['members']) for x in archive_results)},ensure_ascii=False,indent=2))
