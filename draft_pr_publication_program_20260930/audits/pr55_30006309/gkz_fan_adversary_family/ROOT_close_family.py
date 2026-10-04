#!/usr/bin/python3
"""Unexecuted ROOT-only closure after personally reading this family."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,sys
sys.dont_write_bytecode=True
import packet_common as c
assert sys.argv[1:]==['--root-only-close-after-reading']
root=c.ROOT
assert not (root/'SELF_MANIFEST.json').exists()
index,ready=c.check_prepared()
# All paths are checked inside this family before changing any mode.
paths=c.all_files()
for p in paths:c.contained(p)
for p in paths:os.chmod(p,0o444)
manifest={'schema':'pr55-gkz-fan-actual-root-closure/v1','utc':datetime.now(timezone.utc).isoformat(),'actual_closer_pid':os.getpid(),'prepared_payload_file_count':len(index['files']),'files':[c.row(p) for p in paths],'directories':[{'path':str(p),'mode':format(p.stat().st_mode&0o7777,'04o')} for p in c.all_dirs()],'external_references':index['external_references'],'acceptance_authority':False,'ROOT_personal_read_not_inferred_from_integrity':True,'ROOT_closure_assertion':'Caller must personally read the proof, code, scope and actual full captures before using this ROOT-only flag.','historical_prepared_modes':'INDEX records modes at preparation. This closer freezes only checked owned files to 0444. Capture source modes remain dated actual historical 0644; body bytes are retained.','source_integrity_checks_before_closure':c.checks}
p=root/'SELF_MANIFEST.json';p.write_text(json.dumps(manifest,indent=2)+'\n');os.chmod(p,0o444)
c.check_closed()
print(json.dumps({'status':'PASS_ACTUAL_ROOT_GKZ_FAN_CLOSURE','actual_closer_pid':os.getpid(),'manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'file_count_including_manifest':len(paths)+1,'ROOT_personal_read_not_inferred':True,'acceptance_authority':False},sort_keys=True))
