#!/usr/bin/python3
"""UNEXECUTED: ROOT only after full family review; absent-only source closure."""
import datetime,json,os,sys
from family_index import ROOT,validate
if sys.argv[1:]!=['--root-reviewed-family'] or not sys.dont_write_bytecode:
    raise SystemExit('ROOT must full-review first and use python3 -B with --root-reviewed-family')
start=datetime.datetime.now(datetime.timezone.utc).isoformat(); ready,index=validate()
record={'role':'ROOT_SOURCE_CLOSURE_ONLY','operator_pid':os.getpid(),'argv':sys.argv,'start_utc':start,
        'validation_end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'index_sha256':ready['index_sha256'],
        'payload_files':len(index['files']),'native_acceptance_or_merge':False,'historical_intent_resolved':False}
fd=os.open(ROOT/'SELF_MANIFEST.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
with os.fdopen(fd,'w') as out: os.fchmod(out.fileno(),0o444);json.dump(record,out,indent=2);out.write('\n');out.flush();os.fsync(out.fileno())
print(json.dumps(record,sort_keys=True))
