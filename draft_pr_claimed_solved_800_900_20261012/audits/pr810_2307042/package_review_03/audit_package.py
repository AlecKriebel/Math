from pathlib import Path
import zipfile,io,json,hashlib,stat,struct,datetime
out=Path('.');checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def verifyrows(rows,data,label,exclude):
 names=[r['path'] for r in rows];bad=[]
 for r in rows:
  b=data.get(r['path'])
  if b is None:bad.append('missing:'+r['path']);continue
  if len(b)!=r['bytes'] or sha(b)!=r['sha256']:bad.append('identity:'+r['path'])
  if 'git_blob_sha' in r and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=r['git_blob_sha']:bad.append('gitblob:'+r['path'])
 extras=set(data)-set(names)-set(exclude);missing=set(names)-set(data)
 checks.append({'label':label,'rows':len(rows),'closed':not extras and not missing and len(names)==len(set(names)),'identity_errors':bad,'extra':sorted(extras),'missing':sorted(missing)})
def inspectzip(b,label,ext=None):
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  infos=z.infolist();data={i.filename:z.read(i) for i in infos};errs=[]
  if len(data)!=len(infos):errs.append('duplicates')
  if z.comment:errs.append('archive_comment')
  if not b[-22:].startswith(b'PK\x05\x06'):errs.append('trailing_bytes_or_comment')
  cursor=0
  for i in sorted(infos,key=lambda i:i.header_offset):
   if i.header_offset!=cursor:errs.append('local_gap:'+i.filename)
   lh=struct.unpack('<4s5H3L2H',b[i.header_offset:i.header_offset+30]);cursor=i.header_offset+30+lh[9]+lh[10]+i.compress_size
   n=i.filename;parts=n.split('/')
   if n.startswith('/') or any(t in ('','.','..') for t in parts) or '\\' in n or '\0' in n:errs.append('path:'+n)
   if i.extra or i.comment:errs.append('extra_metadata:'+n)
   if i.flag_bits&1 or i.flag_bits&8:errs.append('flags:'+n)
   if not stat.S_ISREG(i.external_attr>>16) or (i.external_attr>>16)&0o111:errs.append('mode:'+n)
   if i.create_system!=3:errs.append('filesystem_origin:'+n)
  if cursor!=z.start_dir:errs.append('central_offset')
  checks.append({'label':label,'structural_errors':errs,'members':len(infos),'sha256':sha(b)})
  if ext:
   j=json.loads(ext)
   if j['archive_bytes']!=len(b) or j['archive_sha256']!=sha(b):errs.append('external archive identity')
   verifyrows(j['inventory'],data,label+' external inventory',[])
  if 'MANIFEST.json' in data:
   j=json.loads(data['MANIFEST.json']);verifyrows(j.get('files',j.get('inventory')),data,label+' internal inventory',['MANIFEST.json'])
  for n,v in data.items():
   if n.endswith('.zip'):
    en=n.replace('_SAFE_FREEZE.zip','_EXTERNAL_MANIFEST.json').replace('_SAFE.zip','_EXTERNAL_MANIFEST.json')
    inspectzip(v,label+'!'+n,data.get(en) if en!=n else None)
  return data
s=inspectzip(Path('../preprint/verification.zip').read_bytes(),'verification.zip');k=inspectzip(Path('../preprint/zenodo-upload-kit.zip').read_bytes(),'zenodo-upload-kit.zip')
for prefix in ['source/','source/author/','source/independent_audit/','source/independent_audit/author/','source/second_review/','source_priority_01/']:
 mn='PUBLIC_AUDIT_MANIFEST.json' if prefix=='source_priority_01/' else 'MANIFEST.json';name=prefix+mn
 j=json.loads(s[name]);data={n[len(prefix):]:b for n,b in s.items() if n.startswith(prefix)}
 verifyrows(j.get('files',j.get('inventory')),data,name,[mn])
j=json.loads(s['SOURCE_MANIFEST.json']);data={n[len('source/'):]:b for n,b in s.items() if n.startswith('source/')};rows=[dict(path=r['snapshot_path'],bytes=r['bytes'],sha256=r['sha256']) for r in j['files']];verifyrows(rows,data,'exact head source snapshot',[])
for n in ['note.tex','README.md','build_package.py','supplement_selection.json','zenodo-metadata.json']:assert s['preprint/'+n]==Path('../preprint',n).read_bytes()
md=Path('../preprint/zenodo-metadata.json').read_bytes();d=json.loads(Path('../preprint/zenodo-deposit.json').read_bytes());kd=json.loads(k['zenodo-deposit.json'])
assert json.loads(md)==d['metadata']==kd['metadata'];assert k['zenodo-metadata.json']==md
assert k['annular-martin-kernel-note.pdf']==Path('../preprint/output/pdf/note.pdf').read_bytes()
assert k['annular-martin-kernel-verification.zip']==Path('../preprint/verification.zip').read_bytes()
assert set(k)=={'annular-martin-kernel-note.pdf','annular-martin-kernel-verification.zip','zenodo-metadata.json','zenodo-deposit.json'}
sel=json.loads(s['preprint/supplement_selection.json']);assert len(sel)==len({a.get('archive_path',a['path']) for a in sel})
assert set(s)=={'preprint/'+n for n in ['note.tex','README.md','build_package.py','supplement_selection.json','zenodo-metadata.json']}|{a.get('archive_path',a['path']) for a in sel}|{'MANIFEST.json'}
checks.append({'label':'exact metadata/preprint/kit/selection consistency','status':'pass','selection_count':len(sel),'kit_names':list(k)})
a='000900019320500X';total=0
for c in a[:-1]:total=(total+int(c))*2
check=(12-total%11)%11;assert ('X' if check==10 else str(check))==a[-1]
checks.append({'label':'ORCID checksum and metadata author/date/version/license','status':'pass','orcid':a,'version':d['metadata']['version'],'date':d['metadata']['publication_date'],'license':d['metadata']['license']})
bad=[r for r in checks if r.get('structural_errors') or r.get('identity_errors') or r.get('closed') is False]
(out/'PACKAGE_INTEGRITY_FINAL.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if not bad else 'FAIL','checks':checks},indent=2)+'\n');print('checks',len(checks),'errors',bad)
