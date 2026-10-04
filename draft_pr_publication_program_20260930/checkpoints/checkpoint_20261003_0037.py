"""ROOT exact owned checkpoint; exclude active families and all foreign bodies."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

P=Path(__file__).resolve().parents[1];R=P.parent
names=set()


def add(path):
    assert path.is_file() and not path.is_symlink()
    assert all(not p.is_symlink()for p in path.parents)
    assert path.stat().st_size <= 100*1024*1024, str(path)
    names.add(path.relative_to(R).as_posix())


def tree(path):
    assert path.is_dir() and not path.is_symlink()
    for p in path.rglob('*'):
        assert not p.is_symlink()
        if p.is_file():add(p)
        else:assert p.is_dir()


def main():
    assert __debug__
    assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
    assert subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R)==b''
    before=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
    assert before=='c61dc0cb572de281b871264819c8b80d647d0373'
    inv=json.loads((P/'inventory.json').read_bytes());assert inv['completed_count']==31
    a42=P/'audits/pr42_2233';a43=P/'audits/pr43_30004386';a44=P/'audits/pr44_2912'
    for a in [a42,a43,a44]:
        for path in a.iterdir():
            if path.is_file():add(path)
        for path in a.glob('root_*_actual_capture'):tree(path)
        for path in a.glob('root_*_capture'):
            if path.is_dir():tree(path)
    for path in [a42/'reviewed_candidate',a42/'whole_current_source_first_family',
                 a43/'reviewed_candidate',a43/'current_preparation_family',
                 a43/'current_source_adversary_family',a44/'source_snapshot',
                 a44/'source_snapshot_v2',a44/'original_git_commands',
                 a44/'original_git_commands_v2']:tree(path)
    for path in (a43/'tmp').glob('root_pr43_current_outer_*'):tree(path)
    for path in (a43/'tmp').glob('root_pr43_current_build_*'):tree(path)
    # Only completed actual PR42 administrative attempts are included.
    for path in (a42/'tmp').glob('root_pr42_current_build_*'):tree(path)
    utc=dt.datetime.now(dt.timezone.utc).isoformat()
    entries={a42:'PR42 scoped math and current whole review clean; actual ROOT currentfreeze60795 and own inspections63639/71361 passed. Original2/5,new0/audit0, fullUNSOLVED, discovery5%, acceptance workflow90%. Final-source review/reconciliation/merge still pending.',
             a43:'PR43 exact published source-match and repaired prior proofs verified. Sourceprep38+self and newsourceadversary20+self clean; actualbuilder68759/operator68758 and ROOT currentinspection76003 passed. Original0/5,new0/audit0, newprojectdiscovery0%, workflow85%. NEW wholeadversary active, final acceptance pending.',
             a44:'PR44 original18/19diff verified at actualbase01358d66. Own export71950 failed before scientific execution because of guessed PROOF filename; oldsource/18exportedfiles/error preserved. Corrected actualexport73037 passed with OBSTRUCTION filename and distinct V2 artifacts. Two independent approach families have early seals and are auditing. Original2/5,new0/audit0, fullproblem discovery0%, audit20%.'}
    for a,text in entries.items():
        with (a/'ROOT_RESEARCH_LOG.md').open('a')as out:out.write('\n'+utc+' — '+text+'\n')
        add(a/'ROOT_RESEARCH_LOG.md')
    with (P/'RESEARCH_LOG.md').open('a')as out:
        out.write('\n'+utc+' — Checkpoint:31/180 accepted, best-guess program completion17.22222222222222%. PR42 current whole review clean;43 credited prior result final review active;44 two independent approaches started. Active families and foreign/restricted source bodies excluded. No new paper/DOI/tracker for these partial statuses. Git snapshots file bytes and executable flags, not complete filesystem0444/special-bit permissions or empty directories; the exact local mode observations remain dated evidence, and mode restoration is needed to reproduce permission-sensitive guards from a fresh clone. Original closed manifests and all old failure records remain unchanged.\n')
    add(P/'RESEARCH_LOG.md');add(Path(__file__))
    rows=[]
    for n in sorted(names):
        p=R/n;raw=p.read_bytes()
        rows.append({'path':n,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'observed_full_stat_S_IMODE':format(stat.S_IMODE(p.stat().st_mode),'05o')})
    output=P/'checkpoints/CHECKPOINT_20261003_0037.json'
    with output.open('x')as out:
        json.dump({'schema':'ROOT_exact_owned_checkpoint/v1','created_utc':utc,'main_before':before,
            'completed_count':31,'total':180,'completion_estimate_percent':31/180*100,
            'owned_files':rows,'owned_member_bytes':sum(r['bytes']for r in rows),
            'active_families_included':False,'foreign_primary_bodies_included':False,
            'full_filesystem_permissions_are_not_Git_tree_metadata':True},out,indent=2);out.write('\n')
    add(output)
    subprocess.run(['git','add','--',*sorted(names)],cwd=R,check=True)
    actual=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0')
    expected=set(names)
    assert {n for n in actual if n}.issubset(expected)
    for n in filter(None,actual):
        staged=subprocess.check_output(['git','show',':'+n],cwd=R)
        assert staged==(R/n).read_bytes() and len(staged)<=100*1024*1024
    print(json.dumps({'status':'PASS_EXACT_OWNED_CHECKPOINT_STAGED','main_before':before,
        'owned_members':len(names),'staged_changed_members':len([n for n in actual if n]),
        'original_member_bytes':sum(r['bytes']for r in rows),'completed':31,'total':180},indent=2))


if __name__=='__main__':main()
