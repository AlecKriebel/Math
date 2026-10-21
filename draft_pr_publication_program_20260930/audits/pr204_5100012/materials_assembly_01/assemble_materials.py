#!/usr/bin/env python3
"""Bounded154-file exclusive-copy assembly; no tests or package clearance."""
import sys
sys.dont_write_bytecode=True
import datetime,gzip,hashlib,json,os,pathlib,stat
HERE=pathlib.Path(__file__).resolve().parent
BASE=HERE.parent.resolve()
DEST=BASE/'publication_package_v1'
PIN='4ed6d852c19e811b87dc68e932888645f355487f16233f69bb3c747d9ab0d3fe'
KITPIN='d414035e74042c22fa2568942cf2cbee44e1b8750741f43d00ea7b33081e95e2'
def require(ok,message):
 if not ok:raise RuntimeError(message)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n'
def sha(x):return hashlib.sha256(x).hexdigest()
def hf(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while True:
   b=f.read(65536)
   if not b:break
   h.update(b)
 return h.hexdigest()
def record(name,data):
 with (HERE/name).open('xb') as f:f.write(data)
def snapshot(root,plan,readonly=False):
 out={}
 for rel,expected in plan.items():
  p=root/rel;require(p.resolve()==p and not p.is_symlink(),'Symlink input '+rel)
  s=p.stat();require(stat.S_ISREG(s.st_mode),'Nonregular input '+rel)
  if readonly:require(s.st_mode&0o222==0,'Unsealed writable source '+rel)
  h=hf(p);t=p.stat()
  require((s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(t.st_size,t.st_mtime_ns,t.st_ctime_ns),'Changed during read '+rel)
  require(h==expected['sha256'] and s.st_size==expected['bytes'],'Byte pin failed '+rel)
  out[rel]=dict(bytes=s.st_size,sha256=h,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns,mode=stat.S_IMODE(s.st_mode),device=s.st_dev,inode=s.st_ino,nlink=s.st_nlink)
 return out
def files():
 out=[]
 for name in ['materials','portable_verification_01']:
  root=DEST/name
  if not root.exists():continue
  require(root.is_dir() and not root.is_symlink(),'Bad destination root')
  for p in root.rglob('*'):
   require(not p.is_symlink(),'Destination symlink '+str(p))
   if not p.is_dir():out.append(str(p.relative_to(DEST)))
 return sorted(out)
def parent(p):
 require(DEST.is_dir() and not DEST.is_symlink(),'Bad package root')
 cur=DEST
 for part in p.relative_to(DEST).parts[:-1]:
  cur=cur/part;require(not cur.is_symlink(),'Destination parent symlink')
  cur.mkdir(exist_ok=True);require(cur.is_dir(),'Non-directory destination parent')
def copy(src,dst,expected,source_stat):
 parent(dst)
 fd=os.open(dst,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 h=hashlib.sha256();count=0
 try:
  with src.open('rb') as f:
   while True:
    block=f.read(65536)
    if not block:break
    h.update(block);count+=len(block);v=memoryview(block)
    while v:
     n=os.write(fd,v);require(n>0,'Zero write');v=v[n:]
  require(count==expected['bytes'] and h.hexdigest()==expected['sha256'],'Copy stream mismatch')
 finally:
  try:os.fchmod(fd,0o444)
  finally:os.close(fd)
 os.utime(dst,ns=(source_stat['mtime_ns'],source_stat['mtime_ns']))
 s=dst.stat()
 require(stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o444 and s.st_nlink==1 and s.st_uid==os.getuid(),'Destination ownership/type/mode/link count failed')
 require((s.st_dev,s.st_ino)!=(source_stat['device'],source_stat['inode']),'Hardlink destination')
 require(s.st_size==expected['bytes'] and hf(dst)==expected['sha256'],'Destination bytes failed')
 return dict(bytes=s.st_size,sha256=expected['sha256'],mode='0444',owner=s.st_uid,nlink=s.st_nlink,device=s.st_dev,inode=s.st_ino)
def main():
 require(not (HERE/'ASSEMBLY_RECEIPT.json').exists(),'Existing assembly outcome; refuse automatic rerun')
 start=utc();done=[];plan={};before=None;current=None;copies={}
 record('RESEARCH_LOG.md',('# Bounded materials assembly\n\n'+start+' — 0%: authorize142 scientific+12 portable copies. First patch-writer setup failed;173-byte direct-write diagnostic succeeded, no payload operations then. Root subsequently authorized19 curated existing files. Exclusive sequential copies, no hardlinks/tests/whole-package clearance.\n').encode())
 try:
  raw=(BASE/'portable_verification_01/INPUT_PINS.json').read_bytes();require(sha(raw)==PIN,'Pins changed')
  scientific=json.loads(raw)['files'];require(len(scientific)==142,'Scientific count')
  for rel,x in scientific.items():plan[rel]=dict(destination='materials/'+rel,**x)
  raw=(BASE/'portable_verification_01/AUTHORED_ALLOWLIST.json').read_bytes();require(sha(raw)==KITPIN,'Portable manifest changed')
  kit=json.loads(raw)['files'];require(len(kit)==11,'Kit count')
  for name,x in kit.items():plan['portable_verification_01/'+name]=dict(destination='portable_verification_01/'+name,**x)
  plan['portable_verification_01/AUTHORED_ALLOWLIST.json']=dict(destination='portable_verification_01/AUTHORED_ALLOWLIST.json',bytes=len(raw),sha256=sha(raw))
  plan=dict(sorted(plan.items()));require(len(plan)==154,'Copy count')
  curated_receipt=BASE/'package_preparation_01/CURATED_PUBLIC_PROVENANCE_01.json'
  curated=json.loads(curated_receipt.read_bytes())['public_provenance_files'];require(len(curated)==19,'Expected19 Root-curated existing paths')
  require(not(set(x['destination'] for x in plan.values())&set(curated)),'Curated path collision')
  require(files()==sorted(curated),'Unexpected existing destination file or missing authorized curated file')
  curated_before=snapshot(DEST,curated);before=snapshot(BASE,plan,True)
  record('SOURCE_DESTINATION_ALLOWLIST.json',enc(dict(scope='Only154 authorized content copies, excluding19 preexisting curated files; no whole-package clearance',files=plan,authorized_preexisting_curated_files=curated,curated_receipt_sha256=hf(curated_receipt))))
  with (HERE/'RESEARCH_LOG.md').open('a') as log:log.write(utc()+' — 20%:154 read-only sources pinned;19 existing curated paths authenticated;154 destination paths absent.\n')
  for i,(rel,x) in enumerate(plan.items(),1):
   current=dict(source=rel,destination=x['destination'],index=i)
   copies[x['destination']]=copy(BASE/rel,DEST/x['destination'],x,before[rel]);done.append(current)
   if i%40==0:
    with (HERE/'RESEARCH_LOG.md').open('a') as log:log.write(utc()+' — '+str(20+int(60*i/154))+'%: '+str(i)+'/154 exclusive regular0444 copies verified.\n')
  after=snapshot(BASE,plan,True);require(before==after,'Sources changed')
  curated_after=snapshot(DEST,curated);require(curated_before==curated_after,'Curated preexisting files changed')
  require(files()==sorted(list(curated)+list(copies)),'Destination set changed')
  for rel,x in copies.items():
   s=(DEST/rel).stat()
   require(hf(DEST/rel)==x['sha256'] and s.st_size==x['bytes'] and stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o444 and s.st_nlink==1 and s.st_uid==os.getuid(),'Final copy integrity '+rel)
  content=dict(scope='Authorized154-file assembly contribution only; not a package seal',file_count=154,scientific_files=142,portable_files=12,total_bytes=sum(x['bytes'] for x in copies.values()),files={r:{k:v for k,v in x.items() if k in ('bytes','sha256','mode')} for r,x in sorted(copies.items())})
  content_raw=enc(content);record('DESTINATION_CONTENT_ALLOWLIST.json',content_raw)
  custody=dict(source_before=before,source_after=dict(identical_to='source_before'),destination_regular_copy_records=copies,authorized_preexisting_curated_before=curated_before,authorized_preexisting_curated_after=dict(identical_to='authorized_preexisting_curated_before'))
  record('SOURCE_COPY_CUSTODY.json.gz',gzip.compress(enc(custody),mtime=0))
  receipt=dict(status='PASS',UTC_start=start,UTC_end=utc(),helper_sha256=hf(pathlib.Path(__file__)),scientific_files=142,portable_files=12,copied_files=154,total_bytes=content['total_bytes'],destination_manifest='DESTINATION_CONTENT_ALLOWLIST.json',destination_manifest_sha256=sha(content_raw),all154_sources_hash_size_mtime_ctime_mode_unchanged=True,all154_destinations_owned_regular_exclusive0444_nlink1=True,authorized19_preexisting_curated_files_unchanged=True,destination_hardlinks=0,tests_run=0,manuscript_metadata_PDF_ZIP_seal_written=False,whole_package_clearance=False,source_destination_plan_sha256=hf(HERE/'SOURCE_DESTINATION_ALLOWLIST.json'),source_copy_custody_sha256=hf(HERE/'SOURCE_COPY_CUSTODY.json.gz'),excluded=['private direct inventory','dependencies','caches','primary PDFs','unlisted material files'])
  record('ASSEMBLY_RECEIPT.json',enc(receipt))
  with (HERE/'RESEARCH_LOG.md').open('a') as log:log.write(utc()+' — 100%:154 copies, '+str(content['total_bytes'])+' bytes; source and19 curated before/after states unchanged; content manifest SHA256 '+sha(content_raw)+'. No tests or package clearance.\n')
  print(json.dumps(receipt,sort_keys=True));return 0
 except Exception as error:
  failure=dict(status='FAIL',UTC_start=start,UTC_end=utc(),error_type=type(error).__name__,error=str(error),failed_operation=current,completed_copies=done,no_retry_or_cleanup=True,whole_package_clearance=False)
  if before is not None:
   try:failure['sources_still_unchanged']=snapshot(BASE,plan,True)==before
   except Exception as other:failure['source_recheck_error']=str(other)
  if current is not None:
   p=DEST/current['destination']
   if p.exists():failure['preserved_partial_destination']=dict(path=current['destination'],bytes=p.stat().st_size,mode=oct(stat.S_IMODE(p.stat().st_mode)),sha256=hf(p))
  try:record('ASSEMBLY_RECEIPT.json',enc(failure))
  except Exception as other:failure['receipt_write_error']=str(other)
  try:
   with (HERE/'RESEARCH_LOG.md').open('a') as log:log.write(utc()+' — '+str(int(100*len(done)/154))+'% copies, FAIL '+repr(error)+'; operation preserved, no retry.\n')
  except Exception:pass
  print(json.dumps(failure,sort_keys=True),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
