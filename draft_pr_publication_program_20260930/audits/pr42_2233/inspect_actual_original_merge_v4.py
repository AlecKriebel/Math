"""Correct repository-relative paths for independent inspection of the actual merge."""
from pathlib import Path
import datetime as dt,hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'root_actual_original_merge_v4_inspection';K=R/'unsolved_math_prioritization/attempts/2233'
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
    assert __debug__;D.mkdir();(D/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    p=json.loads((A/'integration_preflight.json').read_bytes())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==p['main_before']
    assert subprocess.check_output(['git','rev-parse','MERGE_HEAD'],cwd=R).decode().strip()=='099ae5e4d06d8789214cfaaece87309c87e914f9'
    Q='unsolved_math_prioritization/QUEUE.md';assert subprocess.check_output(['git','diff','--name-only','--diff-filter=U'],cwd=R).decode().splitlines()==[Q]
    before=(A/'integration_queue_before.md').read_bytes()
    assert subprocess.check_output(['git','show','HEAD:'+Q],cwd=R)==before==subprocess.check_output(['git','show',':2:'+Q],cwd=R)
    assert subprocess.check_output(['git','show',':3:'+Q],cwd=R)==subprocess.check_output(['git','show','099ae5e4d06d8789214cfaaece87309c87e914f9:'+Q],cwd=R)
    m=json.loads((A/'snapshot_manifest_v2.json').read_bytes());rows=m['files'];assert len(rows)==17
    assert {q.relative_to(K).as_posix()for q in K.rglob('*')if q.is_file()}=={z['path']for z in rows}
    for z in rows:
        q=A/'source_snapshot_v2'/z['path'];candidate=K/z['path'];b=q.read_bytes()
        assert candidate.read_bytes()==b and len(b)==z['size']and sha(b)==z['sha256']
        rel=candidate.relative_to(R).as_posix();assert subprocess.check_output(['git','ls-files','-s','--',rel],cwd=R).decode().startswith('100644 ')
    queue=(R/Q).read_bytes();(D/'merge_conflict_queue.md').write_bytes(queue)
    result={'schema':'root-pr42-original-merge-inspection/v1','status':'PASS_EXPECTED_QUEUE_CONFLICT_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'main_before':p['main_before'],'original_head':'099ae5e4d06d8789214cfaaece87309c87e914f9','original17_bytes_and_modes_verified':True,'merge_queue_preimage_sha256':sha(queue),'previous_wrapper_failed_only_on_wrong_ROOT_queue_path_after_actual_correct_merge':True}
    (D/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
