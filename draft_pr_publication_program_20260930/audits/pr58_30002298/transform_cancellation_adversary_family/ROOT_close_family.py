"""UNEXECUTED at handoff. ROOT must first read this and packet.py.
Invoke separately: python3 -B ROOT_close_family.py --operator ROOT
"""
import os,sys
from packet import B,H,I,R,M,d,verify,write_once,now

assert sys.argv[1:]==['--operator','ROOT']
index,ready=verify(False)
names=sorted([x['name'] for x in index['bodies']]+[I,R])
write_once(M,{'schema':'pr58-transform-literal-self-excluding-manifest/v1','head':H,'operator':'ROOT','actual_closer_pid':os.getpid(),'closed_utc':now(),'literal_self_exclusion':M,'directory':index['directory'],'entries':[d(B/n) for n in names],'prepared_files':len(names),'closed_files':len(names)+1,'mathematical_acceptance':False,'separate_readonly_readback_required':True})
verify(True)
print({'closer_pid':os.getpid(),'manifest_sha256':d(B/M)['sha256'],'closed_regular_files':len(names)+1,'mathematical_acceptance':False})
