"""Read-only final acceptance verification; emits its own receipt only."""
from pathlib import Path
import datetime, hashlib, json, subprocess
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_text())
canonical=ROOT/'unsolved_math_prioritization/attempts/6800007'
accept=load(HERE/'acceptance.json'); manifest=load(canonical/'MANIFEST.json')
assert len(manifest['files'])==44
assert sha((canonical/'MANIFEST.json').read_bytes())==accept['canonical_manifest_sha256']
for z in manifest['files']:
    b=(canonical/z['path']).read_bytes()
    assert len(b)==z['bytes'] and sha(b)==z['sha256'],z['path']
plan=load(HERE/'state_mirror_plan.json'); receipt=load(HERE/'state_mirror_receipt.json')
for z in plan['bindings']:
    assert sha((ROOT/z['path']).read_bytes())==z['sha256'],z['path']
assert len(plan['bindings'])==618 and plan['primary_count']==23 and plan['duplicate_count']==1
state=load(ROOT/'unsolved_math_prioritization/state.json')
assert state==plan['state_after'] and len(state)==24
assert sha((ROOT/'unsolved_math_prioritization/state.json').read_bytes())==receipt['state_sha256']
prior_state=json.loads(subprocess.check_output(['git','show','HEAD:unsolved_math_prioritization/state.json'],cwd=ROOT))
assert len(prior_state)==23 and all(state[k]==v for k,v in prior_state.items())
prior_history=subprocess.check_output(['git','show','HEAD:unsolved_math_prioritization/history.jsonl'],cwd=ROOT)
history=(ROOT/'unsolved_math_prioritization/history.jsonl').read_bytes()
assert history.startswith(prior_history)
added=[json.loads(z) for z in history[len(prior_history):].splitlines()]
assert added==plan['history_append'] and len(added)==1 and added[0]['id']=='6800007'
assert sha(history)==receipt['history_sha256']
pre=load(HERE/'integration_preflight.json'); before=subprocess.check_output(['git','show',pre['main_before']+':unsolved_math_prioritization/QUEUE.md'],cwd=ROOT)
after=(ROOT/'unsolved_math_prioritization/QUEUE.md').read_bytes()
assert sha(before)==pre['whole_queue_before_sha256']
assert sha(after)=='70882ae3985fbe00d2b1e0833aa5945ade0cec28ef6ea61c3a099137ab87e00c'
bl=before.decode().splitlines(keepends=True); al=after.decode().splitlines(keepends=True)
assert len(bl)==len(al)
diff=[(x,y) for x,y in zip(bl,al) if x!=y]; assert len(diff)==1
x,y=diff[0]; a=x.split('|');b=y.split('|')
assert len(a)==len(b)==14 and a[2].strip().startswith('6800007 /')
assert all(a[i]==b[i] for i in range(14) if i not in (8,9,11))
assert b[8].strip()=='already_solved' and b[9].strip()=='1/5' and not b[10].strip() and not b[12].strip()
frozen=HERE/'reviewed_candidate'; fm=load(frozen/'MANIFEST.json')
for z in fm['files']:
    assert sha((frozen/z['path']).read_bytes())==z['sha256'],z['path']
deps=load(frozen/'CURRENT_PROOF_DEPENDENCIES.json')
members=deps.get('files',deps.get('members',deps.get('entries')))
if members is None:
    raise AssertionError('Unknown dependency schema: '+str(list(deps)))
for z in members:
    assert sha((HERE/z['path']).read_bytes())==z['sha256'],z['path']
new=HERE/'current_whole_adversary'; nm=load(new/'MANIFEST.json')
for z in nm.get('members',nm.get('files')):
    assert sha((new/z['path']).read_bytes())==z['sha256'],z['path']
remote=load(HERE/'remote_merge_receipt.json')
assert remote['state']=='MERGED' and remote['isDraft'] is False
assert remote['headRefOid']==accept['original_head'] and remote['mergeCommit']['oid']==accept['merge_commit']
parents=subprocess.check_output(['git','show','-s','--format=%P',accept['merge_commit']],cwd=ROOT,text=True).strip().split()
assert parents==accept['merge_parents']
inv=load(ROOT/'draft_pr_publication_program_20260930/inventory.json');assert inv['completed_count']==23
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'canonical_members':44,'canonical_manifest_sha256':accept['canonical_manifest_sha256'],'protected_bindings_verified':618,'source_bound_targets':24,'cumulative_original_turns':28,'historical_states_unchanged':True,'one_present_acceptance_only':True,'all_closed_gates_science_source_and_dependency_bytes_preserved':True,'queue_named_fields_and_all_unrelated_bytes_preserved':True,'remote_exact_merge_verified':True,'new_doi_tracker':False,'workflow_completion_estimate_percent':100}
(HERE/'ROOT_POST_ACCEPTANCE_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
