from pathlib import Path
import datetime as dt,hashlib,json,os,shutil,stat,sys
R=Path("/Users/alec/Documents/Math")
A="draft_pr_publication_program_20260930/audits/pr18_30001075/"
B="draft_pr_publication_program_20260930/audits/pr45_9900007/"
groups=[
 ("8bf8411d243537ebf9f46340514ea42c8ed2d7a07c9093fe91b08e7312e72259",[A+"primary_scope_family/tmp/simon_gmt_2018.txt",A+"priority_mechanism_family/tmp/simon2018.txt",A+"preprint_round2_adversary_family/tmp/private/captured-simon.txt",A+"preprint_round2_adversary_family/tmp/private/simon.txt"]),
 ("ba7fd4a53bf0f1d0ac54aec50bb72c4bba196b8e784d65cd0a7fd85131a3bf03",[A+"primary_scope_family/tmp/simon_gmt_2018.pdf",A+"priority_mechanism_family/tmp/simon2018.pdf",A+"preprint_round2_adversary_family/tmp/private/simon.pdf"]),
 ("85fb6e472777d2a6efc8fe6892472a5a377132ee1f4429d2ec1ff585e2dab021",[A+"primary_scope_family/tmp/demouth_thesis_2008.pdf",A+"priority_exact_family/tmp/demouth_thesis_v1.pdf",A+"tmp/root_primary/demouth-thesis-complete.pdf"]),
 ("6220db2356d8bab829a3899a290fc9dd8c439fdc8b97d328512a443925b393ad",[A+"primary_scope_family/tmp/shadows_2009_v1.pdf",A+"priority_exact_family/tmp/shadows_v1.pdf"]),
 ("452d18e681d4cdc95b4f7d2b1e5f0a5644028c85106cb3c93742445b8f948851",[B+"whole_current_source_first_family/COMPLETE_RAW_SQL_INSPECTION_BINDINGS.json",B+"whole_current_source_first_family/v3_inspection/COMPLETE_RAW_SQL_INSPECTION_BINDINGS.json"])]
started=dt.datetime.now(dt.timezone.utc).isoformat()
free_before=shutil.disk_usage(R).free
records=[]
for expected,names in groups:
 source=R/names[0]
 body=source.read_bytes()
 sa=source.lstat()
 assert stat.S_ISREG(sa.st_mode) and hashlib.sha256(body).hexdigest()==expected
 changed=[]
 for name in names[1:]:
  dest=R/name
  sb=dest.lstat()
  assert stat.S_ISREG(sb.st_mode) and dest.read_bytes()==body
  assert (stat.S_IMODE(sa.st_mode),sa.st_uid,sa.st_gid)==(stat.S_IMODE(sb.st_mode),sb.st_uid,sb.st_gid)
  if sa.st_ino==sb.st_ino: continue
  dest.unlink()
  try: os.link(source,dest)
  except BaseException:
   with dest.open("xb") as f: f.write(body)
   os.chmod(dest,stat.S_IMODE(sb.st_mode))
   raise
  assert dest.read_bytes()==body and source.stat().st_ino==dest.stat().st_ino
  changed.append(name)
 records.append({"all_paths_preserved":names,"bytes_each":len(body),"sha256_each":expected,"mode":stat.S_IMODE(sa.st_mode),"deduplicated_paths":changed})
F=R/"draft_pr_publication_program_20260930/audits/pr50_10600042/alternate_preprint_access_20261004"
source=sys.orig_argv[-1]
(F/"deduplicate_fixed_owned_copies.py").write_text(source+"\n")
record={"started_utc":started,"finished_utc":dt.datetime.now(dt.timezone.utc).isoformat(),"actual_pid":os.getpid(),"scope":"Explicit byte-identical completed PR18 source copies and immutable read-only program source-inspection snapshots; all paths, bodies and permissions preserved", "groups":records,"unique_data_lost":False,"file_content_or_math_result_changed":False,"actual_free_bytes_before":free_before,"actual_free_bytes_after":shutil.disk_usage(R).free,"freed_blocks_not_inferred_from_file_sizes":True,"executed_inline_source_sha256":hashlib.sha256(source.encode()).hexdigest(),"saved_source_note":"Saved executed inline code afterward with one additional newline, not a prelaunch disk snapshot"}
(F/"FIXED_OWNED_COPIES_STORAGE_RECEIPT.json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record,indent=2))

