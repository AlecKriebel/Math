"""Standalone read-only complete verifier; externally hash these bytes before use."""
from pathlib import Path
import argparse,hashlib,json,tarfile,os,io
P=Path(__file__).resolve().parent
def need(ok,m):
 if not ok:raise RuntimeError(m)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def strict(raw):
 def pairs(items):
  d={}
  for k,v in items:need(k not in d,'Duplicate key');d[k]=v
  return d
 def bad(v):raise RuntimeError('Nonfinite JSON')
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
def main():
 p=argparse.ArgumentParser();p.add_argument('--source-sha256',required=True);p.add_argument('--packet-sha256',required=True);a=p.parse_args();raw=(P/'RECOVERY_MANIFEST.json').read_bytes();need(pin(raw)['sha256']==a.packet_sha256,'Packet anchor differs');m=strict(raw)
 actualfiles={x.relative_to(P).as_posix() for x in P.rglob('*') if x.is_file()};actualdirs={x.relative_to(P).as_posix() for x in P.rglob('*') if x.is_dir()};need(actualfiles=={e['path'] for e in m['files']}|{'RECOVERY_MANIFEST.json','RECOVERY_MANIFEST.sha256'} and actualdirs=={e['path'] for e in m['directories']},'Closed namespace differs')
 for e in m['files']+m['directories']:
  path=P/e['path'];s=path.lstat();need(not path.is_symlink() and s.st_mode&0o777==e['mode'] and s.st_mtime_ns==e['mtime_ns'] and s.st_nlink==e['nlink'],'Packet metadata differs: '+e['path'])
  if 'sha256' in e:need(pin(path.read_bytes())=={k:e[k] for k in ['bytes','sha256']},'Packet bytes differ')
 need(pin((P/'SOURCE_MANIFEST.json').read_bytes())['sha256']==a.source_sha256,'Source anchor differs');source=strict((P/'SOURCE_MANIFEST.json').read_bytes())
 for name,e in source['files'].items():need(pin((P/name).read_bytes())==e,'Runtime source differs')
 b=strict((P/'INPUT_BINDINGS.json').read_bytes())
 for name,e in b['refs'].items():
  path=Path(name);need(not any(x.is_symlink() for x in [path,*path.parents]) and pin(path.read_bytes())==e,'External source/evidence differs')
 prefix=strict((P/'private/CURRENT_CASE_PREFIX.json').read_bytes());need(pin((P/'private/CURRENT_CASE_PREFIX.json').read_bytes())==b['current_prefix'],'Current prefix pin');case=Path(prefix['case_path'])
 for e in prefix['entries']:
  path=case if e['path']=='.' else case/e['path'];s=path.lstat();need(not path.is_symlink() and s.st_dev==e['device'] and s.st_ino==e['inode'] and s.st_mode&0o777==e['mode'],'Original prefix identity differs')
  if e['kind']=='file':need(s.st_mtime_ns==e['mtime_ns'] and s.st_nlink==e['nlink'] and pin(path.read_bytes())=={k:e[k] for k in ['bytes','sha256']},'Original prefix file differs')
  else:need(path.is_dir(),'Original prefix directory differs')
 archive=P/'private/CURRENT_CASE_PREFIX.tar.xz';need(pin(archive.read_bytes())==b['current_prefix_archive'],'Archive pin differs');member_count=0
 with tarfile.open(archive,'r:xz') as t:
  members=t.getmembers();need(len(members)==len(prefix['entries']),'Archive count differs')
  for member,e in zip(members,prefix['entries']):
   need(member.name==e['path'] and member.mode==e['mode'] and int(member.pax_headers['custody_mtime_ns'])==e['mtime_ns'],'Archive metadata differs')
   if e['kind']=='file':need(pin(t.extractfile(member).read())=={k:e[k] for k in ['bytes','sha256']},'Archive member differs');member_count+=1
 # All completed owned test archives get complete-member, not name-only, readback.
 testfiles=0
 for manifest in (P/'private').rglob('*.manifest.json'):
  d=strict(manifest.read_bytes());arc=manifest.parent/d['archive'];need(pin(arc.read_bytes())==d['archive_pin'],'Test archive differs')
  with tarfile.open(arc,'r:xz') as t:
   members=t.getmembers();need(len(members)==len(d['entries']),'Test archive count')
   for member,e in zip(members,d['entries']):
    need(member.name==e['path'] and member.mode==e['mode'] and int(member.pax_headers['custody_mtime_ns'])==e['mtime_ns'],'Test member metadata')
    if e['kind']=='file':need(pin(t.extractfile(member).read())=={k:e[k] for k in ['bytes','sha256']},'Test member bytes');testfiles+=1
 # Compact completed-run container retains exact nested raw evidence and manifests.
 group=strict((P/'private/COMPLETED_RUNS_CUSTODY.json').read_bytes());group_path=P/'private'/group['archive'];need(pin(group_path.read_bytes())==group['archive_pin'],'Completed group archive differs');contents={}
 with tarfile.open(group_path,'r:xz') as t:
  members=t.getmembers();need(len(members)==len(group['entries']),'Completed group namespace')
  for member,e in zip(members,group['entries']):
   need(member.name==e['path'] and member.mode==e['mode'] and int(member.pax_headers['custody_mtime_ns'])==e['mtime_ns'],'Completed group metadata')
   if e['kind']=='file':
    body=t.extractfile(member).read();need(pin(body)=={k:e[k] for k in ['bytes','sha256']},'Completed group payload');contents[member.name]=body
 for name,body in contents.items():
  if not name.endswith('.manifest.json'):continue
  d=strict(body);arcname=str(Path(name).parent/d['archive']);payload=contents[arcname];need(pin(payload)==d['archive_pin'],'Nested test archive pin')
  with tarfile.open(fileobj=io.BytesIO(payload),mode='r:xz') as t:
   members=t.getmembers();need(len(members)==len(d['entries']),'Nested archive count')
   for member,e in zip(members,d['entries']):
    need(member.name==e['path'] and member.mode==e['mode'] and int(member.pax_headers['custody_mtime_ns'])==e['mtime_ns'],'Nested archive metadata')
    if e['kind']=='file':need(pin(t.extractfile(member).read())=={k:e[k] for k in ['bytes','sha256']},'Nested archive member bytes');testfiles+=1
 diagnosis=strict((P/'ROOT_DIAGNOSIS_PIN.json').read_bytes());need(pin(Path(diagnosis['external_read_only_input']).read_bytes())==diagnosis['pin'],'Root diagnosis differs')
 # Original source/dependencies and complete trusted current Journal are read-only.
 core=P.parent/'publication_operations_preparation_07';bootraw=(core/'bootstrap.py').read_bytes();need(pin(bootraw)==b['refs'][str(core/'bootstrap.py')],'Original bootstrap pin');ns={'__name__':'read_only_checked_bootstrap','__file__':str(core/'bootstrap.py')};exec(compile(bootraw,str(core/'bootstrap.py'),'exec',dont_inherit=True),ns);load,_=ns['load_verified'](core,'193013d467111f11726f151ddc2a4f38b0dfa5868950042d860cfdb7f4845148','22c4e8c67a657798c4ffd93c2ab4fcfd33868c716bf7c29c17607692f88b762d');common=load('common');common.Journal(case,strict((case/'HEADER.json').read_bytes())).verify();common.authority(P.parent/'ROOT_PR1208_OPS07_ACTION_ADOPTION.json',b['original_authority_sha256'],'reconcile')
 old=P.parent/'publication_samecase_recovery_preparation01';og={'__name__':'checked_readonly_prior_guard','__file__':str(old/'recovery_guard.py')};exec(compile((old/'recovery_guard.py').read_bytes(),str(old/'recovery_guard.py'),'exec',dont_inherit=True),og);oc=og['contract'](old,b['recovery01_source_sha256']);og['verify_authorization'](oc,b['recovery01_authority_sha256'],'reconcile',lambda:None);og['packet_check'](old,b['refs'][str(old/'RECOVERY_MANIFEST.json')]['sha256']);adapter={'__name__':'checked_readonly_prior_adapter','__file__':str(old/'recovery_adapter.py')};exec(compile((old/'recovery_adapter.py').read_bytes(),str(old/'recovery_adapter.py'),'exec',dont_inherit=True),adapter);captures=adapter['capture_namespace'](case/'reads',strict)[0]
 print(json.dumps({'status':'PASS_READ_ONLY','packet_files':len(m['files']),'packet_dirs':len(m['directories']),'original_CASE_files_fully_read':member_count,'current_capture_pairs':captures,'original_core_Journal_and_prior_authorities':True,'test_archive_files_fully_read':testfiles,'source_and_all_external_pins':True,'production_CASE_changed':False,'readiness':False}))
if __name__=='__main__':main()
