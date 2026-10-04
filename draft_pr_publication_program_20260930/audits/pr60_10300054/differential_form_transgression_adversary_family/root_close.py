#!/usr/bin/env python3
"""Unexecuted ROOT closer: creates only the literal-self-excluded SOURCE manifest."""
import datetime,json,os,pathlib,sys
sys.dont_write_bytecode=True
from root_readback import ROOT,prepared
assert sys.argv[1:]==['--operator','ROOT','--source-only']
assert not (ROOT/'MANIFEST.json').exists()
index,ready,entries=prepared(False)
body={'schema':'pr60-form-SOURCE-manifest/v1','role':'SOURCE','operator':'ROOT',
 'actual_pid':os.getpid(),'actual_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'argv':sys.argv,'files':entries,'directories':index['directories'],
 'literal_self_exclusion':'MANIFEST.json','mathematical_approval_inferred':False}
with (ROOT/'MANIFEST.json').open('xb') as stream:
 stream.write((json.dumps(body,indent=2)+'\n').encode());stream.flush();os.fsync(stream.fileno())
(ROOT/'MANIFEST.json').chmod(0o444)
print(json.dumps({'operation':'ROOT SOURCE closure','actual_pid':body['actual_pid'],'actual_utc':body['actual_utc'],'prepared_regular_bodies':len(entries),'literal_self_exclusion':'MANIFEST.json','mathematical_approval_inferred':False}))
