#!/usr/bin/env python3
"""Read-only mechanical input compatibility check, never a closure preflight.
No remote/API calls; immutable local Git objects and RO SQLite only. Root review
records are inspected solely for schema, pins and measured chronology.
"""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import argparse,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];A=P/'audits/pr967_2616'
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(x):return {'bytes':len(x),'sha256':sha(x)}
p=argparse.ArgumentParser();p.add_argument('--core-sha256',required=True);args=p.parse_args();raw=(P/'close_pr967.py').read_bytes()
if sha(raw)!=args.core_sha256:raise SystemExit('external source pin mismatch')
n={'__name__':'_mechanical_schema_only_','__file__':str(P/'close_pr967.py')};exec(compile(raw,str(P/'close_pr967.py'),'exec',dont_inherit=True,optimize=0),n)
normalraw=(A/'ROOT_FAMILY_AUTHENTICATIONS_NORMALIZED.json').read_bytes()
if sha(normalraw)!='8b6446b4acc4c536375c2dcc3429d9f87e1151846db425a20dedf268b75f0ff6':raise SystemExit('root normalized source pin changed')
doc=json.loads(normalraw);E={};items={}
def reference(path):
 raw=path.read_bytes();name=path.relative_to(n['ROOT']).as_posix();E[name]=pin(raw);return {'path':name,'sha256':sha(raw)}
normref=reference(A/'ROOT_FAMILY_AUTHENTICATIONS_NORMALIZED.json')
for name,record in doc['families'].items():
 manifest=n['ROOT']/record['manifest_path'];items[name]={'manifest':reference(manifest),'authentication':normref}
 for field in ['root_authentication_path','full_intake_path']:reference(n['ROOT']/record[field])
checked={name:n['family'](name,item,E) for name,item in items.items()}
original=n['originals']()
baseline=json.loads((A/'ROOT_NATIVE_AND_PRIOR_BASELINE.json').read_bytes());parent=baseline['immutable_main']
source=n['source_gate'](parent);native=n['native_pins'](parent)
print(json.dumps({'schema':'pr967-readonly-current-input-compatibility-v1','utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_MECHANICAL_SCHEMA_HASHES_ONLY','core_sha256':args.core_sha256,'families':{name:{k:v for k,v in record.items() if k!='sealed_files'} for name,record in checked.items()},'originals_authenticated':len(original),'original_bytes':sum(v['bytes'] for v in original.values()),'source_parent':parent,'source_identity':source,'native_file_pins':native,'actual_remote_or_API_calls':0,'Git_mutation_or_fetch':False,'acceptance_priority_or_clean_review_authority':False,'private_source_bodies_printed_or_retained':False},sort_keys=True))
