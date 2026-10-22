#!/usr/bin/env python3
"""Seal a deliberate public allowlist; no recursion into private/tmp directories."""
from pathlib import Path
import hashlib,json,stat
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];ROOT=P.parent
helpers=['accept_pr952.py','merge_pr952.py','run_pr952_zenodo.py','append_pr952_tracker.py','update_pr952_publication_ledger.py','finalize_pr952_and_gate_next.py']
local=['INTEGRATION.md','RESEARCH_LOG.md','PUBLIC_REPORT.json','integration_inputs.py','test_operations.py','SEAL_PUBLIC.py','LOCAL_FREEZE_CHECK.json','LOCAL_FREEZE_CHECK_FINAL.json','INTEGRATION_PREVIEW.stdout.json','INTEGRATION_PREVIEW.stderr.txt','INTEGRATION_FINAL_PREVIEW.stdout.json','INTEGRATION_FINAL_PREVIEW.stderr.txt']
for attempt in ['01','02','03','04']:
 for mode in ['normal','O','OO']:
  for suffix in ['launch.json','stdout.json','stderr.txt']:local.append('TEST_ATTEMPT'+attempt+'_'+mode+'.'+suffix)
paths=[P/n for n in helpers]+[ROOT/'zenodo_deposit_tool/zenodo.py']+[OWN/n for n in local]
files={}
for path in paths:
 info=path.lstat()
 if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1 or stat.S_IMODE(info.st_mode)!=0o644:raise RuntimeError('public regular single-link0644 required: '+str(path))
 data=path.read_bytes();files[path.relative_to(ROOT).as_posix()]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'mode':'100644'}
manifest={'schema':'pr952-operations-engineering-seal-v1','utc':datetime.now(timezone.utc).isoformat(),'path_base':'repository_root','problem_id':'10400145','pr':952,'original_pr_head':'989a532ae1d50894190d010a0a02ba8c3d71ee05','files':files,'explicit_public_allowlist':list(files),'acceptance_authority':False,'service_or_Git_mutations':0,'scratch_private_files_included':False}
raw=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode();(OWN/'MANIFEST.json').write_bytes(raw);digest=hashlib.sha256(raw).hexdigest();(OWN/'MANIFEST.sha256').write_text(digest+'  MANIFEST.json\n');print(json.dumps({'manifest_sha256':digest,'files':len(files),'bytes':sum(x['bytes'] for x in files.values())}))
