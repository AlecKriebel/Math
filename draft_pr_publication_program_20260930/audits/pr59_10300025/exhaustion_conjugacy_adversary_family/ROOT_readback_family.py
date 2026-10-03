#!/usr/bin/python3
"""UNEXECUTED: separate ROOT readonly source-closure reader; no native acceptance."""
import datetime,json,os,stat,sys
from family_index import ROOT,validate
if sys.argv[1:] or not sys.dont_write_bytecode: raise SystemExit('use python3 -B without arguments')
ready,index=validate(); s=(ROOT/'SELF_MANIFEST.json').lstat()
if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or stat.S_IMODE(s.st_mode)!=0o444: raise SystemExit('source closure mode mismatch')
record=json.loads((ROOT/'SELF_MANIFEST.json').read_text())
if record['role']!='ROOT_SOURCE_CLOSURE_ONLY' or record['index_sha256']!=ready['index_sha256'] or record['payload_files']!=len(index['files']) or record['native_acceptance_or_merge'] or record['historical_intent_resolved']:
    raise SystemExit('source closure mismatch')
print(json.dumps({'role':'ROOT_READONLY_SOURCE_READBACK','pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'index_sha256':ready['index_sha256'],'payload_files':len(index['files']),'pass':True},sort_keys=True))
