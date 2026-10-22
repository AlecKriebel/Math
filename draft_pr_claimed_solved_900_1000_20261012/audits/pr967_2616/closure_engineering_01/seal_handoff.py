#!/usr/bin/env python3
"""Seal the bounded engineering handoff once; no live authority or mutation."""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import hashlib,json,stat
from pathlib import Path
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2]
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
if (OWN/'MANIFEST.json').exists():raise SystemExit('Already sealed; preserve existing handoff')
scope=json.loads((OWN/'SOURCE_AND_SCOPE_PINS.json').read_bytes())
for name,value in scope['live_helper_pins'].items():
 if pin((P.parent/name).read_bytes())!=value:raise SystemExit('Current helper drift before seal')
for mode in ['normal','O','OO']:
 launch=json.loads((OWN/('FINAL02_'+mode+'.launch.json')).read_bytes());result=json.loads((OWN/('FINAL02_'+mode+'.stdout.raw')).read_bytes())
 if launch['returncode']!=0 or result['event_count']!=200 or result['status']!='PASS_OFFLINE_CONTROLS_ONLY' or result['core_sha256']!=scope['live_helper_pins'][(P/'close_pr967.py').relative_to(P.parent).as_posix()]['sha256']:raise SystemExit('Final test/source mismatch')
 if (OWN/('FINAL02_'+mode+'.stderr.raw')).read_bytes():raise SystemExit('Final suite stderr is nonempty')
for stem in ['CURRENT_INPUTS_FINAL','ACTUAL_READONLY_STATUS01']:
 launch=json.loads((OWN/(stem+'.launch.json')).read_bytes())
 if launch['returncode']!=0 or launch['core_sha256']!=scope['live_helper_pins'][(P/'close_pr967.py').relative_to(P.parent).as_posix()]['sha256']:raise SystemExit('Final mechanical probe/source mismatch')
files={}
for path in sorted(OWN.rglob('*')):
 name=path.relative_to(OWN).as_posix()
 if path.is_dir():continue
 if 'private_tmp' in path.relative_to(OWN).parts:raise SystemExit('Private scratch must be empty at seal')
 if not stat.S_ISREG(path.lstat().st_mode) or path.is_symlink():raise SystemExit('Nonregular public artifact')
 files[name]=pin(path.read_bytes())
manifest={'schema':'pr967-proposed-closure-engineering-public-handoff-v1','utc':datetime.now(timezone.utc).isoformat(),'pr':967,'problem_id':'2616','original_pr_head':scope['original_pr_head'],'status':'PROPOSED_ENGINEERING_ONLY_ROOT_AUTHENTICATE_BEFORE_SUBSTANTIVE_INTAKE','explicit_public_allowlist':list(files),'files':files,'public_members':len(files),'public_bytes':sum(x['bytes'] for x in files.values()),'live_helper_pins':scope['live_helper_pins'],'proposed_operations_inventory_sha256':scope['proposed_operations_inventory']['sha256'],'private_source_or_corpus_or_fixture_bodies_included':False,'private_tmp_directory_excluded_empty':True,'adverse_history_preserved':True,'acceptance_priority_or_clean_entire_package_review_authority':False,'service_or_Git_mutations_executed':False,'local_finalizer_executed':False}
raw=(json.dumps(manifest,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode()
with (OWN/'MANIFEST.json').open('xb') as stream:stream.write(raw)
print(json.dumps({'manifest':str(OWN/'MANIFEST.json'),**pin(raw),'public_members':len(files),'public_bytes':manifest['public_bytes'],'current_live_helper_pins':scope['live_helper_pins'],'proposed_operations_inventory_sha256':scope['proposed_operations_inventory']['sha256']},sort_keys=True))
