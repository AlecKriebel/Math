"""Bind the unchanged reviewed88-body packet and explicit closing appendices."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, stat, sys, subprocess
if sys.flags.optimize:
    raise RuntimeError('Optimized final-plan preparation forbidden.')
D = Path(__file__).resolve().parent
A = D.parent
P = A.parent.parent
R = P.parent
V = D / 'completion_packet_review_01'
W = D / 'completion_preparation'
sha = lambda b: hashlib.sha256(b).hexdigest()
def pin(p):
    p = Path(p)
    assert p.is_file() and not p.is_symlink()
    b = p.read_bytes()
    return dict(path=str(p.relative_to(R)), bytes=len(b), sha256=sha(b), mode=stat.S_IMODE(p.stat().st_mode))
planp = W / 'CONTENT_PLAN.json'
assert pin(planp)['sha256'] == 'aa3f453d3bdb86d40228dfcca5f9ba6815665e17db1f9ea4f50b1a495230bad2'
content = json.loads(planp.read_bytes())
clear = json.loads((D / 'ROOT_PR305_COMPLETION_PACKET_CLEARANCE.json').read_bytes())
assert clear['status'] == 'PASS_ROOT_PR305_CLOSED_COMPLETION_PACKET'
assert clear['mandatory_unresolved_findings'] == 0
targets = list(content['targets'])
assert len(targets) == 88
for e in targets:
    assert pin(R / e['input']['path']) == e['input']
    old = e['original_target']
    assert pin(R / e['target']) == old if old is not None else not (R / e['target']).exists()
extras = [planp, D / 'ROOT_PR305_COMPLETION_PACKET_CUSTODY.json',
    D / 'ROOT_PR305_COMPLETION_PACKET_CLEARANCE.json', D / 'root_close_pr305_completion_packet.py',
    Path(__file__).resolve(), D / 'root_checkpoint_pr305_publication_035.py',
    D / 'root_issue_pr305_checkpoint_lease.py', D / 'preprint_review02_candidate_frozen/MANIFEST.json']
# These are reviewer-authored public reports/metadata/programs. Native process
# tapes in the nested reviewer directory remain private and are not selected.
extras += sorted(p for p in V.iterdir() if p.is_file())
seen = {e['target'] for e in targets}
for p in extras:
    e = pin(p)
    assert e['path'] not in seen
    seen.add(e['path'])
    targets.append(dict(input=e, target=e['path'], original_target=e))
final = dict(schema='PR305-exact-completion-checkpoint-execution/v1',
    UTC=datetime.now(timezone.utc).isoformat(), actual_merge=content['actual_merge'],
    original_head=content['original_head'], unresolved_packet_findings=0,
    targets=targets, target_count=len(targets), reviewed_original_packet_unchanged=True,
    original_packet_targets=88, additional_closed_report_or_support_targets=len(extras),
    appended_manifest_is_exact_portable_archive_manifest=True,
    closed_packet_review_evidence={**clear['closed_review_evidence'],
        str(D / 'ROOT_PR305_COMPLETION_PACKET_CUSTODY.json'):clear['root_custody'],
        str(D / 'ROOT_PR305_COMPLETION_PACKET_CLEARANCE.json'):
            {k:v for k,v in pin(D / 'ROOT_PR305_COMPLETION_PACKET_CLEARANCE.json').items() if k != 'path'}},
    only_five_current_progress_mappings=True, no_original_merge_or_service_action=True,
    checkpoint_commit_and_push_not_yet_performed=True, persistent_goal_complete=False,
    public_scope='Unchanged independently reviewed88-body packet plus explicit authored closing reports, inventories, source programs, final plan and exact frozen portable-manifest copy. No private native process streams, foreign sheet values, fixture archive or third-party full text.')
# Operational pins use the established four-digit octal mode representation.
for e in final['closed_packet_review_evidence'].values():
    if isinstance(e['mode'], int):
        e['mode'] = format(e['mode'], '04o')
p = W / 'FINAL_EXECUTION_PLAN.json'
assert not p.exists()
probe = subprocess.run(['/usr/bin/git', 'check-ignore', '--no-index', '--stdin'],
    cwd=R, input=('\n'.join(sorted(seen | {str(p.relative_to(R))})) + '\n').encode(),
    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert probe.returncode == 1 and not probe.stdout and not probe.stderr, 'A literal selected target is ignored.'
with p.open('xb') as f:
    f.write((json.dumps(final, indent=2) + '\n').encode())
p.chmod(0o644)
print(json.dumps(dict(status='PASS_EXACT_FINAL_CHECKPOINT_PLAN_PREPARED',
    plan=pin(p), selected_targets=len(targets), actual_owned_paths=len(targets) + 1,
    five_current_progress_mappings=sum(e['input']['path'] != e['target'] for e in targets),
    original88_body_packet_unchanged=True, no_live_global_target_write=True), indent=2))
