"""Authenticate originals and safe recursive source custody; no supplied code runs."""
from pathlib import Path,PurePosixPath
from io import BytesIO
import json,hashlib,zipfile,tarfile,stat,datetime,subprocess
E=Path(__file__).resolve().parent;P=E.parents[1];S=P/'sources'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,x):(S/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def safe(n):
 q=PurePosixPath(n)
 if not n or '\\' in n or q.is_absolute() or any(x in ['.','..',''] for x in q.parts) or str(q)!=n.rstrip('/'):raise ValueError('unsafe_member_name:'+n)
 return q
members=[];containers=[]
def write_new(path,data):
 if path.exists():
  if path.read_bytes()!=data:raise RuntimeError('existing_extraction_identity_conflict:'+str(path))
 else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
def visit(data,label,base,depth):
 if depth>3:raise ValueError('archive_depth')
 iszip=zipfile.is_zipfile(BytesIO(data));kind='zip' if iszip else 'tar'
 if iszip:
  z=zipfile.ZipFile(BytesIO(data));entries=[]
  for i in z.infolist():
   safe(i.filename);mode=i.external_attr>>16
   if i.is_dir():continue
   if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in [0,stat.S_IFREG]) or i.flag_bits&1:raise ValueError('nonregular_or_encrypted_zip')
   entries.append((i.filename,z.read(i),{'CRC32':f'{i.CRC:08x}','compressed_bytes':i.compress_size,'archive_mode':mode,'ZIP_CRC_read':True}))
 else:
  z=tarfile.open(fileobj=BytesIO(data),mode='r:*');entries=[]
  for i in z:
   safe(i.name)
   if i.isdir():continue
   if not i.isfile():raise ValueError('nonregular_tar')
   entries.append((i.name,z.extractfile(i).read(),{'tar_header_checksum':i.chksum,'archive_mode':i.mode,'tar_header_parsed':True,'CRC32':None}))
 containers.append({'container':label,'kind':kind,'depth':depth,'bytes':len(data),'sha256':sha(data),'extraction_root':str(base),'regular_members':len(entries)})
 seen=set()
 for name,payload,details in entries:
  if name in seen or len(payload)>10000000:raise ValueError('duplicate_or_large_member')
  seen.add(name);dest=base/name
  if not dest.resolve().is_relative_to(S.resolve()):raise ValueError('escape_extraction')
  write_new(dest,payload);nested=zipfile.is_zipfile(BytesIO(payload)) or name.lower().endswith(('.tar','.tar.gz','.tgz','.tar.bz2','.tar.xz'))
  members.append({'container':label,'member':name,'bytes':len(payload),'sha256':sha(payload),'extracted_path':str(dest),'nested_archive':nested,**details})
  if nested:visit(payload,label+'::'+name,S/'nested-source'/(label.replace('::','__')+'__'+name+'.contents'),depth+1)
 z.close()
a=json.loads((S/'record.raw.json').read_text());latest=json.loads((S/'latest.raw.json').read_text());versions=json.loads((S/'versions.raw.json').read_text());assets=json.loads((S/'assets-acquired.json').read_text())['all_assets']
if str(a['id'])!='23146753' or str(latest['id'])!='23146753' or a['status']!='published' or a['metadata']['version']!='1.0' or a['metadata']['publication_date']!='2026-10-04':raise RuntimeError('record_version_identity')
if versions['hits']['total']!=1 or [str(x['id']) for x in versions['hits']['hits']]!=['23146753']:raise RuntimeError('actual_versions_interface')
for x,obj in zip(assets,a['files']):
 data=Path(x['path']).read_bytes()
 if x['original_api_file_object']!=obj or len(data)!=obj['size'] or sha(data)!=x['sha256'] or obj['checksum']!='md5:'+hashlib.md5(data).hexdigest():raise RuntimeError('asset_identity')
 if obj['key'].endswith('.zip'):visit(data,obj['key'],S/'published-source',0)
tex=[{'path':x['extracted_path'],'bytes':x['bytes'],'sha256':x['sha256']} for x in members if x['member'].endswith('.tex')]
pdf=next(Path(x['path']) for x in assets if x['original_api_file_object']['key'].endswith('.pdf'));info=subprocess.check_output(['/opt/homebrew/bin/pdfinfo',str(pdf)],text=True);pages=int(next(x.split(':')[1] for x in info.splitlines() if x.startswith('Pages:')))
if pages!=5 or not pdf.read_bytes().startswith(b'%PDF-'):raise RuntimeError('actual_reader')
save('archive-members.json',{'utc':utc(),'archive_containers':containers,'members':members,'regular_member_occurrences':len(members),'expanded_bytes':sum(x['bytes'] for x in members),'nested_archive_count':len(containers)-1,'embedded_PDFs':[x['container']+'::'+x['member'] for x in members if x['member'].lower().endswith('.pdf')],'all_ZIP_members_CRC_read':all(x.get('ZIP_CRC_read') for x in members if x['CRC32'] is not None),'no_code_execution':True})
save('normalized-metadata.json',{'utc':utc(),'derivative_not_raw_API':True,'metadata':a['metadata'],'record_id':str(a['id']),'conceptrecid':str(a['conceptrecid']),'created':a['created'],'updated':a['updated'],'all_original_API_file_objects':a['files'],'all_assets':assets,'all_TeX_candidates':tex})
save('SOURCE_READY.json',{'utc':utc(),'derived_from_raw':'record.raw.json/latest.raw.json/versions.raw.json; original objects unmodified','record_id':23146753,'title':a['metadata']['title'],'version':a['metadata']['version'],'publication_date':a['metadata']['publication_date'],'created':a['created'],'updated':a['updated'],'doi':a['metadata']['doi'],'conceptrecid':str(a['conceptrecid']),'latest_record_id':latest['id'],'versions_total':versions['hits']['total'],'all_assets':assets,'all_TeX_candidates':tex,'status':'SOURCE_READY_FRESH_PUBLIC_ORIGINALS_COMPLETE_RECURSIVE_CUSTODY','sheet_row':105,'PDF_pages':pages,'safe_regular_member_occurrences':len(members),'expanded_bytes':sum(x['bytes'] for x in members),'nested_archives':len(containers)-1,'source_evaluation':'Original source custody only; no mathematical verdict or inherited review approval.'})
files=[{'path':str(p.relative_to(S)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(S.rglob('*')) if p.is_file() and p.name not in ['SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json']]
save('SOURCE_READY_MANIFEST.json',{'utc':utc(),'files':files,'scope':'All actual raw API/transport/assets and original safely extracted source identities before scientific review'})
save('SOURCE_READY_SEAL.json',{'utc':utc(),'status':'SOURCE_READY','manifest':'SOURCE_READY_MANIFEST.json','manifest_sha256':sha((S/'SOURCE_READY_MANIFEST.json').read_bytes()),'SOURCE_READY_sha256':sha((S/'SOURCE_READY.json').read_bytes()),'bindings':len(files),'mathematical_or_priority_approval':False,'preserve_immutable':True})
print(json.dumps({'ready':True,'PDF_pages':pages,'assets':assets,'TeX_candidates':tex,'member_occurrences':len(members),'containers':len(containers),'seal_sha256':sha((S/'SOURCE_READY_SEAL.json').read_bytes()),'source_bindings':len(files)},ensure_ascii=False,indent=2))
