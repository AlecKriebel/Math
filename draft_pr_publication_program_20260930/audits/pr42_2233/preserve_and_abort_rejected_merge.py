"""Undo only ROOT's rejected original PR42 merge after preserving exact evidence.

An orchestration mistake continued after currentHEAD check failed. No overlay or
commit occurred. This verifies the exact owned merge scope before aborting it.
"""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess
A=Path(__file__).resolve().parent;R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def run(*argv):return subprocess.check_output(list(argv),cwd=R)
def main():
    assert __debug__
    head=run('git','rev-parse','HEAD').decode().strip();assert head=='c2fd4422ddb55face646e7a279733211bc10a486'
    assert run('git','rev-parse','MERGE_HEAD').decode().strip()=='099ae5e4d06d8789214cfaaece87309c87e914f9'
    original=json.loads((A/'snapshot_manifest_v2.json').read_bytes())['files']
    own={'unsolved_math_prioritization/attempts/2233/'+z['path']for z in original};qname='unsolved_math_prioritization/QUEUE.md'
    staged=set(run('git','diff','--cached','--name-only').decode().splitlines());assert staged==own|{qname}
    dirty=set(run('git','diff','--name-only').decode().splitlines())-{qname}
    foreign=[]
    for name in sorted(dirty):
        p=R/name;b=p.read_bytes();foreign.append({'path':name,'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)})
    d=A/'rejected_original_merge_after_concurrent_PR386';d.mkdir()
    (d/'PRELAUNCH_ROOT_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    (d/'actual_conflicted_QUEUE.md').write_bytes((R/qname).read_bytes())
    index=run('git','ls-files','--stage','-z');(d/'whole_actual_index_entries.bin').write_bytes(index)
    for z in original:
        name='unsolved_math_prioritization/attempts/2233/'+z['path'];b=run('git','show',':'+name)
        assert len(b)==z['bytes']and sha(b)==z['sha256']and b==(R/name).read_bytes()
        p=d/'original17'/z['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    qbefore=run('git','show',head+':'+qname);(d/'actual_current_head_QUEUE.md').write_bytes(qbefore)
    start=dt.datetime.now(dt.timezone.utc).isoformat();c=subprocess.Popen(['git','merge','--abort'],cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);b,e=c.communicate();finish=dt.datetime.now(dt.timezone.utc).isoformat()
    (d/'abort.stdout.bin').write_bytes(b);(d/'abort.stderr.bin').write_bytes(e)
    assert c.returncode==0
    assert run('git','rev-parse','HEAD').decode().strip()==head and run('git','diff','--cached','--name-only')==b''
    assert (R/qname).read_bytes()==qbefore and not (R/'unsolved_math_prioritization/attempts/2233').exists()
    assert subprocess.run(['git','rev-parse','--verify','MERGE_HEAD'],cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
    for z in foreign:
        p=R/z['path'];b=p.read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']and stat.S_IMODE(p.stat().st_mode)==z['full_mode']
    rec={'schema':'pr42-root-rejected-own-merge-rollback/v1','utc':finish,'status':'PASS_OWN_REJECTED_MERGE_PRESERVED_AND_ABORTED','actual_ROOT_pid':os.getpid(),'actual_abort_pid':c.pid,'abort_started_utc':start,'abort_finished_utc':finish,'abort_exit_code':c.returncode,'main_unchanged':head,'exact_owned_staged_paths':sorted(staged),'foreign_worktree_preimages_preserved':foreign,'entire_current_head_queue_restored':True,'canonical_absent_restored':True,'index_clean_restored':True,'error':'ROOT launched a dependent original merge after a failed HEAD equality check because that tool result was not used to stop subsequent calls. Concurrent acceptedPR386 changedmain. No overlay/commit/push/native42event occurred. ROOT must stop on every prerequisite failure and repeat fresh ready-state preflight on latestmain.'}
    (d/'ROLLBACK_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps({'status':rec['status'],'main_unchanged':head,'actual_abort_pid':c.pid,'foreign_files_preserved':len(foreign),'exact_owned_staged_paths':len(staged)}))
if __name__=='__main__':main()
