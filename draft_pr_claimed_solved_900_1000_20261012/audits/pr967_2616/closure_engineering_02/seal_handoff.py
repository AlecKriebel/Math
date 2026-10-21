#!/usr/bin/env python3
"""Seal only the finite JSON float repair engineering packet, once."""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import hashlib,json,stat
from pathlib import Path
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2]
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
if (OWN/'MANIFEST.json').exists():raise SystemExit('Preserve existing sealed handoff')
scope=json.loads((OWN/'SOURCE_AND_SCOPE_PINS.json').read_bytes())
for name,record in scope['live_helper_pins'].items():
 if pin((P.parent/name).read_bytes())!=record:raise SystemExit('live helper drift')
old=OWN.parent/'closure_engineering_01';oldraw=(old/'MANIFEST.json').read_bytes()
if pin(oldraw)['sha256']!='3ac3ea788e5ff27faf8943c0f2f5302bd1be1bc2e85cf3aaece79fe58e98a3d1':raise SystemExit('old seal drift')
prior=json.loads(oldraw)
if len(prior['files'])!=119:raise SystemExit('old member count drift')
for name,record in prior['files'].items():
 if pin((old/name).read_bytes())!=record:raise SystemExit('old member drift: '+name)
files={}
for path in sorted(OWN.rglob('*')):
 if path.is_dir():continue
 name=path.relative_to(OWN).as_posix()
 if 'private_tmp' in path.relative_to(OWN).parts:raise SystemExit('private scratch not empty')
 if not stat.S_ISREG(path.lstat().st_mode) or path.is_symlink():raise SystemExit('nonregular member')
 files[name]=pin(path.read_bytes())
manifest={'schema':'pr967-finite-json-parser-repair-engineering-handoff-v1','utc':datetime.now(timezone.utc).isoformat(),'pr':967,'problem_id':'2616','original_pr_head':'b356dec5cb01e5f536b9cfeece56ad08844c03cb','status':'BOUNDED_ENGINEERING_REPAIR_ROOT_AUTHENTICATE_BEFORE_SUBSTANTIVE_INTAKE','explicit_public_allowlist':list(files),'files':files,'public_members':len(files),'public_bytes':sum(x['bytes'] for x in files.values()),'live_helper_pins':scope['live_helper_pins'],'proposed_operations_inventory_sha256':scope['proposed_operations_inventory']['sha256'],'engineering01_manifest_sha256':pin(oldraw)['sha256'],'all119_engineering01_members_unchanged':True,'private_source_corpus_or_fixture_bodies_included':False,'live_service_Git_native_mutations':0,'actual_finalizer_executed':False,'clean_entire_closure_package_review_or_execution_authority':False}
raw=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode()
with (OWN/'MANIFEST.json').open('xb') as stream:stream.write(raw)
print(json.dumps({'manifest':str(OWN/'MANIFEST.json'),**pin(raw),'public_members':len(files),'public_bytes':manifest['public_bytes'],'live_helper_pins':scope['live_helper_pins'],'proposed_operations_inventory_sha256':scope['proposed_operations_inventory']['sha256'],'all119_old01_unchanged':True},sort_keys=True))
