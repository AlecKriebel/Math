#!/usr/bin/env python3
"""Unexecuted ROOT closer; parent must inspect before running with -B."""
import datetime,json,os,sys
from packet import ROOT,SELF,validate
if sys.argv[1:]!=['--operator','ROOT']:raise SystemExit('ROOT operator required')
entries=validate(False)
body={'operator':'ROOT','pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'kind':'exact adversarial evidence closure; no native/remote or implicit mathematical approval',
      'literal_self_excluded':SELF,'domain':[e['path'] for e in entries],'entries':entries}
with (ROOT/SELF).open('x') as f:f.write(json.dumps(body,indent=2)+'\n')
(ROOT/SELF).chmod(0o444)
print(json.dumps({'operator':'ROOT','pid':os.getpid(),'self':SELF,'prepared_files':len(entries),'closed':True}))
