#!/usr/bin/env python3
"""Seal deliberate public installed03 code/evidence; never recurse into private dirs."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];ROOT=P.parent
helpers=['accept_pr952.py','merge_pr952.py','run_pr952_zenodo.py','append_pr952_tracker.py','update_pr952_publication_ledger.py','finalize_pr952_and_gate_next.py']
local=['BASE_accept_pr952.py','PROPOSED_accept_pr952.py','PROPOSED_v01_accept_pr952.py','PROPOSED.patch','PROPOSED_v01.patch','build_proposal.py','test_native_recovery.py','test_native_recovery_attempt01.py','test_native_recovery_attempt02.py','test_native_recovery_attempt03.py','test_native_recovery_attempt04.py','test_operations_installed.py','test_source_gate_installed.py','integration_inputs.py','INTEGRATION.md','PROPOSAL_PLAN.md','PROPOSAL_READINESS.json','PROPOSAL_VERSIONS.json','PUBLIC_REPORT.json','INSTALL_RECEIPT.json','OPERATIONS_INVENTORY.json','OPERATIONS_INVENTORY.stderr.txt','OPERATIONS_INVENTORY_GENERATION.json','RESEARCH_LOG.md','RESEARCH_LOG_SUPERSEDED_TIMING_DRAFT.md','SEAL_PUBLIC.py']
for attempt in ['01','02','03','04']:
 for mode in ['normal','O','OO']:
  for suffix in ['launch.json','stdout.json','stderr.txt']:local.append('TEST_ATTEMPT'+attempt+'_'+mode+'.'+suffix)
for suite in ['native_recovery','operations','source_gate']:
 for mode in ['normal','O','OO']:
  for suffix in ['launch.json','stdout.json','stderr.txt']:local.append('TEST_INSTALLED_'+suite+'_'+mode+'.'+suffix)
files={}
for path in [P/name for name in helpers]+[ROOT/'zenodo_deposit_tool/zenodo.py']+[OWN/name for name in local]:
 info=path.lstat()
 if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1 or stat.S_IMODE(info.st_mode)!=0o644:raise RuntimeError('regular single-link0644 public file required: '+str(path))
 body=path.read_bytes();name=path.relative_to(ROOT).as_posix();files[name]={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'mode':'100644'}
core_key=(P/'accept_pr952.py').relative_to(ROOT).as_posix();inventory_sha=hashlib.sha256((OWN/'OPERATIONS_INVENTORY.json').read_bytes()).hexdigest()
if files[core_key]['sha256']!='888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8':raise RuntimeError('installed exact proposal drift')
if inventory_sha!='86f04bba661b5036a0b3a2b958779569ed4b92543748071f7177ed6d60e6df97':raise RuntimeError('current operations inventory drift')
manifest={'schema':'pr952-operations-engineering-seal-v3','utc':datetime.now(timezone.utc).isoformat(),'path_base':'repository_root','pr':952,'problem_id':'10400145','original_pr_head':'989a532ae1d50894190d010a0a02ba8c3d71ee05','stage':'EXACT_TESTED_PROPOSAL_INSTALLED_AUTHORIZED_REGRESSIONS_PASS','files':files,'explicit_public_allowlist':list(files),'installed_core_sha256':files[core_key]['sha256'],'operations_inventory_sha256':inventory_sha,'previous_family_manifest_sha256':'38929d4dc99b89b58aa13c35efcb6908ca3925252dd9b6addcaa2ed973922069','acceptance_authority':False,'scientific_or_fresh_full_review_credit':False,'actual_Git_or_service_calls':0,'actual_adapter_files_changed':1,'paper_package_FREEZE_runtime_state_changes':0,'private_or_scratch_fixture_bodies_included':False,'historical_failed_receipts_and_source_versions_preserved':True}
raw=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode();(OWN/'MANIFEST.json').write_bytes(raw);digest=hashlib.sha256(raw).hexdigest();(OWN/'MANIFEST.sha256').write_text(digest+'  MANIFEST.json\n');print(json.dumps({'manifest_sha256':digest,'files':len(files),'payload_bytes':sum(v['bytes'] for v in files.values()),'core_sha256':files[core_key]['sha256'],'operations_inventory_sha256':inventory_sha}))
