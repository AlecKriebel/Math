from pathlib import Path,PurePosixPath
import datetime,hashlib,json,stat,subprocess,urllib.request,zipfile
P=Path(__file__).resolve().parents[2];R=P/'reviews/scope';S=P/'sources';S.mkdir(exist_ok=True)
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(v,msg):
 if not v:raise RuntimeError(msg)
def fetch(url,dest):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Research-catalogue-source-review/1.0'}),timeout=90) as res:
  b=res.read();resolved=res.url
 if dest.exists():need(dest.read_bytes()==b,'Existing source differs; do not overwrite '+str(dest))
 else:dest.write_bytes(b)
 return b,resolved
queue_path=P.parents[1]/'reconciliation/queue.json';queue=json.loads(queue_path.read_text())
entries=[]
def walk(v):
 if isinstance(v,dict):
  if v.get('record_id')==23383961 and 'sources' in v:entries.append(v)
  else:
   for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(queue);need(len(entries)==1,'queue identity');q=entries[0]
(R/'queue-entry.json').write_text(json.dumps({'queue_sha256':sha(queue_path.read_bytes()),'entry':q},indent=2)+'\n')
url='https://zenodo.org/api/records/23383961';raw,resolved=fetch(url,S/'record.json');rec=json.loads(raw)
need(rec['id']==23383961 and rec['metadata']['version']=='1.0','record identity/version')
expect={x['filename']:{'size':x['expected_bytes'],'md5':x['expected_md5'],'sha256':x.get('sha256')} for x in q['sources']}
expect.update({x['filename']:{'size':x['filesize'],'md5':x['checksum']} for x in q['supporting_files']})
need(set(f['key'] for f in rec['files'])==set(expect),'API/queue asset inventory')
files=[]
for f in rec['files']:
 name=f['key'];need(PurePosixPath(name).name==name,'unsafe API filename')
 link=f['links'].get('self') or f['links'].get('download');b,u=fetch(link,S/name);e=expect[name]
 need(len(b)==f['size']==e['size'],'API/queue size '+name)
 md5=hashlib.md5(b).hexdigest();need('md5:'+md5==f['checksum'] and md5==e['md5'],'API/queue MD5 '+name)
 if e.get('sha256'):need(sha(b)==e['sha256'],'queue SHA '+name)
 files.append({'name':name,'url':link,'resolved_url':u,'bytes':len(b),'md5':md5,'zenodo_checksum':f['checksum'],'sha256':sha(b),'retrieved_utc':now(),'integrity':'MATCH_API_AND_QUEUE'})
archives=[];readers=[];nested_counter=0

def scan_archive(path,target,depth=0):
 global nested_counter
 need(depth<6,'nested depth');rows=[];target.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(path) as z:
  entries=z.infolist();need(len(entries)<10000,'member bound');need(z.testzip() is None,'ZIP CRC')
  names=set();total=sum(i.file_size for i in entries);need(total<250_000_000,'expanded bound')
  for i in entries:
   rawname=i.filename;norm=rawname.rstrip('/') if i.is_dir() else rawname;n=PurePosixPath(norm)
   need(norm==str(n) and norm not in ('','.') and not n.is_absolute() and '..' not in n.parts and '\\' not in rawname and ':' not in n.parts[0] and '\x00' not in rawname,'unsafe member '+rawname)
   need(norm not in names,'duplicate member '+norm);names.add(norm)
   mode=i.external_attr>>16;kind=stat.S_IFMT(mode)
   need(not(i.flag_bits&1),'encrypted member')
   need(kind in ([0,stat.S_IFDIR] if i.is_dir() else [0,stat.S_IFREG]),'unsafe member type')
   p=target/n;need(not p.is_symlink(),'symlink at destination')
   if i.is_dir():p.mkdir(parents=True,exist_ok=True);b=b''
   else:
    b=z.read(i);need(len(b)==i.file_size,'member length');p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():need(p.read_bytes()==b,'existing extracted bytes differ')
    else:p.write_bytes(b)
   row={'member':rawname,'type':'directory' if i.is_dir() else 'regular','mode_octal':oct(mode),'hidden':any(t.startswith('.') for t in n.parts),'bytes':i.file_size,'compressed_bytes':i.compress_size,'crc32':f'{i.CRC:08x}','sha256':sha(b) if not i.is_dir() else None,'path':str(p.relative_to(S))}
   rows.append(row)
  archives.append({'path':str(path.relative_to(S)),'sha256':sha(path.read_bytes()),'depth':depth,'extraction_root':str(target.relative_to(S)),'crc_test':'PASS','members':rows})
 for row in rows:
  if row['type']!='regular':continue
  p=S/row['path']
  if p.suffix.lower()=='.pdf':read_pdf(p,embedded=True)
  elif p.suffix.lower()=='.zip':
   nested_counter+=1;scan_archive(p,S/'nested-source'/f'{nested_counter:02d}-{p.stem}',depth+1)
  elif p.suffix.lower() in ['.tar','.gz','.bz2','.xz','.7z','.rar']:
   raise RuntimeError('Additional archive format requires explicit safe mapping: '+str(p))

def read_pdf(p,embedded):
 result=subprocess.run(['pdfinfo',str(p)],capture_output=True,text=True,check=True)
 pages=next(int(x.split(':',1)[1]) for x in result.stdout.splitlines() if x.startswith('Pages:'))
 readers.append({'path':str(p.relative_to(S)),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size,'pages':pages,'embedded':embedded})
for f in files:
 p=S/f['name']
 if p.suffix.lower()=='.zip':scan_archive(p,S/'published-source'/p.stem)
 elif p.suffix.lower()=='.pdf':read_pdf(p,False)
(R/'archive-map.json').write_text(json.dumps({'created_utc':now(),'archives':archives},indent=2)+'\n')
(R/'reader-map.json').write_text(json.dumps({'created_utc':now(),'readers':readers,'groups_by_sha256':{h:[r['path'] for r in readers if r['sha256']==h] for h in sorted({r['sha256'] for r in readers})}},indent=2)+'\n')
receipt={'record_id':'23383961','metadata_url':url,'metadata_resolved_url':resolved,'record_sha256':sha(raw),'retrieved_utc':now(),'complete':True,'files':files,'queue_match':True,'archives':{'regular_members':sum(sum(x['type']=='regular' for x in a['members']) for a in archives),'outer_regular_members':sum(sum(x['type']=='regular' for x in a['members']) for a in archives if a['depth']==0),'nested_archives':nested_counter,'hidden_members':sum(sum(x['hidden'] for x in a['members']) for a in archives),'reader_documents':len(readers),'distinct_reader_hashes':len({r['sha256'] for r in readers})},'helper_execution':False}
(S/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
(R/'source-baseline.json').write_text(json.dumps({'created_utc':now(),'files_sha256':{str(f.relative_to(S)):sha(f.read_bytes()) for f in sorted(S.rglob('*')) if f.is_file()}},indent=2)+'\n')
print(json.dumps(receipt,indent=2))
