#!/usr/bin/env python3
"""Construct compact source handoff; does not close it or execute ROOT tools."""
from pathlib import Path
from datetime import datetime,timezone
import json,os,stat
from packet_common import HERE,EXCLUDED,inventory,load,sha,validate_content
assert not any((HERE/n).exists() for n in EXCLUDED),'absent-only initial prepared index/ready/self'
checks=validate_content();readback=load(HERE/'SOURCE_READBACK.json')
assert readback['new_mathematical_verdict'] is None
for p in HERE.rglob('*'):
    if p.is_file():p.chmod(0o444)
    elif p.is_dir():p.chmod(0o755)
HERE.chmod(0o755)
files,dirs=inventory(False);assert len(files)+2<=220 and sum(r['bytes'] for r in files)<1400000
now=datetime.now(timezone.utc).isoformat()
index={'schema':'pr57-original-source-payload-index/v1','created_utc':now,'source_only':True,
 'original_head':'4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29','original_science_file_count':17,
 'files':files,'directories':dirs,'self_exclusions':sorted(EXCLUDED),
 'immutable_external_references':readback['immutable_external_references'],
 'dated_mutable_native_references_in_SOURCE_ACCOUNTING_not_closure_requirements':True}
(HERE/'INDEX.json').write_text(json.dumps(index,indent=2,sort_keys=True)+'\n');(HERE/'INDEX.json').chmod(0o444)
ready={'schema':'pr57-original-source-ready/v1','created_utc':now,
 'source_preparation_completion_percent':100,'new_mathematical_verdict':None,
 'new_discovery_credit_percent':0,'new_mathematical_independence':False,
 'native_acceptance_authority':False,'remote_action_authority':False,
 'ROOT_personal_read_attestation':False,'root_closure_required_after_preparer_exit':True,
 'closer_reader_executed_by_preparer':False,'self_manifest_present_at_preparer_handoff':False,
 'mathematical_reconciliation_and_native_actual_acceptance_remain_pending':True,
 'original_status_proposal':'claimed_solved','original_substantive_routes_used':1,
 'original_substantive_route_limit':5,'native_dated_status':'queued','native_dated_turns':'0/5',
 'generic_original_response_count':'not separately supplied','new_response_or_route_increment':False,
 'payload_file_count':len(files),'payload_total_bytes':sum(r['bytes'] for r in files),
 'complete_prepared_file_count':len(files)+2,'directory_count_including_root':len(dirs),
 'index_sha256':sha((HERE/'INDEX.json').read_bytes()),
 'common_source_sha256':sha((HERE/'packet_common.py').read_bytes()),
 'closer_source_sha256':sha((HERE/'ROOT_close_source.py').read_bytes()),
 'reader_source_sha256':sha((HERE/'ROOT_read_closed_source.py').read_bytes()),
 'preparer_readback_pid':readback['actual_verifier_pid'],'preparer_build_pid':os.getpid(),
 'build_process_completion_not_claimed_here':True,'build_no_separate_process_capture':True,
 'full_published_proof_or_fresh_visual_page_certified':False,
 'final_source_integrity_checks_before_index':checks}
(HERE/'READY.json').write_text(json.dumps(ready,indent=2,sort_keys=True)+'\n');(HERE/'READY.json').chmod(0o444)
from packet_common import validate_ready
allfiles,alldirs,lastchecks=validate_ready(False)
print(json.dumps({'status':'SOURCE_READY_ONLY_NOT_CLOSED','actual_builder_pid':os.getpid(),
 'prepared_files':len(allfiles),'total_bytes':sum(r['bytes'] for r in allfiles),
 'payload_files':len(files),'payload_bytes':ready['payload_total_bytes'],'source_integrity_checks':lastchecks,
 'index_sha256':ready['index_sha256'],'ready_sha256':sha((HERE/'READY.json').read_bytes()),
 'self_manifest_absent':not (HERE/'SELF_MANIFEST.json').exists(),'ROOT_closer_reader_unexecuted':True,
 'math_or_native_acceptance':False},indent=2,sort_keys=True))
