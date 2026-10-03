"""Own text-only precision repair, preserving literal generated source and patch."""
from pathlib import Path
import difflib, hashlib, json, os
H=Path(__file__).resolve().parent
NAMES=['pr46_guards.py','seal_final_evidence.py','capture_root_final_operation.py',
 'integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']
MARK='"""V2 SOURCE ONLY: rejected V1 S1 repaired; independent clean SOURCE audit remains required."""\n'
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    archive=H/'INITIAL_GENERATED_V2_SOURCE';archive.mkdir();changes=[]
    for n in NAMES:
        p=H/n;before=p.read_text();put(archive/n,before.encode());assert before.count(MARK)==1
        after=before.replace(MARK,'',1)
        index=after.index('"""');after=after[:index+3]+'V2 SOURCE ONLY: rejected V1 S1 repaired; new clean SOURCE audit required. '+after[index+3:]
        if n=='pr46_guards.py':
            old="require(type(row['before_worktree_mode']) is int and row['before_worktree_mode']==row['after_worktree_mode']"
            assert after.count(old)==1
            after=after.replace(old,"require(type(row['before_worktree_mode']) is int and type(row['after_worktree_mode']) is int and row['before_worktree_mode']==row['after_worktree_mode']")
        p.write_text(after);changes.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='initial_v2/'+n,tofile='operative_v2/'+n))
    put(H/'V2_PRECISION_REPAIR.patch',''.join(changes).encode())
    print(json.dumps({'status':'PASS_V2_TEXT_ONLY_PRECISION_REPAIR','actual_pid':os.getpid(),'duplicate_docstring_before_future_removed':True,'after_mode_has_exact_int_type':True,'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
