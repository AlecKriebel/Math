"""Fresh original public objects and complete safe recursive archive custody.
No author code, archived audits, foreign primary text, Git mutation or installers.
"""
from pathlib import Path,PurePosixPath
from io import BytesIO
from datetime import datetime,timezone
import hashlib,json,stat,tarfile,zipfile,urllib.request,gzip,bz2,lzma,os,subprocess
from pypdf import PdfReader
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');R=P/'papers/23333046';S=R/'sources';E=R/'reviews/scope'
S.mkdir(parents=True,exist_ok=True)
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(root,name,x):(root/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def binding(p):b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
assert not (S/'SOURCE_READY.json').exists()
# Fresh lean preservation; no stale current-ref assumptions.
protected=set()
for root in [P/'redirects/banach-rigidity-preflight-sol-20261025',P/'papers/23217863/reviews/editorial',P/'papers/23217863/sources']:
 protected.update(p for p in root.rglob('*') if p.is_file())
for n in ['publication.json','promotion.json']:protected.add(P/'papers/23217863'/n)
gitroot=P.parent
for n in ['.git/HEAD','.git/index','.git/refs/heads/main']:
 p=gitroot/n
 if p.is_file():protected.add(p)
env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}
gitrefs={ref:subprocess.run(['git','rev-parse',ref],cwd=gitroot,env=env,check=True,capture_output=True).stdout.decode().strip() for ref in ['HEAD','refs/heads/main']}
save(E,'PRESERVATION_BEFORE.json',{'utc':now(),'files':[binding(p) for p in sorted(protected)],'resolved_Git_refs':gitrefs,'scope':'Prior103 editorial/source/configs, complete preceding legacy preflight, and local main/HEAD/index; concurrent root remote-tracking checkpoints are not prohibited.'})
receipts=[]
def fetch(url,name):
 target=S/name
 if target.exists():raise RuntimeError('refuse original overwrite:'+name)
 start=now();req=urllib.request.Request(url,headers={'User-Agent':'IndependentResearchSourceCustody/1.0','Accept':'application/json' if name.endswith('.json') else '*/*'})
 with urllib.request.urlopen(req,timeout=40) as res:
  b=res.read(48*1024*1024+1);headers=list(res.headers.items());status=res.status;final=res.url
 assert len(b)<=48*1024*1024
 target.write_bytes(b);rec={'requested_url':url,'started_utc':start,'completed_utc':now(),'HTTP_status':status,'final_url':final,'response_headers_in_received_order':headers,'body':binding(target),'fresh_ordinary_HTTPS':True,'not_reused_cache':True};receipts.append(rec);save(S,'api-receipts.json',receipts)
 assert status==200
 return b
api=json.loads(fetch('https://zenodo.org/api/records/23333046','record.raw.json'))
assert api['id']==23333046
latest=json.loads(fetch('https://zenodo.org/api/records/23333046/versions/latest','latest.raw.json'))
versions=json.loads(fetch('https://zenodo.org/api/records/23333046/versions','versions.raw.json'))
assert latest['id']==api['id'] and latest['metadata']==api['metadata'] and latest['files']==api['files']
assets=[]
for obj in api['files']:
 name=obj['key'];assert isinstance(name,str) and name==PurePosixPath(name).name and name not in ['', '.', '..'] and '\\' not in name and '\0' not in name
 assert not any(a['original_api_file_object']['key']==name for a in assets)
 url=obj['links']['self'];assert url.startswith('https://zenodo.org/api/records/23333046/files/')
 b=fetch(url,name);md5=hashlib.md5(b).hexdigest();assert len(b)==obj['size'] and obj['checksum']=='md5:'+md5
 assets.append({'original_api_file_object':obj,**binding(S/name),'md5':md5})
containers=[];members=[];expanded=0;limit=64*1024*1024
def canonical(name):
 assert isinstance(name,str) and not any(x in name for x in ['\\','\0',':']) and not name.startswith('/'),repr(name)
 name=name.rstrip('/')
 while name.startswith('./'):name=name[2:]
 assert name and all(x not in ['', '.', '..'] for x in name.split('/')),repr(name)
 return name
def kind(b,name):
 if zipfile.is_zipfile(BytesIO(b)):return 'zip'
 if b.startswith((b'\x1f\x8b',b'BZh',b'\xfd7zXZ\x00')) or b[257:262]==b'ustar' or name.lower().endswith(('.tar','.tgz','.tar.gz','.tar.xz','.tar.bz2')):
  try:
   with tarfile.open(fileobj=BytesIO(b),mode='r:*'):pass
   return 'tar-compressed-or-plain'
  except tarfile.ReadError:
   if b.startswith(b'\x1f\x8b'):return 'gzip'
   if b.startswith(b'BZh'):return 'bzip2'
   if b.startswith(b'\xfd7zXZ\x00'):return 'xz'
 return None
def inspect(b,ident,root,depth,k):
 global expanded
 assert depth<=8 and len(containers)<32
 containers.append({'container':ident,'kind':k,'depth':depth,'bytes':len(b),'sha256':sha(b),'extraction_root':str(root)})
 root.mkdir(parents=True,exist_ok=True);regular=[];seen=set()
 if k=='zip':
  with zipfile.ZipFile(BytesIO(b)) as z:
   for i in z.infolist():
    mode=i.external_attr>>16;assert not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in [0,stat.S_IFREG,stat.S_IFDIR]
    rel=canonical(i.filename);assert rel not in seen;seen.add(rel)
    if i.is_dir():continue
    assert not i.flag_bits&1;expanded+=i.file_size;assert expanded<=limit
    q=z.read(i);assert len(q)==i.file_size
    regular.append((i.filename,rel,q,{'CRC32':format(i.CRC,'08x'),'compressed_bytes':i.compress_size,'zip_flags':i.flag_bits}))
 elif k.startswith('tar'):
  with tarfile.open(fileobj=BytesIO(b),mode='r:*') as z:
   for i in z:
    if i.isdir() and i.name in ['.','./']:continue
    rel=canonical(i.name);assert rel not in seen;seen.add(rel)
    if i.isdir():continue
    assert i.isfile(),'tar links/special objects forbidden';expanded+=i.size;assert expanded<=limit
    q=z.extractfile(i).read();assert len(q)==i.size;regular.append((i.name,rel,q,{'tar_size':i.size}))
 else:
  # Standalone compression is inventoried even if not a tar. This derived
  # extraction name is explicitly synthetic, never an original API alias.
  if k=='gzip':q=gzip.GzipFile(fileobj=BytesIO(b)).read(limit+1)
  elif k=='bzip2':q=bz2.BZ2Decompressor().decompress(b,max_length=limit+1)
  else:q=lzma.LZMADecompressor().decompress(b,max_length=limit+1)
  expanded+=len(q);assert expanded<=limit;regular.append((None,'DECOMPRESSED_PAYLOAD',q,{'synthetic_extraction_name':True}))
 assert len(members)+len(regular)<=10000
 for original,rel,q,extra in regular:
  p=root/rel;assert not p.exists() and p.resolve().is_relative_to(root.resolve());p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(q)
  nested=kind(q,original or 'payload');members.append({'container':ident,'original_member_name':original,'canonical_extraction_relative_path':rel,'extracted_path':str(p),'bytes':len(q),'sha256':sha(q),'nested_archive_kind':nested,'safe_regular_body':True,**extra})
  if nested:inspect(q,ident+'::'+(original or 'DECOMPRESSED_PAYLOAD'),S/'nested-source'/str(len(containers))/(rel+'.contents'),depth+1,nested)
for a in assets:
 p=Path(a['path']);k=kind(p.read_bytes(),p.name)
 if k:inspect(p.read_bytes(),p.name,S/'published-source',0,k)
pdf=[]
for a in assets:
 p=Path(a['path'])
 if p.suffix.lower()=='.pdf':
  assert p.read_bytes().startswith(b'%PDF-');pdf.append({**binding(p),'pages':len(PdfReader(p).pages),'actual_standalone_API_asset':True})
assert len(pdf)==1 and pdf[0]['bytes']==72991 and pdf[0]['sha256']=='206114a917235504567f9f8487023c284aebacef00440e3c5bebfed98639d8cb'
tex=[m for m in members if (m['original_member_name'] or '').lower().endswith('.tex')]
save(S,'archive-members.json',{'utc':now(),'archive_containers':containers,'members':members,'safe_regular_occurrences':len(members),'container_count':len(containers),'nested_containers':sum(c['depth']>0 for c in containers),'expanded_bytes_all_depths':expanded,'all_format_magic_detection':'ZIP, tar (plain/gzip/bzip2/xz), standalone gzip/bzip2/xz; no embedded code execution','all_safe_bodies_read_and_hashed':True})
save(S,'normalized-metadata.json',{'utc':now(),'derivative_not_raw_API':True,'record_id':api['id'],'metadata':api['metadata'],'version_field_present':'version' in api['metadata'],'version':api['metadata'].get('version'),'created':api['created'],'updated':api['updated'],'all_original_API_file_objects_in_original_order':api['files'],'all_assets':assets,'all_TeX_candidates':tex})
ready={'utc':now(),'status':'SOURCE_READY_FRESH_COMPLETE_PUBLIC_OBJECTS_RECURSIVE_CUSTODY','record_id':23333046,'sheet_row':107,'title':api['metadata']['title'],'version_field_present':'version' in api['metadata'],'version':api['metadata'].get('version'),'publication_date':api['metadata']['publication_date'],'created':api['created'],'updated':api['updated'],'doi':api['metadata'].get('doi',api.get('doi')),'conceptrecid':api.get('conceptrecid'),'latest_record_id':latest['id'],'versions_total_original':versions.get('hits',{}).get('total'),'all_assets_in_original_order':assets,'actual_standalone_readers':pdf,'selected_actual_PDF':pdf[0],'safe_regular_occurrences':len(members),'archive_containers':len(containers),'nested_archives':sum(c['depth']>0 for c in containers),'expanded_bytes_all_depths':expanded,'all_TeX_candidates':tex,'foreign_primary_bodies_historical_current_scientific_opinions_or_archived_audits_read':False,'target_mathematics_not_yet_read':True,'originals_now_immutable':True}
save(S,'SOURCE_READY.json',ready)
files=[{'path':str(p.relative_to(S)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(S.rglob('*')) if p.is_file()]
save(S,'SOURCE_READY_MANIFEST.json',{'utc':now(),'status':'IMMUTABLE_SOURCE_READY','files':files,'file_count':len(files)})
save(S,'SOURCE_READY_SEAL.json',{'utc':now(),'manifest_sha256':sha((S/'SOURCE_READY_MANIFEST.json').read_bytes()),'SOURCE_READY_sha256':sha((S/'SOURCE_READY.json').read_bytes()),'original_bindings':len(files),'immutable':True})
with (E/'RESEARCH_LOG.md').open('a') as f:f.write(f'* {now()} — All fresh original API assets/checksums/transport facts and recursive archive bodies authenticated; SOURCE_READY sealed before mathematical reading/opinions/primaries. Source acquisition100%; scientific review0%; all203 ongoing.\n')
print(json.dumps({'ready':binding(S/'SOURCE_READY.json'),'manifest':binding(S/'SOURCE_READY_MANIFEST.json'),'seal':binding(S/'SOURCE_READY_SEAL.json'),'PDF':pdf,'TeX_candidates':tex,'members':len(members),'containers':len(containers),'expanded_bytes':expanded},indent=2,ensure_ascii=False))
