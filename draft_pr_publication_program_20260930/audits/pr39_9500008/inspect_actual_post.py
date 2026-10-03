"""Root inspection of actual post-acceptance objects; no prepared helper import."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import stat
import subprocess

R = Path('/Users/alec/Documents/Math')
A = R / 'draft_pr_publication_program_20260930/audits/pr39_9500008'
K = R / 'unsolved_math_prioritization/attempts/9500008'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def check(p, z):
    assert p.is_file() and not p.is_symlink()
    b = p.read_bytes()
    assert len(b) == z.get('bytes', z.get('size')) and sha(b) == z['sha256'], str(p)
    return b
def git(*argv): return subprocess.check_output(['git', *argv], cwd=R)

C = A / 'root_integration_post_actual_capture'
c = load(C / 'CAPTURE.json')
assert sha((C / 'CAPTURE.json').read_bytes()) == '024fb7d825cdc199a4e6af14ad9220cd79c120e6f954c4acb67d1fac71449f99'
assert c['status'] == 'PASS' and c['actual_execution'] is True and c['completed'] is True
assert c['pid'] == 69773 and c['exit_code'] == 0 and c['outer_errors'] == []
assert c['fresh_native13_before'] == c['fresh_native13_after']
assert c['fresh_native13_modes_before'] == c['fresh_native13_modes_after']
assert c['actual_changed_native_inputs'] == c['allowed_changed_native_inputs'] == []
assert c['head_before'] == c['head_after'] == git('rev-parse', 'HEAD').decode().strip()
assert c['head_after'] == '2e98e667acc47f2455533e09256eba921748128a'
for z in c['fresh_native13_after']:
    check(R / z['path'], z)
    assert stat.S_IMODE((R / z['path']).stat().st_mode) == c['fresh_native13_modes_after'][z['path']]
for field in ('stdout', 'stderr'): check(C / c[field]['path'], c[field])
assert not (C / c['stderr']['path']).read_bytes()
out = load(C / c['stdout']['path'])
assert out == dict(status='PASS', pr=39, canonical_members=2912, targets=30, turns=37, completed_primary_prs=29, new_proof_turns=0)
source = Path(c['argv'][2])
assert sha(source.read_bytes()) == c['source_sha256'] and stat.S_IMODE(source.stat().st_mode) == c['source_mode']
post = load(A / 'ROOT_POST_ACCEPTANCE_VERIFICATION.json')
assert post['status'] == 'PASS' and post['canonical_members'] == 2912 and post['complete_primary_prs'] == 29
assert post['current_targets'] == 30 and post['consumed_original_substantive_turns'] == 37
assert post['new_substantive_attempts'] == post['verification_attempts_added'] == 0
assert post['full_problem_solved'] is post['positive_novelty_claim'] is post['paper_or_new_doi_or_tracker'] is False
assert post['scientific_scope']['original_substantive_attempts'] == 2
assert post['current_read_only_mirror_validation']['shared_files_changed'] == 0
m = load(K / 'MANIFEST.json')
assert sha((K / 'MANIFEST.json').read_bytes()) == post['canonical_manifest_sha256']
names = []
for z in m['files']:
    check(K / z['path'], z)
    assert stat.S_IMODE((K / z['path']).stat().st_mode) == 0o644
    names.append(z['path'])
assert len(names) == len(set(names)) == 2912
assert {p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file()} == set(names) | {'MANIFEST.json'}
remote = load(A / 'remote_merge_receipt.json')
assert remote['number'] == 39 and remote['state'] == 'MERGED' and remote['isDraft'] is False
assert remote['headRefOid'] == '652b8115080e5e97b2274cb602de3faf8c551f20'
assert remote['mergeCommit']['oid'] == post['merge_commit'] == c['head_after']
assert git('show', '-s', '--format=%T', c['head_after']).decode().strip() == post['merge_tree']
assert git('show', '-s', '--format=%P', c['head_after']).decode().strip().split() == ['6f7cdb80ac4ed9d7e1179380de540a4eb5d9a534', remote['headRefOid']]
mirror = load(A / 'state_mirror_receipt.json')
for field, path in [('state_sha256', R / 'unsolved_math_prioritization/state.json'), ('history_sha256', R / 'unsolved_math_prioritization/history.jsonl')]:
    assert sha(path.read_bytes()) == mirror[field]
assert mirror['complete_primary_count'] == 29 and mirror['current_targets'] == 30 and mirror['history_events_added'] == 1
assert mirror['new_proof_turns_added_by_mirror'] == 0
for z in load(A / 'integration_prepush.json')['foreign_tracked_exclusions']: check(R / z['path'], z)
receipt = dict(schema='pr39-root-entire-actual-post-inspection/v1', status='PASS', utc=dt.datetime.now(dt.timezone.utc).isoformat(), actual_post_pid=c['pid'], capture_sha256=sha((C/'CAPTURE.json').read_bytes()), complete_post_object=post, entire_capture_object=c, whole_canonical_members=2912, complete_remote_object=remote, complete_mirror_receipt=mirror, all_native13_bytes_modes_unchanged=True, full_problem_solved=False, new_substantive_attempts=0, audit_turns=0, completed_primary_prs=29, total_primary_prs=180, completion_percent=29/180*100)
with (A / 'ROOT_ACTUAL_POST_INSPECTION.json').open('x') as f:
    json.dump(receipt, f, indent=2); f.write('\n')
print(json.dumps(dict(status='PASS', actual_post_pid=c['pid'], canonical_members=2912, completed_primary_prs=29, completion_percent=29/180*100)))
