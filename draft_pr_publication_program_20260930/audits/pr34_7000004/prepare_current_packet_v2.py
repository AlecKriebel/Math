"""Active corrected preparation; preserve the frozen v1 builder and packet."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
H=Path(__file__).resolve().parent;R=H.parents[2]
V=H/'reviewed_candidate';C=H/'reviewed_candidate_v2';F=H/'current_whole_adversary'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
assert not C.exists(), 'Never overwrite a frozen revision'
receipt=load(H/'ROOT_NEW1_ACTUAL_REPRODUCTION.json')
assert receipt['all_closed_artifacts_unchanged'] and receipt['nine_outer_replays_equal_except_actual_clock']
assert sha((V/'MANIFEST.json').read_bytes())=='5467c52b1cf076b76b409dd3cefedf7ddda40ed709182d828850276df49204f1'
assert sha((F/'MANIFEST.json').read_bytes())=='94fccf1191d886a8c0eaf4869d1af83324359940e8eae192eced8bdcc343c45f'
for base,entries in [(V,load(V/'MANIFEST.json')['files']),(H,load(V/'CURRENT_PROOF_DEPENDENCIES.json')['files']),(F,load(F/'MANIFEST.json')['files'])]:
    for z in entries:
        b=(base/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256'],z['path']
shutil.copytree(V,C)
(C/'MANIFEST.json').unlink()
old=load(V/'readiness.json');orig=load(C/'original_archive/readiness.json')
ready=load(C/'readiness.json')
ready['historical_original_attempt_metadata']={'scope':'Only original turn1, preserved byte-exact in original_archive/readiness.json; these are not current turn2/campaign restrictions or provenance.','readiness_sha256':sha((C/'original_archive/readiness.json').read_bytes()),'literature_checked_at':orig['literature_checked_at'],'budget':orig['budget']}
ready['literature_checked_at']=now
ready['literature_check_scope']='Actual current source-check checkpoint: complete primary operative source readings and fresh retrieval receipts preserved in dependency closure, plus root replay of the full source/SQL/pure-importer audit. Original September30 timestamp is archival only. This date is not an assertion of exhaustive worldwide novelty search or fresh retrieval of every listed version of record.'
turns=[json.loads(b) for b in (C/'turns.jsonl').read_bytes().splitlines()]
assert len(turns)==2
ready['budget']={'maximum_substantive_attempts':5,'used_substantive_attempts':2,'original_substantive_attempts':1,'new_substantive_attempts':1,'verification_attempts':0,'time_cap_utc':None,'time_scope':'Current persistent human-authorized campaign; no replacement deadline assigned. The expired original turn1 deadline is archival only.','model':turns[1]['model'],'reasoning_effort':turns[1]['reasoning_effort'],'compute':'Current universal algebraic/topological proof and exact prior specialization; root actual unchanged nine outer verifier/audit replays plus supplemental independent controls and actual source-code mutants. No sampled data replaces the universal linking proof.','provenance_scope':'Current parent-agent model and effort are not independently exposed in this runtime; original turn1 model/effort/compute are recorded only in historical_original_attempt_metadata.'}
ready['status']='current_v2_pending_DIFFERENT_NEW_complete_adversary'
ready['independent_review']='Original three distinct families and root reconstruction; first NEW whole review passed mathematics/priority but required historical metadata correction. Root actual replay reproduced that failure. This v2 has no transferred clean verdict and awaits a different NEW whole adversary.'
ready['remaining_gap']='Different NEW complete v2 adversarial gate and acceptance integration pending; no mathematical gap found in the literal counterexample or exact earlier-construction attribution. Later negative-curvature target remains outside scope.'
dump(C/'readiness.json',ready)
status=load(C/'current_status.json');status.update(utc=now,current_gate='pending_DIFFERENT_NEW_complete_v2_adversary',previous_whole_verdict='FIX_REQUIRED_ADMINISTRATIVE_PROVENANCE',metadata_repair='Original model/effort/deadline/compute and literature timestamp explicitly archived; current campaign and actual source checking separately scoped.',current_revision='reviewed_candidate_v2',workflow_completion_estimate_percent=75)
dump(C/'current_status.json',status)
context=load(C/'CURRENT_SOURCE_CONTEXT.json');context.update(utc=now,current_revision='reviewed_candidate_v2',historical_original_literature_checked_at=orig['literature_checked_at'],current_source_check_checkpoint_utc=now,current_source_check_scope=ready['literature_check_scope'],first_whole_verdict='Mathematics/prior PASS, mandatory administrative provenance repair; no clean gate transferred')
dump(C/'CURRENT_SOURCE_CONTEXT.json',context)
note='''

## Explicit v2 historical metadata qualification

The original September30 literature timestamp, expired original deadline, gpt-6-astra/xhigh and original local-compute description describe turn1 only. Their exact values remain in original_archive/readiness.json and historical_original_attempt_metadata in current readiness.json. Current parent-agent model/effort are not independently exposed; no replacement deadline is invented. The original turn1 and previously recorded turn2 JSONL bytes are unchanged. The actual current source-check checkpoint is separately scoped; it does not certify fresh retrieval of every bibliography entry or exhaustive worldwide priority.

The first NEW whole adversary passed the universal mathematics and exact earlier-construction attribution but required this metadata repair. Its complete report, failure verdict, actual code/mutants and root private replay remain immutable and bound. This explicit reviewed_candidate_v2 revision awaits a DIFFERENT NEW complete adversary. The original prepare_current_packet.py is an immutable historical v1 implementation, kept at its bound path; prepare_current_packet_v2.py is the active corrected implementation. No old clean gate is transferred.
'''
for name in ['README.md','pr_body.md','OBSTRUCTION.md','CURRENT_SOURCE_QUALIFICATION.md','CURRENT_AUDIT_SCOPE.md']:
    p=C/name;p.write_text(p.read_text()+note)
log=(V/'CURRENT_RESEARCH_LOG.md').read_text()+'\n'+now+' — workflow75%: first NEW whole mathematics/prior PASS, one metadata repair completed globally in explicit v2. Historical original fields archived; current source-check/model/deadline roles honest. Original turn1 and recorded turn2 unchanged, cumulative2/5; audit0. Root reproduced all nine outer runs and independent controls/mutations. Different NEW complete adversary still required.\n'
for name in ['CURRENT_RESEARCH_LOG.md','RESEARCH_LOG.md']:(C/name).write_text(log)
patch=load(C/'CURRENT_QUEUE_PATCH.json');assert sha((R/'unsolved_math_prioritization/QUEUE.md').read_bytes())==patch['whole_queue_preimage_sha256']
patch.update(utc=now,phase='v2 prospective only; no live writes before DIFFERENT NEW complete gate')
dump(C/'CURRENT_QUEUE_PATCH.json',patch)
admin={'readiness.json','current_status.json','CURRENT_SOURCE_CONTEXT.json','README.md','pr_body.md','OBSTRUCTION.md','CURRENT_SOURCE_QUALIFICATION.md','CURRENT_AUDIT_SCOPE.md','CURRENT_RESEARCH_LOG.md','RESEARCH_LOG.md','CURRENT_QUEUE_PATCH.json','CURRENT_PROOF_DEPENDENCIES.json','MANIFEST.json'}
unchanged=[]
for z in load(V/'MANIFEST.json')['files']:
    if z['path'] not in admin:
        assert (C/z['path']).read_bytes()==(V/z['path']).read_bytes(),z['path'];unchanged.append(z['path'])
assert (C/'turns.jsonl').read_bytes()==(V/'turns.jsonl').read_bytes()
assert ready['reviewed_artifact_sha256']==sha((C/'RESULT.md').read_bytes())=='28697e0bbc736e25f1f9a2935eadba4a72d734a1a492b90691085d9a8280c7cf'
private=H/'tmp/root_v2_controls';private.mkdir(parents=True,exist_ok=True);shutil.copyfile(C/'verify.py',private/'verify.py')
run=subprocess.run(['/usr/bin/python3',str(private/'verify.py')],capture_output=True,timeout=120)
assert run.returncode==0 and not run.stderr,run.stderr.decode()
assert (private/'exact_results.json').read_bytes()==(V/'exact_results.json').read_bytes()==run.stdout
repair={'utc':now,'first_whole_manifest_sha256':sha((F/'MANIFEST.json').read_bytes()),'first_whole_verdict':'FIX_REQUIRED_ADMINISTRATIVE_PROVENANCE','resolved_issue':'Historical original deadline/model/effort/compute/literature-check timestamp looked current in a two-attempt record.','repair':'All original fields explicitly archived, current campaign/model exposure/checkpoint/compute accurately scoped; preparation implementation is explicit new v2 and old builder remains immutable.','scientific_raw_source_original_archive_and_turn_ledger_unchanged':unchanged,'current_mathematical_artifact_sha256':sha((C/'RESULT.md').read_bytes()),'actual_v2_program_exit':run.returncode,'actual_v2_program_result_byte_exact':True,'root_new1_replay_receipt_sha256':sha((H/'ROOT_NEW1_ACTUAL_REPRODUCTION.json').read_bytes()),'new_substantive_attempts_added':0,'cumulative_attempts':'2/5','workflow_completion_estimate_percent':75,'different_new_complete_gate_required':True,'live_queue_state_history_writes':0}
dump(H/'ROOT_V2_ADMINISTRATIVE_REPAIR.json',repair)
deps={z['path']:dict(z) for z in load(V/'CURRENT_PROOF_DEPENDENCIES.json')['files']}
def add(p,role):
    path=str(p.relative_to(H));b=p.read_bytes();z={'path':path,'bytes':len(b),'sha256':sha(b),'role':role}
    if path in deps:assert deps[path]['sha256']==z['sha256'] and deps[path]['bytes']==z['bytes']
    else:deps[path]=z
for folder,role in [(V,'immutable_v1_packet'),(F,'first_NEW_whole_failure_closure')]:
    for z in load(folder/'MANIFEST.json')['files']:add(folder/z['path'],role)
    add(folder/'MANIFEST.json',role+'_manifest')
for p in [Path(__file__),H/'reproduce_root_new1.py',H/'ROOT_NEW1_ACTUAL_REPRODUCTION.json',H/'ROOT_V2_ADMINISTRATIVE_REPAIR.json']:add(p,'actual_v2_repair_or_root_new1_replay')
dump(C/'CURRENT_PROOF_DEPENDENCIES.json',{'utc':now,'base':'../','scope':'Entire unchanged v1 dependency closure, unchanged v1 packet, first NEW whole review failure closure, actual root reproduction and explicit v2 repair code/receipt. No verdict transferred; different NEW complete gate required.','files':list(deps.values())})
members=[{'path':str(p.relative_to(C)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(C.rglob('*')) if p.is_file()]
dump(C/'MANIFEST.json',{'utc':now,'scope':'Complete explicit v2 prospective credited counterexample packet, historical provenance repair; self excluding. Different NEW complete adversary pending.','files_count':len(members),'files':members})
for z in members:
    b=(C/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
for z in deps.values():
    b=(H/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
invpath=R/'draft_pr_publication_program_20260930/inventory.json';inv=load(invpath);item=next(z for z in inv['items'] if z['number']==34)
item.update(stage='v2_historical_metadata_repaired_frozen_pending_DIFFERENT_NEW_whole_gate',workflow_completion_estimate_percent=75,current_revision='reviewed_candidate_v2',reviewed_candidate_manifest_sha256=sha((C/'MANIFEST.json').read_bytes()),previous_whole_verdict='FIX_REQUIRED_ADMINISTRATIVE_PROVENANCE',original_attempts='1/5',new_substantive_attempts=1,cumulative_attempts='2/5')
inv['updated_at_utc']=now;dump(invpath,inv)
with (R/'draft_pr_publication_program_20260930/RESEARCH_LOG.md').open('a') as f:f.write('\n## '+now+' — PR34 explicit v2 metadata repair frozen\n\nWorkflow75%. Actual first NEW whole replays and mutants reproduced; mathematics and earlier-construction equivalence PASS, historical provenance issue fixed globally in explicit v2. Original expired deadline/model/effort/compute/literature timestamp archival only; current campaign and actual source-check checkpoint scoped accurately. All mathematical/raw-source/original16/turn1+turn2 bytes unchanged. Cumulative2/5; audit0. Old v1 packet/builder and failure closure immutable. Different NEW complete review required before acceptance; no paper/newDOI/tracker. Program23/180=12.7778%;18/20holds remain.\n')
print(json.dumps({'candidate_members':len(members),'dependencies':len(deps),'manifest_sha256':sha((C/'MANIFEST.json').read_bytes()),'unchanged_nonadministrative_members':len(unchanged),'budget':'2/5','live_queue_state_history_writes':0},indent=2))
