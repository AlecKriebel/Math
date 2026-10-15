"""UNEXECUTED at handoff. Read-only and separate from the ROOT closer.
Invoke separately: python3 -B ROOT_readback_family.py --operator ROOT
"""
import os,sys
from packet import B,H,I,R,M,d,read,verify,now

assert sys.argv[1:]==['--operator','ROOT']
index,ready=verify(True); manifest=read(M)
names=sorted([x['name'] for x in index['bodies']]+[I,R])
assert manifest['head']==H and manifest['operator']=='ROOT'
assert manifest['literal_self_exclusion']==M
assert manifest['directory']==index['directory']
assert manifest['entries']==[d(B/n) for n in names]
assert manifest['prepared_files']==len(names) and manifest['closed_files']==len(names)+1
assert manifest['mathematical_acceptance'] is False
print({'readback_pid':os.getpid(),'utc':now(),'all_bytes_sizes_full_modes_links_and_domain_verified':True,'manifest_sha256':d(B/M)['sha256'],'closed_regular_files':len(names)+1,'mathematical_acceptance':False})
