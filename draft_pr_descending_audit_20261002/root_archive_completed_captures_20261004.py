"""Losslessly archive completed root-only captures; verify every byte before removal."""
from pathlib import Path
import datetime,hashlib,json,shutil,stat,tarfile
P=Path(__file__).resolve().parent
D=P/'private_storage_recovery_20261004';D.mkdir(exist_ok=True)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def inventory(folder):
 result={}
 for p in sorted(folder.rglob('*')):
  assert not p.is_symlink()
  e={'mode':stat.S_IMODE(p.stat().st_mode),'type':'file' if p.is_file() else 'directory'}
  if p.is_file():
   b=p.read_bytes();e.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  else:assert p.is_dir()
  result[str(p.relative_to(folder))]=e
 return result
receipts=[]
for problem in ['pr359_30001370','pr364_30004048']:
 A=P/'audits'/problem
 for name in ['root_capture_private','root_replay_private']:
  folder=A/name
  if not folder.exists():continue
  assert folder.is_dir() and not folder.is_symlink() and folder.resolve().is_relative_to(A)
  assert not (folder/'ARCHIVED_CAPTURE.json').exists(),'Never archive a pointer or uncertain prior action.'
  records=inventory(folder);assert records
  label=problem+'_'+name
  archive=D/(label+'.tar.gz');manifest=D/(label+'.manifest.json')
  assert not archive.exists() and not manifest.exists()
  x={'utc':utc(),'status':'PREPARED','original_directory':str(folder),'files':records,
     'scope':'Completed root-only native captures; no current356/foreign/agent closed namespace or source downloads.'}
  manifest.write_text(json.dumps(x,indent=2)+'\n')
  with tarfile.open(archive,'w:gz',compresslevel=9) as t:
   t.dereference=True
   for rel in records:t.add(folder/rel,arcname=rel,recursive=False)
  verified={}
  with tarfile.open(archive,'r:gz') as t:
   members=t.getmembers();assert len(members)==len(records)
   for m in members:
    assert m.name in records and not Path(m.name).is_absolute() and '..' not in Path(m.name).parts
    e=records[m.name];assert m.mode==e['mode']
    if e['type']=='file':
     assert m.isfile() and m.size==e['bytes'];f=t.extractfile(m);h=hashlib.sha256();size=0
     while True:
      b=f.read(1024*1024)
      if not b:break
      size+=len(b);h.update(b)
     assert size==e['bytes'] and h.hexdigest()==e['sha256']
    else:assert m.isdir()
    verified[m.name]=True
  assert set(verified)==set(records) and inventory(folder)==records
  archive_hash=hashlib.sha256(archive.read_bytes()).hexdigest()
  x.update(status='ARCHIVE_VERIFIED_EVERY_BYTE_AND_MODE',verified_utc=utc(),archive=str(archive),archive_bytes=archive.stat().st_size,archive_sha256=archive_hash)
  manifest.write_text(json.dumps(x,indent=2)+'\n')
  shutil.rmtree(folder);folder.mkdir()
  pointer={'utc':utc(),'status':'LOSSLESS_VERIFIED_CAPTURE_ARCHIVE','archive':str(archive),'manifest':str(manifest),
     'archive_sha256':archive_hash,'payload_files':sum(e['type']=='file' for e in records.values()),
     'restoration':'Remove only this pointer; restore this exact archive into the original directory with tarfile after verifying archive SHA256. Full legacy root-capture commands require restoration first.',
     'original_bytes_paths_and_modes_preserved_in_archive':True,'closed_agent_namespaces_or_public_papers_changed':False}
  (folder/'ARCHIVED_CAPTURE.json').write_text(json.dumps(pointer,indent=2)+'\n')
  receipts.append(pointer);print(json.dumps({'directory':str(folder),'files':pointer['payload_files'],'archive_bytes':x['archive_bytes'],'status':pointer['status']}),flush=True)
result={'utc':utc(),'status':'COMPLETE_LOSSLESS_ROOT_CAPTURE_STORAGE_RECOVERY','receipts':receipts,
 'math_results_and_published_files_unchanged':True,'percent_pr356_workflow':50}
(P/'ROOT_COMPLETED_CAPTURE_ARCHIVE_RECOVERY_20261004.json').write_text(json.dumps(result,indent=2)+'\n')
