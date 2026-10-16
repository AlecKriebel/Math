from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
O=Path(__file__).resolve().parent
P=O.parent/'publication_package_v1'
r=json.loads((O/'FRESH_PORTABLE_RUN.json').read_text())
binding={'utc':datetime.now(timezone.utc).isoformat(),'tool_observed_parent_invocation':[r['python_executable'],'-B','-O',str(P/'portable_verification_01/verify_portable.py'),'--materials',str(P/'materials'),'--work-dir',str(O/'fresh_work'),'--output',str(O/'FRESH_PORTABLE_RUN.json'),'--jobs','2'],'bytecode_environment':'PYTHONDONTWRITEBYTECODE=1','runtime_environment':r['environment_overrides'],'driver_sha256':r['driver_sha256'],'fresh_receipt_sha256':hashlib.sha256((O/'FRESH_PORTABLE_RUN.json').read_bytes()).hexdigest(),'fresh_raw_sha256':hashlib.sha256((O/'FRESH_PORTABLE_RUN.json.raw.json.gz').read_bytes()).hexdigest(),'completed_utc':r['UTC_end'],'note':'Parent -O flag is bound to the actual execution tool invocation; child ordinary/-O flags are independently checked in raw records. Separate guard probe introspected optimized=True.'}
(O/'FRESH_EXECUTION_BINDING.json').write_text(json.dumps(binding,indent=2)+'\n')
with (O/'RESEARCH_LOG.md').open('a') as f:
 f.write('- '+datetime.now(timezone.utc).isoformat()+' — 85%: fresh28-case run PASS; own exact H/J,38,057 integer cases and24 near-circle/high-modulus/star/complex pole configurations PASS. Five driver guards under -O reject. Original-to-live ASTs differ only by assertion hardening; fresh/historical raw receipt bindings pass. Six PDF pages visually inspected in memory. Shared-storage ENOSPC prevented attempted preview/notes commands but no scientific run failed or was hidden; later stdout-only previews/direct writes succeeded.\n')
 f.write('- '+datetime.now(timezone.utc).isoformat()+' — 100%: completed bounded whole-package review. No substantive correction request found. All445 frozen inputs remain byte-identical; package181files/ZIP177entries and original20/native tree/blob identities rechecked. Final report distinguishes mathematical verification from finite diagnostics and does not grant readiness, novelty, priority or publication authorization.\n')
# Readability correction only in this review's report.
q=O/'FINAL_REPORT.md'
q.write_text(q.read_text().replace('-181 outer','- 181 outer').replace('-177 unique','- 177 unique'))
files={}
for p in sorted(O.rglob('*')):
 if p.is_file() and p.name!='AUTHORED_ALLOWLIST.json':
  b=p.read_bytes();files[str(p.relative_to(O))]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
manifest={'schema':'pr204-whole-package-adversary01-authored-allowlist-v1','utc':datetime.now(timezone.utc).isoformat(),'scope':str(O),'file_count_excluding_self':len(files),'files':files,'self_allowed_not_self_hashed':'AUTHORED_ALLOWLIST.json','all_authored_paths_in_assigned_scope':True,'disposition':'No substantive issue found in bounded review; no publication authorization'}
out=O/'AUTHORED_ALLOWLIST.json';out.write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'authored_files_including_allowlist':len(files)+1,'allowlist_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'report_sha256':files['FINAL_REPORT.md']['sha256'],'analytic_review_sha256':files['ANALYTIC_REVIEW.md']['sha256'],'fresh_receipt_sha256':binding['fresh_receipt_sha256'],'root':str(O)},indent=2))

