#!/usr/bin/env python3
"""One-shot independent readback of the released ascending PR65 priority checkpoint."""
from pathlib import Path
import datetime, hashlib, json, stat, subprocess
R=Path('/Users/alec/Documents/Math'); P=R/'draft_pr_descending_audit_20261002'
OUT=P/'private_shared_resume_20261004T0635_pr65_priority_corrected'
EXPECTED='1420ead077d1fd3055e97a03f25486b8f4d606ba'
BASE='fa829e3839714b2487de8dadf9b34bdd2fb16e47'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
assert not OUT.exists();OUT.mkdir()
def run(tag,argv):
    pre=dict(utc=utc(),argv=argv,cwd=str(R),program=pin(Path(__file__)))
    (OUT/(tag+'.preexecution.json')).write_text(json.dumps(pre,indent=2)+'\n')
    r=subprocess.run(argv,cwd=R,capture_output=True)
    (OUT/(tag+'.stdout')).write_bytes(r.stdout);(OUT/(tag+'.stderr')).write_bytes(r.stderr)
    (OUT/(tag+'.json')).write_text(json.dumps(dict(pre,completed_utc=utc(),exit_status=r.returncode,
        stdout=pin(OUT/(tag+'.stdout')),stderr=pin(OUT/(tag+'.stderr'))),indent=2)+'\n')
    assert r.returncode==0,tag
    return r.stdout
assert run('branch',['git','branch','--show-current']).strip()==b'main'
head=run('head',['git','rev-parse','HEAD']).decode().strip()
remote=run('remote',['git','ls-remote','origin','refs/heads/main']).decode().split()[0]
assert head==remote==EXPECTED
assert not run('staged',['git','diff','--cached','--raw','-z'])
index=run('index',['git','ls-files','--stage','-z'])
old=json.loads((P/'private_shared_pause_20261004T0633_pr65_priority/PAUSE_ACKNOWLEDGEMENT.json').read_text())
checks={rel:pin(R/rel)==value for rel,value in old['dirty_tracked_body_mode_pins_after_status_acknowledgement'].items()}
assert len(checks)==10 and all(checks.values()),checks
assert run('parents',['git','show','-s','--format=%P',head]).decode().strip()==BASE
paths=run('owned_scope',['git','diff','--name-only',BASE,head]).decode().splitlines()
assert len(paths)==30 and all(p.startswith('draft_pr_publication_program_20260930/audits/pr65_') or
    p=='draft_pr_publication_program_20260930/CURRENT_PROGRESS.json' for p in paths)
assert not any('/preprint/' in p or '/publication/' in p or '/publication_package/' in p for p in paths)
queue='unsolved_math_prioritization/QUEUE.md'
assert run('queue_base',['git','show',BASE+':'+queue])==run('queue_after',['git','show',head+':'+queue])
rec=dict(utc=utc(),status='PR65_PRIORITY_AUDIT_CHECKPOINT_RELEASE_VERIFIED',local_main=head,remote_main=remote,
    index_empty=True,whole_index_sha256=hashlib.sha256(index).hexdigest(),
    all_ten_acknowledged_tracked_bodies_modes_preserved=checks,
    native_queue_bytes_unchanged=True,checkpoint_paths=paths,outbound_message_sent=False,
    corrects_previous_attempt='Prior native check confirmed every body/mode unchanged but rejected an incorrect expected count of eight: the post-acknowledgement inventory actually contains ten tracked paths, including two ascending-owned dirty paths. The first attempt stopped before any tracked write.',program=pin(Path(__file__)))
(OUT/'RESUME_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n')
f=P/'SHARED_GIT_WINDOW_STATUS.json';status=json.loads(f.read_text())
status.update(utc=utc(),shared_git_writes_paused=False,
    resumed_because='Explicit PR65 priority checkpoint release followed by native exact-head/main/remote, empty index, all ten acknowledged tracked bodies/modes and unchanged native queue readback.',
    local_main_at_resume=head,remote_main_at_resume=remote,native_resume_capture_directory=str(OUT),
    all_staged_path_count=0,owned_staged_paths=[],dirty_tracked_bodies_modes_frozen_after_acknowledgement=False,
    ascending_pr65_priority_checkpoint_completed=True,descending_git_checkpoint_preparing=False)
f.write_text(json.dumps(status,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as h:h.write('\n### '+utc()+' — PR65 priority checkpoint release verified\n\n'
    'Main and remote '+head+'; thirty owned ascending paths, unchanged native queue, empty entire index and all ten acknowledged tracked bodies/modes preserved. '
    'Shared owned writes resumed. PR344 mathematics100%, bounded priority100%, workflow50%; first fresh package reviewer remains active. '
    'Root independently reproduced the interpreter-output portability defect: system full check succeeds, bundled full check rejects, underlying intrinsic mathematical JSON agrees after interpreter provenance is removed. No merge/upload/tracker mutation.\n')
print(json.dumps(rec,indent=2))
