from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import urllib.request,json,hashlib,zipfile,stat,os
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');P=B/'papers/23444606';S=P/'sources';R=P/'reviews/scope'
def now():return datetime.now(timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def save(n,x):n.write_text(json.dumps(x,indent=2)+'\n')
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'ResearchSourceAudit/1.0'})
 with urllib.request.urlopen(req,timeout=60) as r:return r.read(),r.geturl(),r.status,dict(r.headers)
def walk(x):
 if isinstance(x,dict):
  if x.get('record_id')==23444606 and 'sources' in x:return x
  for v in x.values():
   z=walk(v)
   if z:return z
 elif isinstance(x,list):
  for v in x:
   z=walk(v)
   if z:return z
q=walk(json.loads((B/'reconciliation/queue.json').read_text()));save(R/'queue_identity.json',q)
(R/'RESEARCH_LOG.md').write_text('# Initial omnific models — acquisition and scope\n\n'+now()+' — 5% complete. Read mandatory objective. Fresh public acquisition started; no mathematical approval or helper execution is part of this scope assignment. Prior sealed work remains unchanged.\n')
raw,url,status,headers=get('https://zenodo.org/api/records/23444606');(S/'record.json').write_bytes(raw);record=json.loads(raw)
assert record['id']==23444606 and record['metadata']['version']==q['version'] and record['metadata']['publication_date']==q['publication_date']
expected={x['filename']:(x.get('expected_bytes',x.get('filesize')),x.get('expected_md5',x.get('checksum')),x.get('sha256')) for x in q['sources']+q['supporting_files']}
assert {f['key'] for f in record['files']}==set(expected)
files=[]
for f in record['files']:
 name=f['key'];assert Path(name).name==name
 b,u,st,hh=get(f['links']['self']);n,md,sh=expected[name]
 assert st==200 and len(b)==f['size']==n and hashlib.md5(b).hexdigest()==f['checksum'].split(':')[-1]==md
 if sh:assert sha(b)==sh
 (S/name).write_bytes(b);files.append({'name':name,'url':f['links']['self'],'resolved_url':u,'bytes':len(b),'md5':hashlib.md5(b).hexdigest(),'zenodo_checksum':f['checksum'],'sha256':sha(b),'retrieved_utc':now(),'integrity':'PASS'})
archive=S/'initial-omnific-models-source-and-verification.zip';dest=S/'published-source/initial-omnific-models-source-and-verification';dest.mkdir(parents=True,exist_ok=True)
members=[];readers=[];nested=[];seen=set()
with zipfile.ZipFile(archive) as z:
 for i in z.infolist():
  pp=PurePosixPath(i.filename);assert not pp.is_absolute() and '..' not in pp.parts and '\\' not in i.filename and i.filename not in seen;seen.add(i.filename)
  mode=i.external_attr>>16;typ=stat.S_IFMT(mode);assert typ in (0,stat.S_IFREG,stat.S_IFDIR)
  if i.is_dir():(dest/i.filename).mkdir(parents=True,exist_ok=True);continue
  b=z.read(i);assert len(b)==i.file_size
  out=dest/i.filename;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
  row={'archive':archive.name,'member':i.filename,'bytes':len(b),'sha256':sha(b),'crc32':f'{i.CRC:08x}','mode':oct(mode),'hidden':any(x.startswith('.') for x in pp.parts),'path':str(out)};members.append(row)
  if i.filename.lower().endswith('.pdf'):readers.append(row)
  if i.filename.lower().endswith(('.zip','.tar','.tar.gz','.tgz','.tar.xz','.gz','.7z')):nested.append(row)
receipt={'record_id':'23444606','record_url':'https://zenodo.org/api/records/23444606','record_sha256':sha(raw),'retrieved_utc':now(),'complete':True,'queue_matched':True,'files':files,'archive_regular_member_count':len(members),'embedded_reader_pdfs':readers,'nested_archives':nested}
save(S/'receipt.json',receipt);save(S/'extraction-integrity.json',{'created_utc':now(),'safe_paths':True,'regular_types_only':True,'crc_verified_by_zipfile':True,'hidden_members':[x for x in members if x['hidden']],'members':members,'readers':readers,'nested_archives':nested})
with (R/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now()+' — 20% complete. Fresh metadata and both public assets match frozen queue sizes/MD5 and known main PDF SHA. Archive paths, types, CRCs/modes/hidden members inventoried and safely extracted; reader/nested coverage inventoried. Sources ready for independent reviewers; source bodies remain unchanged.\n')
print(json.dumps({'files':files,'member_count':len(members),'readers':readers,'nested':nested},indent=2))
