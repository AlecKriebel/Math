from pathlib import Path,PurePosixPath
import zipfile,tarfile,io,gzip,bz2,lzma,hashlib,json,datetime,stat
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');S=P/'papers/23124601/sources';rows=[];total=0;counter=0
sha=lambda b:hashlib.sha256(b).hexdigest()
def safe(name):
 q=PurePosixPath(name)
 if q.is_absolute() or '\\' in name or any(x in ('','..','.') for x in q.parts) or not q.parts:raise ValueError(('unsafe path',name))
 return Path(*q.parts)
def store(b,out):
 global total,counter
 counter+=1;total+=len(b)
 if counter>5000 or total>512*1024*1024 or len(b)>64*1024*1024:raise ValueError('bounded archive limit')
 out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('xb') as f:f.write(b)
def inspect(b,label,out,depth=0):
 if depth>6:raise ValueError('archive recursion limit')
 if zipfile.is_zipfile(io.BytesIO(b)):
  seen=set()
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   for ordinal,m in enumerate(z.infolist()):
    rel=safe(m.filename.rstrip('/'));name=rel.as_posix()
    if name in seen:raise ValueError(('duplicate canonical path',label,name))
    seen.add(name)
    mode=(m.external_attr>>16)&0xFFFF
    if stat.S_ISLNK(mode):raise ValueError(('symlink',name))
    if m.is_dir():continue
    body=z.read(m);assert len(body)==m.file_size
    dest=out/rel;store(body,dest)
    rows.append({'archive':label,'ordinal':ordinal,'member':m.filename,'path':str(dest.relative_to(S)),'bytes':len(body),'crc32':format(m.CRC,'08x'),'sha256':sha(body),'depth':depth,'container':'zip'})
    inspect(body,label+'!'+m.filename, S/'nested-archive-members'/str(counter),depth+1)
  return
 try:t=tarfile.open(fileobj=io.BytesIO(b),mode='r:*')
 except (tarfile.TarError,EOFError):t=None
 if t:
  seen=set()
  with t:
   for ordinal,m in enumerate(t):
    rel=safe(m.name.rstrip('/'));name=rel.as_posix()
    if name in seen:raise ValueError(('duplicate canonical path',label,name))
    seen.add(name)
    if m.isdir():continue
    if not m.isfile():raise ValueError(('nonregular tar',label,name,m.type))
    f=t.extractfile(m);body=f.read();assert len(body)==m.size;dest=out/rel;store(body,dest)
    rows.append({'archive':label,'ordinal':ordinal,'member':m.name,'path':str(dest.relative_to(S)),'bytes':len(body),'sha256':sha(body),'depth':depth,'container':'tar'})
    inspect(body,label+'!'+m.name,S/'nested-archive-members'/str(counter),depth+1)
  return
 # Standalone compressed streams; tar detection above already handles tar compression.
 for magic,decode,suffix in [(b'\x1f\x8b',gzip.decompress,'gzip'),(b'BZh',bz2.decompress,'bzip2'),(b'\xfd7zXZ\x00',lzma.decompress,'xz')]:
  if b.startswith(magic):
   body=decode(b);dest=out/('decompressed.'+suffix);store(body,dest)
   rows.append({'archive':label,'ordinal':0,'member':'<decompressed stream>','path':str(dest.relative_to(S)),'bytes':len(body),'sha256':sha(body),'depth':depth,'container':suffix})
   inspect(body,label+'!<stream>',S/'nested-archive-members'/str(counter),depth+1);return
b=(S/'wajnryb-artin-a5-verification.zip').read_bytes();inspect(b,'wajnryb-artin-a5-verification.zip',S/'published-source')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'regular_member_occurrences':counter,'expanded_bytes_across_occurrences':total,'safe_paths_unique_within_containers':True,'nested_container_occurrences':sorted({r['archive'] for r in rows if r['depth']>0}),'members':rows}
(S/'archive-custody.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'regular':counter,'expanded':total,'nested':out['nested_container_occurrences'],'pdfs':[(r['path'],r['bytes'],r['sha256']) for r in rows if r['member'].lower().endswith('.pdf')],'tex':[r['path'] for r in rows if r['member'].lower().endswith('.tex')],'programs':[r['path'] for r in rows if r['member'].lower().endswith(('.py','.sh'))]},indent=2))
