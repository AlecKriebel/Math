#!/usr/bin/env python3
"""Record the confirmed priority closure; inspect later PRs only for exact status."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib,io,json,subprocess,tarfile
P=Path(__file__).resolve().parent;ROOT=P.parent;A=P/'audits/pr932_30003471'

def need(value,message):
    if not value:raise RuntimeError(message)

def run(args):return subprocess.run(args,cwd=ROOT,capture_output=True,text=True,check=True).stdout

def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')

def main():
    now=datetime.now(timezone.utc).isoformat();receipt=json.loads((A/'CLOSURE_RECEIPT.json').read_text())
    need(receipt['outcome']=='closed_without_merge_established_priority' and receipt['pr']==932 and
         receipt['problem_id']=='30003471' and receipt['merge_performed'] is False and
         receipt['preprint_or_DOI_or_sheet_entry_created'] is False,'Closure outcome incomplete')
    pr=json.loads(run(['gh','pr','view','932','--repo','AlecKriebel/Math','--json','number,state,headRefOid,closedAt,mergedAt,url']))
    need(pr['state']=='CLOSED' and pr['mergedAt'] is None and pr['headRefOid']==receipt['original_head'],'Final closure readback differs')
    comment=json.loads(run(['gh','api','repos/AlecKriebel/Math/issues/comments/'+str(receipt['comment']['id'])]))
    need(hashlib.sha256(comment['body'].encode()).hexdigest()==receipt['closure_comment_sha256'] and
         comment['html_url']==receipt['comment']['url'],'Closure comment readback differs')
    record={'utc':now,'pr':932,'problem_id':'30003471','outcome':receipt['outcome'],'original_pr_head':receipt['original_head'],
            'closed_at':pr['closedAt'],'closure_comment_url':comment['html_url'],'decision_sha256':receipt['decision_sha256'],
            'original_turns_preserved':'1/5','original_files_unchanged':29,'mathematical_verdict':'No unresolved gap found in candidate3Dproof',
            'priority_verdict':'Exact full strengthening already covered by verified Winter finite prior theorem; not a novel open-problem resolution',
            'independent_review_families':8,'fresh_adversarial_priority_review':True,'doi':None,'merge_commit':None,
            'tracker_range':None,'native_queue_or_state_mutated':False,'new_author_proof_search_turns':0}
    save(A/'PRIORITY_CLOSURE_FINAL_VERIFICATION.json',{'confirmed_closed_without_merge':True,'comment_exact_readback':True,
         'workflow_completion_percent':100,'no_preprint_deposit_or_tracker_write':True,'record':record})
    state=json.loads((P/'CURRENT_STATE.json').read_text());already=any(r['pr']==932 for r in state['completed_results'])
    need(state.get('active_pr') in (932,None) or already,'Unexpected active target')
    if already and state.get('active_pr') not in (932,None):
        print(json.dumps({'already_finalized':True,'next_pr':state['active_pr']}));return
    completed=[r for r in state['completed_results'] if r['pr']!=932]+[record];completed.sort(key=lambda r:r['pr'])
    state.setdefault('initial_eligible_prs',state['eligible_prs'].copy())
    state.update(utc=now,completed_results=completed,completed_prs=[r['pr'] for r in completed],
                 published_prs=[r['pr'] for r in completed if r['outcome']=='accepted_merged_preprint_published'],
                 closed_prs=[r['pr'] for r in completed if r['outcome'].startswith('closed_')],
                 active_pr=None,active_problem_id=None,active_pr_completion_estimate_percent=0,phase='next_status_gate_after_PR932')
    inventory=json.loads((P/'inventory.json').read_text())
    for row in inventory:
        if row['number']==932:row.update(disposition=record['outcome'],closure_comment_url=record['closure_comment_url'])
    if not already:
        with (P/'README.md').open('a') as out:out.write('\nPR #932 closed without merging on verified exact-priority grounds. Candidate mathematics has no unresolved gap found; Winter\'s prior finite theorem already covers the entire strengthening. No preprint/DOI/tracker entry.\n')
        for f in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
            with f.open('a') as out:out.write(f'\n{now} — PR932 completed100% disposition workflow: closed without merge after verified exact-priority supersession and fresh adversarial falsification. Comment {comment["html_url"]} read back exactly; all29 originals/1of5 preserved. No DOI/preprint/Sheet/nativequeue mutation. Seven of initial12eligible workflows handled; six published and one priority closure.\n')
    # Save the completed outcome before beginning the later status-only scan.
    save(P/'CURRENT_STATE.json',state);save(P/'inventory.json',inventory)
    skipped=[]
    for old in sorted((v for v in inventory if v['number']>932),key=lambda v:v['number']):
        number=old['number'];pr=json.loads(run(['gh','pr','view',str(number),'--repo','AlecKriebel/Math',
              '--json','number,state,isDraft,headRefOid,headRefName,baseRefName,url']))
        if pr['state']!='OPEN' or not pr['isDraft']:
            skipped.append({'pr':number,'action':'SKIP_NOT_OPEN_DRAFT','math_source_read':False})
            if number in state['eligible_prs'] and number not in state['completed_prs']:state['eligible_prs'].remove(number)
            continue
        ids=[str(e['id']) for e in old['entries']];need(len(ids)==1,'Multiple targets need narrow metadata reconciliation')
        key=ids[0];queue=run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['headRefOid'],
                            '-H','Accept: application/vnd.github.raw+json'])
        rows=[r for r in queue.splitlines() if '| '+key+' /' in r];need(len(rows)==1,'Ambiguous target queue row')
        status=rows[0].split('|')[8].strip()
        if status!='claimed_solved':
            skipped.append({'pr':number,'problem_id':key,'status':status,'action':'SKIP_STATUS_ONLY','math_source_read':False})
            old.update(eligible=False,disposition='skipped_status_gate')
            if number in state['eligible_prs'] and number not in state['completed_prs']:state['eligible_prs'].remove(number)
            continue
        need(pr['baseRefName']=='main','Selected next target base changed')
        folder=P/'audits'/f'pr{number}_{key}';folder.mkdir(exist_ok=True)
        need(not (folder/'ORIGINAL_SNAPSHOT.json').exists(),'Next snapshot already exists; inspect before replacing')
        stamp=datetime.now(timezone.utc).isoformat();pr.update(problem_id=key,status=status,eligible=True,gate_utc=stamp,
             queue_row_sha256=hashlib.sha256(rows[0].encode()).hexdigest())
        save(folder/'ELIGIBILITY_GATE.json',pr);(folder/'GATED_QUEUE_ROW.md').write_text(rows[0]+'\n')
        run(['git','fetch','--no-write-fetch-head','origin',pr['headRefOid']])
        prefix='unsolved_math_prioritization/attempts/'+key
        raw=subprocess.run(['git','archive',pr['headRefOid'],prefix],cwd=ROOT,check=True,capture_output=True).stdout
        original=folder/'original';original.mkdir(exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:archive.extractall(original,filter='data')
        files={f.relative_to(original).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(original.rglob('*')) if f.is_file()}
        save(folder/'ORIGINAL_SNAPSHOT.json',{'utc':stamp,'head':pr['headRefOid'],'files':files})
        if number not in state['eligible_prs']:state['eligible_prs'].append(number);state['eligible_prs'].sort()
        for field in ['active_original_head','original_candidate_turns','review_families','priority_families','publication_disposition',
                      'priority_status','full_package_reviews','candidate_revision02_frozen','operational_helper_revision']:
            state.pop(field,None)
        state.update(utc=stamp,active_pr=number,active_problem_id=key,next_pr=number,active_original_head=pr['headRefOid'],
                     phase=f'PR{number}_exact_claimed_solved_gate_passed_before_math_reading',active_pr_completion_estimate_percent=0)
        old.update(eligible=True,status='claimed_solved');break
    state['shard_completion_estimate_percent']=100*len(state['completed_prs'])/len(state['eligible_prs'])
    save(P/'CURRENT_STATE.json',state);save(P/'inventory.json',inventory)
    save(P/'POST_PR932_STATUS_GATES.json',{'utc':datetime.now(timezone.utc).isoformat(),'skipped':skipped,'next_pr':state.get('active_pr')})
    print(json.dumps({'PR932':record,'next_pr':state.get('active_pr'),'status_only_skips':skipped,'shard_completion_estimate_percent':state['shard_completion_estimate_percent']},indent=2))

if __name__=='__main__':main()
