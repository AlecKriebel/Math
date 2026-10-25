from pathlib import Path,PurePosixPath
import json,hashlib,urllib.request,datetime,concurrent.futures,zipfile,stat,zlib,subprocess
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'sources';OUT=ROOT/'reviews/scope'
q=json.loads((OUT/'queue_identity.json').read_text()); record=json.loads((SRC/'record.json').read_text())
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(b):return hashlib.sha256(b).hexdigest()
def get(f):
 url=f['links']['self']; resp=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Research-source-verification/1.0'}),timeout=90);b=resp.read()
 if len(b)!=f['size'] or 'md5:'+hashlib.md5(b).hexdigest()!=f['checksum']:raise ValueError('asset mismatch')
 target=SRC/f['key'];target.write_bytes(b)
 bound=next(x for x in q['sources']+q['supporting_files'] if x['filename']==f['key'])
 if bound.get('expected_bytes',bound.get('filesize'))!=len(b):raise ValueError('queue size')
 if bound.get('expected_md5',bound.get('checksum'))!=hashlib.md5(b).hexdigest():raise ValueError('queue MD5')
 if bound.get('sha256',h(b))!=h(b):raise ValueError('queue SHA')
 return {'name':f['key'],'url':url,'resolved_url':resp.geturl(),'bytes':len(b),'md5':hashlib.md5(b).hexdigest(),'zenodo_checksum':f['checksum'],'sha256':h(b),'retrieved_utc':now(),'integrity':'PASS'}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: files=list(pool.map(get,record['files']))
members=[];readers=[];nested=[]
for f in files:
 if not f['name'].endswith('.zip'):continue
 zpath=SRC/f['name']; target=SRC/'published-source'/zpath.stem
 with zipfile.ZipFile(zpath) as z:
  seen=set()
  for zi in z.infolist():
   p=PurePosixPath(zi.filename);mode=zi.external_attr>>16
   if p.is_absolute() or '..' in p.parts or '\\' in zi.filename or zi.filename in seen:raise ValueError('unsafe/duplicate path')
   seen.add(zi.filename)
   if stat.S_IFMT(mode) not in [0,stat.S_IFREG,stat.S_IFDIR]:raise ValueError('unsupported archive member')
   dst=target/Path(*p.parts)
   if zi.is_dir():dst.mkdir(parents=True,exist_ok=True);continue
   b=z.read(zi)
   if len(b)!=zi.file_size or zlib.crc32(b)&0xffffffff!=zi.CRC:raise ValueError('CRC/size')
   dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
   if mode & 0o777:dst.chmod(mode&0o777)
   item={'archive':zpath.name,'member':zi.filename,'bytes':len(b),'sha256':h(b),'crc32':f'{zi.CRC:08x}','mode':oct(mode),'path':str(dst)}
   members.append(item)
   if dst.suffix.lower()=='.pdf':readers.append(item)
   if dst.name.lower().endswith(('.zip','.tar','.tar.gz','.tgz','.7z')):nested.append(item)
receipt={'record_id':'23393596','record_url':'https://zenodo.org/api/records/23393596','record_sha256':h((SRC/'record.json').read_bytes()),'retrieved_utc':now(),'complete':True,'queue_matched':True,'files':files,'archive_regular_member_count':len(members),'embedded_reader_pdfs':readers,'nested_archives':nested}
(SRC/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
(SRC/'extraction-integrity.json').write_text(json.dumps({'verified_utc':now(),'all_paths_types_and_crc_checked':True,'archive_modes_preserved':True,'members':members,'reader_pdfs':readers,'nested_archives':nested},indent=2)+'\n')
pdf=SRC/'deep-derived-pure-braids-v1.0.pdf'
subprocess.run(['pdftotext','-layout',str(pdf),str(OUT/'cache/paper.txt')],check=True)
print(json.dumps({'files':files,'regular_members':len(members),'readers':readers,'nested':nested},indent=2))
