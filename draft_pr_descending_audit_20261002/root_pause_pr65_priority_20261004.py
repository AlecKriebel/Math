#!/usr/bin/env python3
"""One-shot acknowledgement of the ascending PR65 priority checkpoint window."""
from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess, sys
R = Path('/Users/alec/Documents/Math')
P = R / 'draft_pr_descending_audit_20261002'
OUT = P / 'private_shared_pause_20261004T0633_pr65_priority'
EXPECTED = 'fa829e3839714b2487de8dadf9b34bdd2fb16e47'
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), mode=stat.S_IMODE(p.stat().st_mode))
assert not OUT.exists(), 'One-shot capture exists'
OUT.mkdir()
def run(tag, argv):
    pre = dict(utc=utc(), argv=argv, cwd=str(R), program=pin(Path(__file__)))
    (OUT/(tag+'.preexecution.json')).write_text(json.dumps(pre, indent=2)+'\n')
    r = subprocess.run(argv, cwd=R, capture_output=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
    (OUT/(tag+'.stdout')).write_bytes(r.stdout)
    (OUT/(tag+'.stderr')).write_bytes(r.stderr)
    (OUT/(tag+'.json')).write_text(json.dumps(dict(pre, completed_utc=utc(), exit_status=r.returncode,
        stdout=pin(OUT/(tag+'.stdout')), stderr=pin(OUT/(tag+'.stderr'))), indent=2)+'\n')
    assert r.returncode == 0, tag
    return r.stdout
branch = run('branch', ['git','branch','--show-current']).decode().strip()
head = run('head', ['git','rev-parse','HEAD']).decode().strip()
remote = run('remote', ['git','ls-remote','origin','refs/heads/main']).decode().split()[0]
staged = run('staged', ['git','diff','--cached','--raw','-z'])
index = run('index', ['git','ls-files','--stage','-z'])
assert branch == 'main' and head == remote == EXPECTED and not staged
previous = json.loads((P/'private_shared_pause_20261004T0449_intake/PAUSE_ACKNOWLEDGEMENT.json').read_text())
foreign = {rel:value for rel,value in previous['dirty_tracked_body_mode_pins_before_status_acknowledgement'].items()
           if not rel.startswith('draft_pr_descending_audit_20261002/')}
checks = {rel:pin(R/rel)==value for rel,value in foreign.items()}
assert len(checks)==6 and all(checks.values()), checks
status_path = P/'SHARED_GIT_WINDOW_STATUS.json'
status = json.loads(status_path.read_text())
status.update(utc=utc(), shared_git_writes_paused=True,
    reason='Incoming ascending request for exclusive PR65 priority audit checkpoint; fresh native main/remote equality and empty entire index verified.',
    paused_for='PR65 priority audit checkpoint 20261004',
    resume_on='Explicit ascending completion/release followed by independent exact-head native readback',
    local_main_at_pause=head, remote_main_at_pause=remote,
    all_staged_path_count=0, owned_staged_paths=[],
    entire_index_sha256_at_pause=hashlib.sha256(index).hexdigest(),
    native_pause_capture_directory=str(OUT), outbound_message_sent=False,
    descending_git_checkpoint_preparing=False,
    descending_mathematical_readonly_review_continues=True,
    dirty_tracked_bodies_modes_frozen_after_acknowledgement=True)
status_path.write_text(json.dumps(status,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n### '+utc()+' — PR65 priority checkpoint window acknowledged\n\n'
        'Main and remote are '+head+'; entire index empty. Shared Git/index writers paused and dirty tracked bodies/modes frozen after acknowledgement. '
        'PR344 mathematics100%, bounded priority100%, publication workflow50%. First fresh full-package review continues; '
        'an interpreter-specific expected stdout portability blocker has been found, with repair pending completion of that frozen review. '
        'No PR344 merge or Zenodo publication. No outbound chat message sent.\n')
dirty = run('dirty_after_acknowledgement', ['git','status','--porcelain=v1','-z','--untracked-files=no'])
pins = {}
for record in dirty.decode().split('\0'):
    if record:
        rel=record[3:]
        if (R/rel).is_file(): pins[rel]=pin(R/rel)
assert run('final_head', ['git','rev-parse','HEAD']).decode().strip()==head
assert run('final_index', ['git','ls-files','--stage','-z'])==index
receipt = dict(utc=utc(),status='SHARED_PR65_PRIORITY_AUDIT_CHECKPOINT_WINDOW_PAUSED',
    branch=branch,local_main=head,remote_main=remote,all_staged_path_count=0,
    entire_index_sha256=hashlib.sha256(index).hexdigest(),
    dirty_tracked_body_mode_pins_after_status_acknowledgement=pins,
    prior_foreign_body_mode_checks=checks, python=sys.version,python_executable=sys.executable,
    no_git_or_index_writes=True,program=pin(Path(__file__)))
(OUT/'PAUSE_ACKNOWLEDGEMENT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(dict(utc=receipt['utc'],status=receipt['status'],main=head,
    index_sha256=receipt['entire_index_sha256'],capture=str(OUT)),indent=2))
