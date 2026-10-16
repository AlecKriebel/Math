#!/usr/bin/env python3
"""One-shot independent readback of the released ascending PR65 final qualified-note audit checkpoint."""
from pathlib import Path
import datetime, hashlib, json, stat, subprocess
R=Path('/Users/alec/Documents/Math'); P=R/'draft_pr_descending_audit_20261002'
OUT=P/'private_shared_resume_20261004T0718_pr65_final_note'
EXPECTED='1135765a7fe02d6c2bbeca7bc1a3a4a5259650a9'
BASE='fd3ccfc6435ef2f76ad371c119756c8ce080dfed'
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
old=json.loads((P/'private_shared_pause_20261004T0708_pr65_final_note/PAUSE_ACKNOWLEDGEMENT.json').read_text())
checks={rel:pin(R/rel)==value for rel,value in old['dirty_tracked_body_mode_pins_after_status_acknowledgement'].items()}
assert checks and all(checks.values()),checks
assert run('parents',['git','show','-s','--format=%P',head]).decode().strip()==BASE
paths=run('owned_scope',['git','diff','--name-only',BASE,head]).decode().splitlines()
assert len(paths)==126 and all(p.startswith('draft_pr_publication_program_20260930/audits/pr65_2305051/') or
    p.startswith('draft_pr_publication_program_20260930/audits/pr45_9900007/root_pr65_') or
    p=='draft_pr_publication_program_20260930/CURRENT_PROGRESS.json' for p in paths)
assert not any('/preprint/' in p or '/publication/' in p or '/publication_package/' in p for p in paths)
queue='unsolved_math_prioritization/QUEUE.md'
assert run('queue_base',['git','show',BASE+':'+queue])==run('queue_after',['git','show',head+':'+queue])
rec=dict(utc=utc(),status='PR65_FINAL_QUALIFIED_NOTE_AUDIT_CHECKPOINT_RELEASE_VERIFIED',local_main=head,remote_main=remote,
    index_empty=True,whole_index_sha256=hashlib.sha256(index).hexdigest(),
    all_acknowledged_tracked_bodies_modes_preserved=checks,
    native_queue_bytes_unchanged=True,checkpoint_paths=paths,outbound_message_sent=False,
    acknowledged_path_count=len(checks), release_received=True, program=pin(Path(__file__)))
(OUT/'RESUME_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n')
f=P/'SHARED_GIT_WINDOW_STATUS.json';status=json.loads(f.read_text())
status.update(utc=utc(),shared_git_writes_paused=False,
    resumed_because='Explicit PR65 final qualified-note audit checkpoint release followed by native exact main/remote, empty index, every dynamically inventoried acknowledged tracked body/mode and unchanged native queue readback.',
    local_main_at_resume=head,remote_main_at_resume=remote,native_resume_capture_directory=str(OUT),
    all_staged_path_count=0,owned_staged_paths=[],dirty_tracked_bodies_modes_frozen_after_acknowledgement=False,
    ascending_pr65_final_qualified_note_checkpoint_completed=True,descending_git_checkpoint_preparing=False)
f.write_text(json.dumps(status,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as h:h.write('\n### '+utc()+' — PR65 final qualified-note checkpoint release verified\n\n'
    'Main and remote '+head+';126 owned ascending paths, unchanged native queue, empty entire index and all '+str(len(checks))+' acknowledged tracked bodies/modes preserved. '
    'Shared owned writes resumed. PR344 mathematics100%, bounded priority100%, workflow60%; second fresh package reviewer has frozen an exact generic dual-kernel formula counterexample. '
    'Main proof remains verified; supplementary helper repair and another fresh complete review are required. No merge/upload/tracker mutation.\n')
print(json.dumps(rec,indent=2))
