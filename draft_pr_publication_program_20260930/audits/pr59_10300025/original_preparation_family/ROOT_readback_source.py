#!/usr/bin/env python3
"""Separate unexecuted read-only ROOT source readback."""
import datetime, json, os, sys
from packet import ROOT, SELF, validate
if sys.argv[1:]!=['--operator','ROOT']: raise SystemExit('ROOT operator required')
entries=validate(True); m=json.loads((ROOT/SELF).read_bytes())
assert m['operator']=='ROOT' and type(m['pid']) is int and m['pid']>0
assert m['literal_self_excluded']==SELF and m['domain']==[e['path'] for e in entries] and m['entries']==entries
print(json.dumps({'operator':'ROOT','readback_pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 'closed_pid':m['pid'],'closed_utc':m['utc'],'files':len(entries)+1,'PASS':'exact SOURCE domain, modes, bytes'}))
