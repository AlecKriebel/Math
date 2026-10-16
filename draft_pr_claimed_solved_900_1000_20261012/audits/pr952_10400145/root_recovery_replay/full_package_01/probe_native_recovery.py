import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise RuntimeError('isolated required')
from pathlib import Path
import tempfile,json,hashlib,datetime,sqlite3
O=Path(__file__).resolve().parent;A=O.parents[1];P=A.parents[2]/'draft_pr_claimed_solved_900_1000_20261012';CORE=P/'accept_pr952.py';raw=CORE.read_bytes()
def need(ok,label):
 if not ok:raise RuntimeError(label)
need(hashlib.sha256(raw).hexdigest()=='854a8694e3b4b46d3eff32f207729d2637c262b9714d8a7b052289450831e908','core pin')
n={'__name__':'_explicit_reviewer_inert_native_recovery_','__file__':str(CORE)};exec(compile(raw,str(CORE),'exec',dont_inherit=True,optimize=0),n)
# The real native_write, merged_gate/_merged_gate, source_gate and native_safety
# execute. Explicit substitutions below provide inert remote Git/PR observations
# and the already separately validated acceptance/original metadata boundary.
# No production code/constant is changed and no mutation method can reach Git.
private=O/'private_native_recovery';private.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(dir=private) as td:
 root=Path(td);audit=root/'audit';audit.mkdir();workflow=root/'workflow';workflow.mkdir();n.update(ROOT=root,A=audit,W=workflow,READ_ONLY=True)
 (audit/'source_record_private.txt').write_bytes((A/'source_record_private.txt').read_bytes());source=json.loads((A/'source_record_private.txt').read_bytes());cache=root/'unsolved_math_prioritization/cache';cache.mkdir(parents=True)
 with sqlite3.connect(cache/'catalog.sqlite') as c:c.execute('CREATE TABLE records(key TEXT,payload TEXT,report TEXT)');c.execute('INSERT INTO records VALUES(?,?,?)',(n['KEY'],json.dumps(source['problem']),json.dumps(source['prior_research'])))
 parent='c'*40;merge='b'*40;native='d'*40;oldparent='a'*40;freeze={'files':{}};accepted={'freeze_sha256':'f'*64}
 pr={'number':952,'state':'MERGED','isDraft':False,'headRefOid':n['HEAD'],'headRefName':'inert','baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952','mergeCommit':{'oid':merge},'mergedAt':'2026-10-16T00:00:00Z','currentBaseRefOid':parent}
 n['save'](workflow/'PR_MERGE_RECEIPT.json',pr,exclusive=True)
 event=n['native_event'](accepted,{'id':17,'doi':'10.5281/zenodo.17','record_url':'https://zenodo.org/records/17'},pr,{'updated_range':"'Math Puzzles'!A2:D2"})
 q=b'| 10400145 / AMR-103-0145 | b | c | d | e | f | g | claimed_solved | 1/5 | j | old | old |\n'
 blobs={n['CATALOG']:json.dumps([{'id':10400145,'present':True,'holds':[],'statement_hash':n['STATEMENT'],'review_hash':n['REVIEW']}]).encode(),n['RELATED']:b'{"groups":[]}',n['STATE']:json.dumps({n['KEY']:event}).encode(),n['HISTORY']:(json.dumps(event)+'\n').encode(),n['QUEUE']:q}
 n['blob']=lambda ref,path:blobs[path];n['pr_view']=lambda *a:dict(pr);n['remote_main']=lambda:parent;n['original_check']=lambda *a:{'EXPLICIT_INERT_ORIGINAL_BOUNDARY':'passed elsewhere, no Git write'};n['accepted_package']=lambda context:(accepted,freeze)
 calls=[]
 def inert_run(args,**kwargs):
  calls.append(args)
  if args[:3]==['git','merge-base','--is-ancestor']:return ''
  if args[:5]==['git','show','-s','--format=%P',merge]:return oldparent+' '+n['HEAD']
  raise RuntimeError('NO REAL COMMAND: '+repr(args))
 n['run']=inert_run
 # Exact matching planned/prepared receipts, a known successful native commit
 # on remote main, and no final receipt reproduce the lost-readback window.
 n['save'](workflow/'NATIVE_PUBLICATION_CAS_01_INTENT.json',{'parent':oldparent,'published_event':event,'accepted_freeze_sha256':accepted['freeze_sha256'],'attempt':1},exclusive=True)
 n['save'](workflow/'NATIVE_PUBLICATION_CAS_01_PREPARED.json',{'parent':oldparent,'commit':native,'published_event':event,'accepted_freeze_sha256':accepted['freeze_sha256'],'attempt':1},exclusive=True)
 # Directly demonstrate the specific exact-commit ancestry query would pass.
 need(inert_run(['git','merge-base','--is-ancestor',native,parent])=='','ancestry positive control');calls.clear()
 try:n['native_write'](None,{})
 except RuntimeError as error:rejected=str(error)
 else:raise RuntimeError('Unexpected success; revise reproduction')
 before_recovery=not any(native in args for args in calls)
 need(before_recovery and 'current native target/history differs' in rejected,'reproduced early native-safety blockage')
 print(json.dumps({'schema':'pr952-full01-native-recovery-reproduction-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'finding_id':'R952-FULL01-OPS-01','outer_optimization':sys.flags.optimize,'status':'REPRODUCED_REQUIRED_OPERATIONAL_GAP','observed_error':rejected,'actual_functions_executed':['native_write','merged_gate','_merged_gate','source_gate','native_safety'],'explicit_substitutions':['accepted_package: prevalidated synthetic acceptance only','original_check: separately tested original boundary','pr_view/remote_main/blob/run: inert immutable service/Git observations'],'prepared_matching_commit_present':True,'publication_receipt_absent':True,'remote_state_exactly_expected_event':True,'same_commit_ancestry_would_pass':True,'failed_before_exact_native_commit_reconciliation':before_recovery,'inert_git_queries':calls,'real_Git_or_service_calls':0,'production_edits':0,'private_body_output':False},sort_keys=True))
