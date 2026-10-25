"""Fresh public acquisition and safe byte inventory; execute no submitted helpers."""
from pathlib import Path, PurePosixPath
import datetime,hashlib,io,json,os,stat,subprocess,urllib.request,zipfile
O=Path(__file__).resolve().parent;P=O.parents[1];R=P.parents[1];S=P/'sources'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'ResearchScope/1.0 public scholarly archive verification'})
 with urllib.request.urlopen(req,timeout=60) as r:return r.read(),r.geturl()
queue=json.loads((R/'reconciliation/queue.json').read_text())
def walk(x):
 if isinstance(x,dict):
  if str(x.get('record_id'))=='23356964' and 'sources' in x:yield x
  for y in x.values():yield from walk(y)
 elif isinstance(x,list):
  for y in x:yield from walk(y)
q=list(walk(queue));assert len(q)==1;q=q[0]
save(O/'queue_identity.json',{'queue_sha256':sha((R/'reconciliation/queue.json').read_bytes()),'record':q,'verified_utc':utc()})
(O/'.gitignore').write_text('cache/\n__pycache__/\n')
(O/'RESEARCH_LOG.md').write_text('# Intake and scope log\n\n'+utc()+' — 5%: saved objective read, eligible row72/frozen queue matched. Row71 exclusion left untouched. Fresh public acquisition started; no mathematical approval or helper execution.\n')
raw,resolved=get('https://zenodo.org/api/records/23356964');(S/'record.json').write_bytes(raw);rec=json.loads(raw)
for key in ['title','publication_date','version','doi']:assert rec['metadata'][key]==q[key],(key,rec['metadata'][key],q[key])
expected={x['filename']:(x['expected_bytes'],x['expected_md5']) for x in q['sources']}
expected.update({x['filename']:(x['filesize'],x['checksum']) for x in q['supporting_files']})
assert set(expected)=={x['key'] for x in rec['files']}
assets=[]
for x in rec['files']:
 name=x['key'];assert PurePosixPath(name).name==name
 data,url=get(f'https://zenodo.org/api/records/23356964/files/{name}/content')
 md5=hashlib.md5(data).hexdigest();size,emd5=expected[name]
 assert len(data)==size==x['size'] and md5==emd5==x['checksum'].removeprefix('md5:')
 (S/name).write_bytes(data)
 assets.append({'name':name,'url':f'https://zenodo.org/api/records/23356964/files/{name}/content','resolved_url':url,'bytes':len(data),'md5':md5,'zenodo_checksum':x['checksum'],'sha256':sha(data),'retrieved_utc':utc(),'integrity':'PASS'})
members=[];readers=[];nested=[];seen=set()
def scan_zip(blob,label,extract=None,depth=0):
 assert depth<=5
 with zipfile.ZipFile(io.BytesIO(blob)) as z:
  assert z.testzip() is None
  for info in z.infolist():
   path=PurePosixPath(info.filename);mode=(info.external_attr>>16)&0xffff
   assert not path.is_absolute() and '..' not in path.parts and '\\' not in info.filename
   assert not stat.S_ISLNK(mode)
   if info.is_dir():continue
   assert not stat.S_IFMT(mode) or stat.S_ISREG(mode)
   full=label+'!/'+info.filename;assert full not in seen;seen.add(full)
   data=z.read(info)
   entry={'archive':label,'member':info.filename,'logical_path':full,'bytes':len(data),'sha256':sha(data),'crc32':f'{info.CRC:08x}','original_mode':oct(mode),'hidden':any(t.startswith('.') for t in path.parts),'depth':depth}
   if extract is not None:
    target=extract/str(path);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    if mode&0o777:target.chmod(mode&0o777)
    entry['extracted_path']=str(target.relative_to(P))
   members.append(entry)
   if data.lstrip()[:5]==b'%PDF-':
    target=O/'cache'/('reader-'+sha(data)+'.pdf');target.write_bytes(data)
    readers.append({'logical_path':full,'sha256':sha(data),'bytes':len(data),'cache_path':str(target.relative_to(P))})
   if zipfile.is_zipfile(io.BytesIO(data)):
    nested.append({'logical_path':full,'sha256':sha(data),'bytes':len(data),'type':'zip'})
    scan_zip(data,full,None,depth+1)
archive=S/'generic-wreath-hyperfiniteness-verification.zip'
scan_zip(archive.read_bytes(),archive.name,S/'published-source'/archive.stem)
save(S/'extraction-integrity.json',{'verified_utc':utc(),'archive_sha256':sha(archive.read_bytes()),'crc_pass':True,'regular_members':members,'nested_archives':nested,'reader_pdfs':readers,'safe_paths_and_regular_modes':True})
pdf=S/'generic-wreath-hyperfiniteness-note.pdf'
info=subprocess.run(['pdfinfo',str(pdf)],check=True,text=True,capture_output=True).stdout
subprocess.run(['pdftotext','-layout',str(pdf),str(O/'cache/paper.txt')],check=True)
save(O/'reader_document_map.json',{'published_pdf':{'path':str(pdf.relative_to(P)),'sha256':sha(pdf.read_bytes()),'pdfinfo':info},'embedded_readers':readers,'nested_archives':nested,'distinct_pdf_sha256':sorted({sha(pdf.read_bytes())}|{x['sha256'] for x in readers}),'all_archive_regular_members_scanned_by_magic':True})
save(S/'receipt.json',{'record_id':'23356964','metadata_url':'https://zenodo.org/api/records/23356964','metadata_resolved_url':resolved,'record_sha256':sha(raw),'retrieved_utc':utc(),'complete':True,'files':assets,'archives':{'regular_members':len(members),'outer_regular_members':sum(x['depth']==0 for x in members),'nested_archives':len(nested),'embedded_readers':len(readers)},'queue_match':True,'helper_execution':False})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(utc()+f' — 25%: all {len(assets)} fresh public assets match queue/API MD5 and size; SHA256 bound. {len(members)} safe regular members hashed/CRC checked with original modes retained; {len(nested)} nested archives and {len(readers)} embedded PDFs scanned. No helper or historical opinion body read.\n')
print(json.dumps({'assets':assets,'members':len(members),'nested':nested,'readers':readers,'pdfinfo':info},ensure_ascii=False,indent=2))
