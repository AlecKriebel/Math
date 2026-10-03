#!/usr/bin/env python3
"""Self-only first-party recursive closure; ROOT captures this child externally."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat
B=Path(__file__).resolve().parent;manifest=B/'SELF_MANIFEST.json'
assert (B/'REPORT.md').is_file() and (B/'VERDICT.json').is_file() and (B/'EVIDENCE_VALIDATION_RECEIPT.json').is_file()
files=[];dirs=[]
for p in sorted(B.rglob('*')):
 assert not p.is_symlink(),str(p)
 if p.is_file() and p!=manifest:
  p.chmod(0o444);data=p.read_bytes();files.append({'path':p.relative_to(B).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'full_mode':stat.S_IMODE(p.stat().st_mode)})
 elif p.is_dir():dirs.append({'path':p.relative_to(B).as_posix(),'full_mode':stat.S_IMODE(p.stat().st_mode)})
out={'schema':'pr47-cover-self-only-recursive-closure/v1','created_utc':datetime.now(timezone.utc).isoformat(),'actual_closing_child_pid':os.getpid(),'root':str(B),'sole_self_excluded_from_members':'SELF_MANIFEST.json','sole_self_declared_full_mode':0o444,'root_directory_full_mode':stat.S_IMODE(B.stat().st_mode),'files':files,'directories':dirs,'all_first_party_files_full0444':True,'foreign_download_or_cache_SQL_or_headers_or_OCR_or_pixels_retained':False,'required_external_outer_capture':'ROOT writes separately completed capture outside family after this child exits; this manifest does not certify an unfinished outer capture.'}
manifest.write_text(json.dumps(out,indent=2)+'\n');manifest.chmod(0o444)
actual_files=sorted(p.relative_to(B).as_posix() for p in B.rglob('*') if p.is_file())
assert actual_files==sorted([r['path'] for r in files]+['SELF_MANIFEST.json'])
assert sorted(p.relative_to(B).as_posix() for p in B.rglob('*') if p.is_dir())==[r['path'] for r in dirs]
for r in files:
 p=B/r['path'];data=p.read_bytes();assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
assert stat.S_IMODE(manifest.stat().st_mode)==0o444
print(json.dumps({'closure_completed_inside_child':True,'actual_child_pid':os.getpid(),'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'member_files_plus_sole_self':len(files)+1,'exact_directories':len(dirs),'all_file_modes_full0444':True,'external_outer_capture_pending':True},indent=2))
