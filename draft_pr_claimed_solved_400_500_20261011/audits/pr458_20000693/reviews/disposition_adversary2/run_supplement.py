#!/usr/bin/env python3
"""Additional current-helper controls for exact first-failure and boundary mechanisms.

Uses this review's independent subprocess/model implementation. No old packet edits.
"""
import datetime,base64,json,shutil
from pathlib import Path
import run_controls as h
from audit_evidence import OWN,read,save,bind,need
original_change=h.change
names=['family_internal_readback_hash','classification_draft_hash','priority_gap_list','coverage_gap_list','source_count','source_pr_bool','metadata_pr_float','final_manifest_missing_report','final_manifest_self','final_manifest_parent','final_manifest_private','final_manifest_absolute','final_manifest_hash_type','evidence_empty','evidence_wrong_list_type','evidence_empty_path','evidence_zero_bytes','evidence_missing_hash','gate_object_bool','gate_approval_int','final_issue_bool','final_current_helper_int','final_pub_null','missing_final_result','source_wrong_problem_path','foundation_identity_float','foundation_count_float','frozen_original_resealed','malformed_moved_wrong_blob','uncertain_moved_wrong_blob','reconcile_ref_failure','ref_late_other_commit']

def change(n,program,case,state):
 g=read(case/h.GATE);s=read(state);guard='Canonical frozen foundation bytes differ'
 if n=='family_internal_readback_hash':h.json_change(case,'CLASSIFICATION_FAMILY_READBACK.json',lambda x:[r.update(sha256='0'*64) for r in x['safe_payloads'] if r['path'].endswith('/REPORT.md')])
 elif n=='classification_draft_hash':h.json_change(case,'reviews/classification_adversary/LATER_EXPOSURE_BINDINGS.json',lambda x:[r.update(sha256='0'*64) for r in x['files'] if r['path']=='DRAFT_PRIORITY_DISPOSITION.md'])
 elif n=='priority_gap_list':h.json_change(case,'reviews/priority_adversary/RESULT.json',lambda x:x['unresolved_mathematical_gaps'].pop())
 elif n=='coverage_gap_list':h.json_change(case,'reviews/priority_coverage/RESULT.json',lambda x:x['unresolved_mathematical_gaps'].pop())
 elif n=='source_count':h.json_change(case,'SOURCE_RECEIPT.json',lambda x:x['files'].pop())
 elif n=='source_pr_bool':h.json_change(case,'SOURCE_RECEIPT.json',lambda x:x.update(pr=True))
 elif n=='metadata_pr_float':h.json_change(case,'pr_metadata.json',lambda x:x.update(number=458.0))
 elif n.startswith('final_manifest_'):
  path='reviews/'+h.FAKE+'/PUBLIC_FILES.json';op=n[15:]
  if op=='missing_report':h.json_change(case,path,lambda x:x.update(files=[r for r in x['files'] if r['path']!='REPORT.md']));guard='Complete positive report/result packet required'
  elif op=='self':h.json_change(case,path,lambda x:x['files'].append({'path':'PUBLIC_FILES.json','bytes':1,'sha256':'0'*64}));guard='Complete public payload disconnected or drifted'
  elif op in ['parent','private','absolute']:
   val={'parent':'../REPORT.md','private':'private/a','absolute':'/tmp/a'}[op];h.json_change(case,path,lambda x:x['files'][0].update(path=val));guard='Manifest relative path' if op=='absolute' else 'Complete public payload disconnected or drifted'
  elif op=='hash_type':h.json_change(case,path,lambda x:x['files'][0].update(sha256=None),False);h.rebind_gate_only(case);guard='Manifest record byte/hash schema'
 elif n=='evidence_empty':g['reviewed_files']=[];save(case/h.GATE,g);guard='Empty evidence gate'
 elif n=='evidence_wrong_list_type':g['reviewed_files']={};save(case/h.GATE,g);guard='Empty evidence gate'
 elif n in ['evidence_empty_path','evidence_zero_bytes','evidence_missing_hash']:
  if n=='evidence_empty_path':g['reviewed_files'][0]['path']=''
  elif n=='evidence_zero_bytes':g['reviewed_files'][0]['bytes']=0
  else:g['reviewed_files'][0].pop('sha256')
  save(case/h.GATE,g);guard='Evidence entry type/byte/hash schema'
 elif n=='gate_object_bool':save(case/h.GATE,True);guard='Evidence JSON object required'
 elif n=='gate_approval_int':g['operations_approval']=1;save(case/h.GATE,g);guard='Final exact classification/helper gate absent'
 elif n in ['final_issue_bool','final_current_helper_int','final_pub_null']:
  k,v={'final_issue_bool':('unresolved_disposition_issues',False),'final_current_helper_int':('current_helper_accepted',1),'final_pub_null':('publication_accepted',None)}[n];h.json_change(case,'reviews/'+h.FAKE+'/RESULT.json',lambda x:x.update({k:v}));guard='Operations disposition issues' if n=='final_issue_bool' else 'Operations acceptance scope'
 elif n=='missing_final_result':(case/'reviews'/h.FAKE/'RESULT.json').unlink();guard='Evidence topology'
 elif n=='source_wrong_problem_path':h.json_change(case,'SOURCE_RECEIPT.json',lambda x:x['files'][0].update(path='unsolved_math_prioritization/attempts/other/README.md'))
 elif n in ['foundation_identity_float','foundation_count_float']:
  k,v=('pr',458.0) if n=='foundation_identity_float' else ('actual_foundation_reviews',8.0);h.json_change(case,'FROZEN_FOUNDATION_BINDINGS.json',lambda x:x.update({k:v}));guard='Canonical frozen foundation manifest changed'
 elif n=='frozen_original_resealed':
  p=case/'source_snapshot'/read(case/'SOURCE_RECEIPT.json')['files'][0]['path'];p.write_bytes(p.read_bytes()+b' ');r=read(case/'SOURCE_RECEIPT.json');r['files'][0].update(bind(p));save(case/'SOURCE_RECEIPT.json',r);h.rebind(case)
 elif n in ['malformed_moved_wrong_blob','uncertain_moved_wrong_blob']:
  s['config']={'wrong_blob':True,'patch_raw':'{'} if n.startswith('malformed') else {'wrong_blob':True,'patch_fail':True};guard='QUEUE blob exact bytes differ'
 elif n=='reconcile_ref_failure':s['config']={'patch_fail':True,'ref_stage':4};guard='Branch update uncertain; no retry'
 elif n=='ref_late_other_commit':s['config']={'ref_stage':4};guard='Branch readback differs'
 else:raise RuntimeError('unknown supplement')
 save(state,s);return True,False,guard
h.change=change

def main():
 root=OWN/'private/supplement';need(not root.exists(),'preserve raw');root.mkdir();rows=[];repeats=[]
 for mode in ['normal','optimized']:
  for i,n in enumerate(names):
   r,rep=h.execute(root/(mode+'_'+str(i)),n,mode,i);rows.append(r)
   if rep:repeats.append(rep)
   save(root/'PARTIAL_RESULTS.json',{'runs':rows,'repeat_runs':repeats})
   if r['outcome']!='intended_rejection':print(json.dumps(r),flush=True)
 save(OWN/'SUPPLEMENT_CONTROLS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'case_count_per_mode':len(names),'executions':len(rows),'runs':rows,'repeats':repeats,'all_private_hypothetical':True,'summary':{m:{o:sum(r['mode']==m and r['outcome']==o for r in rows) for o in ['intended_rejection','unexpected_acceptance','wrong_guard_or_harness_failure']} for m in ['normal','optimized']}})
 print('supplement actual executions',len(rows))
if __name__=='__main__':main()
