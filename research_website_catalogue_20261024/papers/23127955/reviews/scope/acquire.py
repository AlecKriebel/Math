from pathlib import Path,PurePosixPath
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess,zipfile,stat,datetime
b=Path(__file__).resolve().parents[2];s=b/'sources';r=b/'reviews/scope'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def download(url,p):
 assert not p.exists(),p
 proc=subprocess.run(['curl','--location','--fail','--silent','--show-error','--max-time','90','--output',str(p),'--write-out','%{url_effective}',url],capture_output=True,text=True)
 if proc.returncode:raise RuntimeError(proc.stderr)
 return proc.stdout
recordurl='https://zenodo.org/api/records/23127955';download(recordurl,s/'record.json');rec=json.loads((s/'record.json').read_text())
expected={'common_tangent_nullness.pdf':(92307,'5a3ab7736863fb3ad1ecedb55c2c7fde','80b3fc3e8cb470a22a1226b960467de9e67dd8c3ccf054b42133d9ba0ce9d327'),'common_tangents_null_locus_v1.zip':(182613,'c7d2f5ba160186731fbc377e441d2953',None)}
assert set(expected)=={x['key'] for x in rec['files']}
def get(f):
 name=f['key'];url=f['links'].get('content') or f['links']['self'];p=s/name;resolved=download(url,p);data=p.read_bytes();md5=hashlib.md5(data).hexdigest();sz,h,hsha=expected[name]
 assert len(data)==sz==f['size'];assert f['checksum']=='md5:'+md5 and md5==h
 if hsha:assert sha(p)==hsha
 return {'name':name,'url':url,'resolved_url':resolved,'bytes':len(data),'md5':md5,'zenodo_checksum':f['checksum'],'sha256':sha(p),'retrieved_utc':now(),'queue_integrity':'PASS'}
with ThreadPoolExecutor(max_workers=2) as pool:files=list(pool.map(get,rec['files']))
archives=[]
for item in files:
 if not item['name'].endswith('.zip'):continue
 p=s/item['name'];out=s/'published-source';out.mkdir(exist_ok=True)
 with zipfile.ZipFile(p) as z:
  info=z.infolist();assert len(info)<10000;assert sum(x.file_size for x in info)<250_000_000
  seen=set();members=[]
  for x in info:
   name=x.filename;parts=PurePosixPath(name).parts;assert parts and not name.startswith('/') and '\\' not in name and '..' not in parts and ':' not in name
   assert name not in seen;seen.add(name);mode=x.external_attr>>16
   assert not stat.S_ISLNK(mode);assert stat.S_IFMT(mode) in (0,stat.S_IFREG,stat.S_IFDIR);assert x.file_size<100_000_000
   q=out.joinpath(*parts)
   if x.is_dir():q.mkdir(parents=True,exist_ok=True);continue
   data=z.read(x);assert len(data)==x.file_size # read validates CRC32
   q.parent.mkdir(parents=True,exist_ok=True);assert not q.exists();q.write_bytes(data)
   members.append({'path':str(q.relative_to(s)),'bytes':len(data),'crc32':f'{x.CRC:08x}','sha256':sha(q)})
  assert z.testzip() is None
 archives.append({'name':p.name,'crc_verified':True,'safe_member_paths':True,'links_special_nodes_rejected':True,'regular_files':len(members),'members':members})
receipt={'record_id':'23127955','complete':True,'retrieved_utc':now(),'record_url':recordurl,'record_sha256':sha(s/'record.json'),'files':files,'archives':archives}
(s/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
(r/'RESEARCH_LOG.md').write_text('# Acquisition and scope — 23127955\n\n## '+now()+' — 15%\n\nFresh metadata and both assets acquired from public Zenodo, matched queue/current sizes and MD5 and queued PDF SHA-256, computed complete SHA-256 bindings. ZIP CRC and bounded safe extraction passed. No historical opinions, source-code replay or mathematical verdict consulted. Sources ready for separate mathematical reviewers.\n')
print(json.dumps({'record':rec['metadata'],'files':files,'archives':[{'name':a['name'],'regular_files':a['regular_files']} for a in archives]},indent=2))
