from pathlib import Path
import contextlib,datetime,hashlib,io,json,stat,sys
R=Path('/Users/alec/Documents/Math');D=R/'draft_pr_claimed_solved_700_800_20261012';T=D/'audits/pr799_30002364/tmp';M=T/'root-receipts'
sys.path.insert(0,str(D));from graphql_scoped_commit import Remote,gql,head_oid,commit_updates
from remote_scoped_commit import oid
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((M/'SHARD_COMPLETE_CHECKPOINT_RECEIPT.json').read_text());remote=Remote(receipt['commit'])
need(not (M/'FINAL_RECEIPT_CHECKPOINT.json').exists(),'Reconcile confirmed final receipt instead of repeating')
state=json.loads(remote.read(D.name+'/STATE.json'))
need(state['status']=='complete' and state['current_pr'] is None and state['overall_completion_estimate_percent']==100,'complete remote state')
need([r['pr'] for r in state['processed']]==[718,734,742,764,765,767,778,781,786,788,789,799],'complete ascending initial eligible list')
need(state['remaining_exact_claimed_solved']==[] and state['skipped_count']==89,'exhausted scope')
need(remote.read(D.name+'/RESULTS.md')==(M/'FINAL_RESULTS.md').read_text(),'final result index exact bytes')
need(remote.read((T.parent/'DISPOSITION.json').relative_to(R).as_posix())==(T.parent/'DISPOSITION.json').read_text(),'frozen native-bound disposition')
for name,mp,cp,checker in [('disposition_scope','7f72f2f949a592f9bfee02caceb4f6fc7095bf21e4617f035818be7ad3f5dab9','ba4d78d7c9316260fae8e1671f46594f4f207859159b9f410e95cb5b7ac19b1b','verify_packet.py')]:
 for fn,expected in [('MANIFEST.json',mp),(checker,cp)]:
  need(hashlib.sha256(remote.read((T/name/fn).relative_to(R).as_posix()).encode()).hexdigest()==expected,'committed final independent packet pin')
delivery=json.loads((M/'ROOT_FINAL_DELIVERY.json').read_text())
for r in delivery['nine_exact_published_PDF_deliverables']:
 need(remote.entry(r['path'])=={'mode':'100644','type':'blob','sha':oid('blob',(R/r['path']).read_bytes())},'committed exact final PDF')
# One last metadata-only101-number capture after the100% checkpoint. All
# immutable open-draft heads must still agree with the independently screened
#89 rows; a changed head requires another eligibility screen, not an assumption.
prior=json.loads((T/'disposition_scope/FINAL_METADATA_CAPTURES.json').read_text())
expected=[r for b in prior['after'] for r in b['response'].values()]
fields='number title state isDraft merged headRefOid headRefName closedAt url mergeCommit { oid }';current=[]
for start in range(700,801,25):
 ns=list(range(start,min(start+25,801)))
 q='query { repository(owner:"AlecKriebel",name:"Math") { '+' '.join(f'p{n}:pullRequest(number:{n}){{{fields}}}' for n in ns)+' } }'
 data=gql(q)['repository'];need(set(data)=={f'p{n}' for n in ns},'direct complete aliases')
 current.extend(data['p'+str(n)] for n in ns)
need(current==expected,'Window metadata changed after final independent screen; rescreen before completion')
old=json.loads((D/'audits/pr789_30001478/tmp/root-receipts/LOCAL_PROGRAM_MIRROR_SYNC_COMPLETE.json').read_text())
baseline=[]
for row in old['only_own6text_mirrors'][:4]:
 p=R/row['path'];need(stat.S_ISREG(p.lstat().st_mode) and p.stat().st_nlink==1,'own local regular text')
 need(sha(p)==row['sha256'],'unrecognized own local edit; preserve')
 baseline.append({'path':row['path'],'sha256':sha(p)})
p=T.parent/'RESEARCH_LOG.md';need(stat.S_ISREG(p.lstat().st_mode) and p.stat().st_nlink==1,'own case log')
baseline.append({'path':p.relative_to(R).as_posix(),'sha256':sha(p)})
confirmation={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS',
 'complete_checkpoint':receipt['commit'],'complete_state_and_results_read_back':True,
 'processed_in_ascending_order':[r['pr'] for r in state['processed']],
 'final_all101_metadata_unchanged_after_independent_screens':current,
 'remaining_exact_claimed_solved':[],'nine_exact_published_PDFs_also_committed':True,
 'native_bound_disposition_and_final_independent_packet_pins_unchanged':True,
 'local_own5_mirror_baselines':baseline,'shared_Git_main_branch_checkout_index_objects_and_refs_untouched':True}
confirm=M/'FINAL_CONFIRMATION.json';confirm.write_text(json.dumps(confirmation,indent=2)+'\n')
updates={p.relative_to(R).as_posix():p.read_bytes() for p in [Path(__file__),confirm,M/'SHARD_COMPLETE_CHECKPOINT_RECEIPT.json']}
for attempt in range(3):
 fresh=Remote(head_oid());u=dict(updates);path=D.name+'/checkpoint_receipts.jsonl';log=fresh.read(path)
 if not any(json.loads(l).get('commit')==receipt['commit'] for l in log.splitlines() if l):log+=json.dumps(receipt)+'\n'
 u[path]=log
 out=io.StringIO()
 with contextlib.redirect_stdout(out):final=commit_updates(fresh,u,'Record final100-percent shard checkpoint receipt and exhaustive readback')
 (M/'FINAL_RECEIPT_CHECKPOINT_RAW.txt').write_text(out.getvalue())
 if final:break
else:raise RuntimeError('Main races exhausted; no confirmed final receipt checkpoint')
(M/'FINAL_RECEIPT_CHECKPOINT.json').write_text(json.dumps(final,indent=2)+'\n');print(json.dumps({'receipt_checkpoint':final['commit']}),flush=True)
# Guarded sync of only five owned text mirrors, after durable publication.
committed=Remote(final['commit']);payloads=[];new=[]
for row in baseline:
 p=R/row['path'];need(sha(p)==row['sha256'],'own mirror changed during final readback')
 raw=committed.read(row['path']).encode();payloads.append((p,raw));new.append({'path':row['path'],'sha256':hashlib.sha256(raw).hexdigest()})
for p,raw in payloads:p.write_bytes(raw)
need(json.loads((D/'STATE.json').read_text())['status']=='complete','local final state')
for name in ['STATE.json','RESULTS.md']:
 need((D/name).read_text()==committed.read(D.name+'/'+name),'local committed final view exact')
sync={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','source_commit':final['commit'],
 'only_own5text_mirrors':new,'authenticated_previous_owned_hashes':True,
 'unrelated_working_files_Git_index_objects_and_local_refs_untouched':True}
(M/'FINAL_LOCAL_MIRROR_SYNC.json').write_text(json.dumps(sync,indent=2)+'\n')
print(json.dumps({'result':'PASS','complete_checkpoint':receipt['commit'],'final_receipt_checkpoint':final['commit'],'own_local_text_mirrors_synchronized':5,'remaining_eligible':0,'goal_ready_to_mark_complete':True}))
