"""Authenticate the actual accepted tree and exact submission before production deposit."""
from root_submission_gate import *

clear = current_clearance()
cap = Capture('post_merge_verification')
m = load(A/'ACTUAL_MERGE_VERIFICATION.json')
assert m['status'] == 'PASS_PR311_EXACT_MERGE'
assert not (A/'ROOT_POST_MERGE_VERIFICATION.json').exists()
api = json.loads(cap.run('merged_pr',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311']).stdout)
assert api['merged'] and api['merge_commit_sha'] == m['actual_merge'] and api['head']['sha'] == m['accepted_head']
merge = m['actual_merge']
assert cap.git('branch','--show-current') == b'main\n'
assert cap.git('show','-s','--format=%P',merge).decode().strip().split() == m['actual_parents']
assert cap.git('show','-s','--format=%T',merge).decode().strip() == m['actual_tree']
cap.git('merge-base','--is-ancestor',merge,'HEAD')
remote = json.loads(cap.run('remote_main',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).stdout)
cap.git('merge-base','--is-ancestor',merge,remote['object']['sha'])
binding = tree_binding(cap,m['base'],merge)
for e in load(A/'repaired_snapshot_manifest.json')['files']:
    assert cap.git('show',merge+':'+e['path']) == (R/e['path']).read_bytes()
for n,e in clear['formal_submission_files'].items():
    p = str((O/n).relative_to(R))
    assert cap.git('show',merge+':'+p) == (O/n).read_bytes() and pin(O/n) == e
current_clearance()
result = {'utc':utc(),'status':'PASS_PR311_POST_MERGE_EXACT_SUBMISSION','actual_merge':merge,
    'accepted_head':m['accepted_head'],**binding,'all_five_formal_Git_disk_cleared_bytes_modes_equal':True,
    'closed_scientific_and_review_inputs_unchanged':True,'capture_directory':str(cap.directory),
    'no_math_artifact_change_or_additional_math_replay_needed':True}
(A/'ROOT_POST_MERGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
