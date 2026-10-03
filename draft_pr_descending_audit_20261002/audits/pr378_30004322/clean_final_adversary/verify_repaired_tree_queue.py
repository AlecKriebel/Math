"""Read-only exact repaired-head gate. Required args: head and actual-main SHA."""
from pathlib import Path
import subprocess,json,hashlib,sys,datetime
R=Path('/Users/alec/Documents/Math')
D=Path(__file__).resolve().parent
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def sha(b):return hashlib.sha256(b).hexdigest()
head,base=sys.argv[1:]
assert git('rev-parse','main').decode().strip()==base,'supplied base is not current actual main'
frozen=json.loads((D.parent/'snapshot_manifest.json').read_text())
math=[e for e in frozen['files'] if e['path'].startswith('problems/')]
assert len(math)==46
for e in math:
    b=git('show',head+':'+e['path'])
    assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']

queue='unsolved_math_prioritization/QUEUE.md'
qb=git('show',base+':'+queue)
qh=git('show',head+':'+queue)
def locate(b):
    found=[line for line in b.splitlines(keepends=True) if line.startswith(b'|') and b'30004322 / OWR-17296-003' in line]
    assert len(found)==1
    chunks=found[0].split(b'|')
    assert len(chunks)==14,('unexpected queue row topology',len(chunks))
    return found[0],chunks
rb,cb=locate(qb);rh,ch=locate(qh)
assert ch[8].strip()==b'unsolved' and ch[9].strip()==b'5/5'
for i in range(len(cb)):
    if i not in (8,9):assert cb[i]==ch[i],('changed protected own queue cell',i)
assert qb.replace(rb,rh)==qh,'changes outside own queue status/turn cells'
mergebase=git('merge-base',base,head).decode().strip()
changes=git('diff','--name-status',base+'...'+head).decode().splitlines()
paths=[line.split('\t')[-1] for line in changes]
assert set(paths)=={e['path'] for e in math}|{queue},('unexpected head-vs-actual-main scope',changes)
assert len(paths)==47
# A second read closes accidental moving-main races during the exact gate.
assert git('rev-parse','main').decode().strip()==base,'main moved during gate'
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repaired_head':head,'actual_main':base,'pr_diff_merge_base':mergebase,'original_head':frozen['head'],'math_files_unchanged':46,'changed_paths_in_pr_diff':47,'queue_target':'30004322 / OWR-17296-003','queue_before_status':cb[8].decode().strip(),'queue_before_turns':cb[9].decode().strip(),'queue_after_status':ch[8].decode().strip(),'queue_after_turns':ch[9].decode().strip(),'only_status_turn_cells_changed':True,'all_other_queue_bytes_identical':True,'base_queue_sha256':sha(qb),'head_queue_sha256':sha(qh),'status':'PASS','mutations':'none'}
(D/'streams'/'repaired_queue_main.txt').write_bytes(qb)
(D/'streams'/'repaired_queue_head.txt').write_bytes(qh)
print(json.dumps(result,sort_keys=True,indent=2))
