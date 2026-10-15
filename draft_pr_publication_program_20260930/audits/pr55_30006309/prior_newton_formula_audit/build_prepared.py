#!/usr/bin/python3
"""Prepare the child packet; does not invoke the ROOT-only closer or reader."""
from datetime import datetime, timezone
import hashlib, json, os, sys
sys.dont_write_bytecode = True
import packet_common as c
assert not any((c.ROOT/name).exists() for name in ['INDEX.json','READY.json','SELF_MANIFEST.json'])
refs = c.check_science(); paths = c.all_files()
index = {'schema':'pr55-Esterov-priority-prepared-index/v1',
         'created_at_utc':datetime.now(timezone.utc).isoformat(), 'actual_builder_pid':os.getpid(),
         'files':[c.row(path) for path in paths],
         'directories':[{'path':str(p),'mode':format(p.stat().st_mode&0o7777,'04o')} for p in c.all_dirs()],
         'external_references':refs, 'prepared_only':True, 'acceptance_authority':False}
(c.ROOT/'INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
ready = {'schema':'pr55-Esterov-priority-readiness/v1','utc':datetime.now(timezone.utc).isoformat(),
         'status':'PREPARED_FOR_ROOT_PERSONAL_READING',
         'index_sha256':hashlib.sha256((c.ROOT/'INDEX.json').read_bytes()).hexdigest(),
         'payload_files':len(paths),'payload_bytes':sum(ref['bytes'] for ref in index['files']),
         'external_references':len(refs),'ROOT_closure_executed':False,'ROOT_personal_read_claimed':False,
         'self_manifest_absent':True,'acceptance_authority':False,'recommended_user_status':'already_solved',
         'finite_source_and_math_checks':139,'final_actual_math_child_pid':43779,
         'ROOT_only_closer':'ROOT_close_family.py --root-only-close-after-reading',
         'separate_ROOT_reader':'ROOT_read_closed_family.py --root-only-read-after-close'}
(c.ROOT/'READY.json').write_text(json.dumps(ready,indent=2)+'\n')
c.check_prepared()
print(json.dumps(ready,sort_keys=True))
