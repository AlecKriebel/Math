from pathlib import Path
import hashlib,json,subprocess,datetime
H=Path(__file__).resolve().parent; A=H.parent; R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(p.read_text())
checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
manifestpaths=[('source_snapshot',A/'snapshot_manifest.json')]+[(d,A/d/'MANIFEST.json') for d in ['reviewed_candidate','primary_scope_family','complex_family','real_family','real_dependency_falsifier']]
entries=[]
for d,m in manifestpaths:
 for f in j(m)['files']:
  b=(A/d/f['path']).read_bytes();ck('finalbytes:'+d+'/'+f['path'],len(b)==f['bytes'] and sha(b)==f['sha256']);entries.append({'scope':d,**f})
ck('candidate23',sum(x['scope']=='reviewed_candidate' for x in entries)==23)
ck('candidate_manifest_binding',sha((A/'reviewed_candidate/MANIFEST.json').read_bytes())=='daeb6f57f65bea40d5392eaec732ba4e024af36653530458b6d1805396f408a1')
ck('candidate_source_binding',sha((A/'reviewed_candidate/SOURCE_AUDIT.md').read_bytes())=='cf775d9ed6ac85cecfb37a8b1f09e253b4eb5fd21681cf579bf987630f2a6569')
for f in j(A/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json')['supporting_first_party_files']:
 b=(R/f['path']).read_bytes();ck('dependency:'+f['path'],len(b)==f['bytes'] and sha(b)==f['sha256'])
early=j(H/'EARLY_SEAL.json')
for f in early['files']:
 b=(H/f['path']).read_bytes();ck('own_early_seal:'+f['path'],len(b)==f['bytes'] and sha(b)==f['sha256'])
baseline=j(H/'INTEGRITY_RECEIPTS.json')['canonical_baseline'];s=R/'unsolved_math_prioritization/state.json';h=R/'unsolved_math_prioritization/history.jsonl'
ck('existing_state_exactly_unchanged',sha(s.read_bytes())==baseline['state_sha256']);ck('existing_history_exactly_unchanged',sha(h.read_bytes())==baseline['history_sha256'])
state=j(s);history=[json.loads(x) for x in h.read_text().splitlines() if x.strip()];ck('no25accepted',not '2800102' in state and not any(str(x.get('id'))=='2800102' for x in history))
perstate=[{'id':k,'event_id':v['event_id'],'status':v['status'],'pr':v.get('pr'),'turns_used':v['turns_used'],'sha256_canonical_json':sha(json.dumps(v,sort_keys=True,separators=(',',':')).encode())} for k,v in sorted(state.items())]
perevent=[{'id':str(v.get('id')),'event_id':v.get('event_id'),'sha256_canonical_json':sha(json.dumps(v,sort_keys=True,separators=(',',':')).encode())} for v in history]
refs=[]
def checkrefs(node):
 if isinstance(node,dict):
  if isinstance(node.get('path'),str) and isinstance(node.get('sha256'),str):
   p=R/node['path'];ck('existing_accepted_evidence:'+node['path'],p.exists() and sha(p.read_bytes())==node['sha256']);refs.append({'path':node['path'],'sha256':node['sha256']})
  for value in node.values():checkrefs(value)
 elif isinstance(node,list):
  for value in node:checkrefs(value)
checkrefs(state)
q=R/'unsolved_math_prioritization/QUEUE.md';queue_rows=[x for x in q.read_text().splitlines() if '2800102 / AMR-027-0102' in x];ck('current_queue_single_row',len(queue_rows)==1 and '| queued | 0/5 |' in queue_rows[0]);diff=subprocess.check_output(['git','diff','--','unsolved_math_prioritization/QUEUE.md'],cwd=R);ck('current_shared_queue_no_working_diff',not diff)
pr=json.loads(subprocess.check_output(['gh','pr','view','25','--json','number,url,title,state,isDraft,headRefOid,headRefName,baseRefOid,body,files'],cwd=R));(H/'tmp/final_live_pr.json').write_text(json.dumps(pr,indent=2)+'\n');ck('final_remote_original_head',pr['headRefOid']=='aa99d4a36eff79cbb7aae55ce3ffe4a0eb31af95');ck('final_open_draft',pr['state']=='OPEN' and pr['isDraft']);ck('final_current_body',pr['body']==(A/'current_pr_body.md').read_text()==(A/'reviewed_candidate/pr_body.md').read_text());ck('final_remote17scope',{x['path'] for x in pr['files']}==set(j(A/'snapshot_manifest.json')['changed_paths']))
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':len(checks),'failed':0,'checks':checks,'input_manifests':[{'path':str(m.relative_to(R)),'sha256':sha(m.read_bytes())} for _,m in manifestpaths],'rechecked_entries':len(entries),'exact23_gate':True,'source_audit_sha256':sha((A/'reviewed_candidate/SOURCE_AUDIT.md').read_bytes()),'candidate_manifest_sha256':sha((A/'reviewed_candidate/MANIFEST.json').read_bytes()),'canonical_state_sha256':sha(s.read_bytes()),'canonical_history_sha256':sha(h.read_bytes()),'existing_state_entries':perstate,'existing_history_events':perevent,'accepted_evidence_reference_checks':len(refs),'canonical25_absent':True,'shared_queue_sha256':sha(q.read_bytes()),'current_shared_queue_row':queue_rows[0],'current_shared_queue_working_diff_sha256':sha(diff),'legacy_generator_sha256':sha((R/'unsolved_math_prioritization/queue.py').read_bytes()),'static_assessments_sha256':sha((R/'unsolved_math_prioritization/assessments.json').read_bytes()),'current_remote':{k:pr[k] for k in ['number','url','title','state','isDraft','headRefOid','headRefName','baseRefOid']},'body_sha256':sha(pr['body'].encode()),'remote_integration_or_current_accepted_mirror_completed_by_this_review':False,'parent_final_binding_still_required':True}
(H/'FINAL_GATE_RECEIPTS.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ['checks','existing_state_entries','existing_history_events']},indent=2))
