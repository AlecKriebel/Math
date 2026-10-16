from pathlib import Path
import datetime as dt,hashlib,json,os,shutil,stat,subprocess,sys
R=Path("/Users/alec/Documents/Math")
D=R/"draft_pr_publication_program_20260930/audits/pr18_30001075/root_final_package_20261003/integration_step1"
a=D/"032.stdout"
base=a.read_bytes()
assert hashlib.sha256(base).hexdigest()=="b54818066c607ae5fbf1caff4b42084b75308998209372b4dda05217c7ca6d19"
started=dt.datetime.now(dt.timezone.utc).isoformat()
free_before=shutil.disk_usage(R).free
records=[]
for name,expected in [("025.stdout","f27d34bae864309480683a568e59631d2f1c7d791ef51f68d52cb3c5a2937846"),("028.stdout","91d7060baba018bb1e3327dd1f81d0fb7da4d56cc7b3b429fa5f00fbf31a2001")]:
 dest=D/name
 old=dest.read_bytes()
 oldstat=dest.lstat()
 assert stat.S_ISREG(oldstat.st_mode) and hashlib.sha256(old).hexdigest()==expected
 assert subprocess.check_output(["git","show","HEAD:"+str(dest.relative_to(R))],cwd=R)==old
 temp=D/(".owned_reflink_"+name)
 assert not temp.exists()
 command=["/bin/cp","-c","-p",str(a),str(temp)]
 begin=dt.datetime.now(dt.timezone.utc).isoformat()
 child=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out,err=child.communicate()
 operation={"argv":command,"pid":child.pid,"started_utc":begin,"finished_utc":dt.datetime.now(dt.timezone.utc).isoformat(),"exit_code":child.returncode,"stdout":out.decode(),"stderr":err.decode()}
 try:
  assert child.returncode==0,operation
  assert temp.read_bytes()==base
  with temp.open("r+b") as f:
   for i in range(0,len(old),4096):
    block=old[i:i+4096]
    if base[i:i+4096]!=block:
     f.seek(i);f.write(block)
   f.truncate(len(old));f.flush();os.fsync(f.fileno())
  os.chmod(temp,stat.S_IMODE(oldstat.st_mode))
  os.utime(temp,ns=(oldstat.st_atime_ns,oldstat.st_mtime_ns))
  assert temp.read_bytes()==old and dest.read_bytes()==old
  os.replace(temp,dest)
  assert dest.read_bytes()==old and a.read_bytes()==base
  assert stat.S_IMODE(dest.stat().st_mode)==stat.S_IMODE(oldstat.st_mode)
  operation.update(path_preserved=str(dest),bytes=len(old),sha256=expected,atomic_replacement_after_full_byte_check=True)
  records.append(operation)
 except BaseException:
  if temp.exists(): temp.unlink()
  raise
F=R/"draft_pr_publication_program_20260930/audits/pr50_10600042/alternate_preprint_access_20261004"
source=sys.orig_argv[-1]
(F/"deduplicate_owned_snapshot_blocks.py").write_text(source+"\n")
record={"started_utc":started,"finished_utc":dt.datetime.now(dt.timezone.utc).isoformat(),"actual_pid":os.getpid(),"scope":"Two completed PR18 committed audit snapshots; native filesystem clones with only differing blocks rewritten; both original filenames and exact contents preserved", "operations":records,"unique_data_lost":False,"actual_free_bytes_before":free_before,"actual_free_bytes_after":shutil.disk_usage(R).free,"freed_blocks_not_inferred_from_file_sizes":True,"executed_inline_source_sha256":hashlib.sha256(source.encode()).hexdigest(),"saved_source_note":"Executed inline source saved afterward with one additional newline, not a prelaunch disk snapshot"}
(F/"OWNED_SNAPSHOT_BLOCK_STORAGE_RECEIPT.json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record,indent=2))

