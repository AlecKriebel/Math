"""Retain the superseded preflight and bind fresh actual inputs after shared-main edits."""
from pathlib import Path
import datetime as dt, hashlib, json, stat, subprocess
A=Path(__file__).resolve().parent;R=A.parents[2]
def ref(p):
    b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    assert __debug__
    assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
    assert subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R)==b''
    dirty=set(subprocess.check_output(['git','diff','--name-only'],cwd=R).decode().splitlines())
    assert dirty=={'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/commands.tsv','paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/full_transcript.log'},'Wait for unrelated active audit to checkpoint its own changes'
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
    previous=json.loads((A/'integration_preflight.json').read_bytes());assert head!=previous['main_before']
    names=['integration_preflight.json','integration_queue_before.md','integration_inventory_before.json','accepted_pr_body.md','integration_state_before.json','integration_history_before.jsonl']
    d=A/'superseded_preflight_after_concurrent_PR387';d.mkdir()
    saved=[]
    for name in names:
        p=A/name;z=ref(p);p.rename(d/name);assert ref(d/name)['sha256']==z['sha256'];saved.append({'old':z,'preserved':ref(d/name)})
    fresh=json.loads((A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V2.json').read_bytes());now=dt.datetime.now(dt.timezone.utc).isoformat()
    fresh.update(created_utc=now,reason_date_utc=now[:10],current_head=head,reason='The genuine V2 sealer and preflight passed, then another authorized audit merged PR387 before ROOT began integration. ROOT retained the complete dated preflight and detected the changed main before any42Git/remote mutation. These thirteen actual current bodies and latest main are fresh authority for the repeated preflight; mathematical/closed V2 evidence remains unchanged.')
    rr=[]
    for z in fresh['files']:
        p=R/z['path'];rr.append({**ref(p),'worktree_mode':stat.S_IMODE(p.stat().st_mode)})
    fresh['files']=rr
    with (A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V3.json').open('x')as f:json.dump(fresh,f,indent=2);f.write('\n')
    record={'schema':'pr42-root-superseded-preflight-preservation/v1','utc':now,'old_main':previous['main_before'],'current_main':head,'superseded_genuine_preflight_utc':previous['utc'],'preserved_complete_preflight_records':saved,'fresh13':ref(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V3.json'),'canonical_or_native_or_remote_PR42_writes_before_detection':False,'old_capture_and_ROOT_approval_unchanged':True,'source_of_detection':'ROOT read-only full preimage check failed its initial currentHEAD equality before body/ready/merge; this ordinary tool invocation has no invented PID or source capture.'}
    with (d/'PRESERVATION.json').open('x')as f:json.dump(record,f,indent=2);f.write('\n')
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==head
    print(json.dumps({'status':'PASS_SUPERSEDED_PREFLIGHT_RETAINED_FRESH_CURRENT_AUTHORITY_CREATED','current_main':head,'fresh13':record['fresh13']}))
if __name__=='__main__':main()
