"""Merge exact PR311 only after a separately closed clean NEW whole review."""
from root_submission_gate import *
import time

window()
clear = current_clearance()
assert not (A/'ACTUAL_MERGE_ATTEMPT.json').exists(), 'Inspect any earlier uncertain merge; never repeat blindly.'
cap = Capture('actual_acceptance')
m = load(A/'repaired_snapshot_manifest.json')
head,base = m['head'],m['base']
expected = {e['path'] for e in m['files']}
assert len(expected) == 31
assert cap.git('branch','--show-current') == b'main\n'
assert not cap.git('diff','--cached','--raw','-z')
assert cap.run('no_active_merge',['/usr/bin/git','rev-parse','-q','--verify','MERGE_HEAD'],ok=(1,)).returncode == 1
assert not cap.git('diff','--name-only','--',*sorted(expected))
assert not cap.git('diff','--name-only','--',*[str((O/n).relative_to(R)) for n in FORMAL])
assert cap.git('rev-parse','HEAD').decode().strip() == base
foreign_args = ['ls-files','--stage','-z','--','.']+[':(exclude)'+n for n in sorted(expected)]
foreign_before,dirty_before = cap.persist_foreign_snapshot('before_actual_merge',expected)
pr = json.loads(cap.run('pr_before',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311']).stdout)
assert pr['state'] == 'open' and pr['head']['sha'] == head and pr['base']['ref'] == 'main'
files = json.loads(cap.run('pr_files',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311/files?per_page=100']).stdout)
assert len(files) == 31 and {x['filename'] for x in files} == expected
assert {x['filename']:x['sha'] for x in files} == {e['path']:e['git_blob_sha'] for e in m['files']}
window()
cap.git('fetch','origin','main')
assert cap.git('rev-parse','origin/main').decode().strip() == base
tree = cap.git('merge-tree','--write-tree',base,head).decode().splitlines()[0]
assert tree == cap.git('show','-s','--format=%T',head).decode().strip()
binding = tree_binding(cap,base,tree)
(A/'ROOT_EXACT_LIVE_PREMERGE.json').write_text(json.dumps({'utc':utc(),'status':'PASS_PR311_EXACT_LIVE_PREMERGE',
    'head':head,'actual_main_base':base,'tree':tree,'api_base_sha_informational_only':pr['base']['sha'],
    **binding,'capture_directory':str(cap.directory)},indent=2)+'\n')
body_path,merge_body_path = A/'accepted_pr_body.txt',A/'merge_body.txt'
assert body_path.is_file() and merge_body_path.is_file()
body = body_path.read_text()
assert all(s in body for s in ['2/5','unrefereed','Gandolfi','Kahle','Conjecture 1','AI'])
current_clearance()
assert cap.git(*foreign_args) == foreign_before and dirty_tracked(cap,expected) == dirty_before
window()
cap.run('edit_body',['/opt/homebrew/bin/gh','pr','edit','311','--repo','AlecKriebel/Math','--body-file',body_path])
if pr['draft']:
    window()
    cap.run('ready',['/opt/homebrew/bin/gh','pr','ready','311','--repo','AlecKriebel/Math'])
for j in range(6):
    last = json.loads(cap.run('last_premerge_api_'+str(j),['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311']).stdout)
    if last['mergeable'] is not None:
        break
    time.sleep(.5)
assert last['state'] == 'open' and not last['draft'] and last['head']['sha'] == head and last['body'] == body
assert last['mergeable'] is True and last['mergeable_state'] == 'clean'
test = json.loads(cap.run('test_merge_commit',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/git/commits/'+last['merge_commit_sha']]).stdout)
assert [p['sha'] for p in test['parents']] == [base,head] and test['tree']['sha'] == tree
remote = json.loads(cap.run('last_main_ref',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).stdout)
assert remote['object']['sha'] == base and cap.git('rev-parse','HEAD').decode().strip() == base
assert not cap.git('diff','--cached','--raw','-z')
assert cap.git(*foreign_args) == foreign_before and dirty_tracked(cap,expected) == dirty_before
current_clearance()
window()
(A/'ACTUAL_MERGE_ATTEMPT.json').write_text(json.dumps({'utc':utc(),'head':head,'base':base,'tree':tree,'capture_directory':str(cap.directory)},indent=2)+'\n')
cap.run('merge',['/opt/homebrew/bin/gh','pr','merge','311','--repo','AlecKriebel/Math','--merge','--match-head-commit',head,
    '--subject','Accept PR #311: verified binary MTP2 edge-model closure (2/5)',
    '--body-file',merge_body_path])
after = json.loads(cap.run('post_merge_api',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311']).stdout)
assert after['merged'] is True and after['merged_at'] and after['head']['sha'] == head
merge = after['merge_commit_sha']
window()
cap.git('fetch','origin','main')
parents = cap.git('show','-s','--format=%P',merge).decode().strip().split()
assert parents == [base,head]
assert cap.git('show','-s','--format=%T',merge).decode().strip() == tree
actual = tree_binding(cap,base,merge)
cap.git('merge-base','--is-ancestor',merge,'origin/main')
# Sync only the exact reviewed merge; a concurrently advanced main must be
# independently reconciled before any wider checkout update.
assert cap.git('rev-parse','origin/main').decode().strip() == merge
window()
cap.git('merge','--ff-only',merge)
assert cap.git('branch','--show-current') == b'main\n'
assert cap.git(*foreign_args) == foreign_before and dirty_tracked(cap,expected) == dirty_before
assert not cap.git('diff','--cached','--raw','-z')
cap.git('merge-base','--is-ancestor',merge,'HEAD')
for e in m['files']:
    assert cap.git('show',merge+':'+e['path']) == (R/e['path']).read_bytes()
current_clearance()
result = {'utc':utc(),'status':'PASS_PR311_EXACT_MERGE','pr':311,'accepted_head':head,
    'base':base,'actual_merge':merge,'actual_parents':parents,'actual_tree':tree,'merged_at':after['merged_at'],
    **actual,'unrelated_index_dirty_tracked_bodies_modes_preserved':True,'main_branch_retained':True,
    'clean_preprint_clearance_unchanged':True,'capture_directory':str(cap.directory),
    'workflow_percent':90,'mathematical_verification_percent':100,'bounded_priority_percent':100,
    'zenodo_pending':True,'tracker_pending':True}
(A/'ACTUAL_MERGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
