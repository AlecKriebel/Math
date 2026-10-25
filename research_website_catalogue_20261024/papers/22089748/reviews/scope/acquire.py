"""Acquire all selected public assets and extract regular tar members safely.
This script does not execute downloaded code or read reviewer verdicts.
"""
from pathlib import Path,PurePosixPath
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import gzip,hashlib,io,json,tarfile,urllib.request

BASE=Path(__file__).resolve().parents[2]
SRC=BASE/'sources'
def digest(data,kind='sha256'):return hashlib.new(kind,data).hexdigest()
record=json.loads((SRC/'record.json').read_text())
queue_expect={
 'complete_graph_extremality_db.pdf':(235224,'0dd3aa46eb01b9f2881843f5d777525d'),
 'complete_graph_extremality_db_source_and_certificates.tar.gz':(394499,'1c3cea054cd7b3c3ba1e7f8fa7d76e7c'),
 'complete_graph_extremality_db_source_and_certificates.tar.gz.sha256':(127,'a35551545b833b4d0ff969cde3c19a0a'),
 'paper_i_complete_graph_extremality_referee_package_2026-08-23_r4.tar.gz':(1041551,'216d015a113cd3facd5213e6bd7f8bba'),
 'paper_i_complete_graph_extremality_referee_package_2026-08-23_r4.tar.gz.sha256':(138,'e417277974f2ca3ca0053ea8abd47be7')}
assert set(f['key'] for f in record['files'])==set(queue_expect)
def acquire(f):
 name=f['key'];url=f['links']['self']
 with urllib.request.urlopen(url,timeout=45) as response:data=response.read()
 expected_size,expected_md5=queue_expect[name]
 assert len(data)==f['size']==expected_size
 assert digest(data,'md5')==f['checksum'].removeprefix('md5:')==expected_md5
 if name.endswith('.pdf'):assert digest(data)=='ec8c09fbc4ef5f382272351f69721b6544c69f5d48bee961447e1907de2c0180'
 path=SRC/name
 assert not path.exists(),name
 path.write_bytes(data)
 return {'name':name,'url':url,'bytes':len(data),'sha256':digest(data),'zenodo_checksum':f['checksum'],'queue_md5_match':True,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
with ThreadPoolExecutor(max_workers=5) as pool:files=list(pool.map(acquire,record['files']))
tar_receipts=[]
for f in files:
 if not f['name'].endswith('.tar.gz'):continue
 archive=SRC/f['name']; expected_line=(SRC/(f['name']+'.sha256')).read_text().strip().split()
 assert len(expected_line)==2 and expected_line[0]==f['sha256'] and Path(expected_line[1].lstrip('*')).name==f['name']
 raw=gzip.decompress(archive.read_bytes()) # verifies gzip CRC32 and uncompressed size
 assert len(raw)<250_000_000
 dest=SRC/'published-source'/f['name'].removesuffix('.tar.gz');dest.mkdir(parents=True,exist_ok=False)
 members=[];seen=set()
 with tarfile.open(fileobj=io.BytesIO(raw),mode='r:') as tar:
  infos=tar.getmembers();assert len(infos)<10000
  for info in infos:
   path=PurePosixPath(info.name)
   assert not path.is_absolute() and '..' not in path.parts and '\\' not in info.name
   assert info.isdir() or info.isfile(),(info.name,'link or special tar member rejected')
   assert path.as_posix() not in seen;seen.add(path.as_posix())
   assert 0<=info.size<100_000_000
   target=dest.joinpath(*path.parts)
   assert target.resolve().is_relative_to(dest.resolve())
   if info.isdir():target.mkdir(parents=True,exist_ok=True);continue
   data=tar.extractfile(info).read();assert len(data)==info.size
   target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
   members.append({'path':str(target.relative_to(SRC)),'bytes':len(data),'sha256':digest(data),'tar_header_checksum':info.chksum})
 tar_receipts.append({'name':f['name'],'gzip_crc_verified':True,'tar_headers_verified':True,'published_sha256_sidecar_verified':True,'uncompressed_bytes':len(raw),'regular_member_count':len(members),'members':members})
receipt={'record_id':'22089748','retrieved_utc':datetime.now(timezone.utc).isoformat(),'record_url':'https://zenodo.org/api/records/22089748','record_metadata_sha256':digest((SRC/'record.json').read_bytes()),'files':files,'archives':tar_receipts,'related_metadata':[{'record_id':'21753405','url':'https://zenodo.org/api/records/21753405','filename':'related-record-21753405.json','sha256':digest((SRC/'related-record-21753405.json').read_bytes()),'purpose':'Historical release metadata only; its 455MB repository archive is not an asset of the selected paper and was not acquired.'}]}
(SRC/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'files':files,'archives':[{k:v for k,v in a.items() if k!='members'} for a in tar_receipts]},indent=2))
