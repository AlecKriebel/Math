from pathlib import Path,PurePosixPath
import json,urllib.request,hashlib,datetime,zipfile,stat
base=Path(__file__).resolve().parents[2];src=base/'sources'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
rec=json.loads((src/'record.json').read_text())
receipt={'record_id':'21753997','record_url':'https://zenodo.org/api/records/21753997','record_sha256':hashlib.sha256((src/'record.json').read_bytes()).hexdigest(),'retrieved_utc':now(),'complete':False,'files':[],'archives':[]}
for f in rec['files']:
 name=f['key'];safe=PurePosixPath(name);assert not safe.is_absolute() and '..' not in safe.parts
 p=src/name;p.parent.mkdir(parents=True,exist_ok=True);md5=hashlib.md5();sha=hashlib.sha256();total=0
 import concurrent.futures
 ranged_url='https://zenodo.org/records/21753997/files/'+name+'?download=1'
 chunk_size=4*1024*1024
 ranges=[(a,min(a+chunk_size,f['size'])-1) for a in range(0,f['size'],chunk_size)]
 def getpart(ab):
  a,b=ab
  request=urllib.request.Request(ranged_url,headers={'Range':f'bytes={a}-{b}'})
  with urllib.request.urlopen(request,timeout=90) as response:
   assert response.status==206 and response.headers.get('Content-Range')==f"bytes {a}-{b}/{f['size']}",dict(response.headers)
   data=response.read();assert len(data)==b-a+1
   return data
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool,p.open('wb') as out:
  for data in pool.map(getpart,ranges):
   out.write(data);md5.update(data);sha.update(data);total+=len(data)
   if total%(16*1024*1024)==0:print(json.dumps({'downloaded_bytes':total,'expected_bytes':f['size'],'utc':now(),'method':'validated_http_ranges'}),flush=True)
 resolved=ranged_url;ct='application/zip'
 assert total==f['size'] and md5.hexdigest()==f['checksum'].split(':')[1]
 assert total==180108207 and md5.hexdigest()=='4d4c43174a28c17a82b8365ead817975'
 receipt['files'].append({'name':name,'url':f['links']['self'],'resolved_url':resolved,'bytes':total,'md5':md5.hexdigest(),'zenodo_checksum':f['checksum'],'sha256':sha.hexdigest(),'retrieved_utc':now(),'queue_integrity':'PASS','content_type':ct})
 print(json.dumps({'archive_download_verified':receipt['files'][-1]}),flush=True)
 entries=[];selected=[];readers=[]
 with zipfile.ZipFile(p) as z:
  for m in z.infolist():
   pp=PurePosixPath(m.filename);mode=(m.external_attr>>16)&0xFFFF
   assert not pp.is_absolute() and '..' not in pp.parts and '\\' not in m.filename
   assert not stat.S_ISLNK(mode) and (m.is_dir() or stat.S_IFMT(mode) in (0,stat.S_IFREG)),m.filename
   entries.append({'path':m.filename,'bytes':m.file_size,'compressed_bytes':m.compress_size,'crc32':format(m.CRC,'08x')})
   if '/weakly_reversible_continuum_no_common_factor/' in m.filename:
    selected.append(m)
  for m in selected:
   if m.is_dir():continue
   data=z.read(m) # enforces member CRC; retained hash identifies bytes
   out=src/'published-source'/m.filename;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
   if m.filename.lower().endswith('.pdf'):readers.append(m.filename)
   next(e for e in entries if e['path']==m.filename).update(sha256=hashlib.sha256(data).hexdigest(),extracted=True)
 receipt['archives'].append({'name':name,'safe_paths_checked_for_all_members':True,'links_special_nodes_rejected':True,'members_count':len(entries),'selected_work_files_extracted':sum(not m.is_dir() for m in selected),'selection':'All members below weakly_reversible_continuum_no_common_factor; other monorepo projects retained only in authenticated complete ZIP.','crc_scope':'All selected members read and CRC checked; complete archive MD5/SHA256 binds all bytes.','reader_pdf_members':readers,'members':entries})
receipt['complete']=True;(src/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'complete':True,'files':receipt['files'],'archives':[{k:v for k,v in a.items() if k!='members'} for a in receipt['archives']]},indent=2))
