#!/usr/bin/env python3
"""Seal only deliberate public02 inputs/outputs and current exact operations."""
from pathlib import Path
import hashlib,json,stat
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];ROOT=P.parent
helpers=['accept_pr952.py','merge_pr952.py','run_pr952_zenodo.py','append_pr952_tracker.py','update_pr952_publication_ledger.py','finalize_pr952_and_gate_next.py']
local=['INTEGRATION.md','RESEARCH_LOG.md','PUBLIC_REPORT.json','PRESERVATION_CHECK.json','LOCAL_FREEZE_CHECK.json','INTEGRATION_PREVIEW.stdout.json','INTEGRATION_PREVIEW.stderr.txt','integration_inputs.py','test_operations.py','test_source_gate.py','SEAL_PUBLIC.py']
for prefix in ['TEST_PRE_FINAL','TEST_FINAL']:
 for suite in ['source_gate','operations']:
  for mode in ['normal','O','OO']:
   for suffix in ['launch.json','stdout.json','stderr.txt']:local.append(prefix+'_'+suite+'_'+mode+'.'+suffix)
paths=[P/n for n in helpers]+[ROOT/'zenodo_deposit_tool/zenodo.py']+[OWN/n for n in local];files={}
for path in paths:
 info=path.lstat()
 if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1 or stat.S_IMODE(info.st_mode)!=0o644:raise RuntimeError('public regular single-link0644 required: '+str(path))
 b=path.read_bytes();files[path.relative_to(ROOT).as_posix()]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':'100644'}
manifest={'schema':'pr952-operations-engineering-seal-v2','utc':datetime.now(timezone.utc).isoformat(),'path_base':'repository_root','pr':952,'problem_id':'10400145','original_pr_head':'989a532ae1d50894190d010a0a02ba8c3d71ee05','files':files,'explicit_public_allowlist':list(files),'previous_family_manifest_sha256':'3fc478015918320f37f980632b9f6aa78a012f5444a85404ccf56ab39e346c7e','acceptance_authority':False,'service_or_Git_mutations':0,'scratch_private_files_included':False}
raw=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode();(OWN/'MANIFEST.json').write_bytes(raw);h=hashlib.sha256(raw).hexdigest();(OWN/'MANIFEST.sha256').write_text(h+'  MANIFEST.json\n');print(json.dumps({'manifest_sha256':h,'files':len(files),'bytes':sum(x['bytes'] for x in files.values())}))
