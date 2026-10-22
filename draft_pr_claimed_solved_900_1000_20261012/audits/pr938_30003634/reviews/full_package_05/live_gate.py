from authenticate import *
f=json.loads((D/'PREPUBLICATION_FREEZE.json').read_bytes());snap=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_bytes())
pr=json.loads(run(['gh','pr','view','938','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,title,body,url']))
(R/'private/live_pr.json').write_text(json.dumps(pr,indent=2)+'\n')
need(pr['state']=='OPEN' and pr['isDraft'] is True and pr['baseRefName']=='main' and pr['headRefOid']==HEAD,'live PR eligibility')
need(sha(pr['body'].encode())==f['pr_description_sha256'],'description pin')
remote=run(['git','ls-remote','origin','refs/heads/main']).decode().split()[0]
try:run(['git','cat-file','-e',remote])
except subprocess.CalledProcessError:raise RuntimeError('remote main object unavailable locally; do not mutate shared checkout')
queue=run(['git','show',HEAD+':unsolved_math_prioritization/QUEUE.md']);(R/'private/immutable_QUEUE.md').write_bytes(queue)
def rowrest(b):
 lines=b.splitlines(keepends=True);hits=[x for x in lines if b'| 30003634 /' in x];need(len(hits)==1,'unique target');return hits[0],b''.join(x for x in lines if x!=hits[0])
row,other=rowrest(queue);cells=row.decode().split('|');need(cells[8].strip()=='claimed_solved' and cells[9].strip()=='1/5','original status/turns')
base=run(['git','merge-base',HEAD,remote]).decode().strip();need(rowrest(run(['git','show',base+':unsolved_math_prioritization/QUEUE.md']))[1]==other,'other queue bytes')
changed=run(['git','diff','--name-only',base,HEAD]).decode().splitlines();need(set(changed)==set(snap['files'])|{'unsolved_math_prioritization/QUEUE.md'},'actual changed scope')
remote_files=run(['gh','api','repos/AlecKriebel/Math/pulls/938/files','--paginate','--jq','.[].filename']).decode().splitlines();need(set(remote_files)==set(changed),'remote file scope')
cat=json.loads(run(['git','show',remote+':unsolved_math_prioritization/catalog.json']));selected=[x for x in cat if str(x['id'])=='30003634'];need(len(selected)==1,'source unique');target=selected[0];(R/'private/selected_catalog.json').write_text(json.dumps(target,indent=2)+'\n')
need(target.get('present') is True and target.get('holds')==[] and target['statement_hash']=='2302f06ebd156e0ce9f1728964208380752184dcd932a117b8b397e409c15d6b' and target['review_hash']=='eebfb186fc2eefe2cb9756aec0572e127127fc1be6e248d6abad78a4fe298bd9','source hashes/holds')
identity={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','head':HEAD,'remote_main':remote,'merge_base':base,'queue_status':'claimed_solved','original_turns':'1/5','changed_files':len(changed),'original_other_queue_bytes_unchanged':True,'current_source_present':True,'current_source_holds':[],'statement_hash':target['statement_hash'],'review_hash':target['review_hash'],'pr_description_exact':True}
(R/'LIVE_GATE.json').write_text(json.dumps(identity,indent=2)+'\n');print(json.dumps(identity))
