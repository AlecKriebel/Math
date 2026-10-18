"""Root finite selection resolution. New own metadata only; no native or five action."""
from pathlib import Path
import types,copy,json,hashlib,os,stat,datetime
D=Path(__file__).absolute().parent;A=D.parent;P=A.parents[1];C=P.parent
Q=A/'logical_packet_preparation_01';H=P/'ordered_intakes_after_PR214_20261017/source_adversary_01'
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def ref(p):return {'path':str(p),**pin(p.read_bytes())}
def output(p,obj):
 b=(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(b);f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
 return ref(p)
sp=Q/'prepare_positive_selection.py';sb=sp.read_bytes()
assert pin(sb)=={'bytes':16898,'sha256':'39784a08c478748ef8089455d4c35533687b9a2dde6904ba43c06c4a748d0e5a'}
s=types.ModuleType('Root_pinned_finite_source_reader');s.__file__=str(sp);exec(compile(sb,str(sp),'exec'),s.__dict__)
bp=Q/'conditional_packet_builder.py';bb=bp.read_bytes();assert pin(bb)=={'bytes':22089,'sha256':'9b673f11ffafccb70c6ce369abe5d8bb17f769f172883f777ec326273a3a1563'}
b=types.ModuleType('Root_pinned_pure_builder');b.__file__=str(bp);exec(compile(bb,str(bp),'exec'),b.__dict__)
raw,unused=s.read_file(Q/'PROPOSED_PUBLIC_SELECTION.json')
assert pin(raw)=={'bytes':345296,'sha256':'81b7cbc8a88c6d2d398b41cb2367f813bfa3e3db7718902e291836dc26cf7fba'}
original=json.loads(raw);plan=copy.deepcopy(original);rows={r['path']:r for r in plan['files']};assert len(rows)==391
for r in rows.values():
 body,mode=s.read_file(Path(r['origin']))
 assert pin(body)=={k:r[k] for k in ('bytes','sha256')} and s.native(body)==r['git_blob'] and mode==r['observed_source_mode']
added=[];mapping=[]
def add(origin,target,role,expected=None):
 body,mode=s.read_file(origin)
 if expected:assert pin(body)=={k:expected[k] for k in ('bytes','sha256')}
 assert b.public(target) and target not in rows
 row={'path':target,'origin':str(origin),**pin(body),'git_blob':s.native(body),'observed_source_mode':mode,'role':role,'selection_basis':'Root_explicit_resolved_finite_leaf'}
 rows[target]=row;added.append(target);return row
qm=json.loads((Q/'PUBLIC_MANIFEST.json').read_bytes())
assert pin((Q/'PUBLIC_MANIFEST.json').read_bytes())=={'bytes':2241,'sha256':'2d88827ba8960af7eac30e12819bc5e15aebf462f4b9ab8a5514d48bf38f49b4'}
for r in qm['files']:add(Q/r['path'],str((Q/r['path']).relative_to(C)),'Frozen inactive logical-selection preparation, historical source-only input',r)
for n in ['PUBLIC_MANIFEST.json','EXTERNAL_SEAL.json']:add(Q/n,str((Q/n).relative_to(C)),'Frozen logical-selection metadata')
hm=json.loads((H/'PUBLIC_MANIFEST.json').read_bytes())
assert pin((H/'PUBLIC_MANIFEST.json').read_bytes())=={'bytes':1631,'sha256':'f7eba3b0e5d35503d39efa1235a0ac0b7abf2fb19a5fa0bb3bbea45a9d52bfbd'}
for r in hm['files']+[{'path':'PUBLIC_MANIFEST.json',**pin((H/'PUBLIC_MANIFEST.json').read_bytes())},{'path':'EXTERNAL_SEAL.json',**pin((H/'EXTERNAL_SEAL.json').read_bytes())}]:
 target=b.CASE+'after214_consumer_archive_01/source_adversary_01/'+r['path']
 add(H/r['path'],target,'Fresh independent after214 consumer source review; no numeric authority',r)
 mapping.append({'origin':str(H/r['path']),'archived_target':target,**{k:r[k] for k in ('bytes','sha256')},'execution_base_unchanged':True})
add(A/'ROOT_AFTER214_STATUS_INTAKE_SOURCE_ACCEPTANCE_01.json',b.CASE+'ROOT_AFTER214_STATUS_INTAKE_SOURCE_ACCEPTANCE_01.json','Root accepted frozen helper source only; actual214 terminal still required')
mp=D/'ADDITIONAL_ARCHIVED_PATH_MAP.json'
output(mp,{'schema':'pr214-Root-additional-byte-exact-archive-relocations-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':mapping,'no_bytes_normalized':True,'no_execution_path_relocation_claimed':True})
add(mp,str(mp.relative_to(C)),'Root explicit fresh consumer review relocation table')
add(Path(__file__).absolute(),str(Path(__file__).absolute().relative_to(C)),'Root finite selection resolver source; metadata only')
resolved={'after214_consumer_final','logical_selection_preparation_final'}
plan['unresolved_slots']=[r for r in plan['unresolved_slots'] if r['id'] not in resolved]
assert len(plan['unresolved_slots'])==2 and all(r['blocks_construction'] is False for r in plan['unresolved_slots'])
plan['resolved_selected_closure_slots']=[{'id':i,'status':'RESOLVED_BY_ACTUAL_FROZEN_BYTES','numeric_authority':False} for i in sorted(resolved)]
plan['files']=[rows[k] for k in sorted(rows)];plan['total_files']=len(rows);plan['total_bytes']=sum(r['bytes'] for r in rows.values())
plan['UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();plan['Root_resolution_source']=ref(Path(__file__).absolute())
plan['Root_original_proposal']=ref(Q/'PROPOSED_PUBLIC_SELECTION.json')
plan['Root_resolution_scope']='Finite exact selection only. Fresh native/local capture and external exact packet audit/Root gate remain separate. No copies/staging/five/lock/native effect or214 completion or215 authority.'
plan['new_publication_or_tracker_append_performed']=False
carry=(P/'audits/pr212_30005310/next_checkpoint_carry_preparation_01/PROPOSED_CARRY_INVENTORY.json').read_bytes()
b.validate_plan(plan,b.validate_carry(carry))
rr=output(D/'ROOT_RESOLVED_PUBLIC_SELECTION_01.json',plan)
ar=output(D/'RESOLUTION_RECEIPT_01.json',{'schema':'pr214-Root-finite-selection-resolution-v1','PR':214,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection':rr,'original_known_files':391,'added_files':len(added),'total_files':len(rows),'total_bytes':plan['total_bytes'],'all_original_and_added_sources_rehashed':True,'selected_closure_slots_genuinely_resolved':sorted(resolved),'pending_external_slots':[r['id'] for r in plan['unresolved_slots']],'goal_complete':False,'case_completion_estimate_percent':85,'actual_completed_count':53,'actual_published_count':37,'no_copies_or_native_or_five_or_lock_actions':True})
print(json.dumps({'selection':rr,'resolution':ar,'files':len(rows),'bytes':plan['total_bytes']}))
