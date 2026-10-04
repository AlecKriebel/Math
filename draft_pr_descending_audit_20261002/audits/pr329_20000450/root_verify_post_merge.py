"""Verify the actual accepted objects before any production deposit."""
from root_submission_gate import *
clear=current_clearance();cap=Capture('post_merge_verification')
m=load(A/'ACTUAL_MERGE_VERIFICATION.json');assert m['status']=='PASS_PR329_EXACT_MERGE'
assert not (A/'ROOT_POST_MERGE_VERIFICATION.json').exists()
api=json.loads(cap.run('merged_pr',['gh','api','repos/AlecKriebel/Math/pulls/329']).stdout)
assert api['merged'] and api['merge_commit_sha']==m['actual_merge'] and api['head']['sha']==m['accepted_head']
merge=m['actual_merge'];assert cap.git('branch','--show-current')==b'main\n'
assert cap.git('show','-s','--format=%P',merge).decode().strip().split()==m['actual_parents']
assert cap.git('show','-s','--format=%T',merge).decode().strip()==m['actual_tree']
cap.git('merge-base','--is-ancestor',merge,'HEAD')
remote=json.loads(cap.run('remote_main',['gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).stdout)
cap.git('merge-base','--is-ancestor',merge,remote['object']['sha'])
binding=tree_binding(cap,m['base'],merge)
for e in load(A/'repaired_snapshot_manifest.json')['files']:
    b=cap.git('show',merge+':'+e['path']);assert b==(R/e['path']).read_bytes()
for n,e in clear['formal_submission_files'].items():
    p=str((O/n).relative_to(R));b=cap.git('show',merge+':'+p)
    assert b==(O/n).read_bytes() and pin(O/n)==e
current_clearance()
result=dict(utc=utc(),status='PASS_PR329_POST_MERGE_EXACT_SUBMISSION',actual_merge=merge,
    accepted_head=m['accepted_head'],**binding,all_four_formal_Git_disk_qualified_bytes_modes_equal=True,
    closed_scientific_and_review_namespaces_unchanged=True,capture_directory=str(cap.directory),
    no_mathematical_artifact_change_or_additional_mathematical_replay_needed=True)
(A/'ROOT_POST_MERGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
