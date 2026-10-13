#!/usr/bin/env python3
"""ROOT-only separate read of closed SOURCE. No writes or acceptance."""
import json,os,sys
from datetime import datetime,timezone
from packet_common import HERE,SELF,load,pin,sha,validate_ready
assert sys.argv[1:]==['--root-only-read-after-close'], 'ROOT must separately execute/read the closed packet'
assert (HERE/SELF).is_file(), 'actual ROOT closure required first'
before=pin(HERE/SELF);closed=load(HERE/SELF)
files,dirs,checks=validate_ready(True)
assert closed['files']==files and closed['directories']==dirs
assert closed['complete_prepared_file_count']==len(files) and closed['source_integrity_checks']==checks
assert closed['index_sha256']==sha((HERE/'INDEX.json').read_bytes()) and closed['ready_sha256']==sha((HERE/'READY.json').read_bytes())
assert closed['source_only'] is True and closed['new_mathematical_verdict'] is None and closed['native_acceptance_authority'] is False
assert before==pin(HERE/SELF) and before['mode']==0o444
print(json.dumps({'status':'PASS_CLOSED_SOURCE_READ_ONLY','actual_reader_pid':os.getpid(),
 'utc':datetime.now(timezone.utc).isoformat(),'self_manifest':before,'complete_prepared_file_count':len(files),
 'source_integrity_checks':checks,'full_body_readback':True,'ROOT_personal_mathematical_review_not_inferred':True,
 'native_or_remote_acceptance':False},indent=2))
