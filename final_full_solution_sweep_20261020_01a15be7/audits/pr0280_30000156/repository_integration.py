#!/usr/bin/env python3
"""PR280 exact original+five overlay, non-force FF, test/actual merge preservation."""
import argparse
import base64
import json
import subprocess
from urllib.parse import quote
from ops_binding import *
from publication_live_gates import collect

BASELINE_ROW = '| 303 | 30000156 / OWR-768-006 | Limiting Cycle Distributions of Birational Maps | 0.1719 | 5.0 | 3 | 2004 | queued | 0/5 |  |  |  |\n'.encode()
DESIRED_ROW = '| 303 | 30000156 / OWR-768-006 | Limiting Cycle Distributions of Birational Maps | 0.1719 | 5.0 | 3 | 2004 | claimed_solved | 1/5 |  | Reviewed counterexample L(u,v)=(u,(u²+1)v): full affine permutations for p≡3 mod4, no point-weighted limit at any fixed 1/2≤x<1. Unconditional arithmetic inputs; rational inverse scope explicit. |  |\n'.encode()


def api(endpoint, method='GET', body=None):
    command=['gh','api','--hostname','github.com','repos/AlecKriebel/Math/'+endpoint,'--method',method]
    data=None
    if body is not None:
        command+=['--input','-']
        data=json.dumps(body,ensure_ascii=False).encode()
    run=subprocess.run(command,input=data,capture_output=True,cwd=REPO)
    if run.returncode:
        raise RuntimeError('GitHub operation failed; reconcile intent before retry: '+run.stderr.decode(errors='replace')[:700])
    return json.loads(run.stdout)


def blob_sha(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def signature(entry):
    return entry['mode'],entry['type'],entry['sha']


def tree_map(tree,recursive=False):
    result=api('git/trees/'+tree+('?recursive=1' if recursive else ''))
    if result.get('truncated'):
        raise RuntimeError('Truncated tree cannot establish preservation')
    entries=result['tree']
    if len({e['path'] for e in entries})!=len(entries):
        raise RuntimeError('Duplicate Git tree entry')
    return {e['path']:e for e in entries}


def subtree(commit,path,recursive=True):
    tree=api('git/commits/'+commit)['tree']['sha']
    for part in path.split('/') if path else []:
        entry=tree_map(tree).get(part)
        if entry is None:
            return {}
        if entry['type']!='tree':
            raise RuntimeError('Expected directory: '+path)
        tree=entry['sha']
    return tree_map(tree,recursive)


def leaves(commit,path):
    return {n:signature(e) for n,e in subtree(commit,path).items() if e['type']!='tree'}


def blob(commit,path):
    parent,name=path.rsplit('/',1)
    item=subtree(commit,parent,False).get(name)
    if item is None or item['type']!='blob' or item['mode']!='100644':
        raise RuntimeError('Missing or irregular Git file: '+path)
    value=api('git/blobs/'+item['sha'])
    if value['encoding']!='base64':
        raise RuntimeError('Unexpected Git blob encoding')
    data=base64.b64decode(value['content'])
    if blob_sha(data)!=item['sha']:
        raise RuntimeError('Git blob checksum mismatch')
    return data


def originals():
    snapshot=json.loads((AUDIT/'SOURCE_SNAPSHOT.json').read_text())
    if snapshot['head']!=ORIGINAL or snapshot['pr']!=280 or len(snapshot['files'])!=17:
        raise RuntimeError('Unexpected original snapshot schema/head/inventory')
    result={}
    for e in snapshot['files']:
        if not e['path'].startswith(PROBLEM+'/'):
            raise RuntimeError('Original repository path outside selected problem')
        name=e['path'][len(PROBLEM)+1:]
        data=safe_file(AUDIT,e['snapshot']).read_bytes()
        if (name in result or len(data)!=e['bytes'] or sha(data)!=e['sha256']
                or blob_sha(data)!=e['git_blob']):
            raise RuntimeError('Original snapshot bytes/blob changed')
        result[name]=('100644','blob',e['git_blob'])
    return result


def selection():
    r=release()
    return {'preprint/'+e['path']:(PUBLICATION/e['path']).read_bytes() for e in r['files']}


def own_queue_row(data):
    rows=[line for line in data.splitlines(keepends=True) if b'| 30000156 / OWR-768-006 |' in line]
    if len(rows)!=1:
        raise RuntimeError('Own QUEUE row absent/duplicated')
    return rows[0]


def original_queue_rows(expected_head):
    if ([p['sha'] for p in api('git/commits/'+ORIGINAL)['parents']] != [ORIGINAL_PARENT]
            or own_queue_row(blob(ORIGINAL_PARENT,QUEUE))!=BASELINE_ROW
            or own_queue_row(blob(ORIGINAL,QUEUE))!=DESIRED_ROW
            or own_queue_row(blob(expected_head,QUEUE))!=DESIRED_ROW):
        raise RuntimeError('Original exact parent/head QUEUE row binding changed')
    return BASELINE_ROW,DESIRED_ROW


def unchanged_parent(before,after,parent,exceptions):
    a={k:signature(v) for k,v in subtree(before,parent,False).items() if k not in exceptions}
    b={k:signature(v) for k,v in subtree(after,parent,False).items() if k not in exceptions}
    if a!=b:
        raise RuntimeError('Unselected entries changed under '+(parent or 'root'))


def assert_scoped_preservation(before,after,queue_changed):
    unchanged_parent(before,after,'',{'unsolved_math_prioritization'})
    unchanged_parent(before,after,'unsolved_math_prioritization',{'attempts','QUEUE.md'} if queue_changed else {'attempts'})
    unchanged_parent(before,after,'unsolved_math_prioritization/attempts',{'30000156'})



def verify_directory_overlay(base,integrated,added_names,original=None):
    def inventory(commit):
        result={n:(v['mode'],v['type']) for n,v in subtree(commit,PROBLEM).items() if v['type']=='tree'}
        if any(v!=('040000','tree') for v in result.values()):
            raise RuntimeError('Unexpected selected directory mode/type')
        return result
    expected=inventory(base)
    if original is not None:expected.update(inventory(original))
    for name in added_names:
        parts=PurePosixPath(name).parts
        for end in range(1,len(parts)):expected['/'.join(parts[:end])]=('040000','tree')
    if inventory(integrated)!=expected:
        raise RuntimeError('Selected subtree directory inventory changed outside exact overlay')

def verify_integrated_tree(base,integrated,expected_head):
    selected=selection()
    expected=leaves(base,PROBLEM)
    added=originals()
    added.update({n:('100644','blob',blob_sha(v)) for n,v in selected.items()})
    for n,identity in added.items():
        if n in expected and expected[n]!=identity:
            raise RuntimeError('Concurrent main changed selected candidate file: '+n)
    expected.update(added)
    verify_directory_overlay(base,integrated,added,ORIGINAL)
    if leaves(integrated,PROBLEM)!=expected:
        raise RuntimeError('Integration differs outside exact original17+publication5 overlay')
    baseline,desired=original_queue_rows(expected_head)
    old_queue=blob(base,QUEUE)
    old=own_queue_row(old_queue)
    if old not in {baseline,desired}:
        raise RuntimeError('Own QUEUE row is neither exact baseline nor reviewed desired row')
    if blob(integrated,QUEUE)!=old_queue.replace(old,desired,1):
        raise RuntimeError('QUEUE changed beyond the exact reviewed own row')
    assert_scoped_preservation(base,integrated,True)
    return {'main':base,'integrated_commit':integrated,'head':expected_head,
            'original_files':17,'publication_files':5,'queue_other_bytes_preserved':True,
            'all_unselected_root_unsolved_attempts_siblings_preserved':True}


def live_pr(expected_head):
    from prepublication_check import validate_pr
    pr=api('pulls/280')
    validate_pr(pr,expected_head,'before_integration')
    return pr


def overlay_entry(name,data):
    entry={'path':PROBLEM+'/'+name,'mode':'100644','type':'blob'}
    try:
        entry['content']=data.decode('utf-8')
    except UnicodeDecodeError:
        result=api('git/blobs','POST',{'encoding':'base64','content':base64.b64encode(data).decode()})
        if result['sha']!=blob_sha(data):
            raise RuntimeError('Uploaded binary Git blob differs')
        entry['sha']=result['sha']
    return entry


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['plan','commit','verify-test-merge','merge'])
    parser.add_argument('--expected-pr-head',required=True)
    args=parser.parse_args()
    verify_destination()
    pr=live_pr(args.expected_pr_head)
    selected=selection()
    if args.action in {'plan','commit'}:
        if args.expected_pr_head!=ORIGINAL or leaves(ORIGINAL,PROBLEM)!=originals():
            raise RuntimeError('Overlay must start at exact reviewed17-file original head')
        original_queue_rows(ORIGINAL)
        if any(n in leaves(ORIGINAL,PROBLEM) for n in selected):
            raise RuntimeError('Publication paths already exist; reconcile instead of overwriting')
        receipt={'timestamp':stamp(),'pr':280,'original_head':ORIGINAL,'action':args.action,
                 'selected_paths':[PROBLEM+'/'+n for n in selected],'shared_checkout_or_index_modified':False}
        if args.action=='plan':
            atomic_json(AUDIT/'PUBLICATION_BRANCH_PLAN.json',receipt)
            print(json.dumps(receipt,indent=2));return
        require_release_clearance()
        gate,_=collect('before_integration',ORIGINAL)
        original_tree=api('git/commits/'+ORIGINAL)['tree']['sha']
        entries=[overlay_entry(n,data) for n,data in selected.items()]
        tree=api('git/trees','POST',{'base_tree':original_tree,'tree':entries})
        commit=api('git/commits','POST',{'message':'Add reviewed birational cycle-distribution note and verification package',
                   'tree':tree['sha'],'parents':[ORIGINAL]})
        new=commit['sha']
        if [p['sha'] for p in commit['parents']]!=[ORIGINAL] or commit['tree']['sha']!=tree['sha']:
            raise RuntimeError('New commit ancestry/tree differs')
        assert_scoped_preservation(ORIGINAL,new,False)
        expected=originals();expected.update({n:('100644','blob',blob_sha(v)) for n,v in selected.items()})
        verify_directory_overlay(ORIGINAL,new,selected)
        if leaves(new,PROBLEM)!=expected:
            raise RuntimeError('New branch commit changed unselected problem files')
        gate,_=collect('before_integration',ORIGINAL)
        live_pr(ORIGINAL)
        intent={**receipt,'commit':new,'tree':tree['sha'],'non_forced':True,'gate_receipt':gate['receipt']}
        atomic_json(AUDIT/'PUBLICATION_BRANCH_PUSH_INTENT.json',intent)
        api('git/refs/heads/'+quote(pr['head']['ref'],safe='/'),'PATCH',{'sha':new,'force':False})
        if api('pulls/280')['head']['sha']!=new:
            raise RuntimeError('Uncertain branch push; reconcile intent before retry')
        atomic_json(AUDIT/'PUBLICATION_BRANCH_COMMIT.json',{**intent,'status':'pushed_and_verified'})
        print(json.dumps(intent,indent=2));return
    require_release_clearance()
    main_sha=api('git/ref/heads/main')['object']['sha']
    if pr.get('mergeable') is not True or not pr.get('merge_commit_sha'):
        raise RuntimeError('No clean current test merge available')
    merged=api('git/commits/'+pr['merge_commit_sha'])
    if [p['sha'] for p in merged['parents']]!=[main_sha,args.expected_pr_head]:
        raise RuntimeError('Test merge is stale')
    receipt=verify_integrated_tree(main_sha,merged['sha'],args.expected_pr_head)
    if api('git/ref/heads/main')['object']['sha']!=main_sha:
        raise RuntimeError('Main advanced during integration check')
    receipt.update(timestamp=stamp(),pr=280,test_merge=merged['sha'],ready_for_exact_head_merge=True)
    atomic_json(AUDIT/'MERGE_INTEGRATION_ACCEPTANCE.json',receipt)
    if args.action=='merge':
        if pr['draft']:
            raise RuntimeError('PR remains draft; root must mark ready after scientific gates')
        gate,_=collect('before_integration',args.expected_pr_head)
        live_pr(args.expected_pr_head)
        if api('git/ref/heads/main')['object']['sha']!=main_sha:
            raise RuntimeError('Main changed immediately before merge')
        atomic_json(AUDIT/'PR_MERGE_INTENT.json',{**receipt,'gate_receipt':gate['receipt']})
        result=api('pulls/280/merge','PUT',{'sha':args.expected_pr_head,'merge_method':'merge',
                   'commit_title':'Merge reviewed PR280 birational cycle-distribution result'})
        atomic_json(AUDIT/'PR_MERGE_RESPONSE.json',result)
        if result.get('merged') is not True:
            raise RuntimeError('Merge not confirmed; reconcile before retry')
        actual=api('git/commits/'+result['sha'])
        if [p['sha'] for p in actual['parents']]!=[main_sha,args.expected_pr_head]:
            raise RuntimeError('Actual merge parents differ; stop publication')
        receipt=verify_integrated_tree(main_sha,result['sha'],args.expected_pr_head)
        atomic_json(AUDIT/'PR_MERGE_VERIFIED.json',{**receipt,'verified_utc':stamp(),'merged':True})
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    main()
