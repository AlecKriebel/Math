#!/usr/bin/env python3
"""Offline scope controls. No GitHub/service or mathematics call is allowed."""
import contextlib,copy,hashlib,io,json,sys,tempfile
from datetime import datetime,timezone
from pathlib import Path
P=Path(__file__).resolve().parent
SOURCE=P/'resweep_draft_statuses_900_1000.py'

def main():
 n={'__file__':str(SOURCE),'__name__':'_scope_controls_'}
 raw=SOURCE.read_bytes();exec(compile(raw,str(SOURCE),'exec'),n)
 def forbidden(*args,**kwargs):raise AssertionError('Unexpected live operation')
 n['run']=forbidden
 tests=[]
 def check(label,fn):
  fn();tests.append({'name':label,'status':'PASS'})
 def need(ok):
  if not ok:raise AssertionError('Control expectation failed')
 def rejects(fn):
  try:fn()
  except RuntimeError:return
  raise AssertionError('Expected closed rejection')
 pr={'number':952,'state':'OPEN','isDraft':True,'headRefOid':'1'*40,'headRefName':'draft/example','baseRefName':'main','baseRefOid':'a'*40,'currentBaseRefOid':'a'*40,'baseRef':{'target':{'oid':'a'*40}},'url':'https://github.com/AlecKriebel/Math/pull/952'}
 old={'headRefOid':'0'*40,'baseRefOid':'a'*40,'currentBaseRefOid':'a'*40,'entries':[{'id':'1'}]}
 def node(paths,count=None,more=False,cursor=None,**changed):
  return {**pr,'changedFiles':len(paths) if count is None else count,'files':{'nodes':[{'path':p} for p in paths],'pageInfo':{'hasNextPage':more,'endCursor':cursor}},**changed}
 def feed(pages):
  it=iter(copy.deepcopy(pages));n['graphql']=lambda *a,**k:{'pullRequest':next(it)}
 def identity(paths):
  feed([node(paths)]);return n['current_identity'](pr,old)
 def row(key,status):return '| 1 | '+key+' / SOURCE | Title | 0 | 0 | 0 | 2020 | '+status+' | 4/5 | | | |'
 check('unchanged_head_uses_original_ID_without_filename_call',lambda:(n.update(graphql=forbidden),need(n['current_identity'](pr,{**old,'headRefOid':pr['headRefOid']})['problem_id']=='1')))
 check('changed_head_derives_new_ID',lambda:need(identity(['unsolved_math_prioritization/attempts/2/proof.md'])['problem_id']=='2'))
 check('ambiguous_changed_IDs_unresolved',lambda:need(not identity(['unsolved_math_prioritization/attempts/2/a','unsolved_math_prioritization/attempts/3/b'])['identity_reconciled']))
 check('missing_attempt_ID_unresolved',lambda:need(not identity(['README.md'])['identity_reconciled']))
 for label,base in [('missing',None),('malformed','bad'),('different','b'*40)]:
  def no_reuse(base=base):
   feed([node(['unsolved_math_prioritization/attempts/2/a'])])
   initial={**old,'headRefOid':pr['headRefOid'],'currentBaseRefOid':base}
   need(n['current_identity'](pr,initial)['problem_id']=='2')
  check('same_head_'+label+'_initial_base_derives_current_ID',no_reuse)
 def paged():
  a=['misc/f'+str(i) for i in range(100)];feed([node(a,101,True,'next'),node(['unsolved_math_prioritization/attempts/2/a'],101)])
  need(n['current_identity'](pr,old)['problem_id']=='2')
 check('complete_two_page_filename_positive',paged)
 for label,pages in [
  ('incomplete_count_reject',[node(['a'],2)]),
  ('duplicate_paths_reject',[node(['a','a'],2)]),
  ('head_race_reject',[node(['a'],headRefOid='2'*40)]),
  ('base_only_page_race_reject',[node(['a'],baseRefOid='b'*40)]),
  ('base_missing_page_reject',[node(['a'],baseRefOid=None)]),
  ('base_malformed_page_reject',[node(['a'],baseRefOid='bad')]),
  ('draft_race_reject',[node(['a'],isDraft=False)]),
  ('count_boolean_reject',[node(['a'],True)]),
  ('noncanonical_path_reject',[node(['a/../b'])]),
  ('path_extra_key_reject',[{**node(['a']),'files':{'nodes':[{'path':'a','contents':'forbidden'}],'pageInfo':{'hasNextPage':False,'endCursor':None}}}]),
  ('missing_cursor_reject',[node(['a'],2,True,None)]),
  ('repeated_cursor_reject',[node(['a'],3,True,'x'),node(['b'],3,True,'x')]),
  ('changed_count_reject',[node(['a'],2,True,'x'),node(['b'],3)]),
 ]:
  def exercise(pages=pages):feed(pages);rejects(lambda:n['changed_paths'](pr))
  check(label,exercise)
 for status in ['claimed_solved','already_solved','unsolved','queued','CLAIMED_SOLVED','claimed_solved_extra']:
  check('literal_status_'+status,lambda status=status:need(n['target_status'](row('2',status),'2')['status']==status))
 check('ambiguous_queue_rows_reject',lambda:rejects(lambda:n['target_status'](row('2','unsolved')+'\n'+row('2','claimed_solved'),'2')))
 queue=row('2','claimed_solved');b=queue.encode();obj={'__typename':'Blob','isBinary':False,'text':queue,'byteSize':len(b),'oid':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
 def queue_reply(value):n['graphql']=lambda *a,**k:{'object':copy.deepcopy(value)}
 check('immutable_queue_blob_positive',lambda:(queue_reply(obj),need(n['immutable_queue']('1'*40)==queue)))
 for label,patch in [('wrong_oid',{'oid':'0'*40}),('wrong_size',{'byteSize':len(b)+1}),('unknown_binary',{'isBinary':None}),('not_blob',{'__typename':'Tree'})]:
  check('immutable_queue_'+label+'_reject',lambda patch=patch:(queue_reply({**obj,**patch}),rejects(lambda:n['immutable_queue']('1'*40))))
 check('duplicate_json_key_reject',lambda:rejects(lambda:n['strict_json']('{"x":1,"x":2}')))
 check('nonfinite_json_reject',lambda:rejects(lambda:n['strict_json']('{"x":NaN}')))
 # Actual live branch target is distinct from associated PR baseRefOid.
 check('normalize_live_target_ignores_spoofed_flattened_field',lambda:need(n['normalize_metadata']({**pr,'currentBaseRefOid':'f'*40})['currentBaseRefOid']=='a'*40))
 for label,base in [('null',None),('missing',{}),('malformed',{'target':{'oid':'bad'}})]:
  def bad_live(base=base):
   feed([node(['a'],baseRef=base)])
   rejects(lambda:n['changed_paths'](pr))
  check('live_base_'+label+'_page_reject',bad_live)
 check('stored_base_unchanged_live_pointer_page_race_reject',lambda:(feed([node(['a'],baseRef={'target':{'oid':'b'*40}})]),rejects(lambda:n['changed_paths'](pr))))
 def stored_only_initial():
  initial={**old,'headRefOid':pr['headRefOid']};initial.pop('currentBaseRefOid')
  feed([node(['unsolved_math_prioritization/attempts/2/a'])])
  need(n['current_identity'](pr,initial)['problem_id']=='2')
 check('matching_stored_base_without_original_live_pin_derives',stored_only_initial)
 def stable_live_advance():
  current={**pr,'currentBaseRefOid':'b'*40,'baseRef':{'target':{'oid':'b'*40}}}
  feed([node(['unsolved_math_prioritization/attempts/2/a'],baseRef=current['baseRef'])])
  need(n['current_identity'](current,{**old,'headRefOid':pr['headRefOid']})['problem_id']=='2')
 check('stable_live_advance_same_head_and_stored_base_derives',stable_live_advance)
 check('fresh_live_base_missing_reject',lambda:rejects(lambda:n['current_identity']({**pr,'currentBaseRefOid':None},old)))
 # Exercise the actual entire range controller against fake service metadata.
 def whole_scan(drift=False,read_failure=False,eligible=True,base_drift=False,live_base_drift=False):
  with tempfile.TemporaryDirectory(prefix='scope-controls-',dir=P) as folder:
   d=Path(folder);inventory=[];first={}
   for number in range(900,1001):
    initial={**pr,'number':number,'headRefOid':str(number).zfill(40),'state':'CLOSED','isDraft':True};first[number]=initial
    inventory.append({**initial,'entries':[{'id':str(number)}]})
   for number in range(900,906):first[number]['state']='OPEN'
   (d/'inventory.json').write_text(json.dumps(inventory))
   second=copy.deepcopy(first)
   if drift:second[904]['headRefOid']='f'*40
   if base_drift:second[904]['baseRefOid']='b'*40
   if live_base_drift:second[904]['currentBaseRefOid']='b'*40;second[904]['baseRef']={'target':{'oid':'b'*40}}
   snapshots=iter([first,second]);n.update(P=d,metadata=lambda:copy.deepcopy(next(snapshots)),changed_paths=forbidden,run=forbidden)
   statuses={900:'already_solved',901:'unsolved',902:'queued',903:'CLAIMED_SOLVED',904:'claimed_solved' if eligible else 'unsolved',905:'claimed_solved_extra'}
   def read(head):
    number=int(head)
    if read_failure and number==901:raise RuntimeError('Synthetic unreadable queue')
    return row(str(number),statuses[number])
   n['immutable_queue']=read;previous=sys.argv[:];sys.argv=[str(SOURCE),'--receipt-name','receipt.json']
   try:
    with contextlib.redirect_stdout(io.StringIO()):n['main']()
   finally:sys.argv=previous
   result=json.loads((d/'receipt.json').read_bytes())
   need(result['pr_count']==101 and not result['source_math_artifact_reads_or_remote_mutations'])
   need([r['pr'] for r in result['eligible_remaining']]==([904] if eligible else []))
   need(result['metadata_stable_across_scan']==(not (drift or base_drift or live_base_drift)))
   need(result['completion_scope_clear']==(not (drift or base_drift or live_base_drift or read_failure or eligible)))
   need(bool(result['unresolved_identities'])==read_failure)
   for r in result['rows']:need(not r['math_or_source_or_artifact_read'] and not r['remote_mutation'])
 check('actual_101_PR_controller_exact_status_scope',whole_scan)
 check('metadata_drift_prevents_final_scope_clear',lambda:whole_scan(drift=True))
 check('read_error_is_unresolved_never_scope_clear',lambda:whole_scan(read_failure=True))
 check('all_excluded_scope_clears_without_math',lambda:whole_scan(eligible=False))
 check('base_only_end_snapshot_drift_blocks_scope_clear',lambda:whole_scan(eligible=False,base_drift=True))
 check('live_base_only_end_snapshot_drift_blocks_scope_clear',lambda:whole_scan(eligible=False,live_base_drift=True))
 out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','passed':len(tests),'failed':0,'source_sha256':hashlib.sha256(raw).hexdigest(),'live_service_calls':0,'scope':'Offline status-selector controls only, not an actual final live range sweep. All transient fake range fixtures removed. Frozen PR948 candidate unchanged.','tests':tests}
 target=P/'FINAL_STATUS_SWEEP_OFFLINE_CONTROLS_20261016_03.json'
 with target.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
 print(json.dumps({k:out[k] for k in ['utc','status','passed','failed','source_sha256','live_service_calls']}))

if __name__=='__main__':main()
