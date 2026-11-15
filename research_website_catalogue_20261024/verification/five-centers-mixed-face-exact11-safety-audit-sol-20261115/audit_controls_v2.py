"""Independent selected-function toy controls. No reviewed import, Git, network or live namespace."""
from pathlib import Path,PurePosixPath
import ast,hashlib,json,os,stat,struct,tempfile,types
D=Path(__file__).resolve().parent
O=D.parent/'five-centers-mixed-face-production-integration-preparation-sol-20261115'
EXPECTED='5ad717c1b8b1d7b80e5d1bbea5ef6558147ea03d24f24a10c8293483fe442d02'

def check(ok,label):
 if not ok:raise RuntimeError(label)
def rejected(call):
 try:call()
 except (RuntimeError,ValueError):return True
 raise RuntimeError('missing rejection')
def sha(b):return hashlib.sha256(b).hexdigest()
def definitions(path,names,env):
 b=path.read_bytes();tree=ast.parse(b);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 check({n.name for n in nodes}==set(names),'exact selected definitions')
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path)+' [selected toy definitions]','exec'),env)
 return env

def main():
 body=(O/'exact11_lib.py').read_bytes();check(sha(body)==EXPECTED,'current code bound before selected compilation')
 # Private proxies prevent patched toy calls from changing the process-wide standard library.
 osp=types.SimpleNamespace(**{name:getattr(os,name) for name in ['fstat','fsync','lseek','read','write','replace','close','SEEK_SET']})
 tmp=types.SimpleNamespace(mkstemp=tempfile.mkstemp)
 e={'Path':Path,'PurePosixPath':PurePosixPath,'hashlib':hashlib,'json':json,'os':osp,'stat':stat,'struct':struct,'tempfile':tmp,'LOCK_BODY':b'Exact11 publication lock; inspect run-state if interrupted\n'}
 selected=['need','sha','safe_rel','owned_entry','write_complete','validate_owned_buffer','unlink_owned','publish_buffer','parse_index','namespace','live_path','read','obj','pin','sealed_namespace','verify_preparation','adoption_fields']
 definitions(O/'exact11_lib.py',selected,e)
 e['LIVE_AUTHORIZED']=False;e['W']=D/'unreachable-live-root'
 results=[]
 with tempfile.TemporaryDirectory(prefix='independent-toys-',dir=D) as n:
  root=Path(n)
  def lock_at(p):
   fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600)
   e['write_complete'](fd,e['LOCK_BODY']);return fd
  def cleanup_lock(p,fd):
   try:e['unlink_owned'](p,fd)
   finally:os.close(fd)
  # 1. Hash and parse the same original seal buffer despite a subsequent path change.
  writer=root/'writer';writer.mkdir();payloads={}
  for k in range(961):
   name=f'p{k:04}';(writer/name).write_bytes(b'x');payloads[name]={'bytes':1,'SHA256':sha(b'x')}
  mb=json.dumps({'payloads':payloads,'directories':[]}).encode();(writer/'OWNED_MANIFEST.json').write_bytes(mb)
  sb=json.dumps({'manifest':{'bytes':len(mb),'SHA256':sha(mb)},'owned_payload_files':961,'marker':'authenticated-original'}).encode()
  seal_path=writer/'FINAL_SEAL.json';seal_path.write_bytes(sb)
  e.update(S=writer,A=root/'audit',STAGE_SEAL=sha(sb),AUDIT_SEAL='unused')
  real_read=e['read'];calls=[0]
  def changed_read(p):
   b=real_read(p)
   if Path(p)==seal_path:
    calls[0]+=1;seal_path.write_bytes(b'{"marker":"changed-after-read"}')
   return b
  e['read']=changed_read
  try:observed,rows=e['sealed_namespace']('writer')
  finally:e['read']=real_read
  check(calls[0]==1 and observed['marker']=='authenticated-original' and seal_path.read_bytes()!=sb,'same immutable buffer parse')
  results.append({'group':1,'mechanism':'same-buffer seal authentication','critical_reads':calls[0],'parsed_whole_authenticated_seal':observed,'toy_payloads':len(rows),'passed':True})
  # 2. Complete short/interrupted writes, same-FD readback, immutable buffer and distinct lock.
  destination=root/'destination';destination.write_bytes(b'old')
  alternate=root/'alternate';captured=b'whole checked 130131 buffer';alternate.write_bytes(captured);alternate.write_bytes(b'changed')
  lock=root/'held-lock';fd=lock_at(lock);identity=(os.fstat(fd).st_dev,os.fstat(fd).st_ino)
  original_write=osp.write;original_read=osp.read;attempts=[0]
  def shortwrite(d,b):
   attempts[0]+=1
   if attempts[0]==1:raise InterruptedError('toy interrupt')
   return original_write(d,b[:3])
  osp.write=shortwrite;osp.read=lambda d,n:original_read(d,min(n,2))
  try:e['publish_buffer'](captured,destination,lock,fd)
  finally:osp.write=original_write;osp.read=original_read
  try:
   check(destination.read_bytes()==captured and alternate.read_bytes()!=captured,'immutable captured bytes published')
   check((lock.lstat().st_dev,lock.lstat().st_ino)==identity and destination.lstat().st_ino!=identity[1],'distinct lock held')
   e['validate_owned_buffer'](lock,fd,e['LOCK_BODY'])
   results.append({'group':2,'mechanism':'captured buffer, short/interrupted writes and same-FD reads','write_attempts':attempts[0],'actual_published_hex':destination.read_bytes().hex(),'distinct_original_lock_held':True,'passed':True})
  finally:cleanup_lock(lock,fd)
  # 3. Reject zero progress; retain substituted foreign/symlink entries; close sibling FD.
  lock=root/'zero-lock';fd=lock_at(lock);destination.write_bytes(b'unchanged')
  osp.write=lambda d,b:0
  try:rejected(lambda:e['publish_buffer'](captured,destination,lock,fd))
  finally:osp.write=original_write
  try:check(destination.read_bytes()==b'unchanged','zero progress before destination write')
  finally:cleanup_lock(lock,fd)
  lock=root/'foreign-lock';fd=lock_at(lock);lock.unlink();lock.write_bytes(b'foreign inode')
  try:rejected(lambda:e['unlink_owned'](lock,fd));check(lock.read_bytes()==b'foreign inode','foreign lock retained')
  finally:os.close(fd)
  target=root/'retained-owned';fd=lock_at(target);alias=root/'symlink-lock';alias.symlink_to(target)
  try:rejected(lambda:e['unlink_owned'](alias,fd));check(alias.is_symlink() and target.exists(),'symlink remains')
  finally:os.close(fd)
  lock=root/'sibling-lock';fd=lock_at(lock);created=[];original_mkstemp=tmp.mkstemp
  def foreign_sibling(*a,**kw):
   d,p=original_mkstemp(*a,**kw);Path(p).unlink();Path(p).write_bytes(b'foreign sibling');created.append((d,p));return d,p
  tmp.mkstemp=foreign_sibling
  try:rejected(lambda:e['publish_buffer'](captured,destination,lock,fd))
  finally:tmp.mkstemp=original_mkstemp
  try:
   check(Path(created[0][1]).read_bytes()==b'foreign sibling','foreign sibling not unlinked')
   try:os.fstat(created[0][0])
   except OSError:closed=True
   else:closed=False
   check(closed,'sibling descriptor closed despite rejected cleanup')
  finally:cleanup_lock(lock,fd)
  results.append({'group':3,'mechanism':'zero progress and foreign/symlink ownership cleanup','destination_unchanged_on_zero_progress':True,'foreign_entries_retained':True,'sibling_descriptor_closed':closed,'passed':True})
  # 4. Demonstrate the admitted final-check-to-rename race without claiming isolation.
  destination.write_bytes(b'old-before-race');lock=root/'race-lock';fd=lock_at(lock);original_replace=osp.replace
  def race_replace(src,dst):
   Path(src).unlink();Path(src).write_bytes(b'foreign last-window bytes');return original_replace(src,dst)
  osp.replace=race_replace
  try:rejected(lambda:e['publish_buffer'](captured,destination,lock,fd))
  finally:osp.replace=original_replace
  try:
   check(destination.read_bytes()==b'foreign last-window bytes','residual interleaving demonstrated')
   results.append({'group':4,'mechanism':'documented residual rename window','foreign_bytes_reached_toy_destination_before_detection':True,'OS_isolation_claim':False,'passed_as_qualification_test':True})
  finally:cleanup_lock(lock,fd)
  # 5. Minimal native index: complete protected bytes, stat mutation, checksum rejection.
  def entry(p):
   h=bytearray(62);h[24:28]=struct.pack('>I',0o100644);h[40:60]=b'1'*20;h[60:62]=struct.pack('>H',len(p))
   b=bytes(h)+p+b'\0';return b+b'\0'*((-len(b))%8)
  records=[entry(p) for p in [b'a-protected',b'b-target',b'c-protected']]
  raw=b'DIRC'+struct.pack('>II',2,3)+b''.join(records);raw+=hashlib.sha1(raw).digest()
  parsed=e['parse_index'](raw,{b'b-target'});check(parsed['protected_record_count']==2,'two complete protected records')
  changed=bytearray(raw);changed[12]^=1;changed[-20:]=hashlib.sha1(changed[:-20]).digest();altered=e['parse_index'](bytes(changed),{b'b-target'})
  check(altered['protected']!=parsed['protected'] and altered['entries'][0][3]==parsed['entries'][0][3],'stat-only change detected beyond stage tuple')
  corrupted=bytearray(raw);corrupted[-1]^=1;rejected(lambda:e['parse_index'](bytes(corrupted),{b'b-target'}))
  results.append({'group':5,'mechanism':'native raw record preservation beyond mode/OID/path tuples','stat_only_mutation_detected':True,'bad_checksum_rejected':True,'original_full_index_hex':raw.hex(),'changed_full_index_hex':bytes(changed).hex(),'passed':True})
  # 6. Exact namespace adversaries and denial of false authority, entirely in own toys.
  pure={'Path':Path};definitions(O/'verify_preparation.py',['need','names'],pure);pure['CHECKS']=0
  loose=root/'pure-names';loose.mkdir();(loose/'payload').write_bytes(b'p');before=pure['names'](loose)
  (loose/'unexpected-empty').mkdir();os.mkfifo(loose/'unexpected-fifo');after=pure['names'](loose)
  check(before==after=={'payload'},'standalone file names ignore empty directory and FIFO')
  packet=root/'library-prep';packet.mkdir();(packet/'payload').write_bytes(b'p')
  manifest={'files':[{'path':'payload','bytes':1,'SHA256':sha(b'p')}]};mb=json.dumps(manifest).encode();(packet/'PREPARATION_MANIFEST.json').write_bytes(mb)
  cb=b'{}';(packet/'PREPARATION_CLOSURE.json').write_bytes(cb)
  sb=json.dumps({'MANIFEST_SHA256':sha(mb),'CLOSURE_SHA256':sha(cb),'owned_payload_count':1}).encode();(packet/'PREPARATION_SEAL.json').write_bytes(sb)
  e['O']=packet;e['verify_preparation']();(packet/'unlisted-empty').mkdir();run=packet/'run-state';run.mkdir();(run/'arbitrary-unsealed').write_bytes(b'not in manifest')
  e['verify_preparation']()
  audit=root/'audit';audit.mkdir();arows=[]
  for k in range(721):
   p=audit/f'a{k:04}';p.write_bytes(b'z');arows.append({'path':str(p),'bytes':1,'SHA256':sha(b'z')})
  amb=json.dumps({'files':arows,'directories':[]}).encode();(audit/'FINAL_MANIFEST.json').write_bytes(amb);(audit/'FINAL_CLOSURE.json').write_bytes(cb)
  asb=json.dumps({'bindings':{'FINAL_MANIFEST.json':{'bytes':len(amb),'SHA256':sha(amb)},'FINAL_CLOSURE.json':{'bytes':len(cb),'SHA256':sha(cb)}},'own_final_owned_payloads':721}).encode();(audit/'FINAL_SEAL.json').write_bytes(asb)
  e.update(A=audit,AUDIT_SEAL=sha(asb));e['sealed_namespace']('audit');(audit/'unexpected-empty').mkdir();e['sealed_namespace']('audit')
  template=json.loads((O/'ROOT_ADOPTION_TEMPLATE.json').read_bytes());rejected(lambda:e['adoption_fields'](template))
  rootreading=json.loads((O/'inputs/root-five-centers-mixed-face-stage-reading-20261115.json').read_bytes());rejected(lambda:e['adoption_fields'](rootreading))
  toy_live=root/'unreachable-live';toy_live.mkdir();(toy_live/'held').write_bytes(b'data');e['W']=toy_live
  rejected(lambda:e['read'](toy_live/'held'));rejected(lambda:e['namespace'](toy_live))
  results.append({'group':6,'mechanism':'strict namespace negative controls and false-authority gates','standalone_ignores_unlisted_empty_directory_and_FIFO':True,'library_prep_accepts_unlisted_empty_directory_and_arbitrary_run_state_payload':True,'audit_sealed_namespace_accepts_unlisted_empty_directory':True,'false_template_and_source_only_root_reading_rejected':True,'live_read_and_list_denied_in_own_toy':True,'strict_closed_directory_requirement_satisfied':False,'control_completed':True})
 print(json.dumps({'status':'COMPLETED_WITH_CONFIRMED_STRICT_NAMESPACE_BLOCKER','current_library_SHA256':EXPECTED,'control_groups':results,'reviewed_code_imported':False,'actual_website_or_real_git_read_list_or_commands':False,'production_authority_created':False,'all_filesystem_fixtures_within_own_temporary_child':True,'temporary_fixtures_removed_after_observation':True},indent=2))
if __name__=='__main__':main()
