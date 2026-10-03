"""Guarded claimed-solved acceptance after two fresh preprint reviews.
Preserve unrelated shared main/index work; stop on a failed fast-forward.
"""
import datetime, hashlib, json, subprocess, sys
from pathlib import Path

A=Path(__file__).resolve().parent
P=A.parents[1]
n=364;problem='30004048'
manifest_name='repaired_snapshot_manifest.json'
body_name='accepted_pr_body.txt'
merge_body_name='merge_body.txt'
clearance=json.loads((A/'PUBLISHING_CLEARANCE.json').read_bytes())
assert clearance['status']=='READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS' and clearance['second_review_mandatory_findings']==0
for e in clearance['sealed_submission_files']:
 b=(A/'preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
assert all(Path(name).name==name for name in [manifest_name,body_name,merge_body_name])
m=json.loads((A/manifest_name).read_text());head=m['head']
queue='unsolved_math_prioritization/QUEUE.md'
expected={e['path'] for e in m['files']}
frozen_queue=subprocess.check_output(['git','show',f'{head}:{queue}']).splitlines()
own=[l for l in frozen_queue if len(l.split(b'|'))>9 and l.split(b'|')[2].strip().split(b' / ')[0].decode()==problem]
assert len(own)==1
proposal=[own[0].split(b'|')[j].strip() for j in (8,9)]
assert proposal==[b'claimed_solved',b'3/5']
status,turns=[x.decode() for x in proposal]
criteria=json.loads((A/'acceptance_criteria.json').read_text())
assert [criteria['accepted_status'],criteria['author_turns']]==[status,turns]
assert not criteria['exact_live_root_and_whole_gates_pending'] and not criteria.get('fresh_whole_exact_live_pending',False)
expected_queue_cells=[8,9,11]
resolution=100
root=json.loads((A/'root_exact_live_receipt.json').read_bytes())
assert root['status']=='PASS_COMPLETE_PR364_EXACT_LIVE_AND_SUBMISSION' and root['head']==head and root['base']==m['base']
assert root['fresh_root_complete_package_replay'] and root['all_agent_full_outputs_compared']
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args])
def run(args,tag,ok=(0,)):
    r=subprocess.run(args,capture_output=True)
    (A/(tag+'.stdout')).write_bytes(r.stdout);(A/(tag+'.stderr')).write_bytes(r.stderr)
    assert r.returncode in ok,(tag,r.returncode,r.stderr.decode())
    return r
def remote(tag):return json.loads(run(['gh','pr','view',str(n),'--json','state,headRefOid,isDraft,mergeable,mergeStateStatus,body,mergedAt,mergeCommit,url'],tag).stdout)
def entries(rev):
    out={}
    for item in git('ls-tree','-rz','--full-tree',rev).split(b'\0'):
        if item:
            meta,path=item.split(b'\t',1);out[path.decode()]=meta
    return out
def check_tree(base,tree):
    paths=set(git('diff','--name-only',base,tree).decode().splitlines())
    assert paths==expected,(paths-expected,expected-paths)
    old_entries=entries(base);new_entries=entries(tree);reviewed_entries=entries(head)
    assert {p for p in old_entries.keys()|new_entries.keys() if old_entries.get(p)!=new_entries.get(p)}==expected
    for p in expected-{queue}:assert new_entries[p]==reviewed_entries[p],('reviewed mode/type/blob',p)
    assert old_entries[queue].split()[:2]==new_entries[queue].split()[:2], 'queue mode/type changed'
    for e in m['files']:
        b=git('show',f"{tree}:{e['path']}")
        if e['path']!=queue:assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
    old=git('show',f'{base}:{queue}');new=git('show',f'{tree}:{queue}')
    a=old.splitlines(keepends=True);b=new.splitlines(keepends=True);assert len(a)==len(b)
    diff=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];assert len(diff)==1,diff
    i=diff[0];x=a[i].split(b'|');y=b[i].split(b'|')
    assert x[2].strip().split(b' / ')[0].decode()==problem
    assert [j for j,(u,v) in enumerate(zip(x,y)) if u!=v]==expected_queue_cells
    assert x[8].strip()==b'queued' and x[9].strip()==b'0/5'
    assert [y[j].strip() for j in (8,9)]==proposal
    return {'all_expected_paths_exact':len(paths),'all_target_file_hashes_exact':len(paths)-1,'queue_physical_line':i+1,'only_queue_pipe_cells':expected_queue_cells,'all_other_queue_bytes_equal':True,'base_row':a[i].decode(),'accepted_row':b[i].decode(),'base_queue_sha256':sha(old),'accepted_queue_sha256':sha(new)}
assert git('branch','--show-current').strip()==b'main'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],capture_output=True).returncode!=0,'foreign merge is active; leave untouched'
assert not git('diff','--name-only','--',*sorted(expected))
assert not git('diff','--cached','--name-only','--',*sorted(expected))
foreign_args=['ls-files','-s','-z','--','.']+[':(exclude)'+p for p in sorted(expected)]
foreign_before=git(*foreign_args)
r=remote('actual_acceptance_remote_before');assert r['state']=='OPEN' and r['headRefOid']==head
body=(A/body_name).read_text()
run(['gh','pr','edit',str(n),'--body-file',str(A/body_name)],'accepted_body_edit')
if r['isDraft']:run(['gh','pr','ready',str(n)],'accepted_ready')
r=remote('actual_pre_merge_remote')
assert r['state']=='OPEN' and r['headRefOid']==head and not r['isDraft'] and r['body']==body
assert r['mergeable']=='MERGEABLE' and r['mergeStateStatus']=='CLEAN',r
run(['git','fetch','origin','main'],'pre_merge_main_fetch')
base=git('rev-parse','origin/main').decode().strip()
assert base==m['base'],('reviewed current main changed; require fresh exact-live review',m['base'],base)
assert git('rev-parse','HEAD').decode().strip()==base,'local main differs from literal reviewed base; require refresh'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],capture_output=True).returncode!=0,'foreign merge became active; leave untouched'
v=run(['git','merge-tree','--write-tree',base,head],'virtual_merge')
tree=v.stdout.decode().splitlines()[0];vi=check_tree(base,tree)
assert tree==git('show','-s','--format=%T',head).decode().strip(),'virtual integration tree differs from reviewed head tree'
(A/'virtual_integration_receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':base,'reviewed_head':head,'virtual_tree':tree,**vi},indent=2)+'\n')
last=json.loads(run(['gh','api',f'repos/AlecKriebel/Math/pulls/{n}'],'actual_last_premerge_api').stdout)
assert last['state']=='open' and not last['draft'] and last['head']['sha']==head and last['base']['sha']==base and last['body']==body
assert last['mergeable'] is True and last['mergeable_state']=='clean'
test=json.loads(run(['gh','api',f'repos/AlecKriebel/Math/git/commits/{last["merge_commit_sha"]}'],'actual_last_testmerge_commit').stdout)
assert [x['sha'] for x in test['parents']]==[base,head] and test['tree']['sha']==tree
current=json.loads(run(['gh','api','repos/AlecKriebel/Math/git/ref/heads/main'],'actual_last_main_ref').stdout)
assert current['object']['sha']==base,'current main advanced; require fresh exact-live review'
assert git('rev-parse','HEAD').decode().strip()==base,'local main advanced; require refresh'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],capture_output=True).returncode!=0,'foreign merge became active; leave untouched'
run(['gh','pr','merge',str(n),'--merge','--match-head-commit',head,'--subject',f'Accept PR #{n}: verified negative answer to biconstrained symmetry ({turns})','--body-file',str(A/merge_body_name)],'actual_merge_execution')
r=remote('post_merge_remote');assert r['state']=='MERGED' and r['headRefOid']==head and r['mergedAt']
merge=r['mergeCommit']['oid']
run(['git','fetch','origin','main'],'post_merge_fetch')
parents=git('show','-s','--format=%P',merge).decode().strip().split();assert parents==[base,head],('actual merge parents differ from reviewed pair',parents,base,head)
actual=check_tree(parents[0],merge)
assert subprocess.run(['git','merge-base','--is-ancestor',merge,'origin/main']).returncode==0
run(['git','merge','--ff-only','origin/main'],'post_merge_main_sync')
assert git(*foreign_args)==foreign_before,'Unrelated staged entries changed during integration'
assert subprocess.run(['git','merge-base','--is-ancestor',merge,'HEAD']).returncode==0
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':n,'reviewed_head':head,'actual_merge':merge,'merged_at':r['mergedAt'],'actual_parents':parents,**actual,'merge_is_ancestor_of_remote_and_local_main':True,'main_reconciled_preserving_concurrent_histories':False,'unrelated_staged_entries_preserved':True,'workflow_percent':90,'original_resolution_percent':resolution,'novel_original_solution_claimed':True,'novelty_certified':False,'status':status,'turns':turns,'paper_prepared':True,'zenodo_publication_pending':True,'tracker_append_pending':True,'release':False}
(A/'ACTUAL_MERGE_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
c=json.loads((A/'acceptance_criteria.json').read_text());c.update(workflow_completion_percent=90,actual_merge_pending=False,actual_merge=merge,actual_merge_verification='ACTUAL_MERGE_VERIFICATION.json');(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n')
inv=json.loads((P/'inventory.json').read_text());x=next(x for x in inv['items'] if x['number']==n);x.update(disposition='merged_claimed_solved_preprint_ready_publication_pending',audit_workflow_percent=90,accepted_head=head,actual_merge=merge,merged_at=r['mergedAt']);inv.setdefault('claimed_solved_merged_by_descending',[367]);assert n not in inv['claimed_solved_merged_by_descending'];inv['claimed_solved_merged_by_descending'].append(n);(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
for f in [A/'ACCEPTANCE_DECISION.md',A/'README.md',P/'RESEARCH_LOG.md']:
    with f.open('a') as h:h.write(f'\n{receipt["utc"]}: PR{n} actual acceptance `{merge}` at {r["mergedAt"]}; all{actual["all_expected_paths_exact"]} paths and{actual["all_target_file_hashes_exact"]} target hashes exact. Only own queue line{actual["queue_physical_line"]} cells{expected_queue_cells}; every other queue byte preserved. Status{status},{turns};mathematical resolution100%, acceptance/publication workflow90%. Two fresh sequential preprint reviews complete; Zenodo/DOI/tracker and fresh post-merge checks pending. Current goal processes only submitted claimed_solved; historic other-status completions are retained as history.\n')
print(json.dumps(receipt,indent=2))
