from pathlib import Path
import json, hashlib, datetime, os

A=Path(__file__).resolve().parent
B=A.parent/'pr95_10400120'
index=B/'CHECKPOINT_GITSHOW_STREAM_COMPACTION_20261006.json'
r=json.loads(index.read_text())
archive=B/r['archive']
if hashlib.sha256(archive.read_bytes()).hexdigest()!=r['archive_sha256']:
    raise RuntimeError('Compressed archive pin changed')
if not r['all_raw_bytes_retained'] or not r['written_archive_fully_reverified']:
    raise RuntimeError('Lossless readback not established')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt={'schema':'pr97-root-owned-storage-recovery/v1','UTC':now,'operator_PID':os.getpid(),'compaction_operator_PID':r['operator_PID'],'compaction_UTC':r['UTC'],'compressed_archive':str(archive),'archive_sha256':r['archive_sha256'],'archive_bytes':r['archive_bytes'],'private_recovery_index':str(index),'index_sha256':hashlib.sha256(index.read_bytes()).hexdigest(),'original_files':len(r['files']),'original_bytes':r['original_bytes'],'all_raw_bytes_retained':True,'all_streams_equal_immutable_main_ancestor_blobs':True,'all_tracked_files_and_original_journals_receipts_unchanged':True,'published_package_unchanged':True,'third_party_papers_or_browser_files_deleted':False,'fresh_write_capacity_restored':True,'restore_method':'Use the private index to identify original_path, bytes and SHA256. Read that exact member from the verified gzip tar (no extraction required), or use its recorded immutable git-show recovery_argv; require original byte count and digest before restoring.','public_checkpoint_contains_archive_or_full_index':False,'PR97_publication_clearance':False,'program_completion_percent':13/99*100,'PR97_workflow_estimate_percent':30}
(A/'ROOT_OWNED_STORAGE_RECOVERY_20261006.json').write_text(json.dumps(receipt,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n### '+now+' — storage recovery\nRecovered write capacity by losslessly compacting 5,315 untracked Root-owned PR95 immutable-Git-output duplicates into a private verified gzip tar. All exact bytes and recovery source identities are preserved; tracked files, original process journals/receipts, source papers and the published package are unchanged. No browser or third-party files were deleted. Preparation resumes; PR97 publication clearance remains false. Estimated program completion 13.13%; PR97 workflow 30%.\n')
print(json.dumps({'UTC':now,'files':len(r['files']),'bytes_saved_before_index':r['original_bytes']-r['archive_bytes'],'all_raw_bytes_retained':True,'publication_clearance':False}))
