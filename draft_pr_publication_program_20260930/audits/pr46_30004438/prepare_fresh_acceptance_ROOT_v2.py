"""ROOT independently binds the present main and thirteen native bodies/modes."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess
A=Path(__file__).resolve().parent; R=A.parents[2]
PROTECTED=['draft_pr_descending_audit_20261002/audits/pr373_30004435/RESEARCH_LOG.md','draft_pr_descending_audit_20261002/audits/pr373_30004435/root_primary_source_receipt.json','draft_pr_publication_program_20260930/audits/pr49_30000703/ROOT_RESEARCH_LOG.md','paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/commands.tsv','paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/full_transcript.log']
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
    out={'schema':'pr46-root-fresh-acceptance-input-preimages/v1','approved_by_root':True,'created_utc':utc,
         'reason_date_utc':utc[:10],'reason':'Fresh actual main and thirteen complete native bodies after genuine PR46 V2 SOURCE review, actual ROOT closed-source reconciliation and final sealer execution are the present integration authority. The earlier current freeze stays archival. The exact five declared dirty tracked files belong to two independent descending-audit files, the pending PR49 ROOT research log and two unrelated paper logs; their bytes, full modes, HEAD and index remain protected. The owned program and PR46 operational logs are not foreign exemptions.',
         'current_head':head,'files':rows,'protected_foreign_tracked_paths':PROTECTED}
    previous=A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json'; archive=A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_083702_ARCHIVAL.json'
    assert hashlib.sha256(previous.read_bytes()).hexdigest()=='7da1a49ad5bf7a40ce90bd0f34b1da1113974882c870a97d1223c7d2d7f0d771' and not archive.exists()
    previous.rename(archive)
    with(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json').open('x')as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({'status':'PASS_FRESH_ACTUAL13_MAIN_AUTHORITY','head':head,'files':len(rows),'protected_paths':PROTECTED}))
if __name__=='__main__':main()
