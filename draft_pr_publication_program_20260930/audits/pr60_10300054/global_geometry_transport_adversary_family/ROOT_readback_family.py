#!/usr/bin/python3
"""UNEXECUTED: separate ROOT readonly SOURCE-closure readback."""
import datetime,json,os,stat,sys
from family_index import ROOT,validate
if sys.argv[1:] or not sys.dont_write_bytecode: raise SystemExit('use python3 -B without arguments')
ready,index=validate();p=ROOT/'SELF_MANIFEST.json';s=p.lstat()
if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or stat.S_IMODE(s.st_mode)!=0o444: raise SystemExit('manifest mode mismatch')
record=json.loads(p.read_text())
if record['role']!='ROOT_SOURCE_CLOSURE_ONLY' or record['index_sha256']!=ready['index_sha256'] or record['payload_files']!=len(index['files']) or record['original_problem_solved'] or record['native_acceptance_or_merge']: raise SystemExit('SOURCE closure mismatch')
print(json.dumps({'role':'ROOT_READONLY_SOURCE_READBACK','pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'index_sha256':ready['index_sha256'],'payload_files':len(index['files']),'pass':True},sort_keys=True))
