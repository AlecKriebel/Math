"""First-party SOURCE text inventory/READY writer; no proposed runtime loading."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,stat
P=Path(__file__).absolute().parent;A=P.parent;R=A.parents[2];OLD=A/'post_push_foreign_epoch_preparation_v5'
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b))
def put(p,b):
 with p.open('xb') as f:f.write(b)
def encode(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
runtime=['epoch_common.py','author_post_push_foreign_epoch_v6.py','execute_post_push_foreign_epoch_phase_v6.py','run_post_push_foreign_epoch_phase_v6.py','inspect_complete_actual_post_epoch_v6.py','integrate_reviewed_partial_epoch_v6.py','state_mirror_reconciliation_epoch_v6.py','close_SOURCE_family.py','verify_closed_SOURCE_family.py'];rows=[]
for name in runtime:
 oldname=name.replace('_v6','_v5');old=(OLD/oldname).read_bytes();new=(P/name).read_bytes();normalized=new.decode().replace('_v6','_v5').replace('_V6','_V5').replace('/v6','/v5').replace('V6','V5')
 if name=='author_post_push_foreign_epoch_v6.py':
  before="last<=c.clock(e['utc'])";after="c.clock(last)<=c.clock(e['utc'])"
  if normalized.count(before)!=1:raise ValueError('Exact one repaired predicate')
  normalized=normalized.replace(before,after)
 if name=='epoch_common.py':
  before="'M4_AND_SUPERSEDED_V4_BINDINGS.json','M5_AND_SUPERSEDED_V5_BINDINGS.json']";after="'M4_AND_SUPERSEDED_V4_BINDINGS.json']"
  if normalized.count(before)!=1:raise ValueError('Exact one new failure SOURCE dependency')
  normalized=normalized.replace(before,after)
 if normalized.encode()!=old:raise ValueError(('Only declared normalized changes',name))
 rows.append(dict(original=ref(OLD/oldname),derived=ref(P/name),normalized_body_equal=True,byte_identical=old==new))
put(P/'FINAL_NORMALIZED_SOURCE_CHANGE_MAP.json',encode(dict(schema='pr48-V6-final-normalized-complete-source-map/v1',proposed_or_production_imported_compiled_executed=False,changes=rows)))
failure=json.loads((P/'M5_AND_SUPERSEDED_V5_BINDINGS.json').read_bytes());operator=A/'capture_root_command.py';needop=ref(operator)
if needop['sha256']!='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec' or needop['bytes']!=2593 or stat.S_IMODE(operator.stat().st_mode)!=0o644:raise ValueError('Actual existing unchanged c1ae full0644')
if needop!={k:failure['existing_installed_c1ae'][k] for k in ['path','bytes','sha256']}:raise ValueError('Existing operator body remained exact through SOURCE preparation')
sources=['epoch_common.py','author_post_push_foreign_epoch_v6.py','execute_post_push_foreign_epoch_phase_v6.py','run_post_push_foreign_epoch_phase_v6.py','inspect_complete_actual_post_epoch_v6.py','integrate_reviewed_partial_epoch_v6.py','state_mirror_reconciliation_epoch_v6.py','CONTRACT.json','REPORT.md','NATIVE_SOURCE_DATE_SURVEY.json','private_mode_controls.py','PRIVATE_MODE_CONTROL_RESULTS.json','close_SOURCE_family.py','verify_closed_SOURCE_family.py','RESEARCH_LOG.md','REPAIR_PLAN.md','ACTUAL_REJECTED_V1_SOURCE_BINDINGS.json','M2_AND_SUPERSEDED_V2_BINDINGS.json','M3_AND_SUPERSEDED_V3_BINDINGS.json','M4_AND_SUPERSEDED_V4_BINDINGS.json','M5_AND_SUPERSEDED_V5_BINDINGS.json']
names=sorted([q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_file()]+['SOURCE_READY.json']);dirs={q.as_posix() for n in names for q in PurePosixPath(n).parents if q.as_posix()!='.'}
if len(names)!=len(set(names)) or any(q.is_symlink() or not(q.is_file() or q.is_dir()) for q in P.rglob('*')):raise ValueError('Exact source topology')
for q in P.rglob('*'):
 if stat.S_IMODE(q.stat().st_mode)!=(0o644 if q.is_file() else 0o755):raise ValueError('Every raw source64/directory75')
if stat.S_IMODE(P.stat().st_mode)!=0o755:raise ValueError('Own root75')
ready=dict(schema='pr48-post-push-epoch-SOURCE-readiness/v6',utc=dt.datetime.now(dt.timezone.utc).isoformat(),role='Prior SOURCE preparer; no independent/ROOT authority',source_only=True,proposed_code_executed=False,production_imported_compiled_executed=False,actual_epoch_or_acceptance_approved=False,source_correction_preparation_percent=100,independent_corrective_review_percent=0,actual_recovery_percent=0,mathematical_discovery_percent=0,source_files=[ref(P/n) for n in sources],closure_payload_files=names,closure_payload_count=len(names),closure_directory_count=len(dirs),closure_manifest_schema='pr48-post-push-epoch-source-closure/v6',closure_manifest_keyset=['schema','source_only','self_excluded','files_count','files','file_modes','directory_modes'],mode_contract='pr48-source-operator-dependency-full07777/v6',original_closed53_unchanged=True,original22_ROOT_contract_unchanged=True,original_first_three_CAPs_unchanged=True,original_science17_pins_unchanged=True,actual_live_ROOT_operator_copied_by_preparer=False,existing_installed_ROOT_operator_reused=True,actual_live_ROOT_operator_path=needop['path'],actual_live_ROOT_operator_full_mode=0o644,actual_live_ROOT_operator_parent_full_mode=0o755,actual_ROOT_outer_parent_required=A.relative_to(R).as_posix(),genuine_ROOT_outer_directories_full_mode=0o700,SOURCE_directories_full_mode=0o755,actual_M5_failure=ref(P/'M5_AND_SUPERSEDED_V5_BINDINGS.json'),final_normalized_change_map=ref(P/'FINAL_NORMALIZED_SOURCE_CHANGE_MAP.json'),actual_private_controls=ref(P/'PRIVATE_MODE_CONTROL_RESULTS.json'),superseded_closed_V5_manifest=ref(OLD/'SOURCE_MANIFEST.json'),superseded_closed_V5_READY=ref(OLD/'SOURCE_READY.json'),remaining_gap='ROOT complete reading/SOURCE closure/separate readback, independent corrective continuity review, then genuine distinct V6 epochs/final3/whole22 ROOT post. Existing c1ae is reused unchanged; no actual future approval or recovered phase is asserted. PR49 paused consumer requires explicit V6 wiring.',future=dict(ROOT_SOURCE_manifest=None,ROOT_SOURCE_closure_capture=None,ROOT_SOURCE_separate_readback=None,independent_corrective_SOURCE_verdict=None,actual_ROOT_epochs=None,actual_final_three_captures=None,actual_ROOT_complete_post=None,approved=False))
put(P/'SOURCE_READY.json',encode(ready));print(json.dumps(dict(status='READY_SOURCE_V6_ONLY',payload_count=len(names),relative_dirs=len(dirs),bytes=sum((P/n).stat().st_size for n in names),READY=ref(P/'SOURCE_READY.json'),report=ref(P/'REPORT.md'),common=ref(P/'epoch_common.py'),author=ref(P/'author_post_push_foreign_epoch_v6.py'),closer=ref(P/'close_SOURCE_family.py'),reader=ref(P/'verify_closed_SOURCE_family.py'))))
