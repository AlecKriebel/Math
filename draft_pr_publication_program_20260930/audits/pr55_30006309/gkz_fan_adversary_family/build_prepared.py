#!/usr/bin/python3
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,sys
sys.dont_write_bytecode=True
import packet_common as c
root=c.ROOT
assert not any((root/n).exists() for n in ['INDEX.json','READY.json','SELF_MANIFEST.json'])
refs=c.check_science()
paths=c.all_files();dirs=c.all_dirs()
index={'schema':'pr55-gkz-fan-prepared-index/v1','created_at_utc':datetime.now(timezone.utc).isoformat(),'actual_builder_pid':os.getpid(),'files':[c.row(p) for p in paths],'directories':[{'path':str(p),'mode':format(p.stat().st_mode&0o7777,'04o')} for p in dirs],'external_references':refs,'prepared_only':True,'acceptance_authority':False}
(root/'INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
ready={'schema':'pr55-gkz-fan-source-readiness/v1','utc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_FOR_ROOT_PERSONAL_READING','index_sha256':hashlib.sha256((root/'INDEX.json').read_bytes()).hexdigest(),'payload_files':len(paths),'payload_bytes':sum(r['bytes'] for r in index['files']),'external_references':len(refs),'ROOT_closure_executed':False,'ROOT_personal_read_claimed':False,'self_manifest_absent':True,'acceptance_authority':False,'mathematical_verdict':'PASS_SCOPED_GKZ_COMBINATORIAL_COMPARISON','priority':'unestablished','source_control_assertions':78,'finite_math_require_evaluations':11955,'finite_math_child_pid':86845,'source_control_child_pid':90796}
(root/'READY.json').write_text(json.dumps(ready,indent=2)+'\n')
c.check_prepared();print(json.dumps(ready,sort_keys=True))
