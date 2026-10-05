"""Issue one bounded bookkeeping checkpoint scope after closed packet review.

This program cannot repeat the original merge, publication or tracker append.
It only opens the cooperative window for the exact final completion plan.
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys, os, json, uuid, fcntl, stat
if sys.flags.optimize:
    raise RuntimeError('Optimized checkpoint lease issuance forbidden.')
D = Path(__file__).resolve().parent
sys.path.insert(0, str(D / 'publication_preparation'))
import submission_gate as g
BASE = 'b3eaf7561c83b37881eec11f5972396dbad9575d'
PLAN = D / 'completion_preparation/FINAL_EXECUTION_PLAN.json'
OPERATOR = D / 'root_checkpoint_pr305_publication_035.py'
CLEAR = D / 'ROOT_PR305_COMPLETION_PACKET_CLEARANCE.json'
fd = os.open(g.P / 'audits/pr311_30005303/root_integration_private/SHARED_WRITE_LEASE.lock', os.O_RDWR | os.O_NOFOLLOW)
lock = os.fdopen(fd, 'r+b')
fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
g.current_clearance()
g.operational_clearance()
clear = g.load(CLEAR)
assert clear['status'] == 'PASS_ROOT_PR305_CLOSED_COMPLETION_PACKET'
assert clear['mandatory_unresolved_findings'] == 0
assert clear['content_plan'] == g.pin(D / 'completion_preparation/CONTENT_PLAN.json')
assert clear['checkpoint_operator'] == g.pin(OPERATOR)
for absolute, e in clear['closed_review_evidence'].items():
    assert g.pin(absolute) == e
plan = g.load(PLAN)
assert plan['actual_merge'] == BASE and plan['unresolved_packet_findings'] == 0
assert plan['closed_packet_review_evidence'][str(CLEAR)] == g.pin(CLEAR)
assert not (D / 'checkpoint035_actual_private').exists()
assert not (g.P / 'checkpoint_305_publication_completion_035_receipt.json').exists()
for e in plan['targets']:
    p = g.R / e['input']['path']
    pin = g.pin(p)
    assert pin['bytes'] == e['input']['bytes'] and pin['sha256'] == e['input']['sha256']
    assert int(pin['mode'], 8) == e['input']['mode']
    assert not Path(e['target']).is_absolute() and '..' not in Path(e['target']).parts
    if e['input']['path'] != e['target']:
        old = e['original_target']
        target = g.R / e['target']
        assert not target.is_symlink()
        if old is None:
            assert not target.exists()
        else:
            targetpin = g.pin(target)
            assert targetpin['bytes'] == old['bytes'] and targetpin['sha256'] == old['sha256']
            assert int(targetpin['mode'], 8) == old['mode']
assert g.load(D / 'ROOT_PR305_POST_MERGE_CUSTODY.json')['status'] == 'PASS_ROOT_PR305_ACTUAL_MERGE_FULL_NATIVE_CUSTODY'
assert g.load(D / 'ROOT_PR305_ACTUAL_MERGE_VERIFICATION.json')['actual_merge'] == BASE
status = g.P / 'SHARED_GIT_WINDOW_STATUS.json'
before = status.read_bytes()
old = json.loads(before)
assert g.pin(status)['sha256'] == '3d4a91cd0ea310e653fcb232482377a3348689808b72d7a8b17c803e20ed690a'
assert old['shared_git_writes_paused'] and not old['descending_writer_window_released']
assert old['descending_305_complete'] and old['descending_305_actual_merge'] == BASE
assert old['descending_305_final_global_checkpoint_pending']
leasep = D / 'ROOT_FINAL_WRITE_LEASE.json'
oldlease = leasep.read_bytes()
assert oldlease == (D / 'ROOT_PR305_NATIVE_MERGE_LEASE_CLOSED_EPOCH.json').read_bytes()
assert datetime.fromisoformat(json.loads(oldlease)['expires_utc']) < datetime.now(timezone.utc)
assert g.git('branch', '--show-current') == b'main\n'
assert g.git('rev-parse', 'HEAD').decode().strip() == BASE
fetch, push = g.safe_endpoints()
assert g.git('ls-remote', fetch, 'refs/heads/main').split()[0].decode() == BASE
assert not g.git('diff', '--cached', '--raw', '-z') and not (g.R / '.git/MERGE_HEAD').exists()
stamp = datetime.now(timezone.utc)
lease = dict(status='ACTIVE_PR305_FINAL_WRITE_LEASE', owner_thread=g.THREAD, pr=305,
    token=str(uuid.uuid4()), issued_utc=stamp.isoformat(), not_before_utc=stamp.isoformat(),
    expires_utc=(stamp + timedelta(seconds=600)).isoformat(), publication_authorized=True,
    git_authorized=True, checkpoint_authorized=True, main=BASE, fetch_endpoint=fetch,
    push_endpoint=push, checkpoint_plan=g.pin(PLAN), checkpoint_operator=g.pin(OPERATOR),
    completion_packet_clearance=g.pin(CLEAR), exact_owned_path_count=len(plan['targets']) + 1,
    scope='One exact scoped bookkeeping checkpoint of the closed completion packet and declared supporting reports/programs. Five reviewed current progress mappings only; preserve all other index entries/flags and dirty bodies/modes/diff. One descendant commit and explicit expected-old push. No original-head merge, GitHub metadata, Zenodo, or tracker action.',
    original_native_merge_not_authorized=True, service_mutations_not_authorized=True)
archive = D / 'ROOT_PR305_PRECHECKPOINT_PAUSED_CONTROL_CLOSED_EPOCH.json'
with archive.open('xb') as f:
    f.write(before); f.flush(); os.fsync(f.fileno())
new = dict(old)
new.update(utc=stamp.isoformat(), shared_git_writes_paused=False,
    reason='Original PR305 merge/publication/tracker fully authenticated. Independent closed completion-packet review has zero required changes; ROOT authorizes only its exact scoped bookkeeping checkpoint for600 seconds.',
    resume_on='ROOT exact checkpoint operator and final plan only; every writer must recheck the complete control and retain75 seconds. Other workers abstain shared Git/index/held writes until explicit release.',
    descending_shared_write_lease=lease, descending_writer_window_released=False,
    descending_305_merge_complete=True, descending_305_native_Git_not_authorized=True,
    descending_305_checkpoint_Git_authorized=True, descending_305_completion_packet_review_closed=True,
    descending_305_completion_packet_required_findings=0,
    local_main_at_resume=BASE, remote_main_at_resume=BASE)
pending = [(D / 'PR305_CHECKPOINT_LEASE_PENDING.json', lease, leasep),
           (D / 'PR305_CHECKPOINT_STATUS_PENDING.json', new, status)]
for p, value, target in pending:
    with p.open('xb') as f:
        f.write((json.dumps(value, indent=2) + '\n').encode()); f.flush(); os.fsync(f.fileno())
assert status.read_bytes() == before and leasep.read_bytes() == oldlease
for p, value, target in pending:
    os.replace(p, target)
assert g.window() == lease
receipt = dict(status='PASS_ROOT_PR305_EXACT_CHECKPOINT_LEASE_ISSUED', UTC=g.utc(),
    lease=g.pin(leasep), control=g.pin(status), token=lease['token'], expires_utc=lease['expires_utc'],
    base=BASE, final_plan=g.pin(PLAN), operator=g.pin(OPERATOR),
    exact_owned_path_count=len(plan['targets']) + 1, no_original_merge_or_service_mutation_authorized=True)
(D / 'ROOT_PR305_CHECKPOINT_LEASE_ISSUANCE.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
