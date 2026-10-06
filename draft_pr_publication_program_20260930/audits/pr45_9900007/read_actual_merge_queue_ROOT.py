"""Read the whole actual conflict body and verify both complete Git conflict stages."""
from pathlib import Path
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];Q='unsolved_math_prioritization/QUEUE.md'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    assert __debug__
    assert git('diff','--name-only','--diff-filter=U')==(Q+'\n').encode()
    raw=(R/Q).read_bytes();text=raw.decode();assert '\0'not in text
    before=(A/'integration_queue_before.md').read_bytes();other=git('show','d9b4acf5d070d1f04ffac86a4f08916a5629ff16:'+Q)
    assert git('show',':2:'+Q)==before and git('show',':3:'+Q)==other
    rows=[line for line in text.splitlines()if line.startswith('|')];target=[line for line in rows if len(line.split('|'))==14 and line.split('|')[2].strip()=='9900007 / AMR-098-0007']
    markers=[{'line':i+1,'literal':line}for i,line in enumerate(text.splitlines())if line.startswith(('<<<<<<<','=======','>>>>>>>'))]
    assert markers and len(markers)%3==0 and len(target)>=1
    with(A/'ROOT_ENTIRE_ACTUAL_AUTOMATIC_MERGE_QUEUE.md').open('xb')as f:f.write(raw)
    o={'schema':'pr45-root-entire-actual-automatic-merge-queue-reading/v1','entire_bytes_read_and_UTF8_lines_parsed':True,
       'bytes':len(raw),'sha256':sha(raw),'table_rows':len(rows),'complete_stage2_equals_actual_fresh_main':True,
       'complete_stage3_equals_original_PR_HEAD':True,'conflict_markers':markers,'target_rows':target,
       'accepted_overlay_will_reconstruct_entire_fresh_main_with_only_selected_Status_Turns_Findings':True}
    with(A/'ROOT_ACTUAL_AUTOMATIC_MERGE_QUEUE_REVIEW.json').open('x')as f:json.dump(o,f,indent=2);f.write('\n')
    print(json.dumps(o))
if __name__=='__main__':main()
