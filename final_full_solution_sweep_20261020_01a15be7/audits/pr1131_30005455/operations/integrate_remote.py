#!/usr/bin/env python3
"""EXTERNAL MUTATIONS: exact remote tree overlay; no local refs/index/checkouts/fetches.
Do not execute until root has independently reviewed and SHA-pinned operational clearance.
"""
import argparse
import base64
from urllib.parse import quote
from ops_common import *
from collect_live import collect

def blob_sha(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def signature(e):return e['mode'],e['type'],e['sha']
def entries(tree,recursive=False):
    r=gh('git/trees/'+tree+('?recursive=1' if recursive else ''))
    need(not r.get('truncated'),'Truncated Git tree')
    es=r['tree'];need(len({e['path'] for e in es})==len(es),'Duplicate tree path')
    return {e['path']:e for e in es}
def subtree(commit,path,recursive=False):
    tree=gh('git/commits/'+commit)['tree']['sha']
    for part in path.split('/') if path else []:
        e=entries(tree).get(part)
        if e is None:return {}
        need(e['type']=='tree' and e['mode']=='040000','Expected ordinary tree');tree=e['sha']
    return entries(tree,recursive)
def leaves(commit,path):return {n:signature(e) for n,e in subtree(commit,path,True).items() if e['type']!='tree'}
def blob(commit,path):
    parent,name=path.rsplit('/',1);e=subtree(commit,parent).get(name)
    need(e and e['type']=='blob' and e['mode']=='100644','Missing/irregular blob')
    r=gh('git/blobs/'+e['sha']);need(r['encoding']=='base64','Unexpected blob encoding')
    b=base64.b64decode(r['content']);need(blob_sha(b)==e['sha'],'Blob checksum');return b

def scoped(before,after):
    for parent,exception in [('', 'unsolved_math_prioritization'),('unsolved_math_prioritization','attempts'),('unsolved_math_prioritization/attempts','30005455')]:
        a={n:signature(e) for n,e in subtree(before,parent).items() if n!=exception}
        b={n:signature(e) for n,e in subtree(after,parent).items() if n!=exception}
        need(a==b,'Unselected siblings changed under '+(parent or 'root'))
    need(blob(before,QUEUE)==blob(after,QUEUE),'QUEUE changed')

def expected_overlay(main):
    pkg=package();_,changes=proposal()
    old={n:pkg['source']['original/'+n] for n in ORIGINALS}
    expected_original={n:('100644','blob',blob_sha(b)) for n,b in old.items()}
    need(leaves(ORIGINAL,PROBLEM)==expected_original,'Original head no longer exactly eight frozen artifacts')
    original_parent=gh('git/commits/'+ORIGINAL)['parents']
    need(len(original_parent)==1,'Unexpected original ancestry')
    scoped(original_parent[0]['sha'],ORIGINAL)
    original_queue=blob(ORIGINAL,QUEUE)
    rows=[x for x in original_queue.splitlines() if b'| 30005455 / OWR-12697708-008 |' in x]
    need(len(rows)==1,'Original own queue row absent/duplicated')
    current=leaves(main,PROBLEM);overlay={PROBLEM+'/'+n:b for n,b in old.items()};overlay.update(changes)
    expected=dict(current)
    for path,b in overlay.items():
        n=path[len(PROBLEM)+1:]
        if n in current:
            # Preserve any concurrent selected work: only absent, original or
            # already exact proposed bytes may be overlaid; everything else stops.
            need(current[n] in {expected_original.get(n),('100644','blob',blob_sha(b))},'Current main selected file conflict: '+n)
        expected[n]=('100644','blob',blob_sha(b))
    return overlay,expected

def verify(main,commit):
    overlay,expected=expected_overlay(main)
    need(leaves(commit,PROBLEM)==expected,'Integrated selected leaves differ from exact overlay')
    def dirs(c):return {n:(e['mode'],e['type']) for n,e in subtree(c,PROBLEM,True).items() if e['type']=='tree'}
    expected_dirs=dirs(main)
    for n in overlay:
        pieces=n[len(PROBLEM)+1:].split('/')
        for end in range(1,len(pieces)):expected_dirs['/'.join(pieces[:end])]=('040000','tree')
    need(dirs(commit)==expected_dirs,'Selected directory inventory changed')
    scoped(main,commit)
    return {'main':main,'commit':commit,'selected_files':len(expected),'original_files':8,'preprint_files':5,'framing_replacements':3,'unselected_siblings_and_queue_preserved':True}

def require_action(args,action):
    c=clearance(args.clearance_sha256,args.operations_sha256);need(action in c['allowed_actions'],'Action not cleared');return c

def remote_write(args,endpoint,method,body,phase,head,gate=None,expected_main=None):
    c=require_action(args,'integrate' if phase=='before_integration' else 'merge')
    g=gate
    if g is None:g,_,_=collect(phase,head,cleared=c)
    validate_pr(gh('pulls/1131'),head,False);fresh(g['at_start'])
    if expected_main is not None:need(g['main']==expected_main and gh('git/ref/heads/main')['object']['sha']==expected_main,'Main advanced before write')
    return command(['gh','api','--hostname','github.com','repos/'+REPOSITORY+'/'+endpoint,'--method',method,'--input','-'],body)

def integrate(args):
    c=require_action(args,'integrate');need(args.expected_pr_head==ORIGINAL,'Initial integration must use original exact PR head')
    pr=gh('pulls/1131');validate_pr(pr,ORIGINAL,False)
    main=gh('git/ref/heads/main')['object']['sha'];overlay,expected=expected_overlay(main)
    g,_,_=collect('before_integration',ORIGINAL,cleared=c)
    need(g['main']==main,'Main advanced during planning')
    durable(RUNTIME/'INTEGRATE_INTENT.json',{'at':stamp(),'head':ORIGINAL,'main':main,'branch':BRANCH,'proposal_sha256':sha((OPS/'INTEGRATION_PROPOSAL.json').read_bytes()),'parents':[ORIGINAL,main],'gate':g['private_capture'],'rule':'Never retry any write after uncertain outcome; inspect objects and exact existing branch, preserve intent.'})
    tree_entries=[]
    for path,b in sorted(overlay.items()):
        obj=remote_write(args,'git/blobs','POST',{'encoding':'base64','content':base64.b64encode(b).decode()},'before_integration',ORIGINAL,gate=g,expected_main=main)
        need(obj['sha']==blob_sha(b),'Uploaded blob mismatch')
        tree_entries.append({'path':path,'mode':'100644','type':'blob','sha':obj['sha']})
    base=gh('git/commits/'+main)['tree']['sha']
    tree=remote_write(args,'git/trees','POST',{'base_tree':base,'tree':tree_entries},'before_integration',ORIGINAL,gate=g,expected_main=main)
    commit=remote_write(args,'git/commits','POST',{'message':'Integrate reviewed finite WARM bounds and frozen preprint package','tree':tree['sha'],'parents':[ORIGINAL,main]},'before_integration',ORIGINAL,gate=g,expected_main=main)
    new=commit['sha'];need([p['sha'] for p in commit['parents']]==[ORIGINAL,main] and commit['tree']['sha']==tree['sha'],'Commit ancestry/tree mismatch')
    checked=verify(main,new)
    durable(RUNTIME/'INTEGRATION_OBJECTS_VERIFIED.json',{**checked,'head':new,'parents':[ORIGINAL,main]})
    need(gh('git/ref/heads/main')['object']['sha']==main,'Main advanced before ref write; stop and reconcile objects')
    remote_write(args,'git/refs/heads/'+quote(BRANCH,safe='/'),'PATCH',{'sha':new,'force':False},'before_integration',ORIGINAL,expected_main=main)
    validate_pr(gh('pulls/1131'),new,False)
    durable(RUNTIME/'INTEGRATION_VERIFIED.json',{**checked,'at':stamp(),'head':new,'parents':[ORIGINAL,main],'non_forced':True})
    return {'head':new,'main':main,'unselected_preservation':True}

def test_merge(args):
    c=require_action(args,'merge');pr=gh('pulls/1131');validate_pr(pr,args.expected_pr_head,False)
    receipt=strict_json((RUNTIME/'INTEGRATION_VERIFIED.json').read_bytes());need(receipt['head']==args.expected_pr_head,'Head lacks verified integration receipt')
    main=gh('git/ref/heads/main')['object']['sha']
    need(pr.get('mergeable') is True and pr.get('merge_commit_sha'),'No clean fresh test merge')
    test=gh('git/commits/'+pr['merge_commit_sha'])
    need([p['sha'] for p in test['parents']]==[main,args.expected_pr_head],'Stale merge parents')
    checked=verify(main,test['sha']);need(gh('git/ref/heads/main')['object']['sha']==main,'Main advanced during test merge check')
    return pr,{**checked,'head':args.expected_pr_head,'test_merge':test['sha'],'tree':test['tree']['sha']}

def describe(args):
    c=require_action(args,'pr-description');pr=gh('pulls/1131');validate_pr(pr,args.expected_pr_head,False)
    receipt=strict_json((RUNTIME/'INTEGRATION_VERIFIED.json').read_bytes());need(receipt['head']==args.expected_pr_head,'Unverified integration head')
    observed=strict_json((OPS/'READ_ONLY_OBSERVATIONS.json').read_bytes())
    need(sha(pr['body'].encode())==observed['original_pr_body_sha256'] and pr['title']==observed['original_pr_title'],'PR description changed; root must review instead of overwriting')
    body=(OPS/'PROPOSED_PR_BODY.md').read_text().replace('{INTEGRATED_HEAD}',args.expected_pr_head)
    g,_,_=collect('before_ready',args.expected_pr_head,cleared=c)
    durable(RUNTIME/'PR_DESCRIPTION_INTENT.json',{'at':stamp(),'head':args.expected_pr_head,'before_body_sha256':observed['original_pr_body_sha256'],'after_body_sha256':sha(body.encode()),'gate':g['private_capture']})
    require_action(args,'pr-description');now=gh('pulls/1131');validate_pr(now,args.expected_pr_head,False)
    need(sha(now['body'].encode())==observed['original_pr_body_sha256'],'PR description advanced before write');fresh(g['at_start'])
    result=command(['gh','api','--hostname','github.com','repos/'+REPOSITORY+'/pulls/1131','--method','PATCH','--input','-'],{'body':body})
    need(result.get('body')==body,'PR description write outcome uncertain')
    now=gh('pulls/1131');validate_pr(now,args.expected_pr_head,False);need(now['body']==body and now['title']==observed['original_pr_title'],'PR description readback mismatch')
    durable(RUNTIME/'PR_DESCRIPTION_VERIFIED.json',{'at':stamp(),'head':args.expected_pr_head,'body_sha256':sha(body.encode())});return {'description_verified':True}


def mark_ready(args):
    c=require_action(args,'ready');pr=gh('pulls/1131');validate_pr(pr,args.expected_pr_head,False)
    receipt=strict_json((RUNTIME/'INTEGRATION_VERIFIED.json').read_bytes());need(receipt['head']==args.expected_pr_head,'Unverified integration head')
    g,_,_=collect('before_ready',args.expected_pr_head,cleared=c)
    need(pr['body']==(OPS/'PROPOSED_PR_BODY.md').read_text().replace('{INTEGRATED_HEAD}',args.expected_pr_head),'Current PR body has not been reconciled to reviewed result')
    need(pr['draft'] is True,'Already ready; reconcile without mutation')
    durable(RUNTIME/'READY_INTENT.json',{'at':stamp(),'head':args.expected_pr_head,'gate':g['private_capture']})
    require_action(args,'ready');validate_pr(gh('pulls/1131'),args.expected_pr_head,False);fresh(g['at_start'])
    result=command(['gh','api','--hostname','github.com','graphql','--input','-'],{'query':'mutation($id:ID!){markPullRequestReadyForReview(input:{pullRequestId:$id}){pullRequest{id isDraft}}}','variables':{'id':pr['node_id']}})
    need(not result.get('errors'),'Ready mutation outcome uncertain')
    current=gh('pulls/1131');validate_pr(current,args.expected_pr_head,False);need(current['draft'] is False,'Ready outcome unconfirmed')
    durable(RUNTIME/'READY_VERIFIED.json',{'at':stamp(),'head':args.expected_pr_head,'draft':False});return {'draft':False}

def merge(args):
    c=require_action(args,'merge');pr,checked=test_merge(args);need(pr['draft'] is False,'Draft PR cannot merge')
    g,_,_=collect('before_merge',args.expected_pr_head,cleared=c)
    need(g['main']==checked['main'],'Main changed since test merge')
    durable(RUNTIME/'MERGE_INTENT.json',{'at':stamp(),**checked,'gate':g['private_capture'],'rule':'Never repeat PUT blindly; inspect PR actual merge SHA, parents, tree.'})
    need(gh('git/ref/heads/main')['object']['sha']==checked['main'],'Main advanced before merge')
    result=remote_write(args,'pulls/1131/merge','PUT',{'sha':args.expected_pr_head,'merge_method':'merge','commit_title':'Merge reviewed finite WARM forest and whisker bounds'},'before_merge',args.expected_pr_head,gate=g,expected_main=checked['main'])
    durable(RUNTIME/'MERGE_RESPONSE.json',result);need(result.get('merged') is True,'Merge not confirmed; reconcile')
    actual=gh('git/commits/'+result['sha'])
    need([p['sha'] for p in actual['parents']]==[checked['main'],args.expected_pr_head] and actual['tree']['sha']==checked['tree'],'Actual merge parents/tree changed; stop publication')
    accepted=verify(checked['main'],actual['sha']);validate_pr(gh('pulls/1131'),args.expected_pr_head,True)
    durable(RUNTIME/'MERGE_VERIFIED.json',{'at':stamp(),**accepted,'head':args.expected_pr_head,'parents':[checked['main'],args.expected_pr_head],'tree':checked['tree'],'merged':True})
    return {'merged':True,'commit':actual['sha']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['integrate','pr-description','ready','verify-test-merge','merge']);p.add_argument('--expected-pr-head',required=True);p.add_argument('--clearance-sha256',required=True);p.add_argument('--operations-sha256',required=True)
    a=p.parse_args();result=test_merge(a)[1] if a.action=='verify-test-merge' else {'integrate':integrate,'pr-description':describe,'ready':mark_ready,'merge':merge}[a.action](a)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
