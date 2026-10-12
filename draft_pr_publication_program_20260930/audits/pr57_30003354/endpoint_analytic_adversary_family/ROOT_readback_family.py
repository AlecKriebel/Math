"""UNEXECUTED at handoff; read-only, separate from the ROOT closer.

python3 -B ROOT_readback_family.py --operator ROOT
Writes no files and makes no mathematical or remote acceptance decision.
"""
import os
import sys
from packet import BASE,INDEX,READY,SELF,digest,json_read,prepared,utc

assert sys.argv[1:]==['--operator','ROOT']
index,ready=prepared(True)
manifest=json_read(SELF)
names=sorted([d['name'] for d in index['bodies']]+[INDEX,READY])
assert manifest['schema']=='pr57-endpoint-literal-self-excluding-manifest/v1'
assert manifest['operator']=='ROOT' and manifest['literal_self_exclusion']==SELF
assert manifest['directory']==index['directory']
assert manifest['entries']==[digest(BASE/n) for n in names]
assert manifest['READY_binding']==digest(BASE/READY)
assert manifest['prepared_regular_files']==len(names)
assert manifest['closed_regular_files']==len(names)+1
assert manifest['mathematical_acceptance'] is False
print({'ROOT_readback_pid':os.getpid(),'readback_utc':utc(),'all_bytes_modes_sizes_links_and_topology_match':True,'SELF_MANIFEST_sha256':digest(BASE/SELF)['sha256'],'closed_regular_files':len(names)+1,'mathematical_acceptance':False})
