#!/usr/bin/env python3
"""Pure offline preparation custody; no network, subprocess, imports of project code, or writes."""
from pathlib import Path,PurePosixPath
import hashlib,json,sys
R=Path(__file__).resolve().parent
EXCLUDED={'PREPARATION_MANIFEST.json','PREPARATION_SEAL.json','PREPARATION_CLOSURE.json'}
N=0
def need(ok,why):
 global N
 N+=1
 if not ok:raise RuntimeError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_bytes())
def bind(root,row):
 rel=PurePosixPath(row['path']);need(not rel.is_absolute()and '..'not in rel.parts and str(rel)==row['path'],'safe owned path')
 p=root/rel;need(p.is_file()and not p.is_symlink()and p.resolve().is_relative_to(root),'owned regular file')
 need(p.stat().st_size==row['bytes']and sha(p)==row['SHA256'],'whole owned bytes');return p
need(sys.argv[1:]in[[],['--preseal']],'bounded custody option')
preseal=sys.argv[1:]==['--preseal'];manifest=obj(R/'PREPARATION_MANIFEST.json');names=[]
for row in manifest['files']:bind(R,row);names.append(row['path'])
need(set(manifest['excluded_terminal_files'])==EXCLUDED,'terminal exclusion boundary')
actual={p.relative_to(R).as_posix()for p in R.rglob('*')if p.is_file()and not p.relative_to(R).as_posix().startswith('run-state/')}-EXCLUDED
need(len(names)==len(set(names))and set(names)==actual,'complete preparation namespace excluding only future run-state')
hook=R/'hooks/pre-push';need(hook.stat().st_mode&0o7777==0o555,'executable read-only0555 hook mode')
capture=obj(R/'PREFLIGHT_CAPTURE.json');need(capture['Git']['protected_record_count']==58531 and capture['Git']['index_record_count']==58533,'fresh exact58531 protection extent')
need(sha(R/'private/shared-index.before')==capture['Git']['index_SHA256']and sha(R/'private/protected-index.raw-records')==capture['Git']['protected_raw_records_SHA256'],'complete raw protection bytes')
template=obj(R/'ROOT_ADOPTION_TEMPLATE.json')
for file,h in template['code_files_SHA256'].items():need(sha(R/file)==h,'root template actual source pin')
need(template['root_stage_adopted']is False and template['production_install_authorized']is False and template['preparation_final_seal_SHA256']is None,'template does not grant root authority')
need(obj(R/'MISSING_ADOPTION_CONTROL.json')['status']=='REJECTED_BEFORE_ANY_INSTALLER_MUTATION','actual missing authority control')
need(obj(R/'GUARD_TEST_RESULTS.json')['status']=='PASS_PURE_STDIN_GUARD_CONTROLS','pure guard controls')
if not preseal:
 seal=obj(R/'PREPARATION_SEAL.json')
 for file,key in [('PREPARATION_MANIFEST.json','MANIFEST_SHA256'),('PREPARATION_CLOSURE.json','CLOSURE_SHA256'),('PREFLIGHT_CAPTURE.json','PREFLIGHT_CAPTURE_SHA256')]:need(sha(R/file)==seal[key],'final preparation seal')
 need(seal['owned_payload_count']==len(names),'final preparation extent')
print(json.dumps({'status':'PREPARATION_CUSTODY_PASS','mode':'preseal'if preseal else'sealed','checks':N,'owned_payload_count':len(names),'protected_index_records':58531,'network_requests':0,'subprocesses':0,'writes':0,'installer_or_push_executed':False},sort_keys=True))
