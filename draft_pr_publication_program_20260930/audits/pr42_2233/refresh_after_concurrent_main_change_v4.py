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
    d=A/'superseded_preflight_after_concurrent_PR386';d.mkdir()
    saved=[]
    for name in names:
        p=A/name;z=ref(p);p.rename(d/name);assert ref(d/name)['sha256']==z['sha256'];saved.append({'old':z,'preserved':ref(d/name)})
    fresh=json.loads((A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V2.json').read_bytes());now=dt.datetime.now(dt.timezone.utc).isoformat()
    fresh.update(created_utc=now,reason_date_utc=now[:10],current_head=head,reason='The genuine V3 preflight passed at 2ee62f2, then authorized concurrent PR386 advanced main. ROOT detected this but erroneously continued to the original merge; the actual aborted merge and two failed rollback wrappers are preserved. Successful rollback verified whole current QUEUE and unrelated working bodies unchanged, clean index, original canonical absence and current main. PR42 was restored to draft. These thirteen actual current bodies and latest main now govern a new preflight; mathematical and closed V2 evidence remain unchanged.')
    rr=[]
    for z in fresh['files']:
        p=R/z['path'];rr.append({**ref(p),'worktree_mode':stat.S_IMODE(p.stat().st_mode)})
    fresh['files']=rr
    with (A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V4.json').open('x')as f:json.dump(fresh,f,indent=2);f.write('\n')
    record={'schema':'pr42-root-superseded-preflight-preservation/v1','utc':now,'old_main':previous['main_before'],'current_main':head,'superseded_genuine_preflight_utc':previous['utc'],'preserved_complete_preflight_records':saved,'fresh13':ref(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V4.json'),'previous_rejected_merge_fully_rolled_back':True,'previous_remote_body_ready_then_restored_draft':True,'old_capture_and_ROOT_approval_unchanged':True,'source_of_detection':'ROOT currentHEAD check failed after metadata readiness. The attempted merge was preserved then genuinely aborted and verified; detailed real captures and full rollback receipt remain in adjacent audit folders.'}
    with (d/'PRESERVATION.json').open('x')as f:json.dump(record,f,indent=2);f.write('\n')
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==head
    print(json.dumps({'status':'PASS_SUPERSEDED_PREFLIGHT_RETAINED_FRESH_CURRENT_AUTHORITY_CREATED','current_main':head,'fresh13':record['fresh13']}))
if __name__=='__main__':main()
