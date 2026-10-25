from pathlib import Path
from urllib.request import Request,urlopen
import json,struct,hashlib,zlib,datetime
base=Path(__file__).resolve().parent;cache=base/'reading-cache'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def get(url,a,b):
 with urlopen(Request(url,headers={'Range':f'bytes={a}-{b}','User-Agent':'Research catalogue verification'}),timeout=60) as r:
  assert r.status==206 and r.headers.get('Content-Range','').startswith(f'bytes {a}-{b}/');d=r.read(b-a+2);assert len(d)==b-a+1;return d
rows=[]
for rid in (21753405,21850042,21852072):
 f=json.load(open(cache/f'zenodo{rid}.json'))['files'][0];url=f['links']['self'];size=f['size'];tail=get(url,size-65536,size-1);idx=tail.rfind(b'PK\x05\x06');e=struct.unpack_from('<4s4H2LH',tail,idx);cdsize,off=e[5:7];cd=get(url,off,off+cdsize-1);(cache/f'{rid}-central.bin').write_bytes(cd)
 members=[];p=0
 while p<len(cd):
  z=struct.unpack_from('<4s6H3L5H2L',cd,p);assert z[0]==b'PK\x01\x02';fn,ex,co=z[10:13];name=cd[p+46:p+46+fn].decode('utf-8');members.append({'name':name,'method':z[4],'crc32':z[7],'compressed_bytes':z[8],'bytes':z[9],'local_offset':z[16]});p+=46+fn+ex+co
 (cache/f'{rid}-central.json').write_text(json.dumps(members,indent=2)+'\n')
 print(rid,'members',len(members),'cdsha',hashlib.sha256(cd).hexdigest(),flush=True)
 for m in members:
  if m['name'].endswith(('.pdf','.tex')) and 'universal_simultaneous_amplification/phase4_landmark_closure/' in m['name'] and ('paper_' in m['name'] or '/manuscript/' in m['name']):print(m['name'],m['bytes'],flush=True)
 rows.append({'record_id':rid,'url':url,'archive_bytes':size,'declared_archive_md5':f['checksum'],'read_method':'HTTP 206 central directory only; whole-archive MD5 not checked','central_directory_sha256':hashlib.sha256(cd).hexdigest(),'members':len(members),'retrieved_utc':now()})
(base/'prior_archive_interface_ledger.json').write_text(json.dumps(rows,indent=2)+'\n')
