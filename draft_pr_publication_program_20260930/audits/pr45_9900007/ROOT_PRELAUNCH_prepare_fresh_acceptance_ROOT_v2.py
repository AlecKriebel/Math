"""ROOT independently binds the present main and thirteen native bodies/modes."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess
A=Path(__file__).resolve().parent; R=A.parents[2]
PROTECTED=['draft_pr_descending_audit_20261002/RESEARCH_LOG.md',
           'draft_pr_descending_audit_20261002/audits/pr379_30000590/README.md',
           'draft_pr_descending_audit_20261002/inventory.json',
           'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/commands.tsv',
           'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/full_transcript.log']
def git(*tail): return subprocess.check_output(['git',*tail],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def main():
    assert __debug__ and git('branch','--show-current')==b'main\n'
    assert not git('diff','--cached','--name-only')
    dirty=set(git('diff','--name-only','-z').decode().split('\0'))-{''}
    assert dirty<=set(PROTECTED),dirty
    head=git('rev-parse','HEAD').decode().strip()
    epoch=json.loads((A/'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes());rows=[]
    native4={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md',
             'unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    assert len(epoch['files'])==13
    for z in sorted(epoch['files'],key=lambda z:z['path']):
        p=R/z['path'];assert p.is_file()and not p.is_symlink()and all(not q.is_symlink()for q in p.parents)
        b=p.read_bytes();row={'path':z['path'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'worktree_mode':stat.S_IMODE(p.stat().st_mode)}
        if z['path'] in native4:assert git('show',head+':'+z['path'])==b
        else:assert len(b)==z['bytes']and row['sha256']==z['sha256']
        rows.append(row)
    assert git('rev-parse','HEAD').decode().strip()==head
    for z in rows:
        p=R/z['path'];b=p.read_bytes();assert len(b)==z['bytes']and hashlib.sha256(b).hexdigest()==z['sha256']and stat.S_IMODE(p.stat().st_mode)==z['worktree_mode']
    utc=dt.datetime.now(dt.timezone.utc).isoformat()
    out={'schema':'pr45-root-fresh-acceptance-input-preimages/v1','approved_by_root':True,'created_utc':utc,
         'reason_date_utc':utc[:10],'reason':'Fresh actual main after the complete independent PR45 mathematical and closed acceptance source review, completed actual final reconciliation and published PR44 predecessor inspection governs present integration. Historical264c26 remains unchanged archival authority; thirteen live bytes and full modes are independently rebound, and the five explicitly declared other-project tracked files (three descending-audit files and two logs) remain protected.',
         'current_head':head,'files':rows,'protected_foreign_tracked_paths':PROTECTED}
    with(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V2.json').open('x')as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({'status':'PASS_FRESH_ACTUAL13_MAIN_AUTHORITY','head':head,'files':len(rows),'protected_paths':PROTECTED}))
if __name__=='__main__':main()
