"""Bind genuine present main/native inputs without altering their bodies."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess
A=Path(__file__).resolve().parent; R=A.parents[2]
def git(*args):
    return subprocess.check_output(['git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def main():
    assert __debug__ and git('branch','--show-current')==b'main\n'
    assert not git('diff','--cached','--name-only')
    foreign=sorted(set(git('diff','--name-only','-z').decode().split('\0'))-{''})
    assert foreign==['paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/commands.tsv','paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/full_transcript.log'],foreign
    head=git('rev-parse','HEAD').decode().strip()
    epoch=json.loads((A/'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes())
    stable=json.loads((A.parent/'pr46_30004438/ROOT_ACTUAL_POST_INSPECTION.json').read_bytes())
    prior={z['path']:z for z in stable['current13']}
    native4={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    assert len(epoch['files'])==len(prior)==13
    rows=[]
    for z in sorted(epoch['files'],key=lambda z:z['path']):
        p=R/z['path'];assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
        b=p.read_bytes(); mode=stat.S_IMODE(p.stat().st_mode); assert mode==0o644
        row=dict(path=z['path'],bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),worktree_mode=mode)
        if z['path'] in native4: assert git('show',head+':'+z['path'])==b
        else: assert row==prior[z['path']]
        rows.append(row)
    assert git('rev-parse','HEAD').decode().strip()==head
    assert not git('diff','--cached','--name-only')
    assert sorted(set(git('diff','--name-only','-z').decode().split('\0'))-{''})==foreign
    for z in rows:
        p=R/z['path']; b=p.read_bytes(); assert len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==z['worktree_mode']
    utc=dt.datetime.now(dt.timezone.utc).isoformat()
    obj=dict(schema='pr47-root-fresh-acceptance-input-preimages/v1',approved_by_root=True,created_utc=utc,reason_date_utc=utc[:10],reason='Present main and all thirteen complete native bodies and full modes were independently checked after genuine PR47 SOURCE reconciliation. Concurrent descending-audit commits and their QUEUE changes are preserved in the whole present QUEUE. Nine stable native bodies remain exact; current state/history retain the accepted PR46 baseline. Only the two named unrelated tracked paper logs are protected foreign inputs. Earlier native observations remain dated.',current_head=head,files=rows,protected_foreign_tracked_paths=foreign)
    with (A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json').open('x') as f: json.dump(obj,f,indent=2); f.write('\n')
    print(json.dumps(dict(status='PASS_FRESH_ACTUAL13_MAIN_AUTHORITY',head=head,files=13,foreign=foreign)))
if __name__=='__main__':main()
