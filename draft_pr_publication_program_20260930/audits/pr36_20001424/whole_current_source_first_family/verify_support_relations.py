#!/usr/bin/env python3
"""Check exact frozen diff payloads, root streams and scalar comparison provenance.
No Git/live data actions; all inputs are bound frozen first-party artifacts.
"""
from pathlib import Path
import json,hashlib,re,datetime
A=Path(__file__).resolve().parent.parent
P=A/'reviewed_candidate'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def need(ok,msg):
 if not ok:raise ValueError(msg)
def main():
 sm=load(A/'snapshot_manifest.json');diff=(A/'pr_input/diff.patch').read_text();chunks=re.split(r'(?=^diff --git )',diff,flags=re.M);paths=[];payloads=[];queue=[]
 for ch in chunks:
  if not ch:continue
  first=ch.splitlines()[0];m=re.fullmatch(r'diff --git a/(.+) b/(.+)',first);need(m and m[1]==m[2],'path header');path=m[1];paths.append(path)
  added=''.join(line[1:] for line in ch.splitlines(True) if line.startswith('+') and not line.startswith('+++'))
  if '/attempts/20001424/' in path:
   rel=path.split('/attempts/20001424/')[1];b=(P/'original_archive'/rel).read_bytes();need(added.encode()==b,'diff complete added payload '+rel);payloads.append(rel)
  else:
   need(path=='unsolved_math_prioritization/QUEUE.md','unrelated original diff path');queue=[x for x in ch.splitlines() if x.startswith(('+|','-|'))];need(len(queue)==2,'queue exact old/new row count')
 need(len(paths)==17 and paths==sm['changed_paths'] and len(payloads)==16,'17 exact changed paths')
 q=load(P/'CURRENT_QUEUE_PATCH.json');need(queue[0][1:]+'\n'==q['row_before'],'current queue named row has exact original preimage');need(queue[1][1:].split('|')[8].strip()=='claimed_solved','dated archival queue conclusion')
 root=load(P/'root_verification/ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json');need(len(root['actual_outer_program_runs'])==28,'root28');retained=load(A/'root_actual_replay/ACTUAL_RUNS.json');need(retained==root['actual_outer_program_runs'],'retained actual runs exact')
 streamchecks=[]
 for row in root['actual_outer_program_runs']:
  for ext in ['stdout','stderr']:
   p=A/'root_actual_replay/streams'/(row['label']+'.'+ext);need(sha(p.read_bytes())==row[ext+'_sha256'],'retained complete stream '+p.name)
  need(row['exit']==row['expected_exit'],'root program status '+row['label']);streamchecks.append(row['label'])
 comparisons=[]
 for row in root['full_structured_receipt_comparisons']:
  old=A/row['file'];new=A/'root_actual_replay/receipts'/row['file'];need(sha(old.read_bytes())==row['original_sha256'],'comparison old pin');need(sha(new.read_bytes())==row['actual_sha256'],'comparison fresh pin');comparisons.append(row['file'])
 # Dated manifest controls cannot be identical input; verify the exact changed fields.
 old=load(A/'arithmetic_graph_priority_family/AUTHORED_MANIFEST_CONTROL_RESULTS.json');fresh=load(A/'root_actual_replay/receipts/arithmetic_graph_priority_family/AUTHORED_MANIFEST_CONTROL_RESULTS.json')
 def nou(x):
  if isinstance(x,dict):return {k:nou(v) for k,v in x.items() if k!='utc'}
  if isinstance(x,list):return [nou(v) for v in x]
  return x
 old=nouse=nou(old);fresh=nou(fresh)
 differences=[]
 for i,(x,y) in enumerate(zip(old['actual_controls'],fresh['actual_controls'])):
  need(x['actual_accept']==y['actual_accept'] and x['correct_result']==y['correct_result'],'dated accept/reject')
  if i in [0,6]:
   need(x['observed']['authored_file_count']==15 and y['observed']['authored_file_count']==18,'dated15 versus current18')
   need(x['observed']['sha256_of_manifest']!=y['observed']['sha256_of_manifest'],'dated different manifest')
   z=dict(y['observed']);z['authored_file_count']=15;z['sha256_of_manifest']=x['observed']['sha256_of_manifest'];need(z==x['observed'],'other dated fields');differences.append(i)
  else:need(x==y,'other negative manifest controls')
 need(differences==[0,6],'exact dated controls scope')
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_WITH_SCOPE','original17_diff_paths_verified':paths,'original16_complete_added_payloads_equal':payloads,'queue_original_preimage_equals_current_named_preimage':True,'full56_root_stream_hashes_rederived':streamchecks,'root28_actual_commands_table_equal':True,'full13_comparison_original_and_retained_hashes_rederived':comparisons,'dated_manifest_actual_observation':'Two positive controls changed input manifest15 to18; all seven acceptance/rejection outcomes and all other fields match. This is not identical-input reproduction.','root_later_integration_requirement':'Whole queue preimage/prospective bytes absent from package. Root must guard actual live whole preimage or create a separately receipted named-row rebase before integration.','new_substantive_attempts':0}
 dest=Path(__file__).with_name('SUPPORT_RELATION_RESULTS.json');dest.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('original17_diff_paths_verified','original16_complete_added_payloads_equal','full56_root_stream_hashes_rederived','full13_comparison_original_and_retained_hashes_rederived')},indent=2))
if __name__=='__main__':main()
