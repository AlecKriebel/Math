import contextlib,hashlib,io,json,pathlib,sys
P=pathlib.Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012');A=P/'audits/pr952_10400145';E=A/'operations_engineering_04';R=A/'root_operations04_log_probe'
raw=(E/'PROPOSED_accept_pr952.py').read_bytes()
def need(x,m):
 if not x:raise RuntimeError(m)
need(hashlib.sha256(raw).hexdigest()=='07d1088bcbf8a81c71f15f5f096fcced98e4638244eb794df7efffcd0783688b','externally authenticated proposal')
n={'__name__':'inert_log_closeout_probe','__file__':str(P/'accept_pr952.py')};exec(compile(raw,str(E/'PROPOSED_accept_pr952.py'),'exec',dont_inherit=True,optimize=0),n)
own=R/'private_fixture';own.mkdir();p=own/'program';p.mkdir();a=own/'audit';a.mkdir();w=own/'workflow';w.mkdir();n.update(P=p,A=a,W=w)
sentinel=b'SYNTHETIC LOG BEFORE PUBLICATION\n'
for log in [p/'RESEARCH_LOG.md',a/'RESEARCH_LOG.md']:log.write_bytes(sentinel)
accepted={'freeze_sha256':'f'*64,'full_package_reviews':[{'manifest_sha256':'1'*64},{'manifest_sha256':'2'*64}]};freeze={};pub={'id':17,'doi':'10.5281/zenodo.17','record_url':'https://zenodo.org/records/17'};merge={'mergeCommit':{'oid':'b'*40}};tracker={'updated_range':"'Math Puzzles'!A2:D2",'row':['Original','','https://doi.org/10.5281/zenodo.17','Synthetic']};native={'commit':'c'*40}
state={'active_pr':952,'completed_prs':[],'completed_results':[],'published_prs':[],'eligible_prs':[952,955]};inventory=[{'number':952,'disposition':'pending_audit','headRefOid':n['HEAD'],'baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952','entries':[{'id':'10400145'}]},{'number':955,'disposition':'eligible'}]
for path,obj in [(p/'CURRENT_STATE.json',state),(p/'inventory.json',inventory),(w/'TRACKER_RECEIPT.json',tracker),(w/'NATIVE_PUBLICATION_RECEIPT.json',native)]:n['save'](path,obj)
n['accepted_package']=lambda context:(accepted,freeze);n['merged_gate']=lambda *args:{};n['publication_links']=lambda *args:(pub,merge);n['independent_public_verify']=lambda *args:{'confirmed':True};n['descriptor_check']=lambda *args:({},[]);n['gws']=lambda *args:{'range':tracker['updated_range'],'values':[tracker['row']]};n['native_verify']=lambda *args:{'confirmed':True};n['accepted_review_check']=lambda *args:None;n['finalize_pr_metadata']=lambda *args:None;n['gate_next']=lambda *args:([],{'number':955,'problem_id':'SYNTHETIC_NEXT','headRefOid':'d'*40})
real=n['reconcile_local_finalization'];first=[True]
def interrupted(*args):
 result=real(*args)
 if first[0]:first[0]=False;raise OSError('INERT_INTERRUPT_AFTER_LOCAL_READBACK_BEFORE_MILESTONE_LOGS')
 return result
n['reconcile_local_finalization']=interrupted
try:n['finalize'](None,{})
except OSError as e:need(str(e)=='INERT_INTERRUPT_AFTER_LOCAL_READBACK_BEFORE_MILESTONE_LOGS','wrong window')
else:raise RuntimeError('expected first interruption')
capture=io.StringIO()
with contextlib.redirect_stdout(capture):n['finalize'](None,{})
result=json.loads(capture.getvalue());logs_unchanged=all(log.read_bytes()==sentinel for log in [p/'RESEARCH_LOG.md',a/'RESEARCH_LOG.md'])
need(result['local_finalization']['confirmed'] and logs_unchanged,'remaining log recovery gap not reproduced')
print(json.dumps({'status':'REPRODUCED_PROPOSAL04_LOG_COMPLETION_RECOVERY_GAP','actual_function':'finalize+reconcile_local_finalization+local_atomic_json','proposal_sha256':hashlib.sha256(raw).hexdigest(),'compile_optimization':0,'second_call_confirmed':result['local_finalization']['confirmed'],'target_already_completed':result['local_finalization']['target_already_completed'],'both_research_logs_remain_without_completion_entry':logs_unchanged,'state_inventory_repair_itself_succeeded':True,'scope':'Actual proposed local helper/read/write/fsync/rename and second finalize; explicit inert accepted/public/source/GWS/native/metadata/gate boundaries; one call-boundary interruption after actual consistent local readback before milestone appends. No real remote or production writes.'},sort_keys=True))
