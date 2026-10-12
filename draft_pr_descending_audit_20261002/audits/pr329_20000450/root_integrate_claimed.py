"""Accept exact PR329 only after a separately closed clean whole-preprint review."""
from root_submission_gate import *

window();clear=current_clearance()
assert not (A/'ACTUAL_MERGE_ATTEMPT.json').exists(),'Inspect any earlier uncertain merge; never repeat blindly.'
cap=Capture('actual_acceptance');m=load(A/'repaired_snapshot_manifest.json')
head=m['head'];base=m['base'];expected={e['path'] for e in m['files']};assert len(expected)==23
assert cap.git('branch','--show-current')==b'main\n'
assert not cap.git('diff','--cached','--raw','-z')
assert cap.run('no_active_merge',['git','rev-parse','-q','--verify','MERGE_HEAD'],ok=(1,)).returncode==1
assert not cap.git('diff','--name-only','--',*sorted(expected))
assert not cap.git('diff','--name-only','--',*[str((O/n).relative_to(R)) for n in FORMAL])
assert cap.git('rev-parse','HEAD').decode().strip()==base
foreign_args=['ls-files','--stage','-z','--','.']+[':(exclude)'+n for n in sorted(expected)]
foreign_before=cap.git(*foreign_args)
def dirty_foreign():
    out={}
    for n in cap.git('diff','--name-only','-z').split(b'\0'):
        if n and n.decode() not in expected:
            p=R/n.decode();out[n.decode()]=(p.exists(),p.read_bytes() if p.is_file() else None,p.stat().st_mode&0o7777 if p.exists() else None)
    return out
dirty_before=dirty_foreign()
pr=json.loads(cap.run('pr_before',['gh','api','repos/AlecKriebel/Math/pulls/329']).stdout)
assert pr['state']=='open' and pr['head']['sha']==head and pr['base']['sha']==base
files=json.loads(cap.run('pr_files',['gh','api','repos/AlecKriebel/Math/pulls/329/files?per_page=100']).stdout)
assert {x['filename'] for x in files}==expected and len(files)==23
window();cap.run('main_fetch',['git','fetch','origin','main'])
assert cap.git('rev-parse','origin/main').decode().strip()==base
v=cap.git('merge-tree','--write-tree',base,head);tree=v.decode().splitlines()[0]
assert tree==cap.git('show','-s','--format=%T',head).decode().strip()
binding=tree_binding(cap,base,tree);package=fresh_package_integrity(cap)
(A/'ROOT_EXACT_LIVE_PREMERGE.json').write_text(json.dumps(dict(utc=utc(),status='PASS_PR329_EXACT_LIVE_PREMERGE',head=head,base=base,tree=tree,**binding,**package,capture_directory=str(cap.directory)),indent=2)+'\n')
body_path=A/'accepted_pr_body.txt';merge_body_path=A/'merge_body.txt'
assert body_path.is_file() and merge_body_path.is_file()
body=body_path.read_text();assert '1/5' in body and 'unrefereed' in body and 'Verdure' in body and 'Morton' in body
current_clearance();assert cap.git(*foreign_args)==foreign_before and dirty_foreign()==dirty_before
window();cap.run('edit_body',['gh','pr','edit','329','--body-file',body_path])
if pr['draft']:window();cap.run('ready',['gh','pr','ready','329'])
last=json.loads(cap.run('last_premerge_api',['gh','api','repos/AlecKriebel/Math/pulls/329']).stdout)
assert last['state']=='open' and not last['draft'] and last['head']['sha']==head and last['base']['sha']==base and last['body']==body
assert last['mergeable'] is True and last['mergeable_state']=='clean'
test=json.loads(cap.run('test_merge_commit',['gh','api','repos/AlecKriebel/Math/git/commits/'+last['merge_commit_sha']]).stdout)
assert [p['sha'] for p in test['parents']]==[base,head] and test['tree']['sha']==tree
remote=json.loads(cap.run('last_main_ref',['gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).stdout)
assert remote['object']['sha']==base and cap.git('rev-parse','HEAD').decode().strip()==base
assert not cap.git('diff','--cached','--raw','-z')
assert cap.git(*foreign_args)==foreign_before and dirty_foreign()==dirty_before
current_clearance();window()
(A/'ACTUAL_MERGE_ATTEMPT.json').write_text(json.dumps(dict(utc=utc(),head=head,base=base,tree=tree,capture_directory=str(cap.directory)),indent=2)+'\n')
cap.run('merge',['gh','pr','merge','329','--merge','--match-head-commit',head,
    '--subject','Accept PR #329: verified full fifth torsion of the pentagonal pencil (1/5)',
    '--body-file',merge_body_path])
after=json.loads(cap.run('post_merge_api',['gh','api','repos/AlecKriebel/Math/pulls/329']).stdout)
assert after['merged'] is True and after['merged_at'] and after['head']['sha']==head
merge=after['merge_commit_sha'];window();cap.run('post_merge_fetch',['git','fetch','origin','main'])
parents=cap.git('show','-s','--format=%P',merge).decode().strip().split();assert parents==[base,head]
assert cap.git('show','-s','--format=%T',merge).decode().strip()==tree
actual=tree_binding(cap,base,merge)
cap.git('merge-base','--is-ancestor',merge,'origin/main')
window();cap.run('sync_main',['git','merge','--ff-only','origin/main'])
assert cap.git('branch','--show-current')==b'main\n'
assert cap.git(*foreign_args)==foreign_before and dirty_foreign()==dirty_before
assert not cap.git('diff','--cached','--raw','-z')
cap.git('merge-base','--is-ancestor',merge,'HEAD')
for e in m['files']:
    assert cap.git('show',merge+':'+e['path'])==(R/e['path']).read_bytes()
for n,e in clear['formal_submission_files'].items():assert pin(O/n)==e
current_clearance()
result=dict(utc=utc(),status='PASS_PR329_EXACT_MERGE',pr=329,accepted_head=head,base=base,actual_merge=merge,
    actual_parents=parents,actual_tree=tree,merged_at=after['merged_at'],**actual,
    unrelated_index_and_dirty_tracked_bodies_modes_preserved=True,main_branch_retained=True,
    complete_clean_preprint_clearance_unchanged=True,capture_directory=str(cap.directory),workflow_percent=90,
    mathematical_verification_percent=100,priority_percent=100,zenodo_pending=True,tracker_pending=True)
(A/'ACTUAL_MERGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
