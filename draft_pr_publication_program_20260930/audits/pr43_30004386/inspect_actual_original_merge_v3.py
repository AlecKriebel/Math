"""Correct repository-relative paths for independent inspection of the actual merge."""
from pathlib import Path
import datetime as dt,hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'root_actual_original_merge_v3_inspection';K=R/'unsolved_math_prioritization/attempts/30004386'
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
    assert __debug__;D.mkdir();(D/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    p=json.loads((A/'integration_preflight.json').read_bytes())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==p['main_before']
    assert subprocess.check_output(['git','rev-parse','MERGE_HEAD'],cwd=R).decode().strip()=='86be0f85c7a37a5cad8d24abd16a32d8d1f27e62'
    Q='unsolved_math_prioritization/QUEUE.md';conflicts=subprocess.check_output(['git','diff','--name-only','--diff-filter=U'],cwd=R).decode().splitlines();assert set(conflicts)<={Q}
    before=(A/'integration_queue_before.md').read_bytes()
    assert subprocess.check_output(['git','show','HEAD:'+Q],cwd=R)==before
    if conflicts:
        assert subprocess.check_output(['git','show',':2:'+Q],cwd=R)==before
        assert subprocess.check_output(['git','show',':3:'+Q],cwd=R)==subprocess.check_output(['git','show','86be0f85c7a37a5cad8d24abd16a32d8d1f27e62:'+Q],cwd=R)
    else:assert subprocess.check_output(['git','show',':'+Q],cwd=R)==(R/Q).read_bytes()
    m=json.loads((A/'snapshot_manifest.json').read_bytes());rows=m['files'];assert len(rows)==16
    assert {q.relative_to(K).as_posix()for q in K.rglob('*')if q.is_file()}=={z['path']for z in rows}
    for z in rows:
        q=A/'source_snapshot'/z['path'];candidate=K/z['path'];b=q.read_bytes()
        assert candidate.read_bytes()==b and len(b)==z['size']and sha(b)==z['sha256']
        rel=candidate.relative_to(R).as_posix();assert subprocess.check_output(['git','ls-files','-s','--',rel],cwd=R).decode().startswith('100644 ')
    queue=(R/Q).read_bytes();(D/'merge_conflict_queue.md').write_bytes(queue)
    result={'schema':'root-pr43-original-merge-inspection/v1','status':'PASS_CORRECT_ORIGINAL_MERGE_AUTOMATIC_QUEUE','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'main_before':p['main_before'],'original_head':'86be0f85c7a37a5cad8d24abd16a32d8d1f27e62','original16_bytes_and_modes_verified':True,'merge_queue_preimage_sha256':sha(queue),'previous_ROOT_wrapper_expected_conflict_exit1_but_actual_merge_correctly_auto_merged_exit0':True,'conflicts':conflicts}
    (D/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
