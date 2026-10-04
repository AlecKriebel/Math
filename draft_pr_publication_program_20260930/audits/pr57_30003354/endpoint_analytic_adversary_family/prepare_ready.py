"""Prepare immutable family only; this is not ROOT closure or acceptance."""
import os
from packet import BASE,INDEX,READY,SELF,RESERVED,create_json,digest,directory,independent_evidence,prepared,utc

assert not any((BASE/n).exists() for n in RESERVED)
independent_evidence()
names=sorted(p.name for p in BASE.iterdir())
assert not set(names)&RESERVED
for name in names:
    digest(BASE/name)
    os.chmod(BASE/name,0o444)
os.chmod(BASE,0o755)
stamp=utc()
index={'schema':'pr57-endpoint-fixed-index/v1','original_head':'4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29','operator':'endpoint_analytic_adversary','preparer_pid':os.getpid(),'prepared_utc':stamp,'directory':directory(),'bodies':[digest(BASE/n) for n in names],'reserved_names':sorted(RESERVED),'index_cannot_hash_itself':True,'ROOT_or_math_acceptance':False}
create_json(INDEX,index)
ready={'schema':'pr57-endpoint-ready/v1','original_head':index['original_head'],'operator':'endpoint_analytic_adversary','preparer_pid':os.getpid(),'prepared_utc':stamp,'bindings':[digest(BASE/n) for n in [INDEX,'REPORT.md','VERDICT.json']],'SELF_manifest_created':False,'ROOT_helpers_executed':False,'ROOT_or_math_acceptance':False}
create_json(READY,ready)
prepared(False)
print({'preparer_pid':os.getpid(),'prepared_utc':stamp,'indexed_bodies':len(names),'prepared_regular_files':len(names)+2,'INDEX_sha256':digest(BASE/INDEX)['sha256'],'READY_sha256':digest(BASE/READY)['sha256'],'SELF_manifest_absent':not (BASE/SELF).exists()})
