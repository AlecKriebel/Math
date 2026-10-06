#!/usr/bin/env python3
"""ROOT-only SOURCE closer. Preparer must leave this source unexecuted."""
import json,os,sys
from datetime import datetime,timezone
from packet_common import HERE,SELF,pin,sha,validate_ready
assert sys.argv[1:]==['--root-only-close-after-reading'], 'ROOT must read exact sources and supply the explicit closure flag'
assert not (HERE/SELF).exists(), 'absent-only; no overwrite or reseal'
files,dirs,checks=validate_ready(False)
value={'schema':'pr57-original-source-self-manifest/v1','ROOT_execution_assertion':'ROOT closure after exact source read',
 'ROOT_personal_read_not_inferred_from_integrity_check':True,'actual_closer_pid':os.getpid(),
 'utc':datetime.now(timezone.utc).isoformat(),'source_only':True,'new_mathematical_verdict':None,
 'native_acceptance_authority':False,'Git_or_remote_action_authority':False,
 'files':files,'directories':dirs,'complete_prepared_file_count':len(files),'source_integrity_checks':checks,
 'index_sha256':sha((HERE/'INDEX.json').read_bytes()),'ready_sha256':sha((HERE/'READY.json').read_bytes())}
with (HERE/SELF).open('xb') as f:f.write((json.dumps(value,indent=2,sort_keys=True)+'\n').encode())
(HERE/SELF).chmod(0o444)
print(json.dumps({'status':'SOURCE_CLOSED_ONLY','actual_closer_pid':os.getpid(),'utc':value['utc'],
 'self_manifest':pin(HERE/SELF),'payload_file_count':len(files),'source_integrity_checks':checks,
 'ROOT_math_or_native_acceptance':False},indent=2))
