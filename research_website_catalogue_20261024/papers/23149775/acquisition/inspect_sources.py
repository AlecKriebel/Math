#!/usr/bin/env python3
"""Safe complete archive custody and reader/TeX identification only.
No scientific manuscript/TeX text is semantically read and no deposited code runs.
"""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import json,hashlib,zipfile,tarfile,gzip,bz2,lzma,stat,unicodedata,sys,subprocess,re,io
RID=sys.argv[1];ROOT=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');P=ROOT/'papers'/RID;S=P/'sources';A=P/'acquisition';C=S/'cache';now=lambda:datetime.now(timezone.utc).isoformat();sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
intake=json.loads((A/'NATIVE_INTAKE.json').read_text());members=[];containers=[];dirs=[];container_index=0;total=0;pdfs=[];tex=[];unsupported=[]
def safe(name):
 if not name or name.startswith('/') or '\\' in name or '\x00' in name or re.match(r'^[A-Za-z]:',name):raise ValueError('unsafe name '+repr(name))
 parts=PurePosixPath(name).parts
 if '..' in parts or '.' in parts or not parts:raise ValueError('unsafe relative name '+repr(name))
 return PurePosixPath(name)
def classify(path):
 with path.open('rb') as f:head=f.read(1024)
 if zipfile.is_zipfile(path):return 'zip'
 for magic,label in [(b'7z\xbc\xaf\x27\x1c','7z'),(b'Rar!\x1a\x07','rar'),(b'\x28\xb5\x2f\xfd','zstd'),(b'\x04\x22\x4d\x18','lz4'),(b'MSCF','cab'),(b'!<arch>\n','ar')]:
  if head.startswith(magic):return 'unsupported:'+label
 try:
  if tarfile.is_tarfile(path):return 'tar'
 except (OSError,tarfile.TarError):pass
 if head.startswith(b'\x1f\x8b'):return 'gzip'
 if head.startswith(b'BZh'):return 'bzip2'
 if head.startswith(b'\xfd7zXZ\x00'):return 'xz'
 if head.startswith(b'PK\x03\x04') or head.startswith(b'PK\x05\x06'):return 'invalid_zip_magic'
 return None
def pdfinfo(path):
 run=subprocess.run(['pdfinfo',str(path)],text=True,capture_output=True,check=True);lines=run.stdout.splitlines();meta={}
 for line in lines:
  if ':' in line:
   key,value=line.split(':',1);meta[key.strip()]=value.strip()
 return {'pages':int(meta['Pages']),'PDF_metadata_title':meta.get('Title'),'PDF_metadata_author':meta.get('Author'),'pdfinfo_raw':run.stdout}
def identify(path,item,origin):
 with path.open('rb') as f:head=f.read(1024)
 if b'%PDF-' in head:
  info=pdfinfo(path);pdfs.append({**item,'origin':origin,**info})
 if path.suffix.lower()=='.tex':tex.append({**item,'origin':origin})
def emit_body(stream,path):
 global total
 if path.exists():raise RuntimeError('refusing overwrite extracted body '+str(path))
 path.parent.mkdir(parents=True,exist_ok=True)
 digest=hashlib.sha256();size=0
 with path.open('xb') as out:
  while True:
   block=stream.read(1024*1024)
   if not block:break
   out.write(block);digest.update(block);size+=len(block)
   if size>1024**3 or total+size>2*1024**3:raise RuntimeError('bounded acquisition expanded-byte safety ceiling exceeded')
 total+=size
 return size,digest.hexdigest()
def visit(path,label,depth):
 global container_index
 kind=classify(path)
 if kind is None:return
 if kind.startswith('unsupported:') or kind=='invalid_zip_magic':
  unsupported.append({'path':str(path),'container':label,'detected_kind':kind});raise RuntimeError('unaccounted nested archive '+kind)
 container_index+=1;number=container_index
 outroot=C/'extracted'/('container-'+str(number).zfill(3))
 if outroot.exists():raise RuntimeError('refusing existing extraction root '+str(outroot))
 outroot.mkdir(parents=True)
 rec={'container':label,'kind':kind,'depth':depth,'source_path':str(path),'bytes':path.stat().st_size,'SHA256':sha(path),'extraction_root':str(outroot)};containers.append(rec)
 if kind=='zip':
  with zipfile.ZipFile(path) as z:
   entries=z.infolist();seen=set();folded=set()
   # Validate every central directory name/type before extracting any member.
   for entry in entries:
    rel=safe(entry.filename);canonical=str(rel);fold=unicodedata.normalize('NFC',canonical).casefold()
    if canonical in seen or fold in folded:raise RuntimeError('duplicate/case-normalized extraction collision '+canonical)
    seen.add(canonical);folded.add(fold)
    mode=(entry.external_attr>>16)&0xffff;filetype=stat.S_IFMT(mode)
    if entry.flag_bits&1:raise RuntimeError('encrypted archive member')
    if entry.is_dir():
     if filetype not in (0,stat.S_IFDIR):raise RuntimeError('invalid directory mode')
    elif filetype not in (0,stat.S_IFREG):raise RuntimeError('nonregular/symlink archive member')
   for ordinal,entry in enumerate(entries,1):
    rel=safe(entry.filename);out=outroot.joinpath(*rel.parts)
    central={'container':label,'archive_kind':kind,'depth':depth,'entry_ordinal':ordinal,'original_member_name':entry.filename,'CRC32':f'{entry.CRC:08x}','declared_uncompressed_bytes':entry.file_size,'compressed_bytes':entry.compress_size,'flag_bits':entry.flag_bits,'compression_method':entry.compress_type,'date_time':list(entry.date_time),'external_attr':entry.external_attr,'create_system':entry.create_system,'comment_hex':entry.comment.hex(),'extra_hex':entry.extra.hex()}
    if entry.is_dir():out.mkdir(parents=True,exist_ok=True);dirs.append(central);continue
    with z.open(entry) as stream:size,digest=emit_body(stream,out)
    if size!=entry.file_size:raise RuntimeError('uncompressed size mismatch')
    item={**central,'extracted_path':str(out),'bytes':size,'SHA256':digest,'safe_regular_body':True,'nested_archive_kind':classify(out)};members.append(item);identify(out,item,'archive-member')
    if item['nested_archive_kind']:visit(out,label+'::'+entry.filename,depth+1)
 elif kind=='tar':
  with tarfile.open(path,'r:*') as tar:
   entries=tar.getmembers();seen=set();folded=set()
   for entry in entries:
    rel=safe(entry.name);canonical=str(rel);fold=unicodedata.normalize('NFC',canonical).casefold()
    if canonical in seen or fold in folded:raise RuntimeError('duplicate TAR name')
    seen.add(canonical);folded.add(fold)
    if not(entry.isfile() or entry.isdir()):raise RuntimeError('nonregular/symlink TAR member')
   for ordinal,entry in enumerate(entries,1):
    rel=safe(entry.name);out=outroot.joinpath(*rel.parts);central={'container':label,'archive_kind':kind,'depth':depth,'entry_ordinal':ordinal,'original_member_name':entry.name,'declared_uncompressed_bytes':entry.size,'mode':entry.mode,'mtime':entry.mtime,'uid':entry.uid,'gid':entry.gid,'pax_headers':entry.pax_headers}
    if entry.isdir():out.mkdir(parents=True,exist_ok=True);dirs.append(central);continue
    with tar.extractfile(entry) as stream:size,digest=emit_body(stream,out)
    if size!=entry.size:raise RuntimeError('TAR size mismatch')
    item={**central,'extracted_path':str(out),'bytes':size,'SHA256':digest,'safe_regular_body':True,'nested_archive_kind':classify(out)};members.append(item);identify(out,item,'archive-member')
    if item['nested_archive_kind']:visit(out,label+'::'+entry.name,depth+1)
 else:
  opener={'gzip':gzip.open,'bzip2':bz2.open,'xz':lzma.open}[kind];out=outroot/'decompressed-payload'
  with opener(path,'rb') as stream:size,digest=emit_body(stream,out)
  item={'container':label,'archive_kind':kind,'depth':depth,'entry_ordinal':1,'original_member_name':'decompressed-payload','extracted_path':str(out),'bytes':size,'SHA256':digest,'safe_regular_body':True,'nested_archive_kind':classify(out)};members.append(item);identify(out,item,'archive-member')
  if item['nested_archive_kind']:visit(out,label+'::decompressed-payload',depth+1)
try:
 native_pdfs=[]
 for asset in intake['all_assets_in_original_order']:
  path=Path(asset['path']);item={'path':str(path),'bytes':asset['bytes'],'SHA256':asset['SHA256'],'original_native_API_asset_key':asset['original_api_file_object']['key']}
  before=len(pdfs);identify(path,item,'native-asset')
  if len(pdfs)>before:native_pdfs.extend(pdfs[before:])
  if classify(path):visit(path,asset['original_api_file_object']['key'],0)
 if len(native_pdfs)!=1:raise RuntimeError('source-only identification expects one native manuscript PDF; explicit disposition required for other case')
 selected=native_pdfs[0];matches=[a for a in pdfs if a['origin']=='archive-member' and a['SHA256']==selected['SHA256']]
 candidates=[]
 for pdf in matches:
  parent=Path(pdf['extracted_path']).parent
  adj=[a for a in tex if Path(a['extracted_path']).parent==parent]
  stem=[a for a in adj if Path(a['extracted_path']).stem==Path(pdf['extracted_path']).stem]
  chosen=stem if stem else adj
  if len(chosen)==1:candidates.append(chosen[0])
 direct=[a for a in candidates if a['depth']==0];eligible=direct if direct else candidates
 if not eligible and len(tex)==1:eligible=tex
 if len({a['SHA256'] for a in eligible})!=1:raise RuntimeError('controlling TeX not uniquely identified by exact reader/adjacency')
 control=eligible[0]
 custody={'UTC':now(),'containers':containers,'regular_members':members,'directory_entries':dirs,'regular_payload_occurrences':len(members),'archive_containers':len(containers),'nested_archives':sum(c['depth']>0 for c in containers),'expanded_bytes_all_depths':total,'unsupported_nested_formats':unsupported,'unsafe_names':[],'duplicate_names':[],'nonregular_payloads':[],'all_safe_regular_bodies_CRC_SHA256_read_and_extracted':True,'manuscript_scientifically_read':False,'deposited_code_executed':False}
 (S/'archive-custody.json').write_text(json.dumps(custody,indent=2)+'\n')
 readers={'UTC':now(),'selected_actual_PDF':selected,'byte_identical_embedded_readers':matches,'all_actual_PDF_occurrences':pdfs,'distinct_PDF_SHA256_count':len(set(a['SHA256'] for a in pdfs)),'all_TeX_candidates':tex,'controlling_TeX':control,'controlling_basis':'Exact native PDF byte match followed by same-stem or sole adjacent TeX; direct native outer-package candidate preferred over nested historical copies. Sole distinct eligible TeX hash.','identification_scope':'PDF header/pdfinfo metadata/page count, filenames/adjacency and hashes only; no scientific manuscript/TeX body or old review prose read.'}
 (A/'READERS_AND_TEX.json').write_text(json.dumps(readers,indent=2)+'\n')
 with (A/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 90% source acquisition: every safe archive container/body CRC-read, hashed and extracted inside preignored cache; all actual PDF/TeX occurrences inventoried and exact native manuscript/control identified structurally. No mathematical reading/execution. Source-ready/independent read-only closure and seal remain.\n')
 print(json.dumps({'record_id':RID,'native_manuscript':selected,'controlling_TeX_path':control['extracted_path'],'controlling_TeX_bytes':control['bytes'],'controlling_TeX_SHA256':control['SHA256'],'regular_payload_occurrences':len(members),'containers':len(containers),'nested_archives':custody['nested_archives'],'expanded_bytes':total,'all_PDF_occurrences':len(pdfs),'distinct_PDF_SHA256_count':readers['distinct_PDF_SHA256_count'],'TeX_candidates':len(tex)},indent=2))
except Exception as exc:
 (A/'ARCHIVE_EXCEPTION.json').write_text(json.dumps({'UTC':now(),'exception_type':type(exc).__name__,'exception':str(exc),'containers_completed':containers,'regular_members_completed':members,'source_ready':False},indent=2)+'\n');raise
