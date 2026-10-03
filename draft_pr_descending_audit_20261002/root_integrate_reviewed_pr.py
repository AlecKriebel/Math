"""Guarded exact-head acceptance, preserving unrelated shared main work."""
import datetime, hashlib, json, subprocess, sys
from pathlib import Path

P=Path(__file__).resolve().parent
A=P/'audits'/sys.argv[1]
n=int(sys.argv[2]);problem=sys.argv[3]
manifest_name=sys.argv[4] if len(sys.argv)>4 else 'repaired_snapshot_manifest.json'
m=json.loads((A/manifest_name).read_text());head=m['head']
queue='unsolved_math_prioritization/QUEUE.md'
expected={e['path'] for e in m['files']}
frozen_queue=subprocess.check_output(['git','show',f'{head}:{queue}']).splitlines()
own=[l for l in frozen_queue if len(l.split(b'|'))>9 and l.split(b'|')[2].strip().split(b' / ')[0].decode()==problem]
assert len(own)==1
proposal=[own[0].split(b'|')[j].strip() for j in (8,9)]
assert proposal in ([b'unsolved',b'5/5'],[b'already_solved',b'0/5'])
status,turns=[x.decode() for x in proposal]
expected_queue_cells=[8,9] if status=='unsolved' else [8]
resolution=0 if status=='unsolved' else 100
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args])
def run(args,tag,ok=(0,)):
    r=subprocess.run(args,capture_output=True)
    (A/(tag+'.stdout')).write_bytes(r.stdout);(A/(tag+'.stderr')).write_bytes(r.stderr)
    assert r.returncode in ok,(tag,r.returncode,r.stderr.decode())
    return r
def remote(tag):return json.loads(run(['gh','pr','view',str(n),'--json','state,headRefOid,isDraft,mergeable,mergeStateStatus,body,mergedAt,mergeCommit,url'],tag).stdout)
def check_tree(base,tree):
    paths=set(git('diff','--name-only',base,tree).decode().splitlines())
    assert paths==expected,(paths-expected,expected-paths)
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
assert not git('diff','--name-only','--',*sorted(expected))
assert not git('diff','--cached','--name-only','--',*sorted(expected))
r=remote('actual_acceptance_remote_before');assert r['state']=='OPEN' and r['headRefOid']==head
body=(A/'accepted_pr_body.txt').read_text()
run(['gh','pr','edit',str(n),'--body-file',str(A/'accepted_pr_body.txt')],'accepted_body_edit')
if r['isDraft']:run(['gh','pr','ready',str(n)],'accepted_ready')
r=remote('actual_pre_merge_remote')
assert r['state']=='OPEN' and r['headRefOid']==head and not r['isDraft'] and r['body']==body
assert r['mergeable']=='MERGEABLE' and r['mergeStateStatus']=='CLEAN',r
run(['git','fetch','origin','main'],'pre_merge_main_fetch')
base=git('rev-parse','origin/main').decode().strip()
v=run(['git','merge-tree','--write-tree',base,head],'virtual_merge')
tree=v.stdout.decode().splitlines()[0];vi=check_tree(base,tree)
(A/'virtual_integration_receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':base,'reviewed_head':head,'virtual_tree':tree,**vi},indent=2)+'\n')
run(['gh','pr','merge',str(n),'--merge','--match-head-commit',head,'--subject',f'Accept PR #{n}: verified {status} partial findings ({turns})','--body-file',str(A/'merge_body.txt')],'actual_merge_execution')
r=remote('post_merge_remote');assert r['state']=='MERGED' and r['headRefOid']==head and r['mergedAt']
merge=r['mergeCommit']['oid']
run(['git','fetch','origin','main'],'post_merge_fetch')
parents=git('show','-s','--format=%P',merge).decode().strip().split();assert len(parents)==2 and parents[1]==head
actual=check_tree(parents[0],merge)
assert subprocess.run(['git','merge-base','--is-ancestor',merge,'origin/main']).returncode==0
sync=run(['git','merge','--ff-only','origin/main'],'post_merge_main_sync',ok=(0,128))
reconciled=False
if sync.returncode:
    assert not git('diff','--name-only','--',*sorted(expected))
    assert not git('diff','--cached','--name-only','--',*sorted(expected))
    run(['git','merge','--no-edit','origin/main'],'post_merge_main_reconcile')
    run(['git','push','origin','main'],'post_merge_main_reconcile_push');reconciled=True
assert subprocess.run(['git','merge-base','--is-ancestor',merge,'HEAD']).returncode==0
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':n,'reviewed_head':head,'actual_merge':merge,'merged_at':r['mergedAt'],'actual_parents':parents,**actual,'merge_is_ancestor_of_remote_and_local_main':True,'main_reconciled_preserving_concurrent_histories':reconciled,'workflow_percent':100,'original_resolution_percent':resolution,'novel_original_solution_claimed':False,'status':status,'turns':turns,'paper':False,'zenodo':False,'doi':False,'tracker_row':False,'release':False}
(A/'ACTUAL_MERGE_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
c=json.loads((A/'acceptance_criteria.json').read_text());c.update(workflow_percent=100,actual_merge_pending=False,actual_merge=merge,actual_merge_verification='ACTUAL_MERGE_VERIFICATION.json');(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n')
inv=json.loads((P/'inventory.json').read_text());x=next(x for x in inv['items'] if x['number']==n);x.update(disposition=f'merged_verified_{status}_partial',audit_workflow_percent=100,accepted_head=head,actual_merge=merge,merged_at=r['mergedAt']);inv['completed_by_descending']+=1;(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
for f in [A/'ACCEPTANCE_DECISION.md',A/'README.md',P/'RESEARCH_LOG.md']:
    with f.open('a') as h:h.write(f'\n{receipt["utc"]}: PR{n} actual acceptance `{merge}` at {r["mergedAt"]}; all{actual["all_expected_paths_exact"]} paths and{actual["all_target_file_hashes_exact"]} target hashes exact. Only own queue line{actual["queue_physical_line"]} cells{expected_queue_cells}; every other queue byte preserved. Status{status},{turns};workflow100%, original resolution{resolution}% (credited prior literature when already_solved); program{inv["completed_by_descending"]}/{len(inv["items"])}={100*inv["completed_by_descending"]/len(inv["items"]):.4f}%. No paper/DOI.\n')
print(json.dumps(receipt,indent=2))
