"""UNEXECUTED at handoff. ROOT must read this and packet.py before invocation.

python3 -B ROOT_close_family.py --operator ROOT
Creates only the literal self-excluding manifest in this family's exact domain.
Actual ROOT execution/time/PID are recorded then; no mathematical approval.
"""
import os
import sys
from packet import BASE,INDEX,READY,SELF,create_json,digest,prepared,topology,utc

assert sys.argv[1:]==['--operator','ROOT']
index,ready=prepared(False)
names=[d['name'] for d in index['bodies']]
names=sorted(names+[INDEX,READY])
manifest={'schema':'pr57-endpoint-literal-self-excluding-manifest/v1','operator':'ROOT','closer_pid':os.getpid(),'closed_utc':utc(),'literal_self_exclusion':SELF,'directory':index['directory'],'entries':[digest(BASE/n) for n in names],'READY_binding':digest(BASE/READY),'prepared_regular_files':len(names),'closed_regular_files':len(names)+1,'mathematical_acceptance':False,'separate_readonly_readback_required':True}
create_json(SELF,manifest)
topology(names+[SELF])
print({'ROOT_closer_pid':os.getpid(),'SELF_MANIFEST_sha256':digest(BASE/SELF)['sha256'],'closed_regular_files':len(names)+1,'mathematical_acceptance':False})
