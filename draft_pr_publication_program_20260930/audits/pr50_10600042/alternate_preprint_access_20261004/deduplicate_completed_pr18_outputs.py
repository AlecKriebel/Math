from pathlib import Path
import datetime as dt,hashlib,json,os,shutil,stat,subprocess,sys
R=Path("/Users/alec/Documents/Math")
D=R/"draft_pr_publication_program_20260930/audits/pr18_30001075/root_final_package_20261003/integration_step1"
a,b=D/"032.stdout",D/"051.stdout"
started=dt.datetime.now(dt.timezone.utc).isoformat()
expected="b54818066c607ae5fbf1caff4b42084b75308998209372b4dda05217c7ca6d19"
sa,sb=a.lstat(),b.lstat()
assert stat.S_ISREG(sa.st_mode) and stat.S_ISREG(sb.st_mode)
assert (sa.st_size,stat.S_IMODE(sa.st_mode),sa.st_uid,sa.st_gid)==(sb.st_size,stat.S_IMODE(sb.st_mode),sb.st_uid,sb.st_gid)
body=a.read_bytes()
assert body==b.read_bytes() and hashlib.sha256(body).hexdigest()==expected
for p in [a,b]:
 committed=subprocess.check_output(["git","show","HEAD:"+str(p.relative_to(R))],cwd=R)
 assert committed==body
complete=json.loads((R/"draft_pr_publication_program_20260930/audits/pr18_30001075/publication/FULLY_COMPLETED_AND_RECONCILED.json").read_text())
assert complete["all_PR18_requirements_complete"] is True
free_before=shutil.disk_usage(R).free
b.unlink()
try:
 os.link(a,b)
except BaseException:
 with b.open("xb") as f: f.write(body)
 raise
assert a.read_bytes()==body==b.read_bytes()
assert a.stat().st_ino==b.stat().st_ino and stat.S_IMODE(b.stat().st_mode)==stat.S_IMODE(sb.st_mode)
F=R/"draft_pr_publication_program_20260930/audits/pr50_10600042/alternate_preprint_access_20261004"
source=sys.orig_argv[-1]
(F/"deduplicate_completed_pr18_outputs.py").write_text(source+"\n")
record={"started_utc":started,"finished_utc":dt.datetime.now(dt.timezone.utc).isoformat(),"actual_pid":os.getpid(),"scope":"Two byte-identical completed PR18 tracked audit outputs; both exact paths and contents preserved through hardlink deduplication", "paths":[str(a),str(b)],"bytes_each":len(body),"sha256_each":expected,"mode_preserved":True,"both_match_committed_git_objects":True,"raw_data_lost":False,"actual_free_disk_bytes_before":free_before,"actual_free_disk_bytes_after":shutil.disk_usage(R).free,"freed_blocks_not_inferred_from_file_size":True,"source_sha256":hashlib.sha256(source.encode()).hexdigest(),"source_capture_note":"Exact executed -c program captured from sys.orig_argv after the verified operation; not described as a prelaunch disk snapshot"}
(F/"OWNED_DUPLICATE_STORAGE_RECEIPT.json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record,indent=2))

